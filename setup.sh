#!/bin/bash
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== LazyMouse Setup ==="

# Install Miniforge if not present
if [ ! -f "$DIR/.miniforge3/bin/mamba" ]; then
    echo "Downloading Miniforge..."
    curl -L -o /tmp/miniforge.sh "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
    bash /tmp/miniforge.sh -b -p "$DIR/.miniforge3"
    rm /tmp/miniforge.sh
fi

export PATH="$DIR/.miniforge3/bin:$PATH"

echo "Creating conda environment (Python 3.12)..."
mamba create -n lazymouse -y python=3.12 opencv pyautogui numpy pip

echo "Installing mediapipe..."
"$DIR/.miniforge3/envs/lazymouse/bin/pip" install "mediapipe==0.10.21"

echo "Downloading hand landmarker model..."
curl -L -o "$DIR/.miniforge3/envs/lazymouse/lib/python3.12/site-packages/mediapipe/hand_landmarker.task" \
    "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task"

echo ""
echo "Setup complete! Run ./run.sh to start LazyMouse."
echo ""
echo "NOTE on macOS: Grant permissions when prompted:"
echo "  - System Settings > Privacy & Security > Camera"
echo "  - System Settings > Privacy & Security > Accessibility"
