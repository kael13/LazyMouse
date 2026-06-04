# LazyMouse

**Your index finger has finally found its purpose.**

Tired of reaching for that mouse like some sort of *peasant*? LazyMouse hijacks your webcam, stalks your index finger, and turns it into a wireless cursor with benefits. Point at things. Tap the air like you're conducting a very tiny orchestra. Watch clicks happen. Never move your wrist again.

It uses MediaPipe, OpenCV, and PyAutoGUI to track your finger, smooth out the shakes, and detect downward taps as clicks — all without touching a single physical object.

### One-time setup (macOS / Linux)

```bash
./setup.sh
```

### One-time setup (Windows)

```powershell
conda create -n lazymouse python=3.12 -y
conda activate lazymouse
pip install opencv-python mediapipe pyautogui numpy
```

### Launch

```bash
./run.sh        # macOS / Linux
.\run.bat       # Windows (create this with: conda run -n lazymouse python main.py)
```

Or on any platform:
```bash
conda activate lazymouse && python main.py
```
