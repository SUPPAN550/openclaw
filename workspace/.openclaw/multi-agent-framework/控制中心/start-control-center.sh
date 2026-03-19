#!/bin/bash

echo "🚀 启动 OpenClaw 多智能体控制中心..."
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

echo "✅ Python 版本: $($PYTHON --version)"

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
HTML_PATH="$SCRIPT_DIR/openclaw-hub.html"

echo "🌐 正在打开控制中心..."

# 根据系统打开浏览器
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open "$HTML_PATH"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open "$HTML_PATH"
else
    # Windows Git Bash
    start "$HTML_PATH"
fi

echo ""
echo "✨ OpenClaw 多智能体控制中心已启动!"
echo "📍 文件位置: $HTML_PATH"
echo ""
echo "团队智能体:"
echo "  🦁 May    - 核心主控"
echo "  🐓 Gock   - 每日新闻"
echo "  🦦 Otter  - 私人助理"
echo "  🐼 Pandas - 开发测试"
echo "  🐵 Monkey - 内容创作"
echo "  🐯 Tiger  - 安全更新"
echo ""
read -p "按任意键退出..."
