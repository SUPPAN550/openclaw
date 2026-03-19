@echo off
rem OpenClaw Gateway (v2026.3.13) - Enhanced startup script
set "DEEPSEEK_API_KEY=sk-23c1af8a63e1471cb6b8eef900cbf76b"
set "TMPDIR=C:\Users\Administrator\AppData\Local\Temp"
set "OPENCLAW_GATEWAY_PORT=18789"
set "OPENCLAW_SYSTEMD_UNIT=openclaw-gateway.service"
set "OPENCLAW_WINDOWS_TASK_NAME=OpenClaw Gateway"
set "OPENCLAW_SERVICE_MARKER=openclaw"
set "OPENCLAW_SERVICE_KIND=gateway"
set "OPENCLAW_SERVICE_VERSION=2026.3.13"

rem Set PATH to include node
set "PATH=C:\Program Files\nodejs;%PATH%"

rem Set working directory
cd /d C:\Users\Administrator\.openclaw

echo ============================================ >> C:\Users\Administrator\.openclaw\gateway.log
echo %date% %time% Starting Gateway... >> C:\Users\Administrator\.openclaw\gateway.log
echo User: %USERNAME% >> C:\Users\Administrator\.openclaw\gateway.log
echo Working Dir: %CD% >> C:\Users\Administrator\.openclaw\gateway.log
echo PATH: %PATH% >> C:\Users\Administrator\.openclaw\gateway.log

rem Check if gateway is already running
netstat -ano | findstr ":18789" >nul 2>&1
if %errorlevel% equ 0 (
    echo %date% %time% Gateway already running on port 18789, skipping. >> C:\Users\Administrator\.openclaw\gateway.log
    exit /b 0
)

echo %date% %time% Port 18789 is free, starting gateway... >> C:\Users\Administrator\.openclaw\gateway.log

rem Start gateway with full path
"C:\Program Files\nodejs\node.exe" C:\Users\Administrator\AppData\Roaming\npm\node_modules\openclaw\dist\index.js gateway --port 18789 >> C:\Users\Administrator\.openclaw\gateway.log 2>&1

echo %date% %time% Gateway exited with code: %errorlevel% >> C:\Users\Administrator\.openclaw\gateway.log
exit /b %errorlevel%
