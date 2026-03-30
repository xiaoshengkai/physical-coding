import RPi.GPIO as GPIO
import time

IR_SENSOR_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("红外传感器已启动，请将物体靠近传感器...")

try:
    while True:
        sensor_state = GPIO.input(IR_SENSOR_PIN)

        if sensor_state == GPIO.LOW:
            print("⚠️ 检测到障碍物！")
        else:
            print("✅ 一切正常")

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n程序已退出")

finally:
    GPIO.cleanup()
