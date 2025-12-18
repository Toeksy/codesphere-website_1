# TRM Session Manager (PowerShell Wrapper)
# Wrapper-skripti Python TRM-työkaluille.

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("start", "update", "finalize")]
    [string]$Action,
    
    [Parameter(Mandatory=$false)]
    [string]$Param1 = "",
    
    [Parameter(Mandatory=$false)]
    [string]$Param2 = ""
)

$ErrorActionPreference = "Stop"

# Värit
function Write-Cyan { param([string]$Text) Write-Host $Text -ForegroundColor Cyan }
function Write-Green { param([string]$Text) Write-Host $Text -ForegroundColor Green }
function Write-Yellow { param([string]$Text) Write-Host $Text -ForegroundColor Yellow }
function Write-Red { param([string]$Text) Write-Host $Text -ForegroundColor Red }

# Tarkista Python
try {
    $pythonVersion = python --version 2>&1
    Write-Cyan "✓ Python löytyi: $pythonVersion"
} catch {
    Write-Red "❌ Virhe: Python ei löydy. Asenna Python ja lisää se PATH-muuttujaan."
    exit 1
}

# Polut
$scriptDir = $PSScriptRoot
$rootDir = Split-Path $scriptDir -Parent

switch ($Action) {
    "start" {
        if (-not $Param1) {
            Write-Red "❌ Virhe: Anna tehtävän kuvaus."
            Write-Yellow "Käyttö: .\trm_session.ps1 start `"Tehtävän kuvaus`""
            exit 1
        }
        Write-Cyan "`n🚀 Aloitetaan uusi TRM-sessio...`n"
        python "$scriptDir\trm_start_session.py" $Param1
    }
    
    "update" {
        if (-not $Param1) {
            Write-Red "❌ Virhe: Anna kierroksen numero (1-10)."
            Write-Yellow "Käyttö: .\trm_session.ps1 update <kierros> [opit]"
            exit 1
        }
        Write-Cyan "`n🔄 Päivitetään TRM-muisti (kierros $Param1)...`n"
        if ($Param2) {
            python "$scriptDir\trm_update_memory.py" $Param1 $Param2
        } else {
            python "$scriptDir\trm_update_memory.py" $Param1
        }
    }
    
    "finalize" {
        if (-not $Param1) {
            Write-Red "❌ Virhe: Anna lopputulos/päätelmä."
            Write-Yellow "Käyttö: .\trm_session.ps1 finalize `"Lopputulos ja hyväksymiskriteerit`""
            exit 1
        }
        Write-Cyan "`n✅ Suljetaan TRM-sessio...`n"
        python "$scriptDir\trm_finalize_session.py" $Param1
    }
}

if ($LASTEXITCODE -ne 0) {
    Write-Red "`n❌ TRM-komento epäonnistui (exit code: $LASTEXITCODE)"
    exit $LASTEXITCODE
}

Write-Green "`n✅ TRM-komento suoritettu onnistuneesti.`n"
