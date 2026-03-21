# Context Monitor for Windows
# Monitors OpenClaw session context usage and alerts when threshold is reached

param(
    [int]$Threshold = 60,
    [string]$LogDir = "$env:USERPROFILE\.openclaw\workspace\logs",
    [string]$LogFile = "$LogDir\context-monitor.log"
)

# Ensure log directory exists
if (!(Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
}

function Write-Log($Message) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp - $Message" | Out-File -Append -FilePath $LogFile
    Write-Host "$timestamp - $Message"
}

# Get session list to check context usage
try {
    # Use .NET Process to properly separate stdout and stderr
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = "C:\Users\Administrator\AppData\Roaming\npm\openclaw.cmd"
    $psi.Arguments = "sessions --json"
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    
    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $psi
    $process.Start() | Out-Null
    
    $stdout = $process.StandardOutput.ReadToEnd()
    $stderr = $process.StandardError.ReadToEnd()
    $process.WaitForExit()
    
    if ($stdout) {
        # Extract JSON from stdout (find content between first { and last })
        $jsonStart = $stdout.IndexOf('{')
        $jsonEnd = $stdout.LastIndexOf('}')
        
        if ($jsonStart -ge 0 -and $jsonEnd -gt $jsonStart) {
            $jsonContent = $stdout.Substring($jsonStart, $jsonEnd - $jsonStart + 1)
            $data = $jsonContent | ConvertFrom-Json -ErrorAction SilentlyContinue
            
            if ($data -and $data.sessions) {
                # Find main session
                $mainSession = $data.sessions | Where-Object { $_.key -eq 'agent:main:main' } | Select-Object -First 1
                
                if ($mainSession -and $mainSession.totalTokens -and $mainSession.contextTokens) {
                    $used = $mainSession.totalTokens
                    $total = $mainSession.contextTokens
                    $usage = [math]::Round(($used / $total) * 100)
                    
                    Write-Log "Context usage: ${usage}% (${used}/${total} tokens)"
                    
                    if ($usage -ge $Threshold) {
                        Write-Log "WARNING: Context usage ${usage}% exceeds threshold ${Threshold}%"
                        
                        # Check memory files
                        $memoryDir = "$env:USERPROFILE\.openclaw\workspace\memory"
                        $memoryLite = "$memoryDir\MEMORY-LITE.md"
                        
                        if (Test-Path $memoryLite) {
                            $content = Get-Content $memoryLite -Raw -ErrorAction SilentlyContinue
                            $wordCount = ($content -split '\s+').Count
                            Write-Log "MEMORY-LITE.md: $wordCount words"
                        }
                        
                        Write-Log "ALERT: Consider starting a new session to reset context"
                    } else {
                        Write-Log "Context usage normal: ${usage}%"
                    }
                } else {
                    Write-Log "Main session found but no token info available"
                }
            } else {
                Write-Log "No sessions data found in JSON"
            }
        } else {
            Write-Log "Could not find JSON content in output"
        }
    } else {
        Write-Log "No output from sessions command"
    }
} catch {
    Write-Log "Error checking context: $_"
}
