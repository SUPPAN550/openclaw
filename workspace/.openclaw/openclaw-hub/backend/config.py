import os
from dotenv import load_dotenv

load_dotenv()

# OpenClaw 网关配置
GATEWAY_HOST = os.getenv('OPENCLAW_GATEWAY_HOST', '127.0.0.1')
GATEWAY_PORT = int(os.getenv('OPENCLAW_GATEWAY_PORT', '18789'))
GATEWAY_URL = f"http://{GATEWAY_HOST}:{GATEWAY_PORT}"

# 后端服务配置
BACKEND_HOST = os.getenv('BACKEND_HOST', '0.0.0.0')
BACKEND_PORT = int(os.getenv('BACKEND_PORT', '5000'))

# CORS 配置
CORS_ORIGINS = [
    "http://localhost:5000",
    "http://127.0.0.1:5000",
    "file://",
    "null"
]

# Agent 配置
AGENTS = [
    {
        "id": "may",
        "name": "May",
        "animal": "🦁",
        "role": "核心主控",
        "type": "primary",
        "model": "deepseek/deepseek-chat",
        "schedule": "always",
        "status": "online",
        "lastOutput": "HEARTBEAT_OK"
    },
    {
        "id": "gock",
        "name": "Gock",
        "animal": "🐓",
        "role": "每日新闻",
        "type": "scheduled",
        "model": "moonshot/kimi-k2.5",
        "schedule": "每日 09:00",
        "status": "online",
        "lastOutput": "AI Trend Report"
    },
    {
        "id": "otter",
        "name": "Otter",
        "animal": "🦦",
        "role": "私人助理",
        "type": "persistent",
        "model": "moonshot/kimi-k2.5",
        "schedule": "每日 07:30",
        "status": "online",
        "lastOutput": "晨报推送"
    },
    {
        "id": "pandas",
        "name": "Pandas",
        "animal": "🐼",
        "role": "开发测试",
        "type": "persistent",
        "model": "deepseek/deepseek-chat",
        "schedule": "24/7 不间断",
        "status": "working",
        "lastOutput": "代码审查"
    },
    {
        "id": "monkey",
        "name": "Monkey",
        "animal": "🐵",
        "role": "内容创作",
        "type": "triggered",
        "model": "moonshot/kimi-k2.5",
        "schedule": "任务触发",
        "status": "idle",
        "lastOutput": "视频转文章"
    },
    {
        "id": "tiger",
        "name": "Tiger",
        "animal": "🐯",
        "role": "安全更新",
        "type": "scheduled",
        "model": "moonshot/kimi-k2.5",
        "schedule": "每周日 02:00",
        "status": "online",
        "lastOutput": "安全扫描报告"
    }
]
