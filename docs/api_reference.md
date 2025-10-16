# 📚 API Reference

Complete API documentation for MusicAITools framework.

## 🔧 Core Module

### Exceptions

#### `MusicAIToolsException`
Base exception class for all framework-related errors.

```python
class MusicAIToolsException(Exception):
    def __init__(self, message: str, details: dict = None):
        """
        Initialize exception with message and optional details.
        
        Args:
            message: Human-readable error description
            details: Additional error context as key-value pairs
        """
```

**Properties:**
- `message: str` - Error message
- `details: Dict[str, Any]` - Additional error context

**Subclasses:**
- `AudioProcessingError` - Audio operation failures
- `FileNotFoundError` - Missing file errors
- `InvalidFormatError` - Format/codec issues
- `ConfigurationError` - Config validation failures
- `ModelLoadError` - ML model loading issues
- `ValidationError` - Data validation failures

### Logging

#### `get_logger() -> logging.Logger`
Get the global logger instance.

```python
from modules.core import get_logger

logger = get_logger()
logger.info("Processing started")
logger.error("Operation failed")
```

#### `setup_logging(level: int, log_file: Optional[Path]) -> logging.Logger`
Setup global logging configuration.

```python
from modules.core import setup_logging
import logging

logger = setup_logging(level=logging.DEBUG, log_file=Path("app.log"))
```

#### `log_performance(operation: str, duration: float, details: Dict[str, Any])`
Log performance metrics for operations.

```python
from modules.core.logger import log_performance

log_performance("audio_loading", 1.234, {"file_size_mb": 50})
```

### Configuration

#### `get_config() -> MusicAIConfig`
Get the global configuration instance.

```python
from modules.core import get_config

config = get_config()
print(config.audio_restoration.noise_reduction)
```

#### `MusicAIConfig`
Master configuration container.

**Properties:**
- `audio_restoration: AudioRestorationConfig`
- `audio_separation: AudioSeparationConfig`
- `visualization: VisualizationConfig`
- `conversion: ConversionConfig`
- `system: SystemConfig`

**Methods:**
- `validate() -> None` - Validate all configuration sections

#### `AudioRestorationConfig`
Configuration for audio restoration operations.

```python
@dataclass
class AudioRestorationConfig:
    noise_reduction: float = 0.2                    # 0.0-1.0
    eq_low: float = 1.2                            # 0.0-3.0
    eq_mid: float = 1.0                            # 0.0-3.0
    eq_high: float = 1.1                           # 0.0-3.0
    enable_spectral_gating: bool = True
    enable_dynamic_range_compression: bool = False
    compression_ratio: float = 2.0                 # 1.0-10.0
```

### Data Models

#### `AudioFile`
Represents an audio file with metadata.

```python
@dataclass
class AudioFile:
    path: Path
    sample_rate: Optional[int] = None
    duration: Optional[float] = None
    channels: Optional[int] = None
    format: Optional[AudioFormat] = None
    file_size_bytes: Optional[int] = None
    bit_depth: Optional[int] = None
```

**Properties:**
- `exists: bool` - Check if file exists
- `size_mb: Optional[float]` - File size in megabytes

**Methods:**
- `validate() -> None` - Validate file properties

#### `ProcessingResult`
Base class for all processing operation results.

```python
@dataclass
class ProcessingResult:
    status: ProcessingStatus
    output_files: List[Path] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None
    processing_time: Optional[float] = None
    timestamp: float = field(default_factory=time.time)
```

**Properties:**
- `success: bool` - Check if processing was successful
- `failed: bool` - Check if processing failed

**Methods:**
- `add_output_file(file_path: Union[str, Path]) -> None`
- `add_metadata(key: str, value: Any) -> None`
- `get_metadata(key: str, default: Any = None) -> Any`

#### `RestorationResult`
Result of audio restoration operation.

```python
@dataclass
class RestorationResult(ProcessingResult):
    restored_file: Optional[Path] = None
    improvement_metrics: Dict[str, float] = field(default_factory=dict)
    restoration_settings: Dict[str, Any] = field(default_factory=dict)
```

**Methods:**
- `get_improvement(metric: str) -> Optional[float]`
- `add_improvement_metric(metric: str, value: float) -> None`
- `overall_improvement: Optional[float]` - Weighted average of improvements

#### `BatchProcessingResult`
Result of batch processing operations.

```python
@dataclass
class BatchProcessingResult:
    individual_results: List[ProcessingResult] = field(default_factory=list)
    total_files: int = 0
    successful_files: int = 0
    failed_files: int = 0
    total_processing_time: float = 0.0
```

**Properties:**
- `success_rate: float` - Success rate as percentage
- `average_processing_time: float` - Average time per file

**Methods:**
- `add_result(result: ProcessingResult) -> None`
- `get_failed_results() -> List[ProcessingResult]`
- `get_successful_results() -> List[ProcessingResult]`

## 🎵 Audio Services

### BaseService

#### `BaseService(service_name: str)`
Abstract base class for all processing services.

**Methods:**

##### `safe_process(input_data: Any, **kwargs) -> ProcessingResult`
Safe wrapper for processing with error handling and monitoring.

```python
result = service.safe_process("audio.wav", custom_settings={"noise_reduction": 0.3})
```

##### `process_batch(input_files: List[Union[str, Path]], **kwargs) -> BatchProcessingResult`
Process multiple files in batch with progress tracking.

```python
batch_result = service.process_batch(["file1.wav", "file2.wav"])
print(f"Success rate: {batch_result.success_rate:.1f}%")
```

##### `get_stats() -> Dict[str, Any]`
Get processing statistics for this service.

```python
stats = service.get_stats()
print(f"Total operations: {stats['total_operations']}")
print(f"Success rate: {stats['success_rate']:.1f}%")
```

##### `reset_stats() -> None`
Reset processing statistics.

### AudioRestorationService

#### `AudioRestorationService()`
Professional audio restoration service.

**Inheritance:** `BaseService`

**Methods:**

##### `process(input_file: str, output_file: Optional[str] = None, custom_settings: Optional[Dict[str, Any]] = None) -> RestorationResult`
Restore audio file with configurable enhancement algorithms.

```python
service = AudioRestorationService()

# Basic usage
result = service.process("input.wav")

# Custom output and settings
result = service.process(
    "input.wav",
    output_file="enhanced.wav",
    custom_settings={
        "noise_reduction": 0.4,
        "eq_low": 1.3,
        "enable_spectral_gating": True
    }
)
```

**Parameters:**
- `input_file: str` - Path to input audio file
- `output_file: Optional[str]` - Output path (auto-generated if None)
- `custom_settings: Optional[Dict[str, Any]]` - Override default settings

**Returns:**
- `RestorationResult` - Comprehensive restoration results with metrics

**Raises:**
- `AudioProcessingError` - If restoration process fails

**Available Settings:**
```python
settings = {
    "noise_reduction": 0.2,                    # 0.0-1.0, noise reduction strength
    "eq_low": 1.2,                            # 0.0-3.0, bass frequency gain
    "eq_mid": 1.0,                            # 0.0-3.0, mid frequency gain
    "eq_high": 1.1,                           # 0.0-3.0, treble frequency gain
    "enable_spectral_gating": True,           # Advanced noise suppression
    "enable_dynamic_range_compression": False, # Apply compression
    "compression_ratio": 2.0                  # 1.0-10.0, compression strength
}
```

## 🔍 Quality Metrics

### Improvement Metrics

The restoration service calculates various quality improvement metrics:

#### SNR Improvement (dB)
Signal-to-noise ratio enhancement.
- **Range**: -∞ to +∞ dB
- **Typical**: +2 to +8 dB improvement
- **Interpretation**: Higher values indicate better noise reduction

#### THD Improvement
Total harmonic distortion reduction.
- **Range**: -∞ to +∞
- **Typical**: 0.01 to 0.1 improvement
- **Interpretation**: Positive values indicate less distortion

#### Spectral Flatness Improvement
Measure of noise-like vs. tonal content improvement.
- **Range**: -1.0 to +1.0
- **Interpretation**: Positive values indicate more tonal content

#### Dynamic Range Improvement (dB)
Peak-to-RMS ratio enhancement.
- **Range**: -∞ to +∞ dB
- **Interpretation**: Positive values indicate better dynamic range

#### Overall Quality Score
Weighted combination of all metrics.
- **Range**: 0 to 100
- **Interpretation**: Higher scores indicate better overall improvement

### Accessing Metrics

```python
result = service.process("audio.wav")

if result.success:
    # Individual metrics
    snr_improvement = result.get_improvement("snr_improvement_db")
    thd_improvement = result.get_improvement("thd_improvement")
    
    # Overall score
    overall_score = result.overall_improvement
    
    # All metrics
    for metric, value in result.improvement_metrics.items():
        print(f"{metric}: {value:.3f}")
```

## 🚨 Error Handling

### Exception Hierarchy

All framework exceptions inherit from `MusicAIToolsException`:

```python
try:
    result = service.process("audio.wav")
except FileNotFoundError as e:
    print(f"File not found: {e.message}")
    print(f"Context: {e.details}")
except AudioProcessingError as e:
    print(f"Processing failed: {e.message}")
except MusicAIToolsException as e:
    print(f"Framework error: {e.message}")
```

### Error Context

Exceptions include structured context information:

```python
try:
    result = service.process("corrupted.wav")
except AudioProcessingError as e:
    print(f"Error: {e.message}")
    if e.details:
        print(f"File: {e.details.get('file_path')}")
        print(f"Operation: {e.details.get('operation')}")
        print(f"Stage: {e.details.get('processing_stage')}")
```

### Safe Processing

Use `safe_process()` for automatic error handling:

```python
# Automatic error handling - never raises exceptions
result = service.safe_process("any_file.wav")

if result.success:
    print("Processing completed successfully")
else:
    print(f"Processing failed: {result.error_message}")
```

## 🔧 Configuration Reference

### Configuration File Format

```yaml
# config.yaml
audio_restoration:
  noise_reduction: 0.2
  eq_low: 1.2
  eq_mid: 1.0
  eq_high: 1.1
  enable_spectral_gating: true
  enable_dynamic_range_compression: false
  compression_ratio: 2.0

system:
  output_dir: "output"
  temp_dir: "temp"
  cache_enabled: true
  max_cache_size_mb: 1000
  parallel_processing: true
  max_workers: 4
  log_level: "INFO"
```

### Environment Variables

Override any configuration value using environment variables:

```bash
# Format: MUSICAI_<SECTION>_<KEY>
export MUSICAI_AUDIO_RESTORATION_NOISE_REDUCTION=0.3
export MUSICAI_SYSTEM_OUTPUT_DIR="/custom/output"
export MUSICAI_SYSTEM_LOG_LEVEL="DEBUG"
```

### Runtime Configuration

```python
from modules.core import get_config

# Get current configuration
config = get_config()

# Modify at runtime
config.audio_restoration.noise_reduction = 0.4

# Validate changes
config.validate()
```

## 📝 Usage Examples

### Basic Audio Restoration

```python
from modules.audio.restoration_service import AudioRestorationService

service = AudioRestorationService()
result = service.safe_process("input.wav")

if result.success:
    print(f"✅ Restored: {result.restored_file}")
    print(f"SNR improved by {result.get_improvement('snr_improvement_db'):.2f}dB")
else:
    print(f"❌ Failed: {result.error_message}")
```

### Custom Settings

```python
custom_settings = {
    "noise_reduction": 0.4,
    "eq_low": 1.3,
    "enable_spectral_gating": True
}

result = service.safe_process(
    "noisy_audio.wav",
    custom_settings=custom_settings
)
```

### Batch Processing

```python
import glob

audio_files = glob.glob("*.wav")
batch_result = service.process_batch(audio_files)

print(f"Processed {batch_result.total_files} files")
print(f"Success rate: {batch_result.success_rate:.1f}%")

# Review failures
for result in batch_result.get_failed_results():
    print(f"Failed: {result.error_message}")
```

### Performance Monitoring

```python
result = service.safe_process("large_file.wav")

print(f"Processing time: {result.processing_time:.2f}s")

# Service statistics
stats = service.get_stats()
print(f"Average processing time: {stats['average_processing_time']:.2f}s")
print(f"Success rate: {stats['success_rate']:.1f}%")
```

---

**For more examples, see the [Examples](./examples/) directory.**