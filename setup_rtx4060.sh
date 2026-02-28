#!/bin/bash
# Quick Start Script for LTX-Video on RTX4060 8GB GPU (Linux/Mac)

echo "================================================"
echo "LTX-Video Setup for RTX4060 8GB GPU"
echo "================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "env" ]; then
    echo "Creating virtual environment..."
    python3 -m venv env
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment"
        echo "Please ensure Python 3.10+ is installed"
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source env/bin/activate

# Check if dependencies are installed
if ! python -c "import ltx_video" 2>/dev/null; then
    echo "Installing dependencies..."
    echo "This may take several minutes..."
    pip install -e .[inference]
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies"
        exit 1
    fi
else
    echo "Dependencies already installed ✓"
fi

# Check CUDA availability
echo ""
echo "Checking GPU availability..."
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"None\"}')"

echo ""
echo "================================================"
echo "Setup complete!"
echo "================================================"
echo ""
echo "Quick Start Examples:"
echo ""
echo "1. Text-to-video:"
echo "   python run_local_rtx4060.py --prompt \"A cat playing with a ball\""
echo ""
echo "2. Image-to-video:"
echo "   python run_local_rtx4060.py --prompt \"Landscape in motion\" --image your_image.jpg"
echo ""
echo "3. Custom settings:"
echo "   python run_local_rtx4060.py --prompt \"Ocean waves\" --width 640 --height 384 --frames 65"
echo ""
echo "For more information, see RTX4060_SETUP.md"
echo ""
