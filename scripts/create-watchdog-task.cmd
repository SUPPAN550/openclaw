@echo off
schtasks /create /tn "OpenClaw Gateway Watchdog" /tr "C:\Users\Administrator\.openclaw\scripts\start-watchdog.bat" /sc onlogon /rl limited /f
