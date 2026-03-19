#!/bin/bash

echo ""
echo "🚀 OpenClaw Hub 启动中..."
echo ""

# 检查 Python
if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo "❌ 未找到 Python，请安装 Python 3.8+"
    exit 1
fi

echo "✅ Python 已安装"

# 检查依赖
echo "📦 检查依赖..."
if [ ! -d "backend/venv" ]; then
    echo "📝 创建虚拟环境..."
    $PYTHON -m venv backend/venv
fi

source backend/venv/bin/activate

if ! pip show flask &> /dev/null; then
    echo "📥 安装依赖..."
    pip install -r backend/requirements.txt
fi

echo "✅ 依赖已安装"

# 启动服务
echo ""
echo "🌐 启动服务..."
cd backend

# 设置环境变量
export FLASK_APP=app.py
export FLASK_ENV=production

python app.py
