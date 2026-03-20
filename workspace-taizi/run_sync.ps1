$python = "C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe"
$script1 = "C:\Users\Administrator\.openclaw\workspace-taizi\scripts\refresh_live_data.py"
$script2 = "C:\Users\Administrator\.openclaw\workspace-taizi\scripts\sync_from_openclaw_runtime.py"

Write-Host "Starting dual refresh loop..."
while ($true) {
    & $python $script1 2>$null
    & $python $script2 2>$null
    Start-Sleep -Seconds 15
}
