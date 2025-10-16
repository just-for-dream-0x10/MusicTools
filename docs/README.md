# 🎵 MusicAITools Documentation

Welcome to the MusicAITools documentation! This guide will help you understand and use the powerful music AI processing framework.

## 📚 Table of Contents

- [Quick Start Guide](./quick_start.md) - Get up and running in 5 minutes
- [Architecture Overview](./architecture.md) - Understanding the framework design
- [Core Components](./core_components.md) - Detailed core functionality reference
- [Audio Processing](./audio_processing.md) - Audio restoration and enhancement
- [Configuration Guide](./configuration.md) - Customizing framework behavior
- [API Reference](./api_reference.md) - Complete API documentation
- [Development Guide](./development.md) - Contributing and extending the framework
- [Examples](./examples/) - Practical usage examples
- [FAQ](./faq.md) - Frequently asked questions

## 🚀 What is MusicAITools?

MusicAITools is a professional-grade music AI processing framework that provides:

- **Advanced Audio Restoration** - Noise reduction, frequency correction, dynamic range optimization
- **Intelligent Audio Analysis** - Quality metrics, spectral analysis, harmonic detection
- **Unified Processing Pipeline** - Type-safe, error-handled, performance-monitored operations
- **Extensible Architecture** - Easy to extend with new algorithms and services
- **Professional Quality** - Enterprise-grade error handling, logging, and configuration

## 🛠️ Core Features

### Audio Restoration
- Advanced spectral subtraction for noise reduction
- Multi-band equalization with precise frequency control
- Dynamic range compression with adaptive algorithms
- Quality assessment with SNR, THD, and spectral metrics

### Framework Architecture
- **Type-safe data models** - Structured representation of audio files and results
- **Unified error handling** - Comprehensive exception hierarchy with context
- **Centralized logging** - Professional logging with performance monitoring
- **Configuration management** - YAML/JSON config with environment overrides
- **Service-oriented design** - Modular, testable, and maintainable architecture

### Processing Pipeline
```python
from modules.core import get_config
from modules.audio.restoration_service import AudioRestorationService

# Initialize service
service = AudioRestorationService()

# Process audio with custom settings
result = service.safe_process(
    "input.wav",
    custom_settings={"noise_reduction": 0.3}
)

if result.success:
    print(f"Restored: {result.restored_file}")
    print(f"SNR improvement: {result.get_improvement('snr_improvement_db'):.2f}dB")
```

## 📦 Installation

```bash
# Clone the repository
git clone <repository-url>
cd MusicAITools

# Install dependencies
conda activate myenv
pip install -r requirements.txt

# Verify installation
python test_new_architecture.py
```

## 🧪 Quick Test

```bash
# Run comprehensive tests
python tests/test_core_architecture.py

# Run demonstrations
python test_new_architecture.py
```

## 📖 Learning Path

1. **Start Here**: [Quick Start Guide](./quick_start.md)
2. **Understand**: [Architecture Overview](./architecture.md)
3. **Configure**: [Configuration Guide](./configuration.md)
4. **Process Audio**: [Audio Processing Guide](./audio_processing.md)
5. **Extend**: [Development Guide](./development.md)

## 🤝 Community

- **Issues**: Report bugs and request features
- **Discussions**: Ask questions and share ideas
- **Contributing**: See [Development Guide](./development.md)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ for the music AI community**