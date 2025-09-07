# User Guide

This guide provides detailed instructions for using the Notched Music application.

## Getting Started

### Launching the Application

1. **Start the application**:
   ```bash
   python src/main.py
   ```

2. **The main window will appear** with the following sections:
   - Input/Output directory selection
   - Notch frequency controls
   - Quality factor adjustment
   - Advanced options
   - Process button and progress indicators
   - Logging area

## Basic Usage

### Step 1: Select Input Directory

1. Click the **"Browse"** button next to "Input Directory"
2. Navigate to the folder containing your audio files
3. Select the folder and click "OK"
4. The path will appear in the input directory field

**Supported file formats**: WAV, MP3, FLAC, AAC, OGG, M4A

### Step 2: Select Output Directory

1. Click the **"Browse"** button next to "Output Directory"
2. Choose where you want to save the processed files
3. The application will create subdirectories to match the input structure

### Step 3: Set Notch Frequency

1. **Use the slider** to adjust the frequency (20 Hz to 20,000 Hz)
2. **Or type directly** in the frequency field
3. **Common frequencies**:
   - 50/60 Hz: Electrical hum
   - 1000 Hz: Test tone removal
   - 8000 Hz: Telephone quality artifacts

### Step 4: Adjust Quality Factor

1. **Use the slider** to adjust quality (1 to 100)
2. **Higher values** = sharper notch (affects fewer nearby frequencies)
3. **Lower values** = wider notch (affects more nearby frequencies)
4. **Recommended range**: 10-50 for most applications

### Step 5: Process Files

1. Click **"Process Audio Files"**
2. Watch the progress bar and log messages
3. Wait for completion notification

## Advanced Options

### Enabling Advanced Options

1. Check the **"Advanced Options"** checkbox
2. The advanced options panel will appear

### Metadata Modification

- **New Artist Name**: Changes the artist metadata for all processed files
- **New Album Name**: Changes the album metadata for all processed files
- **Leave blank** to preserve original metadata

## Understanding the Interface

### Main Controls

| Control | Description |
|---------|-------------|
| Input Directory | Source folder containing audio files |
| Output Directory | Destination folder for processed files |
| Notch Frequency | Frequency to remove (Hz) |
| Quality Factor | Sharpness of the notch filter |
| Advanced Options | Checkbox to show/hide metadata options |
| Process Button | Starts the audio processing |

### Status Indicators

- **Status Label**: Shows current operation status
- **Progress Bar**: Visual progress indicator
- **Log Area**: Detailed processing information

### Log Messages

The log area shows:
- File loading progress
- Filter application status
- File saving confirmation
- Error messages (if any)
- Processing completion summary

## Processing Workflow

### What Happens During Processing

1. **File Discovery**: Scans input directory for supported audio files
2. **Audio Loading**: Loads each file into memory
3. **Filter Application**: Applies notch filter to remove specified frequency
4. **Audio Saving**: Saves filtered audio to output directory
5. **Metadata Copying**: Preserves original metadata (with optional modifications)

### Processing Time

Processing time depends on:
- **File size**: Larger files take longer
- **Number of files**: Batch processing is sequential
- **Computer performance**: CPU and RAM speed
- **Audio format**: WAV files process faster than compressed formats

**Typical processing times**:
- 1-minute WAV file: 2-5 seconds
- 1-minute MP3 file: 5-10 seconds
- 10 files (1 minute each): 30-60 seconds

## Best Practices

### Input Preparation

1. **Organize files**: Keep audio files in organized folders
2. **Backup originals**: Always keep copies of original files
3. **Check formats**: Ensure files are in supported formats
4. **Test first**: Process a small batch before large operations

### Frequency Selection

1. **Identify the problem**: Use audio analysis tools to find unwanted frequencies
2. **Start conservative**: Use lower quality factors initially
3. **Test results**: Listen to processed files before batch processing
4. **Document settings**: Note successful frequency/quality combinations

### Quality Factor Guidelines

| Quality Factor | Use Case | Effect |
|----------------|----------|---------|
| 1-10 | Wide noise removal | Affects many nearby frequencies |
| 10-30 | General purpose | Good balance of precision and safety |
| 30-50 | Precise removal | Minimal effect on nearby frequencies |
| 50-100 | Very precise | Very sharp notch, may cause artifacts |

### Output Management

1. **Organize output**: Use descriptive folder names
2. **Check results**: Verify processed files sound correct
3. **Archive originals**: Move original files to archive folders
4. **Document changes**: Keep notes of processing parameters

## Troubleshooting

### Common Issues

#### "Input directory does not exist"
- **Cause**: Invalid or non-existent path
- **Solution**: Use the Browse button to select a valid directory

#### "No audio files found"
- **Cause**: Directory contains no supported audio files
- **Solution**: Check file formats and directory contents

#### "Error during processing"
- **Cause**: Various issues (file corruption, permissions, etc.)
- **Solution**: Check log messages for specific error details

#### "GUI not responding"
- **Cause**: Processing is running in background
- **Solution**: Wait for processing to complete, check log for progress

### Performance Issues

#### Slow Processing
- **Reduce batch size**: Process fewer files at once
- **Use WAV format**: Faster than compressed formats
- **Close other applications**: Free up system resources
- **Check disk space**: Ensure sufficient free space

#### Memory Issues
- **Process smaller batches**: Reduce memory usage
- **Use shorter files**: Less memory per file
- **Increase system RAM**: Add more memory if possible

### Audio Quality Issues

#### Artifacts in Output
- **Reduce quality factor**: Use lower values (10-30)
- **Check notch frequency**: Ensure correct frequency
- **Test with different settings**: Experiment with parameters

#### Incomplete Frequency Removal
- **Increase quality factor**: Use higher values (30-50)
- **Verify frequency**: Double-check the notch frequency setting
- **Check audio analysis**: Use spectrum analyzer to verify results

## Tips and Tricks

### Efficient Workflow

1. **Test with demo files**: Use provided demo files to test settings
2. **Create presets**: Document successful parameter combinations
3. **Batch similar files**: Group files with similar characteristics
4. **Use descriptive names**: Name output folders clearly

### Advanced Techniques

1. **Multiple passes**: Process files multiple times with different frequencies
2. **Frequency analysis**: Use external tools to identify problem frequencies
3. **Quality comparison**: A/B test different quality factors
4. **Metadata management**: Use advanced options for consistent metadata

### File Organization

```
Project/
├── Original/          # Original audio files
├── Processed/          # Notch-filtered files
├── Archive/           # Backup of originals
└── Settings/          # Documented processing parameters
```

## Getting Help

### Resources

1. **README.md**: Basic information and troubleshooting
2. **Demo files**: Test files in the demo_files directory
3. **Log messages**: Detailed processing information
4. **GitHub Issues**: Community support and bug reports

### Reporting Issues

When reporting problems, include:
- Operating system and version
- Python version
- Complete error messages
- Steps to reproduce the issue
- Sample audio files (if applicable)
- Processing parameters used

