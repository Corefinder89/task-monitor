#!/usr/bin/env python3
"""
Task Monitor - Simple CSV Generator
"""
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import required modules
from app.src.convertcsv import ConvertCSV

def main():
    """Run CSV generation"""
    # Create CSV converter and save performance data
    csv_converter = ConvertCSV()
    csv_converter.save_performance_data()

if __name__ == "__main__":
    main()