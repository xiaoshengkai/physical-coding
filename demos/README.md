# Demo 实验列表

本目录包含所有嵌入式实验的示例代码和文档。

## 实验清单

### 01. LED Blink - 点亮第一盏 LED

**难度**: ⭐

**描述**: 学习最基础的 GPIO 输出控制，点亮一颗 LED 灯

**涉及内容**:
- 树莓派 GPIO 基础
- 电路连接（LED + 电阻）
- Python/Node.js 控制 GPIO

[查看详情](./01-led-blink/README.md)

---

### 02. LED Breathing - 呼吸灯效果

**难度**: ⭐⭐

**描述**: 使用 PWM 实现 LED 亮度渐变

**涉及内容**:
- PWM 脉宽调制
- 软件 PWM vs 硬件 PWM

[查看详情](./02-led-breathing/README.md)

---

### 03. LED Marquee - 跑马灯效果

**难度**: ⭐⭐

**描述**: 控制多颗 LED 依次点亮

**涉及内容**:
- 多 GPIO 口控制
- 循环与延时

[查看详情](./03-led-marquee/README.md)

---

### 04. Traffic Light - 交通灯控制

**难度**: ⭐⭐⭐

**描述**: 模拟真实交通灯红绿黄切换

**涉及内容**:
- 状态机设计
- 定时器应用

[查看详情](./04-traffic-light/README.md)

---

### 05. 7-Segment Display - 数码管显示

**难度**: ⭐⭐⭐

**描述**: 使用 TM1637 数码管模块显示数字和字母

**涉及内容**:
- I2C 协议模拟
- 数码管编码
- 多位显示

[查看详情](./05-7segment-display/README.md)

---

### 06. TFT Display - TFT 彩屏显示

**难度**: ⭐⭐⭐

**描述**: 使用 1.8 英寸 ST7735 TFT 彩屏显示文字

**涉及内容**:
- SPI 通信协议
- TFT 驱动原理
- PIL 绘图基础

[查看详情](./06-tft-display/README.md)

---

### 07. TFT Image - TFT 图片显示

**难度**: ⭐⭐⭐

**描述**: 在 1.8 英寸 ST7735 TFT 彩屏上显示图片

**涉及内容**:
- PIL 图像处理
- 图片格式转换
- 图像缩放

[查看详情](./07-tft-image/README.md)

---

### 08. TFT Video - TFT 视频播放

**难度**: ⭐⭐⭐⭐

**描述**: 在 1.8 英寸 ST7735 TFT 彩屏上播放小视频

**涉及内容**:
- OpenCV 视频处理
- 视频帧提取
- 实时显示

[查看详情](./08-tft-video/README.md)

---

### 09. System Monitor - TFT 系统监视器

**难度**: ⭐⭐⭐⭐

**描述**: 在 1.8 英寸 ST7735 TFT 彩屏上显示树莓派系统监控数据

**涉及内容**:
- psutil 系统监控
- 实时数据采集
- 进度条绘制

[查看详情](./09-system-monitor/README.md)

---

## 如何添加新实验

1. 在 `demos/` 目录下创建新文件夹，命名格式：`XX-experiment-name`
2. 创建 `README.md` 文档
3. 添加实验代码（Python 或 Node.js）
4. 更新本目录
