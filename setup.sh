#!/bin/bash

# setup.sh - Setup script for Video Analysis & Summarizer Agent

echo "🎥 Video Analysis & Summarizer Agent Setup"
echo "=========================================="
echo ""

# Check Python version
echo "🐍 Checking Python version..."
python_version=$(python3 --version 2>&1 | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+' | head -n1)
if [ -z "$python_version" ]; then
    echo "❌ Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

major_version=$(echo $python_version | cut -d. -f1)
minor_version=$(echo $python_version | cut -d. -f2)

if [ "$major_version" -lt 3 ] || ([ "$major_version" -eq 3 ] && [ "$minor_version" -lt 8 ]); then
    echo "❌ Python version $python_version is too old"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "✅ Python $python_version detected"
echo ""

# Create virtual environment
echo "🌍 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip
echo ""

# Install requirements
echo "📚 Installing Python packages..."
pip install -r requirements.txt
echo "✅ All packages installed successfully"
echo ""

# Download NLTK data
echo "🔤 Downloading NLTK data..."
python -c "
import nltk
print('Downloading VADER lexicon...')
nltk.download('vader_lexicon', quiet=True)
print('✅ NLTK data downloaded')
"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created from template"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env file and add your OpenAI API key"
    echo "   OPENAI_API_KEY=your_actual_api_key_here"
    echo ""
else
    echo "✅ .env file already exists"
    echo ""
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p temp
echo "✅ Directories created"
echo ""

# Test imports
echo "🧪 Testing package imports..."
python -c "
try:
    import fastapi
    import streamlit
    import openai
    import langchain
    import nltk
    import moviepy
    import pytube
    print('✅ All critical packages imported successfully')
except ImportError as e:
    print(f'❌ Import error: {e}')
    exit(1)
"
echo ""

# Final instructions
echo "🎉 Setup completed successfully!"
echo ""
echo "📝 Next steps:"
echo "1. Edit the .env file and add your OpenAI API key"
echo "2. To run the application:"
echo "   Backend:  python run_backend.py"
echo "   Frontend: python run_frontend.py"
echo ""
echo "🌐 Access points:"
echo "   Frontend: http://localhost:8501"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "💡 Need help? Check the README.md file for detailed instructions"
echo ""

# Check if .env has been configured
if grep -q "your_openai_api_key_here" .env 2>/dev/null; then
    echo "⚠️  REMINDER: Don't forget to update your OpenAI API key in .env file!"
    echo ""
fi

echo "Happy summarizing! 🚀"
