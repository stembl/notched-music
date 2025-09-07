#!/usr/bin/env python3
"""
Dependency installation script for Notched Music.
This script installs all required dependencies for the project.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"Installing: {description}")
    print(f"Command: {command}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing {description}: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"ERROR: Python 3.8+ is required. Current version: {version.major}.{version.minor}")
        return False
    print(f"Python version: {version.major}.{version.minor}.{version.micro} ✅")
    return True


def upgrade_pip():
    """Upgrade pip to latest version."""
    return run_command(
        f"{sys.executable} -m pip install --upgrade pip",
        "Upgrading pip"
    )


def install_requirements():
    """Install requirements from requirements.txt."""
    project_root = Path(__file__).parent
    requirements_file = project_root / "requirements.txt"
    
    if not requirements_file.exists():
        print(f"ERROR: requirements.txt not found at {requirements_file}")
        return False
    
    return run_command(
        f"{sys.executable} -m pip install -r {requirements_file}",
        "Core dependencies from requirements.txt"
    )


def install_dev_dependencies():
    """Install development dependencies."""
    dev_deps = [
        "pytest>=6.2.0",
        "pytest-cov>=2.12.0",
        "black>=21.0.0",
        "flake8>=3.9.0",
        "mypy>=0.910"
    ]
    
    success = True
    for dep in dev_deps:
        if not run_command(f"{sys.executable} -m pip install {dep}", f"Development dependency: {dep}"):
            success = False
    
    return success


def install_package():
    """Install the package in development mode."""
    return run_command(
        f"{sys.executable} -m pip install -e .",
        "Notched Music package (development mode)"
    )


def verify_installation():
    """Verify that key packages are installed."""
    print(f"\n{'='*60}")
    print("VERIFICATION")
    print(f"{'='*60}")
    
    packages_to_check = [
        "numpy",
        "scipy", 
        "librosa",
        "soundfile",
        "mutagen",
        "Pillow",
        "matplotlib",
        "pytest"
    ]
    
    success = True
    for package in packages_to_check:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NOT INSTALLED")
            success = False
    
    return success


def main():
    """Main installation function."""
    print("Notched Music - Dependency Installation")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Upgrade pip
    if not upgrade_pip():
        print("WARNING: Failed to upgrade pip, continuing anyway...")
    
    # Install core dependencies
    if not install_requirements():
        print("ERROR: Failed to install core dependencies")
        sys.exit(1)
    
    # Install development dependencies
    install_dev = input("\nInstall development dependencies? (y/n): ").lower().strip()
    if install_dev in ['y', 'yes']:
        if not install_dev_dependencies():
            print("WARNING: Some development dependencies failed to install")
    
    # Install package in development mode
    if not install_package():
        print("ERROR: Failed to install package")
        sys.exit(1)
    
    # Verify installation
    if not verify_installation():
        print("ERROR: Installation verification failed")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print("INSTALLATION COMPLETE!")
    print(f"{'='*60}")
    print("You can now run the application with:")
    print("  python src/main.py")
    print("\nOr run tests with:")
    print("  python run_tests.py")
    print("\nOr use pytest directly:")
    print("  pytest tests/")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
