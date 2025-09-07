"""
Script to generate demo audio files for testing the Notched Music application.
"""

import numpy as np
import soundfile as sf
import os
from pathlib import Path


def generate_tone(frequency, duration, sample_rate=44100, amplitude=0.5):
    """Generate a pure tone."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    return amplitude * np.sin(2 * np.pi * frequency * t)


def generate_chord(frequencies, duration, sample_rate=44100, amplitude=0.3):
    """Generate a chord from multiple frequencies."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    signal = np.zeros_like(t)
    for freq in frequencies:
        signal += amplitude * np.sin(2 * np.pi * freq * t)
    return signal


def generate_noise_with_tone(noise_freq, duration, sample_rate=44100, noise_level=0.1):
    """Generate noise with a specific frequency component."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Generate white noise
    noise = np.random.normal(0, noise_level, len(t))
    
    # Add specific frequency component
    tone = 0.5 * np.sin(2 * np.pi * noise_freq * t)
    
    return noise + tone


def create_demo_files():
    """Create demo audio files for testing."""
    demo_dir = Path(__file__).parent
    demo_dir.mkdir(exist_ok=True)
    
    sample_rate = 44100
    
    print("Generating demo audio files...")
    
    # 1. Simple 440 Hz tone (A4 note)
    print("Creating 440 Hz tone...")
    tone_440 = generate_tone(440, 3.0, sample_rate)
    sf.write(demo_dir / "440hz_tone.wav", tone_440, sample_rate)
    
    # 2. Simple 1000 Hz tone (for notch filtering)
    print("Creating 1000 Hz tone...")
    tone_1000 = generate_tone(1000, 3.0, sample_rate)
    sf.write(demo_dir / "1000hz_tone.wav", tone_1000, sample_rate)
    
    # 3. Chord with multiple frequencies
    print("Creating chord...")
    chord = generate_chord([440, 554, 659, 880], 4.0, sample_rate)  # A major chord
    sf.write(demo_dir / "a_major_chord.wav", chord, sample_rate)
    
    # 4. Noise with 1000 Hz component (perfect for notch filtering demo)
    print("Creating noise with 1000 Hz component...")
    noisy_signal = generate_noise_with_tone(1000, 5.0, sample_rate, noise_level=0.2)
    sf.write(demo_dir / "noise_with_1000hz.wav", noisy_signal, sample_rate)
    
    # 5. Stereo file with different frequencies in each channel
    print("Creating stereo file...")
    left_channel = generate_tone(440, 3.0, sample_rate)  # A4
    right_channel = generate_tone(880, 3.0, sample_rate)  # A5
    stereo_signal = np.array([left_channel, right_channel])
    sf.write(demo_dir / "stereo_test.wav", stereo_signal.T, sample_rate)
    
    # 6. Complex signal with multiple frequencies including 1000 Hz
    print("Creating complex signal...")
    complex_signal = (generate_tone(200, 3.0, sample_rate, 0.3) +
                     generate_tone(500, 3.0, sample_rate, 0.3) +
                     generate_tone(1000, 3.0, sample_rate, 0.4) +
                     generate_tone(2000, 3.0, sample_rate, 0.3) +
                     generate_tone(4000, 3.0, sample_rate, 0.2))
    sf.write(demo_dir / "complex_signal.wav", complex_signal, sample_rate)
    
    # 7. Short test file for quick testing
    print("Creating short test file...")
    short_signal = generate_tone(1000, 0.5, sample_rate)
    sf.write(demo_dir / "short_test.wav", short_signal, sample_rate)
    
    # 8. File with metadata (we'll create a simple WAV and add metadata later)
    print("Creating file for metadata testing...")
    metadata_signal = generate_tone(440, 2.0, sample_rate)
    sf.write(demo_dir / "metadata_test.wav", metadata_signal, sample_rate)
    
    # Create additional formats for testing (if dependencies are available)
    try:
        import librosa
        print("\nCreating additional formats...")
        
        # Convert some files to MP3 format (requires ffmpeg)
        wav_files = list(demo_dir.glob("*.wav"))
        for i, wav_file in enumerate(wav_files[:3]):  # Convert first 3 files
            mp3_file = demo_dir / f"{wav_file.stem}.mp3"
            try:
                # Load and save as MP3 (this will create a WAV file with MP3 extension for demo purposes)
                audio_data, sr = librosa.load(str(wav_file), sr=None)
                # Note: In a real implementation, you'd use ffmpeg or similar to create actual MP3
                # For demo purposes, we'll just copy the WAV file with MP3 extension
                import shutil
                shutil.copy2(wav_file, mp3_file)
                print(f"Created {mp3_file.name} (demo format)")
            except Exception as e:
                print(f"Could not create {mp3_file.name}: {e}")
                
    except ImportError:
        print("Librosa not available - skipping additional format creation")
    
    print(f"\nDemo files created in: {demo_dir}")
    print("Files created:")
    for file in demo_dir.glob("*"):
        if file.suffix.lower() in ['.wav', '.mp3', '.flac', '.aac', '.ogg', '.m4a']:
            print(f"  - {file.name}")


if __name__ == "__main__":
    create_demo_files()

