#!/usr/bin/env python3
"""
Audio Format Conversion Module

Provides functionality to convert between various audio formats (WAV, MP3, OGG, FLAC, etc.).

Functions:
    convert_audio_format: Convert audio file to specified format
"""
import os
from pydub import AudioSegment

def convert_audio_format(input_file, output_format=None, output_file=None):
    """
    Convert audio file to specified format

    Args:
        input_file (str): Path to input audio file
        output_format (str, optional): Output format (wav, mp3, ogg, flac)
                                     If None and output_file has extension, will extract from output_file
        output_file (str, optional): Path to output file
                                   If None, will be generated based on input filename

    Returns:
        str: Path to the generated audio file if successful, None otherwise
    """
    try:
        # Check if input file exists
        if not os.path.exists(input_file):
            print(f"Error: Input file {input_file} does not exist")
            return None
            
        # Determine output format
        if output_format is None:
            if output_file is None:
                print("Error: Must specify either output_format or output_file parameter")
                return None
            output_format = os.path.splitext(output_file)[1].lower().lstrip('.')
        
        # Set output file path
        if output_file is None:
            output_file = f"{os.path.splitext(input_file)[0]}.{output_format}"
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # Use pydub for conversion
        print(f"Converting {input_file} to {output_format} format")
        audio = AudioSegment.from_file(input_file)
        
        # Export to specified format
        audio.export(output_file, format=output_format)
        
        print(f"Created audio file: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"Error during conversion: {e}")
        return None


