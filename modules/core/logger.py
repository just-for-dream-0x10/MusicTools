"""
Unified logging system for MusicAITools.

This module provides a centralized logging configuration that ensures
consistent log formatting and handling across all components.
"""

import logging
import sys
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime


class MusicAILogger:
    """
    Singleton logger manager for the MusicAITools framework.
    
    Provides centralized logging configuration with support for:
    - Console and file output
    - Configurable log levels
    - Structured log formatting
    - Performance monitoring
    """
    
    _instance = None
    _logger = None
    
    def __new__(cls):
        """
        Implement singleton pattern to ensure single logger instance.
        
        Returns:
            MusicAILogger instance
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def setup_logger(self, 
                    name: str = "musicaitools",
                    level: int = logging.INFO,
                    log_file: Optional[Path] = None,
                    format_string: Optional[str] = None) -> logging.Logger:
        """
        Configure and initialize the logging system.
        
        Args:
            name: Logger name identifier
            level: Minimum logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Optional file path for log output
            format_string: Custom log format string
            
        Returns:
            Configured logger instance
        """
        if self._logger is not None:
            return self._logger
            
        self._logger = logging.getLogger(name)
        self._logger.setLevel(level)
        
        # Clear any existing handlers to prevent duplication
        self._logger.handlers.clear()
        
        # Default format includes timestamp, level, module, and message
        if format_string is None:
            format_string = (
                '%(asctime)s - %(name)s - %(levelname)s - '
                '%(module)s:%(funcName)s:%(lineno)d - %(message)s'
            )
        
        formatter = logging.Formatter(format_string)
        
        # Console handler for immediate feedback
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)
        
        # File handler for persistent logging
        if log_file:
            log_file = Path(log_file)
            log_file.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            self._logger.addHandler(file_handler)
        
        # Log the initialization
        self._logger.info(f"Logger initialized with level: {logging.getLevelName(level)}")
        
        return self._logger
    
    def get_logger(self) -> logging.Logger:
        """
        Get the current logger instance.
        
        Returns:
            Logger instance, creating default if none exists
        """
        if self._logger is None:
            return self.setup_logger()
        return self._logger
    
    def log_performance(self, operation: str, duration: float, details: Dict[str, Any] = None):
        """
        Log performance metrics for operations.
        
        Args:
            operation: Name of the operation being measured
            duration: Time taken in seconds
            details: Additional performance context
        """
        details_str = ""
        if details:
            details_str = " | " + " | ".join(f"{k}: {v}" for k, v in details.items())
            
        self._logger.info(f"PERFORMANCE: {operation} completed in {duration:.3f}s{details_str}")
    
    def log_error_with_context(self, error: Exception, context: Dict[str, Any] = None):
        """
        Log errors with additional context information.
        
        Args:
            error: Exception that occurred
            context: Additional context about the error
        """
        context_str = ""
        if context:
            context_str = " | Context: " + str(context)
            
        self._logger.error(f"Error: {type(error).__name__}: {str(error)}{context_str}")


# Global logger instance for convenience
_global_logger = MusicAILogger()


def get_logger() -> logging.Logger:
    """
    Get the global logger instance.
    
    Returns:
        Configured logger instance
    """
    return _global_logger.get_logger()


def setup_logging(level: int = logging.INFO, 
                 log_file: Optional[Path] = None) -> logging.Logger:
    """
    Setup global logging configuration.
    
    Args:
        level: Minimum logging level
        log_file: Optional file path for log output
        
    Returns:
        Configured logger instance
    """
    return _global_logger.setup_logger(level=level, log_file=log_file)


def log_performance(operation: str, duration: float, details: Dict[str, Any] = None):
    """
    Log performance metrics for operations.
    
    Args:
        operation: Name of the operation being measured
        duration: Time taken in seconds  
        details: Additional performance context
    """
    _global_logger.log_performance(operation, duration, details)


def log_error_with_context(error: Exception, context: Dict[str, Any] = None):
    """
    Log errors with additional context information.
    
    Args:
        error: Exception that occurred
        context: Additional context about the error
    """
    _global_logger.log_error_with_context(error, context)