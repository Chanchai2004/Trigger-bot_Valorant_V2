import numpy as np  
import keyboard
import time
import mss

# กำหนดค่าเวลา (0.1 วินาที) เพื่อรอการกดปุ่ม
NO_KEY_PRESS_THRESHOLD = 0.1

# เก็บเวลาล่าสุดที่มีการกดปุ่ม w, a, s, d
last_keypress_time = time.time()

# ฟังก์ชันตรวจสอบพิกเซลและทำการกระทำ (trigger action)
def check_and_trigger_action(img):
    global last_keypress_time
    
    # หากกดปุ่ม w, a, s, d จะอัปเดตเวลา `last_keypress_time`
    if keyboard.is_pressed('w') or keyboard.is_pressed('s') or keyboard.is_pressed('d') or keyboard.is_pressed('a'):
        last_keypress_time = time.time()

    # ตรวจสอบว่าผ่านไป 0.1 วินาทีโดยไม่มีการกดปุ่มหรือไม่
    if time.time() - last_keypress_time > NO_KEY_PRESS_THRESHOLD:
        # ตรวจสอบว่าพิกเซลในภาพตรงเงื่อนไขหรือไม่: r > 180, g < 80, b < 80
        if np.any((img[:, :, 2] > 180) & (img[:, :, 1] < 80) & (img[:, :, 0] < 80)):
            # กระทำโดยการกดปุ่ม 'l'
            keyboard.press_and_release('l')  # กดและปล่อยปุ่ม 'l'
            time.sleep(0.2)  # เพิ่มดีเลย์เล็กน้อย
            print('Action triggered')  # แสดงข้อความเมื่อมีการกระทำ
            return True  # มีการกระทำเกิดขึ้น

    return False  # ไม่มีการกระทำ

# เริ่มโปรแกรมหลัก
if __name__ == '__main__':
    print('Starting...')  # แสดงข้อความเริ่มต้น

    # กำหนดพื้นที่หน้าจอสำหรับจับภาพ (6x6 พิกเซล)
    monitor = {"top": 476, "left": 636, "width": 8, "height": 6}

    # สร้างอินสแตนซ์ `mss` สำหรับการจับภาพหน้าจอ
    with mss.mss() as sct:
        while True:
            # จับภาพหน้าจอในพื้นที่ที่กำหนดและแปลงเป็นอาร์เรย์ NumPy
            img = np.array(sct.grab(monitor), dtype=np.uint8)  # ใช้ `dtype` เพื่อเพิ่มประสิทธิภาพ

            # แปลง BGRA (จาก mss) เป็น BGR (สำหรับใช้งานใน NumPy)
            img_bgr = img[:, :, :3]  # ลบช่อง alpha เพื่อเพิ่มประสิทธิภาพ
            
            # ตรวจสอบและทำการกระทำตามพิกเซลในภาพ
            if check_and_trigger_action(img_bgr):
                pass  # อาจเพิ่มเงื่อนไขเพิ่มเติมที่นี่

            # กดปุ่ม 'i' เพื่อหยุดโปรแกรม (สำหรับ debugging)
            if keyboard.is_pressed('i'):
                break  # ออกจากลูป
