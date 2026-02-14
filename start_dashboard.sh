#!/bin/bash

# Task Monitor Dashboard Startup Script
echo "🚀 Starting Task Monitor Dashboard with Apache ECharts..."

# Change to app directory
cd "$(dirname "$0")/app"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if CSV files exist
if [ ! -f "../databag/performance-monitoring.csv" ] || [ ! -f "../databag/performance-snapshot.csv" ]; then
    echo "⚠️  Warning: CSV files not found in databag directory"
    echo "   Make sure you have:"
    echo "   - databag/performance-monitoring.csv"
    echo "   - databag/performance-snapshot.csv"
    echo ""
fi

# Start the Flask server
echo "🌐 Starting Flask server on http://localhost:5000"
echo "   Open your browser and navigate to: http://localhost:5000"
echo "   Press Ctrl+C to stop the server"
echo ""

python backend_server.py