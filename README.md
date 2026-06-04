# LazyMouse

**Your index finger has finally found its purpose.**

Tired of reaching for that mouse like some sort of *peasant*? LazyMouse hijacks your webcam, stalks your index finger, and turns it into a wireless cursor with benefits. Point at things. Tap the air like you're conducting a very tiny orchestra. Watch clicks happen. Never move your wrist again.

It uses MediaPipe, OpenCV, and PyAutoGUI to track your finger, smooth out the shakes, and detect downward taps as clicks — all without touching a single physical object.

### System tray

A tray icon appears in your menu bar (macOS) or system tray (Windows) when LazyMouse runs.

- **Green circle** = tracking is ON
- **Gray circle** = tracking is OFF
- **Toggle** — pause/resume tracking without quitting
- **Quit** — exit the app

### One-time setup (macOS / Linux)

```bash
./setup.sh
.miniforge3/envs/lazymouse/bin/pip install pystray Pillow
```

### One-time setup (Windows)

```powershell
conda create -n lazymouse python=3.12 -y
conda activate lazymouse
pip install opencv-python mediapipe pyautogui numpy pystray Pillow
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
