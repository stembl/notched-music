"""
Tests for the AudioProcessor class.
"""

import pytest
import numpy as np
import tempfile
import os
from pathlib import Path
import sys

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from audio_processor import AudioProcessor


class TestAudioProcessor:
    """Test cases for AudioProcessor class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.processor = AudioProcessor(notch_frequency=1000.0, quality_factor=30.0)
        self.temp_dir = tempfile.mkdtemp()
        
    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_init(self):
        """Test AudioProcessor initialization."""
        assert self.processor.notch_frequency == 1000.0
        assert self.processor.quality_factor == 30.0
        assert self.processor.frequency_range is None
        assert self.processor.sample_rate is None
    
    def test_init_with_frequency_range(self):
        """Test AudioProcessor initialization with frequency range."""
        processor = AudioProcessor(notch_frequency=1000.0, quality_factor=30.0, frequency_range=50.0)
        assert processor.notch_frequency == 1000.0
        assert processor.quality_factor == 30.0
        assert processor.frequency_range == 50.0
        assert processor.sample_rate is None
    
    def test_supported_formats(self):
        """Test supported audio formats."""
        expected_formats = {'.wav', '.mp3', '.flac', '.aac', '.ogg', '.m4a'}
        assert AudioProcessor.SUPPORTED_FORMATS == expected_formats
    
    def test_apply_notch_filter_mono(self):
        """Test notch filter application on mono audio."""
        # Create test audio signal
        sample_rate = 44100
        duration = 1.0  # seconds
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        
        # Create signal with multiple frequencies
        signal_data = (np.sin(2 * np.pi * 500 * t) +  # 500 Hz
                      np.sin(2 * np.pi * 1000 * t) +  # 1000 Hz (to be notched)
                      np.sin(2 * np.pi * 2000 * t))   # 2000 Hz
        
        # Apply notch filter
        filtered_signal = self.processor.apply_notch_filter(signal_data, sample_rate)
        
        # Check that signal was filtered
        assert filtered_signal.shape == signal_data.shape
        assert not np.array_equal(filtered_signal, signal_data)
        
        # Check that the notch frequency component is reduced
        # This is a basic check - in practice, you'd use FFT to verify frequency content
        assert np.max(np.abs(filtered_signal)) < np.max(np.abs(signal_data))
    
    def test_apply_notch_filter_stereo(self):
        """Test notch filter application on stereo audio."""
        # Create test stereo audio signal
        sample_rate = 44100
        duration = 1.0
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        
        # Create stereo signal
        left_channel = np.sin(2 * np.pi * 1000 * t)
        right_channel = np.sin(2 * np.pi * 1000 * t) * 0.5
        signal_data = np.array([left_channel, right_channel])
        
        # Apply notch filter
        filtered_signal = self.processor.apply_notch_filter(signal_data, sample_rate)
        
        # Check that signal was filtered
        assert filtered_signal.shape == signal_data.shape
        assert not np.array_equal(filtered_signal, signal_data)
    
    def test_apply_notch_filter_invalid_frequency(self):
        """Test notch filter with invalid frequency."""
        sample_rate = 44100
        signal_data = np.random.randn(1000)
        
        # Set frequency higher than Nyquist
        self.processor.notch_frequency = sample_rate + 1000
        
        # Should return original signal without error
        filtered_signal = self.processor.apply_notch_filter(signal_data, sample_rate)
        assert np.array_equal(filtered_signal, signal_data)
    
    def test_apply_notch_filter_with_frequency_range(self):
        """Test notch filter with frequency range instead of quality factor."""
        # Create processor with frequency range
        processor = AudioProcessor(notch_frequency=1000.0, frequency_range=50.0)
        
        # Create test audio signal
        sample_rate = 44100
        duration = 1.0
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        signal_data = np.sin(2 * np.pi * 1000 * t)  # 1000 Hz tone
        
        # Apply notch filter
        filtered_signal = processor.apply_notch_filter(signal_data, sample_rate)
        
        # Check that signal was filtered
        assert filtered_signal.shape == signal_data.shape
        assert not np.array_equal(filtered_signal, signal_data)
        
        # Check that the notch frequency component is reduced
        assert np.max(np.abs(filtered_signal)) < np.max(np.abs(signal_data))
    
    def test_save_audio_wav(self):
        """Test saving audio to WAV format."""
        # Create test audio data
        sample_rate = 44100
        duration = 0.1  # Short duration for testing
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        audio_data = np.sin(2 * np.pi * 440 * t)  # A4 note
        
        output_path = os.path.join(self.temp_dir, "test_output.wav")
        
        # Save audio
        self.processor.save_audio(audio_data, sample_rate, output_path)
        
        # Check that file was created
        assert os.path.exists(output_path)
        
        # Verify file size is reasonable
        file_size = os.path.getsize(output_path)
        assert file_size > 0
    
    def test_save_audio_stereo(self):
        """Test saving stereo audio."""
        sample_rate = 44100
        duration = 0.1
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        
        # Create stereo audio
        left_channel = np.sin(2 * np.pi * 440 * t)
        right_channel = np.sin(2 * np.pi * 880 * t)
        audio_data = np.array([left_channel, right_channel])
        
        output_path = os.path.join(self.temp_dir, "test_stereo.wav")
        
        # Save audio
        self.processor.save_audio(audio_data, sample_rate, output_path)
        
        # Check that file was created
        assert os.path.exists(output_path)
    
    def test_copy_metadata_nonexistent_file(self):
        """Test metadata copying with non-existent files."""
        source_path = "nonexistent_source.wav"
        target_path = "nonexistent_target.wav"
        
        # Should not raise exception
        self.processor.copy_metadata(source_path, target_path)
    
    def test_process_file_nonexistent(self):
        """Test processing non-existent file."""
        input_path = "nonexistent_input.wav"
        output_path = os.path.join(self.temp_dir, "output.wav")
        
        result = self.processor.process_file(input_path, output_path)
        assert result is False
    
    def test_process_file_unsupported_format(self):
        """Test processing unsupported file format."""
        input_path = "test.txt"  # Unsupported format
        output_path = os.path.join(self.temp_dir, "output.wav")
        
        result = self.processor.process_file(input_path, output_path)
        assert result is False
    
    def test_process_directory_nonexistent(self):
        """Test processing non-existent directory."""
        input_dir = "nonexistent_directory"
        output_dir = os.path.join(self.temp_dir, "output")
        
        result = self.processor.process_directory(input_dir, output_dir)
        assert result == []
    
    def test_process_directory_empty(self):
        """Test processing empty directory."""
        # Create empty directory
        input_dir = os.path.join(self.temp_dir, "empty_input")
        os.makedirs(input_dir)
        
        output_dir = os.path.join(self.temp_dir, "output")
        
        result = self.processor.process_directory(input_dir, output_dir)
        assert result == []
    
    def test_process_directory_with_audio_files(self):
        """Test processing directory with audio files."""
        # Create input directory with test audio files
        input_dir = os.path.join(self.temp_dir, "input")
        os.makedirs(input_dir)
        
        # Create test audio files (we'll create simple WAV files)
        for i in range(3):
            audio_path = os.path.join(input_dir, f"test_{i}.wav")
            self._create_test_wav_file(audio_path)
        
        output_dir = os.path.join(self.temp_dir, "output")
        
        # Process directory
        result = self.processor.process_directory(input_dir, output_dir)
        
        # Check results
        assert len(result) == 3
        assert os.path.exists(output_dir)
        
        # Check that output files were created
        for i in range(3):
            output_file = os.path.join(output_dir, f"test_{i}.wav")
            assert os.path.exists(output_file)
    
    def _create_test_wav_file(self, file_path):
        """Create a simple test WAV file."""
        import soundfile as sf
        
        sample_rate = 44100
        duration = 0.1
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        audio_data = np.sin(2 * np.pi * 440 * t)  # A4 note
        
        sf.write(file_path, audio_data, sample_rate)


class TestAudioProcessorIntegration:
    """Integration tests for AudioProcessor."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_full_processing_pipeline(self):
        """Test the complete processing pipeline."""
        processor = AudioProcessor(notch_frequency=1000.0, quality_factor=30.0)
        
        # Create test input directory
        input_dir = os.path.join(self.temp_dir, "input")
        os.makedirs(input_dir)
        
        # Create test audio file
        audio_path = os.path.join(input_dir, "test.wav")
        self._create_test_wav_file(audio_path)
        
        # Process file
        output_path = os.path.join(self.temp_dir, "output.wav")
        result = processor.process_file(audio_path, output_path, "Test Artist", "Test Album")
        
        # Verify processing was successful
        assert result is True
        assert os.path.exists(output_path)
        
        # Verify file size is reasonable
        file_size = os.path.getsize(output_path)
        assert file_size > 0
    
    def _create_test_wav_file(self, file_path):
        """Create a simple test WAV file."""
        import soundfile as sf
        
        sample_rate = 44100
        duration = 0.1
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        audio_data = np.sin(2 * np.pi * 440 * t)  # A4 note
        
        sf.write(file_path, audio_data, sample_rate)


if __name__ == "__main__":
    pytest.main([__file__])

