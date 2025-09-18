# backend.py - FastAPI Backend for Video Analysis & Summarizer Agent

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import os
import tempfile
import requests
import re
from datetime import datetime
import uuid

# LangChain and OpenAI imports
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Video processing imports
import pytube
from moviepy.editor import VideoFileClip
import speech_recognition as sr

# NLP and sentiment analysis
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Environment variables
from dotenv import load_dotenv
load_dotenv()

# Download required NLTK data
nltk.download('vader_lexicon', quiet=True)

# Initialize FastAPI app
app = FastAPI(title="Video Summarizer API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
summary_storage = []  # In-memory storage for demo
sentiment_analyzer = SentimentIntensityAnalyzer()

# Pydantic models
class SummaryRequest(BaseModel):
    url: Optional[str] = None
    format: str = "bullet_points"  # bullet_points, narrative, markdown
    length: str = "medium"  # short, medium, long
    language: str = "english"
    include_sentiment: bool = False

class SummaryResponse(BaseModel):
    id: str
    summary: str
    metadata: dict
    transcript: str
    sentiment: Optional[dict] = None
    keywords: Optional[List[str]] = None
    timestamp: str

# Helper functions
def extract_video_id(url: str) -> str:
    """Extract video ID from YouTube URL"""
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    raise ValueError("Invalid YouTube URL")

def get_video_metadata(video_id: str) -> dict:
    """Get video metadata using pytube"""
    try:
        yt = pytube.YouTube(f"https://www.youtube.com/watch?v={video_id}")
        return {
            "title": yt.title,
            "author": yt.author,
            "length": yt.length,
            "views": yt.views,
            "thumbnail": yt.thumbnail_url,
            "publish_date": str(yt.publish_date) if yt.publish_date else None
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching metadata: {str(e)}")

def extract_youtube_transcript(video_id: str) -> str:
    """Extract transcript from YouTube video"""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([item['text'] for item in transcript_list])
        return transcript
    except Exception as e:
        # Fallback to audio extraction and speech recognition
        return extract_audio_transcript(f"https://www.youtube.com/watch?v={video_id}")

def extract_audio_transcript(video_path: str) -> str:
    """Extract transcript from video file using speech recognition"""
    try:
        # Extract audio from video
        video = VideoFileClip(video_path)
        audio_path = tempfile.mktemp(suffix=".wav")
        video.audio.write_audiofile(audio_path, verbose=False, logger=None)
        
        # Convert audio to text
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
            transcript = recognizer.recognize_google(audio)
        
        # Cleanup
        os.remove(audio_path)
        video.close()
        
        return transcript
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error extracting transcript: {str(e)}")

def analyze_sentiment(text: str) -> dict:
    """Analyze sentiment of text using VADER"""
    scores = sentiment_analyzer.polarity_scores(text)
    
    # Determine overall sentiment
    if scores['compound'] >= 0.05:
        overall = 'positive'
    elif scores['compound'] <= -0.05:
        overall = 'negative'
    else:
        overall = 'neutral'
    
    return {
        'overall': overall,
        'positive': scores['pos'],
        'negative': scores['neg'],
        'neutral': scores['neu'],
        'compound': scores['compound']
    }

def extract_keywords(text: str) -> List[str]:
    """Extract keywords from text using regex and common word filtering"""
    import collections
    
    # Simple keyword extraction (can be enhanced with more sophisticated NLP)
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    
    # Filter out common stop words
    stop_words = {'this', 'that', 'with', 'have', 'will', 'from', 'they', 'been', 
                  'were', 'said', 'each', 'which', 'their', 'time', 'about', 'would', 
                  'there', 'could', 'other', 'more', 'very', 'what', 'know', 'just'}
    
    filtered_words = [word for word in words if word not in stop_words and len(word) > 4]
    
    # Get most common keywords
    word_freq = collections.Counter(filtered_words)
    keywords = [word for word, freq in word_freq.most_common(10)]
    
    return keywords

def get_summary_prompt(format_type: str, length: str, language: str) -> str:
    """Generate appropriate prompt based on parameters"""
    
    format_instructions = {
        'bullet_points': "Provide the summary in clear bullet points",
        'narrative': "Write the summary as a flowing narrative story",
        'markdown': "Format the summary using markdown with appropriate headings and structure"
    }
    
    length_instructions = {
        'short': "Keep the summary concise, around 100-150 words",
        'medium': "Provide a comprehensive summary of 200-300 words", 
        'long': "Create a detailed summary of 400-500 words"
    }
    
    prompt = f"""
    Please summarize the following video transcript. 
    
    Format: {format_instructions.get(format_type, format_instructions['bullet_points'])}
    Length: {length_instructions.get(length, length_instructions['medium'])}
    Language: Please provide the summary in {language}
    
    Focus on the main topics, key insights, and important information covered in the video.
    
    Transcript: {{transcript}}
    
    Summary:
    """
    
    return prompt

def generate_summary(transcript: str, format_type: str = "bullet_points", 
                    length: str = "medium", language: str = "english") -> str:
    """Generate summary using OpenAI via LangChain"""
    try:
        # Initialize ChatOpenAI
        llm = ChatOpenAI(
            openai_api_key=os.getenv('OPENAI_API_KEY'),
            model_name="gpt-3.5-turbo",
            temperature=0.3
        )
        
        # Create prompt
        prompt_template = PromptTemplate(
            input_variables=["transcript"],
            template=get_summary_prompt(format_type, length, language)
        )
        
        # Create chain
        chain = LLMChain(llm=llm, prompt=prompt_template)
        
        # Generate summary
        summary = chain.run(transcript=transcript)
        
        return summary.strip()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")

# API Endpoints
@app.post("/summarize", response_model=SummaryResponse)
async def summarize_video(request: SummaryRequest):
    """Main endpoint to summarize video from URL"""
    
    if not request.url:
        raise HTTPException(status_code=400, detail="URL is required")
    
    try:
        # Extract video ID and get metadata
        video_id = extract_video_id(request.url)
        metadata = get_video_metadata(video_id)
        
        # Extract transcript
        transcript = extract_youtube_transcript(video_id)
        
        # Generate summary
        summary = generate_summary(
            transcript, 
            request.format, 
            request.length, 
            request.language
        )
        
        # Optional sentiment analysis
        sentiment = None
        if request.include_sentiment:
            sentiment = analyze_sentiment(transcript)
        
        # Extract keywords
        keywords = extract_keywords(transcript)
        
        # Create response
        response = SummaryResponse(
            id=str(uuid.uuid4()),
            summary=summary,
            metadata=metadata,
            transcript=transcript,
            sentiment=sentiment,
            keywords=keywords,
            timestamp=datetime.now().isoformat()
        )
        
        # Store in memory (replace with database in production)
        summary_storage.append(response.dict())
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize/upload", response_model=SummaryResponse)
async def summarize_uploaded_video(
    file: UploadFile = File(...),
    format: str = "bullet_points",
    length: str = "medium", 
    language: str = "english",
    include_sentiment: bool = False
):
    """Summarize uploaded video file"""
    
    if not file.filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        raise HTTPException(status_code=400, detail="Unsupported file format")
    
    try:
        # Save uploaded file temporarily
        temp_path = tempfile.mktemp(suffix=os.path.splitext(file.filename)[1])
        
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Extract transcript from video file
        transcript = extract_audio_transcript(temp_path)
        
        # Generate summary
        summary = generate_summary(transcript, format, length, language)
        
        # Optional sentiment analysis
        sentiment = None
        if include_sentiment:
            sentiment = analyze_sentiment(transcript)
        
        # Extract keywords
        keywords = extract_keywords(transcript)
        
        # Create metadata for uploaded file
        metadata = {
            "title": file.filename,
            "file_size": len(content),
            "file_type": file.content_type
        }
        
        # Create response
        response = SummaryResponse(
            id=str(uuid.uuid4()),
            summary=summary,
            metadata=metadata,
            transcript=transcript,
            sentiment=sentiment,
            keywords=keywords,
            timestamp=datetime.now().isoformat()
        )
        
        # Store in memory
        summary_storage.append(response.dict())
        
        # Cleanup
        os.remove(temp_path)
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/summaries/{summary_id}")
async def get_summary(summary_id: str):
    """Get specific summary by ID"""
    for summary in summary_storage:
        if summary['id'] == summary_id:
            return summary
    raise HTTPException(status_code=404, detail="Summary not found")

@app.get("/summaries")
async def get_all_summaries():
    """Get all stored summaries"""
    return summary_storage

@app.delete("/summaries/{summary_id}")
async def delete_summary(summary_id: str):
    """Delete specific summary"""
    global summary_storage
    summary_storage = [s for s in summary_storage if s['id'] != summary_id]
    return {"message": "Summary deleted"}

@app.get("/download/{summary_id}")
async def download_summary(summary_id: str, format: str = "txt"):
    """Download summary in specified format"""
    
    summary = None
    for s in summary_storage:
        if s['id'] == summary_id:
            summary = s
            break
    
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    
    # Create temporary file with summary content
    temp_path = tempfile.mktemp(suffix=f".{format}")
    
    content = f"""Title: {summary['metadata'].get('title', 'N/A')}
Generated: {summary['timestamp']}

Summary:
{summary['summary']}

Keywords: {', '.join(summary.get('keywords', []))}
"""
    
    if summary.get('sentiment'):
        content += f"\nSentiment: {summary['sentiment']['overall']} (Score: {summary['sentiment']['compound']:.2f})"
    
    with open(temp_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return FileResponse(
        temp_path, 
        filename=f"summary_{summary_id}.{format}",
        media_type='application/octet-stream'
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
