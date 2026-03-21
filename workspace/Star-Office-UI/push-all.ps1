$ErrorActionPreference = "SilentlyContinue"

$agents = @(
    @{
        "name" = "技术虾"
        "key"  = "ocj_coder_01"
        "dir"  = "C:\Users\Administrator\.openclaw\agents\coder\workspace"
    },
    @{
        "name" = "新闻虾"
        "key"  = "ocj_newsai_01"
        "dir"  = "C:\Users\Administrator\.openclaw\agents\newsai\workspace"
    },
    @{
        "name" = "项目虾"
        "key"  = "ocj_pm_01"
        "dir"  = "C:\Users\Administrator\.openclaw\agents\pm\workspace"
    },
    @{
        "name" = "金融虾"
        "key"  = "ocj_finance_01"
        "dir"  = "C:\Users\Administrator\.openclaw\agents\finance\workspace"
    }
)

$pushScript = "C:\Users\Administrator\.openclaw\workspace\Star-Office-UI\office-agent-push.py"
$python = "C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe"

foreach ($agent in $agents) {
    $env = @{
        "JOIN_KEY"        = $agent.key
        "AGENT_NAME"      = $agent.name
        "OPENCLAW_WORKSPACE_DIR" = $agent.dir
    }

    $proc = Start-Process -FilePath $python -ArgumentList $pushScript -WorkingDirectory (Split-Path $pushScript) -EnvironmentVariables $env -PassThru -WindowStyle Hidden
    Write-Host "Started $($agent.name) (PID: $($proc.Id))"
}

Write-Host "All 4 agents pushed."
