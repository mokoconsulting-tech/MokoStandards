# License Templates

## Purpose

This directory contains authoritative license files that serve as the official templates for all repositories in the `mokoconsulting-tech` organization. These files are the single source of truth for license text used across all projects.

## Authoritative Licenses

The following license files are maintained as authoritative sources:

### GPL-3.0 (GNU General Public License v3.0 or later)

**File**: `GPL-3.0`

**SPDX Identifier**: `GPL-3.0-or-later`

**Usage**: This is the **primary and default license** for all Moko Consulting projects unless explicitly specified otherwise.

**Source**: Official text from Free Software Foundation (https://www.gnu.org/licenses/gpl-3.0.txt)

**Default License For**:
- **Generic repositories** (default)
- **Joomla/WaaS component repositories** (default)
- **Dolibarr/CRM module repositories** (default)
- All software projects, libraries, frameworks, tools and utilities

**Repository Requirements**:
- Copy this file to repository root as `LICENSE` (no extension)
- Include copyright notice in project files
- Update copyright year and owner in project header comments

### MIT License

**File**: `MIT`

**SPDX Identifier**: `MIT`

**Usage**: Alternative permissive license for specific use cases.

**When to Use**:
- When GPL compatibility is not required
- Maximum permissiveness desired
- Integration with MIT-licensed dependencies

### Apache License 2.0

**File**: `Apache-2.0`

**SPDX Identifier**: `Apache-2.0`

**Usage**: Alternative license providing patent protection.

**When to Use**:
- Projects requiring explicit patent grant
- Apache ecosystem integration
- When patent protection is critical

## Using These Licenses

### For New Repositories

1. **Copy the license file** to your repository root:
   ```bash
   # From your repository root
   cp /path/to/MokoStandards/templates/licenses/GPL-3.0 ./LICENSE
   ```

2. **No file extension**: The LICENSE file must not have an extension (use `LICENSE`, not `LICENSE.txt` or `LICENSE.md`)

3. **Add copyright notice**: Update your project's README and source files with appropriate copyright notices

4. **Reference in documentation**: Mention the license in your README.md

### For Existing Repositories

1. **Verify license text**: Compare your existing LICENSE file with the authoritative version
2. **Update if needed**: If text differs, update to match the authoritative version
3. **Document changes**: Note license updates in CHANGELOG.md

## Updating License Templates

When updating these authoritative license files:

1. **Verify source**: Ensure updates come from official sources (FSF, OSI, Apache Foundation)
2. **Document changes**: Update this README with change details
3. **Notify stakeholders**: Announce updates to development team
4. **Version control**: Commit changes with detailed commit message
5. **Propagate**: Update existing repositories as needed

## License Selection Guide

### Decision Tree

```
Is this a new Moko Consulting project?
  └─ Yes → Use GPL-3.0-or-later (default)
  └─ No → See exceptions below

Project Type Default Licenses:
  - Generic Repository → GPL-3.0-or-later
  - Joomla/WaaS Component → GPL-3.0-or-later
  - Dolibarr/CRM Module → GPL-3.0-or-later

Exceptions requiring different licenses:
  - Third-party integration requiring MIT → Use MIT
  - Patent-sensitive project → Use Apache-2.0
  - Client-specific requirements → Consult legal team
```

### Compatibility Matrix

| Your License | Can Use GPL-3.0 | Can Use MIT | Can Use Apache-2.0 |
|--------------|-----------------|-------------|-------------------|
| GPL-3.0-or-later | ✅ Yes | ✅ Yes | ✅ Yes |
| MIT | ❌ No | ✅ Yes | ✅ Yes |
| Apache-2.0 | ⚠️ Compatible but becomes GPL | ✅ Yes | ✅ Yes |

## Compliance Requirements

### GPL-3.0-or-later Projects

**Must**:
- Include complete license text in LICENSE file
- Include copyright notice in source files
- Provide source code to recipients
- Document modifications to GPL code
- License derivative works under GPL-3.0-or-later

**Must Not**:
- Remove or modify license text
- Claim proprietary ownership of GPL code
- Impose additional restrictions

### File Headers

Include this header in all source files:

```
Copyright (C) [YEAR] Moko Consulting <hello@mokoconsulting.tech>

This file is part of [PROJECT NAME].

SPDX-License-Identifier: GPL-3.0-or-later

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
```

## Verification

### Verify License Text Integrity

```bash
# Check if your LICENSE matches the authoritative version
diff LICENSE /path/to/MokoStandards/templates/licenses/GPL-3.0

# Calculate checksum for verification
sha256sum LICENSE
```

### Automated Verification

The repository health workflow automatically verifies:
- LICENSE file exists
- LICENSE file has no extension
- License text matches authoritative version (for GPL-3.0)
- SPDX identifier is present in source files

## References

- [GNU GPL v3.0 Official](https://www.gnu.org/licenses/gpl-3.0.html)
- [SPDX License List](https://spdx.org/licenses/)
- [Choose a License](https://choosealicense.com/)
- [GPL Compliance Guide](https://www.gnu.org/licenses/gpl-compliance.html)
- [MokoStandards License Policy](../../docs/policy/license-compliance.md)

## Maintenance

**Owner**: Legal/Compliance Team  
**Review Cycle**: Annual or when FSF updates licenses  
**Last Updated**: 2026-01-16  
**Next Review**: 2027-01-16

## Change History

| Date | Change | Reason | Author |
|------|--------|--------|--------|
| 2026-01-16 | Initial creation with GPL-3.0 | Establish authoritative license source | GitHub Copilot |

## Contact

For questions about license selection or compliance:
- **Email**: legal@mokoconsulting.tech
- **Documentation**: See [License Compliance Policy](../../docs/policy/license-compliance.md)
- **Issues**: Open an issue in MokoStandards repository
