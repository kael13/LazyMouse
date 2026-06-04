import pystray
from PIL import Image, ImageDraw


def _create_icon(color):
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    margin = 6
    draw.ellipse(
        [margin, margin, size - margin, size - margin],
        fill=color,
        outline="white",
        width=2,
    )
    return img


ICON_ON = _create_icon("#22c55e")
ICON_OFF = _create_icon("#6b7280")


def run_tray(controller):
    icon = pystray.Icon(
        "lazymouse",
        ICON_OFF,
        "LazyMouse",
        menu=pystray.Menu(
            pystray.MenuItem("Toggle", lambda: _toggle(controller, icon)),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", lambda: _quit(controller, icon)),
        ),
    )
    icon.run()


def _toggle(controller, icon):
    controller.enabled = not controller.enabled
    icon.icon = ICON_ON if controller.enabled else ICON_OFF
    icon.title = f"LazyMouse {'ON' if controller.enabled else 'OFF'}"


def _quit(controller, icon):
    controller.running = False
    icon.stop()
