import psutil
import time
import os
from app.src.utils import TaskMonitorLogger

class GetProcesses():
    def __init__(self):
        self.processes = []
        self.logger = TaskMonitorLogger.get_process_logger()
        self.refresh_interval = 2  # seconds
        self._prime_cpu_counters()
    
    def _prime_cpu_counters(self):
        """Prime CPU counters so cpu_percent is meaningful"""
        self.logger.debug("Priming CPU counters...")
        for proc in psutil.process_iter():
            try:
                proc.cpu_percent(None)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        time.sleep(1)
        self.logger.debug("CPU counters primed")
    
    def snapshot_top_memory_processes(self, limit=20):
        """Get top memory-consuming processes (snapshot mode)"""
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
    
    def monitor_top_processes(self, limit=20):
        """Get top processes with both memory and CPU usage (for monitoring mode)"""
        # Don't reset processes list - continuous monitoring
        processes = []
        process_count = 0
        error_count = 0
        
        self.logger.debug(f"Monitoring top {limit} processes with CPU and memory data")
        
        for proc in psutil.process_iter(attrs=['pid', 'name', 'memory_info']):
            try:
                if proc.info['memory_info'] is None:
                    error_count += 1
                    continue
                    
                mem_mb = proc.info['memory_info'].rss / (1024 * 1024)
                cpu = proc.cpu_percent(None)  # % since last call
                
                process_name = proc.info['name'] or 'Unknown'
                processes.append({
                    'pid': proc.info['pid'],
                    'name': process_name,
                    'memory_mb': mem_mb,
                    'cpu_percent': cpu
                })
                
                # Log process details being polled
                self.logger.info(f"Polled process: {process_name} (PID: {proc.info['pid']}) - Memory: {mem_mb:.2f} MB, CPU: {cpu:.1f}%")
                process_count += 1
                
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                error_count += 1
                self.logger.debug(f"Could not access process info: {e}")
            except (AttributeError, TypeError, KeyError) as e:
                error_count += 1
                self.logger.debug(f"Process data error: {e}")
        
        # Sort by memory usage
        top_processes = sorted(processes, key=lambda x: x['memory_mb'], reverse=True)[:limit]
        
        self.logger.debug(f"Monitored {process_count} processes, {error_count} access errors, returning top {len(top_processes)}")
        
        return top_processes
