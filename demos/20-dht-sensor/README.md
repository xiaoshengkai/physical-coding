# 实验 20 - DHT 温湿度传感器

DHT11 数字温湿度传感器是一款性价比高的常用传感器，可同时测量温度和湿度。

## 硬件准备

- DHT11 模块
- 树莓派

## 接线

| DHT 模块  | 树莓派 GPIO | 物理引脚 | 说明   |
|----------|-------------|----------|--------|
| VCC (+)   | 3.3V        | Pin 1  | 供电   |
| GND (-)   | GND         | Pin 6  | 地     |
| DATA (S)  | GPIO4       | Pin 7  | 数据信号 |

**注意**：如果模块没有内置上拉电阻，在 DATA 与 3.3V 之间加一个 4.7kΩ~10kΩ 上拉电阻。

## 软件准备

```bash
sudo apt update
sudo apt install python3-pip
sudo pip3 install adafruit-circuitpython-dht
```

## 运行

```bash
python3 main.py
```

## 输出示例

```
温度: 25.3°C, 湿度: 58.2%
温度: 25.4°C, 湿度: 58.1%
```

## 引脚约定

- DATA → GPIO4