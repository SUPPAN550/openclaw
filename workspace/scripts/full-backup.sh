#!/bin/bash
# Full backup script for OpenClaw to GitHub

set -e

BACKUP_DATE=$(date +%Y-%m-%d-%H%M)
BACKUP_DIR="/tmp/openclaw-backup-${BACKUP_DATE}"
REPO_URL="https://github.com/SUPPAN550/openclaw"
TOKEN="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"

echo "=== OpenClaw Full Backup ==="
echo "Date: ${BACKUP_DATE}"

# Create backup directory
mkdir -p "${BACKUP_DIR}"

# Copy OpenClaw config and workspace
echo "Copying files..."
robocopy "C:\Users\Administrator\.openclaw" "${BACKUP_DIR}" /E /XD node_modules .git /R:3 /W:5 || true

# Initialize git repo
cd "${BACKUP_DIR}"
git init
git config user.email "backup@openclaw.local"
git config user.name "OpenClaw Backup"

# Add all files
git add -A
git commit -m "Full backup ${BACKUP_DATE}"

# Push to GitHub
echo "Pushing to GitHub..."
git remote add origin "https://${TOKEN}@github.com/SUPPAN550/openclaw.git" 2>/dev/null || true
git fetch origin || true

# Create or switch to backup branch
BRANCH_NAME="backups/${BACKUP_DATE}"
git checkout -b "${BRANCH_NAME}" || git checkout "${BRANCH_NAME}"

# Push
git push -u origin "${BRANCH_NAME}" --force

echo "=== Backup Complete ==="
echo "Branch: ${BRANCH_NAME}"
echo "URL: https://github.com/SUPPAN550/openclaw/tree/${BRANCH_NAME}"
