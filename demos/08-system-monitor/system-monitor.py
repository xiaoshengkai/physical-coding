#!/usr/bin/env python3
"""
树莓派系统监视器（高级版·中文标签）
适用于 ST7735 128x160 TFT 屏幕，CS 接 GPIO5，DC 接 GPIO25
显示：CPU 使用率+频率、内存、温度、磁盘、网络速度、IP+时间
"""

import digitalio
import busio
import board
from adafruit_rgb_display import st7735
from PIL import Image, ImageDraw, ImageFont
import time
import psutil
import socket

# ================== 初始化屏幕 ==================
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)      # CS 接 GPIO5
dc = digitalio.DigitalInOut(board.D25)     # DC 接 GPIO25
display = st7735.ST7735R(
    spi, cs=cs, dc=dc,
    width=128, height=160,
    baudrate=24000000
)

# ================== 字体加载 ==================
font_path = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
try:
    font_label = ImageFont.truetype(font_path, 12)   # 标签字体
    font_value = ImageFont.truetype(font_path, 11)   # 数值字体
    font_small = ImageFont.truetype(font_path, 10)   # 小字
except:
    font_label = ImageFont.load_default()
    font_value = ImageFont.load_default()
    font_small = ImageFont.load_default()

# ================== 颜色定义 ==================
BG_COLOR = (0, 0, 0)                # 背景黑色
PANEL_COLOR = (20, 20, 30)          # 面板底色
TITLE_COLOR = (0, 255, 255)         # 标题青色
TEXT_COLOR = (220, 220, 255)        # 文字浅蓝白
BAR_BORDER = (100, 100, 150)        # 进度条边框

# 网络速度追踪
last_net = psutil.net_io_counters()
last_time = time.time()

def get_gradient_color(percent, start_color, end_color):
    r = int(start_color[0] + (end_color[0] - start_color[0]) * percent / 100)
    g = int(start_color[1] + (end_color[1] - start_color[1]) * percent / 100)
    b = int(start_color[2] + (end_color[2] - start_color[2]) * percent / 100)
    return (r, g, b)

def draw_progress(draw, x, y, w, h, percent, low_color, high_color):
    # 边框（尝试圆角）
    try:
        draw.rounded_rectangle((x, y, x+w, y+h), radius=3, outline=BAR_BORDER, width=1)
    except AttributeError:
        draw.rectangle((x, y, x+w, y+h), outline=BAR_BORDER, width=1)

    # 填充
    if percent > 0:
        fill_w = int(w * percent / 100)
        if fill_w > 0:
            color = get_gradient_color(percent, low_color, high_color)
            draw.rectangle((x+1, y+1, x+fill_w, y+h-1), fill=color)

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except:
        ip = 'No IP'
    finally:
        s.close()
    return ip

def get_cpu_temp():
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            return int(f.read()) / 1000.0
    except:
        return 0.0

# ================== 主循环 ==================
print("🚀 系统监视器（高级版）启动，按 Ctrl+C 停止")
try:
    while True:
        frame = Image.new("RGB", (display.width, display.height), BG_COLOR)
        draw = ImageDraw.Draw(frame)

        # 系统数据
        cpu_percent = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory()
        temp = get_cpu_temp()
        disk = psutil.disk_usage('/')
        ip = get_ip()
        now = time.strftime("%H:%M:%S")
        freq = psutil.cpu_freq().current / 1000.0

        # 网络速度
        current_net = psutil.net_io_counters()
        current_time = time.time()
        elapsed = current_time - last_time
        if elapsed > 0:
            down_speed = (current_net.bytes_recv - last_net.bytes_recv) / elapsed / 1024
            up_speed = (current_net.bytes_sent - last_net.bytes_sent) / elapsed / 1024
        else:
            down_speed = up_speed = 0
        last_net = current_net
        last_time = current_time

        # ----- 标题区域 -----
        draw.rectangle((0, 0, 128, 16), fill=PANEL_COLOR)
        draw.text((8, 2), "系统监视器", font=font_label, fill=TITLE_COLOR)
        draw.line((0, 16, 128, 16), fill=(40,40,50), width=1)

        # 增加标题与第一行之间的空隙（y_start 从 18 改为 22）
        y_start = 22          # 原来为 18，增加 4 像素间隙
        line_height = 20      # 每行高度

        # ----- CPU 行 -----
        draw.text((2, y_start), "CPU", font=font_label, fill=TEXT_COLOR)
        draw.text((28, y_start), f"{cpu_percent:3.0f}%", font=font_value, fill=TEXT_COLOR)
        draw.text((58, y_start), f"{freq:.1f}G", font=font_small, fill=(200,200,100))
        # 进度条位置相应下移（原来 y_start+12，现改为 y_start+14）
        draw_progress(draw, 2, y_start+14, 70, 5, cpu_percent,
                      (0,200,0), (200,50,50))

        # ----- 内存行 -----
        y_start += line_height
        draw.text((2, y_start), "内存", font=font_label, fill=TEXT_COLOR)
        draw.text((28, y_start), f"{mem.percent:3.0f}%", font=font_value, fill=TEXT_COLOR)
        draw_progress(draw, 2, y_start+14, 70, 5, mem.percent,
                      (0,200,0), (200,200,0))

        # ----- 温度行 -----
        y_start += line_height
        draw.text((2, y_start), "温度", font=font_label, fill=TEXT_COLOR)
        draw.text((28, y_start), f"{temp:5.1f}°C", font=font_value, fill=TEXT_COLOR)
        temp_percent = min(100, int(temp / 85 * 100))
        draw_progress(draw, 2, y_start+14, 70, 5, temp_percent,
                      (0,200,200), (255,100,0))

        # ----- 磁盘行 -----
        y_start += line_height
        draw.text((2, y_start), "磁盘", font=font_label, fill=TEXT_COLOR)
        draw.text((28, y_start), f"{disk.percent:3.0f}%", font=font_value, fill=TEXT_COLOR)
        draw_progress(draw, 2, y_start+14, 70, 5, disk.percent,
                      (100,200,255), (200,100,255))

        # ----- 网络速度行 -----
        y_start += line_height
        draw.text((2, y_start), "↓", font=font_label, fill=TEXT_COLOR)
        draw.text((12, y_start), f"{down_speed:5.1f}", font=font_small, fill=(100,255,100))
        draw.text((42, y_start), "↑", font=font_label, fill=TEXT_COLOR)
        draw.text((52, y_start), f"{up_speed:5.1f}", font=font_small, fill=(255,100,100))
        draw.text((90, y_start), "KB/s", font=font_small, fill=(150,150,150))

        # ----- IP + 时间行 -----
        y_start += line_height
        draw.rectangle((2, y_start, 126, y_start+16), fill=PANEL_COLOR)
        draw.text((4, y_start+2), ip, font=font_small, fill=TEXT_COLOR)
        time_width = font_small.getlength(now)
        draw.text((126 - time_width - 2, y_start+2), now, font=font_small, fill=(255,255,100))

        display.image(frame)
        time.sleep(1)

except KeyboardInterrupt:
    pass
finally:
    display.image(Image.new("RGB", (display.width, display.height), BG_COLOR))
    print("\n👋 监视器已停止")