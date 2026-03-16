import tm1637
import time
from datetime import datetime

tm = tm1637.TM1637(clk=3, dio=2)
tm.brightness(7)

colon = True
last_update = 0

print("时钟开始，按 Ctrl+C 停止")
try:
    while True:
        now = datetime.now()
        hours = now.hour
        minutes = now.minute

        # 每0.5秒切换冒点
        if time.time() - last_update > 0.5:
            colon = not colon
            last_update = time.time()

        tm.numbers(hours, minutes, colon=colon)
        time.sleep(0.1)  # 降低CPU占用
except KeyboardInterrupt:
    tm.write([0,0,0,0])
    print("\n停止")