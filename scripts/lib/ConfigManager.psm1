# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# This file is part of a Moko Consulting project.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# (./LICENSE).
#
# FILE INFORMATION
# DEFGROUP: MokoStandards.Scripts
# INGROUP: MokoStandards.Library
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# FILE: scripts/powershell/lib/ConfigManager.psm1
# VERSION: 02.00.00
# BRIEF: Centralized configuration management for MokoStandards PowerShell scripts
# PATH: /scripts/powershell/lib/ConfigManager.psm1
# NOTE: Provides YAML-based configuration with environment overrides

<#
.SYNOPSIS
Configuration Manager for MokoStandards PowerShell Scripts.

.DESCRIPTION
This module provides centralized configuration management with:
- XML-based configuration files (MokoStandards.override.xml support)
- Environment variable overrides (MOKOSTANDARDS_* prefix)
- Schema validation
- In-memory caching for performance
- Type-safe configuration access
- Sensible defaults

.EXAMPLE
Basic usage:
    $config = Get-MokoConfig
    Write-Host $config.Organization.Name

.EXAMPLE
Custom config path:
    $config = Get-MokoConfig -ConfigPath "custom-config.yaml"

.EXAMPLE
Using Get() method with defaults:
    $value = Get-MokoConfigValue -Key "github.api_rate_limit" -Default 5000
#>

# ============================================================
# Module Variables
# ============================================================

$script:ConfigCache = $null
$script:ConfigPath = $null
$script:ValueCache = @{}

# Default configuration paths
$homeDir = if ($env:USERPROFILE) { $env:USERPROFILE } elseif ($env:HOME) { $env:HOME } else { "~" }
$script:DefaultConfigPath = Join-Path $homeDir ".mokostandards" "config.yaml"
$script:SyncConfigName = "MokoStandards.override.xml"

# ============================================================
# Configuration Classes
# ============================================================

class OrgConfig {
    <#
    .SYNOPSIS
    Organization configuration.
    #>
    [string]$Name = "mokoconsulting-tech"
    [int]$ProjectNumber = 7
}

class GitHubConfig {
    <#
    .SYNOPSIS
    GitHub API configuration.
    #>
    [int]$ApiRateLimit = 5000
    [int]$RetryAttempts = 3
    [double]$RetryBackoffBase = 2.0
    [int]$TimeoutSeconds = 30
    [string]$TokenEnvVar = "GH_PAT"
}

class AutomationConfig {
    <#
    .SYNOPSIS
    Automation scripts configuration.
    #>
    [string]$DefaultBranch = "chore/sync-mokostandards-updates"
    [string]$TempDir = "$env:TEMP\mokostandards"
    [bool]$ConfirmationRequired = $true
}

class ValidationConfig {
    <#
    .SYNOPSIS
    Validation scripts configuration.
    #>
    [string[]]$ExcludedDirs = @(
        "vendor",
        "node_modules",
        "dist",
        "build",
        ".git",
        "__pycache__"
    )
    [int]$MaxFileSizeMB = 10
    [int]$MaxResults = 50
}

class AuditConfig {
    <#
    .SYNOPSIS
    Audit logging configuration.
    #>
    [bool]$Enabled = $true
    [string]$LogDir = "~/.mokostandards/logs"
    [int]$RetentionDays = 90
    [string]$Format = "json"
}

class SyncConfig {
    <#
    .SYNOPSIS
    Sync configuration for MokoStandards.override.xml files.
    #>
    [bool]$Enabled = $true
    [string[]]$ExcludeFiles = @()
    [string[]]$ProtectedFiles = @()
}

class RepositoryConfig {
    <#
    .SYNOPSIS
    Repository-specific configuration.
    #>
    [string]$ComplianceLevel = "standard"
}

class MokoConfig {
    <#
    .SYNOPSIS
    Main configuration container.
    #>
    [OrgConfig]$Organization
    [GitHubConfig]$GitHub
    [AutomationConfig]$Automation
    [ValidationConfig]$Validation
    [AuditConfig]$Audit
    [SyncConfig]$Sync
    [RepositoryConfig]$Repository
    [string]$ConfigVersion = "2.0"

    MokoConfig() {
        $this.Organization = [OrgConfig]::new()
        $this.GitHub = [GitHubConfig]::new()
        $this.Automation = [AutomationConfig]::new()
        $this.Validation = [ValidationConfig]::new()
        $this.Audit = [AuditConfig]::new()
        $this.Sync = [SyncConfig]::new()
        $this.Repository = [RepositoryConfig]::new()
    }
}

# ============================================================
# Helper Functions
# ============================================================

function Resolve-ConfigPath {
    <#
    .SYNOPSIS
    Resolve the configuration file path.
    
    .DESCRIPTION
    Priority order:
    1. Explicitly provided path
    2. MokoStandards.override.xml in current directory
    3. MokoStandards.override.xml walking up directory tree
    4. Default path (~/.mokostandards/config.yaml)
    
    .PARAMETER ConfigPath
    Optional explicitly provided path.
    
    .OUTPUTS
    String path to configuration file.
    #>
    [OutputType([string])]
    param(
        [Parameter()]
        [string]$ConfigPath
    )

    if ($ConfigPath) {
        return $ConfigPath
    }

    # Check for MokoStandards.override.xml in current and parent directories
    $currentDir = Get-Location
    $searchDir = $currentDir.Path

    while ($searchDir) {
        $syncConfig = Join-Path $searchDir $script:SyncConfigName
        if (Test-Path -Path $syncConfig -ErrorAction SilentlyContinue) {
            return $syncConfig
        }

        $parent = Split-Path $searchDir -Parent
        if (-not $parent -or $parent -eq $searchDir) {
            break
        }
        $searchDir = $parent
    }

    # Fall back to default
    return $script:DefaultConfigPath
}

function Test-YamlModuleAvailable {
    <#
    .SYNOPSIS
    Check if powershell-yaml module is available.
    
    .OUTPUTS
    Boolean indicating if module is available.
    #>
    [OutputType([bool])]
    param()

    $module = Get-Module -ListAvailable -Name powershell-yaml -ErrorAction SilentlyContinue
    return $null -ne $module
}

function ConvertFrom-YamlFile {
    <#
    .SYNOPSIS
    Load YAML file into PowerShell object.
    
    .PARAMETER Path
    Path to YAML file.
    
    .OUTPUTS
    Hashtable representation of YAML content.
    #>
    [OutputType([hashtable])]
    param(
        [Parameter(Mandatory)]
        [string]$Path
    )

    if (Test-YamlModuleAvailable) {
        Import-Module powershell-yaml -ErrorAction Stop
        $content = Get-Content -Path $Path -Raw
        return ConvertFrom-Yaml $content
    }
    else {
        Write-Warning "powershell-yaml module not installed. Cannot load YAML configuration."
        Write-Warning "Install with: Install-Module -Name powershell-yaml"
        Write-Warning "Continuing with default configuration values."
        return @{}
    }
}

function ConvertTo-YamlFile {
    <#
    .SYNOPSIS
    Save PowerShell object to YAML file.
    
    .PARAMETER Data
    Hashtable to convert to YAML.
    
    .PARAMETER Path
    Output file path.
    #>
    param(
        [Parameter(Mandatory)]
        [hashtable]$Data,

        [Parameter(Mandatory)]
        [string]$Path
    )

    if (Test-YamlModuleAvailable) {
        Import-Module powershell-yaml -ErrorAction Stop
        $yaml = ConvertTo-Yaml $Data
        Set-Content -Path $Path -Value $yaml -Encoding UTF8
    }
    else {
        throw "powershell-yaml module is required to save configuration. Install with: Install-Module -Name powershell-yaml"
    }
}

function Merge-ConfigData {
    <#
    .SYNOPSIS
    Merge source hashtable into destination hashtable.
    
    .PARAMETER Destination
    Destination hashtable.
    
    .PARAMETER Source
    Source hashtable.
    #>
    param(
        [Parameter(Mandatory)]
        [hashtable]$Destination,

        [Parameter(Mandatory)]
        [hashtable]$Source
    )

    foreach ($key in $Source.Keys) {
        if ($Source[$key] -is [hashtable] -and $Destination.ContainsKey($key) -and $Destination[$key] -is [hashtable]) {
            Merge-ConfigData -Destination $Destination[$key] -Source $Source[$key]
        }
        else {
            $Destination[$key] = $Source[$key]
        }
    }
}

function Get-EnvironmentOverrides {
    <#
    .SYNOPSIS
    Get configuration overrides from environment variables.
    
    .DESCRIPTION
    Environment variables with MOKOSTANDARDS_* prefix override config values.
    
    .OUTPUTS
    Hashtable with environment overrides.
    #>
    [OutputType([hashtable])]
    param()

    $overrides = @{}

    # Organization overrides
    if ($env:MOKOSTANDARDS_ORG) {
        if (-not $overrides.ContainsKey('organization')) {
            $overrides['organization'] = @{}
        }
        $overrides['organization']['name'] = $env:MOKOSTANDARDS_ORG
    }

    if ($env:MOKOSTANDARDS_ORG_PROJECT_NUMBER) {
        if (-not $overrides.ContainsKey('organization')) {
            $overrides['organization'] = @{}
        }
        try {
            $overrides['organization']['project_number'] = [int]$env:MOKOSTANDARDS_ORG_PROJECT_NUMBER
        }
        catch {
            Write-Warning "Invalid MOKOSTANDARDS_ORG_PROJECT_NUMBER value: $env:MOKOSTANDARDS_ORG_PROJECT_NUMBER"
        }
    }

    # GitHub token override
    if ($env:GH_PAT) {
        if (-not $overrides.ContainsKey('github')) {
            $overrides['github'] = @{}
        }
        $overrides['github']['token_env_var'] = 'GH_PAT'
    }
    elseif ($env:GITHUB_TOKEN) {
        if (-not $overrides.ContainsKey('github')) {
            $overrides['github'] = @{}
        }
        $overrides['github']['token_env_var'] = 'GITHUB_TOKEN'
    }

    # GitHub configuration overrides
    if ($env:MOKOSTANDARDS_GITHUB_RATE_LIMIT) {
        if (-not $overrides.ContainsKey('github')) {
            $overrides['github'] = @{}
        }
        try {
            $overrides['github']['api_rate_limit'] = [int]$env:MOKOSTANDARDS_GITHUB_RATE_LIMIT
        }
        catch {
            Write-Warning "Invalid MOKOSTANDARDS_GITHUB_RATE_LIMIT value: $env:MOKOSTANDARDS_GITHUB_RATE_LIMIT"
        }
    }

    # Automation overrides
    if ($env:MOKOSTANDARDS_TEMP_DIR) {
        if (-not $overrides.ContainsKey('automation')) {
            $overrides['automation'] = @{}
        }
        $overrides['automation']['temp_dir'] = $env:MOKOSTANDARDS_TEMP_DIR
    }

    if ($env:MOKOSTANDARDS_DEFAULT_BRANCH) {
        if (-not $overrides.ContainsKey('automation')) {
            $overrides['automation'] = @{}
        }
        $overrides['automation']['default_branch'] = $env:MOKOSTANDARDS_DEFAULT_BRANCH
    }

    if ($env:MOKOSTANDARDS_CONFIRMATION_REQUIRED) {
        if (-not $overrides.ContainsKey('automation')) {
            $overrides['automation'] = @{}
        }
        $overrides['automation']['confirmation_required'] = $env:MOKOSTANDARDS_CONFIRMATION_REQUIRED -in @('true', '1', 'yes')
    }

    # Audit overrides
    if ($env:MOKOSTANDARDS_AUDIT_ENABLED) {
        if (-not $overrides.ContainsKey('audit')) {
            $overrides['audit'] = @{}
        }
        $overrides['audit']['enabled'] = $env:MOKOSTANDARDS_AUDIT_ENABLED -in @('true', '1', 'yes')
    }

    if ($env:MOKOSTANDARDS_AUDIT_LOG_DIR) {
        if (-not $overrides.ContainsKey('audit')) {
            $overrides['audit'] = @{}
        }
        $overrides['audit']['log_dir'] = $env:MOKOSTANDARDS_AUDIT_LOG_DIR
    }

    # Sync overrides
    if ($env:MOKOSTANDARDS_SYNC_ENABLED) {
        if (-not $overrides.ContainsKey('sync')) {
            $overrides['sync'] = @{}
        }
        $overrides['sync']['enabled'] = $env:MOKOSTANDARDS_SYNC_ENABLED -in @('true', '1', 'yes')
    }

    return $overrides
}

function Build-ConfigFromData {
    <#
    .SYNOPSIS
    Build MokoConfig object from hashtable data.
    
    .PARAMETER Data
    Configuration data hashtable.
    
    .OUTPUTS
    MokoConfig object.
    #>
    [OutputType([MokoConfig])]
    param(
        [Parameter(Mandatory)]
        [hashtable]$Data
    )

    $config = [MokoConfig]::new()

    # Build organization config
    if ($Data.ContainsKey('organization')) {
        $org = $Data['organization']
        if ($org.ContainsKey('name')) {
            $config.Organization.Name = $org['name']
        }
        if ($org.ContainsKey('project_number')) {
            $config.Organization.ProjectNumber = $org['project_number']
        }
    }

    # Build GitHub config
    if ($Data.ContainsKey('github')) {
        $gh = $Data['github']
        if ($gh.ContainsKey('api_rate_limit')) {
            $config.GitHub.ApiRateLimit = $gh['api_rate_limit']
        }
        if ($gh.ContainsKey('retry_attempts')) {
            $config.GitHub.RetryAttempts = $gh['retry_attempts']
        }
        if ($gh.ContainsKey('retry_backoff_base')) {
            $config.GitHub.RetryBackoffBase = $gh['retry_backoff_base']
        }
        if ($gh.ContainsKey('timeout_seconds')) {
            $config.GitHub.TimeoutSeconds = $gh['timeout_seconds']
        }
        if ($gh.ContainsKey('token_env_var')) {
            $config.GitHub.TokenEnvVar = $gh['token_env_var']
        }
    }

    # Build automation config
    if ($Data.ContainsKey('automation')) {
        $auto = $Data['automation']
        if ($auto.ContainsKey('default_branch')) {
            $config.Automation.DefaultBranch = $auto['default_branch']
        }
        if ($auto.ContainsKey('temp_dir')) {
            $config.Automation.TempDir = $auto['temp_dir']
        }
        if ($auto.ContainsKey('confirmation_required')) {
            $config.Automation.ConfirmationRequired = $auto['confirmation_required']
        }
    }

    # Build validation config
    if ($Data.ContainsKey('validation')) {
        $val = $Data['validation']
        if ($val.ContainsKey('excluded_dirs')) {
            $config.Validation.ExcludedDirs = $val['excluded_dirs']
        }
        if ($val.ContainsKey('max_file_size_mb')) {
            $config.Validation.MaxFileSizeMB = $val['max_file_size_mb']
        }
        if ($val.ContainsKey('max_results')) {
            $config.Validation.MaxResults = $val['max_results']
        }
    }

    # Build audit config
    if ($Data.ContainsKey('audit')) {
        $audit = $Data['audit']
        if ($audit.ContainsKey('enabled')) {
            $config.Audit.Enabled = $audit['enabled']
        }
        if ($audit.ContainsKey('log_dir')) {
            $config.Audit.LogDir = $audit['log_dir']
        }
        if ($audit.ContainsKey('retention_days')) {
            $config.Audit.RetentionDays = $audit['retention_days']
        }
        if ($audit.ContainsKey('format')) {
            $config.Audit.Format = $audit['format']
        }
    }

    # Build sync config
    if ($Data.ContainsKey('sync')) {
        $sync = $Data['sync']
        if ($sync.ContainsKey('enabled')) {
            $config.Sync.Enabled = $sync['enabled']
        }
        if ($sync.ContainsKey('exclude_files')) {
            $config.Sync.ExcludeFiles = $sync['exclude_files']
        }
        if ($sync.ContainsKey('protected_files')) {
            $config.Sync.ProtectedFiles = $sync['protected_files']
        }
    }

    # Build repository config
    if ($Data.ContainsKey('repository')) {
        $repo = $Data['repository']
        if ($repo.ContainsKey('compliance_level')) {
            $config.Repository.ComplianceLevel = $repo['compliance_level']
        }
    }

    # Config version
    if ($Data.ContainsKey('config_version')) {
        $config.ConfigVersion = $Data['config_version']
    }

    return $config
}

# ============================================================
# Public Functions
# ============================================================

function Get-MokoConfig {
    <#
    .SYNOPSIS
    Get MokoStandards configuration.
    
    .DESCRIPTION
    Loads configuration from YAML file with environment variable overrides.
    Results are cached for performance.
    
    .PARAMETER ConfigPath
    Optional path to configuration file. If not provided, searches for
    MokoStandards.override.xml or uses default path.
    
    .PARAMETER Force
    Force reload configuration, bypassing cache.
    
    .OUTPUTS
    MokoConfig object.
    
    .EXAMPLE
    $config = Get-MokoConfig
    Write-Host $config.Organization.Name
    
    .EXAMPLE
    $config = Get-MokoConfig -ConfigPath "custom-config.yaml"
    #>
    [CmdletBinding()]
    [OutputType([MokoConfig])]
    param(
        [Parameter()]
        [string]$ConfigPath,

        [Parameter()]
        [switch]$Force
    )

    # Resolve config path
    $resolvedPath = Resolve-ConfigPath -ConfigPath $ConfigPath

    # Return cached config if available and not forcing reload
    if (-not $Force -and $script:ConfigCache -and $script:ConfigPath -eq $resolvedPath) {
        return $script:ConfigCache
    }

    # Update cached path
    $script:ConfigPath = $resolvedPath

    # Initialize with defaults
    $data = @{}

    # Load from file if exists
    if (Test-Path -Path $resolvedPath -ErrorAction SilentlyContinue) {
        try {
            $fileData = ConvertFrom-YamlFile -Path $resolvedPath
            if ($fileData) {
                $data = $fileData
            }
        }
        catch {
            Write-Warning "Failed to load config from ${resolvedPath}: $_"
        }
    }

    # Apply environment overrides
    $envOverrides = Get-EnvironmentOverrides
    if ($envOverrides.Count -gt 0) {
        Merge-ConfigData -Destination $data -Source $envOverrides
    }

    # Validate configuration
    try {
        Test-MokoConfigData -Data $data
    }
    catch {
        Write-Warning "Configuration validation failed: $_"
    }

    # Build config object
    $config = Build-ConfigFromData -Data $data

    # Cache the config
    $script:ConfigCache = $config
    $script:ValueCache.Clear()

    return $config
}

function Set-MokoConfig {
    <#
    .SYNOPSIS
    Save MokoStandards configuration template to file.
    
    .DESCRIPTION
    Creates a configuration template file with default values.
    
    .PARAMETER Path
    Path where to save the configuration template.
    If not provided, uses the resolved config path.
    
    .OUTPUTS
    String path where template was saved.
    
    .EXAMPLE
    Set-MokoConfig -Path "config.yaml"
    
    .EXAMPLE
    Set-MokoConfig
    #>
    [CmdletBinding()]
    [OutputType([string])]
    param(
        [Parameter()]
        [string]$Path
    )

    if (-not $Path) {
        $Path = Resolve-ConfigPath
    }

    # Ensure directory exists
    $directory = Split-Path $Path -Parent
    if ($directory -and -not (Test-Path -Path $directory -ErrorAction SilentlyContinue)) {
        New-Item -Path $directory -ItemType Directory -Force | Out-Null
    }

    $template = @{
        config_version = '2.0'
        organization   = @{
            name           = 'mokoconsulting-tech'
            project_number = 7
        }
        github         = @{
            api_rate_limit      = 5000
            retry_attempts      = 3
            retry_backoff_base  = 2.0
            timeout_seconds     = 30
            token_env_var       = 'GH_PAT'
        }
        automation     = @{
            default_branch         = 'chore/sync-mokostandards-updates'
            temp_dir               = if ($env:TEMP) { "$env:TEMP\mokostandards" } elseif ($env:TMPDIR) { "$env:TMPDIR/mokostandards" } else { "/tmp/mokostandards" }
            confirmation_required  = $true
        }
        validation     = @{
            excluded_dirs   = @(
                'vendor',
                'node_modules',
                'dist',
                'build',
                '.git',
                '__pycache__'
            )
            max_file_size_mb = 10
            max_results      = 50
        }
        audit          = @{
            enabled        = $true
            log_dir        = '~/.mokostandards/logs'
            retention_days = 90
            format         = 'json'
        }
        sync           = @{
            enabled         = $true
            exclude_files   = @()
            protected_files = @()
        }
        repository     = @{
            compliance_level = 'standard'
        }
    }

    ConvertTo-YamlFile -Data $template -Path $Path
    Write-Host "✅ Configuration template saved to: $Path"

    return $Path
}

function Test-MokoConfig {
    <#
    .SYNOPSIS
    Validate a MokoStandards configuration file.
    
    .DESCRIPTION
    Validates configuration file structure and values without loading it into cache.
    
    .PARAMETER Path
    Path to configuration file to validate.
    
    .OUTPUTS
    Boolean indicating if configuration is valid.
    
    .EXAMPLE
    Test-MokoConfig -Path "config.yaml"
    #>
    [CmdletBinding()]
    [OutputType([bool])]
    param(
        [Parameter(Mandatory)]
        [string]$Path
    )

    if (-not (Test-Path -Path $Path -ErrorAction SilentlyContinue)) {
        Write-Error "Config file not found: $Path"
        return $false
    }

    if (-not (Test-YamlModuleAvailable)) {
        Write-Error "powershell-yaml module not installed"
        return $false
    }

    try {
        $data = ConvertFrom-YamlFile -Path $Path

        if (-not $data) {
            Write-Error "Config file is empty"
            return $false
        }

        Test-MokoConfigData -Data $data
        Write-Host "✅ Config file is valid: $Path"
        return $true
    }
    catch {
        Write-Error "Validation error: $_"
        return $false
    }
}

function Test-MokoConfigData {
    <#
    .SYNOPSIS
    Validate configuration data structure and values.
    
    .PARAMETER Data
    Configuration data hashtable to validate.
    
    .EXAMPLE
    Test-MokoConfigData -Data $configData
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [hashtable]$Data
    )

    # Validate organization config
    if ($Data.ContainsKey('organization')) {
        $org = $Data['organization']
        if ($org -isnot [hashtable]) {
            throw "'organization' must be a hashtable"
        }

        if ($org.ContainsKey('name') -and $org['name'] -isnot [string]) {
            throw "'organization.name' must be a string"
        }

        if ($org.ContainsKey('project_number')) {
            if ($org['project_number'] -isnot [int]) {
                throw "'organization.project_number' must be an integer"
            }
            if ($org['project_number'] -lt 0) {
                throw "'organization.project_number' must be non-negative"
            }
        }
    }

    # Validate GitHub config
    if ($Data.ContainsKey('github')) {
        $github = $Data['github']
        if ($github -isnot [hashtable]) {
            throw "'github' must be a hashtable"
        }

        if ($github.ContainsKey('api_rate_limit')) {
            if ($github['api_rate_limit'] -isnot [int]) {
                throw "'github.api_rate_limit' must be an integer"
            }
            if ($github['api_rate_limit'] -le 0) {
                throw "'github.api_rate_limit' must be positive"
            }
        }

        if ($github.ContainsKey('retry_attempts')) {
            if ($github['retry_attempts'] -isnot [int]) {
                throw "'github.retry_attempts' must be an integer"
            }
            if ($github['retry_attempts'] -lt 0) {
                throw "'github.retry_attempts' must be non-negative"
            }
        }

        if ($github.ContainsKey('timeout_seconds')) {
            if ($github['timeout_seconds'] -isnot [int]) {
                throw "'github.timeout_seconds' must be an integer"
            }
            if ($github['timeout_seconds'] -le 0) {
                throw "'github.timeout_seconds' must be positive"
            }
        }
    }

    # Validate validation config
    if ($Data.ContainsKey('validation')) {
        $validation = $Data['validation']
        if ($validation -isnot [hashtable]) {
            throw "'validation' must be a hashtable"
        }

        if ($validation.ContainsKey('excluded_dirs') -and $validation['excluded_dirs'] -isnot [array]) {
            throw "'validation.excluded_dirs' must be an array"
        }

        if ($validation.ContainsKey('max_file_size_mb')) {
            if ($validation['max_file_size_mb'] -isnot [int]) {
                throw "'validation.max_file_size_mb' must be an integer"
            }
            if ($validation['max_file_size_mb'] -le 0) {
                throw "'validation.max_file_size_mb' must be positive"
            }
        }
    }

    # Validate audit config
    if ($Data.ContainsKey('audit')) {
        $audit = $Data['audit']
        if ($audit -isnot [hashtable]) {
            throw "'audit' must be a hashtable"
        }

        if ($audit.ContainsKey('enabled') -and $audit['enabled'] -isnot [bool]) {
            throw "'audit.enabled' must be a boolean"
        }

        if ($audit.ContainsKey('format') -and $audit['format'] -notin @('json', 'csv')) {
            throw "'audit.format' must be 'json' or 'csv'"
        }
    }

    # Validate sync config
    if ($Data.ContainsKey('sync')) {
        $sync = $Data['sync']
        if ($sync -isnot [hashtable]) {
            throw "'sync' must be a hashtable"
        }

        if ($sync.ContainsKey('enabled') -and $sync['enabled'] -isnot [bool]) {
            throw "'sync.enabled' must be a boolean"
        }

        if ($sync.ContainsKey('exclude_files') -and $sync['exclude_files'] -isnot [array]) {
            throw "'sync.exclude_files' must be an array"
        }

        if ($sync.ContainsKey('protected_files') -and $sync['protected_files'] -isnot [array]) {
            throw "'sync.protected_files' must be an array"
        }
    }
}

function Reset-MokoConfig {
    <#
    .SYNOPSIS
    Clear cached configuration.
    
    .DESCRIPTION
    Clears the in-memory configuration cache, forcing reload on next access.
    
    .EXAMPLE
    Reset-MokoConfig
    #>
    [CmdletBinding()]
    param()

    $script:ConfigCache = $null
    $script:ConfigPath = $null
    $script:ValueCache.Clear()

    Write-Verbose "Configuration cache cleared"
}

function Get-MokoConfigValue {
    <#
    .SYNOPSIS
    Get configuration value by dot-notation key with caching.
    
    .DESCRIPTION
    Retrieves a specific configuration value using dot notation (e.g., 'github.api_rate_limit').
    Results are cached for performance.
    
    .PARAMETER Key
    Dot-notation key (e.g., 'github.api_rate_limit').
    
    .PARAMETER Default
    Default value if key not found.
    
    .PARAMETER ConfigPath
    Optional path to configuration file.
    
    .OUTPUTS
    Configuration value or default.
    
    .EXAMPLE
    $rateLimit = Get-MokoConfigValue -Key "github.api_rate_limit" -Default 5000
    
    .EXAMPLE
    $orgName = Get-MokoConfigValue -Key "organization.name" -Default "unknown"
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Key,

        [Parameter()]
        [object]$Default,

        [Parameter()]
        [string]$ConfigPath
    )

    # Check cache first
    if ($script:ValueCache.ContainsKey($Key)) {
        return $script:ValueCache[$Key]
    }

    # Get config
    $config = Get-MokoConfig -ConfigPath $ConfigPath

    # Navigate nested properties
    $parts = $Key -split '\.'
    $value = $config

    try {
        foreach ($part in $parts) {
            $value = $value.$part
        }
        
        # Cache the value
        $script:ValueCache[$Key] = $value
        return $value
    }
    catch {
        return $Default
    }
}

function Export-MokoConfigToJson {
    <#
    .SYNOPSIS
    Export configuration to JSON format.
    
    .DESCRIPTION
    Converts the current configuration to JSON string representation.
    
    .PARAMETER ConfigPath
    Optional path to configuration file.
    
    .PARAMETER Depth
    Maximum depth for JSON conversion (default: 10).
    
    .OUTPUTS
    JSON string representation of configuration.
    
    .EXAMPLE
    $json = Export-MokoConfigToJson
    Write-Host $json
    
    .EXAMPLE
    Export-MokoConfigToJson | Out-File "config.json"
    #>
    [CmdletBinding()]
    [OutputType([string])]
    param(
        [Parameter()]
        [string]$ConfigPath,

        [Parameter()]
        [int]$Depth = 10
    )

    $config = Get-MokoConfig -ConfigPath $ConfigPath
    return $config | ConvertTo-Json -Depth $Depth
}

# ============================================================
# Module Export
# ============================================================

Export-ModuleMember -Function @(
    'Get-MokoConfig',
    'Set-MokoConfig',
    'Test-MokoConfig',
    'Reset-MokoConfig',
    'Get-MokoConfigValue',
    'Export-MokoConfigToJson'
)
