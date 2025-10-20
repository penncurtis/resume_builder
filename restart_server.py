#!/usr/bin/env python3
"""
Resume Builder Server Restart Script
This script automatically restarts the Streamlit server when needed.
"""

import subprocess
import sys
import time
import os
import signal

def kill_streamlit():
    """Kill any existing Streamlit processes"""
    try:
        subprocess.run(['pkill', '-f', 'streamlit'], check=False)
        time.sleep(2)
        print("✅ Stopped existing Streamlit processes")
    except Exception as e:
        print(f"⚠️  Warning: Could not stop existing processes: {e}")

def start_streamlit():
    """Start the Streamlit server"""
    try:
        # Change to project directory
        os.chdir('/Users/penncu/Projects/resume_builder')
        
        # Start streamlit
        cmd = [
            'streamlit', 'run', 'app.py',
            '--server.port', '8502',
            '--server.headless', 'true',
            '--browser.gatherUsageStats', 'false'
        ]
        
        print("🚀 Starting Resume Builder Server...")
        print("🌐 Server will be available at: http://localhost:8502")
        print("📝 Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Start the server
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    kill_streamlit()
    start_streamlit()
