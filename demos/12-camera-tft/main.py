import digitalio
import busio
import board
from adafruit_rgb_display import st7735
from PIL import Image
from picamera2 import Picamera2
from libcamera import controls
import time

# 屏幕初始化
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
dc = digitalio.DigitalInOut(board.D25)
display = st7735.ST7735R(spi, cs=cs, dc=dc, width=128, height=160, baudrate=8000000)

# 摄像头初始化
picam2 = Picamera2()
# 提高采集分辨率，建议 640x480
config = picam2.create_preview_configuration(
    main={"size": (640, 480), "format": "RGB888"},
    controls={"FrameRate": 30}
)
picam2.configure(config)
# 手动白平衡（避免环境光影响）
picam2.set_controls({
    "AwbEnable": False,
    "ColourGains": (1.3, 0.9)   # 可根据环境微调
})
picam2.start()
time.sleep(2)  # 预热

print("取景器已启动，按 Ctrl+C 退出")
try:
    while True:
        frame = picam2.capture_array()
        if frame is None:
            continue
        img = Image.fromarray(frame)
        # 使用高质量缩放算法
        img = img.resize((display.width, display.height), Image.Resampling.LANCZOS)
        display.image(img)
        # 控制帧率约 20-30fps（无需精确延时，防止过快）
        time.sleep(0.03)
except KeyboardInterrupt:
    print("退出")
finally:
    picam2.stop()
    display.image(Image.new("RGB", (display.width, display.height), (0, 0, 0)))