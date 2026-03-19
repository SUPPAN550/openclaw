# OpenClaw 多智能体控制中心启动脚本

Write-Host "🚀 启动 OpenClaw 多智能体控制中心..." -ForegroundColor Green
Write-Host ""

# 检查 Python
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command python3 -ErrorAction SilentlyContinue
}

if (-not $python) {
    Write-Host "❌ 未找到 Python，请安装 Python 3.8+" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Python 版本: $(& $python.Source --version)" -ForegroundColor Green

# 启动控制中心
$htmlPath = Join-Path $PSScriptRoot "openclaw-hub.html"
Write-Host "🌐 正在打开控制中心..." -ForegroundColor Cyan

# 使用默认浏览器打开
Start-Process $htmlPath

Write-Host ""
Write-Host "✨ OpenClaw 多智能体控制中心已启动!" -ForegroundColor Green
Write-Host "📍 文件位置: $htmlPath" -ForegroundColor Gray
Write-Host ""
Write-Host "团队智能体:" -ForegroundColor Yellow
Write-Host "  🦁 May    - 核心主控" -ForegroundColor White
Write-Host "  🐓 Gock   - 每日新闻" -ForegroundColor White
Write-Host "  🦦 Otter  - 私人助理" -ForegroundColor White
Write-Host "  🐼 Pandas - 开发测试" -ForegroundColor White
Write-Host "  🐵 Monkey - 内容创作" -ForegroundColor White
Write-Host "  🐯 Tiger  - 安全更新" -ForegroundColor White
Write-Host ""
Write-Host "按任意键退出..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
