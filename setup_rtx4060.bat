@echo off
REM Quick Start Script for LTX-Video on RTX4060 8GB GPU (Windows)

echo ================================================
echo LTX-Video Setup for RTX4060 8GB GPU
echo ================================================
echo.

REM Check if virtual environment exists
if not exist "env\" (
    echo Creating virtual environment...
    python -m venv env
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        echo Please ensure Python 3.10+ is installed
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call env\Scripts\activate.bat

REM Check if dependencies are installed
python -c "import ltx_video" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    echo This may take several minutes...
    pip install -e .[inference]
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
) else (
    echo Dependencies already installed [OK]
)

REM Check CUDA availability
echo.
echo Checking GPU availability...
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"None\"}')"

echo.
echo ================================================
echo Setup complete!
echo ================================================
echo.
echo Quick Start Examples:
echo.
echo 1. Text-to-video:
echo    python run_local_rtx4060.py --prompt "A cat playing with a ball"
echo.
echo 2. Image-to-video:
echo    python run_local_rtx4060.py --prompt "Landscape in motion" --image your_image.jpg
echo.
echo 3. Custom settings:
echo    python run_local_rtx4060.py --prompt "Ocean waves" --width 640 --height 384 --frames 65
echo.
echo For more information, see RTX4060_SETUP.md
echo.
pause
