import csv
import os
from datetime import datetime
from app.src.gettasks import GetProcesses
from app.src.utils import TaskMonitorLogger

class ConvertCSV():
    def __init__(self):
        self.get_processes = GetProcesses()
        self.output_file = "performance-monitor.csv"
        self.logger = TaskMonitorLogger.get_csv_logger()
    
    def convert_to_csv(self, processes):
        csv_data = "PID,Name,Memory (MB)\n"
        for proc in processes:
            csv_data += f"{proc['pid']},{proc['name']},{proc['memory_mb']:.2f}\n"
        return csv_data
    
    def write_to_csv_file(self, processes):
        """Write process data to performance-monitor.csv file in write mode"""
        try:
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
    
    def save_performance_data(self, limit=20):
        """Get current processes and save them to CSV file"""
        try:
            processes = self.get_processes.get_top_memory_processes(limit)
            return self.write_to_csv_file(processes)
        except Exception as e:
            self.logger.error(f"Error getting process data: {e}")
            return False