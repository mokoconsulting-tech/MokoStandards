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
VERSION: 03.00.00
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
- Use semantic versioning: `01.00.00`, `03.05.12`
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

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Policy                                       |
| Domain         | Governance                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/policy/file-header-standards.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
