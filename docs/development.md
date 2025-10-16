# 🛠️ Development Guide

Guide for contributors and developers extending MusicAITools.

## 🎯 Development Setup

### Prerequisites

- Python 3.8+
- Conda environment: `myenv`
- Git (for version control)
- Code editor with Python support

### Environment Setup

```bash
# 1. Clone repository (if contributing)
git clone <repository-url>
cd MusicAITools

# 2. Activate conda environment
conda activate myenv

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install development dependencies
pip install pytest pytest-cov black isort mypy

# 5. Verify setup
python tests/test_core_architecture.py
```

## 📋 Development Standards

### Code Style

Follow the coding rules defined in `./aim/rules.md`:

1. **No Chinese characters** - All code and comments in English
2. **Comment ratio 3:7** - Maintain good documentation coverage
3. **Unified error handling** - Use framework exception hierarchy
4. **No print statements** - Use logger system only
5. **Code simplicity** - Avoid redundancy, prefer modularity
6. **Python standards** - Follow PEP8 and type hints
7. **No git commands** - Managed externally
8. **Test environment** - Use `conda activate myenv`

### Code Formatting

```bash
# Format code with black
black modules/ tests/

# Sort imports with isort
isort modules/ tests/

# Type checking with mypy
mypy modules/
```

### Type Hints

All code must include comprehensive type hints:

```python
from typing import Optional, Dict, Any, List
from pathlib import Path

def process_audio(
    input_file: str,
    output_file: Optional[str] = None,
    settings: Optional[Dict[str, Any]] = None
) -> ProcessingResult:
    """Process audio with type-safe parameters."""
    pass
```

## 🏗️ Architecture Guidelines

### Service Development

#### 1. Inherit from BaseService

```python
from modules.core.base_service import BaseService
from modules.core.models import ProcessingResult

class NewAudioService(BaseService):
    """New audio processing service."""
    
    def __init__(self):
        super().__init__("NewAudio")
        self.config = get_config().your_config_section
    
    def process(self, input_data: Any, **kwargs) -> ProcessingResult:
        """Implement core processing logic."""
        # Your algorithm here
        pass
```

#### 2. Follow Processing Pipeline

```python
def process(self, input_file: str, **kwargs) -> ProcessingResult:
    """Standard processing pipeline."""
    
    # 1. Input validation
    audio_file = self._validate_audio_file(input_file)
    
    # 2. Configuration handling
    settings = self._merge_settings(kwargs.get('custom_settings'))
    
    # 3. Processing with monitoring
    with self._performance_monitor("main_processing"):
        result_data = self._your_algorithm(audio_file, settings)
    
    # 4. Output generation
    output_path = self._generate_output_path(audio_file)
    self._save_results(result_data, output_path)
    
    # 5. Return structured result
    return YourCustomResult(
        status=ProcessingStatus.SUCCESS,
        output_files=[output_path],
        # ... additional fields
    )
```

### Data Model Development

#### 1. Create Structured Results

```python
from dataclasses import dataclass, field
from modules.core.models import ProcessingResult

@dataclass
class YourCustomResult(ProcessingResult):
    """Custom result for your service."""
    
    your_specific_output: Optional[Path] = None
    your_metrics: Dict[str, float] = field(default_factory=dict)
    algorithm_parameters: Dict[str, Any] = field(default_factory=dict)
    
    def get_your_metric(self, metric: str) -> Optional[float]:
        """Get specific metric value."""
        return self.your_metrics.get(metric)
```

#### 2. Configuration Extensions

```python
from dataclasses import dataclass
from modules.core.exceptions import ValidationError

@dataclass
class YourServiceConfig:
    """Configuration for your service."""
    
    parameter1: float = 1.0
    parameter2: str = "default"
    enable_feature: bool = True
    
    def validate(self) -> None:
        """Validate configuration parameters."""
        if not 0.0 <= self.parameter1 <= 2.0:
            raise ValidationError("parameter1 must be between 0.0 and 2.0")
        
        if self.parameter2 not in ["option1", "option2", "default"]:
            raise ValidationError("parameter2 must be valid option")
```

### Error Handling

#### 1. Use Framework Exceptions

```python
from modules.core.exceptions import AudioProcessingError, ValidationError

def your_processing_method(self, data):
    """Example with proper error handling."""
    try:
        # Your processing logic
        result = some_complex_operation(data)
        return result
        
    except SomeExternalError as e:
        # Wrap external exceptions
        raise AudioProcessingError(
            f"Processing failed in your_method: {e}",
            details={"operation": "your_method", "input_size": len(data)}
        )
```

#### 2. Validation Methods

```python
def _validate_your_input(self, input_data: Any) -> None:
    """Validate service-specific input."""
    if not isinstance(input_data, expected_type):
        raise ValidationError(f"Expected {expected_type}, got {type(input_data)}")
    
    if not self._check_input_constraints(input_data):
        raise ValidationError("Input does not meet constraints")
```

## 🧪 Testing Guidelines

### Test Structure

```python
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

from modules.your_module.your_service import YourService
from modules.core.models import ProcessingStatus

class TestYourService(unittest.TestCase):
    """Test cases for YourService."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.service = YourService()
    
    def test_service_initialization(self):
        """Test service initializes correctly."""
        self.assertEqual(self.service.service_name, "YourService")
        self.assertIsNotNone(self.service.config)
    
    def test_successful_processing(self):
        """Test successful processing flow."""
        # Create test data
        test_input = "test_data"
        
        # Mock external dependencies
        with patch.object(self.service, '_external_method') as mock_external:
            mock_external.return_value = "mocked_result"
            
            result = self.service.safe_process(test_input)
            
            self.assertTrue(result.success)
            self.assertEqual(result.status, ProcessingStatus.SUCCESS)
    
    def test_error_handling(self):
        """Test error handling."""
        result = self.service.safe_process("invalid_input")
        
        self.assertTrue(result.failed)
        self.assertIsNotNone(result.error_message)
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python tests/test_core_architecture.py

# Run with coverage
python -m pytest tests/ --cov=modules --cov-report=html
```

### Test Categories

1. **Unit Tests** - Individual methods and functions
2. **Integration Tests** - Service interactions
3. **Performance Tests** - Speed and resource usage
4. **Error Handling Tests** - Exception scenarios

## 📚 Documentation Standards

### Code Documentation

#### 1. Module Docstrings

```python
"""
Your module description.

This module provides functionality for [specific purpose].
Key features include:
- Feature 1 description
- Feature 2 description
- Integration with other components
"""
```

#### 2. Class Docstrings

```python
class YourService(BaseService):
    """
    Brief description of the service.
    
    Detailed description of what this service does,
    its main algorithms, and use cases.
    
    Examples:
        Basic usage:
        >>> service = YourService()
        >>> result = service.process("input.wav")
        
        Advanced usage:
        >>> result = service.process("input.wav", custom_settings={"param": 1.5})
    """
```

#### 3. Method Docstrings

```python
def process(self, 
           input_data: str,
           output_file: Optional[str] = None,
           settings: Optional[Dict[str, Any]] = None) -> YourResult:
    """
    Process input data with your algorithm.
    
    Args:
        input_data: Path to input file or data identifier
        output_file: Optional output file path (auto-generated if None)
        settings: Optional dictionary of algorithm parameters
        
    Returns:
        YourResult: Processing result with metrics and outputs
        
    Raises:
        AudioProcessingError: If processing fails
        ValidationError: If input validation fails
        
    Examples:
        >>> service = YourService()
        >>> result = service.process("audio.wav")
        >>> print(f"Success: {result.success}")
    """
```

### Documentation Files

When adding new features, update:

1. **API Reference** - Add to `docs/api_reference.md`
2. **Examples** - Create example in `docs/examples/`
3. **Configuration** - Document new config options
4. **FAQ** - Add common questions

## 🚀 Contribution Workflow

### 1. Development Process

```bash
# 1. Create feature branch
git checkout -b feature/your-feature-name

# 2. Implement changes following standards
# - Add comprehensive tests
# - Include type hints
# - Document new functionality

# 3. Test your changes
python tests/test_core_architecture.py
python -m pytest tests/

# 4. Format code
black modules/ tests/
isort modules/ tests/

# 5. Update documentation
# Add to relevant docs/ files
```

### 2. Code Review Checklist

Before submitting:

- [ ] All tests pass
- [ ] Code follows style guidelines
- [ ] Type hints are comprehensive
- [ ] Documentation is updated
- [ ] Error handling is implemented
- [ ] Performance impact is considered
- [ ] Backwards compatibility is maintained

### 3. Performance Considerations

#### Memory Usage

```python
# Good: Process data in chunks
def process_large_file(self, file_path: Path) -> ProcessingResult:
    """Process large files efficiently."""
    chunk_size = 1024 * 1024  # 1MB chunks
    
    with open(file_path, 'rb') as f:
        while chunk := f.read(chunk_size):
            self._process_chunk(chunk)
```

#### CPU Usage

```python
# Good: Use performance monitoring
def cpu_intensive_operation(self, data):
    """CPU-intensive operation with monitoring."""
    with self._performance_monitor("intensive_operation"):
        result = self._complex_algorithm(data)
    return result
```

## 🔧 Advanced Development

### Custom Configuration Integration

```python
# 1. Add to config.py
@dataclass
class YourServiceConfig:
    your_parameter: float = 1.0
    
    def validate(self) -> None:
        if not 0.0 <= self.your_parameter <= 2.0:
            raise ValidationError("Parameter out of range")

# 2. Add to MusicAIConfig
@dataclass
class MusicAIConfig:
    # ... existing configs
    your_service: YourServiceConfig = field(default_factory=YourServiceConfig)

# 3. Use in your service
class YourService(BaseService):
    def __init__(self):
        super().__init__("YourService")
        self.config = get_config().your_service
```

### Plugin Architecture

```python
# For future plugin support
class PluginManager:
    """Manage dynamic service loading."""
    
    def register_service(self, service_class: type) -> None:
        """Register new service type."""
        pass
    
    def create_service(self, service_name: str) -> BaseService:
        """Create service instance by name."""
        pass
```

### Async Support

```python
# For future async processing
import asyncio
from typing import AsyncIterator

class AsyncAudioService(BaseService):
    """Async audio processing service."""
    
    async def process_async(self, input_data: Any) -> ProcessingResult:
        """Async processing method."""
        # Async implementation
        pass
    
    async def process_stream(self, data_stream: AsyncIterator) -> AsyncIterator[ProcessingResult]:
        """Stream processing support."""
        async for chunk in data_stream:
            yield await self.process_async(chunk)
```

## 📊 Quality Assurance

### Code Quality Metrics

- **Test Coverage**: Aim for >80%
- **Type Coverage**: 100% for public APIs
- **Documentation**: All public methods documented
- **Performance**: No regression in benchmarks

### Continuous Integration

```bash
# CI pipeline commands
pytest tests/ --cov=modules --cov-report=xml
black --check modules/ tests/
isort --check-only modules/ tests/
mypy modules/
```

---

## 🤝 Getting Help

### Resources

- **Architecture Overview**: `docs/architecture.md`
- **API Reference**: `docs/api_reference.md`
- **Examples**: `docs/examples/`
- **Configuration**: `docs/configuration.md`

### Contact

- Create issues for bugs and feature requests
- Start discussions for design questions
- Review existing code for patterns and examples

---

**Thank you for contributing to MusicAITools! 🎵**