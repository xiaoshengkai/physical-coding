# 09 - TFT 系统监视器

## 实验目标

在 1.8 英寸 SPI 接口 TFT 彩屏上显示树莓派系统实时监控数据（CPU、内存、温度、磁盘、IP、时间）。

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

# 安装 psutil 系统监控库
pip3 install psutil

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
python demos/09-system-monitor/system-monitor.py
```

或使用快速命令：

```bash
npm run run 09
```

## 效果

屏幕实时显示：
- 系统标题
- CPU 使用率（带进度条）
- 内存使用率（带进度条）
- CPU 温度
- 磁盘使用率（带进度条）
- IP 地址
- 当前时间

## 关键知识点

1. **psutil 库**: Python 系统监控工具
2. **实时数据采集**: 获取 CPU、内存、磁盘等系统信息
3. **进度条绘制**: 使用 PIL 绘制可视化进度条

## 常见问题

**无法显示系统信息？**
- 确认 psutil 已正确安装
- 检查 SPI 接线是否正确

**中文显示为方块？**
- 安装中文字体：`sudo apt install fonts-wqy-microhei`

**显示刷新太慢？**
- 调整 `time.sleep()` 参数
