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
VERSION: 03.01.03
BRIEF: Standards for copyright headers, file information, and document metadata
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

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

**All files MUST include a copyright header as the first content.**

**Required Elements:**
- Copyright notice with year and owner
- Project membership statement
- SPDX license identifier
- Basic license terms (GPL-3.0-or-later)

**Suggested Elements:**
- Full GPL license text including warranty disclaimer
- Additional license details and references

### Minimal Header (Required Elements Only)

For simple files where brevity is preferred, use this minimal header:

#### For Markdown Files

```markdown
<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
DEFGROUP: [Group.Subgroup]
INGROUP: [Parent.Group]
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /path/to/file.md
VERSION: XX.YY.ZZ
BRIEF: Brief description of file purpose
-->
```

### Full Header (With Suggested Elements)

For comprehensive documentation and policies, use this full header with warranty disclaimer:

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

#### For Python Files (Minimal)

```python
#!/usr/bin/env python3
"""
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

FILE INFORMATION
DEFGROUP: [Group.Subgroup]
INGROUP: [Parent.Group]
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /path/to/file.py
VERSION: XX.YY.ZZ
BRIEF: Brief description of file purpose
"""
```

#### For Python Files (Full)

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

#### For PHP Files (Minimal)

```php
<?php
/* Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * This file is part of a Moko Consulting project.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
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

#### For PHP Files (Full)

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

#### For YAML Files (Minimal)

```yaml
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# This file is part of a Moko Consulting project.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# FILE INFORMATION
# DEFGROUP: [Group.Subgroup]
# INGROUP: [Parent.Group]
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: /path/to/file.yml
# VERSION: XX.YY.ZZ
# BRIEF: Brief description of file purpose
```

#### For YAML Files (Full)

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

#### For Shell Scripts (Minimal)

```bash
#!/bin/bash
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# This file is part of a Moko Consulting project.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# FILE INFORMATION
# DEFGROUP: [Group.Subgroup]
# INGROUP: [Parent.Group]
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: /path/to/script.sh
# VERSION: XX.YY.ZZ
# BRIEF: Brief description of file purpose
```

#### For Shell Scripts (Full)

```bash
#!/bin/bash
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# This file is part of a Moko Consulting project.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
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
# PATH: /path/to/script.sh
# VERSION: XX.YY.ZZ
# BRIEF: Brief description of file purpose
```

### Guidance on Header Selection

**Use Minimal Header (without warranty disclaimer) for:**
- Simple configuration files
- Short utility scripts
- Template files
- Example code
- Files under 100 lines

**Use Full Header (with warranty disclaimer) for:**
- Complex application code
- Public-facing APIs
- Distributed libraries
- Security-sensitive code
- Policy documents
- Comprehensive documentation

**When in doubt:** The minimal header is sufficient for most internal files. The warranty disclaimer adds legal clarity but is not required for GPL-3.0-or-later licensed code (it's implied by the license).

### Required Warranty Disclaimer Files

**The following files MUST include the full warranty disclaimer:**

#### 1. index.php Files (Directory Protection)

All `index.php` files used for directory protection MUST include the warranty disclaimer in a comment header:

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
 */

// Prevent directory listing
header("Location: ../");
exit;
```

#### 2. README Files (Visible Text)

README files MUST include the warranty disclaimer as **visible text** (not in comments):

```markdown
# Project Name

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
```

#### 3. Dolibarr Module Descriptor Files

Module descriptor files (`core/modules/mod*.class.php`) MUST include the warranty disclaimer:

```php
<?php
/* Copyright (C) 2026 Your Name <email@example.com>
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
 */
```

#### 4. Joomla Extension XML Files

Joomla manifest XML files MUST include the warranty disclaimer in the `<copyright>` or description section:

```xml
<?xml version="1.0" encoding="utf-8"?>
<extension type="component" version="4.0" method="upgrade">
    <name>COM_EXAMPLE</name>
    <copyright>Copyright (C) 2026 Your Name. All rights reserved.</copyright>
    <license>GNU General Public License version 3 or later</license>
    <description>
        <![CDATA[
        <p>Component description here.</p>
        <p><strong>License:</strong> This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by the Free Software Foundation,
        either version 3 of the License, or (at your option) any later version.</p>
        <p>This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
        without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
        See the GNU General Public License for more details.</p>
        ]]>
    </description>
</extension>
```

**Rationale:** These files are:
- User-facing (README)
- Installation/distribution files (Dolibarr descriptors, Joomla XML)
- Security-critical (index.php directory protection)

Users and administrators directly interact with these files, making explicit warranty disclaimers important for legal clarity.

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
