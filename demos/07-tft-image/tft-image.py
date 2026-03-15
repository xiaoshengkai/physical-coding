import digitalio
import busio
import board
from adafruit_rgb_display import st7735
from PIL import Image
import time

# 初始化 SPI 和引脚（根据你的接线调整）
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)  # GPIO5
dc = digitalio.DigitalInOut(board.D25)  # GPIO25
# 没有 RST 引脚，不传

# 创建显示屏对象（分辨率 128x128，可调整）
display = st7735.ST7735R(spi, cs=cs, dc=dc, width=128, height=160, baudrate=24000000)

# 加载图片（请替换为你的图片路径）
image_path = "/home/xiaoshengkai/Desktop/workspace/PhysicalCoding/static/images/g.jpg"
image = Image.open(image_path)

# 缩放图片以适应屏幕（保持比例，居中显示）
image.thumbnail((display.width, display.height), Image.Resampling.LANCZOS)
# 创建黑色背景
background = Image.new("RGB", (display.width, display.height), (0, 0, 0))
# 计算居中位置
x = (display.width - image.width) // 2
y = (display.height - image.height) // 2
background.paste(image, (x, y))

# 显示图片
display.image(background)

print("图片已显示，按 Ctrl+C 退出")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
