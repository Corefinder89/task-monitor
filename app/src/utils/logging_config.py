#!/usr/bin/env python3
"""
Example configuration file for task monitor logging
Customize logging behavior for the entire application
"""
import logging
import os
from app.src.utils import TaskMonitorLogger

def configure_logging():
    """Configure logging for the entire task monitor application"""
    
    # Get the base directory for log files
    base_dir = os.path.dirname(os.path.dirname(__file__))
    log_dir = os.path.join(base_dir, 'logs')
    
    # Configure different log levels for different environments
    # Development: DEBUG level with console output
    # Production: INFO level with file output
    
    # Example 1: Development configuration
    TaskMonitorLogger.setup_logging(
        log_level=logging.DEBUG,
        log_file=os.path.join(log_dir, 'task-monitor-debug.log'),
        console_output=True
    )
    
    # Example 2: Production configuration (commented out)
    # TaskMonitorLogger.setup_logging(
    #     log_level=logging.INFO,
    #     log_file=os.path.join(log_dir, 'task-monitor-production.log'),
    #     console_output=False
    # )
    
    # Example 3: High verbosity for troubleshooting (commented out)
    # TaskMonitorLogger.setup_logging(
    #     log_level=logging.DEBUG,
    #     log_file=os.path.join(log_dir, 'task-monitor-verbose.log'),
    #     console_output=True
    # )

def main():
    """Example usage of centralized logging configuration"""
    # Configure logging first
    configure_logging()
    
    # Get different loggers for different components
    csv_logger = TaskMonitorLogger.get_csv_logger()
    process_logger = TaskMonitorLogger.get_process_logger()
    perf_logger = TaskMonitorLogger.get_performance_logger()
    
    # Test logging at different levels
    csv_logger.info("CSV logger initialized")
    process_logger.debug("Process logger debug message")
    perf_logger.warning("Performance logger warning message")
    
    # Show that all loggers use the same configuration
    csv_logger.info("Logging configuration applied successfully")

if __name__ == "__main__":
    main()