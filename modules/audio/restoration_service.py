"""
Audio restoration service with advanced signal processing.

This module provides comprehensive audio restoration capabilities including:
- Noise reduction using spectral subtraction
- Multi-band equalization
- Dynamic range processing
- Quality assessment metrics
"""

import numpy as np
import librosa
import soundfile as sf
from scipy import signal
from pathlib import Path
from typing import Optional, Dict, Any, Tuple

from ..core.base_service import BaseService
from ..core.models import (
    ProcessingResult, ProcessingStatus, RestorationResult, 
    AudioFile, AudioFormat
)
from ..core.config import get_config
from ..core.exceptions import AudioProcessingError, ValidationError


class AudioRestorationService(BaseService):
    """
    Professional audio restoration service.
    
    Implements advanced signal processing algorithms for:
    - Noise reduction and artifact removal
    - Frequency response correction
    - Dynamic range optimization
    - Audio quality enhancement
    """
    
    def __init__(self):
        """Initialize audio restoration service."""
        super().__init__("AudioRestoration")
        self.restoration_config = get_config().audio_restoration
    
    def process(self, 
               input_file: str,
               output_file: Optional[str] = None,
               custom_settings: Optional[Dict[str, Any]] = None) -> RestorationResult:
        """
        Restore audio file with configurable enhancement algorithms.
        
        Args:
            input_file: Path to input audio file
            output_file: Path for restored output (auto-generated if None)
            custom_settings: Override default restoration settings
            
        Returns:
            RestorationResult: Comprehensive restoration results with metrics
            
        Raises:
            AudioProcessingError: If restoration process fails
        """
        # Validate and prepare input
        audio_file = self._validate_audio_file(input_file)
        output_path = self._prepare_output_path(audio_file, output_file)
        settings = self._merge_settings(custom_settings)
        
        try:
            with self._performance_monitor("audio_loading"):
                audio_data, sample_rate = self._load_audio(audio_file.path)
            
            # Store original for comparison
            original_audio = audio_data.copy()
            
            # Apply restoration pipeline
            with self._performance_monitor("restoration_pipeline"):
                restored_audio = self._apply_restoration_pipeline(
                    audio_data, sample_rate, settings
                )
            
            # Calculate improvement metrics
            with self._performance_monitor("quality_assessment"):
                improvement_metrics = self._calculate_improvement_metrics(
                    original_audio, restored_audio, sample_rate
                )
            
            # Save restored audio
            with self._performance_monitor("audio_saving"):
                self._save_audio(restored_audio, sample_rate, output_path)
            
            self.logger.info(
                f"Audio restoration completed: {output_path} "
                f"(SNR improvement: {improvement_metrics.get('snr_improvement_db', 0):.2f}dB)"
            )
            
            return RestorationResult(
                status=ProcessingStatus.SUCCESS,
                output_files=[output_path],
                metadata={
                    'input_file': str(audio_file.path),
                    'sample_rate': sample_rate,
                    'duration_seconds': len(original_audio) / sample_rate,
                    'channels': 1 if len(original_audio.shape) == 1 else original_audio.shape[1],
                    'settings_used': settings
                },
                restored_file=output_path,
                improvement_metrics=improvement_metrics,
                restoration_settings=settings
            )
            
        except Exception as e:
            raise AudioProcessingError(f"Audio restoration failed: {e}")
    
    def _prepare_output_path(self, 
                           audio_file: AudioFile, 
                           output_file: Optional[str]) -> Path:
        """
        Prepare output file path with proper naming convention.
        
        Args:
            audio_file: Input audio file object
            output_file: User-specified output path or None
            
        Returns:
            Path: Validated output file path
        """
        if output_file is None:
            return self._generate_output_path(
                audio_file.path, 
                suffix="_restored",
                extension=audio_file.path.suffix
            )
        
        output_path = Path(output_file)
        self._ensure_output_directory(output_path)
        return output_path
    
    def _merge_settings(self, custom_settings: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Merge custom settings with default configuration.
        
        Args:
            custom_settings: User-provided setting overrides
            
        Returns:
            Dict: Merged restoration settings
        """
        settings = {
            'noise_reduction': self.restoration_config.noise_reduction,
            'eq_low': self.restoration_config.eq_low,
            'eq_mid': self.restoration_config.eq_mid,
            'eq_high': self.restoration_config.eq_high,
            'enable_spectral_gating': self.restoration_config.enable_spectral_gating,
            'enable_dynamic_range_compression': self.restoration_config.enable_dynamic_range_compression,
            'compression_ratio': self.restoration_config.compression_ratio
        }
        
        if custom_settings:
            settings.update(custom_settings)
            self.logger.info(f"Applied custom settings: {custom_settings}")
        
        # Validate merged settings
        self._validate_settings(settings)
        
        return settings
    
    def _validate_settings(self, settings: Dict[str, Any]) -> None:
        """
        Validate restoration settings parameters.
        
        Args:
            settings: Settings dictionary to validate
            
        Raises:
            ValidationError: If any setting is invalid
        """
        if not 0.0 <= settings['noise_reduction'] <= 1.0:
            raise ValidationError("noise_reduction must be between 0.0 and 1.0")
        
        for eq_param in ['eq_low', 'eq_mid', 'eq_high']:
            if not 0.0 <= settings[eq_param] <= 3.0:
                raise ValidationError(f"{eq_param} must be between 0.0 and 3.0")
        
        if not 1.0 <= settings['compression_ratio'] <= 10.0:
            raise ValidationError("compression_ratio must be between 1.0 and 10.0")
    
    def _load_audio(self, file_path: Path) -> Tuple[np.ndarray, int]:
        """
        Load audio file with format detection and validation.
        
        Args:
            file_path: Path to audio file
            
        Returns:
            Tuple of (audio_data, sample_rate)
            
        Raises:
            AudioProcessingError: If audio loading fails
        """
        try:
            # Use librosa for robust audio loading
            audio_data, sample_rate = librosa.load(
                str(file_path), 
                sr=None,  # Preserve original sample rate
                mono=False  # Preserve stereo if present
            )
            
            # Ensure consistent data type
            audio_data = audio_data.astype(np.float32)
            
            # Convert stereo to mono if needed for processing
            if len(audio_data.shape) > 1:
                audio_data = librosa.to_mono(audio_data)
            
            self.logger.debug(
                f"Loaded audio: {audio_data.shape} samples at {sample_rate}Hz"
            )
            
            return audio_data, sample_rate
            
        except Exception as e:
            raise AudioProcessingError(f"Failed to load audio file {file_path}: {e}")
    
    def _save_audio(self, 
                   audio_data: np.ndarray, 
                   sample_rate: int, 
                   output_path: Path) -> None:
        """
        Save audio data to file with optimal quality settings.
        
        Args:
            audio_data: Audio data to save
            sample_rate: Audio sample rate
            output_path: Output file path
            
        Raises:
            AudioProcessingError: If audio saving fails
        """
        try:
            # Determine output format and parameters
            file_extension = output_path.suffix.lower().lstrip('.')
            
            # Quality settings based on format
            if file_extension == 'wav':
                subtype = 'PCM_16'
            elif file_extension == 'flac':
                subtype = 'PCM_16'
            else:
                subtype = None
            
            # Save with soundfile for better format support
            sf.write(
                str(output_path),
                audio_data,
                sample_rate,
                subtype=subtype
            )
            
            self.logger.debug(f"Saved restored audio to: {output_path}")
            
        except Exception as e:
            raise AudioProcessingError(f"Failed to save audio to {output_path}: {e}")
    
    def _apply_restoration_pipeline(self, 
                                  audio_data: np.ndarray, 
                                  sample_rate: int,
                                  settings: Dict[str, Any]) -> np.ndarray:
        """
        Apply comprehensive restoration pipeline to audio.
        
        Args:
            audio_data: Input audio data
            sample_rate: Audio sample rate
            settings: Restoration settings
            
        Returns:
            np.ndarray: Restored audio data
        """
        restored = audio_data.copy()
        
        # Step 1: Noise reduction
        if settings['noise_reduction'] > 0:
            self.logger.debug("Applying noise reduction")
            restored = self._apply_noise_reduction(
                restored, sample_rate, settings['noise_reduction']
            )
        
        # Step 2: Spectral gating (advanced noise removal)
        if settings.get('enable_spectral_gating', False):
            self.logger.debug("Applying spectral gating")
            restored = self._apply_spectral_gating(restored, sample_rate)
        
        # Step 3: Equalization
        self.logger.debug("Applying equalization")
        restored = self._apply_multiband_equalizer(restored, sample_rate, settings)
        
        # Step 4: Dynamic range compression
        if settings.get('enable_dynamic_range_compression', False):
            self.logger.debug("Applying dynamic range compression")
            restored = self._apply_dynamic_range_compression(
                restored, settings['compression_ratio']
            )
        
        # Step 5: Final normalization
        restored = self._normalize_audio(restored)
        
        return restored
    
    def _apply_noise_reduction(self, 
                             audio_data: np.ndarray, 
                             sample_rate: int,
                             reduction_strength: float) -> np.ndarray:
        """
        Apply advanced spectral subtraction for noise reduction.
        
        Args:
            audio_data: Input audio data
            sample_rate: Audio sample rate
            reduction_strength: Noise reduction strength (0.0-1.0)
            
        Returns:
            np.ndarray: Noise-reduced audio
        """
        # STFT parameters
        n_fft = 2048
        hop_length = n_fft // 4
        
        # Compute STFT
        stft_matrix = librosa.stft(audio_data, n_fft=n_fft, hop_length=hop_length)
        magnitude = np.abs(stft_matrix)
        phase = np.angle(stft_matrix)
        
        # Estimate noise spectrum from quieter sections
        noise_frames = int(magnitude.shape[1] * 0.1)  # First 10% as noise estimate
        noise_profile = np.median(magnitude[:, :noise_frames], axis=1, keepdims=True)
        
        # Adaptive spectral subtraction
        alpha = reduction_strength * 2.0  # Scaling factor
        beta = 0.01  # Floor factor to prevent over-subtraction
        
        # Calculate spectral gain
        snr_estimate = magnitude / (noise_profile + 1e-10)
        gain = 1.0 - alpha / snr_estimate
        gain = np.maximum(gain, beta)
        
        # Apply smoothing to gain to reduce artifacts
        gain = self._smooth_spectral_gain(gain)
        
        # Apply gain and reconstruct
        enhanced_magnitude = magnitude * gain
        enhanced_stft = enhanced_magnitude * np.exp(1j * phase)
        
        return librosa.istft(enhanced_stft, hop_length=hop_length)
    
    def _smooth_spectral_gain(self, gain: np.ndarray, smoothing_factor: float = 0.7) -> np.ndarray:
        """
        Apply temporal smoothing to spectral gain to reduce musical noise.
        
        Args:
            gain: Spectral gain matrix
            smoothing_factor: Smoothing strength (0.0-1.0)
            
        Returns:
            np.ndarray: Smoothed gain matrix
        """
        smoothed_gain = gain.copy()
        
        for i in range(1, gain.shape[1]):
            smoothed_gain[:, i] = (
                smoothing_factor * smoothed_gain[:, i-1] + 
                (1 - smoothing_factor) * gain[:, i]
            )
        
        return smoothed_gain
    
    def _apply_spectral_gating(self, 
                             audio_data: np.ndarray, 
                             sample_rate: int) -> np.ndarray:
        """
        Apply spectral gating for advanced noise suppression.
        
        Args:
            audio_data: Input audio data
            sample_rate: Audio sample rate
            
        Returns:
            np.ndarray: Processed audio with spectral gating
        """
        # Compute spectral features
        stft_matrix = librosa.stft(audio_data)
        magnitude = np.abs(stft_matrix)
        
        # Calculate spectral centroid and rolloff for gating decisions
        spectral_centroids = librosa.feature.spectral_centroid(S=magnitude)[0]
        spectral_rolloff = librosa.feature.spectral_rolloff(S=magnitude)[0]
        
        # Create gate based on spectral characteristics
        gate_threshold = np.percentile(spectral_centroids, 25)
        gate_mask = spectral_centroids > gate_threshold
        
        # Apply gating to STFT
        gated_stft = stft_matrix.copy()
        for i, should_gate in enumerate(gate_mask):
            if not should_gate:
                gated_stft[:, i] *= 0.3  # Attenuate rather than completely remove
        
        return librosa.istft(gated_stft)
    
    def _apply_multiband_equalizer(self, 
                                 audio_data: np.ndarray, 
                                 sample_rate: int,
                                 settings: Dict[str, Any]) -> np.ndarray:
        """
        Apply sophisticated multiband equalization.
        
        Args:
            audio_data: Input audio data
            sample_rate: Audio sample rate
            settings: EQ settings dictionary
            
        Returns:
            np.ndarray: Equalized audio
        """
        nyquist = sample_rate / 2
        
        # Define frequency bands (Hz)
        low_cutoff = 300 / nyquist
        high_cutoff = 3000 / nyquist
        
        # Design filters with better characteristics
        # Low band (bass): 20-300 Hz
        low_band = self._apply_bandpass_filter(
            audio_data, 0.01, low_cutoff, sample_rate
        ) * settings['eq_low']
        
        # Mid band: 300-3000 Hz  
        mid_band = self._apply_bandpass_filter(
            audio_data, low_cutoff, high_cutoff, sample_rate
        ) * settings['eq_mid']
        
        # High band (treble): 3000+ Hz
        high_band = self._apply_highpass_filter(
            audio_data, high_cutoff, sample_rate
        ) * settings['eq_high']
        
        # Combine bands with overlap compensation
        equalized = low_band + mid_band + high_band
        
        return equalized
    
    def _apply_bandpass_filter(self, 
                             audio_data: np.ndarray,
                             low_freq: float, 
                             high_freq: float,
                             sample_rate: int) -> np.ndarray:
        """
        Apply bandpass filter with specified frequency range.
        
        Args:
            audio_data: Input audio data
            low_freq: Low cutoff frequency (normalized)
            high_freq: High cutoff frequency (normalized)
            sample_rate: Audio sample rate
            
        Returns:
            np.ndarray: Filtered audio
        """
        try:
            # Design Butterworth bandpass filter
            order = 4
            sos = signal.butter(
                order, [low_freq, high_freq], 
                btype='bandpass', output='sos'
            )
            
            # Apply filter with zero-phase filtering
            return signal.sosfiltfilt(sos, audio_data)
            
        except Exception as e:
            self.logger.warning(f"Bandpass filter failed, using original: {e}")
            return audio_data
    
    def _apply_highpass_filter(self, 
                             audio_data: np.ndarray,
                             cutoff_freq: float, 
                             sample_rate: int) -> np.ndarray:
        """
        Apply highpass filter with specified cutoff frequency.
        
        Args:
            audio_data: Input audio data
            cutoff_freq: Cutoff frequency (normalized)
            sample_rate: Audio sample rate
            
        Returns:
            np.ndarray: Filtered audio
        """
        try:
            order = 4
            sos = signal.butter(order, cutoff_freq, btype='highpass', output='sos')
            return signal.sosfiltfilt(sos, audio_data)
            
        except Exception as e:
            self.logger.warning(f"Highpass filter failed, using original: {e}")
            return audio_data
    
    def _apply_dynamic_range_compression(self, 
                                       audio_data: np.ndarray,
                                       compression_ratio: float) -> np.ndarray:
        """
        Apply dynamic range compression to control audio dynamics.
        
        Args:
            audio_data: Input audio data
            compression_ratio: Compression ratio (1.0 = no compression)
            
        Returns:
            np.ndarray: Compressed audio
        """
        # Simple threshold-based compression
        threshold = 0.7
        
        # Calculate envelope
        envelope = np.abs(audio_data)
        
        # Apply compression above threshold
        compressed = audio_data.copy()
        above_threshold = envelope > threshold
        
        if np.any(above_threshold):
            # Compress signals above threshold
            gain_reduction = 1.0 / compression_ratio
            compressed[above_threshold] *= gain_reduction
        
        return compressed
    
    def _normalize_audio(self, audio_data: np.ndarray, target_peak: float = 0.95) -> np.ndarray:
        """
        Normalize audio to specified peak level.
        
        Args:
            audio_data: Input audio data
            target_peak: Target peak level (0.0-1.0)
            
        Returns:
            np.ndarray: Normalized audio
        """
        current_peak = np.max(np.abs(audio_data))
        
        if current_peak > 0:
            normalization_factor = target_peak / current_peak
            return audio_data * normalization_factor
        
        return audio_data
    
    def _calculate_improvement_metrics(self, 
                                     original: np.ndarray,
                                     restored: np.ndarray, 
                                     sample_rate: int) -> Dict[str, float]:
        """
        Calculate comprehensive audio improvement metrics.
        
        Args:
            original: Original audio data
            restored: Restored audio data
            sample_rate: Audio sample rate
            
        Returns:
            Dict: Improvement metrics
        """
        metrics = {}
        
        try:
            # Signal-to-Noise Ratio improvement
            snr_original = self._calculate_snr(original)
            snr_restored = self._calculate_snr(restored)
            metrics['snr_improvement_db'] = snr_restored - snr_original
            
            # Total Harmonic Distortion
            thd_original = self._calculate_thd(original, sample_rate)
            thd_restored = self._calculate_thd(restored, sample_rate)
            metrics['thd_improvement'] = thd_original - thd_restored
            
            # Spectral flatness (measure of noise-like vs tonal content)
            sf_original = self._calculate_spectral_flatness(original)
            sf_restored = self._calculate_spectral_flatness(restored)
            metrics['spectral_flatness_improvement'] = sf_restored - sf_original
            
            # Dynamic range
            dr_original = self._calculate_dynamic_range(original)
            dr_restored = self._calculate_dynamic_range(restored)
            metrics['dynamic_range_improvement'] = dr_restored - dr_original
            
            # Overall quality score (weighted combination)
            metrics['overall_quality_score'] = self._calculate_overall_quality_score(metrics)
            
        except Exception as e:
            self.logger.warning(f"Failed to calculate some improvement metrics: {e}")
        
        return metrics
    
    def _calculate_snr(self, signal_data: np.ndarray) -> float:
        """Calculate Signal-to-Noise Ratio in dB."""
        signal_power = np.mean(signal_data ** 2)
        
        # Estimate noise from quieter sections
        noise_estimate = np.percentile(np.abs(signal_data), 10)
        noise_power = noise_estimate ** 2
        
        if noise_power > 0:
            snr_linear = signal_power / noise_power
            return 10 * np.log10(snr_linear)
        
        return float('inf')
    
    def _calculate_thd(self, signal_data: np.ndarray, sample_rate: int) -> float:
        """Calculate Total Harmonic Distortion."""
        # Simplified THD calculation using spectral analysis
        fft_data = np.fft.fft(signal_data)
        magnitude = np.abs(fft_data[:len(fft_data)//2])
        
        # Find fundamental frequency
        fundamental_idx = np.argmax(magnitude[1:]) + 1
        fundamental_mag = magnitude[fundamental_idx]
        
        # Calculate harmonic content
        harmonic_energy = 0
        for h in range(2, 6):  # 2nd to 5th harmonics
            harmonic_idx = fundamental_idx * h
            if harmonic_idx < len(magnitude):
                harmonic_energy += magnitude[harmonic_idx] ** 2
        
        if fundamental_mag > 0:
            thd = np.sqrt(harmonic_energy) / fundamental_mag
            return thd
        
        return 0.0
    
    def _calculate_spectral_flatness(self, signal_data: np.ndarray) -> float:
        """Calculate spectral flatness (Wiener entropy)."""
        # Compute power spectrum
        _, psd = signal.welch(signal_data, nperseg=1024)
        psd = psd[psd > 0]  # Remove zeros for log calculation
        
        if len(psd) > 0:
            geometric_mean = np.exp(np.mean(np.log(psd)))
            arithmetic_mean = np.mean(psd)
            
            if arithmetic_mean > 0:
                return geometric_mean / arithmetic_mean
        
        return 0.0
    
    def _calculate_dynamic_range(self, signal_data: np.ndarray) -> float:
        """Calculate dynamic range in dB."""
        peak_level = np.max(np.abs(signal_data))
        rms_level = np.sqrt(np.mean(signal_data ** 2))
        
        if rms_level > 0:
            return 20 * np.log10(peak_level / rms_level)
        
        return 0.0
    
    def _calculate_overall_quality_score(self, metrics: Dict[str, float]) -> float:
        """
        Calculate weighted overall quality improvement score.
        
        Args:
            metrics: Dictionary of individual metrics
            
        Returns:
            Float: Overall quality score (0-100)
        """
        # Weights for different metrics
        weights = {
            'snr_improvement_db': 0.4,
            'thd_improvement': 0.2,
            'spectral_flatness_improvement': 0.2,
            'dynamic_range_improvement': 0.2
        }
        
        weighted_score = 0.0
        total_weight = 0.0
        
        for metric, weight in weights.items():
            if metric in metrics:
                # Normalize and clip metric values
                normalized_value = np.clip(metrics[metric] * 10, -50, 50)
                weighted_score += normalized_value * weight
                total_weight += weight
        
        if total_weight > 0:
            # Convert to 0-100 scale
            final_score = (weighted_score / total_weight + 50)
            return np.clip(final_score, 0, 100)
        
        return 50.0  # Neutral score if no metrics available