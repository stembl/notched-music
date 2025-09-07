# Contributing to Notched Music

Thank you for your interest in contributing to Notched Music! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Process](#contributing-process)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing Guidelines](#testing-guidelines)
- [Documentation Guidelines](#documentation-guidelines)
- [Issue Reporting](#issue-reporting)
- [Pull Request Process](#pull-request-process)
- [Release Process](#release-process)

## Code of Conduct

This project follows a code of conduct that ensures a welcoming environment for all contributors. Please:

- Be respectful and inclusive
- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of audio processing concepts
- Familiarity with Python and tkinter (for GUI contributions)

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/notched-music.git
   cd notched-music
   ```

3. **Create a development environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate     # Windows
   ```

4. **Install dependencies**:
   ```bash
   python install_dependencies.py
   ```

5. **Install in development mode**:
   ```bash
   pip install -e .
   ```

6. **Run tests** to ensure everything works:
   ```bash
   python run_tests.py
   ```

## Contributing Process

### Types of Contributions

We welcome several types of contributions:

- **Bug fixes**: Fix issues in existing code
- **New features**: Add new functionality
- **Documentation**: Improve or add documentation
- **Tests**: Add or improve test coverage
- **Performance**: Optimize existing code
- **UI/UX**: Improve the user interface
- **Audio processing**: Enhance audio algorithms

### Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the guidelines below

3. **Test your changes**:
   ```bash
   python run_tests.py
   ```

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** on GitHub

## Code Style Guidelines

### Python Style

- Follow **PEP 8** style guidelines
- Use **type hints** for function parameters and return values
- Write **docstrings** for all public functions and classes
- Use **meaningful variable names**
- Keep functions **small and focused**
- Use **list comprehensions** when appropriate
- Follow **conventional commit messages**

### Code Formatting

We use automated formatting tools:

```bash
# Format code with black
black src/ tests/

# Check style with flake8
flake8 src/ tests/

# Type checking with mypy
mypy src/
```

### Example Code Style

```python
def apply_notch_filter(
    self, 
    audio_data: np.ndarray, 
    sample_rate: int
) -> np.ndarray:
    """
    Apply notch filter to audio data.
    
    Args:
        audio_data: Audio data array
        sample_rate: Sample rate of the audio
        
    Returns:
        Filtered audio data
        
    Raises:
        ValueError: If sample rate is invalid
    """
    if sample_rate <= 0:
        raise ValueError("Sample rate must be positive")
    
    # Implementation here
    return filtered_audio
```

## Testing Guidelines

### Test Requirements

- **All new code must have tests**
- **Maintain or improve test coverage**
- **Tests should be fast and reliable**
- **Use descriptive test names**
- **Test both success and failure cases**

### Test Structure

```python
class TestAudioProcessor:
    """Test cases for AudioProcessor class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.processor = AudioProcessor(1000.0, 30.0)
    
    def test_apply_notch_filter_mono(self):
        """Test notch filter application on mono audio."""
        # Test implementation
        pass
    
    def test_apply_notch_filter_invalid_frequency(self):
        """Test notch filter with invalid frequency."""
        # Test error handling
        pass
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/test_audio_processor.py::TestAudioProcessor::test_apply_notch_filter_mono
```

## Documentation Guidelines

### Code Documentation

- **Docstrings**: Use Google-style docstrings
- **Comments**: Explain complex logic and algorithms
- **Type hints**: Include type information
- **Examples**: Provide usage examples when helpful

### User Documentation

- **README.md**: Keep installation and basic usage current
- **User Guide**: Update when adding new features
- **API Documentation**: Document public interfaces
- **Examples**: Provide clear examples

### Documentation Format

```python
def process_file(
    self, 
    input_path: str, 
    output_path: str,
    new_artist: Optional[str] = None,
    new_album: Optional[str] = None
) -> bool:
    """
    Process a single audio file with notch filtering.
    
    This method loads an audio file, applies a notch filter to remove
    the specified frequency, saves the filtered audio, and optionally
    modifies metadata.
    
    Args:
        input_path: Path to the input audio file
        output_path: Path to save the processed audio file
        new_artist: Optional new artist name for metadata
        new_album: Optional new album name for metadata
        
    Returns:
        True if processing was successful, False otherwise
        
    Example:
        >>> processor = AudioProcessor(1000.0, 30.0)
        >>> success = processor.process_file(
        ...     "input.wav", 
        ...     "output.wav",
        ...     "New Artist",
        ...     "New Album"
        ... )
        >>> print(f"Processing successful: {success}")
    """
```

## Issue Reporting

### Before Creating an Issue

1. **Search existing issues** to avoid duplicates
2. **Check the documentation** for solutions
3. **Test with the latest version**
4. **Gather relevant information**

### Issue Template

When creating an issue, include:

- **Clear title**: Brief description of the problem
- **Description**: Detailed explanation of the issue
- **Steps to reproduce**: Exact steps to reproduce the problem
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Environment**: OS, Python version, package versions
- **Screenshots**: If applicable
- **Sample files**: If audio-related

### Bug Report Example

```markdown
**Bug Report: GUI Freezes During Processing**

**Description:**
The GUI becomes unresponsive when processing large audio files.

**Steps to reproduce:**
1. Open the application
2. Select a directory with large WAV files (>100MB)
3. Set notch frequency to 1000 Hz
4. Click "Process Audio Files"
5. GUI becomes unresponsive

**Expected behavior:**
GUI should remain responsive with progress updates.

**Actual behavior:**
GUI freezes and shows "Not Responding" in title bar.

**Environment:**
- OS: Windows 10
- Python: 3.10.0
- Package version: 1.0.0

**Sample files:**
[Attach small sample file if possible]
```

## Pull Request Process

### Before Submitting

- [ ] **Tests pass**: All tests must pass
- [ ] **Code style**: Follow style guidelines
- [ ] **Documentation**: Update relevant documentation
- [ ] **Commit messages**: Use conventional commit format
- [ ] **Single responsibility**: One feature/fix per PR

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
- [ ] Tests pass
- [ ] New tests added (if applicable)
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)

## Screenshots
[If GUI changes]
```

### Review Process

1. **Automated checks**: CI/CD pipeline runs tests and style checks
2. **Code review**: Maintainers review the code
3. **Testing**: Manual testing may be requested
4. **Approval**: At least one maintainer approval required
5. **Merge**: Changes are merged to main branch

## Release Process

### Version Numbering

We use [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] **Update version numbers** in setup.py and __init__.py
- [ ] **Update CHANGELOG.md** with new features/fixes
- [ ] **Run full test suite**
- [ ] **Update documentation** if needed
- [ ] **Create release tag** in Git
- [ ] **Build and test package**
- [ ] **Publish to PyPI** (if applicable)
- [ ] **Create GitHub release**

## Getting Help

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Pull Requests**: Code review and discussion

### Resources

- **Documentation**: Check docs/ directory
- **Examples**: Look at demo_files/ and tests/
- **Code**: Study existing code in src/

## Recognition

Contributors will be recognized in:
- **README.md**: Contributor list
- **CHANGELOG.md**: Release notes
- **GitHub**: Contributor statistics

Thank you for contributing to Notched Music! 🎵
