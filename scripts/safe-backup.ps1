# Full backup script for OpenClaw to GitHub (excluding secrets)
$ErrorActionPreference = "Stop"

$BACKUP_DATE = Get-Date -Format "yyyy-MM-dd-HHmm"
$BACKUP_DIR = "D:\openclaw-backup-${BACKUP_DATE}"
$REPO_URL = "https://github.com/SUPPAN550/openclaw"
$TOKEN = "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"

Write-Host "=== OpenClaw Full Backup (Safe) ===" -ForegroundColor Green
Write-Host "Date: ${BACKUP_DATE}"

# Create backup directory
New-Item -ItemType Directory -Path $BACKUP_DIR -Force | Out-Null

# Copy OpenClaw config and workspace (excluding sensitive files)
Write-Host "Copying files (excluding secrets)..." -ForegroundColor Yellow
robocopy "C:\Users\Administrator\.openclaw" $BACKUP_DIR /E /XD node_modules .git extensions agents\main\sessions /XF *.jsonl .env *.bak /R:3 /W:5 /MT:8 | Out-Null

# Create .gitignore to exclude sensitive files
@"
# Sensitive files
.env
*.jsonl
*.bak
agents/*/sessions/
credentials/
identity/

# Large files
node_modules/
*.log
"@ | Out-File -FilePath "$BACKUP_DIR\.gitignore" -Encoding UTF8

# Initialize git repo
Set-Location $BACKUP_DIR
git init | Out-Null
git config user.email "backup@openclaw.local" | Out-Null
git config user.name "OpenClaw Backup" | Out-Null

# Add all files
git add -A | Out-Null
git commit -m "Full backup ${BACKUP_DATE} (sensitive data excluded)" | Out-Null

# Push to GitHub
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
git remote add origin "https://${TOKEN}@github.com/SUPPAN550/openclaw.git" 2>$null
git fetch origin 2>$null

# Create or switch to backup branch
$BRANCH_NAME = "backups/${BACKUP_DATE}"
git checkout -b $BRANCH_NAME 2>$null
git push -u origin $BRANCH_NAME --force 2>&1 | Out-Null

Write-Host "=== Backup Complete ===" -ForegroundColor Green
Write-Host "Branch: ${BRANCH_NAME}"
Write-Host "URL: https://github.com/SUPPAN550/openclaw/tree/${BRANCH_NAME}"
Write-Host "Note: Sensitive files (tokens, sessions) excluded for security"
