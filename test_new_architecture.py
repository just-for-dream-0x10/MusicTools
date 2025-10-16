#!/usr/bin/env python3
"""
Test script for new MusicAITools architecture.

This script validates the core components and demonstrates
the improved error handling, logging, and configuration system.
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
    """Test the unified logging system."""
    print("=" * 50)
    print("Testing Logging System")
    print("=" * 50)
    
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
    
    print("✅ Logging system test completed")
    return True


def test_configuration_system():
    """Test the configuration management system."""
    print("\n" + "=" * 50)
    print("Testing Configuration System")
    print("=" * 50)
    
    try:
        # Load default configuration
        config = get_config()
        
        print(f"Audio restoration noise reduction: {config.audio_restoration.noise_reduction}")
        print(f"System output directory: {config.system.output_dir}")
        print(f"Visualization DPI: {config.visualization.dpi}")
        
        # Test configuration validation
        config.validate()
        print("✅ Configuration validation passed")
        
        # Test invalid configuration
        try:
            config.audio_restoration.noise_reduction = 2.0  # Invalid value
            config.validate()
            print("❌ Configuration validation should have failed")
            return False
        except Exception as e:
            print(f"✅ Configuration validation correctly caught error: {e}")
            # Reset to valid value
            config.audio_restoration.noise_reduction = 0.2
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False


def test_data_models():
    """Test the data model classes."""
    print("\n" + "=" * 50)
    print("Testing Data Models")
    print("=" * 50)
    
    try:
        # Test AudioFile model
        audio_file = AudioFile(
            path=Path("test_audio.wav"),
            sample_rate=44100,
            duration=30.0,
            channels=2
        )
        
        print(f"AudioFile created: {audio_file.path}")
        print(f"Sample rate: {audio_file.sample_rate}")
        print(f"Duration: {audio_file.duration}s")
        
        # Test ProcessingResult models
        from modules.core.models import ProcessingResult, RestorationResult
        
        result = ProcessingResult(
            status=ProcessingStatus.SUCCESS,
            output_files=[Path("output.wav")],
            metadata={"test": "value"}
        )
        
        print(f"ProcessingResult status: {result.status}")
        print(f"Success: {result.success}")
        
        # Test RestorationResult
        restoration_result = RestorationResult(
            status=ProcessingStatus.SUCCESS,
            output_files=[Path("restored.wav")],
            metadata={},
            restored_file=Path("restored.wav"),
            improvement_metrics={"snr_improvement_db": 5.2}
        )
        
        print(f"Restoration improvement: {restoration_result.get_improvement('snr_improvement_db')}dB")
        
        print("✅ Data models test completed")
        return True
        
    except Exception as e:
        print(f"❌ Data models test failed: {e}")
        return False


def test_exception_handling():
    """Test the exception handling system."""
    print("\n" + "=" * 50)
    print("Testing Exception Handling")
    print("=" * 50)
    
    try:
        # Test custom exceptions
        try:
            raise AudioProcessingError("Test audio processing error", {"context": "testing"})
        except MusicAIToolsException as e:
            print(f"✅ Caught MusicAIToolsException: {e.message}")
            print(f"✅ Exception details: {e.details}")
        
        try:
            raise AudioProcessingError("Test without details")
        except AudioProcessingError as e:
            print(f"✅ Caught AudioProcessingError: {e}")
        
        print("✅ Exception handling test completed")
        return True
        
    except Exception as e:
        print(f"❌ Exception handling test failed: {e}")
        return False


def test_audio_restoration_service():
    """Test the audio restoration service (without actual audio file)."""
    print("\n" + "=" * 50)
    print("Testing Audio Restoration Service")
    print("=" * 50)
    
    try:
        # Initialize service
        restoration_service = AudioRestorationService()
        
        print(f"Service name: {restoration_service.service_name}")
        print(f"Service stats: {restoration_service.get_stats()}")
        
        # Test settings validation
        try:
            invalid_settings = {"noise_reduction": 2.0}  # Invalid value
            restoration_service._validate_settings(invalid_settings)
            print("❌ Settings validation should have failed")
            return False
        except Exception as e:
            print(f"✅ Settings validation correctly caught error: {e}")
        
        # Test valid settings
        valid_settings = {
            "noise_reduction": 0.3,
            "eq_low": 1.1,
            "eq_mid": 1.0,
            "eq_high": 1.2,
            "compression_ratio": 2.0
        }
        restoration_service._validate_settings(valid_settings)
        print("✅ Valid settings passed validation")
        
        # Test with non-existent file (should handle gracefully)
        try:
            result = restoration_service.safe_process("nonexistent_file.wav")
            if result.failed:
                print(f"✅ Service correctly handled missing file: {result.error_message}")
            else:
                print("❌ Service should have failed with missing file")
                return False
        except Exception as e:
            print(f"❌ Unexpected exception: {e}")
            return False
        
        print("✅ Audio restoration service test completed")
        return True
        
    except Exception as e:
        print(f"❌ Audio restoration service test failed: {e}")
        return False


def run_all_tests():
    """Run all architecture tests."""
    print("🚀 Starting MusicAITools New Architecture Tests")
    print("=" * 60)
    
    tests = [
        test_logging_system,
        test_configuration_system,
        test_data_models,
        test_exception_handling,
        test_audio_restoration_service
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_func in tests:
        try:
            if test_func():
                passed_tests += 1
            else:
                print(f"❌ Test {test_func.__name__} failed")
        except Exception as e:
            print(f"❌ Test {test_func.__name__} crashed: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! New architecture is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please review the output above.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)