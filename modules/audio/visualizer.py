#!/usr/bin/env python3
"""
Advanced Audio Visualization Module

Provides comprehensive visualization functionality for audio files, generating multiple analysis plots
including waveform, spectrogram, mel spectrogram, chromagram, MFCC, onset detection, 
spectral centroid, key analysis, and rhythm analysis.

Functions:
    visualize_audio: Generate comprehensive visualization images for audio files
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib import cm  # Import colormap module
import librosa
import librosa.display
import scipy
from scipy.signal import find_peaks

def visualize_audio(audio_file, output_file=None):
    """
    Generate comprehensive visualization images for an audio file

    Args:
        audio_file (str): Path to input audio file
        output_file (str, optional): Path to output image file
                                    If None, will be generated based on input filename

    Returns:
        str: Path to the generated image file if successful, None otherwise
    """
    try:
        # Check if input file exists
        if not os.path.exists(audio_file):
            print(f"Error: Audio file {audio_file} does not exist")
            return None
            
        # Set output file path
        if output_file is None:
            output_file = f"{os.path.splitext(audio_file)[0]}_visualization.png"
            
        # Ensure output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            
        # Load audio file
        print(f"Loading audio file: {audio_file}")
        y, sr = librosa.load(audio_file, sr=None)
        duration = librosa.get_duration(y=y, sr=sr)
        
        # Set the style for better aesthetics
        plt.style.use('dark_background')
        
        # Create a figure with grid layout for multiple plots
        plt.figure(figsize=(18, 24))
        gs = GridSpec(5, 3, figure=plt.gcf())
        
        # Time array for various plots
        times = np.linspace(0, duration, len(y))
        
        # 1. Waveform plot - Using a vibrant green color
        ax1 = plt.subplot(gs[0, 0])
        ax1.plot(times, y, color='#00FF7F', linewidth=1.0)  # Spring green color
        ax1.set_title('Waveform', color='white', fontsize=12)
        ax1.set_xlabel('Time (s)', color='white')
        ax1.set_ylabel('Amplitude', color='white')
        ax1.set_xlim(0, duration)
        ax1.set_ylim(-1.0, 1.0)
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(colors='white')
        for spine in ax1.spines.values():
            spine.set_color('#555555')
        
        # 2. Spectrogram - Using viridis colormap
        ax2 = plt.subplot(gs[0, 1])
        D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
        img = librosa.display.specshow(D, x_axis='time', y_axis='hz', sr=sr, ax=ax2, cmap=cm.viridis)
        plt.colorbar(img, ax=ax2, format='%+2.0f dB')
        ax2.set_title('Spectrogram', color='white', fontsize=12)
        ax2.tick_params(colors='white')
        for spine in ax2.spines.values():
            spine.set_color('#555555')
        
        # 3. Mel Spectrogram - Using plasma colormap
        ax3 = plt.subplot(gs[0, 2])
        mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
        img = librosa.display.specshow(mel_spec_db, x_axis='time', y_axis='mel', sr=sr, ax=ax3, cmap=cm.plasma)
        plt.colorbar(img, ax=ax3, format='%+2.0f dB')
        ax3.set_title('Mel Spectrogram', color='white', fontsize=12)
        ax3.tick_params(colors='white')
        for spine in ax3.spines.values():
            spine.set_color('#555555')
        
        # 4. Chromagram - Using magma colormap
        ax4 = plt.subplot(gs[1, 0])
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        img = librosa.display.specshow(chroma, x_axis='time', y_axis='chroma', ax=ax4, cmap=cm.magma)
        plt.colorbar(img, ax=ax4)
        ax4.set_title('Chromagram', color='white', fontsize=12)
        ax4.tick_params(colors='white')
        for spine in ax4.spines.values():
            spine.set_color('#555555')
        
        # 5. MFCC - Using inferno colormap
        ax5 = plt.subplot(gs[1, 1])
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        img = librosa.display.specshow(mfccs, x_axis='time', ax=ax5, cmap=cm.inferno)
        plt.colorbar(img, ax=ax5)
        ax5.set_title('MFCC', color='white', fontsize=12)
        ax5.tick_params(colors='white')
        for spine in ax5.spines.values():
            spine.set_color('#555555')
        
        # 6. Onset Detection - Using orange for onset strength and red for onsets
        ax6 = plt.subplot(gs[1, 2])
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)
        onset_times = librosa.frames_to_time(onset_frames, sr=sr)
        
        # Use correct time axis for onset envelope
        onset_times_env = librosa.times_like(onset_env, sr=sr)
        ax6.plot(onset_times_env, librosa.util.normalize(onset_env), color='#FFA500', label='Onset Strength')  # Orange
        ax6.vlines(onset_times, 0, 1, color='#FF3333', alpha=0.9, linestyle='--', label='Onsets')  # Red
        ax6.set_title('Onset Detection', color='white', fontsize=12)
        ax6.set_xlabel('Time (s)', color='white')
        ax6.set_ylabel('Strength', color='white')
        ax6.legend(loc='upper right')
        ax6.tick_params(colors='white')
        for spine in ax6.spines.values():
            spine.set_color('#555555')
        
        # 7. Spectral Centroid - Using purple
        ax7 = plt.subplot(gs[2, 0])
        centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        # Get correct times for centroid
        centroid_times = librosa.times_like(centroid, sr=sr)
        ax7.semilogy(centroid_times, centroid, color='#9370DB', label='Spectral Centroid')  # Medium purple
        ax7.set_title('Spectral Centroid', color='white', fontsize=12)
        ax7.set_xlabel('Time (s)', color='white')
        ax7.set_ylabel('Hz', color='white')
        ax7.legend()
        ax7.tick_params(colors='white')
        for spine in ax7.spines.values():
            spine.set_color('#555555')
        
        # 8. Key Analysis - Using teal colors for bar chart
        ax8 = plt.subplot(gs[2, 1])
        # Use chroma features for key analysis
        pitches = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        
        # Calculate relative strength of each pitch class
        chroma_avg = np.mean(chroma, axis=1)
        chroma_norm = chroma_avg / np.sum(chroma_avg)
        
        # Create color gradient for bars - teal to cyan
        colors = plt.cm.turbo(np.linspace(0, 1, len(pitches)))
        
        # Plot as bar chart
        ax8.bar(pitches, chroma_norm, color=colors)
        ax8.set_title('Key Analysis', color='white', fontsize=12)
        ax8.set_xlabel('Pitch', color='white')
        ax8.set_ylabel('Relative Strength', color='white')
        ax8.tick_params(colors='white')
        for spine in ax8.spines.values():
            spine.set_color('#555555')
        
        # Try to estimate key using librosa
        try:
            # Use librosa's key detection (added in newer versions)
            key = librosa.key_to_notes(np.argmax(chroma_avg))
            ax8.set_title(f'Key Analysis (Est. Key: {key})', color='white', fontsize=12)
        except:
            # Try a simpler approach
            key_idx = np.argmax(chroma_avg)
            key = pitches[key_idx]
            ax8.set_title(f'Key Analysis (Est. Key: {key})', color='white', fontsize=12)
        
        # 9. Rhythm Analysis - Using green for onset strength and lime for beats
        ax9 = plt.subplot(gs[2, 2])
        # Calculate tempo and beat frames
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        
        # Use correct time axis for rhythm analysis
        ax9.plot(onset_times_env, librosa.util.normalize(onset_env), color='#00CED1', label='Onset Strength')  # Dark turquoise
        ax9.vlines(beat_times, 0, 1, color='#7FFF00', alpha=0.9, linestyle='--', label='Beats')  # Chartreuse
        ax9.set_title(f'Rhythm Analysis (Est. Tempo: {tempo:.0f} BPM)', color='white', fontsize=12)
        ax9.set_xlabel('Time (s)', color='white')
        ax9.set_ylabel('Normalized Strength', color='white')
        ax9.legend()
        ax9.tick_params(colors='white')
        for spine in ax9.spines.values():
            spine.set_color('#555555')
        
        # 10. Harmonic-Percussive Source Separation
        ax10 = plt.subplot(gs[3, 0])
        ax11 = plt.subplot(gs[3, 1])
        
        # Separate harmonic and percussive components
        harmonic, percussive = librosa.effects.hpss(y)
        
        # Plot harmonic part - Using cividis colormap
        D_harmonic = librosa.amplitude_to_db(np.abs(librosa.stft(harmonic)), ref=np.max)
        img = librosa.display.specshow(D_harmonic, x_axis='time', y_axis='log', sr=sr, ax=ax10, cmap=cm.cividis)
        ax10.set_title('Harmonic Component', color='white', fontsize=12)
        plt.colorbar(img, ax=ax10, format='%+2.0f dB')
        ax10.tick_params(colors='white')
        for spine in ax10.spines.values():
            spine.set_color('#555555')
        
        # Plot percussive part - Using cool colormap
        D_percussive = librosa.amplitude_to_db(np.abs(librosa.stft(percussive)), ref=np.max)
        img = librosa.display.specshow(D_percussive, x_axis='time', y_axis='log', sr=sr, ax=ax11, cmap=cm.cool)
        ax11.set_title('Percussive Component', color='white', fontsize=12)
        plt.colorbar(img, ax=ax11, format='%+2.0f dB')
        ax11.tick_params(colors='white')
        for spine in ax11.spines.values():
            spine.set_color('#555555')
        
        # 11. Spectral Bandwidth - Using pink
        ax12 = plt.subplot(gs[3, 2])
        spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
        # Correct time axis for spectral bandwidth
        times_spec_bw = librosa.times_like(spec_bw, sr=sr)
        ax12.plot(times_spec_bw, spec_bw, color='#FF69B4')  # Hot pink
        ax12.set_title('Spectral Bandwidth', color='white', fontsize=12)
        ax12.set_xlabel('Time (s)', color='white')
        ax12.set_ylabel('Bandwidth (Hz)', color='white')
        ax12.tick_params(colors='white')
        for spine in ax12.spines.values():
            spine.set_color('#555555')
        
        # 12. Spectral Contrast - Using rainbow colormap
        ax13 = plt.subplot(gs[4, 0])
        contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
        img = librosa.display.specshow(contrast, x_axis='time', ax=ax13, cmap=cm.rainbow)
        plt.colorbar(img, ax=ax13)
        ax13.set_title('Spectral Contrast', color='white', fontsize=12)
        ax13.tick_params(colors='white')
        for spine in ax13.spines.values():
            spine.set_color('#555555')
        
        # 13. Spectral Rolloff - Using gold
        ax14 = plt.subplot(gs[4, 1])
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
        # Correct time axis for rolloff
        times_rolloff = librosa.times_like(rolloff, sr=sr)
        ax14.plot(times_rolloff, rolloff, color='#FFD700')  # Gold
        ax14.set_title('Spectral Rolloff', color='white', fontsize=12)
        ax14.set_xlabel('Time (s)', color='white')
        ax14.set_ylabel('Frequency (Hz)', color='white')
        ax14.tick_params(colors='white')
        for spine in ax14.spines.values():
            spine.set_color('#555555')
        
        # 14. Zero Crossing Rate - Using coral
        ax15 = plt.subplot(gs[4, 2])
        zcr = librosa.feature.zero_crossing_rate(y)[0]
        # Correct time axis for ZCR
        times_zcr = librosa.times_like(zcr, sr=sr)
        ax15.plot(times_zcr, zcr, color='#FF7F50')  # Coral
        ax15.set_title('Zero Crossing Rate', color='white', fontsize=12)
        ax15.set_xlabel('Time (s)', color='white')
        ax15.set_ylabel('Rate', color='white')
        ax15.tick_params(colors='white')
        for spine in ax15.spines.values():
            spine.set_color('#555555')
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, facecolor='black')
        plt.close()
        
        print(f"Created comprehensive visualization image: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"Error generating visualization: {e}")
        import traceback
        traceback.print_exc()
        return None

