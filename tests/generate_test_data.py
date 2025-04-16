#!/usr/bin/env python3
"""
Test Data Generation Script

This script generates test audio, MIDI, and MusicXML files for unit testing.
"""
import os
import numpy as np
import soundfile as sf
import pretty_midi
from music21 import stream, note, metadata

def generate_test_audio():
    """Generate test audio file"""
    print("Generating test audio file...")
    # Create a simple sine wave audio
    sample_rate = 44100
    duration = 2.0  # seconds
    # Create a simple chord (C major triad)
    freqs = [261.63, 329.63, 392.00]  # C4, E4, G4
    
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    audio_data = np.zeros_like(t)
    
    # Add multiple frequencies to create a chord
    for freq in freqs:
        audio_data += 0.2 * np.sin(2 * np.pi * freq * t)
    
    # Add decay envelope
    envelope = np.exp(-t / duration)
    audio_data = audio_data * envelope
    
    # Ensure amplitude is within [-1, 1] range
    audio_data = audio_data / np.max(np.abs(audio_data))
    
    # Output path
    output_dir = os.path.join(os.path.dirname(__file__), 'test_data')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'test_audio.wav')
    
    # Save as WAV file
    sf.write(output_path, audio_data, sample_rate)
    print(f"Generated test audio file saved at: {output_path}")
    return output_path

def generate_test_midi():
    """Generate test MIDI file"""
    print("Generating test MIDI file...")
    # Create a new PrettyMIDI object
    midi = pretty_midi.PrettyMIDI()
    
    # Create an instrument program (piano)
    piano_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')
    piano = pretty_midi.Instrument(program=piano_program)
    
    # Create a simple melody
    note_names = ['C4', 'E4', 'G4', 'C5', 'G4', 'E4', 'C4']
    note_durations = [0.5, 0.5, 0.5, 1.0, 0.5, 0.5, 1.0]
    
    # Add notes
    start_time = 0.0
    for name, duration in zip(note_names, note_durations):
        # Get MIDI pitch
        note_number = pretty_midi.note_name_to_number(name)
        
        # Create note (start time, end time, pitch, and velocity)
        note = pretty_midi.Note(
            velocity=100, 
            pitch=note_number, 
            start=start_time, 
            end=start_time + duration
        )
        
        # Add note to instrument
        piano.notes.append(note)
        
        # Update start time
        start_time += duration
    
    # Add instrument to MIDI
    midi.instruments.append(piano)
    
    # Output path
    output_dir = os.path.join(os.path.dirname(__file__), 'test_data')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'test_midi.mid')
    
    # Save MIDI file
    midi.write(output_path)
    print(f"Generated test MIDI file saved at: {output_path}")
    return output_path

def generate_test_musicxml():
    """Generate test MusicXML file"""
    print("Generating test MusicXML file...")
    # Create a new music stream
    s = stream.Stream()
    
    # Set metadata
    s.metadata = metadata.Metadata()
    s.metadata.title = 'Test Score'
    s.metadata.composer = 'Test Generator'
    
    # Add notes
    note_names = ['C4', 'E4', 'G4', 'C5', 'G4', 'E4', 'C4']
    note_durations = [0.5, 0.5, 0.5, 1.0, 0.5, 0.5, 1.0]
    
    for name, duration in zip(note_names, note_durations):
        n = note.Note(name)
        n.quarterLength = duration  # Set duration
        s.append(n)
    
    # Output path
    output_dir = os.path.join(os.path.dirname(__file__), 'test_data')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'test_score.musicxml')
    
    # Save MusicXML file
    s.write('musicxml', fp=output_path)
    print(f"Generated test MusicXML file saved at: {output_path}")
    return output_path

def main():
    """Main function"""
    # Create test data directory
    test_data_dir = os.path.join(os.path.dirname(__file__), 'test_data')
    os.makedirs(test_data_dir, exist_ok=True)
    
    # Generate test data
    generate_test_audio()
    generate_test_midi()
    generate_test_musicxml()
    
    print("All test data generation complete!")

if __name__ == '__main__':
    main() 