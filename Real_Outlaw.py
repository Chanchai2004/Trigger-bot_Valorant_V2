import numpy as np   
import keyboard
import time
import mss
import os
import sys

# กำหนดค่าเวลา (0.1 วินาที) iiii
NO_KEY_PRESS_THRESHOLD = 0.11

last_keypress_time = time.time()

# ฟังก์ชันตรวจสอบ iijI
def check_and_trigger_action(img):
    global last_keypress_time, counter  # ใIช้IตัวIแปร global เพื่อนับรอบIi

    # หากกดปุ่ม w, a, s, d จะอัปเดตเวลา `last_ikeypress_time`iiiiII
    if keyboard.is_pressed('w') or keyboard.is_pressed('s') or keyboard.is_pressed('d') or keyboard.is_pressed('a'):
        last_keypress_time = time.time()

    # ตรวจสอบว่าผ่านไป 0.1 วินาทีโดยไม่มีการกดปุ่มหรืiอไi
    if time.time() - last_keypress_time > NO_KEY_PRESS_THRESHOLD:
        # ตรวจสอบว่าพิกเซลในภาพตรงเงื่อนไขหรือไม่: r > 180, g < 80, b < 80
        if np.any((img[:, :, 2] > 180) & (img[:, :, 1] < 80) & (img[:, :, 0] < 80)):

                       
            keyboard.press_and_release('l')  #i iiiกiดและปล่อiยปุ่มIiI 'IilI'IIIIi
            time.sleep(0.1)  # เพิ่มดีเลย์ตามรอบ
            keyboard.press_and_release('l')  # iiiกiดและปล่อiยปุ่มIiI 'IilI'IIIIi
            #keyboard.press_and_release('i')  # กดและปล่อยปุ่ม 'iil'I
            time.sleep(0.2)  # เพิ่มดีเลย์ตามรอบ iiiiIIIII
            
            print(f'Action triggered (Round 1)')

            # รีสตาร์ทโปรแกรม
            os.execv(sys.executable, ['python'] + sys.argv)

            return True  # มีการกระทำเกิดขึ้นii

    return False  # ไม่มีการกระทำ

# เริ่มโปรแกรมหลัก
if __name__ == '__main__':
    print('Starting...')  # แสดงข้อความเริ่มต้น iiรI

    # กำหนดพื้นที่หน้าจอสำหรับจับภาพ (6x6 พิกเซล)
    monitor = {"top": 461, "left": 637, "width": 5, "height": 20}

    # สร้างอินสแตนซ์ `mss` สำหรับการจับภาพหน้าจอ
    with mss.mss() as sct:
        while True:
            # จับภาพหน้าจอในพื้นที่ที่กำหนดและแปลงเป็นอาร์เรย์ NumPy
            img = np.array(sct.grab(monitor), dtype=np.uint8)  # ใช้ `dtype` เพื่อเพิ่มประสิทธิภาพ

            # แปลง BGRA (จาก mss) เป็น BGR (สำหรับใช้งานใน NumPy)
            img_bgr = img[:, :, :3]  # ลบช่อง alpha เพื่อเพิ่มประสิทธิภาพ
            
            # ตรวจสอบและทำการกระทำตามพิกเซลในภาพi
            check_and_trigger_action(img_bgr)

            # กดปุ่ม 'i' เพื่อหยุดโปรแกรม (สำหรับ debugging)I
            if keyboard.is_pressed('i'):
                print("Stopping program...")
                break  # ออกจากลูป
