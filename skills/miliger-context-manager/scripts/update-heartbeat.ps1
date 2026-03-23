$state = @{
    lastChecks = @{
        context = [int](Get-Date -UFormat %s)
        email = $null
        calendar = $null
        weather = $null
    }
}
$dir = "$env:USERPROFILE\.openclaw\workspace\skills\miliger-context-manager\state"
if (!(Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
$state | ConvertTo-Json -Depth 3 | Set-Content "$dir\heartbeat-state.json"
Write-Host "Updated heartbeat-state.json"
