#!/usr/bin/env python3
"""
Simple demonstration script for new MusicAITools architecture.

This script provides a basic demonstration of the core components.
For comprehensive testing, use tests/test_core_architecture.py instead.
"""

import sys
import logging
from pathlib import Path

# Add modules to path for testing
sys.path.insert(0, str(Path(__file__).parent))

from modules.core import (
    get_logger, get_config, setup_logging,
    MusicAIToolsException, AudioProcessingError,
    AudioFile, ProcessingStatus
)
from modules.audio.restoration_service import AudioRestorationService


def test_logging_system():
    """Demonstrate the unified logging system."""
    logger = get_logger()
    logger.info("=" * 50)
    logger.info("Demonstrating Logging System")
    logger.info("=" * 50)
    
    # Setup logging with debug level for testing
    logger = setup_logging(level=logging.DEBUG)
    
    logger.info("Testing info level logging")
    logger.debug("Testing debug level logging")
    logger.warning("Testing warning level logging")
    
    # Test performance logging
    from modules.core.logger import log_performance
    log_performance("test_operation", 1.234, {"files_processed": 5})
    
    # Test error logging with context
    from modules.core.logger import log_error_with_context
    test_error = ValueError("Test error for logging")
    log_error_with_context(test_error, {"context": "testing", "module": "test"})
    
    logger.info("✅ Logging system demonstration completed")
    return True


def test_configuration_system():
    """Demonstrate the configuration management system."""
    logger = get_logger()
    logger.info("=" * 50)
    logger.info("Demonstrating Configuration System")
    logger.info("=" * 50)
    
    try:
        # Load default configuration
        config = get_config()
        
        logger.info(f"Audio restoration noise reduction: {config.audio_restoration.noise_reduction}")
        logger.info(f"System output directory: {config.system.output_dir}")
        logger.info(f"Visualization DPI: {config.visualization.dpi}")
        
        # Test configuration validation
        config.validate()
        logger.info("✅ Configuration validation passed")
        
        # Test invalid configuration
        try:
            config.audio_restoration.noise_reduction = 2.0  # Invalid value
            config.validate()
            logger.error("❌ Configuration validation should have failed")
            return False
        except Exception as e:
            logger.info(f"✅ Configuration validation correctly caught error: {e}")
            # Reset to valid value
            config.audio_restoration.noise_reduction = 0.2
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Configuration demonstration failed: {e}")
        return False


def test_data_models():
    """Demonstrate the data model classes."""
    logger = get_logger()
    logger.info("=" * 50)
    logger.info("Demonstrating Data Models")
    logger.info("=" * 50)
    
    try:
        # Test AudioFile model
        audio_file = AudioFile(
            path=Path("test_audio.wav"),
            sample_rate=44100,
            duration=30.0,
            channels=2
        )
        
        logger.info(f"AudioFile created: {audio_file.path}")
        logger.info(f"Sample rate: {audio_file.sample_rate}")
        logger.info(f"Duration: {audio_file.duration}s")
        
        # Test ProcessingResult models
        from modules.core.models import ProcessingResult, RestorationResult
        
        result = ProcessingResult(
            status=ProcessingStatus.SUCCESS,
            output_files=[Path("output.wav")],
            metadata={"test": "value"}
        )
        
        logger.info(f"ProcessingResult status: {result.status}")
        logger.info(f"Success: {result.success}")
        
        # Test RestorationResult
        restoration_result = RestorationResult(
            status=ProcessingStatus.SUCCESS,
            output_files=[Path("restored.wav")],
            metadata={},
            restored_file=Path("restored.wav"),
            improvement_metrics={"snr_improvement_db": 5.2}
        )
        
        logger.info(f"Restoration improvement: {restoration_result.get_improvement('snr_improvement_db')}dB")
        
        logger.info("✅ Data models demonstration completed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Data models demonstration failed: {e}")
        return False


def test_exception_handling():
    """Demonstrate the exception handling system."""
    logger = get_logger()
    logger.info("=" * 50)
    logger.info("Demonstrating Exception Handling")
    logger.info("=" * 50)
    
    try:
        # Test custom exceptions
        try:
            raise AudioProcessingError("Test audio processing error", {"context": "testing"})
        except MusicAIToolsException as e:
            logger.info(f"✅ Caught MusicAIToolsException: {e.message}")
            logger.info(f"✅ Exception details: {e.details}")
        
        try:
            raise AudioProcessingError("Test without details")
        except AudioProcessingError as e:
            logger.info(f"✅ Caught AudioProcessingError: {e}")
        
        logger.info("✅ Exception handling demonstration completed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Exception handling demonstration failed: {e}")
        return False


def test_audio_restoration_service():
    """Demonstrate the audio restoration service (without actual audio file)."""
    logger = get_logger()
    logger.info("=" * 50)
    logger.info("Demonstrating Audio Restoration Service")
    logger.info("=" * 50)
    
    try:
        # Initialize service
        restoration_service = AudioRestorationService()
        
        logger.info(f"Service name: {restoration_service.service_name}")
        logger.info(f"Service stats: {restoration_service.get_stats()}")
        
        # Test settings validation
        try:
            invalid_settings = {"noise_reduction": 2.0}  # Invalid value
            restoration_service._validate_settings(invalid_settings)
            logger.error("❌ Settings validation should have failed")
            return False
        except Exception as e:
            logger.info(f"✅ Settings validation correctly caught error: {e}")
        
        # Test valid settings
        valid_settings = {
            "noise_reduction": 0.3,
            "eq_low": 1.1,
            "eq_mid": 1.0,
            "eq_high": 1.2,
            "compression_ratio": 2.0
        }
        restoration_service._validate_settings(valid_settings)
        logger.info("✅ Valid settings passed validation")
        
        # Test with non-existent file (should handle gracefully)
        try:
            result = restoration_service.safe_process("nonexistent_file.wav")
            if result.failed:
                logger.info(f"✅ Service correctly handled missing file: {result.error_message}")
            else:
                logger.error("❌ Service should have failed with missing file")
                return False
        except Exception as e:
            logger.error(f"❌ Unexpected exception: {e}")
            return False
        
        logger.info("✅ Audio restoration service demonstration completed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Audio restoration service demonstration failed: {e}")
        return False


def run_all_demonstrations():
    """Run all architecture demonstrations."""
    logger = get_logger()
    logger.info("🚀 Starting MusicAITools New Architecture Demonstrations")
    logger.info("=" * 60)
    logger.info("Note: For comprehensive testing, use 'python -m pytest tests/test_core_architecture.py'")
    
    demonstrations = [
        test_logging_system,
        test_configuration_system,
        test_data_models,
        test_exception_handling,
        test_audio_restoration_service
    ]
    
    passed_demos = 0
    total_demos = len(demonstrations)
    
    for demo_func in demonstrations:
        try:
            if demo_func():
                passed_demos += 1
            else:
                logger.warning(f"❌ Demonstration {demo_func.__name__} failed")
        except Exception as e:
            logger.error(f"❌ Demonstration {demo_func.__name__} crashed: {e}")
    
    logger.info("=" * 60)
    logger.info(f"📊 Demonstration Results: {passed_demos}/{total_demos} demonstrations completed")
    
    if passed_demos == total_demos:
        logger.info("🎉 All demonstrations completed! New architecture is working correctly.")
        return True
    else:
        logger.warning("⚠️  Some demonstrations failed. Please review the output above.")
        return False


if __name__ == "__main__":
    success = run_all_demonstrations()
    sys.exit(0 if success else 1)