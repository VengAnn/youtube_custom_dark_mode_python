#!/bin/bash
# run project : bash run.sh

# Ensure script halts on error
set -e

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies if requirements.txt changed or it's a fresh install
if [ ! -f "venv/.installed" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    touch venv/.installed
fi

# Run the application
echo "Starting YouTube Custom Theme Manager..."
python3 main.py
