# 08 - TFT 视频播放

## 实验目标

在 1.8 英寸 SPI 接口 TFT 彩屏上播放小视频。

## 硬件准备

- 树莓派 4B
- 1.8 英寸 ST7735 TFT 彩屏模块
- 杜邦线 7 根

## 软件准备

### 1. 启用 SPI 接口

首次使用需要启用 SPI 接口：

```bash
sudo raspi-config
```

选择 **Interface Options** → **SPI** → **Enable** → 重启树莓派

或者直接检查是否已启用：

```bash
ls /dev/spi*
```

如果看到 `/dev/spidev0.0` 和 `/dev/spidev0.1`，说明 SPI 已启用。

### 2. 安装依赖

```bash
# 安装必要的系统依赖
sudo apt update
sudo apt install python3-dev python3-pip libfreetype6-dev libjpeg-dev build-essential
sudo apt install python3-smbus python3-spidev

# 安装 adafruit-circuitpython-rgb-display 库
pip3 install adafruit-circuitpython-rgb-display

# 安装 OpenCV
pip3 install opencv-python-headless Pillow
```

### 3. 准备视频

将视频文件复制到树莓派的 `~/Desktop/workspace/PhysicalCoding/static/videos/` 目录：

```bash
# 在本地创建目录并放入视频
mkdir -p static/videos
# 将你的视频重命名为 small_video.mp4 放入 static/videos 目录
```

视频要求：
- 分辨率接近 128x160
- 建议使用较小尺寸的视频文件
- 格式支持 MP4、AVI 等常见格式

## 引脚分配

| 屏幕引脚 | 树莓派 GPIO | 物理引脚 | 说明 |
|----------|-------------|----------|------|
| VCC | 3.3V | Pin 1 | 供电（必须 3.3V，不能接 5V！） |
| GND | GND | Pin 6 | 共地 |
| SDI | GPIO10 (MOSI) | Pin 19 | SPI 数据输入 |
| CLK | GPIO11 (SCLK) | Pin 23 | SPI 时钟 |
| CS | GPIO5 | Pin 29 | 片选（低电平有效） |
| DC | GPIO25 | Pin 22 | 数据/命令选择 |
| SDO | 不接 | - | 数据输出，悬空即可 |

## 接线图

```
[树莓派]           [TFT 模块]
3.3V (Pin 1)   ──── VCC
GND   (Pin 6)   ──── GND
GPIO10(Pin 19)  ──── SDI (MOSI)
GPIO11(Pin 23)  ──── CLK (SCLK)
GPIO5 (Pin 29)  ──── CS
GPIO25(Pin 22)  ──── DC
```

## 运行代码

```bash
python demos/08-tft-video/tft-video.py
```

或使用快速命令：

```bash
npm run run 08
```

## 效果

屏幕循环播放指定视频文件 `small_video.mp4`。

## 关键知识点

1. **OpenCV 视频处理**: 使用 OpenCV 读取和解析视频文件
2. **视频帧提取**: 从视频中逐帧提取图像
3. **实时显示**: 将视频帧实时显示到 TFT 屏幕

## 常见问题

**视频无法播放？**
- 检查视频文件路径是否正确
- 确认视频格式和编码被 OpenCV 支持
- 检查 SPI 接线是否正确

**播放卡顿？**
- 降低视频分辨率
- 降低帧率
- 尝试降低 baudrate

**色彩异常？**
- 检查 BGR 转 RGB 是否正确
