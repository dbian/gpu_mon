#!/usr/bin/env python3
import subprocess
import time
import json
from datetime import datetime
from mail import send
import os
from dotenv import load_dotenv

load_dotenv()

ALERT_TEMP = 78  # 温度告警阈值
CHECK_INTERVAL = 60  # 检查间隔(秒)


def get_gpu_info():
    """使用nvidia-smi获取GPU信息"""
    try:
        result = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu=memory.used,memory.total,temperature.gpu",
                "--format=csv,noheader,nounits",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip().split(", ")
    except subprocess.CalledProcessError as e:
        print(f"获取GPU信息失败: {e}")
        return None


def monitor_gpu():
    """监控GPU状态"""
    while True:
        info = get_gpu_info()
        if info:
            mem_used, mem_total, temp = map(float, info)
            mem_percent = (mem_used / mem_total) * 100
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print(
                f"[{current_time}] 显存使用: {mem_percent:.1f}% ({mem_used:.0f}MB/{mem_total:.0f}MB), 温度: {temp}°C"
            )

            if temp >= ALERT_TEMP:
                alert_msg = f"""
                <h1 style="color: red;">GPU温度告警</h1>
                <p>GPU温度已达到 {temp}°C，超过阈值 {ALERT_TEMP}°C</p>
                <p>当前时间: {current_time}</p>
                """
                send("GPU温度告警", alert_msg, [])

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    print("启动GPU监控服务...")
    monitor_gpu()
