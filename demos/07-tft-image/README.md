# 07 - TFT 图片显示

## 实验目标

在 1.8 英寸 SPI 接口 TFT 彩屏上显示一张图片。

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
```

### 3. 准备图片

将图片文件 `g.jpg` 复制到树莓派的 `~/Desktop/workspace/PhysicalCoding/static/images/` 目录：

```bash
# 在本地创建目录并放入图片
mkdir -p static/images
# 将你的图片重命名为 g.jpg 放入 static/images 目录
```

图片要求：
- 建议尺寸 128x128 像素
- 格式支持 JPG、PNG 等常见格式

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
python demos/07-tft-image/tft-image.py
```

或使用快速命令：

```bash
npm run run 07
```

## 效果

屏幕显示指定的图片文件 `g.jpg`。

## 关键知识点

1. **adafruit-circuitpython-rgb-display**: 官方树莓派显示库
2. **PIL 图像处理**: 使用 Python Imaging Library 处理和缩放图片
3. **图片居中显示**: thumbnail + 创建背景画布实现居中

## 常见问题

**图片不显示？**
- 检查图片路径是否正确
- 确认图片文件存在且格式正确
- 检查 SPI 接线是否正确
- 确认库已正确安装

**图片显示变形？**
- 尝试调整缩放方式

**色彩异常？**
- 检查图片模式是否为 RGB
