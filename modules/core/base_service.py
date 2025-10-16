"""
Base service classes for MusicAITools framework.

This module provides abstract base classes and common functionality
for all processing services in the framework.
"""

import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional, Union, List
from contextlib import contextmanager

from .models import (
    ProcessingResult, ProcessingStatus, AudioFile, 
    BatchProcessingResult
)
from .logger import get_logger
from .config import get_config
from .exceptions import (
    MusicAIToolsException, AudioProcessingError, 
    FileNotFoundError, ValidationError
)


class BaseService(ABC):
    """
    Abstract base class for all processing services.
    
    Provides common functionality including:
    - Input validation
    - Error handling
    - Performance monitoring
    - Output management
    - Logging integration
    """
    
    def __init__(self, service_name: str):
        """
        Initialize base service.
        
        Args:
            service_name: Human-readable name for the service
        """
        self.service_name = service_name
        self.logger = get_logger()
        self.config = get_config()
        self._processing_stats = {
            'total_operations': 0,
            'successful_operations': 0,
            'failed_operations': 0,
            'total_processing_time': 0.0
        }
    
    @abstractmethod
    def process(self, input_data: Any, **kwargs) -> ProcessingResult:
        """
        Main processing method to be implemented by subclasses.
        
        Args:
            input_data: Input data for processing
            **kwargs: Additional processing parameters
            
        Returns:
            ProcessingResult: Result of the processing operation
        """
        pass
    
    def safe_process(self, input_data: Any, **kwargs) -> ProcessingResult:
        """
        Safe wrapper for processing with error handling and monitoring.
        
        Args:
            input_data: Input data for processing
            **kwargs: Additional processing parameters
            
        Returns:
            ProcessingResult: Result with error handling applied
        """
        start_time = time.time()
        operation_id = self._generate_operation_id()
        
        try:
            self.logger.info(f"Starting {self.service_name} operation {operation_id}")
            
            # Pre-processing validation
            self._validate_input(input_data, **kwargs)
            
            # Execute main processing
            result = self.process(input_data, **kwargs)
            
            # Post-processing validation
            self._validate_result(result)
            
            # Update timing and statistics
            processing_time = time.time() - start_time
            result.processing_time = processing_time
            
            self._update_stats(success=True, processing_time=processing_time)
            
            self.logger.info(
                f"{self.service_name} operation {operation_id} completed successfully "
                f"in {processing_time:.3f}s"
            )
            
            return result
            
        except MusicAIToolsException as e:
            processing_time = time.time() - start_time
            self._update_stats(success=False, processing_time=processing_time)
            
            self.logger.error(
                f"{self.service_name} operation {operation_id} failed: {e}",
                extra={'operation_id': operation_id, 'error_type': type(e).__name__}
            )
            
            return self._create_error_result(str(e), processing_time)
            
        except Exception as e:
            processing_time = time.time() - start_time
            self._update_stats(success=False, processing_time=processing_time)
            
            self.logger.exception(
                f"Unexpected error in {self.service_name} operation {operation_id}: {e}",
                extra={'operation_id': operation_id}
            )
            
            return self._create_error_result(f"Unexpected error: {str(e)}", processing_time)
    
    def process_batch(self, 
                     input_files: List[Union[str, Path]], 
                     **kwargs) -> BatchProcessingResult:
        """
        Process multiple files in batch with progress tracking.
        
        Args:
            input_files: List of input file paths
            **kwargs: Processing parameters applied to all files
            
        Returns:
            BatchProcessingResult: Aggregated results from all operations
        """
        batch_result = BatchProcessingResult()
        total_files = len(input_files)
        
        self.logger.info(f"Starting batch processing of {total_files} files with {self.service_name}")
        
        for i, input_file in enumerate(input_files, 1):
            self.logger.info(f"Processing file {i}/{total_files}: {input_file}")
            
            try:
                result = self.safe_process(input_file, **kwargs)
                batch_result.add_result(result)
                
                if result.success:
                    self.logger.info(f"File {i}/{total_files} processed successfully")
                else:
                    self.logger.warning(f"File {i}/{total_files} processing failed: {result.error_message}")
                    
            except Exception as e:
                # Create error result for batch tracking
                error_result = self._create_error_result(f"Batch processing error: {e}")
                batch_result.add_result(error_result)
                
                self.logger.error(f"Critical error processing file {i}/{total_files}: {e}")
        
        self.logger.info(
            f"Batch processing completed: {batch_result.successful_files}/{total_files} successful, "
            f"success rate: {batch_result.success_rate:.1f}%"
        )
        
        return batch_result
    
    def _validate_input(self, input_data: Any, **kwargs) -> None:
        """
        Validate input data before processing.
        
        Args:
            input_data: Input data to validate
            **kwargs: Additional parameters to validate
            
        Raises:
            ValidationError: If validation fails
        """
        # Default implementation - subclasses should override for specific validation
        if input_data is None:
            raise ValidationError("Input data cannot be None")
    
    def _validate_result(self, result: ProcessingResult) -> None:
        """
        Validate processing result.
        
        Args:
            result: Processing result to validate
            
        Raises:
            ValidationError: If result validation fails
        """
        if not isinstance(result, ProcessingResult):
            raise ValidationError("Process method must return ProcessingResult instance")
        
        if result.status not in ProcessingStatus:
            raise ValidationError(f"Invalid processing status: {result.status}")
    
    def _validate_audio_file(self, file_path: Union[str, Path]) -> AudioFile:
        """
        Validate and create AudioFile object from path.
        
        Args:
            file_path: Path to audio file
            
        Returns:
            AudioFile: Validated audio file object
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValidationError: If file is invalid
        """
        audio_file = AudioFile(path=Path(file_path))
        
        if not audio_file.exists:
            raise FileNotFoundError(f"Audio file does not exist: {audio_file.path}")
        
        audio_file.validate()
        return audio_file
    
    def _ensure_output_directory(self, output_path: Path) -> None:
        """
        Ensure output directory exists, creating if necessary.
        
        Args:
            output_path: Path that should have existing parent directory
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
    
    def _generate_output_path(self, 
                             input_path: Path, 
                             suffix: str = "", 
                             extension: Optional[str] = None,
                             output_dir: Optional[Path] = None) -> Path:
        """
        Generate output file path based on input path.
        
        Args:
            input_path: Source file path
            suffix: Suffix to add to filename
            extension: New file extension (keeps original if None)
            output_dir: Output directory (uses config default if None)
            
        Returns:
            Generated output file path
        """
        if output_dir is None:
            output_dir = Path(self.config.system.output_dir)
        
        # Build new filename
        stem = input_path.stem + suffix
        ext = extension or input_path.suffix
        if not ext.startswith('.'):
            ext = '.' + ext
        
        output_path = output_dir / f"{stem}{ext}"
        self._ensure_output_directory(output_path)
        
        return output_path
    
    def _create_success_result(self, 
                              output_files: List[Path] = None,
                              metadata: Dict[str, Any] = None) -> ProcessingResult:
        """
        Create successful processing result.
        
        Args:
            output_files: List of output file paths
            metadata: Additional metadata
            
        Returns:
            ProcessingResult: Success result object
        """
        return ProcessingResult(
            status=ProcessingStatus.SUCCESS,
            output_files=output_files or [],
            metadata=metadata or {}
        )
    
    def _create_error_result(self, 
                            error_message: str,
                            processing_time: Optional[float] = None) -> ProcessingResult:
        """
        Create error processing result.
        
        Args:
            error_message: Description of the error
            processing_time: Time spent before error occurred
            
        Returns:
            ProcessingResult: Error result object
        """
        return ProcessingResult(
            status=ProcessingStatus.FAILED,
            error_message=error_message,
            processing_time=processing_time
        )
    
    def _update_stats(self, success: bool, processing_time: float) -> None:
        """
        Update internal processing statistics.
        
        Args:
            success: Whether operation was successful
            processing_time: Time taken for operation
        """
        self._processing_stats['total_operations'] += 1
        self._processing_stats['total_processing_time'] += processing_time
        
        if success:
            self._processing_stats['successful_operations'] += 1
        else:
            self._processing_stats['failed_operations'] += 1
    
    def _generate_operation_id(self) -> str:
        """
        Generate unique operation ID for tracking.
        
        Returns:
            Unique operation identifier
        """
        import uuid
        return str(uuid.uuid4())[:8]
    
    @contextmanager
    def _performance_monitor(self, operation_name: str):
        """
        Context manager for performance monitoring.
        
        Args:
            operation_name: Name of operation being monitored
        """
        start_time = time.time()
        start_memory = self._get_memory_usage()
        
        try:
            yield
        finally:
            end_time = time.time()
            end_memory = self._get_memory_usage()
            
            duration = end_time - start_time
            memory_delta = end_memory - start_memory if start_memory and end_memory else None
            
            self.logger.debug(
                f"Performance: {operation_name} took {duration:.3f}s",
                extra={
                    'operation': operation_name,
                    'duration': duration,
                    'memory_delta_mb': memory_delta
                }
            )
    
    def _get_memory_usage(self) -> Optional[float]:
        """
        Get current memory usage in MB.
        
        Returns:
            Memory usage in MB or None if unavailable
        """
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024
        except ImportError:
            return None
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get processing statistics for this service.
        
        Returns:
            Dictionary with processing statistics
        """
        stats = self._processing_stats.copy()
        
        if stats['total_operations'] > 0:
            stats['success_rate'] = (
                stats['successful_operations'] / stats['total_operations'] * 100
            )
            stats['average_processing_time'] = (
                stats['total_processing_time'] / stats['total_operations']
            )
        else:
            stats['success_rate'] = 0.0
            stats['average_processing_time'] = 0.0
        
        return stats
    
    def reset_stats(self) -> None:
        """Reset processing statistics."""
        self._processing_stats = {
            'total_operations': 0,
            'successful_operations': 0,
            'failed_operations': 0,
            'total_processing_time': 0.0
        }