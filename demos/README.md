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

### 10. Stopwatch - 按键控制秒表

**难度**: ⭐⭐⭐

**描述**: 使用两个按键控制数码管秒表，实现开始/暂停和复位功能

**涉及内容**:
- gpiozero Button 使用
- 状态机设计
- 数码管驱动

[查看详情](./10-stopwatch/README.md)

---

### 11. Camera Photo - 摄像头拍照

**难度**: ⭐⭐

**描述**: 使用 Picamera2 库，按 Enter 键拍照

**涉及内容**:
- Picamera2 摄像头控制
- 图像捕获与保存

[查看详情](./11-camera-preview/README.md)

---

### 12. Camera Record - 摄像头录像（预留）

**难度**: ⭐⭐⭐

**描述**: 摄像头录像实验

---

### 13. Camera Capture - 摄像头拍照进阶（预留）

**难度**: ⭐⭐⭐

**描述**: 摄像头拍照进阶实验

---

### 14. Infrared Sensor - 红外反射式传感器

**难度**: ⭐⭐

**描述**: 使用红外反射式传感器检测前方是否有障碍物

**涉及内容**:
- GPIO 输入检测
- 红外传感器原理

[查看详情](./14-infrared-sensor/README.md)

---

### 15. Infrared LED - 红外传感器 + LED 反馈

**难度**: ⭐⭐

**描述**: 检测到障碍物时 LED 亮起，实现视觉反馈

**涉及内容**:
- GPIO 输入输出结合
- 传感器与执行器联动

[查看详情](./15-infrared-led/README.md)

---

### 16. Ultrasonic Sensor - HC-SR04 超声波测距

**难度**: ⭐⭐⭐

**描述**: 使用 HC-SR04 超声波传感器测量距离

**涉及内容**:
- 超声波测距原理
- GPIO 时序控制
- 分压电路

[查看详情](./16-ultrasonic-sensor/README.md)

---

### 17. Ultrasonic TFT - 超声波测距可视化

**难度**: ⭐⭐⭐⭐

**描述**: 将超声波测得的距离实时显示在 TFT 屏幕上，用柱状图直观表示

**涉及内容**:
- 传感器与屏幕联动
- PIL 图像绘制
- 实时数据可视化

[查看详情](./17-ultrasonic-tft/README.md)

---

## 如何添加新实验

1. 在 `demos/` 目录下创建新文件夹，命名格式：`XX-experiment-name`
2. 创建 `README.md` 文档
3. 添加实验代码（Python 或 Node.js）
4. 更新本目录
