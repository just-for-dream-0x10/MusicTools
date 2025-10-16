"""
Custom exception classes for MusicAITools.

This module defines a hierarchy of exceptions used throughout the framework
to provide specific error handling for different types of failures.
"""


class MusicAIToolsException(Exception):
    """
    Base exception class for all MusicAITools related errors.
    
    All custom exceptions in the framework should inherit from this class
    to provide a consistent error handling interface.
    """
    
    def __init__(self, message: str, details: dict = None):
        """
        Initialize the exception with message and optional details.
        
        Args:
            message: Human-readable error description
            details: Additional error context as key-value pairs
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}


class AudioProcessingError(MusicAIToolsException):
    """
    Exception raised when audio processing operations fail.
    
    This includes errors in:
    - Audio loading/saving
    - Signal processing algorithms
    - Format conversion issues
    - Codec problems
    """
    pass


class FileNotFoundError(MusicAIToolsException):
    """
    Exception raised when required files cannot be located.
    
    This covers:
    - Input audio files
    - Configuration files
    - Model files
    - Output directory issues
    """
    pass


class InvalidFormatError(MusicAIToolsException):
    """
    Exception raised when file formats are not supported or invalid.
    
    This includes:
    - Unsupported audio formats
    - Corrupted file headers
    - Invalid metadata
    - Encoding issues
    """
    pass


class ConfigurationError(MusicAIToolsException):
    """
    Exception raised when configuration parameters are invalid.
    
    This covers:
    - Invalid parameter values
    - Missing required configuration
    - Configuration file parsing errors
    - Environment setup issues
    """
    pass


class ModelLoadError(MusicAIToolsException):
    """
    Exception raised when machine learning models fail to load.
    
    This includes:
    - Missing model files
    - Incompatible model versions
    - GPU/CPU compatibility issues
    - Memory allocation failures
    """
    pass


class ValidationError(MusicAIToolsException):
    """
    Exception raised when data validation fails.
    
    This covers:
    - Invalid input parameters
    - Data type mismatches
    - Range validation failures
    - Schema validation errors
    """
    pass