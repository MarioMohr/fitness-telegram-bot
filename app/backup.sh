#!/bin/bash

# Configuration Paths
REPO_DIR="/home/mario/fitness"
APP_DIR="/home/mario/fitness/app"
SAMBA_DIR="/mnt/media/backups/docker"
USB_DIR="/mnt/MiniUSB/docker"
BACKUP_NAME="fitness_telegram_bot_$(date +%Y%m%d_%H%M%S).tar.gz"
BACKUP_TMP="/tmp/$BACKUP_NAME"

# Prompt for a commit message so your GitHub history is clean
echo "Enter a brief description of the upgrade/changes you made:"
read -r commit_msg

if [ -z "$commit_msg" ]; then
    commit_msg="Manual system upgrade and backup snapshot"
fi

echo "Stopping fitness_trainer to secure the database..."
cd "$APP_DIR" && docker compose stop fitness_trainer

echo "Archiving whole fitness directory (excluding git internals)..."
# Changes to the parent fitness directory, excludes .git, and compresses everything else
tar -czf "$BACKUP_TMP" -C "$REPO_DIR" --exclude='.git' .

# --- Distribution to Storage ---
if [ -d "$SAMBA_DIR" ]; then
    cp "$BACKUP_TMP" "$SAMBA_DIR/"
    echo "✅ Backed up to Samba Share."
else
    echo "⚠️ Warning: Samba Share directory not found, skipping."
fi

if [ -d "$USB_DIR" ]; then
    cp "$BACKUP_TMP" "$USB_DIR/"
    echo "✅ Backed up to USB Drive."
else
    echo "⚠️ Warning: USB Drive directory not found, skipping."
fi

rm "$BACKUP_TMP"

# --- Codebase Version Control ---
echo "Pushing code updates to GitHub..."
cd "$REPO_DIR"
git add .
git commit -m "$commit_msg"
git push origin main
echo "✅ Public codebase pushed to GitHub."

# --- Restart Application ---
echo "Restarting fitness_trainer container with upgrades..."
cd "$APP_DIR"
docker compose up -d --build fitness_trainer

echo "🚀 Upgrade, redundant backups, and GitHub deployment complete!"

