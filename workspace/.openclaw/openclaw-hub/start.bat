@echo off
echo.
echo ===================================
echo    OpenClaw Hub
echo ===================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.8+
    echo.
    pause
    exit /b 1
)

echo [OK] Python found

REM Check dependencies  
echo Checking dependencies...
if not exist "backend\venv" (
    echo Creating virtual environment...
    python -m venv backend\venv
)

call backend\venv\Scripts\activate.bat >nul 2>&1

pip show flask >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r backend\requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
)

echo [OK] Dependencies ready

REM Start service
echo.
echo Starting server on http://localhost:5000
echo.
echo Press Ctrl+C to stop
echo.

cd backend
python app.py

echo.
echo Server stopped.
pause