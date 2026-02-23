[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.03-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Execution Summaries

**Purpose**: Display execution summaries in job/console output before scripts and workflows exit.

## Overview

Execution summaries provide immediate visibility into script and workflow results without requiring users to navigate to separate summary tabs or logs. By displaying formatted summaries at the end of output, users can quickly see:

- Overall success/failure status
- Execution duration
- Statistics and counts
- Errors and warnings
- Next steps or recommendations

## Why Summaries Matter

**Without Summaries:**
- Results buried in output logs
- Must scroll through entire output
- Need to click "Summary" tab in GitHub Actions
- Easy to miss important information

**With Summaries:**
- Results at the bottom of output (last thing seen)
- Quick visual scanning with icons and colors
- Available in both job output AND summary tab
- Clear status and next actions

## When to Use Summaries

Add execution summaries to:

- ✅ Scripts that perform validation/checking
- ✅ Scripts that process multiple files
- ✅ Scripts with pass/fail results
- ✅ Long-running operations
- ✅ Automation workflows
- ✅ CI/CD pipelines
- ✅ Any script where user needs status confirmation

## Summary Content Guidelines

### Required Elements

Every summary should include:

1. **Status** - Overall success/failure/warning
2. **Duration** - How long the operation took
3. **Statistics** - Key metrics (files processed, pass/fail counts, etc.)

### Optional Elements

Include when relevant:

4. **File Counts** - Types of files processed
5. **Errors** - List of errors encountered
6. **Warnings** - List of warnings
7. **Details** - Additional contextual information
8. **Next Steps** - Recommended actions

### Visual Elements

Use visual indicators for quick scanning:

- ✓ Success icon for passed
- ✗ Error icon for failed
- ⚠ Warning icon for warnings
- ⏱ Clock for duration
- 📊 Chart for statistics
- 🎯 Target for next steps

## Implementation Patterns

### PHP Scripts

Use the web interface or CLI framework:

```php
<?php
declare(strict_types=1);

use MokoStandards\Enterprise\ExecutionSummary;

function main(): int
{
    // Create summary
    $summary = new ExecutionSummary(scriptName: 'my_validator', version: '1.0.0');
    $summary->start();
    
    try {
        // Perform work
        $filesChecked = 0;
        $filesPassed = 0;
        $filesFailed = 0;
        
        foreach ($files as $file) {
            $filesChecked++;
            if (validate($file)) {
                $filesPassed++;
            } else {
                $filesFailed++;
                $summary->addError("Validation failed: {$file}");
            }
        }
        
        // Set status
        if ($filesFailed === 0) {
            $summary->setStatus("Success");
        } else {
            $summary->setStatus("Failed");
        }
        
        // Add statistics
        $summary->addStat("Files Checked", $filesChecked);
        $summary->addStat("Passed", $filesPassed);
        $summary->addStat("Failed", $filesFailed);
        
        // Add next steps
        if ($filesFailed > 0) {
            $summary->addNextStep("Fix {$filesFailed} failed validations");
            $summary->addNextStep("Re-run validation after fixes");
        } else {
            $summary->addNextStep("All validations passed - ready to proceed");
        }
        
        return $filesFailed === 0 ? 0 : 1;
        
    } finally {
        // Always show summary
        $summary->stop();
        $summary->printSummary();
    }
}

exit(main());
```

### PowerShell Scripts

Use `VisualUtils` module:

```powershell
Import-Module "$PSScriptRoot/../lib/VisualUtils.psm1"

$startTime = Get-Date

try {
    # Perform work
    $filesChecked = 0
    $filesPassed = 0
    $filesFailed = 0
    
    foreach ($file in $files) {
        $filesChecked++
        if (Test-File $file) {
            $filesPassed++
        } else {
            $filesFailed++
        }
    }
    
    # Determine status
    $status = if ($filesFailed -eq 0) { "Success" } else { "Failed" }
    
} finally {
    # Always show summary
    $duration = (Get-Date) - $startTime
    
    Write-Header -Title "Validation Summary"
    
    if ($filesFailed -eq 0) {
        Write-SuccessMessage "All checks passed"
    } else {
        Write-ErrorMessage "$filesFailed checks failed"
    }
    
    Write-Host "⏱  Duration: $($duration.ToString('mm\:ss'))"
    Write-Host ""
    Write-Host "📊 Results:"
    Write-Host "  - Files Checked: $filesChecked"
    Write-Host "  - Passed: $filesPassed"
    Write-Host "  - Failed: $filesFailed"
    Write-Host ""
    
    if ($filesFailed -gt 0) {
        Write-Host "🎯 Next Steps:"
        Write-Host "  - Fix $filesFailed failed validations"
        Write-Host "  - Re-run validation"
    }
}
```

### Bash Scripts (Workflows)

Use bash functions:

```bash
#!/bin/bash

# Function to display summary
show_summary() {
    local status=$1
    local duration=$2
    local files_checked=$3
    local files_passed=$4
    local files_failed=$5
    
    echo ""
    echo "╔════════════════════════════════════════╗"
    echo "║         EXECUTION SUMMARY              ║"
    echo "╚════════════════════════════════════════╝"
    
    if [ "$status" = "success" ]; then
        echo "✅ Status: Success"
    else
        echo "❌ Status: Failed"
    fi
    
    echo "⏱️  Duration: ${duration}s"
    echo ""
    echo "📊 Results:"
    echo "  - Files Checked: $files_checked"
    echo "  - Passed: $files_passed"
    echo "  - Failed: $files_failed"
    echo ""
    
    if [ $files_failed -gt 0 ]; then
        echo "🎯 Next Steps:"
        echo "  - Fix $files_failed failed validations"
    fi
    echo ""
}

# Track start time
START_TIME=$SECONDS

# Perform work
files_checked=0
files_passed=0
files_failed=0

# ... validation logic ...

# Calculate duration
DURATION=$((SECONDS - START_TIME))

# Determine status
if [ $files_failed -eq 0 ]; then
    status="success"
    exit_code=0
else
    status="failed"
    exit_code=1
fi

# Always show summary
show_summary "$status" "$DURATION" "$files_checked" "$files_passed" "$files_failed"

exit $exit_code
```

### GitHub Actions Workflows

Add summary output at the end of jobs:

```yaml
jobs:
  validation:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Run Validation
        id: validate
        run: |
          # Validation logic
          # ...
          
          # Set outputs
          echo "status=success" >> $GITHUB_OUTPUT
          echo "files_checked=150" >> $GITHUB_OUTPUT
          echo "files_passed=147" >> $GITHUB_OUTPUT
          echo "files_failed=3" >> $GITHUB_OUTPUT
      
      - name: Display Summary
        if: always()
        run: |
          echo ""
          echo "╔════════════════════════════════════════╗"
          echo "║       VALIDATION SUMMARY               ║"
          echo "╚════════════════════════════════════════╝"
          echo "✅ Status: ${{ steps.validate.outputs.status }}"
          echo "📊 Results:"
          echo "  - Files Checked: ${{ steps.validate.outputs.files_checked }}"
          echo "  - Passed: ${{ steps.validate.outputs.files_passed }}"
          echo "  - Failed: ${{ steps.validate.outputs.files_failed }}"
          echo ""
          
          # Also write to GitHub summary tab
          {
            echo "## Validation Summary"
            echo ""
            echo "- Status: ${{ steps.validate.outputs.status }}"
            echo "- Files Checked: ${{ steps.validate.outputs.files_checked }}"
            echo "- Passed: ${{ steps.validate.outputs.files_passed }}"
            echo "- Failed: ${{ steps.validate.outputs.files_failed }}"
          } >> $GITHUB_STEP_SUMMARY
```

## Best Practices

### Content

1. **Keep it Concise** - Summary should fit on one screen
2. **Use Icons** - Visual indicators aid quick scanning
3. **Show Duration** - Users want to know how long things took
4. **Provide Context** - Include relevant statistics
5. **Suggest Actions** - Tell users what to do next

### Formatting

1. **Use Borders** - Box characters create clear visual boundaries
2. **Align Text** - Make data easy to scan
3. **Group Related Info** - Keep statistics together
4. **Use Colors** - When available, use colors for status
5. **Consistent Style** - Follow same pattern across scripts

### Timing

1. **Always Display** - Use try/finally to ensure summary shows
2. **End of Output** - Summary should be last thing displayed
3. **Before Exit** - Display before script returns/exits
4. **On Errors** - Show summary even when script fails

### GitHub Actions

1. **Job Output AND Summary** - Write to both locations
2. **Use `if: always()`** - Ensure summary step runs
3. **Capture Outputs** - Use step outputs for data
4. **Markdown Format** - Use markdown for $GITHUB_STEP_SUMMARY

## Examples

See these files for complete examples:

- `src/Enterprise/ExecutionSummary.php` - PHP implementation
- `.github/workflows/standards-compliance.yml` - Workflow example

## Benefits

**User Experience:**
- ✅ Immediate visibility of results
- ✅ No need to navigate to other tabs
- ✅ Quick status confirmation
- ✅ Clear next actions

**Developer Experience:**
- ✅ Consistent format across scripts
- ✅ Easy to implement with helpers
- ✅ Reusable patterns
- ✅ Better debugging

**Operations:**
- ✅ Faster troubleshooting
- ✅ Better log analysis
- ✅ Clear audit trail
- ✅ Improved monitoring
