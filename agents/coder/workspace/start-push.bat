@echo off
cd /d "%~dp0"
set JOIN_KEY=ocj_coder_01
set AGENT_NAME=技术虾
set OFFICE_URL=http://127.0.0.1:19000
set OFFICE_LOCAL_STATE_FILE=%USERPROFILE%\.openclaw\agents\coder\workspace\office-state.json
python office-agent-push.py
