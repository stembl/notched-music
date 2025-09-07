# Notched Music Suite

A comprehensive Python audio processing suite featuring two powerful tools:

1. **Notched Music** - Audio processor for applying notch filters to remove specific frequencies
2. **Tinnitus Frequency Identifier** - Vintage-style tone generator for frequency identification

Both applications feature a professional GUI with steampunk-inspired design elements.

## Features

### Notched Music (Audio Processor)
- **Simple GUI Interface**: Easy-to-use graphical interface built with tkinter
- **Notch Filtering**: Remove specific frequencies from audio files using IIR notch filters
- **Precise Frequency Control**: Define exact frequency removal range for precise notch width control
- **Batch Processing**: Process entire directories of audio files at once
- **Multiple Format Support**: Supports WAV, MP3, FLAC, AAC, OGG, and M4A files
- **Metadata Preservation**: Automatically copies metadata from original files
- **Advanced Options**: Optionally modify artist and album metadata
- **Real-time Logging**: View processing progress and logs in real-time
- **Quality Control**: Adjustable quality factor or frequency range for notch filter sharpness
- **MP3 Output**: All processed files are converted to MP3 format with proper metadata

### Tinnitus Frequency Identifier (Tone Generator)
- **Vintage 1970s Design**: Steampunk-inspired GUI with brushed metal and wood aesthetics
- **Frequency Sweep**: Generates logarithmic frequency sweeps across defined ranges
- **Multiple Range Controls**: Quality factor, Hz range, and octave range controls
- **Synchronized Controls**: All range controls update each other automatically
- **Equal-Loudness Weighting**: A-weighting for consistent perceived volume across frequencies
- **Real-time Audio**: Continuous audio output with start/stop controls
- **Professional Layout**: Large frequency display with range indicators

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Quick Setup (Recommended)

#### Windows Users
```bash
# Double-click or run:
setup_venv.bat        # Creates virtual environment and installs dependencies
```

#### Linux/macOS Users
```bash
# Make executable and run:
chmod +x setup_venv.sh
./setup_venv.sh
```

#### Activate Existing Environment
```bash
# Windows:
venv_on.bat           # Automatically creates venv if missing, then activates

# Linux/macOS:
source venv/bin/activate
```

### Manual Setup

1. Clone or download this repository
2. Navigate to the project directory
3. Create virtual environment:
   ```bash
   python -m venv venv
   ```
4. Activate virtual environment:
   ```bash
   # Windows:
   venv\Scripts\activate.bat
   
   # Linux/macOS:
   source venv/bin/activate
   ```
5. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

### Running the Applications

#### Notched Music (Audio Processor)
```bash
# Windows - Activate environment and run:
venv_on.bat
python src/main.py

# Linux/macOS - Activate environment and run:
source venv/bin/activate
python src/main.py
```

#### Tinnitus Frequency Identifier (Tone Generator)
```bash
# Windows - Activate environment and run:
venv_on.bat
python run_tone_generator.py

# Or use the batch file:
tone_generator.bat

# Linux/macOS - Activate environment and run:
source venv/bin/activate
python run_tone_generator.py
```

Or install the package and run from anywhere:

```bash
pip install -e .
notched-music
```

### Setup Scripts

The project includes convenient setup scripts:
- `setup_venv.bat` / `setup_venv.sh` - Create and configure virtual environment with all dependencies
- `venv_on.bat` - Activate existing environment (creates venv if missing)
- `install_dependencies.py` - Install/update dependencies
- `run_tests.py` - Run test suite
- `run_demo.py` - Run interactive demo

See [SETUP_VENV_GUIDE.md](SETUP_VENV_GUIDE.md) for detailed setup instructions.

## Usage

### Basic Usage

1. **Launch the application** by running `python src/main.py`
2. **Select Input Directory**: Choose the folder containing your audio files
3. **Select Output Directory**: Choose where to save the processed files
4. **Set Notch Frequency**: Specify the center frequency (in Hz) you want to remove
5. **Choose Notch Width Control**:
   - **Quality Factor**: Control sharpness (higher = sharper notch)
   - **Frequency Range**: Define exact width of the notch in Hz
6. **Click "Process Audio Files"** to start processing

### Advanced Options

- **Enable Advanced Options**: Check the "Advanced Options" checkbox
- **New Artist Name**: Optionally change the artist metadata for all processed files
- **New Album Name**: Optionally change the album metadata for all processed files

### Supported Audio Formats

- WAV (recommended for best quality)
- MP3
- FLAC
- AAC
- OGG
- M4A

## How It Works

### Notched Music - Audio Processing

The application uses IIR (Infinite Impulse Response) notch filters to remove specific frequencies from audio signals. The notch filter is designed using the `scipy.signal.iirnotch` function, which creates a filter that attenuates frequencies around the specified notch frequency.

**Key Parameters:**
- **Notch Frequency**: The center frequency to be removed (in Hz)
- **Quality Factor**: Controls the sharpness of the notch (higher values = sharper notch)

### Audio Processing Pipeline

1. **Load Audio**: Audio files are loaded using `librosa` for maximum compatibility
2. **Apply Filter**: The notch filter is applied to remove the specified frequency
3. **Save Audio**: Filtered audio is saved as MP3 using `soundfile`
4. **Copy Metadata**: Original metadata is preserved and optionally modified using `eyed3`

### Tinnitus Frequency Identifier - Tone Generation

The tone generator creates logarithmic frequency sweeps across user-defined ranges using real-time audio synthesis.

**Key Features:**
- **Frequency Sweep**: Logarithmic progression across the defined frequency range
- **Equal-Loudness Weighting**: A-weighting approximation for consistent perceived volume
- **Synchronized Controls**: Quality factor, Hz range, and octave range are mathematically linked
- **Real-time Audio**: Continuous audio output using `sounddevice`

**Control Relationships:**
```
Q = center_frequency / bandwidth
bandwidth = center_frequency / Q
frequency_range = ±(bandwidth / 2)
octave_range = log₂(1 + frequency_range/frequency)
```

## Testing

The project includes comprehensive tests for both the audio processing engine and GUI components.

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test files
pytest tests/test_audio_processor.py
pytest tests/test_gui.py
```

### Demo Files

The `demo_files/` directory contains sample audio files for testing in multiple formats:

**WAV Files:**
- `440hz_tone.wav`: Pure 440 Hz tone (A4 note)
- `1000hz_tone.wav`: Pure 1000 Hz tone (perfect for notch filtering demo)
- `2000hz_tone.wav`: Pure 2000 Hz tone
- `5000hz_tone.wav`: Pure 5000 Hz tone (5 kHz - high frequency demo)
- `stereo_test.wav`: Stereo file with different frequencies in each channel

**MP3 Files:**
- Various music files for testing with real audio content
- Demo MP3 files created from WAV tones for format testing

**Note**: The demo script automatically detects and copies all supported audio formats (WAV, MP3, FLAC, AAC, OGG, M4A) from the demo_files directory.

## Project Structure

```
notched_music/
├── src/                           # Source code
│   ├── __init__.py
│   ├── main.py                   # Audio processor entry point
│   ├── gui.py                    # Audio processor GUI
│   ├── audio_processor.py        # Audio processing engine
│   └── tone_generator.py         # Tone generator application
├── tests/                         # Test suite
│   ├── __init__.py
│   ├── test_audio_processor.py
│   └── test_gui.py
├── demo_files/                   # Demo audio files
│   ├── generate_demo_files.py
│   ├── create_simple_demo.py
│   └── *.wav, *.mp3             # Sample audio files
├── docs/                         # Documentation
│   ├── DEVELOPER_GUIDE.md
│   ├── INSTALLATION.md
│   └── USER_GUIDE.md
├── test_results/                 # Test output files
├── requirements.txt              # Python dependencies
├── setup.py                     # Package setup
├── pytest.ini                  # Test configuration
├── run_tone_generator.py        # Tone generator launcher
├── tone_generator.bat           # Windows batch launcher
├── TONE_GENERATOR_README.md     # Tone generator documentation
├── icon.ico                     # Application icon (steampunk heart)
├── icon_preview.png             # Icon preview
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## Dependencies

### Core Dependencies
- **numpy**: Numerical computing
- **scipy**: Scientific computing (signal processing)
- **librosa**: Audio analysis and loading
- **soundfile**: Audio file I/O
- **mutagen**: Audio metadata handling
- **eyed3**: Robust MP3 metadata handling

### GUI Dependencies
- **tkinter**: GUI framework (included with Python)
- **Pillow**: Image processing for GUI icons
- **tkinter-tooltip**: Enhanced tooltips

### Audio Dependencies
- **sounddevice**: Real-time audio output for tone generator

### Development Dependencies
- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting
- **matplotlib**: Plotting (for potential future features)
- **pyinstaller**: Creating standalone executables

## Technical Details

### Notch Filter Implementation

The notch filter is implemented using a second-order IIR filter with the transfer function:

```
H(z) = (1 - 2*cos(ω₀)*z⁻¹ + z⁻²) / (1 - 2*r*cos(ω₀)*z⁻¹ + r²*z⁻²)
```

Where:
- ω₀ is the normalized notch frequency
- r is the pole radius (related to quality factor)

### Quality Factor

The quality factor (Q) determines the sharpness of the notch:
- **Low Q (1-10)**: Wide notch, affects nearby frequencies
- **Medium Q (10-50)**: Moderate notch width
- **High Q (50-100)**: Very sharp notch, minimal effect on nearby frequencies

### Performance Considerations

- **Large Files**: Processing large audio files may take time
- **Batch Processing**: Multiple files are processed sequentially
- **Memory Usage**: Audio files are loaded entirely into memory
- **Threading**: GUI remains responsive during processing

## Troubleshooting

### Common Issues

1. **"Input directory does not exist"**
   - Ensure the input directory path is correct
   - Check that the directory contains audio files

2. **"Unsupported file format"**
   - Only supported formats are processed
   - Convert unsupported files to WAV format first

3. **"Error during processing"**
   - Check the log output for specific error messages
   - Ensure output directory is writable
   - Verify audio files are not corrupted

4. **GUI not responding**
   - Processing runs in a separate thread
   - Wait for processing to complete
   - Check the log for progress updates

### Performance Tips

- Use WAV format for best performance and quality
- Process smaller batches of files for better responsiveness
- Ensure sufficient disk space for output files
- Close other applications to free up system resources

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Python and tkinter
- Audio processing powered by scipy and librosa
- Metadata handling by mutagen
- Testing framework by pytest

## Future Enhancements

- [ ] Real-time audio preview
- [ ] Multiple notch frequencies
- [ ] Frequency spectrum visualization
- [ ] Batch processing with progress bars
- [ ] Command-line interface
- [ ] Plugin system for custom filters
- [ ] Audio format conversion
- [ ] Preset management
- [ ] Undo/redo functionality
- [ ] Drag-and-drop file support

