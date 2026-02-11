# Version Badge Documentation

**Document Type**: Guide  
**Version**: 03.02.00  
**Last Updated**: 2026-02-11  
**Status**: Active

## Overview

This document provides guidance for adding MokoStandards version compliance badges to repository documentation. Version badges provide at-a-glance visibility into which version of MokoStandards a repository complies with.

## Purpose

Version badges serve to:

1. **Show Compliance**: Clearly indicate MokoStandards version compliance
2. **Track Updates**: Show when repositories were last updated to standards
3. **Enable Monitoring**: Allow automated tracking of standards adoption
4. **Provide Context**: Help users understand documentation currency
5. **Encourage Updates**: Create visibility for outdated repositories

## Badge Format

### Standard Badge

```markdown
![MokoStandards](https://img.shields.io/badge/MokoStandards-03.02.00-blue)
```

**Renders as**: ![MokoStandards](https://img.shields.io/badge/MokoStandards-03.02.00-blue)

### Badge with Link

```markdown
[![MokoStandards](https://img.shields.io/badge/MokoStandards-03.02.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)
```

**Renders as**: [![MokoStandards](https://img.shields.io/badge/MokoStandards-03.02.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

### Badge Parameters

**shields.io format**: `https://img.shields.io/badge/{LABEL}-{VERSION}-{COLOR}`

- **LABEL**: `MokoStandards` (fixed)
- **VERSION**: Current version (e.g., `03.02.00`)
- **COLOR**: 
  - `blue` - Current version (compliant)
  - `green` - Recent version (1-2 versions behind)
  - `yellow` - Older version (3-4 versions behind)
  - `orange` - Outdated (5+ versions behind)
  - `red` - Non-compliant or unknown

## Placement Requirements

### Required in README.md

**Location**: Near the top of README.md, typically in badges section

**Position**: After status badges (build, tests), before description

**Example**:
```markdown
# ProjectName

![Build](https://img.shields.io/badge/build-passing-brightgreen)
![Tests](https://img.shields.io/badge/tests-100%25-brightgreen)
[![MokoStandards](https://img.shields.io/badge/MokoStandards-03.02.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

## Description
This project...
```

### Recommended in Other Documentation

- **CONTRIBUTING.md**: Show standards for contributors
- **docs/index.md**: Main documentation index
- **docs/README.md**: Documentation overview

## Version Badge Requirements

### For All Repositories

All organization repositories MUST include:

1. **Version badge in README.md**
   - Location: Badges section near top
   - Format: MokoStandards badge with version
   - Link: To MokoStandards repository

2. **Current version number**
   - Must match actual compliance level
   - Update when adopting new standards
   - Reflect major.minor.patch accurately

3. **Badge accessibility**
   - Alt text included
   - Link functional
   - Image loads correctly

### Version Determination

**How to determine your repository's MokoStandards version**:

1. Check when repository last updated to standards
2. Review CHANGELOG or commit history
3. Verify against MokoStandards features:
   - 03.00.00: Basic structure and policies
   - 03.01.00: Enhanced automation scripts
   - 03.02.00: Enterprise libraries and frameworks
4. Use the version of standards actually implemented

**Note**: Not all features required - use version of standards you comply with

## Automation

### Automated Version Detection

**Script**: `scripts/validate/check_standards_compliance.py`

Checks:
- Badge exists in README.md
- Version format correct (XX.YY.ZZ)
- Badge reachable
- Version reasonably current

### Bulk Update Script

**Script**: `scripts/automation/update_version_badges.py`

Updates all repository badges to specified version:

```bash
# Update single repository
./scripts/automation/update_version_badges.py --repo myrepo --version 03.02.00

# Update all org repositories
./scripts/automation/update_version_badges.py --org mokoconsulting-tech --version 03.02.00
```

### CI/CD Integration

**GitHub Actions workflow** (`.github/workflows/standards-check.yml`):

```yaml
name: Standards Compliance Check

on: [push, pull_request]

jobs:
  check-compliance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check MokoStandards Badge
        run: |
          if ! grep -q "img.shields.io/badge/MokoStandards" README.md; then
            echo "ERROR: MokoStandards badge missing from README.md"
            exit 1
          fi
          
      - name: Validate Badge Version
        run: |
          VERSION=$(grep -oP 'MokoStandards-\K[0-9]+\.[0-9]+\.[0-9]+' README.md | head -1)
          if [ -z "$VERSION" ]; then
            echo "ERROR: Could not extract version from badge"
            exit 1
          fi
          echo "Found MokoStandards version: $VERSION"
```

## Version Badge Examples

### Current Compliance (Blue)

```markdown
[![MokoStandards](https://img.shields.io/badge/MokoStandards-03.02.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)
```
Use when: Compliant with current MokoStandards version

### Recent Version (Green)

```markdown
[![MokoStandards](https://img.shields.io/badge/MokoStandards-03.01.05-green)](https://github.com/mokoconsulting-tech/MokoStandards)
```
Use when: 1-2 versions behind, still acceptable

### Older Version (Yellow)

```markdown
[![MokoStandards](https://img.shields.io/badge/MokoStandards-03.00.05-yellow)](https://github.com/mokoconsulting-tech/MokoStandards)
```
Use when: 3-4 versions behind, needs update soon

### Outdated (Orange)

```markdown
[![MokoStandards](https://img.shields.io/badge/MokoStandards-02.05.00-orange)](https://github.com/mokoconsulting-tech/MokoStandards)
```
Use when: 5+ versions behind, priority update needed

### Non-compliant (Red)

```markdown
[![MokoStandards](https://img.shields.io/badge/MokoStandards-unknown-red)](https://github.com/mokoconsulting-tech/MokoStandards)
```
Use when: Version unknown or not yet compliant

## Additional Badge Variants

### With Status

```markdown
[![MokoStandards](https://img.shields.io/badge/MokoStandards-03.02.00%20%7C%20compliant-blue)](https://github.com/mokoconsulting-tech/MokoStandards)
```

### With Date

```markdown
[![MokoStandards](https://img.shields.io/badge/MokoStandards-03.02.00%20(2026--02)-blue)](https://github.com/mokoconsulting-tech/MokoStandards)
```

### Custom Style

```markdown
![MokoStandards](https://img.shields.io/badge/MokoStandards-03.02.00-blue?style=flat-square)
```

Styles: `flat`, `flat-square`, `plastic`, `for-the-badge`, `social`

## Maintenance

### When to Update Badge

Update the version badge when:

1. **Standards Updated**: New MokoStandards version adopted
2. **Major Changes**: Repository structure updated to new standards
3. **Features Added**: New MokoStandards features implemented
4. **Quarterly Review**: Regular compliance check completed

### Automated Updates

Use bulk update script for organization-wide updates:

```bash
# After new MokoStandards release
./scripts/automation/update_version_badges.py \
  --org mokoconsulting-tech \
  --version 03.03.00 \
  --filter compliant
```

### Manual Updates

For individual repositories:

1. Edit README.md
2. Find badge line
3. Update version number: `03.01.05` → `03.02.00`
4. Adjust color if needed
5. Commit and push

## Validation

### Badge Validation Checklist

- [ ] Badge exists in README.md
- [ ] Badge near top of file (in badges section)
- [ ] Version format correct (XX.YY.ZZ)
- [ ] Badge includes link to MokoStandards
- [ ] Image loads correctly
- [ ] Alt text present
- [ ] Version matches actual compliance
- [ ] Color appropriate for version age

### Automated Validation

Run validation script:

```bash
./scripts/validate/check_standards_compliance.py --repo .
```

Expected output:
```
✅ MokoStandards badge found
✅ Version format valid: 03.02.00
✅ Badge link functional
✅ Version current (within 1 release)
```

## Badge Statistics

### Organization Dashboard

Track badge compliance across organization:

- Total repositories: 25
- With badges: 22 (88%)
- Current version (03.02.00): 15 (60%)
- Recent version (03.01.xx): 5 (20%)
- Outdated: 2 (8%)
- Missing badge: 3 (12%)

**Dashboard URL**: `https://github.com/mokoconsulting-tech/standards-dashboard`

## Benefits

### For Repository Maintainers

- ✅ Shows commitment to standards
- ✅ Tracks compliance status
- ✅ Reminds when updates needed
- ✅ Professional appearance

### For Repository Users

- ✅ Understands standards compliance
- ✅ Knows documentation currency
- ✅ Can check standards reference
- ✅ Trusts quality level

### For Organization

- ✅ Tracks standards adoption
- ✅ Identifies outdated repos
- ✅ Measures compliance progress
- ✅ Prioritizes updates

## Troubleshooting

### Badge Not Rendering

**Problem**: Badge shows as broken image  
**Solution**: Check URL syntax, ensure no typos in shields.io URL

### Version Appears Incorrect

**Problem**: Badge shows old version  
**Solution**: Clear browser cache or use private/incognito mode

### Link Not Working

**Problem**: Clicking badge doesn't go to MokoStandards  
**Solution**: Verify link format: `[![...](badge-url)](link-url)`

### CI Check Failing

**Problem**: Standards check fails in CI  
**Solution**: Ensure badge in README.md, format correct, version extractable

## Related Documentation

- **[README Standards](../policy/readme-standards.md)** - README.md requirements
- **[Standards Compliance](../policy/standards-compliance.md)** - Compliance checking
- **[Version Planning](../../ROADMAP.md)** - MokoStandards versions
- **[CHANGELOG](../../CHANGELOG.md)** - Version history

## Examples from Organization

### MokoStandards (This Repository)

```markdown
[![MokoStandards](https://img.shields.io/badge/MokoStandards-03.02.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)
```

### Typical Repository

```markdown
# MyProject

![Build](https://img.shields.io/github/workflow/status/mokoconsulting-tech/myproject/CI)
![License](https://img.shields.io/badge/license-GPL--3.0-blue)
[![MokoStandards](https://img.shields.io/badge/MokoStandards-03.02.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

Modern web application following MokoStandards...
```

## Quick Reference

### Badge Template

```markdown
[![MokoStandards](https://img.shields.io/badge/MokoStandards-{VERSION}-{COLOR})](https://github.com/mokoconsulting-tech/MokoStandards)
```

### Common Versions

- Current: `03.02.00` (blue)
- Previous: `03.01.05` (green)
- Older: `03.00.xx` (yellow)

### Update Command

```bash
# Update badge in README.md
sed -i 's/MokoStandards-[0-9.]*-/MokoStandards-03.02.00-/' README.md
```

## Metadata

| Field | Value |
|-------|-------|
| Document Type | Guide |
| Domain | Documentation Standards |
| Applies To | All Repositories |
| Owner | Documentation Team |
| Path | docs/guides/version-badge-guide.md |
| Version | 03.02.00 |
| Status | Active |
| Last Reviewed | 2026-02-11 |

---

**Current MokoStandards Version**: 03.02.00  
**Badge Generation**: https://shields.io/  
**Validation Script**: `scripts/validate/check_standards_compliance.py`
