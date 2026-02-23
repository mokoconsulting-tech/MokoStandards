[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.03-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

---
TITLE: Help Flag Implementation Pattern
DESCRIPTION: Standard pattern for adding --help documentation flags to all scripts
AUTHOR: Moko Consulting LLC
COPYRIGHT: 2025-2026 Moko Consulting LLC
LICENSE: MIT
VERSION: 04.00.03
CREATED: 2026-01-29
UPDATED: 2026-01-29
CATEGORY: Development
TAGS: documentation, help, scripts, patterns
STATUS: Active
---

# Help Flag Implementation Pattern

All MokoStandards scripts should support `--help-doc` and `--help-full` flags to display their associated markdown documentation.

## Python Scripts

### 1. Import doc_helper module

```python
#!/usr/bin/env python3
"""Script description"""

import sys
from pathlib import Path

# Add scripts/lib to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'lib'))
try:
    from doc_helper import add_help_argument, handle_help_flags
    DOC_HELPER_AVAILABLE = True
except ImportError:
    DOC_HELPER_AVAILABLE = False
```

### 2. Add help arguments to ArgumentParser

```python
def main():
    parser = argparse.ArgumentParser(
        description='Script description',
        epilog='For complete documentation, use: --help-doc'
    )
    
    # Regular arguments
    parser.add_argument('--input', help='Input file')
    
    # Add documentation help flags
    if DOC_HELPER_AVAILABLE:
        add_help_argument(parser, __file__, 'category/script-name.md')
    
    args = parser.parse_args()
    
    # Handle help flags (must be before other logic)
    if DOC_HELPER_AVAILABLE and handle_help_flags(args, __file__, 'category/script-name.md'):
        return 0
    
    # Rest of script logic
    ...
```

### 3. Documentation file naming

Place documentation in `docs/{category}/{script-name}.md`:

- `scripts/validate/check_repo_health.py` → `docs/validate/check-repo-health.md`
- `scripts/automation/bulk_update_repos.py` → `docs/automation/bulk-update-repos.md`
- `scripts/run/load_demo_data.py` → `docs/demo/demo-data-loader.md`

## PowerShell Scripts

### 1. Add help parameters

```powershell
<#
.SYNOPSIS
    Script description

.PARAMETER HelpDoc
    Display full documentation from markdown files
#>

[CmdletBinding()]
param(
    [Parameter()]
    [switch]$HelpDoc,
    
    # Other parameters
    [Parameter()]
    [string]$InputFile
)

# Display documentation if requested
if ($HelpDoc) {
    $docPath = Join-Path $PSScriptRoot "..\..\docs\category\script-name.md"
    
    if (Test-Path $docPath) {
        Get-Content $docPath | Write-Host
    } else {
        Write-Host "Documentation not found: $docPath"
        Write-Host "For general documentation, see:"
        Write-Host "https://github.com/mokoconsulting-tech/MokoStandards/tree/main/docs"
    }
    
    exit 0
}

# Rest of script logic
...
```

## Shell Scripts

### 1. Add help flag handling

```bash
#!/bin/bash

# Show help documentation
show_help_doc() {
    local doc_path="../../docs/category/script-name.md"
    
    if [ -f "$doc_path" ]; then
        cat "$doc_path"
    else
        echo "Documentation not found: $doc_path"
        echo "For general documentation, see:"
        echo "https://github.com/mokoconsulting-tech/MokoStandards/tree/main/docs"
    fi
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --help-doc|--help-full)
            show_help_doc
            exit 0
            ;;
        --input)
            INPUT_FILE="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Rest of script logic
...
```

## PHP Scripts

### 1. Add help flag handling

```php
<?php
/**
 * Script description
 */

// Check for help flag
if (isset($_GET['help']) || (isset($argv) && in_array('--help-doc', $argv))) {
    $doc_path = __DIR__ . '/../../docs/category/script-name.md';
    
    if (file_exists($doc_path)) {
        echo file_get_contents($doc_path);
    } else {
        echo "Documentation not found: $doc_path\n";
        echo "For general documentation, see:\n";
        echo "https://github.com/mokoconsulting-tech/MokoStandards/tree/main/docs\n";
    }
    
    exit(0);
}

// Rest of script logic
...
?>
```

## Documentation File Format

Each script should have a corresponding markdown documentation file with this structure:

```markdown
---
TITLE: Script Name
DESCRIPTION: Brief description
AUTHOR: Moko Consulting LLC
COPYRIGHT: 2025-2026 Moko Consulting LLC
LICENSE: MIT
VERSION: 04.00.03
CREATED: YYYY-MM-DD
UPDATED: YYYY-MM-DD
CATEGORY: Category
TAGS: tag1, tag2
STATUS: Active
---

# Script Name

Brief overview of what the script does.

## Quick Start

```bash
# Basic usage example
python3 script.py --input file.txt
```

## Options

Describe all command-line options

## Examples

Provide usage examples

## Troubleshooting

Common issues and solutions
```

## Implementation Checklist

For each script:

- [ ] Create/update documentation markdown file
- [ ] Add help flag support to script
- [ ] Test `--help-doc` displays documentation
- [ ] Test regular `--help` still works
- [ ] Verify documentation path is correct
- [ ] Update script README if needed

## Scripts to Update

Priority order:

1. **High Priority** (user-facing):
   - validate/* scripts
   - automation/* scripts  
   - run/* scripts
   - maintenance/* scripts

2. **Medium Priority**:
   - analysis/* scripts
   - build/* scripts
   - release/* scripts

3. **Low Priority**:
   - tests/* scripts
   - lib/* utilities

## Benefits

- ✅ Consistent help documentation across all scripts
- ✅ Users can access detailed docs without leaving terminal
- ✅ Documentation stays in sync with code
- ✅ Reduces need to browse GitHub for help
- ✅ Improves discoverability of features

## Related Files

- `scripts/lib/doc_helper.py` - Python helper module
- `docs/` - All script documentation
- This file - Implementation pattern guide
