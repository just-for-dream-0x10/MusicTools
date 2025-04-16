#!/usr/bin/env python3
"""
MusicXML to MIDI Conversion Module

Provides functionality to convert MusicXML files to MIDI format for playback and performance.

Functions:
    musicxml_to_midi: Convert MusicXML file to MIDI format
"""
import os
from music21 import converter

def musicxml_to_midi(musicxml_file, output_midi=None):
    """
    Convert MusicXML file to MIDI format

    Args:
        musicxml_file (str): Path to input MusicXML file
        output_midi (str, optional): Path to output MIDI file
                                    If None, a default name will be used

    Returns:
        str: Path to the generated MIDI file if successful, None otherwise
    """
    try:
        # Check if input file exists
        if not os.path.exists(musicxml_file):
            print(f"Error: Input file {musicxml_file} does not exist")
            return None
            
        # Set output MIDI file path
        if output_midi is None:
            output_midi = os.path.splitext(musicxml_file)[0] + ".mid"

        # Ensure output directory exists
        output_dir = os.path.dirname(output_midi)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        # Load MusicXML file
        print(f"Loading MusicXML file: {musicxml_file}")
        score = converter.parse(musicxml_file)

        # Write to MIDI file
        print(f"Converting to MIDI: {output_midi}")
        score.write("midi", fp=output_midi)

        print(f"Created MIDI file: {output_midi}")
        return output_midi
        
    except Exception as e:
        print(f"Error during conversion: {e}")
        return None


# if __name__ == "__main__":
#     import argparse
    
#     parser = argparse.ArgumentParser(description='Convert MusicXML to MIDI')
#     parser.add_argument('musicxml_file', help='Path to input MusicXML file')
#     parser.add_argument('-o', '--output', help='Path to output MIDI file')
    
#     args = parser.parse_args()
#     musicxml_to_midi(args.musicxml_file, args.output) 