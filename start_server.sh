#!/bin/bash

# Resume Builder Server Startup Script
# This script ensures the server starts properly and stays running

echo "🚀 Starting Resume Builder Server..."

# Kill any existing streamlit processes
pkill -f streamlit 2>/dev/null || true

# Wait a moment for processes to fully stop
sleep 2

# Navigate to project directory
cd /Users/penncu/Projects/resume_builder

# Activate virtual environment
source .venv/bin/activate

# Start streamlit with proper configuration
echo "🌐 Starting server on http://localhost:8502"
streamlit run app.py --server.port 8502 --server.headless true --browser.gatherUsageStats false
