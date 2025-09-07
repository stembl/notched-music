# Developer Guide

This guide provides information for developers who want to contribute to or extend the Notched Music application.

## Project Architecture

### Overview

The Notched Music application follows a modular architecture with clear separation of concerns:

```
src/
├── main.py              # Application entry point
├── gui.py               # GUI layer (tkinter)
├── audio_processor.py   # Audio processing engine
└── __init__.py          # Package initialization
```

### Core Components

#### 1. AudioProcessor Class

**Location**: `src/audio_processor.py`

**Responsibilities**:
- Audio file loading and saving
- Notch filter implementation
- Metadata handling
- Batch processing coordination

**Key Methods**:
- `load_audio()`: Load audio files using librosa
- `apply_notch_filter()`: Apply IIR notch filter
- `save_audio()`: Save processed audio
- `copy_metadata()`: Handle metadata preservation
- `process_file()`: Complete file processing pipeline
- `process_directory()`: Batch processing

#### 2. GUI Application

**Location**: `src/gui.py`

**Responsibilities**:
- User interface management
- Input validation
- Progress reporting
- Error handling

**Key Components**:
- `NotchedMusicGUI`: Main GUI class
- Input/output directory selection
- Parameter controls (frequency, quality)
- Advanced options panel
- Processing status and logging

#### 3. Main Entry Point

**Location**: `src/main.py`

**Responsibilities**:
- Application initialization
- Logging setup
- Error handling
- Entry point for command-line usage

## Development Setup

### Prerequisites

1. **Python 3.8+**
2. **Git** for version control
3. **IDE** (VS Code, PyCharm, etc.)
4. **Audio analysis tools** (optional, for testing)

### Development Environment

1. **Clone the repository**:
   ```bash
   git clone https://github.com/username/notched-music.git
   cd notched-music
   ```

2. **Create development environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov black flake8 mypy
   ```

4. **Install in development mode**:
   ```bash
   pip install -e .
   ```

### Code Quality Tools

#### Linting and Formatting

```bash
# Code formatting
black src/ tests/

# Linting
flake8 src/ tests/

# Type checking
mypy src/
```

#### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_audio_processor.py -v
```

## Audio Processing Details

### Notch Filter Implementation

The notch filter is implemented using scipy's `iirnotch` function:

```python
def apply_notch_filter(self, audio_data: np.ndarray, sample_rate: int) -> np.ndarray:
    # Design IIR notch filter
    nyquist = sample_rate / 2
    normalized_freq = self.notch_frequency / nyquist
    
    # Ensure frequency is within valid range
    if normalized_freq >= 1.0:
        return audio_data
    
    # Design IIR notch filter
    b, a = signal.iirnotch(self.notch_frequency, self.quality_factor, sample_rate)
    
    # Apply filter using zero-phase filtering
    if audio_data.ndim == 1:
        filtered_audio = signal.filtfilt(b, a, audio_data)
    else:
        filtered_audio = np.zeros_like(audio_data)
        for channel in range(audio_data.shape[0]):
            filtered_audio[channel] = signal.filtfilt(b, a, audio_data[channel])
    
    return filtered_audio
```

### Filter Design Parameters

- **Notch Frequency**: Center frequency to be removed
- **Quality Factor**: Controls filter sharpness (Q = f₀ / bandwidth)
- **Sample Rate**: Audio sample rate (typically 44.1 kHz)

### Audio Format Support

Supported formats are defined in `AudioProcessor.SUPPORTED_FORMATS`:

```python
SUPPORTED_FORMATS = {'.wav', '.mp3', '.flac', '.aac', '.ogg', '.m4a'}
```

Format handling:
- **WAV**: Direct processing with soundfile
- **MP3/FLAC/AAC/OGG/M4A**: Loaded with librosa, saved as WAV
- **Metadata**: Preserved using mutagen

## Testing Strategy

### Test Structure

```
tests/
├── __init__.py
├── test_audio_processor.py    # Audio processing tests
├── test_gui.py                # GUI component tests
└── conftest.py               # Test fixtures (if needed)
```

### Test Categories

#### 1. Unit Tests

**AudioProcessor Tests**:
- Filter application on mono/stereo audio
- Invalid frequency handling
- File format validation
- Metadata copying

**GUI Tests**:
- Input validation
- Widget state management
- Error handling

#### 2. Integration Tests

- Complete processing pipeline
- File I/O operations
- GUI-to-processor communication

#### 3. Performance Tests

- Large file processing
- Batch processing efficiency
- Memory usage monitoring

### Test Data

Demo files in `demo_files/`:
- Pure tones at various frequencies
- Stereo test files
- Short duration files for quick testing

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Specific test
pytest tests/test_audio_processor.py::TestAudioProcessor::test_apply_notch_filter_mono

# Performance tests
pytest -m slow

# Integration tests
pytest -m integration
```

## Contributing Guidelines

### Code Style

- **PEP 8**: Follow Python style guidelines
- **Type Hints**: Use type annotations for function parameters and returns
- **Docstrings**: Document all public functions and classes
- **Comments**: Explain complex logic and algorithms

### Commit Messages

Use conventional commit format:

```
feat: add support for new audio format
fix: resolve memory leak in batch processing
docs: update installation guide
test: add integration tests for GUI
refactor: simplify audio loading logic
```

### Pull Request Process

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/new-feature`
3. **Make changes** with tests
4. **Run tests**: `pytest`
5. **Check code quality**: `black`, `flake8`, `mypy`
6. **Commit changes**: Use conventional commit format
7. **Push branch**: `git push origin feature/new-feature`
8. **Create pull request**

### Code Review Checklist

- [ ] Code follows style guidelines
- [ ] Tests pass and coverage is maintained
- [ ] Documentation is updated
- [ ] No breaking changes (or properly documented)
- [ ] Performance impact is considered
- [ ] Error handling is appropriate

## Extending the Application

### Adding New Audio Formats

1. **Update supported formats**:
   ```python
   SUPPORTED_FORMATS = {'.wav', '.mp3', '.flac', '.aac', '.ogg', '.m4a', '.new_format'}
   ```

2. **Handle format-specific loading/saving**:
   ```python
   def load_audio(self, file_path: str) -> Tuple[np.ndarray, int]:
       # Add format-specific handling
       if file_path.endswith('.new_format'):
           # Custom loading logic
           pass
   ```

3. **Add tests** for new format support

### Adding New Filter Types

1. **Create filter class**:
   ```python
   class HighPassFilter:
       def __init__(self, cutoff_frequency: float):
           self.cutoff_frequency = cutoff_frequency
       
       def apply_filter(self, audio_data: np.ndarray, sample_rate: int) -> np.ndarray:
           # Filter implementation
           pass
   ```

2. **Integrate with AudioProcessor**:
   ```python
   def apply_custom_filter(self, filter_type: str, **kwargs):
       if filter_type == 'highpass':
           filter_obj = HighPassFilter(**kwargs)
           return filter_obj.apply_filter(self.audio_data, self.sample_rate)
   ```

3. **Update GUI** to include new filter options

### Adding Batch Processing Features

1. **Progress tracking**:
   ```python
   def process_directory_with_progress(self, input_dir: str, output_dir: str, 
                                     progress_callback=None):
       files = self._get_audio_files(input_dir)
       for i, file in enumerate(files):
           self.process_file(file, output_path)
           if progress_callback:
               progress_callback(i + 1, len(files))
   ```

2. **Parallel processing**:
   ```python
   from concurrent.futures import ThreadPoolExecutor
   
   def process_directory_parallel(self, input_dir: str, output_dir: str, 
                                 max_workers: int = 4):
       with ThreadPoolExecutor(max_workers=max_workers) as executor:
           # Submit processing tasks
           pass
   ```

### Adding Command-Line Interface

1. **Create CLI module**:
   ```python
   import argparse
   
   def create_parser():
       parser = argparse.ArgumentParser(description='Notched Music CLI')
       parser.add_argument('--input', required=True, help='Input directory')
       parser.add_argument('--output', required=True, help='Output directory')
       parser.add_argument('--frequency', type=float, required=True, help='Notch frequency')
       return parser
   ```

2. **Update main.py**:
   ```python
   def main():
       if len(sys.argv) > 1:
           # CLI mode
           cli_main()
       else:
           # GUI mode
           gui_main()
   ```

## Performance Optimization

### Memory Management

- **Streaming processing**: For very large files
- **Chunk-based processing**: Process audio in chunks
- **Memory monitoring**: Track memory usage during processing

### CPU Optimization

- **Vectorized operations**: Use NumPy efficiently
- **Parallel processing**: Multi-threading for batch operations
- **Caching**: Cache filter coefficients for repeated use

### I/O Optimization

- **Async I/O**: Non-blocking file operations
- **Batch I/O**: Group file operations
- **Compression**: Use appropriate compression levels

## Debugging

### Common Issues

1. **Audio artifacts**: Check filter parameters and implementation
2. **Memory leaks**: Monitor memory usage during long operations
3. **GUI freezing**: Ensure processing runs in separate threads
4. **File format issues**: Verify format support and metadata handling

### Debugging Tools

- **Logging**: Use Python logging for detailed information
- **Profiling**: Use cProfile for performance analysis
- **Memory profiling**: Use memory_profiler for memory issues
- **Audio analysis**: Use external tools to verify filter results

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Release Process

### Version Management

- **Semantic versioning**: MAJOR.MINOR.PATCH
- **Changelog**: Document all changes
- **Git tags**: Tag releases in Git

### Release Checklist

- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Version numbers are updated
- [ ] Changelog is updated
- [ ] Release notes are written
- [ ] Package is built and tested
- [ ] Release is tagged in Git

### Building Packages

```bash
# Build source distribution
python setup.py sdist

# Build wheel
python setup.py bdist_wheel

# Install locally for testing
pip install dist/notched_music-1.0.0-py3-none-any.whl
```

