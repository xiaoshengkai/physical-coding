# Physical Coding

从点亮第一盏 LED 到让树莓派学会呼吸、跑马、指挥交通——这里记录了一个像素级工程师的硬核（物理）转型之路。

## 项目简介

作为一个前端工程师，我踏上了嵌入式开发的学习之旅。本项目记录了每一个小实验，从最基础的 LED 点亮开始，逐步进阶到更复杂的项目。

> Diode Of the Material (D.O.M.) —— 材料二极管，让硬件" Dom "化（可控化）

## 技术栈

- **树莓派**: Raspberry Pi 4B
- **编程语言**: Node.js / Python
- **硬件**: GPIO 编程、传感器、电路

## 快速开始

### 0. 安装 sshpass（密码登录必需）

```bash
# macOS
brew install hudochenkov/sshpass/sshpass

# Ubuntu/Debian
sudo apt install sshpass

# CentOS/RHEL
sudo yum install sshpass
```

### 1. 初始化配置

```bash
npm run setup
```

### 2. 连接树莓派并同步代码

```bash
npm run connect
```

### 3. 监听代码变更（自动同步）

```bash
npm run watch
```

## Demo 示例

每个实验都记录在 `demos/` 目录下：

| 序号 | 实验名称 | 描述 | 难度 |
|------|----------|------|------|
| 01 | LED Blink | 点亮第一盏 LED | ⭐ |
| 02 | LED Breathing | LED 呼吸灯效果 | ⭐⭐ |
| 03 | LED Marquee | 跑马灯效果 | ⭐⭐ |
| 04 | Traffic Light | 交通灯控制 | ⭐⭐⭐ |

详细文档见 [Demos](./demos/README.md)

## 项目结构

```
PhysicalCoding/
├── config/              # 配置文件
│   └── config.json      # 用户配置
├── demos/               # 实验示例
│   ├── 01-led-blink/
│   ├── 02-led-breathing/
│   └── ...
├── scripts/             # 工具脚本
│   ├── connect.js      # 连接树莓派
│   ├── sync.js         # 代码同步
│   └── watch.js        # 监听变更
├── package.json
└── README.md
```

## 配置说明

首次使用请运行 `npm run setup` 配置以下信息：

- 树莓派 IP 地址
- SSH 用户名
- 代码同步目标目录
- SSH 密钥路径（可选）

## License

MIT
