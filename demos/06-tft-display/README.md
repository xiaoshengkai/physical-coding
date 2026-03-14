# 06 - TFT 彩屏显示

## 实验目标

使用 1.8 英寸 SPI 接口 TFT 彩屏显示 "Hello Pi!"。

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

# 安装 luma.lcd
pip3 install luma.lcd

# （可选）安装中文字体，用于显示中文
sudo apt install fonts-wqy-microhei
```

## 引脚分配

| 屏幕引脚 | 树莓派 GPIO | 物理引脚 | 说明 |
|----------|-------------|----------|------|
| VCC | 3.3V | Pin 1 | 供电（必须 3.3V，不能接 5V！） |
| GND | GND | Pin 6 | 共地 |
| SDI | GPIO10 (MOSI) | Pin 19 | SPI 数据输入 |
| CLK | GPIO11 (SCLK) | Pin 23 | SPI 时钟 |
| CS | GPIO8 (CE0) | Pin 24 | 片选（低电平有效） |
| DC | GPIO25 | Pin 22 | 数据/命令选择 |
| SDO | 不接 | - | 数据输出，悬空即可 |

## 接线图

```
[树莓派]           [TFT 模块]
3.3V (Pin 1)   ──── VCC
GND   (Pin 6)   ──── GND
GPIO10(Pin 19)  ──── SDI (MOSI)
GPIO11(Pin 23)  ──── CLK (SCLK)
GPIO8 (Pin 24)  ──── CS
GPIO25(Pin 22)  ──── DC
```

## 运行代码

```bash
python demos/06-tft-display/tft-display.py
```

或使用快速命令：

```bash
npm run run 06
```

## 效果

屏幕显示：
- 深蓝色背景
- 黄色文字 "Hello Pi!"
- 青色文字 "TFT Works"
- 几何图形测试

## 关键知识点

1. **SPI 通信协议**: 了解 SPI 的时钟、数据输入、片选等信号
2. **TFT 驱动**: 理解 ST7735 控制器的初始化流程
3. **PIL 绘图**: 使用 Python Imaging Library 绘制图形和文字

## 常见问题

**屏幕不显示？**
- 检查所有接线是否牢固
- 确认 BLK 接 5V（背光）
- 检查 CS、D/C 接线是否正确

**显示模糊？**
- 尝试调整 `rotate` 参数（0, 1, 2, 3）

**颜色显示异常？**
- 检查 SDI (MOSI) 和 CLK 接线是否正确
