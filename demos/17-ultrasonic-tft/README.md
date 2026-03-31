# 17 - 超声波测距可视化

## 实验目标

将 HC-SR04 超声波测得的距离实时显示在 TFT 屏幕上，并用动态柱状图直观表示。

## 硬件准备

- 树莓派 4B
- HC-SR04 超声波传感器模块
- 10kΩ 电阻 × 2
- 1.8 寸 ST7735 TFT 屏幕
- 杜邦线若干

## 硬件连接

### TFT 屏幕（ST7735）

| 屏幕引脚 | 树莓派 GPIO | 物理引脚 |
|----------|-------------|----------|
| VCC | 3.3V | Pin 1 |
| GND | GND | Pin 6 |
| SDI | GPIO10 (MOSI) | Pin 19 |
| CLK | GPIO11 (SCLK) | Pin 23 |
| CS | GPIO5 | Pin 29 |
| DC | GPIO25 | Pin 22 |

### HC-SR04 超声波

| 模块 | 树莓派 GPIO | 物理引脚 |
|------|-------------|----------|
| VCC | 5V | Pin 2 |
| GND | GND | Pin 6 |
| Trig | GPIO23 | Pin 16 |
| Echo | GPIO24（经分压） | Pin 18 |

### 分压电路（两只 10kΩ 电阻）

```
HC-SR04 Echo ──┬── 10kΩ ──┬── GPIO24
                │           │
                │          10kΩ
                │           │
                GND        GND
```

## 软件准备

1. 安装依赖：

```bash
pip install Pillow
pip install adafruit-circuitpython-rgb-display
sudo apt install python3-rpi.gpio
```

**Pillow**：Python 图像处理库，用于在 TFT 屏幕上绘制文字、图形、柱状图等界面元素。

2. 查找中文字体路径：

```bash
fc-list :lang=zh file
```

找到字体后修改代码中的 `font_path` 路径。

## 运行代码

```bash
python demos/17-ultrasonic-tft/main.py
```

或使用快速命令：

```bash
npm run run 17
```

## 效果

- TFT 屏幕显示当前距离数值（cm）
- 垂直柱状图实时反映距离变化
  - 距离越近，柱子越高
  - 距离越远，柱子越低
- 按 Ctrl+C 退出