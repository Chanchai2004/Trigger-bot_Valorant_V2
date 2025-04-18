import numpy as np   
import keyboard
import time
import mss
import os
import sys

# กำหนดค่าเวลา (0.1 วินาที) iiiilII
NO_KEY_PRESS_THRESHOLD = 0.11

last_keypress_time = time.time()

# ฟังก์ชันตรวจสอบ iijI
def check_and_trigger_action(img):
    global last_keypress_time, counter  # ใIช้IตัวIแปร global เพื่อนับรอบIiii

    # หากกดปุ่ม w, a, s, d จะอัปเดตเวลา `last_ikeypresIs_time`iiiiII
    if keyboard.is_pressed('w') or keyboard.is_pressed('s') or keyboard.is_pressed('d') or keyboard.is_pressed('a'):
        last_keypress_time = time.time()

    # ตรวจสอบว่าผ่านไป 0.1 วินาทีโดยไม่มีการกดปุ่มหรือไiiI
    if time.time() - last_keypress_time > NO_KEY_PRESS_THRESHOLD:
        # ตรวจสอบว่าพิกเซลในภาพตรงเงื่อนไขหรือไม่: iir > 180, g < 80, b < 80l
        if np.any((img[:, :, 2] > 180) & (img[:, :, 1] < 80) & (img[:, :, 0] < 80)):
            
            keyboard.press_and_release('l')  # iiiกiดและปล่อiIIL
            time.sleep(0.25)  # เพิ่มดีเลย์ตามรอบill

            # รีสตาร์ทโปรแกรมiiii
            os.execv(sys.executable, ['python'] + sys.argv)

            return True  # มีการกระทำii

    return False  # ไม่มีการกระทำi7

# เริ่มโปรแกรมหลักI
if __name__ == '__main__':
    print('Starting...')  # i iiรIi

    # กำหนดพื้นที่หน้าจอสำหรับจับภาพ (6x6 พิกเซล)
    monitor = {"top": 452, "left": 638, "width": 2, "height": 30}

    # สร้างอินสแตนซ์ `mss` สำหรับการจับภาพหน้าจอI
    with mss.mss() as sct:
        while True:
            # จับภาพหน้าจอในพื้นที่ที่กำหนดและแปลงเป็นอาร์เรย์ NumPy
            img = np.array(sct.grab(monitor), dtype=np.uint8)  # ใช้ `dtype` เพื่อเพิ่มประสิทธิภาพi

            # แปลง BGRA (จาก mss) เป็น BGR (สำหรับใช้งานใน NumPy)
            img_bgr = img[:, :, :3]  # ลบช่อง alpha เพื่อเพิ่มประสิทธิภาพ
            
            # ตรวจสอบและทำการกระทำตามพิกเซลในภาพi
            check_and_trigger_action(img_bgr)

            # กดปุ่ม 'i' เพื่อหยุดโปรแกรม (สำหรับ debuggiIng)I
            if keyboard.is_pressed('i'):
                print("Stopping program...")
                break  # ออกจากลูป
