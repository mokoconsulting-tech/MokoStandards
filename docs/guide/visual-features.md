[![MokoStandards](https://img.shields.io/badge/MokoStandards-03.02.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Visual Features Guide

This guide explains all visual output features available in MokoStandards scripts.

## Overview

MokoStandards provides rich visual output to improve user experience:
- **Color-coded messages** for quick visual scanning
- **Progress bars** for long-running operations  
- **Status icons** for clear feedback
- **Formatted tables** for data display
- **Box frames** for important messages
- **Spinners** for background operations

## Python Scripts - visual_helper Module

### Installation

The `visual_helper.py` module is located in `scripts/lib/` and is automatically available to all Python scripts.

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'lib'))
from visual_helper import *
```

### Status Messages

```python
from visual_helper import print_success, print_error, print_warning, print_info

print_success('Operation completed successfully!')
#  ✓ Operation completed successfully!

print_error('Failed to connect to database')
#  ✗ Failed to connect to database

print_warning('Configuration file not found, using defaults')
#  ⚠ Configuration file not found, using defaults

print_info('Processing 150 files...')
#  ℹ Processing 150 files...
```

### Headers

```python
from visual_helper import print_header

print_header('Repository Validator', 'Version 03.01.00')
```

Output:
```
╔══════════════════════════════════════════════════╗
║           Repository Validator                   ║
║            Version 03.01.00                      ║
╚══════════════════════════════════════════════════╝
```

### Progress Bars

```python
from visual_helper import ProgressBar

progress = ProgressBar(total=100, prefix='Processing files')

for i in range(100):
    # Do work
    progress.update(i + 1, suffix=f'file_{i}.txt')
    
progress.finish('All files processed')
```

Output:
```
Processing files: 50/100 50.0% [█████████████████████░░░░░░░░░░] ETA: 2.5s
✓ All files processed (took 5.23s)
```

### Spinners

```python
from visual_helper import Spinner

spinner = Spinner('Loading configuration')
spinner.start()

# Do long-running work
import time
time.sleep(3)

spinner.stop('Configuration loaded')
```

Output:
```
⠋ Loading configuration...
✓ Configuration loaded
```

### Message Boxes

```python
from visual_helper import print_box

print_box('This is an important informational message that users should read carefully.', 'info')
print_box('Operation completed successfully!', 'success')
print_box('Warning: This action cannot be undone.', 'warning')
print_box('Error: Connection failed.', 'error')
```

Output:
```
┌────────────────────────────────────────────────────┐
│ This is an important informational message that    │
│ users should read carefully.                       │
└────────────────────────────────────────────────────┘
```

### Tables

```python
from visual_helper import print_table

print_table(
    headers=['Script', 'Status', 'Duration', 'Files'],
    rows=[
        ['validate_structure.py', 'Pass', '1.2s', '150'],
        ['check_repo_health.py', 'Pass', '0.8s', '87'],
        ['security_scan.py', 'Warn', '2.1s', '3'],
    ],
    title='Validation Results',
    show_index=True
)
```

Output:
```
Validation Results
┌───┬───────────────────────┬────────┬──────────┬───────┐
│ # │ Script                │ Status │ Duration │ Files │
├───┼───────────────────────┼────────┼──────────┼───────┤
│ 1 │ validate_structure.py │ Pass   │ 1.2s     │ 150   │
│ 2 │ check_repo_health.py  │ Pass   │ 0.8s     │ 87    │
│ 3 │ security_scan.py      │ Warn   │ 2.1s     │ 3     │
└───┴───────────────────────┴────────┴──────────┴───────┘
```

### Summaries

```python
from visual_helper import print_summary

print_summary({
    'Total Files': 150,
    'Passed': 147,
    'Warnings': 3,
    'Errors': 0,
    'Duration': '2.5s',
    'Status': 'SUCCESS'
}, title='Execution Summary')
```

Output:
```
════════════════════════════════════════════════════════════
  Execution Summary
════════════════════════════════════════════════════════════
  Total Files:  150
  Passed:       147
  Warnings:     3
  Errors:       0
  Duration:     2.5s
  Status:       SUCCESS
════════════════════════════════════════════════════════════
```

### Confirmation Prompts

```python
from visual_helper import confirm

if confirm('Delete all temporary files?', default=False):
    print_success('Files deleted')
else:
    print_info('Operation cancelled')
```

Output:
```
? Delete all temporary files? [y/N]: y
✓ Files deleted
```

### Colors

```python
from visual_helper import colorize, Color

text = colorize('This is red text', Color.RED, bold=True)
print(text)

# Available colors:
# RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE
# BRIGHT_RED, BRIGHT_GREEN, BRIGHT_YELLOW, etc.
```

## PowerShell Scripts - VisualUtils Module

### Installation

```powershell
Import-Module "$PSScriptRoot/../lib/VisualUtils.psm1" -Force
```

### Status Messages

```powershell
Write-SuccessMessage 'Operation completed successfully!'
# ✓ Operation completed successfully!

Write-ErrorMessage 'Failed to connect to database'
# ✗ Failed to connect to database

Write-WarningMessage 'Configuration file not found'
# ⚠ Configuration file not found

Write-InfoMessage 'Processing 150 files...'
# ℹ Processing 150 files...
```

### Headers

```powershell
Write-Header -Title 'Repository Validator' -Subtitle 'Version 03.01.00'
```

### Progress Bars

```powershell
$total = 100
for ($i = 1; $i -le $total; $i++) {
    Write-ProgressBar -Current $i -Total $total -Activity 'Processing'
    Start-Sleep -Milliseconds 50
}
Write-Host ''  # New line after completion
Write-SuccessMessage 'Processing complete'
```

### Message Boxes

```powershell
Write-Box -Message 'Important information' -Type Info
Write-Box -Message 'Success!' -Type Success
Write-Box -Message 'Warning message' -Type Warning
Write-Box -Message 'Error occurred' -Type Error
```

### Tables

```powershell
$data = @(
    @{Script='validate_structure.py'; Status='Pass'; Files='150'},
    @{Script='check_repo_health.py'; Status='Pass'; Files='87'},
    @{Script='security_scan.py'; Status='Warn'; Files='3'}
)

Write-Table -Headers @('Script', 'Status', 'Files') -Rows $data -Title 'Results'
```

### Summaries

```powershell
$summary = @{
    'Total Files' = 150
    'Passed' = 147
    'Warnings' = 3
    'Errors' = 0
    'Duration' = '2.5s'
}

Write-Summary -Items $summary -Title 'Execution Summary'
```

### Confirmation Prompts

```powershell
if (Read-Confirmation -Message 'Delete temporary files?' -Default 'N') {
    Write-SuccessMessage 'Files deleted'
} else {
    Write-InfoMessage 'Operation cancelled'
}
```

## GUI Applications

### Windows PowerShell GUIs

MokoStandards provides GUI alternatives for Windows users:

**Available GUIs:**
- `Invoke-BulkUpdateGUI.ps1` - Bulk repository updates
- `Invoke-RepoHealthCheckGUI.ps1` - Repository health checks
- `Invoke-DemoDataLoaderGUI.ps1` - Demo data loading

**Launch:**
```powershell
.\scripts\run\Invoke-DemoDataLoaderGUI.ps1
```

**Features:**
- File/folder selection dialogs
- Visual configuration forms
- Real-time output display
- Progress indicators
- Error dialogs

## Best Practices

### When to Use Visual Components

**Always Use:**
- Status messages for operation results
- Progress bars for operations > 10 items
- Headers for script output sections
- Summaries for final results

**Consider Using:**
- Tables for structured data (> 3 rows)
- Boxes for important warnings/errors
- Spinners for indeterminate waits
- Colors for emphasis

**Avoid:**
- Excessive colors (use sparingly)
- Progress bars for < 10 items
- Complex visuals in CI/CD logs

### Performance Considerations

```python
# Check if terminal supports color before heavy use
from visual_helper import supports_color

if supports_color():
    # Use rich output
    print_header('My Script')
else:
    # Use plain output
    print('=== My Script ===')
```

### Logging vs Visual Output

```python
import logging
from visual_helper import print_success, print_error

# Visual output for user
print_success('File processed successfully')

# Logging for audit trail
logging.info('Processed file: example.txt (150 lines)')
```

## Examples

### Complete Script Example

```python
#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'lib'))
from visual_helper import (
    print_header, print_info, print_success, 
    ProgressBar, print_table, print_summary
)

def main():
    # Header
    print_header('File Processor', 'Version 1.0.0')
    
    # Info
    print_info('Starting file processing...')
    
    # Process with progress
    files = ['file1.txt', 'file2.txt', 'file3.txt']
    progress = ProgressBar(total=len(files), prefix='Processing')
    
    results = []
    for i, file in enumerate(files):
        # Process file
        result = process_file(file)
        results.append([file, result['status'], result['lines']])
        progress.update(i + 1)
    
    progress.finish('Processing complete')
    
    # Results table
    print_table(
        headers=['File', 'Status', 'Lines'],
        rows=results,
        title='Processing Results'
    )
    
    # Summary
    print_summary({
        'Total Files': len(files),
        'Processed': len([r for r in results if r[1] == 'Success']),
        'Status': 'COMPLETE'
    })
    
    print_success('All operations completed successfully!')

if __name__ == '__main__':
    main()
```

## See Also

- [visual_helper.py](../../scripts/lib/visual_helper.py) - Python implementation
- [VisualUtils.psm1](../../scripts/lib/VisualUtils.psm1) - PowerShell implementation
- [GuiUtils.psm1](../../scripts/lib/GuiUtils.psm1) - GUI utilities for Windows
