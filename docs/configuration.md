# ⚙️ Configuration Guide

MusicAITools provides a flexible, hierarchical configuration system that supports file-based configuration, environment variables, and runtime overrides.

## 🔧 Configuration Structure

### Configuration Hierarchy

```yaml
# Complete configuration structure
audio_restoration:          # Audio restoration settings
  noise_reduction: 0.2
  eq_low: 1.2
  eq_mid: 1.0
  eq_high: 1.1
  enable_spectral_gating: true
  enable_dynamic_range_compression: false
  compression_ratio: 2.0

audio_separation:           # Audio source separation
  model_name: "htdemucs"
  device: "auto"
  split_tracks: true
  overlap: 0.25
  shifts: 1
  segment_length: null

visualization:              # Visualization settings
  dpi: 300
  figure_size: [15, 10]
  color_scheme: "viridis"
  save_format: "png"
  show_plots: false
  n_fft: 2048
  hop_length: 512
  n_mels: 128

conversion:                 # Format conversion
  default_sample_rate: 22050
  default_bit_depth: 16
  enable_resampling: true
  conversion_quality: "high"
  preserve_metadata: true
  normalize_audio: false

system:                     # System-wide settings
  output_dir: "output"
  temp_dir: "temp"
  cache_enabled: true
  max_cache_size_mb: 1000
  parallel_processing: true
  max_workers: 4
  memory_limit_mb: null
  log_level: "INFO"
```

## 📁 Configuration Files

### Default Configuration

The framework includes a default `config.yaml` file:

```yaml
# MusicAITools/config.yaml
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

### Custom Configuration Files

#### YAML Format

```yaml
# my_config.yaml
audio_restoration:
  noise_reduction: 0.3      # Stronger noise reduction
  eq_low: 1.5              # More bass boost
  enable_spectral_gating: true

system:
  output_dir: "/custom/output"
  log_level: "DEBUG"
```

#### JSON Format

```json
{
  "audio_restoration": {
    "noise_reduction": 0.3,
    "eq_low": 1.5,
    "enable_spectral_gating": true
  },
  "system": {
    "output_dir": "/custom/output",
    "log_level": "DEBUG"
  }
}
```

### Loading Configuration Files

```python
from modules.core.config import ConfigManager

# Load from specific file
config_manager = ConfigManager("my_config.yaml")
config = config_manager.load_config()

# Or use global configuration
from modules.core import get_config
config = get_config()
```

## 🌍 Environment Variables

Override any configuration value using environment variables with the pattern:
`MUSICAI_<SECTION>_<KEY>`

### Examples

```bash
# Audio restoration settings
export MUSICAI_AUDIO_RESTORATION_NOISE_REDUCTION=0.4
export MUSICAI_AUDIO_RESTORATION_EQ_LOW=1.3
export MUSICAI_AUDIO_RESTORATION_ENABLE_SPECTRAL_GATING=true

# System settings
export MUSICAI_SYSTEM_OUTPUT_DIR="/data/output"
export MUSICAI_SYSTEM_LOG_LEVEL="DEBUG"
export MUSICAI_SYSTEM_MAX_WORKERS=8

# Visualization settings
export MUSICAI_VISUALIZATION_DPI=600
export MUSICAI_VISUALIZATION_COLOR_SCHEME="plasma"
```

### Type Conversion

Environment variables are automatically converted to the correct type:

```bash
export MUSICAI_AUDIO_RESTORATION_NOISE_REDUCTION=0.3     # → float
export MUSICAI_SYSTEM_MAX_WORKERS=8                      # → int
export MUSICAI_AUDIO_RESTORATION_ENABLE_SPECTRAL_GATING=true  # → bool
export MUSICAI_VISUALIZATION_FIGURE_SIZE="12,8"          # → tuple
```

## ⚡ Runtime Configuration

### Accessing Configuration

```python
from modules.core import get_config

config = get_config()

# Access nested settings
noise_reduction = config.audio_restoration.noise_reduction
output_dir = config.system.output_dir
dpi = config.visualization.dpi

print(f"Noise reduction: {noise_reduction}")
print(f"Output directory: {output_dir}")
```

### Runtime Modifications

```python
# Modify configuration at runtime
config.audio_restoration.noise_reduction = 0.5
config.system.output_dir = "/tmp/output"

# Validate changes
try:
    config.validate()
    print("✅ Configuration is valid")
except ValidationError as e:
    print(f"❌ Configuration error: {e}")
```

### Per-Operation Overrides

```python
from modules.audio.restoration_service import AudioRestorationService

service = AudioRestorationService()

# Override settings for specific operation
custom_settings = {
    "noise_reduction": 0.4,
    "eq_low": 1.3,
    "enable_spectral_gating": True
}

result = service.safe_process(
    "audio.wav",
    custom_settings=custom_settings
)
```

## 📊 Configuration Sections

### Audio Restoration

Controls audio enhancement and restoration algorithms.

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

**Parameters:**
- `noise_reduction` - Noise reduction strength (0=none, 1=maximum)
- `eq_low` - Bass frequency gain multiplier
- `eq_mid` - Mid frequency gain multiplier  
- `eq_high` - Treble frequency gain multiplier
- `enable_spectral_gating` - Advanced noise suppression
- `enable_dynamic_range_compression` - Apply dynamic compression
- `compression_ratio` - Compression strength (1=none, 10=maximum)

### Audio Separation

Settings for audio source separation.

```python
@dataclass
class AudioSeparationConfig:
    model_name: str = "htdemucs"      # Model to use
    device: str = "auto"              # auto, cpu, cuda, mps
    split_tracks: bool = True
    overlap: float = 0.25             # 0.0-1.0
    shifts: int = 1                   # Number of shifts
    segment_length: Optional[int] = None
```

### Visualization

Controls plot generation and visualization output.

```python
@dataclass
class VisualizationConfig:
    dpi: int = 300                    # 50-600
    figure_size: tuple = (15, 10)     # (width, height)
    color_scheme: str = "viridis"     # matplotlib colormap
    save_format: str = "png"          # png, jpg, pdf, svg
    show_plots: bool = False
    n_fft: int = 2048                # 256-8192
    hop_length: int = 512             # 64-n_fft/2
    n_mels: int = 128                 # 13-256
```

### Conversion

Format conversion and audio processing settings.

```python
@dataclass
class ConversionConfig:
    default_sample_rate: int = 22050   # 8000, 16000, 22050, 44100, 48000, 96000
    default_bit_depth: int = 16        # 8, 16, 24, 32
    enable_resampling: bool = True
    conversion_quality: str = "high"   # low, medium, high, lossless
    preserve_metadata: bool = True
    normalize_audio: bool = False
```

### System

System-wide settings and resource management.

```python
@dataclass
class SystemConfig:
    output_dir: str = "output"
    temp_dir: str = "temp"
    cache_enabled: bool = True
    max_cache_size_mb: int = 1000      # 10+
    parallel_processing: bool = True
    max_workers: int = 4               # 1-32
    memory_limit_mb: Optional[int] = None  # 100+ or None
    log_level: str = "INFO"            # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

## ✅ Configuration Validation

### Automatic Validation

All configuration parameters are automatically validated:

```python
config = get_config()

try:
    config.validate()
    print("✅ Configuration is valid")
except ValidationError as e:
    print(f"❌ Validation failed: {e}")
```

### Validation Rules

#### Audio Restoration
- `noise_reduction`: 0.0 ≤ value ≤ 1.0
- `eq_low`, `eq_mid`, `eq_high`: 0.0 ≤ value ≤ 3.0
- `compression_ratio`: 1.0 ≤ value ≤ 10.0

#### Audio Separation
- `model_name`: Must be supported model
- `overlap`: 0.0 ≤ value ≤ 1.0
- `shifts`: value ≥ 1

#### Visualization
- `dpi`: 50 ≤ value ≤ 600
- `figure_size`: Two positive numbers
- `save_format`: Must be supported format
- `n_fft`: 256 ≤ value ≤ 8192
- `hop_length`: 64 ≤ value ≤ n_fft/2
- `n_mels`: 13 ≤ value ≤ 256

#### System
- `max_cache_size_mb`: value ≥ 10
- `max_workers`: 1 ≤ value ≤ 32
- `memory_limit_mb`: value ≥ 100 or None
- `log_level`: Must be valid log level

## 🎛️ Configuration Profiles

### Creating Profiles

```yaml
# profiles/high_quality.yaml
audio_restoration:
  noise_reduction: 0.1
  enable_spectral_gating: true
  enable_dynamic_range_compression: true

visualization:
  dpi: 600
  save_format: "png"

system:
  max_workers: 8
```

```yaml
# profiles/fast_processing.yaml
audio_restoration:
  noise_reduction: 0.2
  enable_spectral_gating: false

system:
  parallel_processing: true
  max_workers: 16
  cache_enabled: true
```

### Loading Profiles

```python
from modules.core.config import ConfigManager

# Load high quality profile
config_manager = ConfigManager("profiles/high_quality.yaml")
config = config_manager.load_config()

# Or programmatically
def load_profile(profile_name: str):
    config_file = f"profiles/{profile_name}.yaml"
    manager = ConfigManager(config_file)
    return manager.load_config()

high_quality_config = load_profile("high_quality")
fast_config = load_profile("fast_processing")
```

## 🔍 Configuration Best Practices

### 1. Environment-Specific Configuration

```bash
# Development
export MUSICAI_SYSTEM_LOG_LEVEL="DEBUG"
export MUSICAI_SYSTEM_OUTPUT_DIR="./dev_output"

# Production
export MUSICAI_SYSTEM_LOG_LEVEL="INFO"
export MUSICAI_SYSTEM_OUTPUT_DIR="/data/production_output"
export MUSICAI_SYSTEM_MAX_WORKERS=16
```

### 2. Application-Specific Settings

```python
# For broadcast audio processing
broadcast_settings = {
    "noise_reduction": 0.1,
    "enable_spectral_gating": False,
    "enable_dynamic_range_compression": True,
    "compression_ratio": 3.0
}

# For podcast enhancement
podcast_settings = {
    "noise_reduction": 0.4,
    "enable_spectral_gating": True,
    "eq_mid": 1.2,  # Enhance speech frequencies
    "enable_dynamic_range_compression": True
}

# For music restoration
music_settings = {
    "noise_reduction": 0.2,
    "enable_spectral_gating": True,
    "enable_dynamic_range_compression": False
}
```

### 3. Resource Management

```python
# High-memory system
high_memory_config = {
    "max_cache_size_mb": 4000,
    "max_workers": 12,
    "memory_limit_mb": None
}

# Limited resources
limited_config = {
    "max_cache_size_mb": 500,
    "max_workers": 2,
    "memory_limit_mb": 2000,
    "cache_enabled": False
}
```

## 💾 Saving Configuration

### Save Current Configuration

```python
from modules.core.config import ConfigManager

# Get current configuration
config = get_config()

# Modify settings
config.audio_restoration.noise_reduction = 0.3
config.system.output_dir = "/custom/output"

# Save to file
config_manager = ConfigManager("my_settings.yaml")
config_manager.save_config(config)
```

### Export Configuration

```python
from modules.core.config import save_config_to_file

# Save current config to specific file
config = get_config()
save_config_to_file(config, "exported_config.yaml")
```

## 🚀 Advanced Configuration

### Dynamic Configuration Loading

```python
import os
from modules.core.config import ConfigManager

def load_environment_config():
    """Load configuration based on environment"""
    env = os.getenv("ENVIRONMENT", "development")
    
    config_files = {
        "development": "config/dev.yaml",
        "staging": "config/staging.yaml", 
        "production": "config/prod.yaml"
    }
    
    config_file = config_files.get(env, "config.yaml")
    manager = ConfigManager(config_file)
    return manager.load_config()

config = load_environment_config()
```

### Configuration Monitoring

```python
import time
from pathlib import Path

class ConfigurationWatcher:
    """Watch configuration file for changes"""
    
    def __init__(self, config_file: Path):
        self.config_file = config_file
        self.last_modified = config_file.stat().st_mtime
        
    def check_for_updates(self):
        """Check if configuration file has been modified"""
        current_modified = self.config_file.stat().st_mtime
        
        if current_modified > self.last_modified:
            self.last_modified = current_modified
            return True
        return False
    
    def reload_if_changed(self):
        """Reload configuration if file has changed"""
        if self.check_for_updates():
            manager = ConfigManager(self.config_file)
            new_config = manager.load_config()
            print("Configuration reloaded")
            return new_config
        return None
```

---

For more configuration examples, see the [Examples](./examples/) directory.