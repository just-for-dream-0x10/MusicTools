import unittest
import os
import tempfile
import shutil
from modules.analysis.musicxml_analyzer import analyze_musicxml, change_instrument

class TestAnalysis(unittest.TestCase):
    """Music analysis module tests"""
    
    def setUp(self):
        """Set up test environment"""
        # Create temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        # Test MusicXML file path
        self.test_musicxml = os.path.join(os.path.dirname(__file__), 'test_data', 'test_score.musicxml')
        
    def tearDown(self):
        """Clean up test environment"""
        # Remove temporary directory and its contents
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    @unittest.skipIf(not os.path.exists('tests/test_data/test_score.musicxml'), 
                     "Test MusicXML file does not exist")
    def test_analyze_musicxml(self):
        """Test MusicXML analysis functionality"""
        try:
            # analyze_musicxml function returns True/False, not a key-value dictionary
            result = analyze_musicxml(self.test_musicxml)
            self.assertTrue(result)
        except Exception as e:
            self.fail(f"MusicXML analysis test failed: {e}")
    
    @unittest.skipIf(not os.path.exists('tests/test_data/test_score.musicxml'), 
                     "Test MusicXML file does not exist")
    def test_change_instrument(self):
        """Test instrument change functionality"""
        output_file = os.path.join(self.test_dir, 'modified_score.musicxml')
        new_instrument = "Violin"
        
        try:
            result = change_instrument(self.test_musicxml, new_instrument, output_file)
            self.assertTrue(os.path.exists(output_file))
            self.assertEqual(result, output_file)
        except Exception as e:
            self.fail(f"Instrument change test failed: {e}")


if __name__ == '__main__':
    # Ensure test data directory exists
    test_data_dir = os.path.join(os.path.dirname(__file__), 'test_data')
    os.makedirs(test_data_dir, exist_ok=True)
    
    unittest.main()
