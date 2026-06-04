import threading

from hand_controller import HandController

try:
    from tray_icon import run_tray

    HAS_TRAY = True
except ImportError:
    HAS_TRAY = False


if __name__ == "__main__":
    controller = HandController()

    if HAS_TRAY:
        t = threading.Thread(target=run_tray, args=(controller,), daemon=True)
        t.start()
    else:
        print("System tray not available — install pystray + Pillow for tray support.")

    controller.start()
