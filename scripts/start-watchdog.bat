@echo off
cd /d C:\Users\Administrator\.openclaw\scripts
set OPENCLAW_WATCHDOG=1
powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\Users\Administrator\.openclaw\scripts\gateway-watchdog.ps1"
