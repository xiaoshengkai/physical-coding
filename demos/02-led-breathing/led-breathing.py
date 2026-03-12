#!/usr/bin/env python3
from gpiozero import PWMLED
from time import sleep

led = PWMLED(17)

print("呼吸灯开始，按 Ctrl+C 停止")

try:
    while True:
        for brightness in range(0, 101, 1):
            led.value = brightness / 100.0
            sleep(0.02)
        for brightness in range(100, -1, -1):
            led.value = brightness / 100.0
            sleep(0.02)
except KeyboardInterrupt:
    led.off()
    print("\n程序结束")
