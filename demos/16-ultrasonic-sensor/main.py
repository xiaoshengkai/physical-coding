import RPi.GPIO as GPIO
import time

TRIG = 23
ECHO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)
time.sleep(2)


def get_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    timeout = time.time() + 0.1
    while GPIO.input(ECHO) == 0:
        if time.time() > timeout:
            return None

    pulse_start = time.time()
    while GPIO.input(ECHO) == 1:
        if time.time() > timeout:
            return None
    pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 34300 / 2
    return round(distance, 2)


print("HC-SR04 超声波测距开始，按 Ctrl+C 退出")
try:
    while True:
        dist = get_distance()
        if dist is not None:
            print(f"距离: {dist} cm")
        else:
            print("测量超时，请检查传感器连接或距离太远")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\n程序结束")
finally:
    GPIO.cleanup()
