# 🚀 Quick Start Guide

Get up and running with MusicAITools in just a few minutes!

## 🎯 Prerequisites

- Python 3.8+ 
- Conda environment (recommended: `myenv`)
- Audio files to process

## 📦 Installation

```bash
# Activate conda environment
conda activate myenv

# Install dependencies
pip install -r requirements.txt

# Verify installation
python test_new_architecture.py
```

## 🎵 Your First Audio Restoration

### Step 1: Basic Usage

```python
from modules.audio.restoration_service import AudioRestorationService

# Initialize the service
service = AudioRestorationService()

# Process an audio file
result = service.safe_process("your_audio.wav")

# Check results
if result.success:
    print(f"✅ Restoration completed!")
    print(f"Output: {result.restored_file}")
    print(f"SNR improvement: {result.get_improvement('snr_improvement_db'):.2f}dB")
else:
    print(f"❌ Processing failed: {result.error_message}")
```

### Step 2: Custom Settings

```python
# Define custom restoration settings
custom_settings = {
    "noise_reduction": 0.4,        # Stronger noise reduction
    "eq_low": 1.3,                 # Boost bass frequencies
    "eq_mid": 0.9,                 # Slightly reduce midrange
    "eq_high": 1.2,                # Enhance treble
    "enable_spectral_gating": True, # Advanced noise suppression
    "compression_ratio": 2.5        # Dynamic range compression
}

# Apply custom settings
result = service.safe_process(
    "your_audio.wav",
    output_file="enhanced_audio.wav",
    custom_settings=custom_settings
)
```

### Step 3: Batch Processing

```python
import glob

# Get all audio files
audio_files = glob.glob("*.wav")

# Process all files
batch_result = service.process_batch(
    audio_files,
    custom_settings={"noise_reduction": 0.3}
)

print(f"Processed {batch_result.total_files} files")
print(f"Success rate: {batch_result.success_rate:.1f}%")
```

## 🔧 Configuration

### Using Configuration Files

Create a `config.yaml` file:

```yaml
audio_restoration:
  noise_reduction: 0.3
  eq_low: 1.2
  eq_mid: 1.0
  eq_high: 1.1
  enable_spectral_gating: true

system:
  output_dir: "enhanced_audio"
  log_level: "INFO"
```

Load and use the configuration:

```python
from modules.core import get_config

# Load configuration
config = get_config()

# Access settings
print(f"Noise reduction: {config.audio_restoration.noise_reduction}")
print(f"Output directory: {config.system.output_dir}")
```

### Environment Variables

Override settings with environment variables:

```bash
export MUSICAI_AUDIO_RESTORATION_NOISE_REDUCTION=0.5
export MUSICAI_SYSTEM_OUTPUT_DIR="my_output"
```

## 📊 Understanding Results

### Processing Result Structure

```python
# Successful result
if result.success:
    print(f"Status: {result.status}")
    print(f"Output files: {result.output_files}")
    print(f"Processing time: {result.processing_time:.2f}s")
    
    # Restoration-specific results
    print(f"Restored file: {result.restored_file}")
    
    # Quality improvements
    for metric, value in result.improvement_metrics.items():
        print(f"{metric}: {value:.3f}")

# Failed result
else:
    print(f"Error: {result.error_message}")
    print(f"Processing time: {result.processing_time:.2f}s")
```

### Quality Metrics Explained

- **SNR Improvement (dB)**: Signal-to-noise ratio enhancement
- **THD Improvement**: Total harmonic distortion reduction
- **Spectral Flatness**: Measure of noise vs. tonal content
- **Dynamic Range**: Peak-to-RMS ratio improvement
- **Overall Quality Score**: Weighted combination (0-100)

## 🧪 Testing Your Setup

### Run Built-in Tests

```bash
# Comprehensive test suite
python tests/test_core_architecture.py

# Simple demonstrations
python test_new_architecture.py
```

### Validate Configuration

```python
from modules.core import get_config

try:
    config = get_config()
    config.validate()
    print("✅ Configuration is valid")
except Exception as e:
    print(f"❌ Configuration error: {e}")
```

## 📈 Performance Tips

### 1. Audio File Formats
- **Best**: WAV, FLAC (lossless)
- **Good**: High-bitrate MP3, AAC
- **Avoid**: Low-bitrate compressed formats

### 2. Processing Settings
- Start with default settings
- Gradually adjust based on audio content
- Use spectral gating for very noisy audio
- Apply compression for dynamic content

### 3. Batch Processing
```python
# Efficient batch processing
import multiprocessing

# Use parallel processing for large batches
batch_result = service.process_batch(
    audio_files,
    max_workers=multiprocessing.cpu_count()
)
```

## 🚨 Common Issues

### Issue: Import Errors
```bash
# Solution: Check Python path
export PYTHONPATH="${PYTHONPATH}:/path/to/MusicAITools"
```

### Issue: Audio Loading Fails
```python
# Solution: Verify file format support
from modules.core.models import AudioFormat
print("Supported formats:", [fmt.value for fmt in AudioFormat])
```

### Issue: Poor Quality Results
```python
# Solution: Adjust settings for your content
settings = {
    "noise_reduction": 0.1,  # Lower for clean audio
    "eq_low": 1.0,           # Neutral for balanced content
    "enable_spectral_gating": False  # Disable for music
}
```

## 🎉 What's Next?

1. **Explore Advanced Features**: [Audio Processing Guide](./audio_processing.md)
2. **Understand Architecture**: [Architecture Overview](./architecture.md)
3. **Customize Configuration**: [Configuration Guide](./configuration.md)
4. **Build Extensions**: [Development Guide](./development.md)

## 💬 Need Help?

- Check the [FAQ](./faq.md)
- Review [Examples](./examples/)
- Read the [API Reference](./api_reference.md)

---

**Happy audio processing! 🎵**