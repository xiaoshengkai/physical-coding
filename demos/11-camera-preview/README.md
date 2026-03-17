# 11 - 摄像头预览

## 实验目标

使用树莓派官方摄像头模块 V2.1，通过 OpenCV 实时预览摄像头画面。

## 硬件准备

- 树莓派 4B
- Raspberry Pi Camera Module V2.1
- 摄像头排线

## 硬件连接

找到树莓派上的 CSI 接口（HDMI 接口和音频口之间），小心抬起卡扣，将摄像头排线插入（金属触点朝下），压下卡扣固定。

## 软件准备

1. 启用摄像头（在树莓派终端执行）：

```bash
sudo raspi-config
```

进入 Interface Options → Camera → Enable → 重启

2. 检查摄像头：

```bash
rpicam-hello --list-cameras
```

3. 安装 OpenCV：

```bash
pip install opencv-python
```

## 运行代码

```bash
python demos/11-camera-preview/main.py
```

或使用快速命令：

```bash
npm run run 11
```

## 操作说明

- 运行后显示实时摄像头画面
- 按 `q` 键退出

## 效果

- 窗口显示摄像头实时画面
- 按 q 退出程序
