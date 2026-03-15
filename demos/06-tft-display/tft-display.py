import digitalio
import busio
import board
from adafruit_rgb_display import st7735
from PIL import Image, ImageDraw, ImageFont
import time

# 初始化屏幕
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
dc = digitalio.DigitalInOut(board.D25)
display = st7735.ST7735R(spi, cs=cs, dc=dc, width=128, height=160, baudrate=24000000)

# 加载中文字体（请确保字体文件存在）
font_path = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
try:
    font = ImageFont.truetype(font_path, 16)
except:
    print("字体加载失败，使用默认字体（中文可能显示为方块）")
    font = ImageFont.load_default()

text = "樊淑颖，你最棒！"

# 获取文字尺寸（先用一张临时图片测量）
temp_img = Image.new("RGB", (1, 1))
temp_draw = ImageDraw.Draw(temp_img)
bbox = temp_draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

# 屏幕尺寸
screen_width = display.width
screen_height = display.height

# 初始位置（从右侧外开始）
x = screen_width
y = (screen_height - text_height) // 2
speed = 2
direction = -1  # 向左移动

print("滚动显示开始，按 Ctrl+C 退出")
try:
    while True:
        # 创建黑色背景的画布
        frame = Image.new("RGB", (screen_width, screen_height), (0, 0, 0))
        draw = ImageDraw.Draw(frame)
        draw.text((x, y), text, font=font, fill=(255, 255, 255))

        # 显示到屏幕
        display.image(frame)

        # 更新位置
        x += speed * direction

        # 边界反转
        if x + text_width < 0:  # 完全移出左侧
            x = 0
            direction = 1
        elif x > screen_width:  # 完全移出右侧
            x = screen_width - text_width
            direction = -1

        time.sleep(0.05)
except KeyboardInterrupt:
    # 退出清屏
    display.image(Image.new("RGB", (screen_width, screen_height), (0, 0, 0)))
    print("\n程序结束")
