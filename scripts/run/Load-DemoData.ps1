<#
.SYNOPSIS
    Demo Data Loader for Joomla/Dolibarr (Remote)

.DESCRIPTION
    This script loads SQL demo data into a MySQL/MariaDB database from a remote system.
    It can parse Joomla or Dolibarr configuration files or accept manual server entry.

.PARAMETER SqlFile
    Path to SQL file to load (required)

.PARAMETER ConfigFile
    Path to Joomla/Dolibarr configuration file

.PARAMETER IniConfig
    Path to demo loader INI configuration file

.PARAMETER Host
    Database host

.PARAMETER Port
    Database port (default: 3306)

.PARAMETER User
    Database username

.PARAMETER Password
    Database password

.PARAMETER Database
    Database name

.PARAMETER Prefix
    Table prefix

.PARAMETER NoIpCheck
    Skip IP whitelist check

.EXAMPLE
    .\Load-DemoData.ps1 -SqlFile demo_data.sql

.EXAMPLE
    .\Load-DemoData.ps1 -SqlFile demo_data.sql -ConfigFile C:\joomla\configuration.php

.EXAMPLE
    .\Load-DemoData.ps1 -SqlFile demo_data.sql -Host localhost -User root -Database mydb

.NOTES
    AUTHOR: Moko Consulting LLC
    COPYRIGHT: 2025-2026 Moko Consulting LLC
    LICENSE: MIT
    VERSION: 01.00.00
    CREATED: 2026-01-29
    UPDATED: 2026-01-29
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [string]$SqlFile,
    
    [Parameter()]
    [string]$ConfigFile,
    
    [Parameter()]
    [string]$IniConfig = "demo_loader_config.ini",
    
    [Parameter()]
    [string]$Host,
    
    [Parameter()]
    [int]$Port = 3306,
    
    [Parameter()]
    [string]$User,
    
    [Parameter()]
    [string]$Password,
    
    [Parameter()]
    [string]$Database,
    
    [Parameter()]
    [string]$Prefix,
    
    [Parameter()]
    [switch]$NoIpCheck
)

# Check for MySQL .NET Connector
$mysqlAvailable = $false
try {
    Add-Type -Path "MySql.Data.dll" -ErrorAction SilentlyContinue
    $mysqlAvailable = $true
} catch {
    Write-Warning "MySQL .NET Connector not found. Trying to load from GAC..."
    try {
        [void][System.Reflection.Assembly]::LoadWithPartialName("MySql.Data")
        $mysqlAvailable = $true
    } catch {
        Write-Error "MySQL .NET Connector is required. Download from: https://dev.mysql.com/downloads/connector/net/"
        exit 1
    }
}

function Get-ClientIP {
    try {
        $publicIp = (Invoke-WebRequest -Uri "http://ifconfig.me/ip" -UseBasicParsing -TimeoutSec 5).Content.Trim()
        return $publicIp
    } catch {
        return "unknown"
    }
}

function Test-IPWhitelist {
    param([string]$ConfigPath)
    
    if (-not (Test-Path $ConfigPath)) {
        Write-Warning "Config file not found: $ConfigPath"
        return $true
    }
    
    $config = Get-IniContent $ConfigPath
    
    if (-not $config.security -or -not $config.security.allowed_ips) {
        return $true
    }
    
    $allowedIps = $config.security.allowed_ips -split ',' | ForEach-Object { $_.Trim() }
    
    if ($allowedIps -contains '*') {
        return $true
    }
    
    $clientIp = Get-ClientIP
    
    if ($allowedIps -contains $clientIp) {
        return $true
    }
    
    Write-Error "Access denied. Your IP ($clientIp) is not authorized."
    return $false
}

function Get-IniContent {
    param([string]$Path)
    
    $ini = @{}
    $section = $null
    
    Get-Content $Path | ForEach-Object {
        $line = $_.Trim()
        
        if ($line -match '^\[(.+)\]$') {
            $section = $matches[1]
            $ini[$section] = @{}
        }
        elseif ($line -match '^([^#;].+?)\s*=\s*(.+)$') {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim()
            if ($section) {
                $ini[$section][$key] = $value
            }
        }
    }
    
    return $ini
}

function Parse-JoomlaConfig {
    param([string]$ConfigPath)
    
    if (-not (Test-Path $ConfigPath)) {
        return $null
    }
    
    $content = Get-Content $ConfigPath -Raw
    
    $config = @{}
    
    if ($content -match "public \`$host = '([^']+)'") { $config.host = $matches[1] }
    if ($content -match "public \`$user = '([^']+)'") { $config.user = $matches[1] }
    if ($content -match "public \`$password = '([^']+)'") { $config.password = $matches[1] }
    if ($content -match "public \`$db = '([^']+)'") { $config.db = $matches[1] }
    if ($content -match "public \`$dbprefix = '([^']*)'") { $config.dbprefix = $matches[1] }
    
    return $config
}

function Parse-DolibarrConfig {
    param([string]$ConfigPath)
    
    if (-not (Test-Path $ConfigPath)) {
        return $null
    }
    
    $content = Get-Content $ConfigPath -Raw
    
    $config = @{}
    
    if ($content -match '\$dolibarr_main_db_host\s*=\s*[''"]([^''"]+)') { $config.host = $matches[1] }
    if ($content -match '\$dolibarr_main_db_user\s*=\s*[''"]([^''"]+)') { $config.user = $matches[1] }
    if ($content -match '\$dolibarr_main_db_pass\s*=\s*[''"]([^''"]+)') { $config.password = $matches[1] }
    if ($content -match '\$dolibarr_main_db_name\s*=\s*[''"]([^''"]+)') { $config.db = $matches[1] }
    if ($content -match '\$dolibarr_main_db_prefix\s*=\s*[''"]([^''"]+)') { $config.dbprefix = $matches[1] }
    
    return $config
}

function Get-DatabaseConfigFromIni {
    param([string]$IniPath)
    
    if (-not (Test-Path $IniPath)) {
        return $null
    }
    
    $ini = Get-IniContent $IniPath
    
    if (-not $ini.database) {
        return $null
    }
    
    return @{
        host = $ini.database.host
        user = $ini.database.user
        password = $ini.database.password
        db = $ini.database.name
        dbprefix = $ini.database.prefix
    }
}

function Get-DatabaseCredentials {
    Write-Host "`nEnter database connection details:" -ForegroundColor Cyan
    
    $dbHost = Read-Host "Host [localhost]"
    if ([string]::IsNullOrWhiteSpace($dbHost)) { $dbHost = "localhost" }
    
    $dbUser = Read-Host "Username"
    $dbPass = Read-Host "Password" -AsSecureString
    $dbPassPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [Runtime.InteropServices.Marshal]::SecureStringToBSTR($dbPass)
    )
    $dbName = Read-Host "Database name"
    $dbPrefix = Read-Host "Table prefix (optional)"
    
    return @{
        host = $dbHost
        user = $dbUser
        password = $dbPassPlain
        db = $dbName
        dbprefix = $dbPrefix
    }
}

function Invoke-SqlFile {
    param(
        [object]$Connection,
        [string]$SqlFilePath,
        [string]$TablePrefix = ''
    )
    
    if (-not (Test-Path $SqlFilePath)) {
        Write-Error "SQL file not found: $SqlFilePath"
        return $false
    }
    
    Write-Host "Reading SQL file: $SqlFilePath"
    $content = Get-Content $SqlFilePath -Raw
    
    # Replace table prefix placeholder
    if ($TablePrefix -and $content -match '\{PREFIX\}') {
        $content = $content -replace '\{PREFIX\}', $TablePrefix
        Write-Host "Replaced {PREFIX} with: $TablePrefix"
    }
    
    # Split into statements
    $statements = $content -split ';' | Where-Object {
        $stmt = $_.Trim()
        $stmt -and -not $stmt.StartsWith('--')
    }
    
    Write-Host "Executing $($statements.Count) SQL statements..."
    
    $success = 0
    $errors = 0
    
    foreach ($statement in $statements) {
        $cmd = $Connection.CreateCommand()
        $cmd.CommandText = $statement.Trim()
        
        try {
            [void]$cmd.ExecuteNonQuery()
            $success++
        } catch {
            $errors++
            Write-Warning $_.Exception.Message
        } finally {
            $cmd.Dispose()
        }
    }
    
    Write-Host "`nDone! Success: $success, Errors: $errors" -ForegroundColor Green
    return $true
}

# Main execution
try {
    # Check IP whitelist
    if (-not $NoIpCheck -and -not (Test-IPWhitelist $IniConfig)) {
        exit 1
    }
    
    # Determine database configuration
    $dbConfig = $null
    $source = $null
    
    # Try command-line arguments first
    if ($Host -and $User -and $Database) {
        $dbConfig = @{
            host = $Host
            user = $User
            password = $Password
            db = $Database
            dbprefix = $Prefix
        }
        $source = "command-line"
    }
    
    # Try specified config file
    if (-not $dbConfig -and $ConfigFile) {
        if ($ConfigFile -like "*configuration.php") {
            $dbConfig = Parse-JoomlaConfig $ConfigFile
            if ($dbConfig) { $source = "Joomla" }
        }
        elseif ($ConfigFile -like "*conf.php") {
            $dbConfig = Parse-DolibarrConfig $ConfigFile
            if ($dbConfig) { $source = "Dolibarr" }
        }
    }
    
    # Try INI config file
    if (-not $dbConfig) {
        $dbConfig = Get-DatabaseConfigFromIni $IniConfig
        if ($dbConfig) { $source = "INI config" }
    }
    
    # Prompt for credentials
    if (-not $dbConfig) {
        $dbConfig = Get-DatabaseCredentials
        $source = "manual entry"
    }
    
    if (-not $dbConfig -or -not $dbConfig.user) {
        Write-Error "Database configuration incomplete"
        exit 1
    }
    
    Write-Host "Using database configuration from: $source" -ForegroundColor Cyan
    
    # Build connection string
    $connString = "Server=$($dbConfig.host);Port=$Port;Database=$($dbConfig.db);Uid=$($dbConfig.user);Pwd=$($dbConfig.password);CharSet=utf8mb4;"
    
    # Connect to database
    $connection = New-Object MySql.Data.MySqlClient.MySqlConnection($connString)
    $connection.Open()
    
    Write-Host "Connected to database: $($dbConfig.db)" -ForegroundColor Green
    
    # Load SQL file
    $success = Invoke-SqlFile -Connection $connection -SqlFilePath $SqlFile -TablePrefix $dbConfig.dbprefix
    
    $connection.Close()
    
    exit $(if ($success) { 0 } else { 1 })
    
} catch {
    Write-Error "Database connection failed: $($_.Exception.Message)"
    exit 1
}
