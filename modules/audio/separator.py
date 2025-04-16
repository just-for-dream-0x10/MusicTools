#!/usr/bin/env python3
"""
Audio Separation Module

Provides audio separation functionality that can split mixed audio into vocals, drums, bass, and other instruments.

Functions:
    separate_audio: Separate audio file into different tracks
"""
import os
import subprocess
import warnings

def separate_audio(input_file, output_dir=None):
    """
    Use demucs to separate audio into vocals, drums, bass, and other instruments

    Args:
        input_file (str): Path to input audio file
        output_dir (str, optional): Path to output directory
                                   If None, will use default output directory

    Returns:
        dict: Dictionary containing paths to separated tracks, or None if failed
    """
    try:
        # Check if input file exists
        if not os.path.exists(input_file):
            print(f"Error: Input file {input_file} does not exist")
            return None
            
        # Set output directory
        if output_dir is None:
            output_dir = os.path.join(os.path.dirname(input_file), "separated")
            
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Get base filename
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        
        print(f"Separating audio: {input_file}")
        print(f"Output directory: {output_dir}")

        # Build command, use demucs for audio separation
        cmd = ["demucs", "--out", output_dir, input_file]
        
        # Execute command
        subprocess.run(cmd, check=True, capture_output=True, text=True)

        # Check output files
        expected_subdir = os.path.join(output_dir, "htdemucs", base_name)
        
        if os.path.exists(expected_subdir):
            # Extract paths to separated tracks
            tracks = {}
            for track in ["vocals", "drums", "bass", "other"]:
                track_path = os.path.join(expected_subdir, f"{track}.wav")
                if os.path.exists(track_path):
                    tracks[track] = track_path
            
            if tracks:
                print(f"Audio separation successful, created the following tracks:")
                for track, path in tracks.items():
                    print(f"- {track}: {path}")
                return tracks
        
        print("Audio separation failed, could not find expected output files")
        return None
        
    except subprocess.CalledProcessError as e:
        print(f"Error running demucs: {e}")
        return None
        
    except Exception as e:
        print(f"Error during audio separation: {e}")
        return None


# if __name__ == "__main__":
#     import argparse
    
#     parser = argparse.ArgumentParser(description='Audio Separation')
#     parser.add_argument('input_file', help='Path to input audio file')
#     parser.add_argument('-o', '--output-dir', help='Output directory')
    
#     args = parser.parse_args()
#     separate_audio(args.input_file, args.output_dir) 