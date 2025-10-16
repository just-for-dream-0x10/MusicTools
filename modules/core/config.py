"""
Configuration management system for MusicAITools.

This module provides centralized configuration handling with support for:
- Default configurations
- File-based configuration loading
- Environment variable overrides
- Configuration validation
"""

import json
import yaml
import os
from pathlib import Path
from dataclasses import dataclass, asdict, field
from typing import Dict, Any, Optional, Union, List
from enum import Enum

from .logger import get_logger
from .exceptions import ConfigurationError, ValidationError


class DeviceType(Enum):
    """Supported computation device types."""
    AUTO = "auto"
    CPU = "cpu"
    CUDA = "cuda"
    MPS = "mps"


@dataclass
class AudioRestorationConfig:
    """
    Configuration for audio restoration operations.
    
    Controls noise reduction, equalization, and audio enhancement parameters.
    """
    noise_reduction: float = 0.2
    eq_low: float = 1.2
    eq_mid: float = 1.0
    eq_high: float = 1.1
    enable_spectral_gating: bool = True
    enable_dynamic_range_compression: bool = False
    compression_ratio: float = 2.0
    
    def validate(self) -> None:
        """
        Validate configuration parameters.
        
        Raises:
            ValidationError: If parameters are outside valid ranges
        """
        if not 0.0 <= self.noise_reduction <= 1.0:
            raise ValidationError("noise_reduction must be between 0.0 and 1.0")
        
        if not 0.0 <= self.eq_low <= 3.0:
            raise ValidationError("eq_low must be between 0.0 and 3.0")
            
        if not 0.0 <= self.eq_mid <= 3.0:
            raise ValidationError("eq_mid must be between 0.0 and 3.0")
            
        if not 0.0 <= self.eq_high <= 3.0:
            raise ValidationError("eq_high must be between 0.0 and 3.0")
            
        if not 1.0 <= self.compression_ratio <= 10.0:
            raise ValidationError("compression_ratio must be between 1.0 and 10.0")


@dataclass
class AudioSeparationConfig:
    """
    Configuration for audio source separation.
    
    Controls model selection, device usage, and separation parameters.
    """
    model_name: str = "htdemucs"
    device: DeviceType = DeviceType.AUTO
    split_tracks: bool = True
    overlap: float = 0.25
    shifts: int = 1
    segment_length: Optional[int] = None
    
    def validate(self) -> None:
        """
        Validate separation configuration.
        
        Raises:
            ValidationError: If parameters are invalid
        """
        valid_models = ["htdemucs", "hdemucs_mmi", "mdx", "mdx_extra"]
        if self.model_name not in valid_models:
            raise ValidationError(f"model_name must be one of: {valid_models}")
            
        if not 0.0 <= self.overlap <= 1.0:
            raise ValidationError("overlap must be between 0.0 and 1.0")
            
        if self.shifts < 1:
            raise ValidationError("shifts must be at least 1")
            
        if self.segment_length is not None and self.segment_length < 1:
            raise ValidationError("segment_length must be positive or None")


@dataclass
class VisualizationConfig:
    """
    Configuration for audio visualization and plotting.
    
    Controls output quality, styling, and visualization parameters.
    """
    dpi: int = 300
    figure_size: tuple = (15, 10)
    color_scheme: str = "viridis"
    save_format: str = "png"
    show_plots: bool = False
    n_fft: int = 2048
    hop_length: int = 512
    n_mels: int = 128
    
    def validate(self) -> None:
        """
        Validate visualization configuration.
        
        Raises:
            ValidationError: If parameters are invalid
        """
        if self.dpi < 50 or self.dpi > 600:
            raise ValidationError("dpi must be between 50 and 600")
            
        if len(self.figure_size) != 2 or any(x <= 0 for x in self.figure_size):
            raise ValidationError("figure_size must be a tuple of two positive numbers")
            
        valid_formats = ["png", "jpg", "pdf", "svg"]
        if self.save_format not in valid_formats:
            raise ValidationError(f"save_format must be one of: {valid_formats}")
            
        if self.n_fft < 256 or self.n_fft > 8192:
            raise ValidationError("n_fft must be between 256 and 8192")
            
        if self.hop_length < 64 or self.hop_length > self.n_fft // 2:
            raise ValidationError("hop_length must be between 64 and n_fft/2")
            
        if self.n_mels < 13 or self.n_mels > 256:
            raise ValidationError("n_mels must be between 13 and 256")


@dataclass
class ConversionConfig:
    """
    Configuration for audio and format conversion operations.
    
    Controls quality settings, codec parameters, and conversion options.
    """
    default_sample_rate: int = 22050
    default_bit_depth: int = 16
    enable_resampling: bool = True
    conversion_quality: str = "high"
    preserve_metadata: bool = True
    normalize_audio: bool = False
    
    def validate(self) -> None:
        """
        Validate conversion configuration.
        
        Raises:
            ValidationError: If parameters are invalid
        """
        valid_sample_rates = [8000, 16000, 22050, 44100, 48000, 96000]
        if self.default_sample_rate not in valid_sample_rates:
            raise ValidationError(f"default_sample_rate must be one of: {valid_sample_rates}")
            
        valid_bit_depths = [8, 16, 24, 32]
        if self.default_bit_depth not in valid_bit_depths:
            raise ValidationError(f"default_bit_depth must be one of: {valid_bit_depths}")
            
        valid_qualities = ["low", "medium", "high", "lossless"]
        if self.conversion_quality not in valid_qualities:
            raise ValidationError(f"conversion_quality must be one of: {valid_qualities}")


@dataclass
class SystemConfig:
    """
    System-level configuration options.
    
    Controls global behavior, resource management, and performance settings.
    """
    output_dir: str = "output"
    temp_dir: str = "temp"
    cache_enabled: bool = True
    max_cache_size_mb: int = 1000
    parallel_processing: bool = True
    max_workers: int = 4
    memory_limit_mb: Optional[int] = None
    log_level: str = "INFO"
    
    def validate(self) -> None:
        """
        Validate system configuration.
        
        Raises:
            ValidationError: If parameters are invalid
        """
        if self.max_cache_size_mb < 10:
            raise ValidationError("max_cache_size_mb must be at least 10")
            
        if self.max_workers < 1 or self.max_workers > 32:
            raise ValidationError("max_workers must be between 1 and 32")
            
        if self.memory_limit_mb is not None and self.memory_limit_mb < 100:
            raise ValidationError("memory_limit_mb must be at least 100 or None")
            
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if self.log_level not in valid_log_levels:
            raise ValidationError(f"log_level must be one of: {valid_log_levels}")


@dataclass
class MusicAIConfig:
    """
    Master configuration container for all MusicAITools settings.
    
    Combines all subsystem configurations into a single, coherent structure.
    """
    audio_restoration: AudioRestorationConfig = field(default_factory=AudioRestorationConfig)
    audio_separation: AudioSeparationConfig = field(default_factory=AudioSeparationConfig)
    visualization: VisualizationConfig = field(default_factory=VisualizationConfig)
    conversion: ConversionConfig = field(default_factory=ConversionConfig)
    system: SystemConfig = field(default_factory=SystemConfig)
    
    def validate(self) -> None:
        """
        Validate all configuration sections.
        
        Raises:
            ValidationError: If any subsection is invalid
        """
        self.audio_restoration.validate()
        self.audio_separation.validate()
        self.visualization.validate()
        self.conversion.validate()
        self.system.validate()


class ConfigManager:
    """
    Configuration manager with file loading and environment override support.
    
    Handles loading configuration from files, applying environment overrides,
    and providing validated configuration objects.
    """
    
    def __init__(self, config_file: Optional[Union[str, Path]] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_file: Path to configuration file (YAML or JSON)
        """
        self.logger = get_logger()
        self.config_file = Path(config_file) if config_file else None
        self._config = None
        
    def load_config(self) -> MusicAIConfig:
        """
        Load and validate configuration from file and environment.
        
        Returns:
            Validated configuration object
            
        Raises:
            ConfigurationError: If configuration loading or validation fails
        """
        if self._config is not None:
            return self._config
            
        # Start with default configuration
        config = MusicAIConfig()
        
        # Load from file if specified
        if self.config_file and self.config_file.exists():
            try:
                config = self._load_from_file(self.config_file, config)
                self.logger.info(f"Configuration loaded from: {self.config_file}")
            except Exception as e:
                self.logger.warning(f"Failed to load config file {self.config_file}: {e}")
                self.logger.info("Using default configuration")
        
        # Apply environment overrides
        config = self._apply_environment_overrides(config)
        
        # Validate final configuration
        try:
            config.validate()
            self.logger.info("Configuration validation successful")
        except ValidationError as e:
            raise ConfigurationError(f"Configuration validation failed: {e}")
        
        self._config = config
        return config
    
    def save_config(self, config: Optional[MusicAIConfig] = None) -> None:
        """
        Save current configuration to file.
        
        Args:
            config: Configuration to save (uses current if None)
            
        Raises:
            ConfigurationError: If saving fails
        """
        if config is None:
            config = self.get_config()
            
        if self.config_file is None:
            self.config_file = Path("musicaitools_config.yaml")
            
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(asdict(config), f, default_flow_style=False, sort_keys=False)
            
            self.logger.info(f"Configuration saved to: {self.config_file}")
            
        except Exception as e:
            raise ConfigurationError(f"Failed to save configuration: {e}")
    
    def get_config(self) -> MusicAIConfig:
        """
        Get current configuration, loading if necessary.
        
        Returns:
            Current configuration object
        """
        if self._config is None:
            return self.load_config()
        return self._config
    
    def _load_from_file(self, file_path: Path, base_config: MusicAIConfig) -> MusicAIConfig:
        """
        Load configuration from YAML or JSON file.
        
        Args:
            file_path: Path to configuration file
            base_config: Base configuration to update
            
        Returns:
            Updated configuration object
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            if file_path.suffix.lower() == '.yaml':
                data = yaml.safe_load(f)
            elif file_path.suffix.lower() == '.json':
                data = json.load(f)
            else:
                raise ConfigurationError(f"Unsupported config file format: {file_path.suffix}")
        
        return self._update_config_from_dict(base_config, data)
    
    def _update_config_from_dict(self, config: MusicAIConfig, data: Dict[str, Any]) -> MusicAIConfig:
        """
        Update configuration object from dictionary data.
        
        Args:
            config: Configuration object to update
            data: Dictionary with configuration values
            
        Returns:
            Updated configuration object
        """
        for section_name, section_data in data.items():
            if hasattr(config, section_name):
                section_obj = getattr(config, section_name)
                if hasattr(section_obj, '__dict__'):
                    for key, value in section_data.items():
                        if hasattr(section_obj, key):
                            setattr(section_obj, key, value)
                        else:
                            self.logger.warning(f"Unknown config key: {section_name}.{key}")
                else:
                    setattr(config, section_name, section_data)
            else:
                self.logger.warning(f"Unknown config section: {section_name}")
        
        return config
    
    def _apply_environment_overrides(self, config: MusicAIConfig) -> MusicAIConfig:
        """
        Apply environment variable overrides to configuration.
        
        Environment variables follow the pattern: MUSICAI_<SECTION>_<KEY>
        
        Args:
            config: Configuration object to update
            
        Returns:
            Configuration with environment overrides applied
        """
        env_prefix = "MUSICAI_"
        
        for env_key, env_value in os.environ.items():
            if not env_key.startswith(env_prefix):
                continue
                
            # Parse environment variable name
            config_path = env_key[len(env_prefix):].lower().split('_')
            if len(config_path) < 2:
                continue
                
            section_name = config_path[0]
            key_name = '_'.join(config_path[1:])
            
            # Apply override if section and key exist
            if hasattr(config, section_name):
                section_obj = getattr(config, section_name)
                if hasattr(section_obj, key_name):
                    # Convert string value to appropriate type
                    current_value = getattr(section_obj, key_name)
                    converted_value = self._convert_env_value(env_value, type(current_value))
                    setattr(section_obj, key_name, converted_value)
                    
                    self.logger.info(f"Applied environment override: {env_key}={env_value}")
        
        return config
    
    def _convert_env_value(self, value: str, target_type: type) -> Any:
        """
        Convert environment variable string to target type.
        
        Args:
            value: String value from environment
            target_type: Desired type for conversion
            
        Returns:
            Converted value
        """
        if target_type == bool:
            return value.lower() in ('true', '1', 'yes', 'on')
        elif target_type == int:
            return int(value)
        elif target_type == float:
            return float(value)
        elif target_type == tuple:
            # Assume comma-separated values for tuples
            return tuple(float(x.strip()) for x in value.split(','))
        else:
            return value


# Global configuration manager instance
_global_config_manager = ConfigManager()


def get_config() -> MusicAIConfig:
    """
    Get the global configuration instance.
    
    Returns:
        Current global configuration
    """
    return _global_config_manager.get_config()


def load_config_from_file(config_file: Union[str, Path]) -> MusicAIConfig:
    """
    Load configuration from specified file.
    
    Args:
        config_file: Path to configuration file
        
    Returns:
        Loaded configuration
    """
    manager = ConfigManager(config_file)
    return manager.load_config()


def save_config_to_file(config: MusicAIConfig, config_file: Union[str, Path]) -> None:
    """
    Save configuration to specified file.
    
    Args:
        config: Configuration to save
        config_file: Path for output file
    """
    manager = ConfigManager(config_file)
    manager.save_config(config)