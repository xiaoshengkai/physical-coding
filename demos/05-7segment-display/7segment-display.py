import tm1637
import time

tm = tm1637.TM1637(clk=3, dio=2)

tm.brightness(7)

print("7-Segment Display Test Started")

try:
    print("Show: 1234")
    tm.show("1234")
    time.sleep(2)

    print("Show: COOL")
    tm.show("COOL")
    time.sleep(2)

    print("Show: -123")
    tm.number(-123)
    time.sleep(2)

    print("Show: 0xDEAD")
    tm.hex(0xDEAD)
    time.sleep(2)

    print("Show: 12:59")
    tm.numbers(12, 59, colon=True)
    time.sleep(2)

    print("Show: 24C")
    tm.temperature(24)
    time.sleep(2)

    print("Scroll: HELLO WORLD")
    tm.scroll("HELLO WORLD", delay=200)

    tm.show("    ")
    print("Test Complete")

except KeyboardInterrupt:
    tm.write([0, 0, 0, 0])
    print("\nProgram Stopped")
