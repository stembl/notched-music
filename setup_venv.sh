#!/bin/bash
# ========================================
# Notched Music - Virtual Environment Setup (Linux/macOS)
# ========================================

# Change to script directory
cd "$(dirname "$0")"

echo ""
echo "========================================"
echo "Notched Music - Virtual Environment Setup"
echo "========================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

echo "Python version:"
python3 --version
echo ""

# Create the virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Check if venv creation succeeded
if [ -f "venv/bin/activate" ]; then
    echo "✅ Virtual environment created successfully."
    echo ""

    # Activate the virtual environment
    echo "Activating the virtual environment..."
    source venv/bin/activate
    echo ""

    # Upgrade pip
    echo "Upgrading pip..."
    python -m pip install --upgrade pip
    echo ""

    # Install required packages from requirements.txt if it exists
    if [ -f "requirements.txt" ]; then
        echo "Installing packages from requirements.txt..."
        pip install -r requirements.txt
        echo ""
    else
        echo "WARNING: No requirements.txt found. Skipping package installation."
        echo ""
    fi

    # Install the package in development mode
    echo "Installing Notched Music package in development mode..."
    pip install -e .
    echo ""

    # Verify installation
    echo "Verifying installation..."
    if python -c "import sys; sys.path.insert(0, 'src'); from audio_processor import AudioProcessor; print('✅ Audio processor imports successfully')" 2>/dev/null; then
        echo "✅ Core components verified"
    else
        echo "⚠️  Some dependencies may not be installed correctly"
        echo "You can run: python install_dependencies.py"
    fi
    echo ""

    # Show final status
    echo "========================================"
    echo "Virtual environment is ready!"
    echo "========================================"
    echo ""
    echo "To activate the environment manually:"
    echo "  source venv/bin/activate"
    echo ""
    echo "To run the application:"
    echo "  python src/main.py"
    echo ""
    echo "To run tests:"
    echo "  python run_tests.py"
    echo ""
    echo "To run demo:"
    echo "  python run_demo.py"
    echo ""
else
    echo "❌ Failed to create virtual environment."
    echo "Please check your Python installation and try again."
    exit 1
fi
