@echo off
REM Tinnitus Frequency Identifier Launcher
cd /d %~dp0
call venv\Scripts\activate.bat
python run_tone_generator.py
pause
