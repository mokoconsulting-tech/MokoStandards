# Script Wrappers

This directory contains shell and PowerShell wrappers for all Python scripts in the MokoStandards repository.

## Purpose

Wrappers provide a convenient way to run Python scripts from different environments:
- **Bash wrappers** (`.sh`): For Linux, macOS, and Git Bash on Windows
- **PowerShell wrappers** (`.ps1`): For Windows PowerShell and PowerShell Core (cross-platform)

## Benefits

1. **Simplified execution**: No need to remember Python interpreter commands
2. **Automatic logging**: All output is captured to `logs/` directory
3. **Error handling**: Proper exit codes and error messages
4. **Path resolution**: Automatically finds script locations relative to repository root
5. **Cross-platform**: Works on any platform with appropriate shell

## Directory Structure

```
wrappers/
├── bash/           - Bash/shell wrappers (.sh files)
├── powershell/     - PowerShell wrappers (.ps1 files)
└── README.md       - This file
```

## Usage

### Bash Wrappers (Linux/macOS/Git Bash)

```bash
# Make wrapper executable (first time only)
chmod +x scripts/wrappers/bash/bulk_update_repos.sh

# Run the wrapper
./scripts/wrappers/bash/bulk_update_repos.sh --dry-run

# Or from anywhere in the repository
scripts/wrappers/bash/validate_repo_health.sh
```

### PowerShell Wrappers (Windows/PowerShell Core)

```powershell
# Run the wrapper
.\scripts\wrappers\powershell\bulk_update_repos.ps1 -DryRun

# Or from anywhere in the repository
scripts\wrappers\powershell\validate_repo_health.ps1
```

## Features

### Automatic Logging

All wrapper executions are logged to the `logs/` directory:
- Logs are organized by category (automation, validation, maintenance, etc.)
- Log files include timestamps: `{script_name}_{timestamp}.log`
- Both stdout and stderr are captured

Example log location:
```
logs/automation/bulk_update_repos_20260128_110830.log
```

### Error Handling

Wrappers properly handle errors:
- Exit with the same code as the Python script
- Display colorized error messages
- Point to log files for debugging

### Requirements Check

Wrappers automatically check for:
- Python 3 installation
- Script file existence
- Repository structure

## Regenerating Wrappers

If Python scripts are added, removed, or moved, regenerate wrappers:

```bash
# Preview changes
python3 scripts/automation/generate_wrappers.py --dry-run

# Generate all wrappers
python3 scripts/automation/generate_wrappers.py

# Generate only bash wrappers
python3 scripts/automation/generate_wrappers.py --bash-only

# Generate only PowerShell wrappers
python3 scripts/automation/generate_wrappers.py --powershell-only
```

## Wrapper Coverage

| Category | Python Scripts | Wrappers |
|----------|---------------|----------|
| Automation | 10 | ✅ 10 |
| Validation | 16 | ✅ 16 |
| Maintenance | 4 | ✅ 4 |
| Analysis | 4 | ✅ 4 |
| Release | 4 | ✅ 4 |
| Build | 1 | ✅ 1 |
| Docs | 1 | ✅ 1 |
| Tests | 14 | ✅ 14 |
| **Total** | **54** | **✅ 54** |

## Examples

### Validate Repository Health

```bash
# Bash
./scripts/wrappers/bash/validate_repo_health.sh

# PowerShell
.\scripts\wrappers\powershell\validate_repo_health.ps1
```

### Bulk Update Repositories (Dry Run)

```bash
# Bash
./scripts/wrappers/bash/bulk_update_repos.sh --dry-run

# PowerShell
.\scripts\wrappers\powershell\bulk_update_repos.ps1 --dry-run
```

### Distribute Files

```bash
# Bash
./scripts/wrappers/bash/file-distributor.sh --source myfile.txt --root /path/to/repos

# PowerShell
.\scripts\wrappers\powershell\file-distributor.ps1 -SourceFile myfile.txt -RootDirectory C:\repos
```

## Troubleshooting

### Python Not Found

If you see "Python is not installed or not in PATH":
1. Install Python 3.7 or later from https://www.python.org/
2. Ensure Python is in your PATH
3. On Windows, you may need to restart your terminal

### Script Not Found

If you see "Python script not found":
1. Ensure you're running from within the repository
2. Check that the Python script exists at the expected location
3. Regenerate wrappers if scripts have moved

### Permission Denied (Linux/macOS)

If you see "Permission denied":
```bash
chmod +x scripts/wrappers/bash/*.sh
```

### Execution Policy (Windows PowerShell)

If you see "execution of scripts is disabled":
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## See Also

- [Scripts README](../README.md) - Overview of all scripts
- [Python Scripts Documentation](../../docs/scripts/)
- [Logs Directory](../../logs/README.md) - Log file structure and retention
