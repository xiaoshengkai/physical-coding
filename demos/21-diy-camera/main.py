#!/usr/bin/env python3

import sys
import time
import digitalio
import board
from adafruit_rgb_display import st7789
from PIL import Image, ImageDraw

def phase1_screen():
    print("=== Phase 1: 屏幕测试 ===")
    try:
        spi = board.SPI()
        cs_pin = digitalio.DigitalInOut(board.D5)
        dc_pin = digitalio.DigitalInOut(board.D25)
        reset_pin = digitalio.DigitalInOut(board.D27)

        display = st7789.ST7789(
            spi,
            cs=cs_pin,
            dc=dc_pin,
            rst=reset_pin,
            width=480,
            height=320,
            baudrate=24000000,
            rotation=0,          # 可尝试改为 0 测试
        )

        # 打印实际尺寸，调试用
        print(f"屏幕初始化成功，实际尺寸: {display.width} x {display.height}")

        # 使用 display.width 和 display.height 创建图像
        image = Image.new("RGB", (display.width, display.height), "BLACK")
        draw = ImageDraw.Draw(image)
        draw.rectangle((20, 20, display.width-20, display.height-20), outline="GREEN", width=3)
        draw.text((display.width//2-100, display.height//2-10), "DIY Camera Ready!", fill="WHITE")
        display.image(image)

        print("屏幕显示测试成功！按 Ctrl+C 退出")
        while True:
            time.sleep(1)
    except Exception as e:
        print(f"屏幕测试失败: {e}")
        sys.exit(1)

def phase2_encoder():
    print("=== Phase 2: 旋转编码器测试 ===")
    try:
        from gpiozero import RotaryEncoder
        encoder = RotaryEncoder(a=17, b=18, wrap=100)
        print("旋转旋钮查看数值变化")
        print("按下按钮确认")
        print("按 Ctrl+C 退出")
        last_value = 0
        while True:
            current = encoder.value
            if current != last_value:
                direction = "+" if current > last_value else "-"
                print(f"旋转 {direction}: {current}")
                last_value = current
            time.sleep(0.05)
    except ImportError:
        print("请安装: sudo pip3 install gpiozero")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n编码器测试结束")

def phase3_camera():
    print("=== Phase 3: 摄像头取景测试 ===")
    try:
        from picamera2 import Picamera2
        picam2 = Picamera2()
        config = picam2.create_preview_configuration(
            main={"size": (480, 320), "format": "RGB888"}
        )
        picam2.configure(config)
        picam2.start()
        print("摄像头取景中，按 Ctrl+C 退出")
        while True:
            frame = picam2.capture_array()
            # 此处可添加显示到屏幕的代码，但仅测试时不显示
            time.sleep(0.1)
    except ImportError:
        print("请安装: sudo pip3 install picamera2")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n摄像头测试结束")
    finally:
        picam2.stop()

def main():
    print("DIY 相机 - 综合测试")
    print("1. 屏幕测试")
    print("2. 旋转编码器测试")
    print("3. 摄像头取景测试")
    choice = input("选择测试项目 (1-3): ").strip()
    if choice == "1":
        phase1_screen()
    elif choice == "2":
        phase2_encoder()
    elif choice == "3":
        phase3_camera()
    else:
        print("无效选择")

if __name__ == "__main__":
    main()