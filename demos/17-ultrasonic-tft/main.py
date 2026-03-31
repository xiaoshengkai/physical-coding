import RPi.GPIO as GPIO
import time
import digitalio
import busio
import board
from adafruit_rgb_display import st7735
from PIL import Image, ImageDraw, ImageFont
import os

# ================== 屏幕初始化 ==================
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)   # CS 接 GPIO5
dc = digitalio.DigitalInOut(board.D25)  # DC 接 GPIO25
display = st7735.ST7735R(
    spi, cs=cs, dc=dc,
    width=128, height=160,
    baudrate=8000000          # 8MHz 稳定
)

# ================== 字体加载 ==================
# 尝试多个字体路径，优先使用大号英文字体
font_paths = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",     # 英文大字体
    "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
]
title_font = None   # 标题字体（小）
value_font = None   # 数值字体（大）
for path in font_paths:
    if os.path.exists(path):
        try:
            title_font = ImageFont.truetype(path, 12)
            value_font = ImageFont.truetype(path, 28)
            print(f"✅ 使用字体: {path}")
            break
        except:
            continue
if title_font is None:
    title_font = ImageFont.load_default()
    value_font = ImageFont.load_default()
    print("⚠️ 使用默认字体（小字号）")

# ================== 超声波引脚 ==================
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

def draw_dashboard(dist):
    # 创建深色渐变背景（从上到下由深蓝到黑）
    frame = Image.new("RGB", (display.width, display.height), (10, 10, 30))
    draw = ImageDraw.Draw(frame)

    # 手动渐变（简单叠加）
    for y in range(display.height):
        r = int(10 * (1 - y/display.height))
        g = int(10 * (1 - y/display.height))
        b = int(30 + 30 * (y/display.height))
        draw.rectangle((0, y, display.width, y+1), fill=(r, g, b))

    # 标题（带阴影）
    title = "Ultrasonic Distance"
    draw.text((6, 6), title, font=title_font, fill=(0, 0, 0))
    draw.text((5, 5), title, font=title_font, fill=(0, 255, 255))

    # 距离数值（大号，带阴影）
    if dist is not None:
        text = f"{dist:.1f} cm"
        # 获取文字尺寸
        bbox = draw.textbbox((0, 0), text, font=value_font)
        text_w = bbox[2] - bbox[0]
        x = (display.width - text_w) // 2
        y = 40
        # 黑色阴影
        draw.text((x+2, y+2), text, font=value_font, fill=(0, 0, 0))
        # 亮黄色数字
        draw.text((x, y), text, font=value_font, fill=(255, 255, 0))
    else:
        draw.text((20, 40), "Out of range", font=title_font, fill=(255, 0, 0))

    # 进度条（圆角矩形，颜色随距离变化）
    max_dist = 100.0
    bar_x = 20
    bar_y = 100
    bar_width = 88
    bar_height = 20

    # 背景条（灰色圆角）
    draw.rounded_rectangle((bar_x, bar_y, bar_x+bar_width, bar_y+bar_height),
                           radius=8, fill=(40, 40, 40))

    if dist is not None:
        ratio = min(dist / max_dist, 1.0)
        fill_width = int(bar_width * ratio)
        if fill_width > 0:
            # 动态颜色：绿→黄→红
            if ratio < 0.5:
                color = (0, 255, 0)          # 绿
            elif ratio < 0.8:
                color = (255, 255, 0)        # 黄
            else:
                color = (255, 0, 0)          # 红
            draw.rounded_rectangle((bar_x, bar_y, bar_x+fill_width, bar_y+bar_height),
                                   radius=8, fill=color)

        # 刻度文字
        draw.text((bar_x-12, bar_y+2), "0", font=title_font, fill=(150,150,150))
        draw.text((bar_x+bar_width+2, bar_y+2), "100", font=title_font, fill=(150,150,150))
    else:
        draw.text((bar_x+10, bar_y+2), "No signal", font=title_font, fill=(255,0,0))

    # 添加单位提示
    draw.text((display.width-20, display.height-10), "cm", font=title_font, fill=(100,100,100))

    display.image(frame)

print("超声波距离可视化启动（PIL 美观版）")
try:
    while True:
        dist = get_distance()
        draw_dashboard(dist)
        if dist is not None:
            print(f"✅ 距离: {dist} cm")
        else:
            print("⚠️ 无信号")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\n程序结束")
finally:
    # 清屏并释放 GPIO
    display.image(Image.new("RGB", (display.width, display.height), (0, 0, 0)))
    GPIO.cleanup()