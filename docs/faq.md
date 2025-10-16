# ❓ Frequently Asked Questions

Common questions and answers about MusicAITools.

## 🚀 Getting Started

### Q: How do I install MusicAITools?

**A:** Follow these steps:

```bash
# 1. Activate conda environment
conda activate myenv

# 2. Install dependencies
pip install -r requirements.txt

# 3. Verify installation
python test_new_architecture.py
```

### Q: What audio formats are supported?

**A:** MusicAITools supports:
- **Recommended**: WAV, FLAC (lossless formats)
- **Supported**: MP3, AAC, M4A, OGG
- **Best Results**: 16-bit or 24-bit, 44.1kHz or higher

### Q: Can I process stereo audio files?

**A:** Yes! The framework automatically handles:
- Mono and stereo files
- Automatic mono conversion for processing
- Stereo preservation where appropriate

## 🎵 Audio Processing

### Q: What's the difference between noise reduction settings?

**A:** Noise reduction strength (0.0-1.0):
- **0.1-0.2**: Light cleaning for high-quality audio
- **0.3-0.4**: Moderate cleaning for typical recordings
- **0.5-0.7**: Aggressive cleaning for very noisy audio
- **0.8-1.0**: Maximum cleaning (may affect audio quality)

### Q: When should I enable spectral gating?

**A:** Enable spectral gating when:
- ✅ Audio has constant background noise
- ✅ Recording has hiss or hum
- ✅ You need aggressive noise suppression
- ❌ Avoid for clean music (may affect dynamics)

### Q: How do EQ settings work?

**A:** EQ multipliers (0.0-3.0):
- **eq_low**: Bass frequencies (20-300 Hz)
- **eq_mid**: Mid frequencies (300-3000 Hz)  
- **eq_high**: Treble frequencies (3000+ Hz)
- **1.0**: No change
- **>1.0**: Boost frequencies
- **<1.0**: Reduce frequencies

### Q: What quality improvements can I expect?

**A:** Typical improvements:
- **SNR**: +3 to +8 dB improvement
- **Noise**: 50-80% reduction
- **Clarity**: Noticeable enhancement
- **Dynamics**: Preserved or improved

## ⚙️ Configuration

### Q: How do I customize default settings?

**A:** Three methods:

1. **Configuration file** (recommended):
```yaml
# config.yaml
audio_restoration:
  noise_reduction: 0.3
  eq_low: 1.2
```

2. **Environment variables**:
```bash
export MUSICAI_AUDIO_RESTORATION_NOISE_REDUCTION=0.3
```

3. **Runtime settings**:
```python
custom_settings = {"noise_reduction": 0.3}
result = service.safe_process("audio.wav", custom_settings=custom_settings)
```

### Q: Where are output files saved?

**A:** By default:
- **Location**: `./output/` directory
- **Naming**: `original_name_restored.wav`
- **Customizable**: Set `output_dir` in config or specify `output_file`

## 🔧 Troubleshooting

### Q: Import errors when running code

**A:** Check your Python path:
```bash
# Add MusicAITools to Python path
export PYTHONPATH="${PYTHONPATH}:/path/to/MusicAITools"

# Or run from MusicAITools directory
cd MusicAITools
python your_script.py
```

### Q: "Module not found" errors

**A:** Ensure conda environment is activated:
```bash
conda activate myenv
python -c "import librosa; print('✅ Dependencies OK')"
```

### Q: Poor restoration results

**A:** Try these adjustments:

**For very noisy audio:**
```python
settings = {
    "noise_reduction": 0.5,
    "enable_spectral_gating": True
}
```

**For clean audio:**
```python
settings = {
    "noise_reduction": 0.1,
    "enable_spectral_gating": False
}
```

**For speech:**
```python
settings = {
    "noise_reduction": 0.3,
    "eq_mid": 1.2,  # Boost speech frequencies
    "enable_dynamic_range_compression": True
}
```

### Q: Processing is very slow

**A:** Optimize performance:

1. **Enable parallel processing**:
```python
config.system.parallel_processing = True
config.system.max_workers = 8
```

2. **Use appropriate file sizes**:
- Files > 100MB may be slow
- Consider splitting large files

3. **Disable unnecessary features**:
```python
settings = {
    "enable_spectral_gating": False,  # Faster processing
    "enable_dynamic_range_compression": False
}
```

### Q: Memory errors with large files

**A:** Reduce memory usage:

```python
# Set memory limit
config.system.memory_limit_mb = 2000

# Reduce cache size
config.system.max_cache_size_mb = 500

# Disable caching
config.system.cache_enabled = False
```

## 📊 Results and Metrics

### Q: How do I interpret improvement metrics?

**A:** Metric explanations:

- **SNR Improvement**: Higher = better noise reduction
- **THD Improvement**: Positive = less distortion
- **Spectral Flatness**: Positive = more musical content
- **Overall Quality**: 0-100 scale, higher = better

### Q: Why do some metrics show negative values?

**A:** Negative values can indicate:
- Over-processing (reduce settings)
- Different audio characteristics
- Processing trade-offs (less noise but more artifacts)

### Q: Can I batch process multiple files?

**A:** Yes! Use batch processing:

```python
import glob

# Get all audio files
audio_files = glob.glob("*.wav")

# Process all files
batch_result = service.process_batch(audio_files)

print(f"Success rate: {batch_result.success_rate:.1f}%")
```

## 🛠️ Advanced Usage

### Q: How do I add custom processing algorithms?

**A:** Extend the BaseService class:

```python
from modules.core.base_service import BaseService
from modules.core.models import ProcessingResult

class CustomAudioService(BaseService):
    def __init__(self):
        super().__init__("CustomAudio")
    
    def process(self, input_data, **kwargs):
        # Your custom processing logic
        # Automatic error handling, monitoring, etc.
        pass
```

### Q: Can I integrate with other audio libraries?

**A:** Yes! The framework is designed for integration:

```python
# Example: Integrate with custom library
import my_audio_library

class CustomService(BaseService):
    def process(self, input_file, **kwargs):
        # Load with framework
        audio_file = self._validate_audio_file(input_file)
        
        # Process with custom library
        result = my_audio_library.process(audio_file.path)
        
        # Return standardized result
        return self._create_success_result([result.output_path])
```

### Q: How do I monitor processing progress?

**A:** Use the built-in monitoring:

```python
# Service-level statistics
stats = service.get_stats()
print(f"Average processing time: {stats['average_processing_time']:.2f}s")

# Individual operation timing
result = service.safe_process("audio.wav")
print(f"Processing took: {result.processing_time:.2f}s")

# Batch processing progress
batch_result = service.process_batch(files)
for i, result in enumerate(batch_result.individual_results):
    print(f"File {i+1}: {'✅' if result.success else '❌'}")
```

## 🚨 Error Messages

### Q: "Audio file does not exist"

**A:** Check:
- File path is correct
- File actually exists
- You have read permissions

### Q: "Configuration validation failed"

**A:** Check parameter ranges:
```python
# Valid ranges
noise_reduction: 0.0-1.0
eq_low/mid/high: 0.0-3.0
compression_ratio: 1.0-10.0
```

### Q: "Audio restoration failed: module 'numpy' has no attribute 'float'"

**A:** NumPy version compatibility issue:
```bash
# Update NumPy
pip install numpy>=1.20.0

# Or use the testing environment
conda activate myenv
```

## 📈 Performance

### Q: How can I speed up processing?

**A:** Performance optimization tips:

1. **Use appropriate workers**:
```python
config.system.max_workers = min(8, cpu_count())
```

2. **Enable caching**:
```python
config.system.cache_enabled = True
config.system.max_cache_size_mb = 2000
```

3. **Optimize settings**:
```python
# Faster settings
settings = {
    "noise_reduction": 0.2,  # Lower values are faster
    "enable_spectral_gating": False  # Disable if not needed
}
```

### Q: What are the system requirements?

**A:** Minimum requirements:
- **CPU**: Multi-core recommended
- **RAM**: 4GB minimum, 8GB+ recommended
- **Storage**: 1GB free space
- **Python**: 3.8+
- **OS**: Windows, macOS, Linux

**For large files:**
- **RAM**: 16GB+
- **CPU**: 8+ cores
- **Storage**: SSD recommended

## 🤝 Community

### Q: How do I report bugs?

**A:** 
1. Check existing issues
2. Provide minimal reproduction example
3. Include system information
4. Attach relevant log files

### Q: How can I contribute?

**A:** See the [Development Guide](./development.md) for:
- Code contribution guidelines
- Testing requirements
- Documentation standards

### Q: Where can I get help?

**A:**
- 📖 Check this documentation
- 🔍 Search existing issues
- 💬 Start a discussion
- 📧 Contact maintainers

---

**Still have questions? Feel free to ask in our community discussions!**