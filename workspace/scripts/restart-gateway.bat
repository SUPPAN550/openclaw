@echo off
echo [Restart OpenClaw Gateway]

:: 1. Stop existing process
echo Stopping existing process...
taskkill /F /IM node.exe /FI "WINDOWTITLE eq openclaw*" 2>nul
taskkill /F /IM node.exe /FI "COMMANDLINE eq *openclaw*gateway*" 2>nul

:: Wait for process to exit
timeout /t 2 /nobreak >nul

:: 2. Check port
echo Checking port 18789...
netstat -ano | findstr :18789 >nul
if %errorlevel% equ 0 (
    echo Warning: Port still in use, forcing release...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :18789') do taskkill /F /PID %%a 2>nul
)

:: 3. Start Gateway
echo Starting Gateway...
start /B cmd /c "openclaw gateway start"

:: 4. Wait for startup
timeout /t 3 /nobreak >nul

:: 5. Verify status
echo Verifying status...
openclaw gateway status | findstr "RPC probe: ok" >nul
if %errorlevel% equ 0 (
    echo [OK] Gateway restarted successfully
) else (
    echo [ERROR] Gateway failed to start, check logs
)
