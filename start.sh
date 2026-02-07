#!/bin/bash
# Task Monitor - Quick Start Script

echo "🖥️  Task Monitor Application"
echo "=============================="
echo

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found. Please install Python 3."
    exit 1
fi

# Check if required packages are installed
echo "📦 Checking dependencies..."
python3 -c "import psutil" 2>/dev/null || {
    echo "⚠️  psutil package not found. Installing..."
    pip3 install psutil
}

echo "✅ Dependencies checked"
echo

# Run the application
echo "🚀 Starting Task Monitor..."
echo
python3 run.py "$@"