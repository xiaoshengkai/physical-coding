import digitalio
import busio
import board
from adafruit_rgb_display import st7735
from PIL import Image
import cv2
import time
import urllib.request
import os

# 初始化屏幕 (128x160)，降低SPI速度到8MHz提高稳定性
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
dc = digitalio.DigitalInOut(board.D25)
display = st7735.ST7735R(spi, cs=cs, dc=dc, width=128, height=160, baudrate=8000000)

# 视频路径（你的本地小视频）
local_video_path = (
    "/home/xiaoshengkai/Desktop/workspace/PhysicalCoding/static/videos/small_video.mp4"
)
online_video_url = (
    "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
)
online_video_path = "/tmp/big_buck_bunny.mp4"


def download_video(url, path):
    print(f"Downloading video from: {url}")
    try:
        urllib.request.urlretrieve(url, path)
        print("Download completed!")
        return True
    except Exception as e:
        print(f"Download failed: {e}")
        return False


# 尝试打开本地视频
cap = cv2.VideoCapture(local_video_path)
if not cap.isOpened():
    print("Cannot open local video, trying online video...")
    if download_video(online_video_url, online_video_path):
        cap = cv2.VideoCapture(online_video_path)
    else:
        print("Cannot open any video")
        exit()

if not cap.isOpened():
    print("Cannot open any video")
    exit()

# 获取原始视频尺寸和帧率
orig_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
orig_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
print(f"Video info: {orig_width}x{orig_height}, {fps:.2f} fps")

# 强制目标帧率（不超过15fps，减轻处理压力）
target_fps = min(fps, 15) if fps > 0 else 10
frame_time = 1.0 / target_fps

# 预计算缩放尺寸（保持比例，居中裁剪为屏幕尺寸）
screen_w, screen_h = display.width, display.height
scale = max(screen_w / orig_width, screen_h / orig_height)
new_w = int(orig_width * scale)
new_h = int(orig_height * scale)
crop_x = (new_w - screen_w) // 2
crop_y = (new_h - screen_h) // 2

print(f"Target playback speed: {target_fps} fps")

try:
    while True:
        loop_start = time.time()

        ret, frame = cap.read()
        if not ret:
            # 循环播放
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        # BGR → RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)

        # 缩放并裁剪到屏幕尺寸（避免全图缩放导致的变形）
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        img = img.crop((crop_x, crop_y, crop_x + screen_w, crop_y + screen_h))

        # 显示
        display.image(img)

        # 控制帧率
        elapsed = time.time() - loop_start
        if elapsed < frame_time:
            time.sleep(frame_time - elapsed)
except KeyboardInterrupt:
    pass
finally:
    cap.release()
    display.image(Image.new("RGB", (screen_w, screen_h), (0, 0, 0)))
    print("\nPlayback stopped")
