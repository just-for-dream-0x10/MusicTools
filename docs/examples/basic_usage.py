#!/usr/bin/env python3
"""
Basic Usage Examples for MusicAITools

This script demonstrates the fundamental usage patterns of the MusicAITools framework.
"""

import sys
from pathlib import Path

# Add MusicAITools to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.core import get_logger, get_config
from modules.audio.restoration_service import AudioRestorationService


def example_1_basic_restoration():
    """Example 1: Basic audio restoration"""
    print("=" * 50)
    print("Example 1: Basic Audio Restoration")
    print("=" * 50)
    
    # Initialize service
    service = AudioRestorationService()
    
    # Process audio with default settings
    result = service.safe_process("sample_audio.wav")
    
    if result.success:
        print(f"✅ Restoration completed!")
        print(f"Output file: {result.restored_file}")
        print(f"Processing time: {result.processing_time:.2f}s")
        
        # Display improvement metrics
        snr_improvement = result.get_improvement("snr_improvement_db")
        if snr_improvement:
            print(f"SNR improvement: {snr_improvement:.2f}dB")
            
    else:
        print(f"❌ Processing failed: {result.error_message}")


def example_2_custom_settings():
    """Example 2: Custom restoration settings"""
    print("\n" + "=" * 50)
    print("Example 2: Custom Restoration Settings")
    print("=" * 50)
    
    service = AudioRestorationService()
    
    # Define custom settings for noisy audio
    custom_settings = {
        "noise_reduction": 0.4,        # Stronger noise reduction
        "eq_low": 1.3,                 # Boost bass
        "eq_mid": 0.9,                 # Slightly reduce midrange
        "eq_high": 1.2,                # Enhance treble
        "enable_spectral_gating": True, # Advanced noise suppression
        "compression_ratio": 2.5        # Light compression
    }
    
    result = service.safe_process(
        "noisy_audio.wav",
        output_file="enhanced_audio.wav",
        custom_settings=custom_settings
    )
    
    if result.success:
        print(f"✅ Custom processing completed!")
        print(f"Settings used: {result.restoration_settings}")
        
        # Show all improvement metrics
        print("\nImprovement Metrics:")
        for metric, value in result.improvement_metrics.items():
            print(f"  {metric}: {value:.3f}")
            
    else:
        print(f"❌ Processing failed: {result.error_message}")


def example_3_batch_processing():
    """Example 3: Batch processing multiple files"""
    print("\n" + "=" * 50)
    print("Example 3: Batch Processing")
    print("=" * 50)
    
    service = AudioRestorationService()
    
    # List of audio files to process
    audio_files = [
        "audio1.wav",
        "audio2.wav", 
        "audio3.wav"
    ]
    
    # Settings for podcast enhancement
    podcast_settings = {
        "noise_reduction": 0.3,
        "eq_mid": 1.2,  # Boost speech frequencies
        "enable_dynamic_range_compression": True,
        "compression_ratio": 3.0
    }
    
    # Process all files
    batch_result = service.process_batch(
        audio_files,
        custom_settings=podcast_settings
    )
    
    print(f"📊 Batch Processing Results:")
    print(f"Total files: {batch_result.total_files}")
    print(f"Successful: {batch_result.successful_files}")
    print(f"Failed: {batch_result.failed_files}")
    print(f"Success rate: {batch_result.success_rate:.1f}%")
    print(f"Average time: {batch_result.average_processing_time:.2f}s")
    
    # Review failed files
    failed_results = batch_result.get_failed_results()
    if failed_results:
        print("\n❌ Failed Files:")
        for result in failed_results:
            print(f"  - {result.error_message}")


def example_4_configuration():
    """Example 4: Working with configuration"""
    print("\n" + "=" * 50)
    print("Example 4: Configuration Management")
    print("=" * 50)
    
    # Get current configuration
    config = get_config()
    
    print("Current Configuration:")
    print(f"  Noise reduction: {config.audio_restoration.noise_reduction}")
    print(f"  Output directory: {config.system.output_dir}")
    print(f"  Log level: {config.system.log_level}")
    print(f"  Max workers: {config.system.max_workers}")
    
    # Modify configuration at runtime
    print("\nModifying configuration...")
    config.audio_restoration.noise_reduction = 0.3
    config.system.output_dir = "custom_output"
    
    # Validate changes
    try:
        config.validate()
        print("✅ Configuration changes are valid")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
    
    # Use modified configuration
    service = AudioRestorationService()
    result = service.safe_process("audio.wav")
    
    if result.success:
        print(f"✅ Processed with modified config")
        print(f"Output saved to: {result.restored_file}")


def example_5_error_handling():
    """Example 5: Error handling and logging"""
    print("\n" + "=" * 50)
    print("Example 5: Error Handling")
    print("=" * 50)
    
    logger = get_logger()
    service = AudioRestorationService()
    
    # Test with non-existent file
    logger.info("Testing error handling with missing file...")
    result = service.safe_process("nonexistent_file.wav")
    
    if result.failed:
        print(f"✅ Error handled gracefully: {result.error_message}")
        logger.warning(f"Processing failed as expected: {result.error_message}")
    
    # Test with invalid settings
    logger.info("Testing with invalid settings...")
    invalid_settings = {
        "noise_reduction": 2.0  # Invalid value (must be 0.0-1.0)
    }
    
    try:
        result = service.safe_process("audio.wav", custom_settings=invalid_settings)
        if result.failed:
            print(f"✅ Invalid settings handled: {result.error_message}")
    except Exception as e:
        print(f"✅ Exception caught: {e}")
    
    # Show service statistics
    stats = service.get_stats()
    print(f"\nService Statistics:")
    print(f"  Total operations: {stats['total_operations']}")
    print(f"  Success rate: {stats['success_rate']:.1f}%")
    print(f"  Average time: {stats['average_processing_time']:.2f}s")


def example_6_performance_monitoring():
    """Example 6: Performance monitoring"""
    print("\n" + "=" * 50)
    print("Example 6: Performance Monitoring")
    print("=" * 50)
    
    from modules.core.logger import log_performance
    import time
    
    logger = get_logger()
    service = AudioRestorationService()
    
    # Monitor overall processing
    start_time = time.time()
    
    result = service.safe_process("audio.wav")
    
    total_time = time.time() - start_time
    
    # Log performance metrics
    log_performance(
        "complete_workflow", 
        total_time,
        {
            "file_size_mb": 10.5,
            "success": result.success,
            "improvement_score": result.overall_improvement or 0
        }
    )
    
    print(f"📊 Performance Analysis:")
    print(f"  Total workflow time: {total_time:.2f}s")
    print(f"  Processing time: {result.processing_time:.2f}s")
    print(f"  Overhead time: {total_time - (result.processing_time or 0):.2f}s")
    
    # Service-level statistics
    stats = service.get_stats()
    print(f"  Service efficiency: {stats['average_processing_time']:.2f}s avg")


def run_all_examples():
    """Run all examples"""
    logger = get_logger()
    logger.info("🚀 Starting MusicAITools Examples")
    
    try:
        example_1_basic_restoration()
        example_2_custom_settings()
        example_3_batch_processing()
        example_4_configuration()
        example_5_error_handling()
        example_6_performance_monitoring()
        
        print("\n" + "=" * 50)
        print("🎉 All examples completed!")
        print("=" * 50)
        
    except Exception as e:
        logger.error(f"Example execution failed: {e}")
        print(f"❌ Error running examples: {e}")


if __name__ == "__main__":
    # Note: This example uses placeholder audio files
    print("📖 MusicAITools Basic Usage Examples")
    print("Note: Replace 'sample_audio.wav' etc. with actual audio files")
    print("")
    
    # For demonstration, we'll show the code structure
    # In real usage, provide actual audio files
    
    run_all_examples()