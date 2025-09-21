# 🎥 YouTube Video Summarizer - Complete Documentation

## 📋 Table of Contents

1. [Project Overview](#-project-overview)
2. [Features](#-features)
3. [Architecture](#-architecture)
4. [Technology Stack](#-technology-stack)
5. [Installation Guide](#-installation-guide)
6. [Usage Instructions](#-usage-instructions)
7. [API Documentation](#-api-documentation)
8. [File Structure](#-file-structure)
9. [Configuration](#-configuration)
10. [Deployment](#-deployment)
11. [Contributing](#-contributing)
12. [Troubleshooting](#-troubleshooting)
13. [License](#-license)

## 🎬 Project Overview

The **YouTube Video Summarizer** is an AI-powered application that automatically generates concise summaries of YouTube videos using advanced natural language processing techniques. Built with FastAPI for the backend and Streamlit for the frontend, this application leverages OpenAI's GPT models through LangChain to provide intelligent video content analysis.

### Key Capabilities

- **YouTube URL Processing**: Extract and summarize content from any public YouTube video
- **Video File Upload**: Support for local video file processing (MP4, AVI, MOV, MKV)
- **Multiple Summary Formats**: Bullet points, narrative story, or structured markdown
- **Multi-language Support**: Generate summaries in 6 different languages
- **Sentiment Analysis**: Analyze emotional tone and sentiment of video content
- **Keyword Extraction**: Identify key topics and themes automatically
- **Export Options**: Download summaries in multiple formats
- **History Management**: Track and manage previous summarizations

## ✨ Features

### Core Functionality
- 🎥 **YouTube Video Summarization**: Process videos directly from YouTube URLs
- 📁 **File Upload Support**: Handle local video files with transcript extraction
- 🤖 **AI-Powered Summarization**: Utilize OpenAI GPT models via LangChain
- 📊 **Sentiment Analysis**: NLTK VADER-based emotional tone analysis
- 🔍 **Keyword Extraction**: Automatic identification of key topics
- 🌍 **Multi-language Output**: Support for English, Spanish, French, German, Japanese, Chinese

### User Experience
- 📱 **Responsive Interface**: Clean, modern Streamlit-based frontend
- 📝 **Customizable Output**: Choose format (bullet points, narrative, markdown) and length
- 📊 **Visual Analytics**: Sentiment distribution charts and keyword analysis
- 📚 **History Tracking**: Save and manage summarization history
- 💾 **Export Options**: Download summaries as text or markdown files

### Technical Features
- 🚀 **FastAPI Backend**: High-performance REST API with automatic documentation
- 🔄 **Asynchronous Processing**: Efficient handling of video processing tasks
- 🛡️ **Error Handling**: Comprehensive error management and user feedback
- 📈 **Scalable Architecture**: Modular design for easy extension
- 🐳 **Containerization Ready**: Docker-friendly setup scripts

## 🏗️ Architecture

### System Architecture

```
┌─────────────────┐    HTTP/REST    ┌─────────────────┐
│  Streamlit      │ ◄──────────────► │  FastAPI        │
│  Frontend       │                 │  Backend        │
│  (Port 8501)    │                 │  (Port 8000)    │
└─────────────────┘                 └─────────────────┘
                                            │
                                            ▼
                                    ┌─────────────────┐
                                    │  AI/ML Pipeline │
                                    │                 │
                                    │ • OpenAI GPT    │
                                    │ • LangChain     │
                                    │ • NLTK VADER    │
                                    │ • pytube        │
                                    │ • MoviePy       │
                                    └─────────────────┘
```

### Component Breakdown

1. **Frontend Layer (Streamlit)**
   - User interface and interaction management
   - File upload handling
   - Results visualization
   - History management

2. **Backend Layer (FastAPI)**
   - REST API endpoints
   - Video processing coordination
   - AI model integration
   - Data persistence

3. **AI/ML Pipeline**
   - Transcript extraction (youtube-transcript-api, SpeechRecognition)
   - Text summarization (OpenAI + LangChain)
   - Sentiment analysis (NLTK VADER)
   - Keyword extraction (custom NLP)

## 🛠️ Technology Stack

### Backend Technologies
| Technology | Version | Purpose |
|------------|---------|---------|
| FastAPI | 0.104.1 | High-performance web framework |
| OpenAI | 1.3.7 | GPT model integration |
| LangChain | 0.0.340 | LLM orchestration and chaining |
| pytube | 15.0.0 | YouTube video processing |
| MoviePy | 1.0.3 | Video file manipulation |
| NLTK | 3.8.1 | Natural language processing |
| uvicorn | 0.24.0 | ASGI server implementation |

### Frontend Technologies
| Technology | Version | Purpose |
|------------|---------|---------|
| Streamlit | 1.28.1 | Interactive web application framework |
| Plotly | 5.17.0 | Data visualization and charts |
| Matplotlib | 3.8.2 | Statistical plotting |
| Pandas | 2.1.3 | Data manipulation and analysis |

### Supporting Libraries
| Technology | Purpose |
|------------|---------|
| youtube-transcript-api | YouTube subtitle extraction |
| SpeechRecognition | Audio-to-text conversion |
| pydub | Audio processing |
| requests | HTTP client library |
| python-dotenv | Environment variable management |

## 📦 Installation Guide

### Prerequisites

- **Python 3.8+** (Python 3.9 or 3.10 recommended)
- **OpenAI API Key** (required for summarization functionality)
- **Git** (for cloning the repository)
- **ffmpeg** (for audio processing, auto-installed with MoviePy)

### Step 1: Clone the Repository

```bash
git clone https://github.com/madhusri2004/youtube-video-summarizer.git
cd youtube-video-summarizer
```

### Step 2: Automatic Setup (Recommended)

Run the automated setup script:

```bash
# On Linux/Mac
chmod +x setup.sh
./setup.sh

# On Windows
bash setup.sh
```

The setup script will:
- Check Python version compatibility
- Create and activate virtual environment
- Install all dependencies
- Download required NLTK data
- Create environment configuration files

### Step 3: Manual Setup (Alternative)

If you prefer manual installation:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('vader_lexicon')"
```

### Step 4: Environment Configuration

1. Copy the environment template:
```bash
cp .env.example .env
```

2. Edit `.env` file and add your OpenAI API key:
```bash
OPENAI_API_KEY=your_actual_openai_api_key_here
```

### Step 5: Verify Installation

Test the installation by running:

```bash
python -c "
import fastapi, streamlit, openai, langchain, nltk, moviepy, pytube
print('✅ All packages installed successfully!')
"
```

## 🚀 Usage Instructions

### Running the Application

#### Method 1: Using Run Scripts (Recommended)

**Terminal 1 - Start Backend:**
```bash
python run_backend.py
```

**Terminal 2 - Start Frontend:**
```bash
python run_frontend.py
```

#### Method 2: Direct Commands

**Backend:**
```bash
uvicorn backend:app --host 0.0.0.0 --port 8000 --reload
```

**Frontend:**
```bash
streamlit run frontend.py --server.port 8501
```

### Accessing the Application

- **Frontend Interface**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### Using the Interface

#### 1. Summarizing YouTube Videos

1. Navigate to the "🔗 YouTube URL" tab
2. Paste a YouTube video URL
3. Configure settings in the sidebar:
   - **Format**: Choose between bullet points, narrative, or markdown
   - **Length**: Select short (100-150 words), medium (200-300), or long (400-500)
   - **Language**: Pick from 6 supported languages
   - **Sentiment Analysis**: Enable/disable emotional analysis
4. Click "🚀 Generate Summary"
5. View results in organized tabs:
   - **Summary**: Generated text summary
   - **Details**: Video metadata and keywords
   - **Sentiment**: Emotional analysis with charts
   - **Transcript**: Full video transcript

#### 2. Uploading Video Files

1. Navigate to the "📁 Upload Video File" tab
2. Upload a video file (MP4, AVI, MOV, MKV)
3. Configure processing settings
4. Click "🚀 Analyze Uploaded Video"
5. Review results similar to YouTube URL processing

#### 3. Managing History

1. Go to the "📜 Summary History" page
2. View all previous summarizations
3. Access full details, download summaries, or delete entries
4. Use the search and filter functionality

### Advanced Configuration

#### Customizing Summary Prompts

Edit the `get_summary_prompt()` function in `backend.py` to modify how summaries are generated:

```python
def get_summary_prompt(format_type: str, length: str, language: str) -> str:
    # Customize prompts based on your needs
    # Add specific instructions, tone, or focus areas
```

#### Adding New Languages

Extend language support by modifying the language options in both `frontend.py` and `backend.py`:

```python
languages = ["english", "spanish", "french", "german", "japanese", "chinese", "your_new_language"]
```

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### POST `/summarize`
Summarize a YouTube video from URL.

**Request Body:**
```json
{
    "url": "https://www.youtube.com/watch?v=VIDEO_ID",
    "format": "bullet_points",  // bullet_points, narrative, markdown
    "length": "medium",         // short, medium, long
    "language": "english",      // english, spanish, french, german, japanese, chinese
    "include_sentiment": true   // boolean
}
```

**Response:**
```json
{
    "id": "uuid-string",
    "summary": "Generated summary text...",
    "metadata": {
        "title": "Video Title",
        "author": "Channel Name",
        "length": 1234,
        "views": 1000000,
        "thumbnail": "thumbnail_url"
    },
    "transcript": "Full video transcript...",
    "sentiment": {
        "overall": "positive",
        "positive": 0.7,
        "negative": 0.1,
        "neutral": 0.2,
        "compound": 0.6
    },
    "keywords": ["keyword1", "keyword2", ...],
    "timestamp": "2024-01-01T12:00:00"
}
```

#### POST `/summarize/upload`
Summarize an uploaded video file.

**Request:** Multipart form data with file and parameters

#### GET `/summaries`
Retrieve all stored summaries.

#### GET `/summaries/{summary_id}`
Retrieve a specific summary by ID.

#### DELETE `/summaries/{summary_id}`
Delete a specific summary.

#### GET `/download/{summary_id}`
Download a summary in specified format.

#### GET `/health`
Health check endpoint.

### Error Responses

```json
{
    "detail": "Error message describing the issue"
}
```

Common HTTP status codes:
- `200`: Success
- `400`: Bad Request (invalid URL, missing parameters)
- `404`: Not Found (summary not found)
- `500`: Internal Server Error (processing failures)

## 📂 File Structure

```
youtube-video-summarizer/
│
├── 📄 README.md                 # Project documentation
├── 📄 LICENSE                   # MIT license file
├── 📄 requirements.txt          # Python dependencies
├── 📄 .env.example             # Environment template
├── 📄 .gitignore               # Git ignore rules
├── 📄 setup.sh                 # Automated setup script
│
├── 🐍 backend.py               # FastAPI backend application
├── 🐍 frontend.py              # Streamlit frontend application
├── 🐍 run_backend.py           # Backend startup script
├── 🐍 run_frontend.py          # Frontend startup script
│
├── 📁 logs/                    # Application logs (auto-created)
├── 📁 temp/                    # Temporary processing files
└── 📁 venv/                    # Virtual environment (auto-created)
```

### Key Files Description

- **`backend.py`**: Core FastAPI application with all API endpoints and video processing logic
- **`frontend.py`**: Complete Streamlit interface with multi-page navigation and visualizations
- **`requirements.txt`**: Comprehensive list of Python dependencies with version specifications
- **`setup.sh`**: Automated setup script with error handling and dependency checking
- **`.env.example`**: Template for environment variables configuration

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional (with defaults)
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
FRONTEND_HOST=localhost
FRONTEND_PORT=8501

# Development
DEBUG=False
LOG_LEVEL=INFO
```

### Application Configuration

#### Backend Configuration (`backend.py`)

```python
# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI settings
OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_TEMPERATURE = 0.3
```

#### Frontend Configuration (`frontend.py`)

```python
# Streamlit page configuration
st.set_page_config(
    page_title="Video Analysis & Summarizer Agent",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API connection
API_BASE_URL = "http://localhost:8000"
```

## 🚢 Deployment

### Local Deployment

Follow the installation and usage instructions above for local deployment.

### Cloud Deployment Options

#### 1. Streamlit Cloud + External API

Deploy frontend on Streamlit Cloud and backend on services like:
- **Railway**
- **Render**  
- **DigitalOcean App Platform**
- **Heroku**

#### 2. Docker Deployment

Create `Dockerfile` for containerized deployment:

```dockerfile
# Backend Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY backend.py .
COPY .env .

EXPOSE 8000
CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 3. Docker Compose

```yaml
version: '3.8'
services:
  backend:
    build: 
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
  
  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "8501:8501"
    depends_on:
      - backend
```

### Environment-Specific Configurations

#### Production Settings

```python
# Disable debug mode
DEBUG = False

# Configure CORS properly
allow_origins = [
    "https://your-frontend-domain.com",
    "https://your-app.streamlit.app"
]

# Use production-grade ASGI server
# gunicorn backend:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 🤝 Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

3. Make your changes and commit:
```bash
git commit -m "Add your feature"
```

4. Push and create a pull request:
```bash
git push origin feature/your-feature-name
```

### Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Add docstrings to functions and classes
- Include error handling and logging

### Testing

Run tests before submitting:

```bash
# Test backend endpoints
python -c "import requests; print(requests.get('http://localhost:8000/health').status_code)"

# Test frontend connectivity
streamlit run frontend.py --server.headless true
```

## 🔧 Troubleshooting

### Common Issues

#### 1. "Cannot connect to backend API"

**Problem**: Frontend cannot reach backend
**Solutions**:
- Ensure backend is running on port 8000
- Check firewall settings
- Verify API_BASE_URL in frontend configuration

#### 2. "OpenAI API key not configured"

**Problem**: Missing or invalid OpenAI API key
**Solutions**:
- Verify `.env` file exists and contains valid key
- Check key format (should start with 'sk-')
- Ensure environment variables are loaded

#### 3. "Error extracting transcript"

**Problem**: Cannot get YouTube transcript
**Solutions**:
- Verify video has captions/subtitles
- Check if video is public and accessible
- Try with different video URL

#### 4. "Video processing failed"

**Problem**: Uploaded video cannot be processed
**Solutions**:
- Ensure video format is supported (MP4, AVI, MOV, MKV)
- Check video file is not corrupted
- Verify sufficient disk space for temporary files

#### 5. Package installation issues

**Problem**: Dependencies fail to install
**Solutions**:
```bash
# Update pip
pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v

# Install individual packages
pip install fastapi uvicorn streamlit openai langchain
```

### Debug Mode

Enable debug logging:

```python
# In backend.py
import logging
logging.basicConfig(level=logging.DEBUG)

# In frontend.py  
st.set_option('client.showErrorDetails', True)
```

### Performance Optimization

- Use caching for repeated summarizations
- Implement request rate limiting
- Optimize video processing chunk sizes
- Consider using faster AI models for development

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Veera Madhu Sri Adabala

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

**Built with ❤️ using FastAPI, Streamlit, and OpenAI**

For questions and support, please open an issue on GitHub or contact the maintainers.