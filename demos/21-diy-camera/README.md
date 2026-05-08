# 实验 21 - DIY 相机

这是一个综合项目，将多个模块集成在一起，构建一个功能完整的 DIY 相机。

## 硬件清单

| 组件 | 数量 | 备注 |
|------|------|------|
| 树莓派 4B | 1 | 主控 |
| 摄像头 v1.3 | 1 | CSI 接口 |
| 3.5寸 SPI 屏幕 ILI9488 | 1 | 480x320, [Wiki](http://www.lcdwiki.com/zh/3.5inch_SPI_Module_ILI9488_SKU:MSP3520) |
| 旋转编码器 KY-040 | 1 | 带按钮 |
| 按键 | 3 | 拍照、录像、菜单 |
| 蜂鸣器 | 1 | 无源（需 PWM） |

## 接线

### 屏幕 (ILI9488, 3.5寸 480x320)

| 屏幕引脚 | 功能 | 树莓派 GPIO | 物理引脚 |
|----------|------|-------------|----------|
| VCC | 电源 | 5V | Pin 2/4 |
| GND | 地 | GND | Pin 6 |
| SCLK | SPI 时钟 | GPIO11 | Pin 23 |
| MOSI | SPI 数据 | GPIO10 | Pin 19 |
| CS | 片选 | GPIO5 | Pin 29 |
| DC | 数据/命令 | GPIO24 | Pin 18 |
| RST | 复位 | GPIO25 | Pin 22 |
| BL | 背光 | 3.3V | Pin 1 |

### 按键拍照 (GPIO17)

```
GND ──┐
        │
       [按键]
        │
GPIO17 ─┘
```

- GPIO17 接按键一端，另一端接 GND
- 树莓派内置上拉，按下触发低电平

### 蜂鸣器 (GPIO18, 无源蜂鸣器)

| 蜂鸣器引脚 | 连接 |
|------------|------|
| I/O | GPIO18 |
| VCC | 3.3V |
| GND | GND |

- 无源蜂鸣器需要 PWM 驱动
- 频率 1000Hz，占空比 50% 发声


## 依赖安装

```bash
sudo apt update
sudo apt install python3-pip python3-pil python3-numpy libcamera-tools
pip3 install spidev gpiozero picamera2
```

## 启用 SPI

```bash
sudo raspi-config
```

选择 **Interface Options** → **SPI** → **Enable** → 重启

验证：
```bash
ls /dev/spi*
```

应看到 `/dev/spidev0.0` 和 `/dev/spidev0.1`

## 测试摄像头

```bash
rpicam-hello
```

有日志输出说明正确。

## 运行

```bash
cd demos/21-diy-camera
python3 main.py
```

## 渐进式开发步骤

### Phase 1: 点亮屏幕

**目标**: 确认屏幕驱动正常

**关键点**:
1. 向商家索要 Wiki 文档，确认芯片型号（ILI9341 vs ILI9488）
2. 根据芯片选择正确的色彩模式（RGB565 vs RGB666）
3. ILI9488 必须用 RGB666

```python
cmd(0x3A)
data(0x66)  # RGB666
```

**测试代码**: 红绿蓝白黑循环显示

### Phase 2: 摄像头预览

**目标**: 摄像头画面显示在屏幕上

**前置**: `rpicam-hello` 测试通过

**关键点**:
1. Picamera2 输出 RGB888，需转换为 RGB666
2. 分辨率影响帧率，需要权衡
3. 居中显示比拉伸更美观

**分辨率与帧率对照**:

| 分辨率 | 帧率体验 |
|--------|----------|
| 320×240 | 卡顿 |
| 280×210 | 可接受 |
| 192×144 | 流畅 |
| 160×120 | 很流畅 |

**保持 4:3 比例避免拉伸变形**

### Phase 3: 按键拍照 + 蜂鸣器

**目标**: 按键拍照并保存高清照片

**设计思路**:

1. **按键**: 轮询 + 内置上拉，简单不破坏预览循环
2. **蜂鸣器**: 无源蜂鸣器，PWM 驱动
3. **拍照**: 预览低分辨率，拍照高分辨率

**关键代码**:

```python
# 按键检测（内置上拉）
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# 无源蜂鸣器 PWM
buzzer = GPIO.PWM(BUZZER_PIN, 1000)
buzzer.start(0)

# 主循环中轮询
if GPIO.input(BUTTON_PIN) == 0:  # 按下
    buzzer.ChangeDutyCycle(50)   # 蜂鸣
    time.sleep(0.1)
    buzzer.ChangeDutyCycle(0)
    img = picam2.capture_image() # 高清拍照
    img.save(f"photo_{timestamp}.jpg")
```

**预览 vs 拍照**:

| 模式 | 分辨率 | 目的 |
|------|--------|------|
| 预览 | 320×240 | 流畅 |
| 拍照 | 传感器最高 | 清晰 |

## 性能调优经验

### 核心问题

SPI 带宽有限，高分辨率 + 高帧率 = 不可能三角

### 优化策略

#### 1. SPI 提速

```python
spi.max_speed_hz = 40000000  # 40MHz 极限
```

#### 2. 降低分辨率

最大收益，帧率直接提升

#### 3. 居中显示

不拉伸，保持画面比例

#### 4. 跳帧

```python
if frame_count % 2 != 0:
    continue
```

用时间换带宽

#### 5. 自适应跳帧

检测运动幅度，大运动时自动降帧：

```python
def is_motion_large(prev, curr, threshold=18):
    diff = np.abs(curr.astype(np.int16) - prev.astype(np.int16))
    return np.mean(diff) > threshold
```

### 本质

实时系统的 trade-off：**分辨率 vs 流畅度**

| 模式 | 分辨率 | 目的 |
|------|--------|------|
| 预览 | 低 | 流畅 |
| 拍照 | 高 | 清晰 |

## 调试经验

### 白屏

- 原因：驱动不匹配
- 解决：确认芯片型号（看 Wiki 或问商家）

### 黑屏/花屏

- 原因：色彩模式错误
- 解决：ILI9488 用 RGB666（0x66）

### 卡顿严重

- 原因：分辨率过高
- 解决：降到 192×144 或更低

## 项目阶段

- [x] Phase 1: 点亮屏幕
- [x] Phase 2: 摄像头预览
- [x] Phase 3: 按键拍照 + 蜂鸣器提示
- [ ] Phase 4: 数码变焦（旋钮控制）
- [ ] Phase 5: 录像
- [ ] Phase 6: 菜单界面
