[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

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

## PHP Scripts - Visual Output Features

### Installation

Visual output is available through the PHP enterprise libraries.

```php
<?php
declare(strict_types=1);

use MokoStandards\Enterprise\VisualHelper;

$visual = new VisualHelper();
```

### Status Messages

```php
$visual->printSuccess('Operation completed successfully!');
//  ✓ Operation completed successfully!

$visual->printError('Failed to connect to database');
//  ✗ Failed to connect to database

$visual->printWarning('Configuration file not found, using defaults');
//  ⚠ Configuration file not found, using defaults

$visual->printInfo('Processing 150 files...');
//  ℹ Processing 150 files...
```

### Headers

```php
$visual->printHeader('Repository Validator', 'Version 04.00.00');
```

Output:
```
╔══════════════════════════════════════════════════╗
║           Repository Validator                   ║
║            Version 04.00.00                      ║
╚══════════════════════════════════════════════════╝
```

### Progress Bars

```php
$progress = new ProgressBar(total: 100, prefix: 'Processing files');

for ($i = 0; $i < 100; $i++) {
    // Do work
    $progress->update($i + 1, suffix: "file_{$i}.txt");
}
    
$progress->finish('All files processed');
```

Output:
```
Processing files: 50/100 50.0% [█████████████████████░░░░░░░░░░] ETA: 2.5s
✓ All files processed (took 5.23s)
```

### Spinners

```php
$spinner = new Spinner('Loading configuration');
$spinner->start();

// Do long-running work
sleep(3);

$spinner->stop('Configuration loaded');
```

Output:
```
⠋ Loading configuration...
✓ Configuration loaded
```

### Message Boxes

```php
$visual->printBox('This is an important informational message that users should read carefully.', 'info');
$visual->printBox('Operation completed successfully!', 'success');
$visual->printBox('Warning: This action cannot be undone.', 'warning');
$visual->printBox('Error: Connection failed.', 'error');
```

Output:
```
┌────────────────────────────────────────────────────┐
│ This is an important informational message that    │
│ users should read carefully.                       │
└────────────────────────────────────────────────────┘
```

### Tables

```php
$visual->printTable(
    headers: ['Script', 'Status', 'Duration', 'Files'],
    rows: [
        ['validate_structure', 'Pass', '1.2s', '150'],
        ['check_repo_health', 'Pass', '0.8s', '87'],
        ['security_scan', 'Warn', '2.1s', '3'],
    ],
    title: 'Validation Results',
    showIndex: true
);
```

Output:
```
Validation Results
┌───┬────────────────────┬────────┬──────────┬───────┐
│ # │ Script             │ Status │ Duration │ Files │
├───┼────────────────────┼────────┼──────────┼───────┤
│ 1 │ validate_structure │ Pass   │ 1.2s     │ 150   │
│ 2 │ check_repo_health  │ Pass   │ 0.8s     │ 87    │
│ 3 │ security_scan      │ Warn   │ 2.1s     │ 3     │
└───┴────────────────────┴────────┴──────────┴───────┘
```

### Summaries

```php
$visual->printSummary(
    items: [
        'Total Files' => 150,
        'Passed' => 147,
        'Warnings' => 3,
        'Errors' => 0,
        'Duration' => '2.5s',
        'Status' => 'SUCCESS'
    ],
    title: 'Execution Summary'
);
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

```php
if ($visual->confirm('Delete all temporary files?', default: false)) {
    $visual->printSuccess('Files deleted');
} else {
    $visual->printInfo('Operation cancelled');
}
```

Output:
```
? Delete all temporary files? [y/N]: y
✓ Files deleted
```

### Colors

```php
$text = $visual->colorize('This is red text', Color::RED, bold: true);
echo $text;

// Available colors:
// RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE
// BRIGHT_RED, BRIGHT_GREEN, BRIGHT_YELLOW, etc.
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

```php
// Check if terminal supports color before heavy use
if ($visual->supportsColor()) {
    // Use rich output
    $visual->printHeader('My Script');
} else {
    // Use plain output
    echo "=== My Script ===\n";
}
```

### Logging vs Visual Output

```php
use MokoStandards\Enterprise\AuditLogger;

$audit = new AuditLogger();

// Visual output for user
$visual->printSuccess('File processed successfully');

// Logging for audit trail
$audit->info('Processed file: example.txt (150 lines)');
```

## Examples

### Complete Script Example

```php
<?php
declare(strict_types=1);

use MokoStandards\Enterprise\VisualHelper;
use MokoStandards\Enterprise\ProgressBar;

function main(): void
{
    $visual = new VisualHelper();
    
    // Header
    $visual->printHeader('File Processor', 'Version 1.0.0');
    
    // Info
    $visual->printInfo('Starting file processing...');
    
    // Process with progress
    $files = ['file1.txt', 'file2.txt', 'file3.txt'];
    $progress = new ProgressBar(total: count($files), prefix: 'Processing');
    
    $results = [];
    foreach ($files as $i => $file) {
        // Process file
        $result = processFile($file);
        $results[] = [$file, $result['status'], $result['lines']];
        $progress->update($i + 1);
    }
    
    $progress->finish('Processing complete');
    
    // Results table
    $visual->printTable(
        headers: ['File', 'Status', 'Lines'],
        rows: $results,
        title: 'Processing Results'
    );
    
    // Summary
    $processed = count(array_filter($results, fn($r) => $r[1] === 'Success'));
    $visual->printSummary([
        'Total Files' => count($files),
        'Processed' => $processed,
        'Status' => 'COMPLETE'
    ]);
    
    $visual->printSuccess('All operations completed successfully!');
}

main();
```

## See Also

- `src/Enterprise/VisualHelper.php` - PHP implementation
- Web-based interfaces for GUI operations
