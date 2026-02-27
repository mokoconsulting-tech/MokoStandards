<#
.SYNOPSIS
    PowerShell wrapper template for Python scripts.

.DESCRIPTION
    Provides a convenient way to call Python scripts from PowerShell with proper error handling,
    logging, and cross-platform support.

.NOTES
    File Name   : wrapper-template.ps1
    Author      : Moko Consulting <hello@mokoconsulting.tech>
    Version     : 03.00.00
    License     : GPL-3.0-or-later

.PARAMETER Arguments
    All arguments to pass to the Python script.

.EXAMPLE
    .\wrapper.ps1 --dry-run --verbose
#>

[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments)]
    [string[]]$Arguments
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Script Configuration - UPDATE THESE FOR EACH WRAPPER
$ScriptName = "validate_file_headers"
$ScriptPath = "scripts/maintenance/validate_file_headers.py"
$ScriptCategory = "maintenance"  # automation, validation, maintenance, etc.

#region Helper Functions

function Write-InfoLog {
    param([string]$Message)
    Write-Host "ℹ️  $Message" -ForegroundColor Blue
}

function Write-SuccessLog {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-WarningLog {
    param([string]$Message)
    Write-Host "⚠️  $Message" -ForegroundColor Yellow
}

function Write-ErrorLog {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

function Get-RepoRoot {
    try {
        $gitRoot = git rev-parse --show-toplevel 2>$null
        if ($gitRoot) {
            return $gitRoot
        }
    }
    catch {
        # Not in a git repository
    }
    return $PWD.Path
}

function Get-PythonCommand {
    $pythonCommands = @('python3', 'python', 'py')
    
    foreach ($cmd in $pythonCommands) {
        try {
            $null = Get-Command $cmd -ErrorAction Stop
            # Verify it's Python 3
            $version = & $cmd --version 2>&1
            if ($version -match 'Python 3') {
                return $cmd
            }
        }
        catch {
            continue
        }
    }
    
    Write-ErrorLog "Python 3 is not installed or not in PATH"
    Write-Host "Please install Python 3.7 or later from https://www.python.org/"
    exit 1
}

#endregion

#region Main Execution

try {
    # Get repository root
    $repoRoot = Get-RepoRoot
    
    # Get Python command
    $pythonCmd = Get-PythonCommand
    
    # Build full script path
    $fullScriptPath = Join-Path $repoRoot $ScriptPath
    
    # Check if script exists
    if (-not (Test-Path $fullScriptPath)) {
        Write-ErrorLog "Python script not found: $fullScriptPath"
        exit 1
    }
    
    # Setup logging directory
    $logDir = Join-Path $repoRoot "logs/$ScriptCategory"
    if (-not (Test-Path $logDir)) {
        New-Item -ItemType Directory -Path $logDir -Force | Out-Null
    }
    
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $logFile = Join-Path $logDir "${ScriptName}_${timestamp}.log"
    
    # Execute Python script with all arguments
    Write-InfoLog "Running $ScriptName..."
    Write-InfoLog "Log file: $logFile"
    
    # Build argument list
    $pythonArgs = @($fullScriptPath) + $Arguments
    
    # Execute and capture output
    $output = & $pythonCmd @pythonArgs 2>&1 | Tee-Object -FilePath $logFile
    $exitCode = $LASTEXITCODE
    
    if ($exitCode -eq 0) {
        Write-SuccessLog "$ScriptName completed successfully"
        exit 0
    }
    else {
        Write-ErrorLog "$ScriptName failed with exit code: $exitCode"
        Write-InfoLog "Check log file for details: $logFile"
        exit $exitCode
    }
}
catch {
    Write-ErrorLog "Wrapper execution failed: $_"
    exit 1
}

#endregion
