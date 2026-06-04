import pyautogui

try:
    SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
except Exception:
    SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080

CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
ROI_MARGIN = 0.1
SMOOTHING_FACTOR = 0.35  # EMA fallback (used if ONE_EURO disabled)
ONE_EURO_ENABLED = True
MIN_CUTOFF = 0.6        # Hz — lower = smoother when still
BETA = 2.0              # more = less smoothing during fast movement
DCUTOFF = 1.0           # derivative cutoff
MAX_FPS = 60
CLICK_COOLDOWN = 0.3
TAP_DOWN_THRESHOLD = 0.025
TAP_RELEASE_THRESHOLD = 0.010
DEADZONE_RADIUS = 0.012
DEADZONE_FRAMES = 8
