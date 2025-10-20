#!/bin/bash

# Quick Resume Builder Server Start
# Usage: ./run_app.sh

echo "🚀 Resume Builder - Quick Start"
echo "================================"

# Kill any existing processes
pkill -f streamlit 2>/dev/null || true
sleep 1

# Start the server
cd /Users/penncu/Projects/resume_builder
source .venv/bin/activate
streamlit run app.py --server.port 8502 --server.headless true --browser.gatherUsageStats false

echo "🌐 Server running at: http://localhost:8502"
