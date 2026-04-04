import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
DO_PIN = 17
GPIO.setup(DO_PIN, GPIO.IN)

print("烟雾探测器已启动，按下 Ctrl+C 退出。")

try:
    while True:
        if GPIO.input(DO_PIN) == 0:
            print("警告：检测到烟雾或可燃气体！")
        else:
            print("环境安全")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\n程序已退出。")
finally:
    GPIO.cleanup()
