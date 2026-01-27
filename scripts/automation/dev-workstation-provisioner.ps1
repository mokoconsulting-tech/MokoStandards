# =========================================================
# Dev Bootstrapper: Winget Monthly Task + Optional WSL Ubuntu
# =========================================================

param(
	[switch]$VerboseMode
)

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName Microsoft.VisualBasic

function Log {
	param([string]$Message)
	if ($VerboseMode) {
		Write-Host "[INFO] $Message"
	}
}

function Require-Admin {
	$id = [Security.Principal.WindowsIdentity]::GetCurrent()
	$p  = New-Object Security.Principal.WindowsPrincipal($id)
	if (-not $p.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
		[System.Windows.Forms.MessageBox]::Show(
			"Run this script as Administrator.",
			"Elevation Required",
			[System.Windows.Forms.MessageBoxButtons]::OK,
			[System.Windows.Forms.MessageBoxIcon]::Error
		) | Out-Null
		exit 1
	}
}

function Ensure-Folder([string]$Path) {
	if (-not (Test-Path $Path)) {
		New-Item -ItemType Directory -Path $Path -Force | Out-Null
	}
}

function Get-DefaultWorkspacePath {
	Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'Workspace'
}

function Write-WingetMonthlyCmd([string]$CmdPath) {
@"
@echo off
setlocal

set LOGROOT=C:\Logs\Winget
if not exist %LOGROOT% mkdir %LOGROOT%

for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value ^| find "="') do set LDT=%%I
set STAMP=%LDT:~0,8%
set LOGFILE=%LOGROOT%\winget-upgrade-%STAMP%.log

echo [%DATE% %TIME%] Starting winget upgrade >> "%LOGFILE%"
winget upgrade --all --silent --accept-package-agreements --accept-source-agreements ^
	--exclude Python.Python.3.10 ^
	--exclude PHP.PHP >> "%LOGFILE%" 2>&1

echo [%DATE% %TIME%] Completed winget upgrade >> "%LOGFILE%"
endlocal
"@ | Set-Content -Path $CmdPath -Encoding ASCII
}

function Create-MonthlyTask {
	param(
		[string]$TaskName,
		[string]$CmdPath,
		[int]$Day,
		[string]$Time
	)

	schtasks /Delete /TN $TaskName /F *> $null 2>&1 | Out-Null
	schtasks /Create /F `
		/TN $TaskName `
		/SC MONTHLY `
		/D $Day `
		/ST $Time `
		/RL HIGHEST `
		/TR "cmd.exe /c `"$CmdPath`""
}

function Get-WSLState {
	try {
		Get-Command wsl -ErrorAction Stop | Out-Null
	} catch {
		return 'missing'
	}

	$distros = @()
	try {
		$distros = (wsl -l -q 2>$null) | Where-Object { $_ -and $_.Trim() }
	} catch {
		return 'not_installed'
	}

	if ($distros.Count -gt 0) { return 'installed' }
	return 'not_installed'
}

function Enable-WSLFeatures {
	Log "Enabling WSL features"
	dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart | Out-Null
	dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart | Out-Null
}

function Install-Ubuntu {
	Log "Installing Ubuntu WSL distro"
	wsl --install -d Ubuntu | Out-Null
}

function Reset-WSL {
	Log "Resetting WSL"
	wsl --shutdown
	wsl --unregister Ubuntu
	wsl --install -d Ubuntu | Out-Null
}

function Provision-UbuntuPHP {
	Log "Provisioning PHP inside Ubuntu"
	$bash = @'
set -euo pipefail

sudo apt update
sudo apt install -y \
	php8.3-cli php8.3-common php8.3-opcache php8.3-mysql \
	php8.3-curl php8.3-mbstring php8.3-intl php8.3-gd php8.3-zip php8.3-soap \
	php8.3-imagick php8.3-apcu php8.3-imap

sudo phpenmod -v 8.3 -s cli \
	curl mbstring intl gd zip soap imagick opcache mysqli pdo_mysql apcu imap

php -v
php -m | sort
'@

	Start-Process wsl -ArgumentList @('-d','Ubuntu','--','bash','-lc',$bash) -Wait -NoNewWindow | Out-Null
}

# ------------------------
# Execution
# ------------------------
Require-Admin
Log "Bootstrap started"

# Workspace prompt
$workspace = [Microsoft.VisualBasic.Interaction]::InputBox(
	"What is your default Workspace folder?",
	"Workspace Folder",
	(Get-DefaultWorkspacePath)
).Trim()

if (-not $workspace) { exit 1 }
Ensure-Folder $workspace

# Write monthly update script
$cmdPath = Join-Path $workspace 'winget-monthly-update.cmd'
Write-WingetMonthlyCmd $cmdPath

# Schedule
$day  = 1
$time = '09:00'
Create-MonthlyTask `
	-TaskName 'Winget Monthly Update (Exclude PHP and Python)' `
	-CmdPath $cmdPath `
	-Day $day `
	-Time $time

# WSL logic
$wslState = Get-WSLState
Log "WSL state: $wslState"

if ($wslState -eq 'installed') {
	$reset = [System.Windows.Forms.MessageBox]::Show(
		"WSL is already installed.`r`nDo you want to RESET Ubuntu WSL?",
		"WSL Detected",
		[System.Windows.Forms.MessageBoxButtons]::YesNo,
		[System.Windows.Forms.MessageBoxIcon]::Warning
	)
	if ($reset -eq 'Yes') {
		Reset-WSL
		Provision-UbuntuPHP
	}
}
elseif ($wslState -ne 'installed') {
	$install = [System.Windows.Forms.MessageBox]::Show(
		"WSL is not fully provisioned.`r`nInstall WSL with Ubuntu?",
		"WSL Not Installed",
		[System.Windows.Forms.MessageBoxButtons]::YesNo,
		[System.Windows.Forms.MessageBoxIcon]::Question
	)
	if ($install -eq 'Yes') {
		Enable-WSLFeatures
		Install-Ubuntu
		Provision-UbuntuPHP
	}
}

[System.Windows.Forms.MessageBox]::Show(
	"Bootstrap completed successfully.",
	"Done",
	[System.Windows.Forms.MessageBoxButtons]::OK,
	[System.Windows.Forms.MessageBoxIcon]::Information
) | Out-Null
