import numpy as np  
import keyboard
import time
import mss

# ระยะเวลาสูงสุดที่ไม่กดปุ่ม (0.1 วินาที)
NO_KEY_PRESS_THRESHOLD = 0.1
# ใช้ติดตามเวลาที่กดปุ่ม w, a, s, d ล่าสุด
last_keypress_time = time.time()

# ฟังก์ชันที่ปรับปรุงเพื่อเช็คว่ามีพิกเซลในพื้นที่ที่ตรงเงื่อนไขหรือไม่
def check_and_trigger_action(img):
    global last_keypress_time
    
    # อัปเดตเวลาการกดปุ่มล่าสุดหากกดปุ่ม w, a, s, d
    if keyboard.is_pressed('w') or keyboard.is_pressed('s') or keyboard.is_pressed('d') or keyboard.is_pressed('a'):
        last_keypress_time = time.time()

    # ตรวจสอบว่ามีช่วงเวลาที่ไม่กดปุ่มเกิน 0.1 วินาทีหรือไม่
    if time.time() - last_keypress_time > NO_KEY_PRESS_THRESHOLD:
        # สร้างหน้ากาก (mask) สำหรับพิกเซลที่ตรงเงื่อนไข: r > 180, g < 80, b < 80
        # การตรวจสอบพิกเซลที่ปรับปรุงให้รวมเงื่อนไขในขั้นตอนเดียว
        if np.any((img[:, :, 2] > 180) & (img[:, :, 1] < 80) & (img[:, :, 0] < 80)):
            # เรียกใช้งานคำสั่งเมื่อพิกเซลตรงเงื่อนไข

            # กดและปล่อยปุ่ม 'j' (หรือสามารถปรับเป็น 'l' ได้หากต้องการ)
            keyboard.press_and_release('j')
            time.sleep(0.11)  # เพิ่มดีเลย์เล็กน้อยเพื่อเลียนแบบการกระทำ
            
            # คืนค่า True เพื่อบอกว่ามีการเรียกใช้คำสั่ง
            return True

    return False  # คืนค่า False หากไม่มีการเรียกใช้คำสั่ง

# จุดเริ่มต้นของสคริปต์
if __name__ == '__main__':
    print('เริ่มต้นการทำงาน...')

    # กำหนดพื้นที่จอภาพสำหรับการจับภาพ (ขนาด 6x6 พิกเซล)
    monitor = {"top": 476, "left": 636, "width": 8, "height": 6}

    # สร้างอินสแตนซ์ mss สำหรับการจับภาพหน้าจอที่รวดเร็ว
    with mss.mss() as sct:
        while True:
            # จับภาพหน้าจอในพื้นที่ที่กำหนดและแปลงเป็นอาร์เรย์ NumPy
            img = np.array(sct.grab(monitor), dtype=np.uint8)  # ปรับ dtype เพื่อเพิ่มประสิทธิภาพการประมวลผล

            # แปลง BGRA (จาก mss) เป็น BGR (สำหรับการใช้งานใน NumPy)
            img_bgr = img[:, :, :3]  # ลบช่อง alpha ออก (ปรับให้ทำงานเร็วขึ้นด้วยการหลีกเลี่ยงการคัดลอกข้อมูลเพิ่มเติม)
            
            # ตรวจสอบและเรียกใช้คำสั่งตามค่าพิกเซล
            if check_and_trigger_action(img_bgr):
                # ตัวเลือก: หยุดลูปหรือตรวจสอบอินพุตผู้ใช้งาน (ถ้าจำเป็น)
                pass

            # ตัวเลือก: กดปุ่ม 'i' เพื่อหยุดลูป (สำหรับการดีบัก)
            if keyboard.is_pressed('i'):
                break
