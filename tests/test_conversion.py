import unittest
import os
import tempfile
import shutil
from modules.conversion.audio_to_midi import audio_to_midi
from modules.conversion.midi_to_musicxml import midi_to_musicxml
from modules.conversion.musicxml_to_midi import musicxml_to_midi
from modules.conversion.format_converter import convert_audio_format


class TestConversion(unittest.TestCase):
    """Audio and score format conversion module tests"""
    
    def setUp(self):
        """Set up test environment"""
        # Create temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        # Test audio, MIDI and MusicXML file paths
        self.test_audio = os.path.join(os.path.dirname(__file__), 'test_data', 'test_audio.wav')
        self.test_midi = os.path.join(os.path.dirname(__file__), 'test_data', 'test_midi.mid')
        self.test_musicxml = os.path.join(os.path.dirname(__file__), 'test_data', 'test_score.musicxml')
        
    def tearDown(self):
        """Clean up test environment"""
        # Remove temporary directory and its contents
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    @unittest.skipIf(not os.path.exists('tests/test_data/test_audio.wav'), 
                     "Test audio file does not exist")
    def test_audio_to_midi(self):
        """Test audio to MIDI conversion functionality"""
        output_file = os.path.join(self.test_dir, 'output.mid')
        
        try:
            result = audio_to_midi(self.test_audio, output_file)
            self.assertTrue(os.path.exists(output_file))
            self.assertEqual(result, output_file)
        except Exception as e:
            self.fail(f"Audio to MIDI conversion test failed: {e}")
    
    @unittest.skipIf(not os.path.exists('tests/test_data/test_midi.mid'), 
                     "Test MIDI file does not exist")
    def test_midi_to_musicxml(self):
        """Test MIDI to MusicXML conversion functionality"""
        output_file = os.path.join(self.test_dir, 'output.musicxml')
        
        try:
            result = midi_to_musicxml(self.test_midi, output_file)
            self.assertTrue(os.path.exists(output_file))
            self.assertEqual(result, output_file)
        except Exception as e:
            self.fail(f"MIDI to MusicXML conversion test failed: {e}")
    
    @unittest.skipIf(not os.path.exists('tests/test_data/test_score.musicxml'), 
                     "Test MusicXML file does not exist")
    def test_musicxml_to_midi(self):
        """Test MusicXML to MIDI conversion functionality"""
        output_file = os.path.join(self.test_dir, 'output.mid')
        
        try:
            result = musicxml_to_midi(self.test_musicxml, output_file)
            self.assertTrue(os.path.exists(output_file))
            self.assertEqual(result, output_file)
        except Exception as e:
            self.fail(f"MusicXML to MIDI conversion test failed: {e}")
    
    @unittest.skipIf(not os.path.exists('tests/test_data/test_audio.wav'), 
                     "Test audio file does not exist")
    def test_format_conversion(self):
        """Test audio format conversion functionality"""
        formats_to_test = ['mp3', 'ogg', 'flac', 'wav']
        
        for fmt in formats_to_test:
            with self.subTest(format=fmt):
                output_file = os.path.join(self.test_dir, f'output.{fmt}')
                
                try:
                    result = convert_audio_format(self.test_audio, fmt, output_file)
                    self.assertTrue(os.path.exists(output_file))
                    self.assertEqual(result, output_file)
                except Exception as e:
                    self.fail(f"Audio format conversion to {fmt} test failed: {e}")


if __name__ == '__main__':
    # Ensure test data directory exists
    test_data_dir = os.path.join(os.path.dirname(__file__), 'test_data')
    os.makedirs(test_data_dir, exist_ok=True)
    
    unittest.main()
