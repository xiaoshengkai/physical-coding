from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.lcd.device import st7735
from PIL import ImageFont, ImageDraw
import time

# 初始化 SPI（根据你之前的成功配置调整）
serial = spi(port=0, device=0, gpio_DC=25, gpio_RST=None)
device = st7735(serial, width=128, height=128, rotate=0)  # 若你的屏幕是128x160则改回

# 加载中文字体
font_path = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
try:
    font = ImageFont.truetype(font_path, 16)  # 字号16，可调整
    print("✅ 中文字体加载成功")
except Exception as e:
    print("⚠️ 未找到中文字体，将使用默认字体（中文可能显示为方块）")
    font = ImageFont.load_default()

text = "樊淑颖，你最棒！"

# 获取文本尺寸（兼容新版 Pillow）
bbox = font.getbbox(text)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

# 屏幕尺寸
screen_width = device.width
screen_height = device.height

# 初始位置（从右侧外开始向左移动）
x = screen_width
y = (screen_height - text_height) // 2  # 垂直居中

# 移动速度（像素/帧）
speed = 2

# 方向：-1 向左，1 向右
direction = -1

print("🚀 开始滚动显示... 按 Ctrl+C 停止")

try:
    while True:
        with canvas(device) as draw:
            # 清屏（黑色背景）
            draw.rectangle(device.bounding_box, outline="black", fill="black")
            # 绘制文字（白色）
            draw.text((x, y), text, font=font, fill="white")
        
        # 更新位置
        x += speed * direction
        
        # 边界判断：当文字完全移出左侧时，改为向右移动
        if x + text_width < 0:
            x = 0
            direction = 1
        # 当文字完全移出右侧时，改为向左移动
        elif x > screen_width:
            x = screen_width - text_width
            direction = -1
        
        # 控制帧率
        time.sleep(0.05)
except KeyboardInterrupt:
    # 退出时清屏
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="black", fill="black")
    print("\n👋 程序结束")