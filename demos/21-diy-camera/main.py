#!/usr/bin/env python3
import time
import spidev
import RPi.GPIO as GPIO
import numpy as np
from picamera2 import Picamera2

# ================= 屏幕 =================
LCD_W, LCD_H = 320, 480
CAM_W, CAM_H = 320, 240
OFFSET_X = (LCD_W - CAM_W) // 2
OFFSET_Y = (LCD_H - CAM_H) // 2

# ================= GPIO =================
DC, RST, CS = 24, 25, 5
BUTTON_PIN = 17
BUZZER_PIN = 18

GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

GPIO.setup(DC, GPIO.OUT)
GPIO.setup(RST, GPIO.OUT)
GPIO.setup(CS, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

buzzer = GPIO.PWM(BUZZER_PIN, 1000)
buzzer.start(0)

# ================= SPI =================
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 40000000
spi.mode = 0
GPIO.output(CS, 0)

# ================= LCD底层 =================
def cmd(c):
    GPIO.output(DC, 0)
    spi.writebytes([c])

def data(d):
    GPIO.output(DC, 1)
    spi.writebytes(d if isinstance(d, list) else [d])

def reset():
    GPIO.output(RST, 0)
    time.sleep(0.1)
    GPIO.output(RST, 1)
    time.sleep(0.1)

def lcd_init():
    reset()
    cmd(0x11)
    time.sleep(0.12)
    cmd(0x3A)
    data(0x66)   # RGB666
    cmd(0x36)
    data(0x48)
    cmd(0x29)
    time.sleep(0.05)

def set_window(x0, y0, x1, y1):
    cmd(0x2A)
    data([x0 >> 8, x0 & 0xFF, x1 >> 8, x1 & 0xFF])
    cmd(0x2B)
    data([y0 >> 8, y0 & 0xFF, y1 >> 8, y1 & 0xFF])
    cmd(0x2C)

def send_frame(buf):
    GPIO.output(DC, 1)
    chunk = 4096
    for i in range(0, len(buf), chunk):
        spi.xfer3(list(buf[i:i+chunk]))

# ================= 图像转换 =================
def rgb888_to_rgb666(arr):
    r = arr[:, :, 2] & 0xFC
    g = arr[:, :, 1] & 0xFC
    b = arr[:, :, 0] & 0xFC
    return np.dstack((r, g, b)).astype(np.uint8).flatten().tobytes()

# ================= 摄像头 =================
picam2 = Picamera2()
config = picam2.create_video_configuration(
    main={"size": (CAM_W, CAM_H), "format": "RGB888"},
    controls={"FrameRate": 15}
)
picam2.configure(config)
picam2.start()
time.sleep(1)

# ================= LCD初始化 =================
lcd_init()
black = bytes([0, 0, 0] * LCD_W * LCD_H)
set_window(0, 0, LCD_W - 1, LCD_H - 1)
send_frame(black)

# ================= 主循环 =================
prev_frame = None
frame_count = 0

try:
    while True:
        frame = picam2.capture_array()
        frame_count += 1

        # 自适应跳帧
        if prev_frame is not None:
            diff = np.abs(frame.astype(np.int16) - prev_frame.astype(np.int16))
            if np.mean(diff) > 18:
                if frame_count % 2 != 0:
                    continue
        prev_frame = frame

        buf = rgb888_to_rgb666(frame)
        set_window(OFFSET_X, OFFSET_Y, OFFSET_X + CAM_W - 1, OFFSET_Y + CAM_H - 1)
        send_frame(buf)

        # 按键拍照
        if GPIO.input(BUTTON_PIN) == 0:
            time.sleep(0.05)  # 防抖
            if GPIO.input(BUTTON_PIN) == 0:
                print("拍照！")
                buzzer.ChangeDutyCycle(50)
                time.sleep(0.1)
                buzzer.ChangeDutyCycle(0)

                img = picam2.capture_image()
                timestamp = int(time.time())
                img.save(f"photo_{timestamp}.jpg")
                print(f"保存 photo_{timestamp}.jpg")

                time.sleep(1)  # 拍照停留

except KeyboardInterrupt:
    print("退出")

finally:
    buzzer.stop()
    picam2.stop()
    GPIO.cleanup()
    spi.close()