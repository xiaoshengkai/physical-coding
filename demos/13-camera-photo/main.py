import time
import digitalio
import busio
import board
from adafruit_rgb_display import st7735
from PIL import Image, ImageDraw, ImageFont
from picamera2 import Picamera2
from gpiozero import Button
import os

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
    spi, cs=cs, dc=dc, rst=rst, width=128, height=160, baudrate=10000000
)

btn = Button(26, pull_up=True)

picam2 = Picamera2()
config = picam2.create_preview_configuration(
    main={"size": (640, 480), "format": "RGB888"}, controls={"FrameRate": 30}
)
picam2.configure(config)
picam2.set_controls({"AwbEnable": True})
picam2.start()
time.sleep(1)

screen_size = (display.width, display.height)

photo_dir = "/home/xiaoshengkai/Desktop/workspace/PhysicalCoding/demos/13-camera-photo/photos"
os.makedirs(photo_dir, exist_ok=True)

try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
except:
    font = ImageFont.load_default()


def reduce_blue(image, factor=0.7):
    r, g, b = image.split()
    b = b.point(lambda x: int(x * factor))
    return Image.merge("RGB", (r, g, b))


def show_message(text, duration=1):
    msg_img = Image.new("RGB", screen_size, (0, 0, 0))
    draw = ImageDraw.Draw(msg_img)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (screen_size[0] - text_w) // 2
    y = (screen_size[1] - text_h) // 2
    draw.text((x, y), text, font=font, fill=(0, 255, 0))
    display.image(msg_img)
    time.sleep(duration)


def capture_photo():
    img = picam2.capture_image()
    r, g, b = img.split()
    img = Image.merge("RGB", (b, g, r))
    img = reduce_blue(img, factor=0.7)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"{photo_dir}/photo_{timestamp}.jpg"
    img.save(filename)
    print(f"照片已保存：{filename}")
    show_message("Photo saved!", duration=1)


print("取景器已启动，按按钮拍照，按 Ctrl+C 退出")
try:
    while True:
        img = picam2.capture_image()
        r, g, b = img.split()
        img = Image.merge("RGB", (b, g, r))
        img = reduce_blue(img, factor=0.7)
        img = img.resize(screen_size, Image.Resampling.NEAREST)
        display.image(img)

        if btn.is_pressed:
            time.sleep(0.05)
            if btn.is_pressed:
                capture_photo()
                while btn.is_pressed:
                    time.sleep(0.01)
except KeyboardInterrupt:
    print("退出")
finally:
    picam2.stop()
    display.image(Image.new("RGB", screen_size, (0, 0, 0)))
