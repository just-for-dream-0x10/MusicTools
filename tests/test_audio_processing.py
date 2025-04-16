import unittest
import os
import tempfile
import shutil
from modules.audio.restoration import restore_audio
from modules.audio.separator import separate_audio
from modules.audio.visualizer import visualize_audio

class TestAudioProcessing(unittest.TestCase):
    """Audio processing module tests"""
    
    def setUp(self):
        """Set up test environment"""
        # Create temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        # Test audio file path, in actual testing a valid test audio would be provided
        self.test_audio = os.path.join(os.path.dirname(__file__), 'test_data', 'test_audio.wav')
        
    def tearDown(self):
        """Clean up test environment"""
        # Remove temporary directory and its contents
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    @unittest.skipIf(not os.path.exists('tests/test_data/test_audio.wav'), 
                     "Test audio file does not exist")
    def test_restoration(self):
        """Test audio restoration functionality"""
        output_file = os.path.join(self.test_dir, 'restored.wav')
        settings = {
            'noise_reduction': 0.2,
            'eq_low': 1.2,
            'eq_mid': 1.0,
            'eq_high': 1.1
        }
        
        # In actual testing, a valid test audio file is needed
        try:
            restore_audio(self.test_audio, output_file, settings)
            self.assertTrue(os.path.exists(output_file))
            # More tests could be added, such as checking file size, audio quality, etc.
        except Exception as e:
            self.fail(f"Audio restoration test failed: {e}")
    
    @unittest.skipIf(not os.path.exists('tests/test_data/test_audio.wav'), 
                     "Test audio file does not exist")
    def test_separation(self):
        """Test audio separation functionality"""
        output_dir = os.path.join(self.test_dir, 'separated')
        
        try:
            result = separate_audio(self.test_audio, output_dir)
            if result:
                # Check if separated tracks were created
                for track_name, track_path in result.items():
                    self.assertTrue(os.path.exists(track_path))
            else:
                self.fail("Audio separation failed, no tracks returned")
        except Exception as e:
            self.fail(f"Audio separation test failed: {e}")
    
    @unittest.skipIf(not os.path.exists('tests/test_data/test_audio.wav'), 
                     "Test audio file does not exist")
    def test_visualization(self):
        """Test audio visualization functionality"""
        output_file = os.path.join(self.test_dir, 'visualization.png')
        
        try:
            visualize_audio(self.test_audio, output_file)
            self.assertTrue(os.path.exists(output_file))
            # More tests could be added, such as checking image dimensions, etc.
        except Exception as e:
            self.fail(f"Audio visualization test failed: {e}")


if __name__ == '__main__':
    # Ensure test data directory exists
    test_data_dir = os.path.join(os.path.dirname(__file__), 'test_data')
    os.makedirs(test_data_dir, exist_ok=True)
    
    unittest.main()
