import csv
import os
import time
from datetime import datetime
from pathlib import Path
from app.src.gettasks import GetProcesses
from app.src.utils import TaskMonitorLogger

class CSVConverter():
    def __init__(self):
        self.get_processes = GetProcesses()
        self.output_file = "databag/performance-snapshot.csv"
        self.logger = TaskMonitorLogger.get_snapshot_logger()
    
    def _ensure_databag_directory(self):
        """Ensure the databag directory exists, create if it doesn't"""
        databag_dir = Path('databag')
        if not databag_dir.exists():
            databag_dir.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Created databag directory: {databag_dir.absolute()}")
    
    def snapshot_to_csv(self, processes):
        csv_data = "PID,Name,Memory (MB)\n"
        for proc in processes:
            csv_data += f"{proc['pid']},{proc['name']},{proc['memory_mb']:.2f}\n"
        return csv_data
    
    def write_to_csv_file(self, processes):
        """Write process data to performance-snapshot.csv file in write mode"""
        try:
            # Ensure databag directory exists
            self._ensure_databag_directory()
            
            with open(self.output_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                
                # Write header
                writer.writerow(['Timestamp', 'PID', 'Name', 'Memory (MB)'])
                
                # Write process data with timestamp
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                for proc in processes:
                    writer.writerow([
                        timestamp,
                        proc['pid'],
                        proc['name'],
                        f"{proc['memory_mb']:.2f}"
                    ])
                        
            self.logger.info(f"Data successfully written to {self.output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error writing to CSV file: {e}")
            return False
    
    def append_to_csv_file(self, timestamp, processes):
        """Append process data to CSV file (for monitoring mode)"""
        try:
            # Ensure databag directory exists
            self._ensure_databag_directory()
            
            file_exists = Path(self.output_file).exists()
            
            with open(self.output_file, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                
                # Write header only if file doesn't exist
                if not file_exists:
                    if any('cpu_percent' in proc for proc in processes):
                        writer.writerow(['Timestamp', 'PID', 'Name', 'Memory (MB)', 'CPU (%)'])
                    else:
                        writer.writerow(['Timestamp', 'PID', 'Name', 'Memory (MB)'])
                
                # Write process data with timestamp
                for proc in processes:
                    if 'cpu_percent' in proc:
                        writer.writerow([
                            timestamp,
                            proc['pid'],
                            proc['name'],
                            round(proc['memory_mb'], 2),
                            round(proc['cpu_percent'], 2)
                        ])
                    else:
                        writer.writerow([
                            timestamp,
                            proc['pid'],
                            proc['name'],
                            round(proc['memory_mb'], 2)
                        ])
            
            self.logger.debug(f"Data appended to {self.output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error appending to CSV file: {e}")
            return False
    
    def save_performance_data(self, limit=20):
        """Get current processes and save them to CSV file"""
        try:
            processes = self.get_processes.snapshot_top_memory_processes(limit)
            return self.write_to_csv_file(processes)
        except Exception as e:
            self.logger.error(f"Error getting process data: {e}")
            return False
    
    def start_monitoring(self, limit=20, refresh_interval=2):
        """Start continuous monitoring mode"""
        self.logger.info(f"Starting continuous monitoring with {refresh_interval}s intervals")
        self.logger.info("Press Ctrl+C to stop monitoring")
        
        # Set output file for monitoring
        self.output_file = "databag/performance-monitoring.csv"
        
        try:
            while True:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                processes = self.get_processes.monitor_top_processes(limit)
                
                # Save to CSV
                self.append_to_csv_file(timestamp, processes)
                
                time.sleep(refresh_interval)
                
        except KeyboardInterrupt:
            self.logger.info("\n\nMonitoring stopped. CSV saved.")
            self.logger.info("Monitoring stopped by user")
            return True
        except Exception as e:
            self.logger.error(f"Error during monitoring: {e}")
            return False