# frontend.py - Streamlit Frontend for Video Analysis & Summarizer Agent

import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime
import base64
import io
import matplotlib.pyplot as plt
import plotly.express as px
from typing import Dict, List, Optional

# Configure Streamlit page
st.set_page_config(
    page_title="Video Analysis & Summarizer Agent",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding-top: 1rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Backend API URL (adjust as needed)
API_BASE_URL = "http://localhost:8000"

# Helper functions
def extract_video_id(url: str) -> str:
    """Extract video ID from YouTube URL for thumbnail display"""
    import re
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_thumbnail_url(video_id: str) -> str:
    """Get YouTube thumbnail URL"""
    return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

def create_sentiment_chart(sentiment_data: Dict) -> plt.Figure:
    """Create a pie chart for sentiment analysis"""
    if not sentiment_data:
        return None
    
    labels = ['Positive', 'Neutral', 'Negative']
    sizes = [
        sentiment_data.get('positive', 0),
        sentiment_data.get('neutral', 0), 
        sentiment_data.get('negative', 0)
    ]
    colors = ['#4CAF50', '#FFC107', '#F44336']
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.set_title('Sentiment Analysis Distribution')
    return fig

def display_video_info(metadata: Dict):
    """Display video metadata in a nice format"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Views", f"{metadata.get('views', 'N/A'):,}" if isinstance(metadata.get('views'), int) else "N/A")
    
    with col2:
        length = metadata.get('length', 0)
        if isinstance(length, int):
            minutes = length // 60
            seconds = length % 60
            st.metric("Duration", f"{minutes}:{seconds:02d}")
        else:
            st.metric("Duration", "N/A")
    
    with col3:
        st.metric("Author", metadata.get('author', 'N/A'))
    
    with col4:
        publish_date = metadata.get('publish_date', 'N/A')
        if publish_date != 'N/A':
            try:
                date_obj = datetime.fromisoformat(publish_date.replace('Z', '+00:00'))
                st.metric("Published", date_obj.strftime('%Y-%m-%d'))
            except:
                st.metric("Published", "N/A")
        else:
            st.metric("Published", "N/A")

# Initialize session state
if 'summary_history' not in st.session_state:
    st.session_state.summary_history = []

# Main app layout
st.title("🎥 Ultimate Video Summarizer Agent")
st.markdown("**AI-Powered Video Analysis and Summarization with Advanced Features**")

# Sidebar for navigation and settings
with st.sidebar:
    st.header("📋 Navigation")
    page = st.selectbox(
        "Choose Action:",
        ["Summarize Video", "History", "Settings"]
    )
    
    st.header("⚙️ Advanced Settings")
    
    # Summary format options
    summary_format = st.selectbox(
        "Summary Format:",
        ["bullet_points", "narrative", "markdown"],
        format_func=lambda x: {
            "bullet_points": "• Bullet Points",
            "narrative": "📖 Narrative Story", 
            "markdown": "📝 Markdown Format"
        }[x]
    )
    
    # Summary length
    summary_length = st.selectbox(
        "Summary Length:",
        ["short", "medium", "long"],
        index=1,
        format_func=lambda x: {
            "short": "📄 Short (100-150 words)",
            "medium": "📄 Medium (200-300 words)",
            "long": "📄 Long (400-500 words)"
        }[x]
    )
    
    # Language selection
    language = st.selectbox(
        "Output Language:",
        ["english", "spanish", "french", "german", "japanese", "chinese"],
        format_func=lambda x: {
            "english": "🇺🇸 English",
            "spanish": "🇪🇸 Spanish", 
            "french": "🇫🇷 French",
            "german": "🇩🇪 German",
            "japanese": "🇯🇵 Japanese",
            "chinese": "🇨🇳 Chinese"
        }[x]
    )
    
    # Include sentiment analysis
    include_sentiment = st.checkbox("📊 Include Sentiment Analysis", value=True)
    
    st.divider()
    
    # Data management
    st.header("🗂️ Data Management")
    if st.button("🗑️ Clear History", type="secondary"):
        st.session_state.summary_history = []
        st.success("History cleared!")
        st.rerun()

# Main content area
if page == "Summarize Video":
    
    # Create tabs for different input methods
    tab1, tab2 = st.tabs(["🔗 YouTube URL", "📁 Upload Video File"])
    
    with tab1:
        st.header("🔗 Summarize YouTube Video")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            video_url = st.text_input(
                "Enter YouTube URL:",
                placeholder="https://www.youtube.com/watch?v=...",
                help="Paste any YouTube video URL here"
            )
        
        with col2:
            st.write("") # Spacer
            st.write("") # Spacer
            generate_btn = st.button("🚀 Generate Summary", type="primary", use_container_width=True)
        
        # Preview video if URL is provided
        if video_url:
            try:
                video_id = extract_video_id(video_url)
                if video_id:
                    st.subheader("📺 Video Preview")
                    
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        # Display thumbnail
                        thumbnail_url = get_thumbnail_url(video_id)
                        st.image(thumbnail_url, use_column_width=True)
                    
                    with col2:
                        # Embed video player
                        st.video(video_url)
            except:
                st.warning("⚠️ Invalid YouTube URL format")
        
        # Generate summary when button is clicked
        if generate_btn and video_url:
            with st.spinner("🔄 Processing video... This may take a few moments"):
                try:
                    # Prepare request payload
                    payload = {
                        "url": video_url,
                        "format": summary_format,
                        "length": summary_length,
                        "language": language,
                        "include_sentiment": include_sentiment
                    }
                    
                    # Make API request
                    response = requests.post(f"{API_BASE_URL}/summarize", json=payload)
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Store in session state
                        st.session_state.summary_history.append(result)
                        
                        # Display results
                        st.success("✅ Summary generated successfully!")
                        
                        # Create tabs for different views
                        result_tab1, result_tab2, result_tab3, result_tab4 = st.tabs([
                            "📝 Summary", "📊 Details", "🎯 Sentiment", "📋 Full Transcript"
                        ])
                        
                        with result_tab1:
                            st.subheader("📝 Generated Summary")
                            st.markdown(result['summary'])
                            
                            # Download options
                            st.subheader("💾 Download Options")
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                if st.button("📄 Download as Text"):
                                    download_response = requests.get(f"{API_BASE_URL}/download/{result['id']}?format=txt")
                                    if download_response.status_code == 200:
                                        st.download_button(
                                            label="📥 Download Text File",
                                            data=download_response.content,
                                            file_name=f"summary_{result['id']}.txt",
                                            mime="text/plain"
                                        )
                            
                            with col2:
                                if st.button("📝 Download as Markdown"):
                                    st.download_button(
                                        label="📥 Download Markdown",
                                        data=f"# Video Summary\\n\\n{result['summary']}",
                                        file_name=f"summary_{result['id']}.md",
                                        mime="text/markdown"
                                    )
                        
                        with result_tab2:
                            st.subheader("📊 Video Information")
                            display_video_info(result['metadata'])
                            
                            # Keywords section
                            if result.get('keywords'):
                                st.subheader("🔍 Key Topics")
                                keywords_df = pd.DataFrame({
                                    'Keywords': result['keywords'][:10],
                                    'Relevance': [f"#{i+1}" for i in range(len(result['keywords'][:10]))]
                                })
                                st.dataframe(keywords_df, use_container_width=True)
                        
                        with result_tab3:
                            if result.get('sentiment') and include_sentiment:
                                st.subheader("📊 Sentiment Analysis")
                                
                                sentiment = result['sentiment']
                                
                                # Display overall sentiment
                                overall_sentiment = sentiment.get('overall', 'neutral')
                                sentiment_emoji = {
                                    'positive': '😊',
                                    'negative': '😞', 
                                    'neutral': '😐'
                                }
                                
                                st.metric(
                                    "Overall Sentiment", 
                                    f"{sentiment_emoji.get(overall_sentiment, '😐')} {overall_sentiment.title()}",
                                    f"Score: {sentiment.get('compound', 0):.2f}"
                                )
                                
                                # Create sentiment chart
                                fig = create_sentiment_chart(sentiment)
                                if fig:
                                    st.pyplot(fig)
                                    
                                # Detailed scores
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("😊 Positive", f"{sentiment.get('positive', 0):.1%}")
                                with col2:
                                    st.metric("😐 Neutral", f"{sentiment.get('neutral', 0):.1%}")
                                with col3:
                                    st.metric("😞 Negative", f"{sentiment.get('negative', 0):.1%}")
                            else:
                                st.info("Sentiment analysis not included. Enable it in the sidebar settings.")
                        
                        with result_tab4:
                            st.subheader("📋 Full Video Transcript")
                            with st.expander("Click to view full transcript", expanded=False):
                                st.text_area(
                                    "Transcript:", 
                                    result['transcript'], 
                                    height=300,
                                    disabled=True
                                )
                    
                    else:
                        st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to backend API. Please ensure the backend is running on port 8000.")
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")
    
    with tab2:
        st.header("📁 Upload and Analyze Video File")
        
        uploaded_file = st.file_uploader(
            "Choose a video file:",
            type=['mp4', 'avi', 'mov', 'mkv'],
            help="Upload MP4, AVI, MOV, or MKV files"
        )
        
        if uploaded_file is not None:
            # Display file info
            st.info(f"📁 File: {uploaded_file.name} ({uploaded_file.size / (1024*1024):.1f} MB)")
            
            # Advanced settings for file upload
            with st.expander("⚙️ Advanced Settings", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    file_format = st.selectbox("Format:", ["bullet_points", "narrative", "markdown"], key="file_format")
                    file_length = st.selectbox("Length:", ["short", "medium", "long"], index=1, key="file_length")
                
                with col2:
                    file_language = st.selectbox("Language:", ["english", "spanish", "french"], key="file_language")
                    file_sentiment = st.checkbox("Include Sentiment", value=True, key="file_sentiment")
            
            if st.button("🚀 Analyze Uploaded Video", type="primary"):
                with st.spinner("🔄 Processing uploaded video... This may take several minutes"):
                    try:
                        # Prepare files and data for upload
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                        data = {
                            "format": file_format,
                            "length": file_length,
                            "language": file_language,
                            "include_sentiment": file_sentiment
                        }
                        
                        # Make API request
                        response = requests.post(f"{API_BASE_URL}/summarize/upload", files=files, data=data)
                        
                        if response.status_code == 200:
                            result = response.json()
                            
                            # Store in session state
                            st.session_state.summary_history.append(result)
                            
                            st.success("✅ Video analyzed successfully!")
                            
                            # Display results (similar to URL tab)
                            st.subheader("📝 Analysis Results")
                            
                            # Summary
                            st.markdown("**Summary:**")
                            st.markdown(result['summary'])
                            
                            # File details
                            if result.get('metadata'):
                                st.markdown("**File Details:**")
                                metadata = result['metadata']
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.metric("File Size", f"{metadata.get('file_size', 0) / (1024*1024):.1f} MB")
                                with col2:
                                    st.metric("File Type", metadata.get('file_type', 'N/A'))
                            
                            # Sentiment and keywords (if available)
                            if result.get('sentiment') and file_sentiment:
                                st.markdown("**Sentiment Analysis:**")
                                sentiment = result['sentiment']
                                st.metric("Overall Sentiment", sentiment.get('overall', 'neutral').title())
                            
                            if result.get('keywords'):
                                st.markdown("**Key Topics:**")
                                st.write(", ".join(result['keywords'][:10]))
                        
                        else:
                            st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
                    
                    except Exception as e:
                        st.error(f"❌ An error occurred: {str(e)}")

elif page == "History":
    st.header("📜 Summary History")
    
    if st.session_state.summary_history:
        st.info(f"📊 Total summaries: {len(st.session_state.summary_history)}")
        
        # Display summaries in reverse chronological order
        for i, summary in enumerate(reversed(st.session_state.summary_history)):
            with st.expander(f"📝 {summary['metadata'].get('title', f'Summary {len(st.session_state.summary_history)-i}')} - {summary['timestamp'][:19]}"):
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown("**Summary:**")
                    st.markdown(summary['summary'][:500] + "..." if len(summary['summary']) > 500 else summary['summary'])
                
                with col2:
                    if summary.get('sentiment'):
                        sentiment = summary['sentiment']['overall']
                        emoji = {'positive': '😊', 'negative': '😞', 'neutral': '😐'}
                        st.metric("Sentiment", f"{emoji.get(sentiment, '😐')} {sentiment.title()}")
                    
                    if summary.get('keywords'):
                        st.markdown("**Top Keywords:**")
                        st.write(", ".join(summary['keywords'][:5]))
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button(f"📄 View Full", key=f"view_{i}"):
                        st.json(summary)
                
                with col2:
                    if st.button(f"💾 Download", key=f"download_{i}"):
                        download_content = f"""
Title: {summary['metadata'].get('title', 'N/A')}
Generated: {summary['timestamp']}

Summary:
{summary['summary']}

Keywords: {', '.join(summary.get('keywords', []))}
"""
                        st.download_button(
                            label="📥 Download",
                            data=download_content,
                            file_name=f"summary_{summary['id']}.txt",
                            mime="text/plain",
                            key=f"dl_btn_{i}"
                        )
                
                with col3:
                    if st.button(f"🗑️ Delete", key=f"delete_{i}"):
                        # Remove from session state
                        original_index = len(st.session_state.summary_history) - 1 - i
                        st.session_state.summary_history.pop(original_index)
                        st.success("Summary deleted!")
                        st.rerun()
    else:
        st.info("📭 No summaries yet. Go to 'Summarize Video' to create your first summary!")
        
        if st.button("🚀 Start Summarizing"):
            st.session_state.page = "Summarize Video"
            st.rerun()

elif page == "Settings":
    st.header("⚙️ Application Settings")
    
    st.subheader("🔧 API Configuration")
    
    with st.expander("🔗 Backend API Settings"):
        new_api_url = st.text_input("Backend API URL:", value=API_BASE_URL)
        if st.button("🔄 Update API URL"):
            # Note: In a real app, you'd want to persist this setting
            st.success(f"API URL updated to: {new_api_url}")
    
    st.subheader("🎨 Display Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        default_format = st.selectbox(
            "Default Summary Format:",
            ["bullet_points", "narrative", "markdown"],
            format_func=lambda x: x.replace("_", " ").title()
        )
        
        default_length = st.selectbox(
            "Default Summary Length:",
            ["short", "medium", "long"],
            index=1
        )
    
    with col2:
        default_language = st.selectbox(
            "Default Language:",
            ["english", "spanish", "french", "german", "japanese", "chinese"]
        )
        
        auto_sentiment = st.checkbox("Auto-enable Sentiment Analysis", value=True)
    
    if st.button("💾 Save Preferences"):
        st.success("✅ Preferences saved!")
    
    st.subheader("📊 Usage Statistics")
    
    if st.session_state.summary_history:
        total_summaries = len(st.session_state.summary_history)
        
        # Calculate stats
        format_counts = {}
        language_counts = {}
        
        for summary in st.session_state.summary_history:
            # These would be stored if we tracked the original settings
            # For now, showing placeholder data
            pass
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Summaries", total_summaries)
        
        with col2:
            st.metric("This Session", len([s for s in st.session_state.summary_history if s.get('timestamp', '').startswith(datetime.now().strftime('%Y-%m-%d'))]))
        
        with col3:
            avg_length = sum(len(s.get('summary', '')) for s in st.session_state.summary_history) / total_summaries if total_summaries > 0 else 0
            st.metric("Avg Summary Length", f"{avg_length:.0f} chars")
    
    else:
        st.info("📊 No usage data available yet.")
    
    st.subheader("ℹ️ About")
    
    st.markdown("""
    **Ultimate Video Summarizer Agent v1.0**
    
    This application uses advanced AI models to analyze and summarize video content with the following features:
    
    - 🎥 **Multi-format Support**: YouTube URLs and uploaded video files
    - 🤖 **AI-Powered Summarization**: Using OpenAI GPT models via LangChain
    - 📊 **Sentiment Analysis**: Emotional tone analysis using NLTK's VADER
    - 🔍 **Keyword Extraction**: Automatic identification of key topics
    - 🌍 **Multi-language Support**: Summaries in multiple languages
    - 📱 **Responsive Design**: Works on desktop and mobile devices
    - 💾 **Export Options**: Download summaries in various formats
    
    **Tech Stack:**
    - Frontend: Streamlit
    - Backend: FastAPI
    - AI Models: OpenAI GPT via LangChain
    - Video Processing: MoviePy, pytube
    - Sentiment Analysis: NLTK
    """)

# Footer
st.markdown("---")
st.markdown("Made by Ahmad using Streamlit and FastAPI | © 2024 Video Summarizer Agent")

# Run the app with: streamlit run frontend.py
