import tm1637
from gpiozero import Button
import time

tm = tm1637.TM1637(clk=3, dio=2)
tm.brightness(7)

btn = Button(26, pull_up=True)

running = False
elapsed = 0.0
last_time = 0.0
last_press = 0
long_press_threshold = 1.0  # 长按1秒复位

print("单按钮秒表：短按开始/暂停，长按复位")
try:
    while True:
        now = time.time()
        if btn.is_pressed:
            press_start = time.time()
            while btn.is_pressed:  # 等待松开
                time.sleep(0.05)
            press_duration = time.time() - press_start
            if press_duration > long_press_threshold:
                # 长按复位
                running = False
                elapsed = 0.0
                tm.number(0)
                print("↩️ 复位")
            else:
                # 短按切换
                running = not running
                if running:
                    last_time = time.time()
                    print("▶️ 开始")
                else:
                    print("⏸️ 暂停")
            # 防抖延时
            time.sleep(0.2)

        if running:
            current = time.time()
            elapsed += current - last_time
            last_time = current
            if elapsed >= 10000:
                elapsed = 0
            tm.number(int(elapsed))

        time.sleep(0.1)
except KeyboardInterrupt:
    tm.write([0, 0, 0, 0])
    print("\n退出")
