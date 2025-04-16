#!/usr/bin/env python3
"""
MusicXML Analyzer Module

Provides MusicXML file analysis and instrument changing functionality.

Functions:
    analyze_musicxml: Analyze MusicXML file and output statistics
    change_instrument: Change instrument in a MusicXML file
"""
import os
from music21 import converter, analysis, instrument, pitch

def analyze_musicxml(input_file):
    """
    Analyze MusicXML file, providing key, note statistics, and other information

    Args:
        input_file (str): Path to input MusicXML file

    Returns:
        bool: True if analysis is successful, False otherwise
    """
    # Ensure input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} does not exist")
        return False

    try:
        # Load MusicXML file
        print(f"Loading MusicXML file: {input_file}")
        score = converter.parse(input_file)

        # Basic information
        print("\nBasic Information:")
        title = score.metadata.title if score.metadata and score.metadata.title else 'Unknown'
        composer = score.metadata.composer if score.metadata and score.metadata.composer else 'Unknown'
        print(f"Title: {title}")
        print(f"Composer: {composer}")
        
        # Extract and print instrument information
        instruments = []
        for p in score.parts:
            if p.partName:
                instruments.append(p.partName)
            else:
                instruments.append('Unnamed Instrument')
        
        print(f"Instruments: {', '.join(instruments)}")

        # Key analysis
        print("\nKey Analysis:")
        try:
            key = score.analyze("key")
            print(f"Estimated key: {key}")
        except Exception as e:
            print(f"Key analysis failed: {e}")

        # Note statistics
        print("\nNote Statistics:")
        notes = score.flat.notes
        print(f"Total notes: {len(notes)}")

        # Pitch distribution
        print("\nPitch Distribution:")
        pitch_count = {}
        for note in notes:
            if hasattr(note, 'isChord') and note.isChord:
                for p in note.pitches:
                    name = p.nameWithOctave
                    pitch_count[name] = pitch_count.get(name, 0) + 1
            elif hasattr(note, 'pitch'):
                name = note.pitch.nameWithOctave
                pitch_count[name] = pitch_count.get(name, 0) + 1

        # Sort by occurrence count
        sorted_pitches = sorted(pitch_count.items(), key=lambda x: x[1], reverse=True)
        for pitch, count in sorted_pitches[:10]:  # Show only top 10
            print(f"{pitch}: {count} occurrences")

        # Rhythm analysis
        print("\nRhythm Analysis:")
        durations = {}
        for note in notes:
            if hasattr(note, 'duration') and hasattr(note.duration, 'quarterLength'):
                dur = note.duration.quarterLength
                durations[dur] = durations.get(dur, 0) + 1

        # Sort by occurrence count
        sorted_durations = sorted(durations.items(), key=lambda x: x[1], reverse=True)
        for dur, count in sorted_durations:
            print(f"Duration {dur}: {count} occurrences")

        return True

    except Exception as e:
        print(f"Error during analysis: {e}")
        return False


def change_instrument(input_file, instrument_name, output_file=None):
    """
    Change instrument in MusicXML file

    Args:
        input_file (str): Path to input MusicXML file
        instrument_name (str): New instrument name (e.g., 'Piano', 'Violin', 'Flute')
        output_file (str, optional): Path to output MusicXML file
                                    If None, will be generated based on input filename

    Returns:
        str: Path to output file if successful, None otherwise
    """
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} does not exist")
        return None

    try:
        # If output file path is not provided, generate default path
        if not output_file:
            base_name, ext = os.path.splitext(input_file)
            output_file = f"{base_name}_{instrument_name}{ext}"
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            
        # Load file
        print(f"Loading file: {input_file}")
        score = converter.parse(input_file)
        
        # Create instrument object based on name
        instrument_obj = None
        
        # Try to directly get instrument class using name
        try:
            # Dynamically get instrument class
            instrument_class = getattr(instrument, instrument_name)
            instrument_obj = instrument_class()
        except (AttributeError, TypeError):
            # If failed, try to find common instruments
            lowercase_name = instrument_name.lower()
            instrument_map = {
                'piano': instrument.Piano(),
                'violin': instrument.Violin(),
                'viola': instrument.Viola(),
                'cello': instrument.Violoncello(),
                'bass': instrument.ElectricBass(),
                'guitar': instrument.Guitar(),
                'flute': instrument.Flute(),
                'clarinet': instrument.Clarinet(),
                'oboe': instrument.Oboe(),
                'trumpet': instrument.Trumpet(),
                'horn': instrument.Horn(),
                'trombone': instrument.Trombone(),
                'drums': instrument.UnpitchedPercussion(),
                'percussion': instrument.UnpitchedPercussion(),
                'voice': instrument.Vocalist(),
                'vocal': instrument.Vocalist(),
                'organ': instrument.PipeOrgan(),
                'saxophone': instrument.Saxophone()
            }
            
            if lowercase_name in instrument_map:
                instrument_obj = instrument_map[lowercase_name]
            else:
                # Default to piano
                print(f"Instrument '{instrument_name}' not found, using piano as default.")
                instrument_obj = instrument.Piano()
        
        # Apply to all parts
        for part in score.parts:
            # Replace existing instrument objects
            for elem in part.recurse().getElementsByClass('Instrument'):
                part.remove(elem)
                    
            # Insert new instrument at beginning
            part.insert(0, instrument_obj)
            
            # Update part name
            part.partName = instrument_name

        # Save to output file
        print(f"Saving file with {instrument_name} to: {output_file}")
        score.write('musicxml', fp=output_file)
        
        return output_file
        
    except Exception as e:
        print(f"Error changing instrument: {e}")
        return None


# if __name__ == "__main__":
#     import argparse
    
#     parser = argparse.ArgumentParser(description='MusicXML Analysis and Processing')
#     subparsers = parser.add_subparsers(dest='command', help='Commands')
    
#     # Analyze command
#     analyze_parser = subparsers.add_parser('analyze', help='Analyze MusicXML file')
#     analyze_parser.add_argument('input_file', help='Path to input MusicXML file')
    
#     # Change instrument command
#     change_parser = subparsers.add_parser('change-instrument', help='Change instrument in MusicXML file')
#     change_parser.add_argument('input_file', help='Path to input file')
#     change_parser.add_argument('instrument', help='New instrument name')
#     change_parser.add_argument('-o', '--output', help='Path to output file')
    
#     args = parser.parse_args()
    
#     if args.command == 'analyze':
#         analyze_musicxml(args.input_file)
#     elif args.command == 'change-instrument':
#         change_instrument(args.input_file, args.instrument, args.output)
#     else:
#         parser.print_help() 