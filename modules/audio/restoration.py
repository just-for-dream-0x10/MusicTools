#!/usr/bin/env python3
"""
Audio Restoration Module

Provides audio restoration and enhancement functionality for processing low-quality recordings and old audio.

Functions:
    restore_audio: Restore and enhance audio
"""
import os
import numpy as np
import librosa
import soundfile as sf
from scipy import signal

def restore_audio(input_file, output_file=None, settings=None):
    """
    Restore and enhance audio file quality

    Args:
        input_file (str): Path to input audio file
        output_file (str, optional): Path to output audio file
                                   If None, will be generated based on input filename
        settings (dict, optional): Restoration settings parameters
            - noise_reduction (float): Noise reduction strength, 0.0-1.0
            - eq_low (float): Low frequency equalization gain, 0.0-2.0
            - eq_mid (float): Mid frequency equalization gain, 0.0-2.0
            - eq_high (float): High frequency equalization gain, 0.0-2.0

    Returns:
        str: Path to the restored audio file if successful, None otherwise
    """
    try:
        # Check if input file exists
        if not os.path.exists(input_file):
            print(f"Error: Input file {input_file} does not exist")
            return None
            
        # Set output file path
        if output_file is None:
            output_file = f"{os.path.splitext(input_file)[0]}_restored.wav"
            
        # Ensure output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # Default settings
        default_settings = {
            'noise_reduction': 0.2,  # Noise reduction strength
            'eq_low': 1.2,           # Low frequency gain
            'eq_mid': 1.0,           # Mid frequency gain
            'eq_high': 1.1           # High frequency gain
        }
        
        # Merge user settings
        if settings is None:
            settings = {}
        
        for key in default_settings:
            if key not in settings:
                settings[key] = default_settings[key]
                
        print(f"Restoring audio: {input_file}")
        print(f"Settings: {settings}")
        
        # Load audio
        y, sr = librosa.load(input_file, sr=None)
        
        # Noise reduction (simple spectral subtraction)
        if settings['noise_reduction'] > 0:
            # Estimate noise spectrum
            S = np.abs(librosa.stft(y))
            noise_spectrum = np.mean(S[:, :int(S.shape[1] * 0.1)], axis=1).reshape(-1, 1)
            
            # Spectral subtraction
            gain = 1 - settings['noise_reduction']
            S_reduced = S - noise_spectrum * gain
            S_reduced = np.maximum(S_reduced, 0.0)
            
            # Inverse transform
            y = librosa.istft(S_reduced * np.exp(1j * np.angle(librosa.stft(y))))
        
        # Equalizer (using 3-band EQ)
        low_processed = False
        mid_processed = False
        high_processed = False
        processed_audio = np.zeros_like(y)
        
        # Define three frequency bands
        nyq = sr / 2
        low_cutoff = 300 / nyq
        mid_cutoff = 3000 / nyq
        
        # Low frequency processing
        if settings['eq_low'] != 1.0:
            b, a = signal.butter(2, low_cutoff, btype='lowpass')
            low = signal.filtfilt(b, a, y) * settings['eq_low']
            processed_audio += low
            low_processed = True
            
        # Mid frequency processing
        if settings['eq_mid'] != 1.0:
            b1, a1 = signal.butter(2, low_cutoff, btype='highpass')
            b2, a2 = signal.butter(2, mid_cutoff, btype='lowpass')
            mid_temp = signal.filtfilt(b1, a1, y)
            mid = signal.filtfilt(b2, a2, mid_temp) * settings['eq_mid']
            processed_audio += mid
            mid_processed = True
            
        # High frequency processing
        if settings['eq_high'] != 1.0:
            b, a = signal.butter(2, mid_cutoff, btype='highpass')
            high = signal.filtfilt(b, a, y) * settings['eq_high']
            processed_audio += high
            high_processed = True
        
        # Apply EQ only if any band has been processed
        if low_processed or mid_processed or high_processed:
            y = processed_audio
            # Normalize
            if np.max(np.abs(y)) > 0:  # Avoid division by zero
                y = y / np.max(np.abs(y))
        
        # Write output file
        sf.write(output_file, y, sr)
        
        print(f"Created restored audio file: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"Error during audio restoration: {e}")
        return None


# if __name__ == "__main__":
#     import argparse
    
#     parser = argparse.ArgumentParser(description='Audio Restoration and Enhancement')
#     parser.add_argument('input_file', help='Path to input audio file')
#     parser.add_argument('-o', '--output', help='Path to output audio file')
#     parser.add_argument('--noise-reduction', type=float, default=0.2, help='Noise reduction strength (0.0-1.0)')
#     parser.add_argument('--eq-low', type=float, default=1.2, help='Low frequency gain (0.0-2.0)')
#     parser.add_argument('--eq-mid', type=float, default=1.0, help='Mid frequency gain (0.0-2.0)')
#     parser.add_argument('--eq-high', type=float, default=1.1, help='High frequency gain (0.0-2.0)')
    
#     args = parser.parse_args()
    
#     settings = {
#         'noise_reduction': args.noise_reduction,
#         'eq_low': args.eq_low,
#         'eq_mid': args.eq_mid,
#         'eq_high': args.eq_high
#     }
    
#     restore_audio(args.input_file, args.output, settings)