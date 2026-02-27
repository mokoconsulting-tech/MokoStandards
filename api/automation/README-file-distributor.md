# File Distributor v03.00.00

Enterprise file distribution utility with GUI, depth control, and comprehensive audit logging.

## Features

- **GUI-based** file and directory selection
- **Configurable recursion depth** (0 to N levels, or -1 for full recursion)
- **Per-folder confirmation dialogs** with Yes to All option
- **Dry run mode** for safe testing
- **Overwrite control** for existing files
- **Structured audit logging** (CSV and JSON)
- **Progress reporting** with visual feedback
- **Configuration file support** (.json)
- **SHA256 hash tracking** for file integrity
- **Hidden folder inclusion** control
- **Comprehensive error handling** with try-catch blocks
- **Verbose and Debug output** support
- **PowerShell 5.1 and 7+ compatible**

## Requirements

- PowerShell 5.1 or later
- Windows (for WinForms GUI)
- No additional modules required

## Usage

### Interactive Mode (GUI)

```powershell
.\file-distributor.ps1
```

Launches the GUI for interactive file distribution with dialogs for file selection, directory selection, and configuration.

### Command-Line Mode

```powershell
.\file-distributor.ps1 -SourceFile "C:\template.txt" -RootDirectory "C:\Projects" -Depth 1 -DryRun
```

Distributes template.txt to C:\Projects and immediate subdirectories in dry run mode.

### With Configuration File

```powershell
.\file-distributor.ps1 -ConfigFile ".\config.json" -Verbose
```

Uses settings from config.json with verbose output.

### WhatIf Mode

```powershell
.\file-distributor.ps1 -SourceFile ".\LICENSE" -RootDirectory "C:\Repos" -Depth -1 -Overwrite -WhatIf
```

Shows what would happen when distributing LICENSE to all subdirectories with overwrite.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `SourceFile` | String | Path to the file to distribute |
| `RootDirectory` | String | Root directory for distribution |
| `Depth` | Int | Recursion depth: 0=root only, 1=root+1 level, -1=full recursive |
| `DryRun` | Switch | Simulate without making changes |
| `Overwrite` | Switch | Overwrite existing files |
| `ConfirmEach` | Switch | Confirm each folder operation |
| `IncludeHidden` | Switch | Include hidden folders |
| `LogDirectory` | String | Directory for audit logs |
| `ConfigFile` | String | Path to JSON configuration file |
| `UseGUI` | Switch | Force GUI mode |
| `WhatIf` | Switch | Show what would happen without executing |
| `Verbose` | Switch | Display detailed progress information |

## Depth Modes

- **0** : Root directory only
- **1** : Root + immediate subdirectories
- **N** : Root + N levels deep
- **-1** : Full recursive (all subdirectories)

## Configuration File

Create a JSON file with your preferred settings:

```json
{
  "SourceFile": "C:\\path\\to\\source\\file.txt",
  "RootDirectory": "C:\\path\\to\\root",
  "Depth": 1,
  "DryRun": true,
  "Overwrite": false,
  "ConfirmEach": false,
  "IncludeHidden": true,
  "LogDirectory": "C:\\path\\to\\logs"
}
```

## Audit Logging

The script generates comprehensive audit logs in two formats:

- **CSV**: For spreadsheet analysis
- **JSON**: For programmatic processing

Logs include:
- Run ID (GUID)
- Timestamps
- Source and target paths
- Actions planned and taken
- File hashes (SHA256)
- Success/error status
- User decisions

Default log location: `~/Documents/FileDistributorLogs/`

## Examples

### Example 1: GUI Mode
```powershell
.\file-distributor.ps1
```

### Example 2: Dry Run
```powershell
.\file-distributor.ps1 -SourceFile "template.txt" -RootDirectory "C:\Projects" -Depth 2 -DryRun
```

### Example 3: Full Recursive with Overwrite
```powershell
.\file-distributor.ps1 -SourceFile "LICENSE" -RootDirectory "C:\Repos" -Depth -1 -Overwrite
```

### Example 4: With Per-Folder Confirmation
```powershell
.\file-distributor.ps1 -SourceFile "config.json" -RootDirectory "C:\Apps" -Depth 1 -ConfirmEach
```

### Example 5: Using Config File
```powershell
.\file-distributor.ps1 -ConfigFile "my-settings.json" -Verbose
```

## Output

The script provides:
- Color-coded console output (Green=Success, Yellow=Skip, Red=Error, Magenta=DryRun)
- Progress bars for long operations
- Summary dialog (GUI mode)
- Detailed statistics
- Audit log file locations

## Error Handling

The script includes comprehensive error handling:
- Parameter validation
- Path existence checks
- Try-catch blocks for all operations
- Detailed error messages
- Graceful degradation

## Functions

The script is modularized into testable functions:

1. `Get-DistributorConfig` - Load JSON configuration
2. `Merge-Configuration` - Merge config with parameters
3. `Select-SourceFileGUI` - File selection dialog
4. `Select-RootDirectoryGUI` - Directory selection dialog
5. `Show-OptionsDialogGUI` - Main configuration dialog
6. `Show-FolderConfirmationGUI` - Per-folder confirmation
7. `Show-SummaryDialogGUI` - Results summary
8. `Get-DefaultLogDirectory` - Get/create log directory
9. `Get-FoldersByDepth` - Enumerate folders by depth
10. `Write-AuditLogs` - Write CSV and JSON logs
11. `Invoke-FileDistribution` - Main distribution function

## Version History

### v03.00.00 (Current)
- Complete rebuild with modern PowerShell standards
- Comprehensive comment-based help
- Parameter validation attributes
- Enhanced error handling (15 try-catch blocks)
- Progress reporting
- Verbose and Debug output support (35 statements)
- PowerShell 7+ compatibility
- Refactored into 11 unit-testable functions
- Improved GUI with modern styling
- JSON configuration file support
- No backward compatibility with v01.x

## Notes

- Requires Windows for GUI functionality
- WinForms dialogs are only available on Windows
- CLI mode can run on any PowerShell-supported platform (with appropriate file paths)
- Always test with `-DryRun` first
- Review audit logs for compliance

## Support

For issues, questions, or contributions, please refer to the MokoStandards repository.

## License

See LICENSE file in the repository root.
