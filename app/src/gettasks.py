import psutil
from app.src.utils import TaskMonitorLogger

class GetProcesses():
    def __init__(self):
        self.processes = []
        self.logger = TaskMonitorLogger.get_process_logger()
    
    def get_top_memory_processes(self, limit=20):
        # Reset processes list for fresh data
        self.processes = []
        self.logger.debug(f"Starting to collect top {limit} memory processes")
        
        # Get all processes and their memory usage
        process_count = 0
        error_count = 0
        
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                # Check if memory_info is available and not None
                if proc.info['memory_info'] is None:
                    error_count += 1
                    self.logger.debug(f"Process {proc.info.get('pid', 'unknown')} has no memory info")
                    continue
                    
                mem_mb = proc.info['memory_info'].rss / (1024 * 1024)  # Convert bytes to MB
                self.processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'] or 'Unknown',
                    'memory_mb': mem_mb
                })
                process_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                error_count += 1
                self.logger.debug(f"Could not access process info: {e}")
            except (AttributeError, TypeError, KeyError) as e:
                error_count += 1
                self.logger.debug(f"Process data error: {e}")
        
        # Sort processes by memory usage and return the top n
        top_processes = sorted(self.processes, key=lambda x: x['memory_mb'], reverse=True)[:limit]
        
        self.logger.info(f"Collected {process_count} processes, {error_count} access errors, returning top {len(top_processes)}")
        
        return top_processes