"""
Tests for the GUI module.
"""

import pytest
import tkinter as tk
import sys
from pathlib import Path
import tempfile
import os

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gui import NotchedMusicGUI


class TestNotchedMusicGUI:
    """Test cases for NotchedMusicGUI class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        try:
            self.root = tk.Tk()
            self.root.withdraw()  # Hide the window during tests
            self.gui = NotchedMusicGUI(self.root)
            self.temp_dir = tempfile.mkdtemp()
        except tk.TclError as e:
            pytest.skip(f"Tkinter not available: {e}")
    
    def teardown_method(self):
        """Clean up test fixtures."""
        if hasattr(self, 'root') and self.root:
            self.root.destroy()
        if hasattr(self, 'temp_dir'):
            import shutil
            shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_gui_initialization(self):
        """Test GUI initialization."""
        assert self.gui.input_dir.get() == ""
        assert self.gui.output_dir.get() == ""
        assert self.gui.notch_frequency.get() == 1000.0
        assert self.gui.quality_factor.get() == 30.0
        assert self.gui.frequency_range.get() == 50.0
        assert self.gui.use_frequency_range.get() is False
        assert self.gui.new_artist.get() == ""
        assert self.gui.new_album.get() == ""
        assert self.gui.advanced_mode.get() is False
        assert self.gui.is_processing is False
    
    def test_browse_input_dir(self):
        """Test input directory browsing."""
        # This test would require mocking filedialog.askdirectory
        # For now, we'll just test that the method exists and is callable
        assert callable(self.gui.browse_input_dir)
    
    def test_browse_output_dir(self):
        """Test output directory browsing."""
        # This test would require mocking filedialog.askdirectory
        # For now, we'll just test that the method exists and is callable
        assert callable(self.gui.browse_output_dir)
    
    def test_toggle_advanced(self):
        """Test advanced options toggle."""
        # Initially advanced options should be hidden
        assert self.gui.advanced_mode.get() is False
        
        # Toggle advanced mode
        self.gui.advanced_mode.set(True)
        self.gui.toggle_advanced()
        
        # Toggle back
        self.gui.advanced_mode.set(False)
        self.gui.toggle_advanced()
    
    def test_toggle_range_mode(self):
        """Test frequency range mode toggle."""
        # Initially frequency range mode should be disabled
        assert self.gui.use_frequency_range.get() is False
        
        # Toggle to frequency range mode
        self.gui.use_frequency_range.set(True)
        self.gui.toggle_range_mode()
        
        # Toggle back to quality factor mode
        self.gui.use_frequency_range.set(False)
        self.gui.toggle_range_mode()
    
    def test_validate_inputs_empty(self):
        """Test input validation with empty inputs."""
        # All inputs empty
        result = self.gui.validate_inputs()
        assert result is False
    
    def test_validate_inputs_missing_input_dir(self):
        """Test input validation with missing input directory."""
        self.gui.output_dir.set("/some/output/path")
        result = self.gui.validate_inputs()
        assert result is False
    
    def test_validate_inputs_missing_output_dir(self):
        """Test input validation with missing output directory."""
        self.gui.input_dir.set("/some/input/path")
        result = self.gui.validate_inputs()
        assert result is False
    
    def test_validate_inputs_nonexistent_input_dir(self):
        """Test input validation with non-existent input directory."""
        self.gui.input_dir.set("/nonexistent/path")
        self.gui.output_dir.set("/some/output/path")
        result = self.gui.validate_inputs()
        assert result is False
    
    def test_validate_inputs_invalid_frequency(self):
        """Test input validation with invalid frequency."""
        # Create a temporary directory for input
        input_dir = os.path.join(self.temp_dir, "input")
        os.makedirs(input_dir)
        
        self.gui.input_dir.set(input_dir)
        self.gui.output_dir.set("/some/output/path")
        self.gui.notch_frequency.set(0)  # Invalid frequency
        result = self.gui.validate_inputs()
        assert result is False
    
    def test_validate_inputs_invalid_quality_factor(self):
        """Test input validation with invalid quality factor."""
        # Create a temporary directory for input
        input_dir = os.path.join(self.temp_dir, "input")
        os.makedirs(input_dir)
        
        self.gui.input_dir.set(input_dir)
        self.gui.output_dir.set("/some/output/path")
        self.gui.quality_factor.set(0)  # Invalid quality factor
        result = self.gui.validate_inputs()
        assert result is False
    
    def test_validate_inputs_valid(self):
        """Test input validation with valid inputs."""
        # Create a temporary directory for input
        input_dir = os.path.join(self.temp_dir, "input")
        os.makedirs(input_dir)
        
        self.gui.input_dir.set(input_dir)
        self.gui.output_dir.set("/some/output/path")
        self.gui.notch_frequency.set(1000.0)
        self.gui.quality_factor.set(30.0)
        result = self.gui.validate_inputs()
        assert result is True
    
    def test_start_processing_invalid_inputs(self):
        """Test starting processing with invalid inputs."""
        # Should not start processing with invalid inputs
        self.gui.start_processing()
        assert self.gui.is_processing is False
    
    def test_start_processing_already_processing(self):
        """Test starting processing when already processing."""
        # Set up valid inputs
        input_dir = os.path.join(self.temp_dir, "input")
        os.makedirs(input_dir)
        
        self.gui.input_dir.set(input_dir)
        self.gui.output_dir.set("/some/output/path")
        
        # Set processing state
        self.gui.is_processing = True
        
        # Should not start new processing
        self.gui.start_processing()
        assert self.gui.is_processing is True


class TestGUIIntegration:
    """Integration tests for GUI components."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_gui_creation_and_destruction(self):
        """Test GUI creation and destruction."""
        try:
            root = tk.Tk()
            root.withdraw()  # Hide the window
            
            try:
                gui = NotchedMusicGUI(root)
                assert gui is not None
                assert gui.root == root
            finally:
                root.destroy()
        except tk.TclError as e:
            pytest.skip(f"Tkinter not available: {e}")
    
    def test_gui_widgets_exist(self):
        """Test that all expected widgets exist."""
        try:
            root = tk.Tk()
            root.withdraw()  # Hide the window
            
            try:
                gui = NotchedMusicGUI(root)
                
                # Check that key widgets exist
                assert hasattr(gui, 'input_dir')
                assert hasattr(gui, 'output_dir')
                assert hasattr(gui, 'notch_frequency')
                assert hasattr(gui, 'quality_factor')
                assert hasattr(gui, 'new_artist')
                assert hasattr(gui, 'new_album')
                assert hasattr(gui, 'advanced_mode')
                assert hasattr(gui, 'process_button')
                assert hasattr(gui, 'progress_bar')
                assert hasattr(gui, 'status_label')
                assert hasattr(gui, 'log_text')
                
            finally:
                root.destroy()
        except tk.TclError as e:
            pytest.skip(f"Tkinter not available: {e}")


if __name__ == "__main__":
    pytest.main([__file__])

