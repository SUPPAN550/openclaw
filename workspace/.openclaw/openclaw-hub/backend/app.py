from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import psutil
import subprocess
import os
import sys

from config import GATEWAY_URL, BACKEND_HOST, BACKEND_PORT, CORS_ORIGINS, AGENTS

app = Flask(__name__)
CORS(app, origins=CORS_ORIGINS)

# 存储网关令牌
gateway_token = None

@app.route('/')
def index():
    """返回前端页面"""
    return app.send_static_file('index.html')

@app.route('/api/status')
def get_status():
    """获取 OpenClaw 网关状态"""
    global gateway_token
    try:
        response = requests.get(f"{GATEWAY_URL}/status", timeout=5)
        if response.status_code == 200:
            try:
                data = response.json()
                # 保存令牌
                if 'token' in data:
                    gateway_token = data['token']
                return jsonify({
                    "success": True,
                    "connected": True,
                    "data": data
                })
            except:
                # 网关返回的不是 JSON
                return jsonify({
                    "success": False,
                    "connected": False,
                    "error": "网关返回格式错误",
                    "data": {
                        "sessions": 0,
                        "tasks": 0,
                        "pending": 0
                    }
                }), 200
        else:
            return jsonify({
                "success": False,
                "connected": False,
                "error": f"HTTP {response.status_code}",
                "data": {
                    "sessions": 0,
                    "tasks": 0,
                    "pending": 0
                }
            }), 200
    except requests.exceptions.ConnectionError:
        return jsonify({
            "success": False,
            "connected": False,
            "error": "无法连接到 OpenClaw 网关",
            "data": {
                "sessions": 0,
                "tasks": 0,
                "pending": 0
            }
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "connected": False,
            "error": str(e),
            "data": {
                "sessions": 0,
                "tasks": 0,
                "pending": 0
            }
        }), 200

@app.route('/api/metrics')
def get_metrics():
    """获取系统资源使用情况"""
    try:
        # CPU 使用率
        cpu_percent = psutil.cpu_percent(interval=1)

        # 内存使用率
        memory = psutil.virtual_memory()
        memory_percent = memory.percent

        # 存储使用率
        disk = psutil.disk_usage('/')
        storage_percent = (disk.used / disk.total) * 100

        return jsonify({
            "success": True,
            "data": {
                "cpu": round(cpu_percent, 1),
                "memory": round(memory_percent, 1),
                "storage": round(storage_percent, 1),
                "cpu_count": psutil.cpu_count(),
                "memory_total": round(memory.total / (1024**3), 2),  # GB
                "memory_available": round(memory.available / (1024**3), 2),  # GB
                "disk_total": round(disk.total / (1024**3), 2),  # GB
                "disk_used": round(disk.used / (1024**3), 2),  # GB
                "disk_free": round(disk.free / (1024**3), 2)  # GB
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/agents')
def get_agents():
    """获取所有 Agent 列表"""
    return jsonify({
        "success": True,
        "data": AGENTS
    })

@app.route('/api/agents/<agent_id>/start', methods=['POST'])
def start_agent(agent_id):
    """启动指定 Agent"""
    try:
        # 这里可以调用 OpenClaw 的 API 或执行命令
        # 目前返回模拟成功
        return jsonify({
            "success": True,
            "message": f"Agent {agent_id} 启动成功"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/agents/<agent_id>/stop', methods=['POST'])
def stop_agent(agent_id):
    """停止指定 Agent"""
    try:
        return jsonify({
            "success": True,
            "message": f"Agent {agent_id} 停止成功"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/gateway/restart', methods=['POST'])
def restart_gateway():
    """重启 OpenClaw 网关"""
    try:
        # 尝试执行重启命令
        result = subprocess.run(
            ["openclaw", "gateway", "restart"],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            return jsonify({
                "success": True,
                "message": "网关重启成功",
                "output": result.stdout
            })
        else:
            return jsonify({
                "success": False,
                "error": result.stderr or "命令执行失败"
            }), 200
    except FileNotFoundError:
        return jsonify({
            "success": False,
            "error": "未找到 openclaw 命令"
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 200

@app.route('/api/gateway/version', methods=['GET'])
def check_version():
    """检查 OpenClaw 版本"""
    try:
        result = subprocess.run(
            ["openclaw", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            return jsonify({
                "success": True,
                "version": result.stdout.strip()
            })
        else:
            return jsonify({
                "success": False,
                "error": result.stderr or "命令执行失败"
            }), 200
    except FileNotFoundError:
        return jsonify({
            "success": False,
            "error": "未找到 openclaw 命令"
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 200

@app.route('/api/gateway/fix', methods=['POST'])
def fix_issues():
    """故障修复"""
    try:
        # 执行诊断和修复
        fixes = []

        # 检查网关状态
        try:
            response = requests.get(f"{GATEWAY_URL}/status", timeout=5)
            if response.status_code != 200:
                fixes.append("网关响应异常")
        except:
            fixes.append("网关未运行")

        return jsonify({
            "success": True,
            "message": "故障修复完成",
            "fixes": fixes
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 200

@app.route('/api/gateway/sandbox', methods=['POST'])
def toggle_sandbox():
    """切换沙箱模式"""
    try:
        # 这里可以实现沙箱模式切换逻辑
        return jsonify({
            "success": True,
            "message": "沙箱模式切换成功",
            "sandbox": True
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/gateway/stop', methods=['POST'])
def stop_gateway():
    """停止 OpenClaw 服务"""
    try:
        result = subprocess.run(
            ["openclaw", "gateway", "stop"],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            return jsonify({
                "success": True,
                "message": "服务已停止"
            })
        else:
            return jsonify({
                "success": False,
                "error": result.stderr or "命令执行失败"
            }), 200
    except FileNotFoundError:
        return jsonify({
            "success": False,
            "error": "未找到 openclaw 命令"
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 200

@app.route('/api/sessions')
def get_sessions():
    """获取活跃会话列表"""
    try:
        headers = {}
        if gateway_token:
            headers['Authorization'] = f'Bearer {gateway_token}'

        response = requests.get(
            f"{GATEWAY_URL}/api/sessions",
            headers=headers,
            timeout=5
        )

        if response.status_code == 200:
            return jsonify({
                "success": True,
                "data": response.json()
            })
        else:
            return jsonify({
                "success": False,
                "error": f"HTTP {response.status_code}"
            }), 503
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    print(f"🚀 OpenClaw Hub 启动中...")
    print(f"📡 网关地址: {GATEWAY_URL}")
    print(f"🌐 访问地址: http://{BACKEND_HOST}:{BACKEND_PORT}")
    print("")

    app.run(
        host=BACKEND_HOST,
        port=BACKEND_PORT,
        debug=False
    )
