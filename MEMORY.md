# LazyMouse

A hand-tracking mouse controller using webcam + MediaPipe + PyAutoGUI.  
Point your index finger to move the cursor; tap downward to click.

---

## Quick Start

```bash
./setup.sh   # one-time install (Conda env + model)
./run.sh     # launch
```

---

## File Map

| File | Purpose |
|---|---|
| `main.py` | Entry point |
| `hand_controller.py` | Core tracking, filtering, click detection |
| `config.py` | Tunable parameters |
| `requirements.txt` | Python dependencies |
| `setup.sh` | One-time environment setup |
| `run.sh` | Launch script via Conda |
| `.gitignore` | Ignores `.miniforge3/`, `venv/`, `__pycache__/` |

---

## Architecture

```
main.py
  └─ HandController (hand_controller.py)
       ├─ MediaPipe Hands → index finger tip (landmark 8)
       ├─ ROI clamp + normalise → screen coordinates
       ├─ 1€ filter (adaptive smoothing)
       ├─ Deadzone lock (sticky cursor when holding still)
       ├─ Tap detection (downward velocity → click)
       └─ pyautogui.moveTo / pyautogui.click
```

### Deadzone (Sticky Cursor)
When the finger holds still within `DEADZONE_RADIUS` for `DEADZONE_FRAMES` consecutive frames, the cursor locks in place. This eliminates jitter while aiming, giving you a steady target to tap on.

### Tap-to-Click Flow
1. Finger moves down fast → `TAP_DOWN_THRESHOLD` → arm click
2. Finger slows/stops → `TAP_RELEASE_THRESHOLD` → fire click
3. `CLICK_COOLDOWN` prevents double-clicks

---

## Config (`config.py`)

| Parameter | Default | Description |
|---|---|---|
| `ONE_EURO_ENABLED` | `True` | Use 1€ adaptive filter |
| `MIN_CUTOFF` | `0.6` | Smoothness when hand is still (Hz) |
| `BETA` | `2.0` | Responsiveness during fast movement |
| `DCUTOFF` | `1.0` | Derivative cutoff (Hz) |
| `SMOOTHING_FACTOR` | `0.35` | Fallback EMA smoothing factor |
| `TAP_DOWN_THRESHOLD` | `0.025` | Velocity to arm a click |
| `TAP_RELEASE_THRESHOLD` | `0.010` | Velocity to fire the click |
| `CLICK_COOLDOWN` | `0.3` | Debounce between clicks (s) |
| `DEADZONE_RADIUS` | `0.012` | Normalized distance to trigger cursor lock |
| `DEADZONE_FRAMES` | `8` | Consecutive still frames before lock |
| `ROI_MARGIN` | `0.1` | Fraction cropped from frame edges |
| `CAMERA_INDEX` | `0` | Webcam device index |
| `FRAME_WIDTH/HEIGHT` | `640×480` | Capture resolution |
| `MAX_FPS` | `60` | Camera FPS target |

---

## Recent Changes (Jun 4)

- `config.py` & `hand_controller.py` — latest edits (18:52)
- `setup.sh` & `run.sh` — created (18:39)
- Initial scaffold: `main.py`, `requirements.txt`, `.gitignore` (18:13)
- No git repo — changes are untracked
