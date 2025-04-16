#!/usr/bin/env python3
"""
Audio to MIDI Conversion Module

Provides functionality to convert audio files to MIDI format using machine learning models for note detection.

Functions:
    audio_to_midi: Convert audio file to MIDI format
"""
import os
import subprocess
import shutil
import glob

def audio_to_midi(audio_file, output_midi=None):
    """
    Convert audio file to MIDI format

    Args:
        audio_file (str): Path to input audio file
        output_midi (str, optional): Path to output MIDI file
                                    If None, a default name will be used

    Returns:
        str: Path to the generated MIDI file if successful, None otherwise
    """
    try:
        # Check if input file exists
        if not os.path.exists(audio_file):
            print(f"Error: Input file {audio_file} does not exist")
            return None
            
        # Set output MIDI file path
        if output_midi is None:
            output_midi = os.path.splitext(audio_file)[0] + ".mid"

        # Ensure output directory exists
        output_dir = os.path.dirname(output_midi)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        # Use command line tool for conversion
        print(f"Analyzing audio file: {audio_file}")
        
        # Use basic-pitch command line tool for conversion
        temp_dir = os.path.dirname(output_midi) or "."
        cmd = ["basic-pitch", "--save-midi", temp_dir, audio_file]
        
        # Run command
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        # Find generated MIDI file
        base_name = os.path.splitext(os.path.basename(audio_file))[0]
        expected_midi = os.path.join(temp_dir, f"{base_name}_basic_pitch.mid")
        
        if os.path.exists(expected_midi):
            # Copy file if output path is different
            if expected_midi != output_midi:
                shutil.copy2(expected_midi, output_midi)
                
            print(f"Successfully created MIDI file: {output_midi}")
            return output_midi
            
        # If expected MIDI file not found, look for any generated MIDI files
        midi_files = glob.glob(os.path.join(temp_dir, "*.mid"))
        if midi_files:
            # Copy the first MIDI file found
            if midi_files[0] != output_midi:
                shutil.copy2(midi_files[0], output_midi)
                
            print(f"Successfully created MIDI file: {output_midi}")
            return output_midi
            
        print("Could not find generated MIDI file")
        return None
        
    except subprocess.CalledProcessError as e:
        print(f"Error running basic-pitch: {e}")
        return None
    except Exception as e:
        print(f"Error during conversion: {e}")
        return None


