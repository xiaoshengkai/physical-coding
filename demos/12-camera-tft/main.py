import time
import digitalio
import busio
import board
from adafruit_rgb_display import st7735
from PIL import Image
from picamera2 import Picamera2

# --- 屏幕初始化（SPI 速度 10MHz）---
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
dc = digitalio.DigitalInOut(board.D25)
rst = digitalio.DigitalInOut(board.D27)

rst.direction = digitalio.Direction.OUTPUT
rst.value = False
time.sleep(0.1)
rst.value = True
time.sleep(0.1)

display = st7735.ST7735R(
    spi, cs=cs, dc=dc, rst=rst,
    width=128, height=160,
    baudrate=10000000          # 10MHz 稳定且快速
)

# --- 摄像头初始化 ---
picam2 = Picamera2()
config = picam2.create_preview_configuration(
    main={"size": (640, 480), "format": "RGB888"},
    controls={"FrameRate": 30}
)
picam2.configure(config)
picam2.set_controls({"AwbEnable": True})
picam2.start()
time.sleep(1)

screen_size = (display.width, display.height)

def reduce_blue(image, factor=0.7):
    r, g, b = image.split()
    b = b.point(lambda x: int(x * factor))
    return Image.merge("RGB", (r, g, b))

print("取景器已启动（无延时版），按 Ctrl+C 退出")
try:
    while True:
        img = picam2.capture_image()          # 等待摄像头捕获（自动限速）
        r, g, b = img.split()
        img = Image.merge("RGB", (b, g, r))   # 交换红蓝
        img = reduce_blue(img, factor=0.7)    # 削弱蓝色
        img = img.resize(screen_size, Image.Resampling.NEAREST)
        display.image(img)
        # 不加任何延时，让循环以摄像头实际帧率运行
except KeyboardInterrupt:
    print("退出")
finally:
    picam2.stop()
    display.image(Image.new("RGB", screen_size, (0, 0, 0)))