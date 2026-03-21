@echo off
cd /d "%~dp0"
set OFFICE_URL=http://127.0.0.1:19000
set OFFICE_STATE_FILE=%USERPROFILE%\.openclaw\agents\coder\workspace\office-state.json
start "CoderPush" python office-agent-push.py
