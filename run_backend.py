# run_backend.py - Script to run the FastAPI backend

import subprocess
import sys
import os
from pathlib import Path

def check_requirements():
    """Check if all required packages are installed"""
    try:
        import fastapi
        import uvicorn
        import openai
        import langchain
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found")
        print("Please copy .env.example to .env and add your OpenAI API key")
        return False
    
    # Check for OpenAI API key
    with open(env_file, 'r') as f:
        content = f.read()
        if 'OPENAI_API_KEY=' not in content or 'your_openai_api_key_here' in content:
            print("❌ OpenAI API key not configured in .env file")
            print("Please add your OpenAI API key to the .env file")
            return False
    
    print("✅ Environment configuration looks good")
    return True

def main():
    """Main function to run the backend"""
    print("🚀 Starting Video Summarizer Backend...")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check environment
    if not check_env_file():
        sys.exit(1)
    
    # Run the backend
    try:
        print("🔄 Starting FastAPI server on http://localhost:8000")
        print("📚 API documentation available at http://localhost:8000/docs")
        print("🛑 Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Run uvicorn with the backend
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "backend:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload",
            "--log-level", "info"
        ]
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
