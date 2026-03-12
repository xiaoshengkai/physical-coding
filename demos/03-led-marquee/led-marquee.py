#!/usr/bin/env python3
from gpiozero import LED
from time import sleep

led_pins = [17, 18, 22, 23]
leds = [LED(pin) for pin in led_pins]

print("流水灯开始，按 Ctrl+C 停止")

try:
    while True:
        for led in leds:
            led.on()
            sleep(0.2)
            led.off()
        for led in reversed(leds):
            led.on()
            sleep(0.2)
            led.off()
except KeyboardInterrupt:
    for led in leds:
        led.off()
    print("\n程序结束")
