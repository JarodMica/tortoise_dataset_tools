@echo off
setlocal enabledelayedexpansion

:: Check if Python 3.9 is installed
py -3.10 --version >nul 2>&1
if errorlevel 1 (
    echo Python 3.10 is not installed. Please install it and try again.
    pause
    exit /b 1
)

py -3.10 -m venv venv
call .\venv\Scripts\activate.bat

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install git+https://github.com/m-bain/whisperx.git
pip install -r requirements.txt

pause
