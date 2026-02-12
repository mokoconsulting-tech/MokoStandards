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
 (./LICENSE).
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# File Headers Policy

**Version:** 1.0.0
**Status:** Active
**Last Updated:** 2025-01-28

## Overview

This policy defines when to use full warranty disclaimers versus compressed headers in source files across the MokoStandards project. The goal is to maintain legal compliance while improving code readability and reducing visual clutter in configuration and workflow files.

## Policy Statement

All files must include copyright and licensing information, but the format varies based on file type and usage context.

## Header Types

### 1. Full Warranty Disclaimer

**Required for:**
- All Markdown documentation files (`.md`)
- Standalone executable scripts (with shebang `#!/...` or executable permission bit)
- Platform-specific integration files:
  - Dolibarr modules and customizations
  - Joomla extensions and components
  - WordPress plugins and themes
  - Any file directly executed by end-users or distributed as standalone software

**Format (YAML/Shell/Python):**
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
```

**Format (HTML/Markdown):**
```html
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
 (./LICENSE).
-->
```

### 2. Compressed Header

**Required for:**
- GitHub Actions workflow files (`.github/workflows/*.yml`)
- Configuration files (`.github/*.yml`, `pyproject.toml`, etc.)
- Template files (`templates/**/*.yml`)
- Non-executable modules and libraries
- Internal automation scripts (not distributed)
- Schema definitions

**Format:**
```yaml
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
# SPDX-License-Identifier: GPL-3.0-or-later
```

or for HTML/XML:
```html
<!-- Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech> -->
<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
```

## Rationale

### Why Compressed Headers?

1. **Improved Readability**: Workflow and configuration files are often long and complex. Removing 15+ lines of legal boilerplate at the top makes the actual functional content more accessible.

2. **Legal Sufficiency**: SPDX identifiers are legally recognized shorthand for full license terms. The compressed format provides:
   - Clear copyright attribution
   - Unambiguous license identification via SPDX-License-Identifier
   - Traceability to the full license text (in repository root)

3. **Industry Best Practice**: Major projects (Linux kernel, LLVM, etc.) use SPDX identifiers for most source files.

4. **Workflow Context**: GitHub Actions workflows are:
   - Not distributed as standalone software
   - Executed within GitHub's infrastructure
   - Part of a larger repository with LICENSE file at root
   - Primarily internal automation, not end-user facing

5. **Reduced Maintenance**: Fewer lines to maintain, update, and validate across hundreds of files.

### Why Keep Full Disclaimers?

1. **Markdown Documentation**: Documentation files are often:
   - Viewed independently (on web, in editors)
   - May be copied/extracted from the repository
   - Serve as primary reference material
   - Should be self-contained regarding licensing

2. **Executable Scripts**: Scripts that run independently require:
   - Clear warranty disclaimer for liability protection
   - Explicit GPL terms since they're standalone programs
   - Full license notice per GPL requirements

3. **Platform-Specific Files**: Integration files for Dolibarr, Joomla, etc.:
   - Often distributed separately from main repository
   - May be installed as modules/plugins by end-users
   - Subject to platform-specific licensing requirements
   - Need explicit warranty disclaimers per GPL v3 section 15-16

## Implementation

### Automated Tool

Use `scripts/fix/file_headers.py` to automatically apply the correct header format:

```bash
# Dry run to preview changes
python3 scripts/fix/file_headers.py --dry-run

# Apply fixes to specific directory
python3 scripts/fix/file_headers.py --dir .github/workflows --fix

# Apply fixes to entire repository
python3 scripts/fix/file_headers.py --fix
```

### Manual Updates

When creating new files:

1. Determine if file requires full disclaimer or compressed header (see criteria above)
2. Copy appropriate template from this document
3. Update copyright year to current year
4. For compressed headers, ensure only 2 lines are used

## Exceptions

- Files without copyright/license information should be evaluated case-by-case
- Third-party code must retain original license headers
- Generated files (by tools) may omit headers if impractical

## Compliance

All new files must follow this policy. Existing files will be migrated progressively using the automated tool.

## Related Policies

- [File Header Standards](file-header-standards.md) - Complete header format specifications
- [License Compliance](license-compliance.md) - Overall licensing requirements
- [Scripting Standards](scripting-standards.md) - Script-specific requirements

## Revision History

| Version | Date       | Author           | Changes                     |
|---------|------------|------------------|-----------------------------|
| 1.0.0   | 2025-01-28 | Moko Consulting  | Initial policy document     |

## References

1. [SPDX License List](https://spdx.org/licenses/)
2. [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.html)
3. [Linux Kernel Licensing Rules](https://www.kernel.org/doc/html/latest/process/license-rules.html)
4. [GitHub Actions Documentation](https://docs.github.com/en/actions)
