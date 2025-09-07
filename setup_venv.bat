@echo off
REM ========================================
REM Notched Music - Virtual Environment Setup
REM ========================================

REM Change directory to the script location
cd /d %~dp0

echo.
echo ========================================
echo Notched Music - Virtual Environment Setup
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo Python version:
python --version
echo.

REM Create the virtual environment in a "venv" folder
echo Creating virtual environment...
python -m venv venv

REM Check if venv creation succeeded
if exist venv\Scripts\activate.bat (
    echo ✅ Virtual environment created successfully.
    echo.

    REM Activate the virtual environment
    echo Activating the virtual environment...
    call venv\Scripts\activate.bat
    echo.

    REM Upgrade pip
    echo Upgrading pip...
    python -m pip install --upgrade pip
    echo.

    REM Install required packages from requirements.txt if it exists
    if exist requirements.txt (
        echo Installing packages from requirements.txt...
        pip install -r requirements.txt
        echo.
    ) else (
        echo WARNING: No requirements.txt found. Skipping package installation.
        echo.
    )

    REM Install the package in development mode
    echo Installing Notched Music package in development mode...
    pip install -e .
    echo.

    REM Verify installation
    echo Verifying installation...
    python -c "import sys; sys.path.insert(0, 'src'); from audio_processor import AudioProcessor; print('✅ Audio processor imports successfully')" 2>nul
    if errorlevel 1 (
        echo ⚠️  Some dependencies may not be installed correctly
        echo You can run: python install_dependencies.py
    ) else (
        echo ✅ Core components verified
    )
    echo.

    REM Show final status
    echo ========================================
    echo Virtual environment is ready!
    echo ========================================
    echo.
    echo To activate the environment manually:
    echo   call venv\Scripts\activate.bat
    echo.
    echo To run the application:
    echo   python src\main.py
    echo.
    echo To run tests:
    echo   python run_tests.py
    echo.
    echo To run demo:
    echo   python run_demo.py
    echo.
    pause
) else (
    echo ❌ Failed to create virtual environment.
    echo Please check your Python installation and try again.
    pause
    exit /b 1
)
