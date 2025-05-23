# GPU Monitor

[![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

基于Python的GPU监控工具，实时监控显存使用情况和温度，支持邮件告警功能。

## 功能特性

- 实时监控GPU显存使用率
- 实时监控GPU温度
- 温度超过阈值自动发送邮件告警
- 支持HTML格式告警邮件
- 支持作为系统服务后台运行

## 系统要求

- NVIDIA显卡及驱动
- nvidia-smi工具
- Python 3.13+
- 邮件服务器配置(用于告警功能)

## 安装指南

1. 克隆仓库：
   ```bash
   git clone https://github.com/your-repo/gpu_mon.git
   cd gpu_mon
   ```

2. 创建虚拟环境：
   ```bash
   uv venv .venv
   source .venv/bin/activate  # Linux/macOS
   ```
   
3. 安装依赖：
   ```bash
   uv pip install -e .
   ```

## 配置说明

在项目根目录创建`.env`文件，配置邮件相关参数：

```ini
EMAIL_SENDER=your-email@example.com
EMAIL_RECV=receiver@example.com
EMAIL_PASSWORD=your-email-password
EMAIL_SMTP=smtp.example.com
EMAIL_PORT=587
```

### 代理配置（可选）

如果需要通过代理发送邮件，可以设置`https_proxy`环境变量：

```bash
export https_proxy=http://proxy.example.com:8080
```

或者直接在`.env`文件中添加：

```ini
https_proxy=http://proxy.example.com:8080
```

代理格式要求：
- 必须包含协议(http://)
- 必须包含主机名和端口号
- 示例格式: `http://proxy.example.com:8080`

## 使用方法

### 直接运行
```bash
python gpu_monitor.py
```

### 作为系统服务运行

1. 复制服务文件：
   ```bash
   sudo cp gpu-monitor.service /etc/systemd/system/
   ```

2. 重载服务配置：
   ```bash
   sudo systemctl daemon-reload
   ```

3. 启动服务：
   ```bash
   sudo systemctl start gpu-monitor
   ```

4. 设置开机启动：
   ```bash
   sudo systemctl enable gpu-monitor
   ```

## 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。
