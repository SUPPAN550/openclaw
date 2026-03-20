# refresh loop for Windows - runs every 15 seconds
$python = "C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe"
$script = "C:\Users\Administrator\.openclaw\workspace-taizi\scripts\refresh_live_data.py"

Write-Host "Starting refresh loop (Ctrl+C to stop)"
while ($true) {
    try {
        & $python $script 2>&1 | Out-Null
    } catch {
        Write-Host "[ERROR] $($_.Exception.Message)"
    }
    Start-Sleep -Seconds 15
}
