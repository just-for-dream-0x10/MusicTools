"""
Core module for MusicAITools framework.

This module provides fundamental components including:
- Exception handling
- Logging system  
- Configuration management
- Data models
- Base service classes
"""

from .exceptions import (
    MusicAIToolsException,
    AudioProcessingError,
    FileNotFoundError,
    InvalidFormatError
)

from .logger import MusicAILogger, get_logger, setup_logging

from .config import (
    AudioRestorationConfig,
    AudioSeparationConfig, 
    VisualizationConfig,
    MusicAIConfig,
    ConfigManager,
    get_config
)

from .models import (
    AudioFile,
    ProcessingResult,
    SeparationResult,
    RestorationResult,
    ConversionResult,
    VisualizationResult,
    AudioFormat,
    ProcessingStatus
)

from .base_service import BaseService

__all__ = [
    # Exceptions
    'MusicAIToolsException',
    'AudioProcessingError', 
    'FileNotFoundError',
    'InvalidFormatError',
    
    # Logging
    'MusicAILogger',
    'get_logger',
    'setup_logging',
    
    # Configuration
    'AudioRestorationConfig',
    'AudioSeparationConfig',
    'VisualizationConfig', 
    'MusicAIConfig',
    'ConfigManager',
    'get_config',
    
    # Models
    'AudioFile',
    'ProcessingResult',
    'SeparationResult',
    'RestorationResult',
    'ConversionResult',
    'VisualizationResult',
    'AudioFormat',
    'ProcessingStatus',
    
    # Base classes
    'BaseService'
]