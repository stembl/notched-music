"""
Simple demo file creation without external dependencies.
Creates basic WAV files using only Python standard library.
"""

import wave
import struct
import math
import os
import shutil
from pathlib import Path


def create_tone_wav(filename, frequency, duration, sample_rate=44100, amplitude=0.5):
    """Create a WAV file with a pure tone."""
    num_samples = int(sample_rate * duration)
    
    # Generate audio data
    audio_data = []
    for i in range(num_samples):
        sample = amplitude * math.sin(2 * math.pi * frequency * i / sample_rate)
        audio_data.append(int(sample * 32767))  # Convert to 16-bit integer
    
    # Create WAV file
    with wave.open(str(filename), 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
        wav_file.setframerate(sample_rate)
        wav_file.setnframes(num_samples)
        
        # Write audio data
        for sample in audio_data:
            wav_file.writeframes(struct.pack('<h', sample))


def create_stereo_tone_wav(filename, left_freq, right_freq, duration, sample_rate=44100, amplitude=0.5):
    """Create a stereo WAV file with different frequencies in each channel."""
    num_samples = int(sample_rate * duration)
    
    # Generate audio data for both channels
    audio_data = []
    for i in range(num_samples):
        left_sample = amplitude * math.sin(2 * math.pi * left_freq * i / sample_rate)
        right_sample = amplitude * math.sin(2 * math.pi * right_freq * i / sample_rate)
        audio_data.append((int(left_sample * 32767), int(right_sample * 32767)))
    
    # Create WAV file
    with wave.open(str(filename), 'w') as wav_file:
        wav_file.setnchannels(2)  # Stereo
        wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
        wav_file.setframerate(sample_rate)
        wav_file.setnframes(num_samples)
        
        # Write audio data (interleaved stereo)
        for left_sample, right_sample in audio_data:
            wav_file.writeframes(struct.pack('<hh', left_sample, right_sample))


def create_demo_files():
    """Create demo audio files."""
    demo_dir = Path(__file__).parent
    demo_dir.mkdir(exist_ok=True)
    
    print("Creating simple demo audio files...")
    
    # 1. 440 Hz tone (A4 note)
    print("Creating 440 Hz tone...")
    create_tone_wav(demo_dir / "440hz_tone.wav", 440, 3.0)
    
    # 2. 1000 Hz tone (for notch filtering)
    print("Creating 1000 Hz tone...")
    create_tone_wav(demo_dir / "1000hz_tone.wav", 1000, 3.0)
    
    # 3. 2000 Hz tone
    print("Creating 2000 Hz tone...")
    create_tone_wav(demo_dir / "2000hz_tone.wav", 2000, 3.0)
    
    # 4. Stereo file with different frequencies
    print("Creating stereo file...")
    create_stereo_tone_wav(demo_dir / "stereo_test.wav", 440, 880, 3.0)
    
    # 5. Short test file
    print("Creating short test file...")
    create_tone_wav(demo_dir / "short_test.wav", 1000, 0.5)
    
    # 6. Low frequency tone
    print("Creating low frequency tone...")
    create_tone_wav(demo_dir / "low_freq_tone.wav", 100, 2.0)
    
    # 7. High frequency tone
    print("Creating high frequency tone...")
    create_tone_wav(demo_dir / "high_freq_tone.wav", 8000, 2.0)
    
    # Create additional formats for testing
    print("\nCreating additional formats...")
    wav_files = list(demo_dir.glob("*.wav"))
    
    # Create MP3 versions of some files (demo purposes - just copy with different extension)
    for i, wav_file in enumerate(wav_files[:3]):  # Convert first 3 files
        mp3_file = demo_dir / f"{wav_file.stem}.mp3"
        shutil.copy2(wav_file, mp3_file)
        print(f"Created {mp3_file.name} (demo format)")
    
    print(f"\nDemo files created in: {demo_dir}")
    print("Files created:")
    for file in demo_dir.glob("*"):
        if file.suffix.lower() in ['.wav', '.mp3', '.flac', '.aac', '.ogg', '.m4a']:
            print(f"  - {file.name}")


if __name__ == "__main__":
    create_demo_files()
