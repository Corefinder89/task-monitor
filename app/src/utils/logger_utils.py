"""
Centralized logging utility for the task monitor application
"""
import logging
import os
from datetime import datetime


class TaskMonitorLogger:
    """Centralized logger for task monitor application"""
    
    _loggers = {}
    _configured = False
    
    @classmethod
    def setup_logging(cls, log_level=logging.INFO, log_file=None, console_output=True):
        """
        Setup global logging configuration
        
        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Optional file path for logging output
            console_output: Whether to output logs to console
        """
        if cls._configured:
            return
            
        # Create logs directory if logging to file
        if log_file:
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)
        
        # Clear existing handlers
        root_logger.handlers = []
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Add console handler if requested
        if console_output:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)
        
        # Add file handler if requested
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        
        cls._configured = True
    
    @classmethod
    def get_logger(cls, name):
        """
        Get a logger instance for a specific module
        
        Args:
            name: Logger name (usually __name__ of the module)
            
        Returns:
            Logger instance
        """
        if name not in cls._loggers:
            # Setup default logging if not configured
            if not cls._configured:
                cls.setup_logging()
            
            cls._loggers[name] = logging.getLogger(name)
        
        return cls._loggers[name]
    
    @classmethod
    def get_performance_logger(cls):
        """Get a specific logger for performance monitoring"""
        return cls.get_logger('performance_monitor')
    
    @classmethod
    def get_csv_logger(cls):
        """Get a specific logger for CSV operations"""
        return cls.get_logger('csv_converter')
    
    @classmethod
    def get_process_logger(cls):
        """Get a specific logger for process monitoring"""
        return cls.get_logger('process_monitor')


# Convenience functions for quick access
def get_logger(name=None):
    """
    Convenience function to get a logger
    
    Args:
        name: Logger name (defaults to calling module)
        
    Returns:
        Logger instance
    """
    if name is None:
        # Try to get the calling module's name
        import inspect
        frame = inspect.currentframe().f_back
        name = frame.f_globals.get('__name__', 'task_monitor')
    
    return TaskMonitorLogger.get_logger(name)


def setup_logging(log_level=logging.INFO, log_file=None, console_output=True):
    """
    Convenience function to setup logging
    
    Args:
        log_level: Logging level
        log_file: Optional log file path
        console_output: Whether to output to console
    """
    TaskMonitorLogger.setup_logging(log_level, log_file, console_output)


# Default configuration - can be overridden
if not TaskMonitorLogger._configured:
    setup_logging(
        log_level=logging.INFO,
        log_file=os.path.join(os.path.dirname(__file__), '..', '..', 'logs', 'task-monitor.log'),
        console_output=True
    )