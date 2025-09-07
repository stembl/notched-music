@echo off
REM Notched Music - Activate Virtual Environment

REM Change directory to the script location
cd /d %~dp0

REM Check if virtual environment exists, create if missing
if not exist "venv" (
    python -m venv venv >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Always check and install requirements
if exist "requirements.txt" (
    pip install -r requirements.txt >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Failed to install requirements
        exit /b 1
    )
)