#!/usr/bin/env python3
"""
Demo runner script for the Notched Music project.
This script demonstrates the application with sample files.
"""

import os
import sys
import subprocess
from pathlib import Path
import tempfile
import shutil


def create_demo_environment():
    """Create a demo environment with sample files."""
    print("Setting up demo environment...")
    
    # Create temporary directories
    demo_dir = Path("demo_run")
    input_dir = demo_dir / "input"
    output_dir = demo_dir / "output"
    
    # Clean up any existing demo directory
    if demo_dir.exists():
        shutil.rmtree(demo_dir)
    
    # Create directories
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy demo files to input directory
    demo_files_dir = Path("demo_files")
    if demo_files_dir.exists():
        # Supported audio formats from AudioProcessor
        supported_formats = {'.wav', '.mp3', '.flac', '.aac', '.ogg', '.m4a'}
        
        copied_count = 0
        for audio_file in demo_files_dir.iterdir():
            if audio_file.is_file() and audio_file.suffix.lower() in supported_formats:
                shutil.copy2(audio_file, input_dir)
                print(f"Copied {audio_file.name} to input directory")
                copied_count += 1
        
        if copied_count == 0:
            print("No supported audio files found in demo_files directory")
        else:
            print(f"Copied {copied_count} audio file(s) to input directory")
    
    print(f"Demo environment created:")
    print(f"  Input directory: {input_dir.absolute()}")
    print(f"  Output directory: {output_dir.absolute()}")
    
    return input_dir, output_dir


def run_audio_processing_demo():
    """Run a command-line demo of the audio processing."""
    print("\n" + "="*60)
    print("COMMAND-LINE AUDIO PROCESSING DEMO")
    print("="*60)
    
    # Create demo environment
    input_dir, output_dir = create_demo_environment()
    
    # Import and use the audio processor
    try:
        sys.path.insert(0, str(Path("src")))
        from audio_processor import AudioProcessor
        
        # Create processor with 1000 Hz notch filter
        processor = AudioProcessor(notch_frequency=1000.0, quality_factor=30.0)
        
        print(f"\nProcessing files from: {input_dir}")
        print(f"Saving to: {output_dir}")
        print(f"Notch frequency: 1000 Hz")
        print(f"Quality factor: 30")
        
        # Process files
        processed_files = processor.process_directory(
            str(input_dir),
            str(output_dir),
            new_artist="Demo Artist",
            new_album="Notched Music Demo"
        )
        
        print(f"\nProcessing complete!")
        print(f"Files processed: {len(processed_files)}")
        
        # List output files
        print(f"\nOutput files:")
        for file in output_dir.glob("*.wav"):
            size_kb = file.stat().st_size / 1024
            print(f"  {file.name} ({size_kb:.1f} KB)")
        
        return True
        
    except Exception as e:
        print(f"Error during processing: {e}")
        return False


def run_gui_demo():
    """Run the GUI application."""
    print("\n" + "="*60)
    print("GUI APPLICATION DEMO")
    print("="*60)
    
    print("Launching GUI application...")
    print("In the GUI:")
    print("1. Set input directory to: demo_run/input")
    print("2. Set output directory to: demo_run/output")
    print("3. Set notch frequency to: 1000 Hz")
    print("4. Set quality factor to: 30")
    print("5. Enable advanced options and set artist/album names")
    print("6. Click 'Process Audio Files'")
    
    try:
        # Launch GUI
        subprocess.run([sys.executable, "src/main.py"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error launching GUI: {e}")
        return False
    except KeyboardInterrupt:
        print("\nGUI demo interrupted by user")
        return True


def cleanup_demo():
    """Clean up demo files."""
    demo_dir = Path("demo_run")
    if demo_dir.exists():
        cleanup = input(f"\nClean up demo files in {demo_dir}? (y/n): ").lower().strip()
        if cleanup in ['y', 'yes']:
            shutil.rmtree(demo_dir)
            print("Demo files cleaned up")
        else:
            print(f"Demo files preserved in {demo_dir}")


def main():
    """Main demo function."""
    print("Notched Music - Demo Runner")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("src").exists() or not Path("demo_files").exists():
        print("ERROR: Please run this script from the project root directory")
        print("Expected structure:")
        print("  notched_music/")
        print("    ├── src/")
        print("    ├── demo_files/")
        print("    └── run_demo.py")
        sys.exit(1)
    
    print("This demo will:")
    print("1. Create sample audio files")
    print("2. Demonstrate command-line processing")
    print("3. Launch the GUI application")
    print("4. Show you how to use the application")
    
    proceed = input("\nProceed with demo? (y/n): ").lower().strip()
    if proceed not in ['y', 'yes']:
        print("Demo cancelled")
        return 0
    
    # Run command-line demo
    if not run_audio_processing_demo():
        print("Command-line demo failed")
        return 1
    
    # Ask about GUI demo
    gui_demo = input("\nLaunch GUI demo? (y/n): ").lower().strip()
    if gui_demo in ['y', 'yes']:
        if not run_gui_demo():
            print("GUI demo failed")
            return 1
    
    # Cleanup
    cleanup_demo()
    
    print(f"\n{'='*60}")
    print("DEMO COMPLETE!")
    print(f"{'='*60}")
    print("You can now:")
    print("  - Run the application: python src/main.py")
    print("  - Run tests: python run_tests.py")
    print("  - Process your own audio files")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
