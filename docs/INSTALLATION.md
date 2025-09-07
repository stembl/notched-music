# Installation Guide

This guide provides detailed instructions for installing and setting up the Notched Music application.

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.8 or higher
- **RAM**: 4 GB minimum, 8 GB recommended
- **Storage**: 500 MB free space for installation and temporary files
- **Audio**: Sound card or audio interface for testing

### Recommended Requirements
- **Python**: Version 3.10 or 3.11
- **RAM**: 16 GB or more
- **Storage**: 2 GB free space
- **CPU**: Multi-core processor for faster batch processing

## Installation Methods

### Method 1: Direct Installation (Recommended)

1. **Download the project**
   ```bash
   git clone https://github.com/username/notched-music.git
   cd notched-music
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install the package**
   ```bash
   pip install -e .
   ```

5. **Run the application**
   ```bash
   python src/main.py
   ```

### Method 2: Using pip (if published to PyPI)

```bash
pip install notched-music
notched-music
```

### Method 3: Using conda (if available)

```bash
conda create -n notched-music python=3.10
conda activate notched-music
pip install -r requirements.txt
python src/main.py
```

## Dependency Installation

### Core Dependencies

The following packages are automatically installed with `pip install -r requirements.txt`:

- **numpy** (≥1.21.0): Numerical computing
- **scipy** (≥1.7.0): Scientific computing and signal processing
- **librosa** (≥0.9.0): Audio analysis and loading
- **soundfile** (≥0.10.0): Audio file I/O
- **mutagen** (≥1.45.0): Audio metadata handling
- **Pillow** (≥8.3.0): Image processing
- **matplotlib** (≥3.4.0): Plotting and visualization

### Development Dependencies

For development and testing:

```bash
pip install pytest pytest-cov
```

## Platform-Specific Instructions

### Windows

1. **Install Python** from [python.org](https://python.org)
2. **Enable long paths** in Windows 10/11:
   - Run `gpedit.msc` as administrator
   - Navigate to Computer Configuration > Administrative Templates > System > Filesystem
   - Enable "Enable Win32 long paths"
3. **Install Visual C++ Redistributable** if you encounter build errors

### macOS

1. **Install Python** using Homebrew:
   ```bash
   brew install python@3.10
   ```
2. **Install Xcode Command Line Tools**:
   ```bash
   xcode-select --install
   ```

### Linux (Ubuntu/Debian)

1. **Install Python and development tools**:
   ```bash
   sudo apt update
   sudo apt install python3.10 python3.10-venv python3-pip
   sudo apt install build-essential libasound2-dev portaudio19-dev
   ```

2. **Install audio libraries**:
   ```bash
   sudo apt install libsndfile1 libsndfile1-dev
   ```

## Troubleshooting Installation

### Common Issues

#### 1. "No module named 'tkinter'"

**Solution**: Install tkinter (usually included with Python)
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# CentOS/RHEL
sudo yum install tkinter
```

#### 2. "Microsoft Visual C++ 14.0 is required"

**Solution**: Install Visual Studio Build Tools
- Download from [Microsoft](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- Install "C++ build tools" workload

#### 3. "Failed building wheel for numpy"

**Solution**: Update pip and install pre-compiled wheels
```bash
pip install --upgrade pip setuptools wheel
pip install numpy scipy
```

#### 4. Audio library errors

**Solution**: Install system audio libraries
```bash
# Ubuntu/Debian
sudo apt install libsndfile1 libsndfile1-dev libasound2-dev

# macOS
brew install libsndfile portaudio

# Windows
# Usually handled by conda or pre-compiled wheels
```

#### 5. Permission errors

**Solution**: Use virtual environments or install with --user flag
```bash
pip install --user -r requirements.txt
```

### Verification

After installation, verify everything works:

1. **Run tests**:
   ```bash
   pytest tests/
   ```

2. **Test demo files**:
   ```bash
   cd demo_files
   python create_simple_demo.py
   ```

3. **Launch GUI**:
   ```bash
   python src/main.py
   ```

## Uninstallation

To remove the application:

1. **Deactivate virtual environment** (if used)
2. **Remove the directory**:
   ```bash
   rm -rf notched-music  # Linux/macOS
   rmdir /s notched-music  # Windows
   ```

3. **Remove from pip** (if installed globally):
   ```bash
   pip uninstall notched-music
   ```

## Getting Help

If you encounter issues during installation:

1. Check the [troubleshooting section](#troubleshooting-installation)
2. Review the [README.md](../README.md) for common issues
3. Check the [GitHub Issues](https://github.com/username/notched-music/issues)
4. Create a new issue with:
   - Operating system and version
   - Python version
   - Complete error message
   - Steps to reproduce the issue

