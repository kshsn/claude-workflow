#!/usr/bin/env bash
# Claude Code Global Configuration Installer — Mac / Linux
# Run from the repo root: chmod +x install.sh && ./install.sh

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

echo "Installing Claude Code configuration to $CLAUDE_DIR ..."

# Create all directories
for d in hooks commands agents rules docs templates logs; do
    mkdir -p "$CLAUDE_DIR/$d"
done

# Copy all files except meta/installer files
rsync -av \
    --exclude='.git' \
    --exclude='README.md' \
    --exclude='install.ps1' \
    --exclude='install.sh' \
    --exclude='settings.template.json' \
    "$REPO_DIR/" "$CLAUDE_DIR/"

# Generate settings.json with correct absolute paths
sed "s|\${CLAUDE_HOME}|$CLAUDE_DIR|g" "$REPO_DIR/settings.template.json" > "$CLAUDE_DIR/settings.json"
echo "  Generated: settings.json"

echo ""
echo "Done! Claude Code global configuration installed."
echo "Restart Claude Code to activate hooks and commands."
