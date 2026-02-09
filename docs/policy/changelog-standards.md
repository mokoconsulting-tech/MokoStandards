<!--
 Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

 This file is part of a Moko Consulting project.

 SPDX-License-Identifier: GPL-3.0-or-later

 # FILE INFORMATION
 DEFGROUP: MokoStandards
 INGROUP: Policy.Documentation
 REPO: https://github.com/mokoconsulting-tech/MokoStandards
 PATH: /docs/policy/changelog-standards.md
 VERSION: 03.01.02
 BRIEF: Policy defining changelog format and maintenance standards for MokoStandards repositories.
-->

# MokoStandards: Changelog Standards Policy

## Purpose

This policy defines the standard format and maintenance requirements for CHANGELOG.md files across all MokoStandards repositories.

## Standard Format

### H1 Header Format

**Required Format:**
```markdown
# CHANGELOG - RepositoryName (VERSION: XX.YY.ZZ)
```

**Example:**
```markdown
# CHANGELOG - MokoStandards (VERSION: 03.01.02)
```

**Rules:**
- H1 must start with "CHANGELOG - " followed by repository name and current version
- Format: `# CHANGELOG - RepositoryName (VERSION: XX.YY.ZZ)`
- Version must match the latest released version in the changelog
- This is the standard header for all MokoStandards repository changelogs

### Required Sections

1. **Metadata Section** (after H1):
   ```markdown
   All notable changes to this project will be documented in this file.

   The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
   and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
   ```

2. **[Unreleased] Section** (H2):
   ```markdown
   ## [Unreleased]
   ```
   - Must use exact format: `## [Unreleased]` (note lowercase 'nreleased')
   - Must be present even if empty
   - Contains changes not yet released

3. **Version Sections** (H2):
   ```markdown
   ## [XX.YY.ZZ] - YYYY-MM-DD
   ```
   - Each released version as H2
   - Format: `## [Version] - Date`
   - Dates in ISO 8601 format (YYYY-MM-DD)

### Category Organization

Within each version section, changes are organized by category using H3:

```markdown
### Added
- New features

### Changed
- Changes to existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security-related changes
```

**Categories** (in order of preference):
1. **Added** - New features
2. **Changed** - Changes to existing functionality
3. **Deprecated** - Soon-to-be removed features
4. **Removed** - Removed features
5. **Fixed** - Bug fixes
6. **Security** - Security-related changes

## Complete Example

```markdown
# CHANGELOG - MokoStandards (VERSION: 03.01.02)

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Updated README with new examples

### Fixed
- Corrected typo in documentation

## [03.01.00] - 2026-01-28

### Added
- New validation scripts
- PowerShell GUI utilities

### Changed
- Reorganized scripts directory structure
- Updated documentation format

### Fixed
- Tab policy enforcement
- Version number consistency

## [03.00.00] - 2026-01-15

### Added
- Initial release of MokoStandards
- Core policy documents
- Validation scripts
```

## Automation Tools

### Scripts

- **scripts/maintenance/update_changelog.py**: Add entries to [Unreleased] section
- **.github/workflows/auto-update-changelog.yml**: Automated changelog maintenance
- **.github/workflows/standards-compliance.yml**: Validates changelog format

### Validation

The standards compliance workflow checks:
- Presence of `## [Unreleased]` section (exact format)
- Valid Keep a Changelog format
- Version numbers in releases
- Date formats

## Compliance Requirements

### Required Elements

✅ H1 with `# CHANGELOG - RepositoryName (VERSION: X.Y.Z)` format
✅ Keep a Changelog reference
✅ `## [Unreleased]` section (case-sensitive)
✅ Version sections as H2
✅ Categories as H3
✅ ISO 8601 dates

### Prohibited Elements

❌ Generic "# Changelog" or "# CHANGELOG" headers without repo name and version
❌ `## [UNRELEASED]` (all caps)
❌ `## UNRELEASED` (no brackets)
❌ Missing [Unreleased] section
❌ Non-standard date formats
❌ Version numbers as H1
❌ Missing "CHANGELOG - " prefix in H1

## Maintenance Workflow

### Adding Changes

1. All changes go to `## [Unreleased]` first
2. Categorize using appropriate H3 section
3. Use bullet points for individual changes
4. Be descriptive but concise

### Creating Releases

1. Move [Unreleased] changes to new version section
2. Update H1 with new version number
3. Add release date
4. Create new empty [Unreleased] section
5. Commit with message: `chore: Release version X.Y.Z`

### Tools Usage

```bash
# Add a change to [Unreleased]
python3 scripts/maintenance/update_changelog.py --category Changed --message "Updated script organization"

# Validate changelog format
# (runs automatically in CI)
```

## References

- [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
- [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
- [MokoStandards Documentation Standards](./documentation-governance.md)

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Policy                                       |
| Domain         | Documentation                                         |
| Applies To     | All MokoStandards Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/MokoStandards                                      |
| Path           | /docs/policy/changelog-standards.md                                      |
| Version        | 03.01.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-29                                  |
| Reviewed By    | Documentation Team                                    |

## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-29 | Moko Consulting | Created changelog standards policy   | Established H1 format with repo name + version |
