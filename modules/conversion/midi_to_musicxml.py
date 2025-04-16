#!/usr/bin/env python3
"""
MIDI to MusicXML Conversion Module

Provides functionality to convert MIDI files to MusicXML format for score editing and analysis.

Functions:
    midi_to_musicxml: Convert MIDI file to MusicXML format
"""
import os
from music21 import converter

def midi_to_musicxml(midi_file, output_musicxml=None):
    """
    Convert MIDI file to MusicXML format

    Args:
        midi_file (str): Path to input MIDI file
        output_musicxml (str, optional): Path to output MusicXML file
                                        If None, a default name will be used

    Returns:
        str: Path to the generated MusicXML file if successful, None otherwise
    """
    try:
        # Check if input file exists
        if not os.path.exists(midi_file):
            print(f"Error: Input file {midi_file} does not exist")
            return None
            
        # Set output MusicXML file path
        if output_musicxml is None:
            output_musicxml = os.path.splitext(midi_file)[0] + ".musicxml"

        # Ensure output directory exists
        output_dir = os.path.dirname(output_musicxml)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        # Load MIDI file
        print(f"Loading MIDI file: {midi_file}")
        score = converter.parse(midi_file)

        # Write to MusicXML file
        print(f"Converting to MusicXML: {output_musicxml}")
        score.write("musicxml", fp=output_musicxml)

        print(f"Created MusicXML file: {output_musicxml}")
        return output_musicxml
        
    except Exception as e:
        print(f"Error during conversion: {e}")
        return None


