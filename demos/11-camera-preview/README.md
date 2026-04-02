# 11 - 摄像头拍照

## 实验目标

使用树莓派官方摄像头模块 1.3版，拍照并保存。

## 硬件准备

- 树莓派 4B
- Raspberry Pi Camera Module 1.3
- 摄像头排线

## 硬件连接

找到树莓派上的 CSI 接口（HDMI 接口和音频口之间），小心抬起卡扣，将摄像头排线插入（金属触点朝下），压下卡扣固定。

## 软件准备

1. 启用摄像头（如果未开启，在树莓派终端执行）：

```bash
sudo raspi-config
```

进入 Interface Options → Camera → Enable → 重启

2. 检查摄像头：

```bash
rpicam-hello --list-cameras
# 如果没有权限，尝试：
sudo rpicam-hello --list-cameras
```

正常输出示例：`0 : imx219 [3280x2464 10-bit RGGB]` 或 `ov5647`

3. 安装 Picamera2：

```bash
pip install picamera2
```

## 运行代码

```bash
python demos/11-camera-preview/main.py
```

或使用快速命令：

```bash
npm run run 11
```

## 效果

- 照片保存为 test.jpg