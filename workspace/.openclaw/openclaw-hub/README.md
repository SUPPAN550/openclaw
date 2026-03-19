# OpenClaw Hub - 完整版

## 项目结构

```
openclaw-hub/
├── backend/                 # Python Flask 后端
│   ├── app.py              # 主应用
│   ├── requirements.txt    # 依赖
│   ├── config.py           # 配置
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── gateway.py      # 网关 API 代理
│   │   ├── system.py       # 系统资源监控
│   │   ├── agents.py       # Agent 管理
│   │   └── tasks.py        # 任务管理
│   └── utils/
│       ├── __init__.py
│       └── helpers.py      # 工具函数
├── frontend/               # 前端静态文件
│   ├── index.html          # 主页面
│   ├── css/
│   │   └── style.css       # 样式
│   └── js/
│       └── app.js          # 前端逻辑
└── start.bat              # Windows 启动脚本
└── start.sh               # Linux/Mac 启动脚本
```

## 快速启动

### 1. 安装依赖
```bash
cd backend
pip install -r requirements.txt
```

### 2. 启动服务
```bash
# Windows
start.bat

# Linux/Mac
bash start.sh
```

### 3. 访问控制面板
打开浏览器访问: http://localhost:5000

## 功能特性

- ✅ 连接 OpenClaw 网关 (127.0.0.1:18789)
- ✅ 实时系统资源监控 (CPU/内存/存储)
- ✅ Agent 管理与控制
- ✅ 任务调度与执行
- ✅ 日志实时查看
- ✅ 快捷操作按钮

## API 端点

| 端点 | 方法 | 功能 |
|------|------|------|
| /api/status | GET | 获取网关状态 |
| /api/metrics | GET | 获取系统资源 |
| /api/agents | GET | 获取 Agent 列表 |
| /api/agents/<id>/start | POST | 启动 Agent |
| /api/agents/<id>/stop | POST | 停止 Agent |
| /api/gateway/restart | POST | 重启网关 |
| /api/gateway/version | GET | 检查版本 |
| /api/gateway/fix | POST | 故障修复 |
| /api/gateway/sandbox | POST | 切换沙箱模式 |
| /api/gateway/stop | POST | 停止服务 |

## 配置

编辑 `backend/config.py` 修改网关地址和端口。
