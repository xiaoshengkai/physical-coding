# 13 - 摄像头拍照

## 实验目标

在 TFT 屏幕取景器基础上，增加拍照按钮功能。

## 硬件准备

- 树莓派 4B
- 1.8 寸 ST7735 TFT 屏幕
- Raspberry Pi Camera Module 1.3
- 普通按键一个
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
| RST | GPIO27 | Pin 13 |

### 按钮

| 按钮引脚 | 树莓派 GPIO | 物理引脚 |
|----------|-------------|----------|
| 一端 | GPIO26 | Pin 37 |
| 另一端 | GND | Pin 6 |

## 软件准备

```bash
pip install picamera2 adafruit-circuitpython-rgb-display pillow gpiozero
```

## 运行代码

```bash
python demos/13-camera-photo/main.py
```

或使用快速命令：

```bash
npm run run 13
```

## 效果

- TFT 屏幕实时显示摄像头取景
- 按下按钮：保存当前画面为 JPEG（带时间戳）
- 屏幕显示绿色"Photo saved!"提示 1 秒
- 照片保存在 `/home/xiaoshengkai/Desktop/photos/`
- 按 Ctrl+C 退出