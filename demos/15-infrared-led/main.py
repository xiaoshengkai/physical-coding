import RPi.GPIO as GPIO
import time

IR_SENSOR_PIN = 26
LED_PIN = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_SENSOR_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)

print("红外传感器 + LED 已启动，检测到障碍物时 LED 亮起...")

try:
    while True:
        if GPIO.input(IR_SENSOR_PIN) == GPIO.LOW:
            GPIO.output(LED_PIN, GPIO.HIGH)
            print("⚠️ 检测到障碍物！LED 亮")
        else:
            GPIO.output(LED_PIN, GPIO.LOW)
            print("✅ 一切正常")
        time.sleep(0.2)

except KeyboardInterrupt:
    print("\n程序已退出")
finally:
    GPIO.cleanup()
