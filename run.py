#!/usr/bin/env python3
"""
Task Monitor - CSV Snapshot and Monitoring Tool
"""
import sys
import argparse
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import required modules
from app.src.snapshotcsv import SnapshotCSV
from app.src.utils.logger_utils import get_logger

# Setup logger
logger = get_logger('main')

def main():
    """Main function with argument parsing"""
    parser = argparse.ArgumentParser(description="Task Monitor - System Performance Analysis Tool")
    
    # Add mutually exclusive options
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--snapshot', action='store_true', help='Take a single performance snapshot')
    group.add_argument('--monitor', action='store_true', help='Start continuous monitoring mode')
    
    # Optional arguments
    parser.add_argument('--limit', type=int, default=20, help='Number of top processes to monitor (default: 20)')
    parser.add_argument('--interval', type=int, default=2, help='Monitoring refresh interval in seconds (default: 2)')
    
    args = parser.parse_args()
    
    # Create CSV snapshot generator
    csv_snapshot = SnapshotCSV()
    
    if args.snapshot:
        # Run single snapshot
        logger.info("📊 Taking performance snapshot...")
        success = csv_snapshot.save_performance_data(limit=args.limit)
        if success:
            logger.info(f"✅ Snapshot saved to {csv_snapshot.output_file}")
        else:
            logger.error("❌ Snapshot failed")
            return 1
    elif args.monitor:
        # Run monitoring mode
        logger.info(f"🔄 Starting continuous monitoring mode...")
        logger.info(f"📊 Monitoring top {args.limit} processes every {args.interval} seconds")
        success = csv_snapshot.start_monitoring(limit=args.limit, refresh_interval=args.interval)
        if success:
            logger.info("✅ Monitoring completed")
        else:
            logger.error("❌ Monitoring failed")
            return 1
    else:
        logger.error("No valid mode selected. Use --snapshot or --monitor.")
        return 1
    
    return 0

if __name__ == "__main__":
    main()