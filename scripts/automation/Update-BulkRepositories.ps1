<#
.SYNOPSIS
    Schema-driven bulk repository synchronization for Moko Consulting projects.

.DESCRIPTION
    Updates multiple GitHub repositories with standardized workflows, configurations,
    and maintenance scripts from MokoStandards repository. Automatically detects
    platform type (Joomla/Dolibarr/Generic) and syncs appropriate files.
    
    Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
    
    This file is part of a Moko Consulting project.
    
    SPDX-License-Identifier: GPL-3.0-or-later
    
    FILE INFORMATION
    DEFGROUP: MokoStandards.Automation
    INGROUP: MokoStandards.Scripts
    REPO: https://github.com/mokoconsulting-tech/MokoStandards
    PATH: /scripts/powershell/automation/Update-BulkRepositories.ps1
    VERSION: 02.00.00
    BRIEF: PowerShell implementation of bulk repository sync

.PARAMETER Organization
    GitHub organization name. Default: mokoconsulting-tech

.PARAMETER Repositories
    Specific repositories to update. If not specified, all non-archived repositories
    starting with "Moko" will be processed.

.PARAMETER Exclude
    Repositories to exclude from the update process.

.PARAMETER Branch
    Branch name for changes. Default: chore/sync-mokostandards-updates

.PARAMETER CommitMessage
    Commit message for changes. Default: "chore: sync workflows, scripts, and configurations from MokoStandards"

.PARAMETER PrTitle
    Pull request title. Default: "chore: Sync MokoStandards workflows and configurations"

.PARAMETER PrBody
    Pull request body/description.

.PARAMETER SourceDir
    Source directory containing files to sync. Default: current directory

.PARAMETER TempDir
    Temporary directory for cloning repositories. Default: $env:TEMP\bulk-update-repos

.PARAMETER DryRun
    Show what would be done without making changes.

.PARAMETER Force
    Skip confirmation prompt (use for automation).

.EXAMPLE
    Update-BulkRepositories.ps1 -DryRun
    Show what would be done for all repositories

.EXAMPLE
    Update-BulkRepositories.ps1 -Repositories "MokoModule1","MokoModule2" -Force
    Update specific repositories without confirmation

.EXAMPLE
    Update-BulkRepositories.ps1 -Exclude "MokoStandards","MokoTemplate" -DryRun
    Update all repositories except excluded ones (dry run)

.NOTES
    Requires:
    - PowerShell 7.0 or later
    - GitHub CLI (gh) installed and authenticated
    - Python 3.x for platform detection script
    - Git command line tools
#>

[CmdletBinding(SupportsShouldProcess, ConfirmImpact = 'High')]
param(
    [Parameter(Position = 0)]
    [string]$Organization = "mokoconsulting-tech",
    
    [Parameter(Position = 1)]
    [string[]]$Repositories,
    
    [Parameter()]
    [string[]]$Exclude = @(),
    
    [Parameter()]
    [string]$Branch = "chore/sync-mokostandards-updates",
    
    [Parameter()]
    [string]$CommitMessage = "chore: sync workflows, scripts, and configurations from MokoStandards",
    
    [Parameter()]
    [string]$PrTitle = "chore: Sync MokoStandards workflows and configurations",
    
    [Parameter()]
    [string]$PrBody = @"
This PR syncs workflows, scripts, and configurations from the MokoStandards repository.

Updated files:
- GitHub workflows (CI, build, release, etc.)
- Dependabot configuration
- Maintenance scripts
- Platform-specific configurations

Files are synced based on detected platform type (generic/dolibarr/joomla).

Please review and merge if appropriate for this repository.
"@,
    
    [Parameter()]
    [string]$SourceDir = (Get-Location).Path,
    
    [Parameter()]
    [string]$TempDir = (Join-Path $env:TEMP "bulk-update-repos"),
    
    [Parameter()]
    [switch]$DryRun,
    
    [Parameter()]
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

#region Configuration

# File sync configuration - mirrors Python FileSyncConfig class
$script:FileSyncConfig = @{
    CoreConfigs = @{
        ".github/dependabot.yml" = ".github/dependabot.yml"
        ".github/copilot.yml" = ".github/copilot.yml"
    }
    
    WorkflowTemplates = @{
        universal = @{
            "templates/workflows/build.yml.template" = ".github/workflows/build.yml"
            "templates/workflows/unified-ci.yml.template" = ".github/workflows/ci.yml"
        }
        generic = @{
            "templates/workflows/generic/code-quality.yml" = ".github/workflows/code-quality.yml"
            "templates/workflows/generic/codeql-analysis.yml" = ".github/workflows/codeql-analysis.yml"
            "templates/workflows/generic/repo-health.yml" = ".github/workflows/repo-health.yml"
        }
        dolibarr = @{
            "templates/workflows/dolibarr/release.yml.template" = ".github/workflows/release.yml"
            "templates/workflows/dolibarr/sync-changelogs.yml.template" = ".github/workflows/sync-changelogs.yml"
        }
        joomla = @{
            "templates/workflows/joomla/release.yml.template" = ".github/workflows/release.yml"
            "templates/workflows/joomla/repo_health.yml.template" = ".github/workflows/repo-health.yml"
        }
    }
    
    ReusableWorkflows = @{
        "templates/workflows/reusable-build.yml.template" = ".github/workflows/reusable-build.yml"
        "templates/workflows/reusable-ci-validation.yml" = ".github/workflows/reusable-ci-validation.yml"
        "templates/workflows/reusable-release.yml.template" = ".github/workflows/reusable-release.yml"
        "templates/workflows/reusable-php-quality.yml" = ".github/workflows/reusable-php-quality.yml"
        "templates/workflows/reusable-platform-testing.yml" = ".github/workflows/reusable-platform-testing.yml"
        "templates/workflows/reusable-project-detector.yml" = ".github/workflows/reusable-project-detector.yml"
        "templates/workflows/reusable-deploy.yml" = ".github/workflows/reusable-deploy.yml"
        "templates/workflows/reusable-script-executor.yml" = ".github/workflows/reusable-script-executor.yml"
    }
    
    SharedAutomation = @{
        ".github/workflows/enterprise-firewall-setup.yml" = ".github/workflows/enterprise-firewall-setup.yml"
    }
}

# Scripts to sync
$script:DefaultScriptsToSync = @(
    "scripts/maintenance/validate_file_headers.py"
    "scripts/maintenance/update_changelog.py"
    "scripts/maintenance/release_version.py"
    "scripts/validate/validate_codeql_config.py"
    "scripts/validate/auto_detect_platform.py"
    "scripts/validate/validate_structure_v2.py"
    "scripts/release/deploy_to_dev.py"
    "scripts/definitions/crm-module.xml"
    "scripts/definitions/default-repository.xml"
    "scripts/definitions/waas-component.xml"
)

#endregion Configuration

#region Helper Functions

function Invoke-CommandSafe {
    <#
    .SYNOPSIS
        Execute a command safely and return result object
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Command,
        
        [Parameter()]
        [string[]]$Arguments = @(),
        
        [Parameter()]
        [string]$WorkingDirectory
    )
    
    try {
        $processInfo = @{
            FilePath = $Command
            ArgumentList = $Arguments
            NoNewWindow = $true
            Wait = $true
            PassThru = $true
            RedirectStandardOutput = $true
            RedirectStandardError = $true
        }
        
        if ($WorkingDirectory) {
            $processInfo.WorkingDirectory = $WorkingDirectory
        }
        
        $process = Start-Process @processInfo
        
        $stdout = $process.StandardOutput.ReadToEnd()
        $stderr = $process.StandardError.ReadToEnd()
        
        return [PSCustomObject]@{
            Success = ($process.ExitCode -eq 0)
            ExitCode = $process.ExitCode
            StdOut = $stdout.Trim()
            StdErr = $stderr.Trim()
        }
    }
    catch {
        return [PSCustomObject]@{
            Success = $false
            ExitCode = -1
            StdOut = ""
            StdErr = $_.Exception.Message
        }
    }
}

function Get-OrganizationRepositories {
    <#
    .SYNOPSIS
        Get list of repositories in the organization starting with 'Moko'
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Organization,
        
        [Parameter()]
        [bool]$ExcludeArchived = $true,
        
        [Parameter()]
        [bool]$IncludeTemplates = $true
    )
    
    Write-Verbose "Fetching repositories from $Organization..."
    
    $result = Invoke-CommandSafe -Command "gh" -Arguments @(
        "repo", "list", $Organization,
        "--json", "name,isArchived,isTemplate",
        "--limit", "1000"
    )
    
    if (-not $result.Success) {
        Write-Error "Failed to fetch repositories: $($result.StdErr)"
        return @()
    }
    
    try {
        $repos = $result.StdOut | ConvertFrom-Json
        
        if ($ExcludeArchived) {
            $repos = $repos | Where-Object { -not $_.isArchived }
        }
        
        if (-not $IncludeTemplates) {
            $repos = $repos | Where-Object { -not $_.isTemplate }
        }
        
        # Filter to only repositories beginning with "Moko"
        $repoNames = $repos | Where-Object { $_.name -like "Moko*" } | Select-Object -ExpandProperty name
        
        Write-Verbose "Found $($repoNames.Count) repositories"
        return $repoNames
    }
    catch {
        Write-Error "Failed to parse repository list: $_"
        return @()
    }
}

function Invoke-PlatformDetection {
    <#
    .SYNOPSIS
        Detect the platform type of a repository
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$RepositoryPath,
        
        [Parameter(Mandatory)]
        [string]$SourceDir
    )
    
    $scriptPath = Join-Path $SourceDir "scripts/validate/auto_detect_platform.py"
    
    if (-not (Test-Path $scriptPath)) {
        Write-Warning "Platform detection script not found at $scriptPath"
        return $null
    }
    
    try {
        $result = Invoke-CommandSafe -Command "python3" -Arguments @(
            $scriptPath,
            "--repo-path", $RepositoryPath,
            "--json"
        )
        
        if ($result.Success -and $result.StdOut) {
            try {
                $detection = $result.StdOut | ConvertFrom-Json
                return $detection.platform_type ?? "generic"
            }
            catch {
                Write-Warning "Failed to parse platform detection output"
                return $null
            }
        }
        else {
            Write-Warning "Platform detection failed: $($result.StdErr)"
            return $null
        }
    }
    catch {
        Write-Warning "Platform detection error: $_"
        return $null
    }
}

function Get-FilesToSync {
    <#
    .SYNOPSIS
        Get the list of files to sync based on platform type
    #>
    [CmdletBinding()]
    param(
        [Parameter()]
        [ValidateSet('generic', 'dolibarr', 'joomla')]
        [string]$Platform = 'generic'
    )
    
    $files = @{}
    
    # Add core configs
    foreach ($kvp in $script:FileSyncConfig.CoreConfigs.GetEnumerator()) {
        $files[$kvp.Key] = $kvp.Value
    }
    
    # Add universal workflows
    foreach ($kvp in $script:FileSyncConfig.WorkflowTemplates.universal.GetEnumerator()) {
        $files[$kvp.Key] = $kvp.Value
    }
    
    # Add platform-specific workflows
    if ($script:FileSyncConfig.WorkflowTemplates.ContainsKey($Platform)) {
        foreach ($kvp in $script:FileSyncConfig.WorkflowTemplates[$Platform].GetEnumerator()) {
            $files[$kvp.Key] = $kvp.Value
        }
    }
    else {
        # Default to generic
        foreach ($kvp in $script:FileSyncConfig.WorkflowTemplates.generic.GetEnumerator()) {
            $files[$kvp.Key] = $kvp.Value
        }
    }
    
    # Add reusable workflows
    foreach ($kvp in $script:FileSyncConfig.ReusableWorkflows.GetEnumerator()) {
        $files[$kvp.Key] = $kvp.Value
    }
    
    # Add shared automation
    foreach ($kvp in $script:FileSyncConfig.SharedAutomation.GetEnumerator()) {
        $files[$kvp.Key] = $kvp.Value
    }
    
    return $files
}

function Test-SourceFiles {
    <#
    .SYNOPSIS
        Validate that source files exist
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [hashtable]$FilesToSync,
        
        [Parameter(Mandatory)]
        [string]$SourceDir
    )
    
    $existing = @()
    $missing = @()
    
    foreach ($sourceRel in $FilesToSync.Keys) {
        $sourcePath = Join-Path $SourceDir $sourceRel
        if (Test-Path $sourcePath) {
            $existing += $sourceRel
        }
        else {
            $missing += $sourceRel
        }
    }
    
    return @{
        Existing = $existing
        Missing = $missing
    }
}

function Copy-FileWithTracking {
    <#
    .SYNOPSIS
        Copy a file and track if it was created or overwritten
    #>
    [CmdletBinding(SupportsShouldProcess)]
    param(
        [Parameter(Mandatory)]
        [string]$SourceFile,
        
        [Parameter(Mandatory)]
        [string]$DestinationDir,
        
        [Parameter(Mandatory)]
        [string]$DestinationPath
    )
    
    if (-not (Test-Path $SourceFile)) {
        Write-Warning "Source file does not exist: $SourceFile"
        return @{ Success = $false; Action = "missing" }
    }
    
    $destFull = Join-Path $DestinationDir $DestinationPath
    $destDir = Split-Path $destFull -Parent
    
    # Create directory if needed
    if (-not (Test-Path $destDir)) {
        $null = New-Item -Path $destDir -ItemType Directory -Force
    }
    
    $action = if (Test-Path $destFull) { "overwritten" } else { "created" }
    
    try {
        if ($PSCmdlet.ShouldProcess($destFull, "Copy file")) {
            Copy-Item -Path $SourceFile -Destination $destFull -Force
        }
        return @{ Success = $true; Action = $action }
    }
    catch {
        Write-Error "Failed to copy $SourceFile to $destFull : $_"
        return @{ Success = $false; Action = "error" }
    }
}

function Invoke-RepositoryClone {
    <#
    .SYNOPSIS
        Clone a repository to a temporary directory
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Organization,
        
        [Parameter(Mandatory)]
        [string]$Repository,
        
        [Parameter(Mandatory)]
        [string]$TargetDir
    )
    
    $result = Invoke-CommandSafe -Command "gh" -Arguments @(
        "repo", "clone", "$Organization/$Repository", $TargetDir
    )
    
    if (-not $result.Success) {
        Write-Error "Failed to clone ${Repository}: $($result.StdErr)"
        return $false
    }
    
    # Configure git credential helper
    $null = Invoke-CommandSafe -Command "git" -Arguments @(
        "config", "--local", "credential.helper", ""
    ) -WorkingDirectory $TargetDir
    
    $null = Invoke-CommandSafe -Command "git" -Arguments @(
        "config", "--local", "credential.helper", "!gh auth git-credential"
    ) -WorkingDirectory $TargetDir
    
    return $true
}

function New-GitBranch {
    <#
    .SYNOPSIS
        Create and checkout a branch
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$RepositoryPath,
        
        [Parameter(Mandatory)]
        [string]$BranchName
    )
    
    # Check if branch exists
    $checkResult = Invoke-CommandSafe -Command "git" -Arguments @(
        "rev-parse", "--verify", $BranchName
    ) -WorkingDirectory $RepositoryPath
    
    if ($checkResult.Success) {
        # Branch exists, checkout
        $result = Invoke-CommandSafe -Command "git" -Arguments @(
            "checkout", $BranchName
        ) -WorkingDirectory $RepositoryPath
    }
    else {
        # Create new branch
        $result = Invoke-CommandSafe -Command "git" -Arguments @(
            "checkout", "-b", $BranchName
        ) -WorkingDirectory $RepositoryPath
    }
    
    if (-not $result.Success) {
        Write-Error "Failed to create/checkout branch: $($result.StdErr)"
        return $false
    }
    
    return $true
}

function Invoke-GitCommit {
    <#
    .SYNOPSIS
        Commit changes in repository
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$RepositoryPath,
        
        [Parameter(Mandatory)]
        [string]$Message
    )
    
    # Add all changes
    $result = Invoke-CommandSafe -Command "git" -Arguments @(
        "add", "."
    ) -WorkingDirectory $RepositoryPath
    
    if (-not $result.Success) {
        Write-Error "Failed to add files: $($result.StdErr)"
        return $false
    }
    
    # Check if there are changes to commit
    $diffResult = Invoke-CommandSafe -Command "git" -Arguments @(
        "diff", "--cached", "--quiet"
    ) -WorkingDirectory $RepositoryPath
    
    if ($diffResult.Success) {
        Write-Verbose "No changes to commit"
        return $true
    }
    
    # Commit changes
    $result = Invoke-CommandSafe -Command "git" -Arguments @(
        "commit", "-m", $Message
    ) -WorkingDirectory $RepositoryPath
    
    if (-not $result.Success) {
        Write-Error "Failed to commit changes: $($result.StdErr)"
        return $false
    }
    
    return $true
}

function Invoke-GitPush {
    <#
    .SYNOPSIS
        Push branch to remote
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$RepositoryPath,
        
        [Parameter(Mandatory)]
        [string]$BranchName
    )
    
    $result = Invoke-CommandSafe -Command "git" -Arguments @(
        "push", "-u", "origin", $BranchName
    ) -WorkingDirectory $RepositoryPath
    
    if (-not $result.Success) {
        Write-Error "Failed to push branch: $($result.StdErr)"
        return $false
    }
    
    return $true
}

function New-PullRequest {
    <#
    .SYNOPSIS
        Create a pull request
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Organization,
        
        [Parameter(Mandatory)]
        [string]$Repository,
        
        [Parameter(Mandatory)]
        [string]$BranchName,
        
        [Parameter(Mandatory)]
        [string]$Title,
        
        [Parameter(Mandatory)]
        [string]$Body
    )
    
    $result = Invoke-CommandSafe -Command "gh" -Arguments @(
        "pr", "create",
        "--repo", "$Organization/$Repository",
        "--head", $BranchName,
        "--title", $Title,
        "--body", $Body
    )
    
    if (-not $result.Success) {
        if ($result.StdErr -like "*already exists*") {
            Write-Verbose "Pull request already exists for branch $BranchName"
            return $true
        }
        Write-Error "Failed to create pull request: $($result.StdErr)"
        return $false
    }
    
    Write-Verbose "Created pull request: $($result.StdOut)"
    return $true
}

function Update-Repository {
    <#
    .SYNOPSIS
        Update a single repository with files and scripts
    #>
    [CmdletBinding(SupportsShouldProcess)]
    param(
        [Parameter(Mandatory)]
        [string]$Organization,
        
        [Parameter(Mandatory)]
        [string]$Repository,
        
        [Parameter(Mandatory)]
        [string]$SourceDir,
        
        [Parameter(Mandatory)]
        [string]$BranchName,
        
        [Parameter(Mandatory)]
        [string]$CommitMessage,
        
        [Parameter(Mandatory)]
        [string]$PrTitle,
        
        [Parameter(Mandatory)]
        [string]$PrBody,
        
        [Parameter(Mandatory)]
        [string]$TempDir,
        
        [Parameter()]
        [switch]$DryRun
    )
    
    $stats = @{
        FilesCreated = 0
        FilesOverwritten = 0
        FilesCopied = @()
        FilesOverwrittenList = @()
        Platform = "unknown"
    }
    
    $prefix = if ($DryRun) { "[DRY RUN] " } else { "" }
    Write-Host "`n${prefix}Processing repository: $Organization/$Repository" -ForegroundColor Cyan
    
    $repoDir = Join-Path $TempDir $Repository
    
    if ($DryRun) {
        Write-Host "  Would clone and sync repository" -ForegroundColor Gray
        return @{ Success = $true; Stats = $stats }
    }
    
    # Clone repository
    Write-Host "  Cloning repository..." -ForegroundColor Gray
    if (-not (Invoke-RepositoryClone -Organization $Organization -Repository $Repository -TargetDir $repoDir)) {
        return @{ Success = $false; Stats = $stats }
    }
    
    # Detect platform
    Write-Host "  Detecting platform type..." -ForegroundColor Gray
    $platformType = Invoke-PlatformDetection -RepositoryPath $repoDir -SourceDir $SourceDir
    
    if ($platformType) {
        Write-Host "    Detected platform: $platformType" -ForegroundColor Green
        $stats.Platform = $platformType
    }
    else {
        Write-Host "    Platform detection failed, using generic defaults" -ForegroundColor Yellow
        $platformType = "generic"
        $stats.Platform = "generic"
    }
    
    # Get files to sync
    $filesToSync = Get-FilesToSync -Platform $platformType
    
    # Validate source files
    $validation = Test-SourceFiles -FilesToSync $filesToSync -SourceDir $SourceDir
    
    if ($validation.Missing.Count -gt 0) {
        Write-Warning "  $($validation.Missing.Count) source files missing:"
        $validation.Missing | Select-Object -First 5 | ForEach-Object {
            Write-Warning "    - $_"
        }
        if ($validation.Missing.Count -gt 5) {
            Write-Warning "    ... and $($validation.Missing.Count - 5) more"
        }
        
        # Filter out missing files
        $existingFiles = @{}
        foreach ($key in $filesToSync.Keys) {
            if ($validation.Existing -contains $key) {
                $existingFiles[$key] = $filesToSync[$key]
            }
        }
        $filesToSync = $existingFiles
    }
    
    # Create branch
    Write-Host "  Creating branch: $BranchName" -ForegroundColor Gray
    if (-not (New-GitBranch -RepositoryPath $repoDir -BranchName $BranchName)) {
        return @{ Success = $false; Stats = $stats }
    }
    
    # Copy workflow files
    foreach ($kvp in $filesToSync.GetEnumerator()) {
        $sourceFile = Join-Path $SourceDir $kvp.Key
        $copyResult = Copy-FileWithTracking -SourceFile $sourceFile -DestinationDir $repoDir -DestinationPath $kvp.Value
        
        if ($copyResult.Success) {
            if ($copyResult.Action -eq "created") {
                $stats.FilesCreated++
                $stats.FilesCopied += $kvp.Value
                Write-Host "    ✓ Created: $($kvp.Value)" -ForegroundColor Green
            }
            elseif ($copyResult.Action -eq "overwritten") {
                $stats.FilesOverwritten++
                $stats.FilesOverwrittenList += $kvp.Value
                Write-Host "    ↻ Updated: $($kvp.Value)" -ForegroundColor Yellow
            }
        }
    }
    
    # Copy scripts
    foreach ($script in $script:DefaultScriptsToSync) {
        $sourceFile = Join-Path $SourceDir $script
        $copyResult = Copy-FileWithTracking -SourceFile $sourceFile -DestinationDir $repoDir -DestinationPath $script
        
        if ($copyResult.Success) {
            if ($copyResult.Action -eq "created") {
                $stats.FilesCreated++
                $stats.FilesCopied += $script
                Write-Host "    ✓ Created: $script" -ForegroundColor Green
            }
            elseif ($copyResult.Action -eq "overwritten") {
                $stats.FilesOverwritten++
                $stats.FilesOverwrittenList += $script
                Write-Host "    ↻ Updated: $script" -ForegroundColor Yellow
            }
        }
    }
    
    $totalFiles = $stats.FilesCreated + $stats.FilesOverwritten
    
    if ($totalFiles -eq 0) {
        Write-Host "  No files were copied, skipping commit" -ForegroundColor Gray
        return @{ Success = $true; Stats = $stats }
    }
    
    # Commit changes
    Write-Host "  Committing changes..." -ForegroundColor Gray
    if (-not (Invoke-GitCommit -RepositoryPath $repoDir -Message $CommitMessage)) {
        return @{ Success = $false; Stats = $stats }
    }
    
    # Push branch
    Write-Host "  Pushing branch..." -ForegroundColor Gray
    if (-not (Invoke-GitPush -RepositoryPath $repoDir -BranchName $BranchName)) {
        return @{ Success = $false; Stats = $stats }
    }
    
    # Create pull request
    Write-Host "  Creating pull request..." -ForegroundColor Gray
    if (-not (New-PullRequest -Organization $Organization -Repository $Repository -BranchName $BranchName -Title $PrTitle -Body $PrBody)) {
        return @{ Success = $false; Stats = $stats }
    }
    
    Write-Host "  ✓ Successfully updated $Organization/$Repository" -ForegroundColor Green
    Write-Host "    - Platform: $($stats.Platform)" -ForegroundColor Gray
    Write-Host "    - Created: $($stats.FilesCreated) files" -ForegroundColor Gray
    Write-Host "    - Updated: $($stats.FilesOverwritten) files" -ForegroundColor Gray
    
    return @{ Success = $true; Stats = $stats }
}

#endregion Helper Functions

#region Main Execution

# Check prerequisites
Write-Verbose "Checking prerequisites..."

# Check for gh CLI
$ghVersion = Invoke-CommandSafe -Command "gh" -Arguments @("--version")
if (-not $ghVersion.Success) {
    Write-Error "GitHub CLI (gh) is not installed or not in PATH. Install from: https://cli.github.com/"
    exit 1
}

# Check gh authentication
$ghAuth = Invoke-CommandSafe -Command "gh" -Arguments @("auth", "status")
if (-not $ghAuth.Success) {
    Write-Error "Not authenticated with GitHub CLI. Run: gh auth login"
    exit 1
}

# Get repositories to update
if ($Repositories) {
    $reposToUpdate = $Repositories
}
else {
    Write-Host "Fetching repositories from $Organization..." -ForegroundColor Cyan
    $reposToUpdate = Get-OrganizationRepositories -Organization $Organization
    
    if ($reposToUpdate.Count -eq 0) {
        Write-Error "No repositories found or error fetching repositories"
        exit 1
    }
}

# Apply exclusions
if ($Exclude.Count -gt 0) {
    $reposToUpdate = $reposToUpdate | Where-Object { $_ -notin $Exclude }
}

# Display repositories
$prefix = if ($DryRun) { "DRY RUN: " } else { "" }
Write-Host "`n${prefix}Will update $($reposToUpdate.Count) repositories:" -ForegroundColor Cyan
foreach ($repo in $reposToUpdate) {
    Write-Host "  - $repo" -ForegroundColor Gray
}

# Confirmation
if (-not $DryRun -and -not $Force -and -not $WhatIfPreference) {
    $response = Read-Host "`nContinue? (yes/no)"
    if ($response -notin @('yes', 'y')) {
        Write-Host "Aborted" -ForegroundColor Yellow
        exit 0
    }
}

# Create temp directory
if (-not $DryRun) {
    if (-not (Test-Path $TempDir)) {
        $null = New-Item -Path $TempDir -ItemType Directory -Force
    }
}

# Process repositories
$successCount = 0
$failedRepos = @()
$allStats = @{}
$totalCreated = 0
$totalOverwritten = 0

for ($i = 0; $i -lt $reposToUpdate.Count; $i++) {
    $repo = $reposToUpdate[$i]
    
    # Show progress
    $progressParams = @{
        Activity = "Updating Repositories"
        Status = "Processing $repo ($($i + 1)/$($reposToUpdate.Count))"
        PercentComplete = (($i + 1) / $reposToUpdate.Count) * 100
    }
    Write-Progress @progressParams
    
    try {
        $result = Update-Repository `
            -Organization $Organization `
            -Repository $repo `
            -SourceDir $SourceDir `
            -BranchName $Branch `
            -CommitMessage $CommitMessage `
            -PrTitle $PrTitle `
            -PrBody $PrBody `
            -TempDir $TempDir `
            -DryRun:$DryRun
        
        if ($result.Success) {
            $successCount++
            $allStats[$repo] = $result.Stats
            $totalCreated += $result.Stats.FilesCreated
            $totalOverwritten += $result.Stats.FilesOverwritten
        }
        else {
            $failedRepos += $repo
        }
    }
    catch {
        Write-Error "Error updating ${repo}: $_"
        $failedRepos += $repo
    }
}

Write-Progress -Activity "Updating Repositories" -Completed

# Display summary
$separator = "=" * 70
Write-Host "`n$separator" -ForegroundColor Cyan
Write-Host "$(if ($DryRun) { 'DRY RUN ' })SUMMARY" -ForegroundColor Cyan
Write-Host $separator -ForegroundColor Cyan
Write-Host "Successfully $(if ($DryRun) { 'would update' } else { 'updated' }): $successCount/$($reposToUpdate.Count) repositories" -ForegroundColor Green

Write-Host "`nFile Operations:" -ForegroundColor White
Write-Host "  - Total files created: $totalCreated" -ForegroundColor Gray
Write-Host "  - Total files updated: $totalOverwritten" -ForegroundColor Gray
Write-Host "  - Total operations: $($totalCreated + $totalOverwritten)" -ForegroundColor Gray

if ($allStats.Count -gt 0) {
    Write-Host "`nPer-Repository Details:" -ForegroundColor White
    foreach ($kvp in $allStats.GetEnumerator()) {
        $repo = $kvp.Key
        $stats = $kvp.Value
        
        if ($stats.FilesCreated -gt 0 -or $stats.FilesOverwritten -gt 0) {
            Write-Host "  ${repo}:" -ForegroundColor Cyan
            Write-Host "    Platform: $($stats.Platform)" -ForegroundColor Gray
            Write-Host "    Created: $($stats.FilesCreated), Updated: $($stats.FilesOverwritten)" -ForegroundColor Gray
        }
    }
}

if ($failedRepos.Count -gt 0) {
    Write-Host "`nFailed Repositories ($($failedRepos.Count)):" -ForegroundColor Red
    foreach ($repo in $failedRepos) {
        Write-Host "  - $repo" -ForegroundColor Red
    }
    Write-Host $separator -ForegroundColor Cyan
    exit 1
}

Write-Host "`n$separator" -ForegroundColor Cyan
exit 0

#endregion Main Execution
