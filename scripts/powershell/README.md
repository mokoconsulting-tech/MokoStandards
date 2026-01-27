# PowerShell Scripts - MokoStandards

**Version**: 1.0  
**Created**: 2026-01-19  
**Status**: Building PowerShell equivalents of all Python scripts

## Overview

This directory contains PowerShell (.ps1) versions of all MokoStandards Python scripts, providing Windows-native automation capabilities.

## Structure

```
scripts/powershell/
├── lib/                    # Core PowerShell modules
│   ├── Common.psm1        # Common utilities (clone of common.py)
│   ├── ConfigManager.psm1 # Configuration (clone of config_manager.py)
│   ├── GitHubClient.psm1  # GitHub API (clone of github_client.py)
│   └── ValidationFramework.psm1 # Validation (clone of validation_framework.py)
│
├── validate/              # Validation scripts
│   ├── Invoke-PlatformDetection.ps1 # Platform detection
│   ├── Test-RepositoryStructure.ps1 # Structure validation
│   └── Test-RepositoryHealth.ps1    # Health checks
│
├── automation/            # Automation scripts
│   ├── Update-BulkRepositories.ps1  # Bulk repo sync
│   ├── New-OrgProject.ps1           # Project creation
│   └── Sync-Changelog.ps1           # Changelog sync
│
├── release/               # Release management
│   ├── Deploy-ToDev.ps1   # Development deployment
│   └── New-Release.ps1    # Release creation
│
└── maintenance/           # Maintenance scripts
    ├── Update-Version.ps1  # Version management
    └── Update-Changelog.ps1 # Changelog updates
```

## Requirements

- **PowerShell 7+** recommended (cross-platform)
- **PowerShell 5.1** minimum (Windows only)
- **Git** for Windows
- **GitHub CLI** (`gh`) for GitHub operations

## Design Principles

1. **Cmdlet Naming**: Follow PowerShell verb-noun conventions
   - `Get-*`: Retrieve information
   - `Set-*`: Modify configuration
   - `New-*`: Create new items
   - `Test-*`: Validate/check
   - `Invoke-*`: Execute operations

2. **Parameter Validation**: Use PowerShell attributes
   - `[ValidateNotNullOrEmpty()]`
   - `[ValidateSet()]`
   - `[ValidateScript()]`

3. **Error Handling**: Proper try-catch-finally blocks

4. **Pipeline Support**: Accept pipeline input where appropriate

5. **Comment-Based Help**: All functions have `.SYNOPSIS`, `.DESCRIPTION`, `.PARAMETER`, `.EXAMPLE`

6. **Progress Reporting**: Use `Write-Progress` for long operations

7. **Verbose/Debug**: Support `-Verbose` and `-Debug` parameters

## Module vs Script

- **Modules (.psm1)**: Reusable functions, imported with `Import-Module`
- **Scripts (.ps1)**: Standalone executables with CLI interface

## Compatibility

All scripts support:
- PowerShell 7+ (Windows, Linux, macOS with limitations)
- PowerShell 5.1 (Windows only, legacy support)
- Both interactive and non-interactive modes

## Usage Examples

### Import Core Module
```powershell
Import-Module ./scripts/powershell/lib/Common.psm1
```

### Run Validation
```powershell
./scripts/powershell/validate/Invoke-PlatformDetection.ps1 -Path . -Verbose
```

### Bulk Repository Update
```powershell
./scripts/powershell/automation/Update-BulkRepositories.ps1 `
    -Organization "mokoconsulting-tech" `
    -DryRun `
    -Verbose
```

## Development

### Creating New PowerShell Scripts

1. **Start with comment-based help**:
```powershell
<#
.SYNOPSIS
    Brief description

.DESCRIPTION
    Detailed description

.PARAMETER ParameterName
    Parameter description

.EXAMPLE
    Example usage
#>
```

2. **Use proper error handling**:
```powershell
try {
    # Operation
} catch {
    Write-Error "Failed: $_"
    throw
}
```

3. **Add progress reporting**:
```powershell
Write-Progress -Activity "Processing" -Status "Item $i of $total" -PercentComplete (($i / $total) * 100)
```

4. **Support common parameters**:
```powershell
[CmdletBinding()]
param(
    [switch]$WhatIf,
    [switch]$Force
)
```

## Testing

Run tests with Pester:
```powershell
Invoke-Pester -Path ./scripts/powershell/tests/
```

## Status

**Current**: Building PowerShell equivalents
- [x] file-distributor.ps1 v02.00.00 (rebuilt)
- [ ] Common.psm1 (in progress)
- [ ] 42 more scripts to create

## References

- [PowerShell Best Practices](https://github.com/PoshCode/PowerShellPracticeAndStyle)
- [Approved Verbs](https://docs.microsoft.com/en-us/powershell/scripting/developer/cmdlet/approved-verbs-for-windows-powershell-commands)
- [Comment-Based Help](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_comment_based_help)

---

**Maintained by**: Moko Consulting  
**Questions**: hello@mokoconsulting.tech  
**Repository**: https://github.com/mokoconsulting-tech/MokoStandards
