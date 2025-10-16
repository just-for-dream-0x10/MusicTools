#!/usr/bin/env python3
"""
Test MusicAITools with instrumental.wav file

Simple test script using the provided instrumental.wav file.
"""

import sys
from pathlib import Path

# Add MusicAITools to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from modules.core import get_logger, get_config
    from modules.audio.restoration_service import AudioRestorationService
    print("✅ Successfully imported MusicAITools modules")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure you're running from the MusicAITools directory")
    sys.exit(1)


def test_basic_restoration():
    """Test basic audio restoration with instrumental.wav"""
    print("=" * 60)
    print("🎵 Testing Audio Restoration with instrumental.wav")
    print("=" * 60)
    
    # Check for test file
    test_file = Path("docs/examples/instrumental.wav")
    if not test_file.exists():
        print(f"❌ Test file not found: {test_file}")
        print("💡 Please ensure instrumental.wav is in docs/examples/ directory")
        return False
    
    print(f"✅ Found test file: {test_file}")
    print(f"📁 File size: {test_file.stat().st_size / (1024*1024):.2f} MB")
    
    # Initialize service
    service = AudioRestorationService()
    print(f"🔧 Initialized {service.service_name} service")
    
    # Process with default settings
    print("🎯 Processing with default settings...")
    result = service.safe_process(str(test_file))
    
    if result.success:
        print("🎉 Processing completed successfully!")
        print(f"📤 Output file: {result.restored_file}")
        print(f"⏱️  Processing time: {result.processing_time:.2f}s")
        
        # Show improvement metrics
        print("\n📊 Improvement Metrics:")
        for metric, value in result.improvement_metrics.items():
            print(f"  {metric}: {value:.3f}")
        
        if result.overall_improvement:
            print(f"\n⭐ Overall quality score: {result.overall_improvement:.1f}/100")
        
        return True
    else:
        print(f"❌ Processing failed: {result.error_message}")
        return False


def test_custom_settings():
    """Test with custom restoration settings"""
    print("\n" + "=" * 60)
    print("🎛️  Testing Custom Settings")
    print("=" * 60)
    
    test_file = Path("docs/examples/instrumental.wav")
    if not test_file.exists():
        print(f"❌ Test file not found: {test_file}")
        return False
    
    service = AudioRestorationService()
    
    # Custom settings for music enhancement
    custom_settings = {
        "noise_reduction": 0.3,
        "eq_low": 1.1,      # Slight bass boost
        "eq_mid": 1.0,      # Keep mids neutral
        "eq_high": 1.2,     # Enhance treble for clarity
        "enable_spectral_gating": True
    }
    
    print(f"🎛️  Custom settings: {custom_settings}")
    
    result = service.safe_process(
        str(test_file),
        custom_settings=custom_settings
    )
    
    if result.success:
        print("🎉 Custom processing completed!")
        print(f"📤 Output file: {result.restored_file}")
        print(f"⏱️  Processing time: {result.processing_time:.2f}s")
        
        print("\n📊 Quality Improvements:")
        for metric, value in result.improvement_metrics.items():
            print(f"  {metric}: {value:.3f}")
        
        return True
    else:
        print(f"❌ Custom processing failed: {result.error_message}")
        return False


def test_service_stats():
    """Test service statistics tracking"""
    print("\n" + "=" * 60)
    print("📈 Testing Service Statistics")
    print("=" * 60)
    
    service = AudioRestorationService()
    
    # Get initial stats
    initial_stats = service.get_stats()
    print(f"📊 Initial stats: {initial_stats}")
    
    # Process file to generate stats
    test_file = Path("docs/examples/instrumental.wav")
    if test_file.exists():
        print("🎯 Processing file to generate statistics...")
        result = service.safe_process(str(test_file))
        
        # Get updated stats
        final_stats = service.get_stats()
        print(f"\n📊 Final statistics:")
        print(f"  Total operations: {final_stats['total_operations']}")
        print(f"  Successful operations: {final_stats['successful_operations']}")
        print(f"  Success rate: {final_stats['success_rate']:.1f}%")
        print(f"  Average processing time: {final_stats['average_processing_time']:.3f}s")
        
        return True
    else:
        print("❌ Test file not available for statistics test")
        return False


def test_error_handling():
    """Test error handling capabilities"""
    print("\n" + "=" * 60)
    print("🚨 Testing Error Handling")
    print("=" * 60)
    
    service = AudioRestorationService()
    
    # Test 1: Non-existent file
    print("🧪 Test 1: Non-existent file")
    result = service.safe_process("nonexistent_file.wav")
    if result.failed:
        print(f"✅ Correctly handled missing file: {result.error_message}")
    else:
        print("❌ Should have failed with missing file")
    
    # Test 2: Invalid settings
    print("\n🧪 Test 2: Invalid settings")
    invalid_settings = {"noise_reduction": 2.0}  # Invalid range
    
    try:
        service._validate_settings(invalid_settings)
        print("❌ Should have failed validation")
    except Exception as e:
        print(f"✅ Correctly caught invalid settings: {e}")
    
    return True


def run_all_tests():
    """Run all test functions"""
    logger = get_logger()
    logger.info("🚀 Starting MusicAITools tests with instrumental.wav")
    
    tests = [
        ("Basic Restoration", test_basic_restoration),
        ("Custom Settings", test_custom_settings),
        ("Service Statistics", test_service_stats),
        ("Error Handling", test_error_handling)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            print(f"\n🧪 Running: {test_name}")
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"💥 {test_name}: ERROR - {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! MusicAITools is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above.")
    
    return passed == total


if __name__ == "__main__":
    print("🎵 MusicAITools Test with instrumental.wav")
    print("=" * 60)
    
    # Check configuration
    try:
        config = get_config()
        print(f"⚙️  Configuration loaded successfully")
        print(f"📁 Output directory: {config.system.output_dir}")
        print(f"📊 Log level: {config.system.log_level}")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
    
    # Run tests
    success = run_all_tests()
    
    sys.exit(0 if success else 1)