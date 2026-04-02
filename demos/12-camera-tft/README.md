# 12 - TFT 屏幕取景器

## 实验目标

使用摄像头实时拍摄，将画面显示在 128x160 TFT 屏幕上。

## 硬件准备

- 树莓派 4B
- 1.8 寸 ST7735 TFT 屏幕
- Raspberry Pi Camera Module 1.3
- 摄像头排线
- 杜邦线若干

## 硬件连接

### TFT 屏幕

| 屏幕引脚 | 树莓派 GPIO | 物理引脚 |
|----------|-------------|----------|
| VCC | 3.3V | Pin 1 |
| GND | GND | Pin 6 |
| SDI (MOSI) | GPIO10 | Pin 19 |
| CLK (SCLK) | GPIO11 | Pin 23 |
| CS | GPIO5 | Pin 29 |
| DC | GPIO25 | Pin 22 |

### 摄像头

CSI 接口（HDMI 接口和音频口之间），排线金属触点朝下。

## 软件准备

安装依赖：

```bash
pip install picamera2 adafruit-circuitpython-rgb-display pillow
```

## 运行代码

```bash
python demos/12-camera-tft/main.py
```

或使用快速命令：

```bash
npm run run 12
```

## 效果

- TFT 屏幕实时显示摄像头画面
- 帧率约 15-20 fps
- 按 Ctrl+C 退出