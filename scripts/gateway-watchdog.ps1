$GatewayPort = 18789
$CheckInterval = 30
$LogDir = "C:\Users\Administrator\.openclaw\logs"
$LogFile = "$LogDir\gateway-startup.log"

if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
}

function Write-Log {
    param([string]$Type, [string]$Message)
    $Timestamp = Get-Date -Format "yyyy/MM/dd HH:mm:ss"
    Add-Content -Path $LogFile -Value "$Timestamp [$Type] $Message" -ErrorAction SilentlyContinue
    Write-Host "$Timestamp [$Type] $Message"
}

function Test-Gateway {
    try {
        $client = New-Object System.Net.Sockets.TcpClient
        $client.Connect("127.0.0.1", $GatewayPort)
        $client.Close()
        return $true
    } catch {
        return $false
    }
}

$StartupType = if ($env:OPENCLAW_WATCHDOG -eq "1") { "Watchdog" } else { "Manual" }
Write-Log "INFO" "=== Watchdog Started ($StartupType) ==="

if (Test-Gateway) {
    Write-Log "INFO" "Gateway running (startup: $StartupType)"
}

$count = 0
while ($true) {
    if (-not (Test-Gateway)) {
        $count++
        Write-Log "WARN" "Gateway down, restart attempt #$count"
        Stop-Process -Name "node" -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 3
        for ($i = 0; $i -lt 10; $i++) {
            try {
                $c = New-Object System.Net.Sockets.TcpClient
                $c.Connect("127.0.0.1", $GatewayPort)
                $c.Close()
                Start-Sleep -Seconds 2
            } catch { break }
        }
        Write-Log "INFO" "Starting Gateway (Watchdog)"
        Start-Process -FilePath "openclaw" -ArgumentList "gateway","start" -WindowStyle Hidden -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 5
        if (Test-Gateway) {
            Write-Log "INFO" "Gateway started OK"
            $count = 0
        } else {
            Write-Log "ERROR" "Gateway start failed"
        }
    }
    Start-Sleep -Seconds $CheckInterval
}
