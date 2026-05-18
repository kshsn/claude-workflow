# Claude Code Global Configuration Installer — Windows
# Run from the repo root: .\install.ps1

$ErrorActionPreference = "Stop"
$RepoDir = $PSScriptRoot
$ClaudeDir = "$env:USERPROFILE\.claude"

Write-Host "Installing Claude Code configuration to $ClaudeDir ..." -ForegroundColor Cyan

# Create all directories
$dirs = @("hooks", "commands", "agents", "rules", "docs", "templates", "logs")
foreach ($d in $dirs) {
    New-Item -ItemType Directory -Force -Path "$ClaudeDir\$d" | Out-Null
}

# Copy all files except installer/meta files
$excludeTopLevel = @("install.ps1", "install.sh", "README.md", ".git", "settings.template.json")
Get-ChildItem -Path $RepoDir -Recurse -File | Where-Object {
    $rel = $_.FullName.Substring($RepoDir.Length).TrimStart('\')
    $top = $rel.Split('\')[0]
    $excludeTopLevel -notcontains $top
} | ForEach-Object {
    $rel = $_.FullName.Substring($RepoDir.Length).TrimStart('\')
    $dest = Join-Path $ClaudeDir $rel
    $destDir = Split-Path $dest -Parent
    New-Item -ItemType Directory -Force -Path $destDir | Out-Null
    Copy-Item $_.FullName -Destination $dest -Force
    Write-Host "  Copied: $rel" -ForegroundColor Gray
}

# Generate settings.json with correct absolute paths
$template = Get-Content "$RepoDir\settings.template.json" -Raw
$claudeDirForward = $ClaudeDir.Replace('\', '/')
$generated = $template -replace '\$\{CLAUDE_HOME\}', $claudeDirForward
$generated | Set-Content "$ClaudeDir\settings.json" -Encoding UTF8
Write-Host "  Generated: settings.json" -ForegroundColor Gray

Write-Host ""
Write-Host "Done! Claude Code global configuration installed." -ForegroundColor Green
Write-Host "Restart Claude Code to activate hooks and commands." -ForegroundColor Yellow
Write-Host ""

# VPS lessons config setup
$vpsConfig = "$ClaudeDir\lessons-api.json"
if (Test-Path $vpsConfig) {
    Write-Host "VPS config already exists at $vpsConfig — skipping setup." -ForegroundColor Gray
} else {
    Write-Host "VPS Lessons API not configured on this device." -ForegroundColor Yellow
    $setupVps = Read-Host "Set up VPS lesson sync now? [y/N]"
    if ($setupVps -eq 'y' -or $setupVps -eq 'Y') {
        python "$ClaudeDir\scripts\setup-vps-config.py"
    } else {
        Write-Host "Skipped. Run later: python `"$ClaudeDir\scripts\setup-vps-config.py`"" -ForegroundColor Gray
    }
}
