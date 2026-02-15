#!/bin/bash

# Task Monitor Dashboard Startup Script
echo "🚀 Starting Task Monitor Dashboard..."

# Check if app/logs directory exists, if not create it
if [ ! -d "app/logs" ]; then
    echo "📦 Creating app/logs directory..."
    mkdir -p app/logs
fi

# Check if databag directory exists, if not create it
if [ ! -d "databag" ]; then
    echo "📦 Creating databag directory..."
    mkdir -p databag
fi

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

# Go back to project root for data collection
cd ..

# Step 1: Take a fresh performance snapshot
echo "📊 Taking performance snapshot..."
python run.py --snapshot --limit 20
if [ $? -eq 0 ]; then
    echo "✅ Snapshot completed successfully"
else
    echo "⚠️  Snapshot failed, but continuing..."
fi

# Step 2: Start background monitoring process
echo "🔄 Starting background monitoring process..."
python run.py --monitor --limit 20 --interval 2 &
MONITOR_PID=$!
echo "   📈 Background monitoring started (PID: $MONITOR_PID)"
echo "   📊 Collecting data every 2 seconds"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down Task Monitor..."
    if [ ! -z "$MONITOR_PID" ] && kill -0 $MONITOR_PID 2>/dev/null; then
        echo "   Stopping background monitoring (PID: $MONITOR_PID)..."
        kill $MONITOR_PID 2>/dev/null
        wait $MONITOR_PID 2>/dev/null
        echo "   ✅ Background monitoring stopped"
    fi
    echo "✅ Task Monitor shutdown complete"
    exit 0
}

# Set up signal handlers
trap cleanup EXIT INT TERM

# Wait a moment for monitoring to initialize
sleep 2

# Step 3: Start the Flask dashboard server
cd app
echo "🌐 Starting Flask dashboard server on http://localhost:5000"
echo "   📊 Real-time data: Monitoring running in background"
echo "   🌍 Web interface: http://localhost:5000"
echo "   ⏹️  Press Ctrl+C to stop all processes"
echo ""

python backend_server.py