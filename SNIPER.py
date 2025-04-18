import numpy as np
import keyboard
import time
import mss
import os
import sys
import winsound  # สำหรับเล่นเสียงใน Windows

# กำหนดค่าเวลา (0.1 วินาที)
NO_KEY_PRESS_THRESHOLD = 0.11

last_keypress_time = time.time()

def beep_twice():
    frequency = 1000  # ความถี่เสียง (Hz)
    duration = 100    # ระยะเวลาเสียงแต่ละปิ๊บ (ms)
    winsound.Beep(frequency, duration)
    time.sleep(0.2)
    winsound.Beep(frequency, duration)

# ฟังก์ชันตรวจสอบ
def check_and_trigger_action(img):
    global last_keypress_time

    if keyboard.is_pressed('w') or keyboard.is_pressed('s') or keyboard.is_pressed('d') or keyboard.is_pressed('a'):
        last_keypress_time = time.time()

    if time.time() - last_keypress_time > NO_KEY_PRESS_THRESHOLD:
        if np.any((img[:, :, 2] > 180) & (img[:, :, 1] < 80) & (img[:, :, 0] < 80)):
            keyboard.press_and_release('l')
            time.sleep(0.05)
            time.sleep(0.2)
            print(f'Action triggered (Round 1)')

            os.execv(sys.executable, ['python'] + sys.argv)
            return True

    return False

# เริ่มโปรแกรมหลัก
if __name__ == '__main__':
    try:

        monitor = {"top": 476, "left": 636, "width": 8, "height": 6}

        with mss.mss() as sct:
            while True:
                img = np.array(sct.grab(monitor), dtype=np.uint8)
                img_bgr = img[:, :, :3]
                check_and_trigger_action(img_bgr)

                if keyboard.is_pressed('i'):
                    print("Stopping program...")
                    beep_twice()
                    break

    except Exception as e:
        print(f"An error occurred: {e}")
        beep_twice()
        sys.exit(1)

    except KeyboardInterrupt:
        print("Program interrupted by user.")
        beep_twice()
        sys.exit(0)
