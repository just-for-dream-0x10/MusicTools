"""
Data models for MusicAITools framework.

This module defines structured data classes for representing audio files,
processing results, and other framework entities with type safety and validation.
"""

import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from enum import Enum
import numpy as np

from .exceptions import ValidationError


class AudioFormat(Enum):
    """Supported audio file formats."""
    WAV = "wav"
    MP3 = "mp3"
    FLAC = "flac"
    OGG = "ogg"
    M4A = "m4a"
    AAC = "aac"


class ProcessingStatus(Enum):
    """Status codes for processing operations."""
    SUCCESS = "success"
    FAILED = "failed"
    PROCESSING = "processing"
    CANCELLED = "cancelled"
    PENDING = "pending"


class TrackType(Enum):
    """Types of separated audio tracks."""
    VOCALS = "vocals"
    DRUMS = "drums"
    BASS = "bass"
    OTHER = "other"
    PIANO = "piano"
    GUITAR = "guitar"


@dataclass
class AudioFile:
    """
    Represents an audio file with metadata and validation.
    
    Provides structured representation of audio files including
    path validation, format detection, and metadata storage.
    """
    path: Path
    sample_rate: Optional[int] = None
    duration: Optional[float] = None
    channels: Optional[int] = None
    format: Optional[AudioFormat] = None
    file_size_bytes: Optional[int] = None
    bit_depth: Optional[int] = None
    
    def __post_init__(self):
        """
        Post-initialization validation and format detection.
        
        Automatically converts string paths to Path objects and
        attempts to detect audio format from file extension.
        """
        if isinstance(self.path, str):
            self.path = Path(self.path)
        
        # Auto-detect format from extension
        if self.format is None and self.path.suffix:
            try:
                format_str = self.path.suffix.lower().lstrip('.')
                self.format = AudioFormat(format_str)
            except ValueError:
                # Unknown format, will be detected during processing
                pass
        
        # Get file size if file exists
        if self.path.exists():
            self.file_size_bytes = self.path.stat().st_size
    
    @property
    def exists(self) -> bool:
        """Check if the audio file exists on disk."""
        return self.path.exists()
    
    @property
    def size_mb(self) -> Optional[float]:
        """Get file size in megabytes."""
        if self.file_size_bytes is not None:
            return self.file_size_bytes / (1024 * 1024)
        return None
    
    def validate(self) -> None:
        """
        Validate audio file properties.
        
        Raises:
            ValidationError: If validation fails
        """
        if not self.path.exists():
            raise ValidationError(f"Audio file does not exist: {self.path}")
        
        if not self.path.is_file():
            raise ValidationError(f"Path is not a regular file: {self.path}")
        
        if self.sample_rate is not None and self.sample_rate <= 0:
            raise ValidationError(f"Invalid sample rate: {self.sample_rate}")
        
        if self.duration is not None and self.duration <= 0:
            raise ValidationError(f"Invalid duration: {self.duration}")
        
        if self.channels is not None and self.channels <= 0:
            raise ValidationError(f"Invalid channel count: {self.channels}")


@dataclass
class ProcessingResult:
    """
    Base class for all processing operation results.
    
    Provides standardized structure for operation outcomes including
    status tracking, error handling, and performance metrics.
    """
    status: ProcessingStatus
    output_files: List[Path] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None
    processing_time: Optional[float] = None
    timestamp: float = field(default_factory=time.time)
    
    @property
    def success(self) -> bool:
        """Check if processing was successful."""
        return self.status == ProcessingStatus.SUCCESS
    
    @property
    def failed(self) -> bool:
        """Check if processing failed."""
        return self.status == ProcessingStatus.FAILED
    
    def add_output_file(self, file_path: Union[str, Path]) -> None:
        """
        Add an output file to the result.
        
        Args:
            file_path: Path to the output file
        """
        self.output_files.append(Path(file_path))
    
    def add_metadata(self, key: str, value: Any) -> None:
        """
        Add metadata to the result.
        
        Args:
            key: Metadata key
            value: Metadata value
        """
        self.metadata[key] = value
    
    def get_metadata(self, key: str, default: Any = None) -> Any:
        """
        Get metadata value by key.
        
        Args:
            key: Metadata key
            default: Default value if key not found
            
        Returns:
            Metadata value or default
        """
        return self.metadata.get(key, default)


@dataclass
class SeparationResult(ProcessingResult):
    """
    Result of audio source separation operation.
    
    Contains separated track files organized by track type
    with additional separation-specific metadata.
    """
    separated_tracks: Dict[TrackType, Path] = field(default_factory=dict)
    separation_model: Optional[str] = None
    separation_quality_score: Optional[float] = None
    
    def get_track(self, track_type: Union[TrackType, str]) -> Optional[Path]:
        """
        Get path to separated track by type.
        
        Args:
            track_type: Type of track to retrieve
            
        Returns:
            Path to track file or None if not found
        """
        if isinstance(track_type, str):
            try:
                track_type = TrackType(track_type.lower())
            except ValueError:
                return None
        
        return self.separated_tracks.get(track_type)
    
    def add_track(self, track_type: Union[TrackType, str], file_path: Union[str, Path]) -> None:
        """
        Add a separated track to the result.
        
        Args:
            track_type: Type of the track
            file_path: Path to the track file
        """
        if isinstance(track_type, str):
            track_type = TrackType(track_type.lower())
        
        track_path = Path(file_path)
        self.separated_tracks[track_type] = track_path
        self.add_output_file(track_path)
    
    @property
    def available_tracks(self) -> List[TrackType]:
        """Get list of available track types."""
        return list(self.separated_tracks.keys())


@dataclass
class RestorationResult(ProcessingResult):
    """
    Result of audio restoration operation.
    
    Contains restored audio file and quality improvement metrics.
    """
    restored_file: Optional[Path] = None
    improvement_metrics: Dict[str, float] = field(default_factory=dict)
    restoration_settings: Dict[str, Any] = field(default_factory=dict)
    
    def get_improvement(self, metric: str) -> Optional[float]:
        """
        Get improvement value for specific metric.
        
        Args:
            metric: Name of the improvement metric
            
        Returns:
            Improvement value or None if not available
        """
        return self.improvement_metrics.get(metric)
    
    def add_improvement_metric(self, metric: str, value: float) -> None:
        """
        Add an improvement metric to the result.
        
        Args:
            metric: Name of the metric
            value: Improvement value
        """
        self.improvement_metrics[metric] = value
    
    @property
    def overall_improvement(self) -> Optional[float]:
        """
        Calculate overall improvement score.
        
        Returns:
            Weighted average of improvement metrics
        """
        if not self.improvement_metrics:
            return None
        
        # Weighted scoring for different metrics
        weights = {
            'snr_improvement_db': 0.4,
            'thd_improvement': 0.3,
            'spectral_flatness_improvement': 0.2,
            'noise_reduction_score': 0.1
        }
        
        weighted_sum = 0.0
        total_weight = 0.0
        
        for metric, value in self.improvement_metrics.items():
            weight = weights.get(metric, 0.1)
            weighted_sum += value * weight
            total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else None


@dataclass
class ConversionResult(ProcessingResult):
    """
    Result of format conversion operation.
    
    Contains converted file and conversion metadata.
    """
    converted_file: Optional[Path] = None
    original_format: Optional[AudioFormat] = None
    target_format: Optional[AudioFormat] = None
    quality_loss: Optional[float] = None
    compression_ratio: Optional[float] = None
    
    @property
    def format_changed(self) -> bool:
        """Check if format was actually changed."""
        return (self.original_format is not None and 
                self.target_format is not None and
                self.original_format != self.target_format)


@dataclass
class VisualizationResult(ProcessingResult):
    """
    Result of audio visualization operation.
    
    Contains generated visualization files and plot metadata.
    """
    image_files: List[Path] = field(default_factory=list)
    plot_types: List[str] = field(default_factory=list)
    visualization_config: Dict[str, Any] = field(default_factory=dict)
    
    def add_visualization(self, plot_type: str, file_path: Union[str, Path]) -> None:
        """
        Add a visualization to the result.
        
        Args:
            plot_type: Type of visualization (e.g., 'waveform', 'spectrogram')
            file_path: Path to the visualization file
        """
        image_path = Path(file_path)
        self.plot_types.append(plot_type)
        self.image_files.append(image_path)
        self.add_output_file(image_path)
    
    def get_visualization(self, plot_type: str) -> Optional[Path]:
        """
        Get visualization file by plot type.
        
        Args:
            plot_type: Type of visualization to retrieve
            
        Returns:
            Path to visualization file or None if not found
        """
        try:
            index = self.plot_types.index(plot_type)
            return self.image_files[index]
        except (ValueError, IndexError):
            return None


@dataclass
class AnalysisResult(ProcessingResult):
    """
    Result of audio analysis operation.
    
    Contains analysis data and extracted features.
    """
    analysis_data: Dict[str, Any] = field(default_factory=dict)
    features: Dict[str, np.ndarray] = field(default_factory=dict)
    analysis_type: Optional[str] = None
    
    def add_feature(self, feature_name: str, feature_data: np.ndarray) -> None:
        """
        Add extracted feature to the result.
        
        Args:
            feature_name: Name of the feature
            feature_data: Feature data array
        """
        self.features[feature_name] = feature_data
    
    def get_feature(self, feature_name: str) -> Optional[np.ndarray]:
        """
        Get feature data by name.
        
        Args:
            feature_name: Name of the feature to retrieve
            
        Returns:
            Feature data array or None if not found
        """
        return self.features.get(feature_name)
    
    def add_analysis_data(self, key: str, value: Any) -> None:
        """
        Add analysis data to the result.
        
        Args:
            key: Data key
            value: Data value
        """
        self.analysis_data[key] = value
    
    def get_analysis_data(self, key: str, default: Any = None) -> Any:
        """
        Get analysis data by key.
        
        Args:
            key: Data key
            default: Default value if key not found
            
        Returns:
            Analysis data or default value
        """
        return self.analysis_data.get(key, default)


@dataclass
class BatchProcessingResult:
    """
    Result of batch processing operations.
    
    Aggregates results from multiple individual operations.
    """
    individual_results: List[ProcessingResult] = field(default_factory=list)
    total_files: int = 0
    successful_files: int = 0
    failed_files: int = 0
    total_processing_time: float = 0.0
    
    def add_result(self, result: ProcessingResult) -> None:
        """
        Add an individual processing result.
        
        Args:
            result: Processing result to add
        """
        self.individual_results.append(result)
        self.total_files += 1
        
        if result.success:
            self.successful_files += 1
        else:
            self.failed_files += 1
        
        if result.processing_time:
            self.total_processing_time += result.processing_time
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage."""
        if self.total_files == 0:
            return 0.0
        return (self.successful_files / self.total_files) * 100.0
    
    @property
    def average_processing_time(self) -> float:
        """Calculate average processing time per file."""
        if self.total_files == 0:
            return 0.0
        return self.total_processing_time / self.total_files
    
    def get_failed_results(self) -> List[ProcessingResult]:
        """Get list of failed processing results."""
        return [result for result in self.individual_results if result.failed]
    
    def get_successful_results(self) -> List[ProcessingResult]:
        """Get list of successful processing results."""
        return [result for result in self.individual_results if result.success]