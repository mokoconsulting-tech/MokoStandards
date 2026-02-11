[![MokoStandards](https://img.shields.io/badge/MokoStandards-03.02.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# InGroup and DefGroup Parameters

**Purpose**: Standardized metadata system for categorizing and grouping scripts, workflows, and documentation in MokoStandards.

---

## Overview

The `InGroup` and `DefGroup` parameters provide a standardized way to categorize scripts, workflows, and documentation across the MokoStandards repository. This enables:

- **Discovery**: Find all scripts in a functional group
- **Organization**: Logical grouping beyond directory structure
- **Documentation**: Auto-generate catalogs by group
- **Filtering**: Select scripts by purpose or domain
- **Relationships**: Show related scripts across directories

## Parameter Definitions

### InGroup (Member Of)

**Purpose**: Indicates which group(s) a script/workflow belongs to.

**Type**: Array/List of group names

**Usage**: A script can belong to multiple groups

**Example**: A script might be in both `MokoStandards.Validation` and `MokoStandards.Security`

### DefGroup (Defines Group)

**Purpose**: Indicates that this file defines or represents a group.

**Type**: Single group name

**Usage**: Used for group definition files, catalogs, or primary representatives

**Example**: A README defining `MokoStandards.Documentation` group

## Standard MokoStandards Groups

### Core Functional Groups

| Group Name | Purpose | Examples |
|------------|---------|----------|
| `MokoStandards.Documentation` | Documentation generation, management, and updates | generate_docs.py, update_readme.py |
| `MokoStandards.Validation` | Validation, checking, and verification | validate_structure.py, check_repo_health.py |
| `MokoStandards.Automation` | Automation workflows and bulk operations | bulk_update_repos.py, file-distributor.py |
| `MokoStandards.Maintenance` | Maintenance, updates, and housekeeping | update_changelog.py, clean_old_branches.py |
| `MokoStandards.Analysis` | Analysis, metrics, and reporting | code_metrics.py, analyze_dependencies.py |
| `MokoStandards.Build` | Build systems and compilation | Makefiles, build scripts |
| `MokoStandards.Release` | Release management and versioning | release_version.py, package_extension.py |
| `MokoStandards.Testing` | Testing utilities and test data | test runners, demo data loaders |
| `MokoStandards.Security` | Security scanning and compliance | security_scan.py, no_secrets.py |
| `MokoStandards.GUI` | GUI applications and interfaces | Invoke-*GUI.ps1 scripts |

### Platform/Technology Groups

| Group Name | Purpose | Examples |
|------------|---------|----------|
| `MokoStandards.Joomla` | Joomla-specific tools | Joomla validators, builders |
| `MokoStandards.Dolibarr` | Dolibarr-specific tools | Dolibarr release tools |
| `MokoStandards.Terraform` | Terraform configurations | Terraform modules, validators |
| `MokoStandards.Workflows` | GitHub Actions workflows | Reusable workflows |
| `MokoStandards.Python` | Python-specific utilities | Python helpers, modules |
| `MokoStandards.PowerShell` | PowerShell-specific utilities | PowerShell modules |

### Special Purpose Groups

| Group Name | Purpose | Examples |
|------------|---------|----------|
| `MokoStandards.Demo` | Demo and example files | Demo data, sample configs |
| `MokoStandards.Templates` | Template files | File templates, scaffolding |
| `MokoStandards.Helpers` | Helper/utility modules | Common libraries, utilities |
| `MokoStandards.Wrappers` | Wrapper scripts | Cross-platform wrappers |
| `MokoStandards.Internal` | Internal/infrastructure scripts | Repository management |

## Implementation Patterns

### Python Scripts

Add group metadata in the file header:

```python
#!/usr/bin/env python3
"""
FILE: scripts/validate/check_repo_health.py
AUTHOR: MokoStandards Team
DATE: 2026-01-30
VERSION: 03.01.03
DESCRIPTION: Validate repository health and structure
INGROUP: MokoStandards.Validation, MokoStandards.Analysis
"""
```

Or in a metadata dictionary:

```python
# Script Metadata
METADATA = {
    'name': 'Repository Health Checker',
    'version': '01.00.00',
    'author': 'MokoStandards Team',
    'ingroup': ['MokoStandards.Validation', 'MokoStandards.Analysis'],
    'description': 'Validate repository health and structure'
}
```

### PowerShell Scripts

Add group metadata in the comment-based help:

```powershell
<#
.SYNOPSIS
    Repository health checker GUI

.DESCRIPTION
    GUI interface for checking repository health and structure

.METADATA
    InGroup: MokoStandards.Validation, MokoStandards.GUI
    DefGroup: -
    Version: 01.00.00
    Author: MokoStandards Team

.EXAMPLE
    .\Invoke-RepoHealthCheckGUI.ps1
#>
```

Or in a metadata hashtable:

```powershell
# Script Metadata
$Metadata = @{
    Name = 'Repository Health Checker GUI'
    Version = '01.00.00'
    Author = 'MokoStandards Team'
    InGroup = @('MokoStandards.Validation', 'MokoStandards.GUI')
    Description = 'GUI for repository health checking'
}
```

### Shell Scripts

Add group metadata in the file header:

```bash
#!/bin/bash
#
# FILE: scripts/wrappers/bash/check_repo_health.sh
# AUTHOR: MokoStandards Team
# DATE: 2026-01-30
# VERSION: 03.01.03
# DESCRIPTION: Wrapper for repository health checker
# INGROUP: MokoStandards.Validation, MokoStandards.Wrappers
```

### Markdown Documentation

Add group metadata in YAML frontmatter:

```markdown
---
title: Repository Health Validation
author: MokoStandards Team
date: 2026-01-30
version: 01.00.00
ingroup:
  - MokoStandards.Documentation
  - MokoStandards.Validation
defgroup: MokoStandards.Validation
---

# Repository Health Validation

Documentation for repository health checking...
```

### GitHub Actions Workflows

Add group metadata in workflow file:

```yaml
name: Standards Compliance
# Metadata:
#   InGroup: MokoStandards.Workflows, MokoStandards.Validation
#   Purpose: Enforce coding standards across repository
#   Schedule: On push, pull request

on:
  push:
    branches: [main]
  pull_request:

jobs:
  validate:
    runs-on: ubuntu-latest
    # ...
```

## Usage Examples

### Discovering Scripts by Group

**Python Script** (`scripts/discovery/find_by_group.py`):

```python
#!/usr/bin/env python3
"""Find all scripts in a specific group."""

import os
import re
from pathlib import Path

def find_scripts_in_group(group_name, root_dir='.'):
    """Find all scripts that belong to a specific group."""
    scripts = []
    
    for path in Path(root_dir).rglob('*.py'):
        with open(path) as f:
            content = f.read(2000)  # Read first 2KB
            if f'INGROUP:' in content.upper():
                # Extract group metadata
                match = re.search(r'INGROUP:\s*(.+)', content, re.IGNORECASE)
                if match:
                    groups = [g.strip() for g in match.group(1).split(',')]
                    if group_name in groups:
                        scripts.append(str(path))
    
    return scripts

# Usage
validation_scripts = find_scripts_in_group('MokoStandards.Validation')
print(f"Found {len(validation_scripts)} validation scripts:")
for script in validation_scripts:
    print(f"  - {script}")
```

### Generating Group Catalogs

**Python Script** (`scripts/docs/generate_group_catalog.py`):

```python
#!/usr/bin/env python3
"""Generate catalog of scripts by group."""

from collections import defaultdict
import re
from pathlib import Path

def generate_catalog():
    """Generate markdown catalog organized by groups."""
    groups = defaultdict(list)
    
    # Scan all Python scripts
    for path in Path('scripts').rglob('*.py'):
        with open(path) as f:
            content = f.read(2000)
            match = re.search(r'INGROUP:\s*(.+)', content, re.IGNORECASE)
            if match:
                script_groups = [g.strip() for g in match.group(1).split(',')]
                desc_match = re.search(r'DESCRIPTION:\s*(.+)', content)
                description = desc_match.group(1) if desc_match else 'No description'
                
                for group in script_groups:
                    groups[group].append({
                        'path': str(path),
                        'description': description
                    })
    
    # Generate markdown
    catalog = "# MokoStandards Script Catalog\n\n"
    
    for group in sorted(groups.keys()):
        catalog += f"\n## {group}\n\n"
        for script in sorted(groups[group], key=lambda x: x['path']):
            catalog += f"- **{script['path']}**: {script['description']}\n"
    
    return catalog

# Usage
catalog = generate_catalog()
with open('docs/SCRIPT_CATALOG.md', 'w') as f:
    f.write(catalog)
```

### Filtering in Scripts

```python
#!/usr/bin/env python3
"""Script that can filter operations by group."""

import argparse

METADATA = {
    'ingroup': ['MokoStandards.Validation', 'MokoStandards.Analysis']
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--group-filter', help='Only process scripts in this group')
    args = parser.parse_args()
    
    if args.group_filter:
        if args.group_filter not in METADATA['ingroup']:
            print(f"This script is not in group: {args.group_filter}")
            return 1
    
    # Continue with main logic
    print(f"Running in groups: {', '.join(METADATA['ingroup'])}")

if __name__ == "__main__":
    main()
```

## Best Practices

### Naming Conventions

1. **Use Namespace Prefix**: All groups start with `MokoStandards.`
2. **Use PascalCase**: Capitalize each word (e.g., `MokoStandards.ValidationTools`)
3. **Be Descriptive**: Clear, self-explanatory names
4. **Avoid Redundancy**: Don't repeat "MokoStandards" in the suffix

### Group Assignment

1. **Primary Group First**: List the primary/most relevant group first
2. **Limit Groups**: Usually 1-3 groups per script (avoid over-categorization)
3. **Logical Grouping**: Groups should make sense together
4. **Consider Discovery**: Think about how users will search

### Documentation

1. **Always Include Description**: Explain the group's purpose
2. **List Members**: Document which scripts belong to each group
3. **Show Relationships**: Indicate related groups
4. **Provide Examples**: Show typical group usage

## Group Registry

The official group registry is maintained in `docs/reference/group-registry.md`.

To propose a new group:

1. Check if existing group covers the use case
2. Follow naming conventions
3. Provide clear purpose and scope
4. List initial members
5. Submit PR with documentation

## Discovery Tools

### List All Groups

```bash
# Find all unique groups in repository
grep -rh "INGROUP:" scripts/ | \
  sed 's/.*INGROUP:\s*//' | \
  tr ',' '\n' | \
  sed 's/^[[:space:]]*//' | \
  sort -u
```

### Count Scripts by Group

```bash
# Count scripts in each group
for group in $(grep -rh "INGROUP:" scripts/ | sed 's/.*INGROUP:\s*//' | tr ',' '\n' | sed 's/^[[:space:]]*//' | sort -u); do
  count=$(grep -rl "INGROUP:.*$group" scripts/ | wc -l)
  echo "$count scripts in $group"
done
```

### Find Group Definitions

```bash
# Find files that define groups
grep -rl "DEFGROUP:" docs/ scripts/
```

## Benefits

**Organization:**
- ✅ Clear categorization beyond directory structure
- ✅ Cross-cutting concerns easily grouped
- ✅ Related scripts discoverable

**Discovery:**
- ✅ Find scripts by purpose
- ✅ Generate catalogs automatically
- ✅ Filter operations by group

**Documentation:**
- ✅ Auto-generate group documentation
- ✅ Show relationships between scripts
- ✅ Maintain script inventory

**Automation:**
- ✅ Run groups of scripts together
- ✅ Selective processing by group
- ✅ Group-based workflows

## See Also

- `docs/reference/group-registry.md` - Official group registry
- `docs/policy/file-header-standards.md` - File header requirements
- `docs/scripts/SCRIPT_CATALOG.md` - Auto-generated catalog
- `scripts/docs/generate_group_catalog.py` - Catalog generator
