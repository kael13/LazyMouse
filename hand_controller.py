import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time
import math
import sys

from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, CAMERA_INDEX,
    FRAME_WIDTH, FRAME_HEIGHT, ROI_MARGIN,
    SMOOTHING_FACTOR, ONE_EURO_ENABLED, MIN_CUTOFF, BETA, DCUTOFF,
    MAX_FPS, CLICK_COOLDOWN,
    TAP_DOWN_THRESHOLD, TAP_RELEASE_THRESHOLD,
)

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0


class HandController:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5,
        )
        self.cap = cv2.VideoCapture(CAMERA_INDEX)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, MAX_FPS)

        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            sys.exit(1)

        self.prev_click_time = 0
        self._prev_y = 0.5
        self._tap_armed = False
        self._filt_x = 0.5
        self._filt_y = 0.5
        self._dx_filt = 0.0
        self._dy_filt = 0.0
        self._last_time = 0.0
        self._roi_min = ROI_MARGIN
        self._roi_max = 1.0 - ROI_MARGIN
        self._roi_range = 1.0 - 2 * ROI_MARGIN
        self.enabled = True
        self.running = True

    def _norm_to_screen(self, nx, ny):
        return int((nx - self._roi_min) / self._roi_range * SCREEN_WIDTH), \
               int((ny - self._roi_min) / self._roi_range * SCREEN_HEIGHT)

    def _filter(self, raw_nx, raw_ny):
        now = time.time()
        dt = now - self._last_time
        self._last_time = now

        if dt <= 0 or dt > 0.1:
            self._filt_x, self._filt_y = raw_nx, raw_ny
            self._dx_filt, self._dy_filt = 0.0, 0.0
            return self._norm_to_screen(raw_nx, raw_ny)

        if ONE_EURO_ENABLED:
            dx = (raw_nx - self._filt_x) / dt
            dy = (raw_ny - self._filt_y) / dt

            tau = 1.0 / (2 * math.pi * DCUTOFF)
            a = dt / (dt + tau)
            self._dx_filt += (dx - self._dx_filt) * a
            self._dy_filt += (dy - self._dy_filt) * a

            fc_x = MIN_CUTOFF + BETA * abs(self._dx_filt)
            fc_y = MIN_CUTOFF + BETA * abs(self._dy_filt)

            alpha_x = 1.0 / (1.0 + dt * 2 * math.pi * fc_x)

            alpha_y = 1.0 / (1.0 + dt * 2 * math.pi * fc_y)
            self._filt_x += (raw_nx - self._filt_x) * (1 - alpha_x)
            self._filt_y += (raw_ny - self._filt_y) * (1 - alpha_y)
        else:
            self._filt_x = self._filt_x * SMOOTHING_FACTOR + raw_nx * (1 - SMOOTHING_FACTOR)
            self._filt_y = self._filt_y * SMOOTHING_FACTOR + raw_ny * (1 - SMOOTHING_FACTOR)

        return self._norm_to_screen(self._filt_x, self._filt_y)

    def _detect_tap(self, y_norm):
        velocity = y_norm - self._prev_y
        self._prev_y = y_norm

        if self._tap_armed:
            if velocity < TAP_RELEASE_THRESHOLD:
                self._tap_armed = False
                return True
            return False

        if velocity > TAP_DOWN_THRESHOLD:
            self._tap_armed = True

        return False

    def start(self):
        print(f"LazyMouse started | Screen: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        print("Point with index finger. Tap finger downward to click.")
        print("Press Ctrl+C to quit.")

        try:
            while self.running:
                ret, frame = self.cap.read()
                if not ret:
                    print("Error: Failed to capture frame.")
                    break

                frame = cv2.flip(frame, 1)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.hands.process(rgb)

                if results.multi_hand_landmarks:
                    if not self.enabled:
                        continue

                    hand = results.multi_hand_landmarks[0]
                    tip = hand.landmark[8]

                    nx = max(self._roi_min, min(self._roi_max, tip.x))
                    ny = max(self._roi_min, min(self._roi_max, tip.y))
                    final_x, final_y = self._filter(nx, ny)
                    pyautogui.moveTo(final_x, final_y)

                    if (
                        self._detect_tap(tip.y)
                        and (time.time() - self.prev_click_time) > CLICK_COOLDOWN
                    ):
                        pyautogui.click()
                        self.prev_click_time = time.time()

        except KeyboardInterrupt:
            print("\nLazyMouse stopped.")
        finally:
            self._cleanup()

    def _cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()
