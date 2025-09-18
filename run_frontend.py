# run_frontend.py - Script to run the Streamlit frontend

import subprocess
import sys
import os
from pathlib import Path
import time
import requests

def check_requirements():
    """Check if all required packages are installed"""
    try:
        import streamlit
        import requests
        import pandas
        import matplotlib
        import plotly
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_backend_connection():
    """Check if backend is running and accessible"""
    backend_url = "http://localhost:8000"
    
    print("🔍 Checking backend connection...")
    
    for attempt in range(5):
        try:
            response = requests.get(f"{backend_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Backend is running and accessible")
                return True
        except requests.exceptions.RequestException:
            if attempt < 4:
                print(f"⏳ Backend not ready, retrying in 2 seconds... (attempt {attempt + 1}/5)")
                time.sleep(2)
            else:
                print("❌ Cannot connect to backend")
                print("Please make sure the backend is running on port 8000")
                print("Run: python run_backend.py (in another terminal)")
                return False
    
    return False

def main():
    """Main function to run the frontend"""
    print("🎥 Starting Video Summarizer Frontend...")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check backend connection
    if not check_backend_connection():
        print("\n💡 To start the complete application:")
        print("1. Open a new terminal")
        print("2. Run: python run_backend.py")
        print("3. Then run this frontend script again")
        print("\nOr start frontend anyway? The app will show connection errors until backend is running.")
        
        choice = input("Continue anyway? (y/N): ").lower().strip()
        if choice != 'y':
            sys.exit(1)
    
    # Run the frontend
    try:
        print("🔄 Starting Streamlit frontend on http://localhost:8501")
        print("🌐 The app will open in your default browser")
        print("🛑 Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Run streamlit
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            "frontend.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ]
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
