@echo off
REM ========================================
REM Notched Music - Virtual Environment Setup (Python 3.11)
REM ========================================

REM Change directory to the script location
cd /d %~dp0

echo.
echo ========================================
echo Notched Music - Virtual Environment Setup (Python 3.11)
echo ========================================
echo.

REM Set your Python 3.11 executable path
set PYTHON_EXE=C:\tools\Python311\python.exe

REM Check if Python 3.11 is available
%PYTHON_EXE% --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3.11 not found at %PYTHON_EXE%
    echo Please update the PYTHON_EXE path in this script
    echo or use setup_venv.bat for default Python installation
    pause
    exit /b 1
)

echo Python 3.11 version:
%PYTHON_EXE% --version
echo.

REM Create the virtual environment in a "venv" folder
echo Creating virtual environment with Python 3.11...
%PYTHON_EXE% -m venv venv

REM Check if venv creation succeeded
if exist venv\Scripts\activate.bat (
    echo ✅ Virtual environment created successfully with Python 3.11.
    echo.

    REM Activate the virtual environment
    echo Activating the virtual environment...
    call venv\Scripts\activate.bat
    echo.

    REM Show Python version in venv
    echo Python version in virtual environment:
    python --version
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
    echo Please check your Python 3.11 installation and try again.
    pause
    exit /b 1
)
