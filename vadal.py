import numpy as np   
import keyboard
import time
import mss
import os
import sys

import cv2  # เพิ่มการใช้งาน OpenCV

# def show_and_resize_image(img):
#     # ปรับขนาดภาพให้เป็น 200x200 พิกเซล
#     resized_img = cv2.resize(img, (400, 400))
    
#     # แสดงภาพในหน้าต่างใหม่
#     cv2.imshow("Captured Image", resized_img)
    
#     # รอให้ผู้ใช้กดปุ่มเพื่อปิดหน้าต่าง (รอ 1 ms)
#     cv2.waitKey(1)  # รอการกดปุ่ม 1 มิลลิวินาที

#     # ปิดหน้าต่างเมื่อกดปุ่ม 'q'
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         cv2.destroyAllWindows()

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
            
            time.sleep(0.1)
            keyboard.press_and_release('l')  # iiiกiดและปล่อiIIL
            # time.sleep(0.1)  # เพิ่มดีเลย์ตามรอบill
            # keyboard.press_and_release('l')  # iiiกiดและปล่อiIIL
            time.sleep(0.2)

            # รีสตาร์ทโปรแกรมiiii
            os.execv(sys.executable, ['python'] + sys.argv)

            return True  # มีการกระทำii

    return False  # ไม่มีการกระทำi7

# เริ่มโปรแกรมหลักI
if __name__ == '__main__':
    print('Starting...')  # i iiรIi

    # กำหนดพื้นที่หน้าจอสำหรับจับภาพ (6x6 พิกเซล)
    monitor = {"top": 461, "left": 637, "width": 5, "height": 20}

    # สร้างอินสแตนซ์ `mss` สำหรับการจับภาพหน้าจอI
    with mss.mss() as sct:
        while True:
            # จับภาพหน้าจอในพื้นที่ที่กำหนดและแปลงเป็นอาร์เรย์ NumPy
            img = np.array(sct.grab(monitor), dtype=np.uint8)  # ใช้ `dtype` เพื่อเพิ่มประสิทธิภาพi

            # แปลง BGRA (จาก mss) เป็น BGR (สำหรับใช้งานใน NumPy)
            img_bgr = img[:, :, :3]  # ลบช่อง alpha เพื่อเพิ่มประสิทธิภาพ

            # show_and_resize_image(img_bgr)
            
            # ตรวจสอบและทำการกระทำตามพิกเซลในภาพi
            check_and_trigger_action(img_bgr)

            # กดปุ่ม 'i' เพื่อหยุดโปรแกรม (สำหรับ debuggiIng)I
            if keyboard.is_pressed('i'):
                print("Stopping program...")
                break  # ออกจากลูป
