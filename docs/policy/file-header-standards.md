<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

# FILE INFORMATION
DEFGROUP: MokoStandards.Policy
INGROUP: MokoStandards.Documentation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/policy/file-header-standards.md
VERSION: 01.00.00
BRIEF: Standards for copyright headers, file information, and document metadata
-->

# File Header Standards Policy

## Purpose

This policy establishes mandatory requirements for copyright headers, file information blocks, and metadata sections in all files across MokoStandards-governed repositories. It ensures legal compliance, traceability, version control, and consistent documentation structure.

## Scope

This policy applies to:

- All source code files (PHP, Python, JavaScript, etc.)
- All configuration files where comments are supported
- All markdown documentation files
- All scripts and automation files
- All workflow files (YAML)
- Template files and examples

This policy does not apply to:

- Binary files (images, PDFs, compiled code)
- JSON files (do not support comments)
- Generated files (must be marked as generated)
- Third-party files (preserve original headers)
- Data files (CSV, plain text data)

## Responsibilities

### File Authors

Responsible for:

- Adding proper copyright header to all new files
- Including complete file information block
- Adding metadata section to markdown files
- Updating version on significant changes
- Maintaining revision history

### Code Reviewers

Responsible for:

- Verifying headers present and correct
- Checking metadata completeness
- Validating revision history updates
- Ensuring compliance in pull requests

### Repository Maintainers

Accountable for:

- Enforcing header standards
- Updating copyright years
- Auditing file compliance
- Managing exceptions

## Copyright Header Requirements

### Standard Copyright Header

**All files MUST include this copyright header as the first content:**

#### For Markdown Files

```markdown
<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

# FILE INFORMATION
DEFGROUP: [Group.Subgroup]
INGROUP: [Parent.Group]
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /path/to/file.md
VERSION: XX.YY.ZZ
BRIEF: Brief description of file purpose
-->
```

#### For Python Files

```python
#!/usr/bin/env python3
"""
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

FILE INFORMATION
DEFGROUP: [Group.Subgroup]
INGROUP: [Parent.Group]
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /path/to/file.py
VERSION: XX.YY.ZZ
BRIEF: Brief description of file purpose
"""
```

#### For PHP Files

```php
<?php
/* Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * This file is part of a Moko Consulting project.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 *
 * FILE INFORMATION
 * DEFGROUP: [Group.Subgroup]
 * INGROUP: [Parent.Group]
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /path/to/file.php
 * VERSION: XX.YY.ZZ
 * BRIEF: Brief description of file purpose
 */
```

#### For YAML Files

```yaml
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# This file is part of a Moko Consulting project.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# FILE INFORMATION
# DEFGROUP: [Group.Subgroup]
# INGROUP: [Parent.Group]
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: /path/to/file.yml
# VERSION: XX.YY.ZZ
# BRIEF: Brief description of file purpose
```

#### For Shell Scripts

```bash
#!/bin/bash
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# This file is part of a Moko Consulting project.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# [Full license header...]
#
# FILE INFORMATION
# DEFGROUP: [Group.Subgroup]
# INGROUP: [Parent.Group]
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: /path/to/script.sh
# VERSION: XX.YY.ZZ
# BRIEF: Brief description of file purpose
```

### File Information Block Fields

**Required Fields:**

- **DEFGROUP**: Defining group (logical grouping of related files)
- **INGROUP**: Parent group (hierarchical organization)
- **REPO**: Full repository URL
- **PATH**: Absolute path from repository root
- **VERSION**: Semantic version (MAJOR.MINOR.PATCH)
- **BRIEF**: One-line description of file purpose

**Optional Fields:**

- **NOTE**: Additional notes or warnings
- **AUTHOR**: Original author if not standard
- **DEPRECATED**: Deprecation notice if applicable

**Field Guidelines:**

**DEFGROUP Examples**:
- `MokoStandards.Policy`
- `MokoStandards.Scripts`
- `MokoStandards.Automation`
- `MokoCRM.Modules`
- `MokoWaaS.Components`

**INGROUP Examples**:
- `MokoStandards.Documentation`
- `MokoStandards.Security`
- `MokoCRM.Extensions`

**VERSION Format**:
- Use semantic versioning: `01.00.00`, `02.03.04`
- Zero-pad for consistency: `01.00.00` not `1.0.0`
- Increment MAJOR for breaking changes
- Increment MINOR for new features
- Increment PATCH for bug fixes

**BRIEF Guidelines**:
- Maximum 80 characters
- Start with action verb or noun
- Describe what, not how
- Examples:
  - "Development standards for MokoCRM Dolibarr platform"
  - "Automated sync of documentation to GitHub Project"
  - "Security scanning policy and vulnerability management"

## Markdown Document Requirements

### Metadata Section

**All markdown documents MUST include a metadata section near the end:**

```markdown
## Metadata

| Field              | Value                                |
| ------------------ | ------------------------------------ |
| Document           | [Document Name]                      |
| Path               | /path/to/document.md                 |
| Repository         | [Repository URL]                     |
| Owner              | [Owner Name/Role]                    |
| Scope              | [Scope description]                  |
| Status             | [Draft/Review/Published/Deprecated]  |
| Effective          | [YYYY-MM-DD]                         |

## Revision History

| Date       | Version  | Author          | Notes                        |
| ---------- | -------- | --------------- | ---------------------------- |
| 2026-01-04 | 01.00.00 | Moko Consulting | Initial document creation    |
```

**For Policy Documents, add additional metadata fields:**

```markdown
## Metadata

- **Document Type**: policy
- **Document Subtype**: core / waas / crm / security
- **Owner Role**: [Governance Owner / Security Owner / etc.]
- **Approval Required**: Yes / No
- **Evidence Required**: Yes / No
- **Review Cycle**: Annual / Semiannual / Quarterly / Ad hoc
- **Retention**: Indefinite / 7 Years / 5 Years / 3 Years
- **Compliance Tags**: [Governance, Audit, Security, etc.]
- **Status**: [Draft / Review / Published / Deprecated]
```

### Revision History Requirements

**Every change to a markdown document MUST be recorded:**

**Format**:
```markdown
| Date       | Version  | Author          | Notes                           |
| ---------- | -------- | --------------- | ------------------------------- |
| 2026-01-04 | 01.00.00 | Moko Consulting | Initial document creation       |
| 2026-01-15 | 01.01.00 | John Doe        | Added security requirements     |
| 2026-02-01 | 02.00.00 | Jane Smith      | Major restructuring             |
```

**Guidelines**:
- Use ISO date format: YYYY-MM-DD
- Use semantic versioning for version numbers
- Include author name or role
- Brief but descriptive notes
- Most recent change at bottom
- Keep all historical entries

## File Exemptions

### Files That Don't Require Headers

**Exempt Files**:
- `package.json` and other package manifests
- `.gitignore`, `.gitattributes`, `.editorconfig`
- `LICENSE` and `LICENSE.md` (standard license text)
- `README.md` at repository root (optionally omit header)
- Auto-generated files (must be clearly marked as generated)
- Third-party files (preserve original headers)

**Exempt File Types**:
- Binary files (images, fonts, compiled code)
- JSON files (no comment support)
- Plain text data files
- Lock files (`package-lock.json`, `Gemfile.lock`, etc.)

### Marking Generated Files

**Generated files that do support comments MUST include:**

```python
"""
THIS FILE IS AUTO-GENERATED. DO NOT EDIT MANUALLY.

Generated by: [script name]
Generated on: [timestamp]
Source: [source file or data]

Changes will be overwritten on next generation.
"""
```

## Copyright Year Updates

### When to Update Copyright Year

**Update copyright year when:**
- Making substantial modifications to file
- Adding new functionality
- Refactoring significant portions
- Beginning new year with active development

**Format for multiple years:**
- Single year: `Copyright (C) 2026`
- Range: `Copyright (C) 2024-2026`
- Multiple non-consecutive: `Copyright (C) 2024, 2026`

**Do NOT update copyright year for:**
- Trivial changes (typo fixes)
- Formatting-only changes
- Comment additions
- Whitespace changes

## Enforcement and Validation

### Automated Checks

**CI/CD MUST validate headers:**

```python
# scripts/validate/headers.py
def check_file_header(filepath):
    """Validate copyright header presence."""
    with open(filepath, 'r') as f:
        content = f.read(1000)  # Check first 1000 chars
    
    required_patterns = [
        'Copyright (C)',
        'Moko Consulting',
        'GPL-3.0-or-later',
        'FILE INFORMATION',
        'DEFGROUP:',
        'PATH:',
        'VERSION:'
    ]
    
    for pattern in required_patterns:
        if pattern not in content:
            return False, f"Missing: {pattern}"
    
    return True, "Header valid"
```

### Manual Review Checklist

**Pull request review MUST verify:**

- [ ] Copyright header present
- [ ] File information block complete
- [ ] All required fields populated
- [ ] Version number appropriate
- [ ] BRIEF accurately describes file
- [ ] Markdown documents have metadata section
- [ ] Markdown documents have revision history
- [ ] Revision history updated for changes
- [ ] Copyright year current (if substantial changes)

### Remediation Process

**For existing files missing headers:**

1. Create issue tracking header additions
2. Prioritize by file type and importance
3. Add headers in batches by directory
4. Update in dedicated pull requests
5. Do not mix header additions with functional changes

**Header Addition Script**:

```python
# scripts/add_headers.py
"""Add copyright headers to files missing them."""

import os
from pathlib import Path

def add_python_header(filepath):
    """Add copyright header to Python file."""
    header = '''#!/usr/bin/env python3
"""
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
[... full header ...]
"""

'''
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    if 'Copyright' not in content[:500]:
        with open(filepath, 'w') as f:
            f.write(header + content)
```

## Migration Plan

### Phase 1: New Files (Immediate)
- All new files MUST have headers from creation
- Pull request template includes header checklist
- CI validates headers on new files

### Phase 2: Critical Files (Month 1)
- Add headers to all policy documents
- Add headers to all scripts
- Add headers to all workflow files

### Phase 3: Documentation (Month 2)
- Add headers to all markdown docs
- Add metadata sections to docs
- Add revision history to docs

### Phase 4: Complete Coverage (Month 3)
- Add headers to remaining files
- Complete validation coverage
- Archive or remove files without headers

## Exceptions and Waivers

**Exception Process**:

1. Document technical justification
2. Identify alternative compliance method
3. Get maintainer approval
4. Document in file or EXCEPTIONS.md
5. Review exception annually

**Common Exceptions**:
- Minified files (document in source file)
- Vendor files (preserve original licensing)
- Platform-required files (follow platform standards)

## Tools and Automation

### Recommended Tools

**Header Templates**:
- VSCode: File Header extension
- IntelliJ: File templates
- Vim: Header template plugins

**Automation**:
- Pre-commit hooks to add headers
- CI validation scripts
- Bulk header addition scripts

### Header Template Repository

**Store templates in repository:**

```
.github/
└── templates/
    ├── header-python.txt
    ├── header-php.txt
    ├── header-markdown.txt
    └── header-yaml.txt
```

## Compliance and Audit

### Audit Process

**Quarterly header compliance audit:**

1. Scan all tracked files
2. Identify files missing headers
3. Generate compliance report
4. Create remediation issues
5. Track to completion

### Compliance Metrics

**Track:**
- Percentage of files with headers
- Percentage with complete metadata
- Percentage with revision history
- Time to remediate violations

**Goals:**
- 100% compliance for new files
- 95% compliance for existing files within 3 months
- 99% compliance within 6 months

## Related Policies

This policy works with:

- [Document Formatting Policy](document-formatting.md) - Overall formatting standards
- [Scripting Standards](scripting-standards.md) - Script-specific requirements
- [Documentation Governance](documentation-governance.md) - Document lifecycle

## Dependencies

This policy requires:

- Git repository with tracked files
- CI/CD capable of running validation scripts
- Code review process enforcing standards
- Documentation of exceptions

## Acceptance Criteria

- [ ] All new files include copyright header
- [ ] All new files include file information block
- [ ] All markdown docs include metadata section
- [ ] All markdown docs include revision history
- [ ] CI validates headers on pull requests
- [ ] Review process checks header compliance
- [ ] Exceptions documented and tracked
- [ ] Remediation plan for existing files

## Metadata

- **Document Type**: policy
- **Document Subtype**: core
- **Owner Role**: Documentation Owner
- **Approval Required**: Yes
- **Evidence Required**: Yes
- **Review Cycle**: Annual
- **Retention**: Indefinite
- **Compliance Tags**: Documentation, Governance, Legal
- **Status**: Published

## Revision History

| Date       | Version  | Author          | Notes                                 |
| ---------- | -------- | --------------- | ------------------------------------- |
| 2026-01-04 | 01.00.00 | Moko Consulting | Initial file header standards policy  |
