#!/bin/bash
# ========================================
# Notched Music - Activate Virtual Environment (Linux/macOS)
# ========================================

# Change to script directory
cd "$(dirname "$0")"

echo ""
echo "========================================"
echo "Notched Music - Activating Virtual Environment"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found."
    echo ""
    echo "Please run the setup script first:"
    echo "  ./setup_venv.sh"
    echo ""
    exit 1
else
    echo "✅ Virtual environment found."
fi

echo "Activating virtual environment..."
source venv/bin/activate

# Show Python version
echo ""
echo "Python version in virtual environment:"
python --version
echo ""

# Check if packages are installed
echo "Checking installed packages..."
if python -c "import numpy, scipy, librosa, soundfile, mutagen; print('✅ Core audio packages available')" 2>/dev/null; then
    echo "✅ Audio processing packages ready"
else
    echo "⚠️  Some audio packages may not be installed"
    echo "Run: pip install -r requirements.txt"
fi

echo ""
echo "========================================"
echo "✅ Notched Music environment ready!"
echo "========================================"
echo ""
echo "Available commands:"
echo "  python src/main.py          - Run the GUI application"
echo "  python run_tests.py         - Run test suite"
echo "  python run_demo.py          - Run interactive demo"
echo "  python install_dependencies.py - Install/update dependencies"
echo ""
echo "To deactivate: deactivate"
echo ""
