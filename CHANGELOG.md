# Changelog

All notable changes to the Notched Music project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-07

### Added
- Initial release of Notched Music application
- GUI interface built with tkinter
- Audio processing engine with IIR notch filtering
- Support for multiple audio formats (WAV, MP3, FLAC, AAC, OGG, M4A)
- Batch processing capabilities
- Metadata preservation and editing
- Advanced options for artist/album name modification
- Comprehensive test suite with pytest
- Demo audio files for testing
- Complete documentation (README, User Guide, Developer Guide, Installation Guide)
- CI/CD pipeline with GitHub Actions
- Cross-platform support (Windows, macOS, Linux)
- Real-time logging and progress tracking
- Input validation and error handling
- Quality factor adjustment for notch filter sharpness
- Frequency range: 20 Hz to 20,000 Hz
- Quality factor range: 1 to 100

### Technical Features
- Audio loading with librosa for maximum compatibility
- IIR notch filter implementation using scipy.signal.iirnotch
- Zero-phase filtering with scipy.signal.filtfilt
- Metadata handling with mutagen
- Audio I/O with soundfile
- Threading for responsive GUI during processing
- Modular architecture with clear separation of concerns

### Documentation
- Comprehensive README with installation and usage instructions
- User Guide with detailed workflow instructions
- Developer Guide for contributors and extenders
- Installation Guide with platform-specific instructions
- API documentation in docstrings
- Test documentation and examples

### Testing
- Unit tests for audio processing engine
- GUI component tests
- Integration tests for complete workflow
- Performance tests for large files
- Demo files for testing and validation
- Coverage reporting with pytest-cov

### Project Structure
- Modular source code organization
- Comprehensive test suite
- Demo files and scripts
- Documentation in multiple formats
- CI/CD configuration
- Package setup and distribution files

## [Unreleased]

### Planned Features
- Real-time audio preview
- Multiple notch frequencies
- Frequency spectrum visualization
- Command-line interface
- Plugin system for custom filters
- Audio format conversion
- Preset management
- Undo/redo functionality
- Drag-and-drop file support
- Parallel processing for improved performance
- Streaming processing for very large files
- Advanced filter types (high-pass, low-pass, band-pass)
- Audio analysis tools integration
- Batch processing with progress bars
- Configuration file support
- Logging to file
- Audio quality metrics
- Processing statistics and reports

### Potential Improvements
- Performance optimization for large files
- Memory usage optimization
- Better error recovery
- More audio format support
- Enhanced metadata editing
- Audio normalization options
- Frequency analysis tools
- Custom filter design
- Audio comparison tools
- Processing history tracking
- Export/import settings
- Multi-language support
- Accessibility improvements
- Dark mode theme
- Customizable interface
- Keyboard shortcuts
- Context menus
- File association support
- System tray integration
- Automatic updates
- Cloud processing support
- Mobile app version
- Web interface
- API for third-party integration
