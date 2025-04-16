#!/usr/bin/env python3
"""
MusicAITools - Integrated Command Line Interface

This script provides a unified command-line interface that integrates various audio and score processing functionalities.
Including format conversion, analysis, restoration, separation, and visualization.

Usage:
    python main.py <command> [options]
    
Run 'python main.py -h' for help information.
"""
import argparse
import os
import sys
import warnings

# Import project modules
from modules.conversion.audio_to_midi import audio_to_midi
from modules.conversion.midi_to_musicxml import midi_to_musicxml
from modules.conversion.musicxml_to_midi import musicxml_to_midi
from modules.conversion.format_converter import convert_audio_format
from modules.analysis.musicxml_analyzer import analyze_musicxml, change_instrument
from modules.audio.visualizer import visualize_audio
from modules.audio.separator import separate_audio
from modules.audio.restoration import restore_audio
from modules.utils.helpers import ensure_dir, get_file_info, find_files

# Suppress unnecessary warnings
warnings.filterwarnings("ignore", category=UserWarning)


def main():
    # Create command line parser
    parser = argparse.ArgumentParser(description='Music AI Processing Toolkit')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # 1. Audio to MIDI
    audio_to_midi_parser = subparsers.add_parser('audio-to-midi', help='Convert audio to MIDI')
    audio_to_midi_parser.add_argument('audio_file', help='Input audio file')
    audio_to_midi_parser.add_argument('-o', '--output', help='Output MIDI file')

    # 2. MIDI and MusicXML conversion
    midi_to_xml_parser = subparsers.add_parser('midi-to-xml', help='Convert MIDI to MusicXML')
    midi_to_xml_parser.add_argument('midi_file', help='Input MIDI file')
    midi_to_xml_parser.add_argument('-o', '--output', help='Output MusicXML file')

    xml_to_midi_parser = subparsers.add_parser('xml-to-midi', help='Convert MusicXML to MIDI')
    xml_to_midi_parser.add_argument('musicxml_file', help='Input MusicXML file')
    xml_to_midi_parser.add_argument('-o', '--output', help='Output MIDI file')

    # 3. MusicXML analysis and instrument change
    analyze_parser = subparsers.add_parser('analyze', help='Analyze MusicXML file')
    analyze_parser.add_argument('input_file', help='Input MusicXML file')

    change_parser = subparsers.add_parser('change-instrument', help='Change MusicXML instrument')
    change_parser.add_argument('input_file', help='Input file')
    change_parser.add_argument('instrument', help='New instrument name')
    change_parser.add_argument('-o', '--output', help='Output file')

    # 4. Audio separation and visualization
    separate_parser = subparsers.add_parser('separate', help='Audio separation')
    separate_parser.add_argument('input_file', help='Input audio file')
    separate_parser.add_argument('--output-dir', '-o', help='Output directory')

    visualize_parser = subparsers.add_parser('visualize', help='Audio visualization')
    visualize_parser.add_argument('audio_file', help='Input audio file')
    visualize_parser.add_argument('--output-file', '-o', help='Output image file')

    # 5. Audio restoration
    restore_parser = subparsers.add_parser('restore', help='Audio restoration and enhancement')
    restore_parser.add_argument('input_file', help='Input audio file')
    restore_parser.add_argument('--output-file', '-o', help='Output audio file')
    restore_parser.add_argument('--noise-reduction', type=float, default=0.2, help='Noise reduction strength (0.0-1.0)')
    restore_parser.add_argument('--eq-low', type=float, default=1.2, help='Low frequency gain (0.0-2.0)')
    restore_parser.add_argument('--eq-mid', type=float, default=1.0, help='Mid frequency gain (0.0-2.0)')
    restore_parser.add_argument('--eq-high', type=float, default=1.1, help='High frequency gain (0.0-2.0)')

    # 6. Audio format conversion
    convert_parser = subparsers.add_parser('convert-format', help='Audio format conversion')
    convert_parser.add_argument('input_file', help='Input audio file')
    convert_parser.add_argument('-f', '--output-format', required=True, choices=['wav', 'mp3', 'ogg', 'flac'], help='Output format')
    convert_parser.add_argument('-o', '--output-file', help='Output file')

    # Parse command line arguments
    args = parser.parse_args()

    # Execute the appropriate functionality based on command
    if args.command == 'audio-to-midi':
        audio_to_midi(args.audio_file, args.output)
        
    elif args.command == 'midi-to-xml':
        midi_to_musicxml(args.midi_file, args.output)
        
    elif args.command == 'xml-to-midi':
        musicxml_to_midi(args.musicxml_file, args.output)
        
    elif args.command == 'analyze':
        analyze_musicxml(args.input_file)
        
    elif args.command == 'change-instrument':
        change_instrument(args.input_file, args.instrument, args.output)
        
    elif args.command == 'separate':
        separate_audio(args.input_file, args.output_dir)
        
    elif args.command == 'visualize':
        visualize_audio(args.audio_file, args.output_file)
        
    elif args.command == 'restore':
        settings = {
            'noise_reduction': args.noise_reduction,
            'eq_low': args.eq_low,
            'eq_mid': args.eq_mid,
            'eq_high': args.eq_high
        }
        restore_audio(args.input_file, args.output_file, settings)
        
    elif args.command == 'convert-format':
        convert_audio_format(args.input_file, args.output_format, args.output_file)
        
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
