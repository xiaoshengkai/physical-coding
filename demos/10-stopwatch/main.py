import tm1637
from gpiozero import Button
import time

tm = tm1637.TM1637(clk=3, dio=2)
tm.brightness(7)

# 使用两个按钮，启用内部上拉
btn_start = Button(26, pull_up=True, bounce_time=0.05)
btn_reset = Button(19, pull_up=True, bounce_time=0.05)

running = False
elapsed = 0
last_time = 0

print("秒表已启动，按 Ctrl+C 退出")

try:
    while True:
        # 处理开始/暂停按钮
        if btn_start.is_pressed:
            # 避免长按多次触发，加小延时
            time.sleep(0.1)
            running = not running
            if running:
                last_time = time.time()
                print("▶️ 开始")
            else:
                print("⏸️ 暂停")

        # 处理复位按钮
        if btn_reset.is_pressed:
            time.sleep(0.1)
            running = False
            elapsed = 0
            tm.number(0)
            print("↩️ 复位")

        if running:
            now = time.time()
            elapsed += now - last_time
            last_time = now
            if elapsed >= 10000:
                elapsed = 0  # 防止溢出
            tm.number(int(elapsed))

        time.sleep(0.1)
except KeyboardInterrupt:
    tm.write([0, 0, 0, 0])
    print("\n退出")