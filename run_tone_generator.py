#!/usr/bin/env python3
"""
Launcher script for the Tinnitus Frequency Identifier
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from tone_generator import main
    print("🎵 Starting Tinnitus Frequency Identifier...")
    print("📻 Vintage Stereo Style - Identify Your Tinnitus Frequency!")
    print()
    main()
except ImportError as e:
    print(f"❌ Error importing tinnitus identifier: {e}")
    print("💡 Make sure you're in the correct directory and all dependencies are installed.")
    print("   Run: pip install -r requirements.txt")
except Exception as e:
    print(f"❌ Error running tinnitus identifier: {e}")
    print("💡 Check that sounddevice is properly installed and audio drivers are working.")
