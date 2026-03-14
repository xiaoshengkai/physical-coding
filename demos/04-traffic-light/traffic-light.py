from gpiozero import LED
from time import sleep

red = LED(17)
yellow = LED(18)
green = LED(22)

print("Traffic Light Simulation Started")

try:
    while True:
        red.on()
        sleep(5)
        red.off()

        green.on()
        sleep(5)
        green.off()

        yellow.on()
        sleep(2)
        yellow.off()
except KeyboardInterrupt:
    red.off()
    yellow.off()
    green.off()
    print("\nProgram Stopped")
