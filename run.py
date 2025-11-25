#!/usr/bin/env python3
"""
🚀 RAG Knowledge Assistant - Launcher
Starts the Streamlit application
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    required = ['streamlit', 'flask', 'sklearn', 'numpy', 'PyPDF2']
    missing = []
    
    for package in required:
        try:
            __import__(package.lower().replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print("Installing dependencies...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt', '-q'])

def main():
    """Main launcher"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║           🤖 RAG Knowledge Assistant v2.0                    ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Starting application...                                     ║
║                                                              ║
║  Features:                                                   ║
║    • 🔍 Semantic search in knowledge base                    ║
║    • 🤖 AI-powered answers via OpenRouter                    ║
║    • 📚 Support for PDF, MD, TXT, JSON files                 ║
║    • 💬 Natural language interface                           ║
║    • 📊 Multiple AI models to choose from                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    # Ensure logs directory exists
    Path('logs').mkdir(exist_ok=True)
    
    # Check dependencies
    check_dependencies()
    
    # Set environment variables
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    
    # Run Streamlit
    print("🌐 Opening browser at http://localhost:8501")
    print("🛑 Press Ctrl+C to stop\n")
    
    subprocess.run([
        sys.executable, '-m', 'streamlit', 'run', 'app.py',
        '--server.port', '8501',
        '--server.address', 'localhost',
        '--theme.base', 'dark',
        '--theme.primaryColor', '#e94560'
    ])

if __name__ == '__main__':
    main()

