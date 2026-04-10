# 实验 21 - DIY 相机

这是一个综合项目，将多个模块集成在一起，构建一个功能完整的 DIY 相机。

## 硬件清单

| 组件 | 数量 | 备注 |
|------|------|------|
| 树莓派 4B | 1 | 主控 |
| 摄像头 v1.3 | 1 | CSI 接口 |
| 3.5寸 SPI 屏幕 ST779 | 1 | 480x320 |
| 旋转编码器 KY-040 | 1 | 带按钮 |
| 按键 | 3 | 拍照、录像、菜单 |
| 蜂鸣器 | 1 | 无源 |

## 接线

### 屏幕 (ST779, 3.5寸 480x320)

| 屏幕引脚 | 功能 | 树莓派 GPIO | 物理引脚 | 备注 |
|----------|------|-------------|----------|------|
| VCC | 电源 (5V) | 5V | Pin 2/4 | 必须接 5V，否则背光不亮 |
| GND | 地 | GND | Pin 6 | 共地 |
| SCLK / SCK | SPI 时钟 | GPIO11 | Pin 23 | SPI 时钟线 |
| MOSI / SDI | SPI 数据 | GPIO10 | Pin 19 | 数据线 |
| CS / SS | 片选 | GPIO7 (CE1) | Pin 26 |
| DC / RS | 数据/命令 | GPIO25 | Pin 22 | 数据/命令选择 |
| RST | 复位 | GPIO27 | Pin 13 | 大多数驱动需要 |
| BL | 背光 | 3.3V | Pin 1 | 背光供电 |

### 旋转编码器 (KY-040)

| 编码器 | 树莓派 GPIO | 物理引脚 |
|--------|-------------|----------|
| CLK | GPIO17 | Pin 11 |
| DT | GPIO18 | Pin 12 |
| SW | GPIO22 | Pin 15 |
| VCC | 3.3V | Pin 1 |
| GND | GND | Pin 6 |

### 其他

| 模块 | GPIO | 物理引脚 |
|------|------|----------|
| 拍照按钮 | GPIO26 | Pin 37 |
| 蜂鸣器 | GPIO21 | Pin 40 |

## 依赖安装

### 1. 启用 SPI 接口

```bash
sudo raspi-config
```

选择 **Interface Options** → **SPI** → **Enable** → 重启树莓派

或者直接检查是否已启用：

```bash
ls /dev/spi*
```

如果看到 `/dev/spidev0.0` 和 `/dev/spidev0.1`，说明 SPI 已启用。

### 2. 安装 Python 库

```bash
sudo apt update
sudo pip3 install adafruit-circuitpython-rgb-display pillow gpiozero picamera2
```

## 运行测试

```bash
cd demos/21-diy-camera
python3 main.py
```

按数字选择测试各个模块。

## 项目阶段

### Phase 1: 点亮屏幕

显示红、绿、蓝纯色，确认驱动正常。

### Phase 2: 旋转编码器

读取旋钮方向和按钮按下事件。

### Phase 3: 摄像头取景

实时显示摄像头画面在屏幕上。

### Phase 4: 按键拍照 + 蜂鸣器提示

按下按键拍照，蜂鸣器响一声。

### Phase 5: 数码变焦

旋钮控制变焦倍数 (1x-4x)。

### Phase 6: 录像

长按切换拍照/录像模式。

### Phase 7: 菜单界面

OSD 菜单调整白平衡等参数。

## 引脚约定

- 屏幕 CS → GPIO8
- 屏幕 DC → GPIO25
- 屏幕 RST → GPIO27
- 旋钮 CLK → GPIO17, DT → GPIO18, SW → GPIO22
- 拍照按钮 → GPIO26
- 蜂鸣器 → GPIO21