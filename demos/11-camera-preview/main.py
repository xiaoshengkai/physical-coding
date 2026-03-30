#!/usr/bin/env python3
"""
简单实验：按 Enter 键拍照
使用 picamera2 库
"""

from picamera2 import Picamera2
import time

picam2 = Picamera2()
config = picam2.create_still_configuration()
picam2.configure(config)
picam2.start()

print("摄像头已启动，按 Enter 键拍照（按 Ctrl+C 退出）")

try:
    while True:
        input()
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"photo_{timestamp}.jpg"
        picam2.capture_file(filename)
        print(f"✅ 照片已保存：{filename}")

except KeyboardInterrupt:
    print("\n👋 退出")
finally:
    picam2.stop()
