import numpy as np  
import keyboard
import time
import mss


# ฟังก์ชันที่ปรับปรุงให้เช็คว่ามีพิกเซลในพื้นที่ที่ตรงกับเงื่อนไขหรือไม่
def check_and_trigger_action(img):
    # ตรวจสอบว่ามีพิกเซลที่ตรงเงื่อนไข: สีแดง (r > 180), สีเขียว (g < 80), สีฟ้า (b < 80)
    if np.any((img[:, :, 2] > 180) & (img[:, :, 1] < 80) & (img[:, :, 0] < 80)):
        # กดปุ่ม 'shift+x'
        keyboard.press('shift+x')
        time.sleep(0.1)  # เพิ่มดีเลย์เล็กน้อยเพื่อเลียนแบบการกดปุ่ม
        keyboard.release('shift+x')  # ปล่อยปุ่ม 'shift+x'
        
        time.sleep(0.1)  # เวลาพักเพื่อปรับความเร็ว
        print('Action triggered')  # แสดงข้อความว่ามีการกระทำเกิดขึ้น
        return True  # คืนค่า True เพื่อระบุว่ามีการกระทำเกิดขึ้น
    else:
        return False  # คืนค่า False หากไม่มีการกระทำเกิดขึ้น

# จุดเริ่มต้นของโปรแกรม
if __name__ == '__main__':
    print('Starting...')  # แสดงข้อความว่าโปรแกรมกำลังเริ่มทำงาน

    # กำหนดพื้นที่หน้าจอสำหรับการจับภาพ (ขนาด 6x6 พิกเซล)
    monitor = {"top": 476, "left": 636, "width": 8, "height": 6}

    # สร้างอินสแตนซ์ mss เพื่อจับภาพหน้าจออย่างรวดเร็ว
    with mss.mss() as sct:
        while True:
            # จับภาพหน้าจอในพื้นที่ที่กำหนดและแปลงเป็นอาร์เรย์ NumPy
            img = np.array(sct.grab(monitor), dtype=np.uint8)  # ปรับปรุงการประมวลผลโดยใช้ dtype ที่เหมาะสม

            # แปลง BGRA (จาก mss) เป็น BGR (สำหรับใช้งานกับ NumPy)
            img_bgr = img[:, :, :3]  # ลบช่อง alpha ออกเพื่อเพิ่มประสิทธิภาพ
            
            # ตรวจสอบและเรียกใช้งานคำสั่งตามค่าของพิกเซล
            if check_and_trigger_action(img_bgr):
                # ตัวเลือก: หยุดหรือกระทำเพิ่มเติมตามคำสั่ง
                pass

            # ตัวเลือก: หากต้องการหยุดลูป ให้กดปุ่ม 'i'
            if keyboard.is_pressed('i'):
                break
