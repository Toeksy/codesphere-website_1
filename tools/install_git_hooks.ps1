# Install Git hooks for this repo (local config only)
# Sets core.hooksPath to the versioned `.githooks/` folder.

[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [ValidateSet("install", "uninstall", "status")]
    [string]$Action = "install"
)

$ErrorActionPreference = "Stop"

function Write-Cyan { param([string]$Text) Write-Host $Text -ForegroundColor Cyan }
function Write-Green { param([string]$Text) Write-Host $Text -ForegroundColor Green }
function Write-Yellow { param([string]$Text) Write-Host $Text -ForegroundColor Yellow }
function Write-Red { param([string]$Text) Write-Host $Text -ForegroundColor Red }

$repoRoot = Split-Path -Parent $PSScriptRoot
$hooksDir = Join-Path $repoRoot ".githooks"

if (-not (Test-Path $hooksDir)) {
    Write-Red "❌ Missing $hooksDir"
    exit 1
}

try {
    $null = git --version 2>$null
} catch {
    Write-Red "❌ Git not found on PATH. Install Git first."
    exit 1
}

Push-Location $repoRoot
try {
    switch ($Action) {
        "status" {
            $current = git config --local core.hooksPath
            if ($LASTEXITCODE -ne 0 -or -not $current) {
                Write-Yellow "ℹ️ core.hooksPath not set (using default .git/hooks)"
                exit 0
            }
            Write-Green "✓ core.hooksPath = $current"
            exit 0
        }
        "install" {
            git config --local core.hooksPath .githooks
            if ($LASTEXITCODE -ne 0) { throw "git config failed" }

            $current = git config --local core.hooksPath
            Write-Green "✅ Installed hooks: core.hooksPath = $current"
            Write-Cyan "Hooks enabled: pre-commit will run 'python tools/trm_check.py'"
            exit 0
        }
        "uninstall" {
            # Unset returns non-zero if not set; treat as ok.
            git config --local --unset core.hooksPath 2>$null
            Write-Green "✅ Uninstalled: core.hooksPath unset (back to default .git/hooks)"
            exit 0
        }
    }
} finally {
    Pop-Location
}
