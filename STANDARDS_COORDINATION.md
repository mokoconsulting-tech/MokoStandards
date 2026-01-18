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
DEFGROUP: MokoStandards.Documentation
INGROUP: MokoStandards.Coordination
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /STANDARDS_COORDINATION.md
VERSION: 01.00.00
BRIEF: Coordination between public standards and private enforcement
-->

# Standards Coordination

## Overview

This document explains how Moko Consulting coordinates between **public coding standards** (MokoStandards repository) and **private organizational enforcement** (internal repositories). The coordination ensures consistent quality across all projects while protecting sensitive organizational policies.

## Architecture Overview

Moko Consulting uses a two-tier repository architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                    Organization                             │
│                                                             │
│  ┌───────────────────┐         ┌──────────────────────┐   │
│  │  MokoStandards    │         │  .github-private     │   │
│  │  (Public Tier)    │◄────────┤  (Private Tier)      │   │
│  │                   │  refs   │                      │   │
│  │  • Standards      │         │  • Enforcement       │   │
│  │  • Templates      │         │  • Automation        │   │
│  │  • Guidelines     │         │  • Access Control    │   │
│  └─────────┬─────────┘         └──────────┬───────────┘   │
│            │                               │               │
│            └───────────┬───────────────────┘               │
│                        │                                   │
│              ┌─────────▼──────────┐                        │
│              │  Project Repos     │                        │
│              │  • Use standards   │                        │
│              │  • Apply workflows │                        │
│              └────────────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

### Tier 1: MokoStandards (Public Standards Repository)

**Purpose**: Provide reusable, open-source coding standards and quality guidelines

**Contents**:
- Coding style guidelines (PSR-12, Joomla, Dolibarr)
- Reusable workflow templates
- Quality validation scripts
- Platform-specific development standards
- Public documentation and guides

**Visibility**: Open source, public GitHub repository

**Access**: Anyone can view, fork, and contribute

### Tier 2: Private Enforcement (Internal Repositories)

**Purpose**: Implement organizational policies and automated enforcement

**Contents**:
- Mandatory workflow enforcement
- Access control policies (CODEOWNERS)
- Internal automation scripts
- Proprietary deployment pipelines
- Organization-specific configurations

**Visibility**: Private, organization-only repositories

**Access**: Restricted to organization members

## How Repositories Use Standards

### Public Repository Usage

Public repositories can adopt MokoStandards independently:

```yaml
# public-project/.github/workflows/ci.yml
name: CI Pipeline

on: [push, pull_request]

jobs:
  quality-checks:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      profile: standard
```

**Benefits**:
- No organizational affiliation required
- Self-service adoption
- Community-driven improvements
- Open-source best practices

### Internal Repository Usage

Internal repositories use both tiers:

```yaml
# internal-project/.github/workflows/ci.yml
name: Internal CI Pipeline

on: [push, pull_request]

jobs:
  # Public standards from MokoStandards
  quality-checks:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      profile: full
      
  # Private enforcement from .github-private
  security-enforcement:
    needs: quality-checks
    uses: mokoconsulting-tech/.github-private/.github/workflows/enforce-security.yml@main
    secrets: inherit
```

**Benefits**:
- Consistent quality standards
- Organizational policy enforcement
- Automated compliance checks
- Secure deployment automation

## Standards Update Process

### Updating Public Standards (MokoStandards)

#### Process Flow

```
Developer identifies need
        ↓
Create feature branch
        ↓
Update standard/workflow
        ↓
Test changes locally
        ↓
Create pull request
        ↓
Community review
        ↓
Maintainer approval
        ↓
Merge to main branch
        ↓
Version tag release
        ↓
Announce to community
```

#### Step-by-Step Guide

**1. Identify Need for Update**

```bash
# Examples of update triggers:
# - New PHP version support
# - Updated coding standard
# - New platform support
# - Bug fix in workflow
# - Community feature request
```

**2. Create Feature Branch**

```bash
cd MokoStandards
git checkout -b update/php-8-3-support
```

**3. Make Changes**

```bash
# Update relevant files
vim docs/policy/generic-php-standard.md
vim .github/workflows/reusable-php-quality.yml

# Test changes
./scripts/validate_file_headers.py
./scripts/lint_workflows.py .github/workflows/
```

**4. Document Changes**

```bash
# Update CHANGELOG.md
vim CHANGELOG.md

# Add entry:
# ## [Unreleased]
# ### Added
# - Support for PHP 8.3 in quality workflows
```

**5. Create Pull Request**

```bash
git add .
git commit -m "feat: add PHP 8.3 support to quality workflows"
git push origin update/php-8-3-support

# Create PR on GitHub with description:
# - What changed
# - Why it changed
# - How to test
# - Breaking changes (if any)
```

**6. Review Process**

- Automated checks run
- Community members review
- Maintainers provide feedback
- Address review comments
- Approval and merge

**7. Release and Announce**

```bash
# Tag release
git tag -a v1.3.0 -m "Release v1.3.0: PHP 8.3 support"
git push origin v1.3.0

# Create GitHub release with changelog
# Announce in repository discussions
# Update documentation
```

### Updating Private Enforcement

#### Process Flow (Internal Only)

```
Internal need identified
        ↓
Create private branch
        ↓
Update enforcement logic
        ↓
Test with internal repos
        ↓
Create internal PR
        ↓
Internal team review
        ↓
Security review
        ↓
Merge to main
        ↓
Deploy to organization
```

#### Coordination with Public Standards

When private enforcement depends on public standards:

**1. Ensure Public Standard is Updated First**

```bash
# Wait for MokoStandards PR to merge
# Monitor: https://github.com/mokoconsulting-tech/MokoStandards/pulls

# Once merged, note the commit SHA or tag
# Example: v1.3.0
```

**2. Update Private Enforcement to Reference New Version**

```yaml
# .github-private/.github/workflows/enforce-standards.yml
jobs:
  enforce:
    steps:
      - name: Apply public standards
        uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@v1.3.0
        # ^-- Updated to new version
```

**3. Test Enforcement**

```bash
# Test against sample internal repository
# Verify new standard is applied correctly
# Check for breaking changes
```

**4. Roll Out Gradually**

```bash
# Phase 1: Test repository
# Phase 2: Dev repositories
# Phase 3: All repositories
```

## Coordination Scenarios

### Scenario 1: New Coding Standard

**Situation**: Organization adopts stricter PHPStan level

**Coordination Steps**:

1. **Update MokoStandards (Public)**
   ```yaml
   # .github/workflows/reusable-php-quality.yml
   # Change default PHPStan level from 6 to 8
   inputs:
     phpstan-level:
       default: 8  # Was: 6
   ```

2. **Document Change**
   ```markdown
   # docs/policy/generic-php-standard.md
   ## Static Analysis
   Projects must use PHPStan level 8 (previously level 6).
   ```

3. **Create Migration Guide**
   ```markdown
   # docs/guide/phpstan-level-8-migration.md
   Guide for upgrading from level 6 to level 8...
   ```

4. **Update Private Enforcement**
   ```yaml
   # .github-private/.github/workflows/enforce-quality.yml
   # Reference updated MokoStandards version
   uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-php-quality.yml@v2.0.0
   ```

5. **Notify Teams**
   - Internal announcement
   - Migration timeline
   - Support channels

### Scenario 2: New Platform Support

**Situation**: Add support for Laravel framework

**Coordination Steps**:

1. **Create Public Standard**
   ```bash
   # In MokoStandards
   touch docs/policy/laravel-development-standard.md
   touch .github/workflows/reusable-laravel-testing.yml
   ```

2. **Develop Standard**
   ```markdown
   # docs/policy/laravel-development-standard.md
   - Laravel coding conventions
   - Eloquent best practices
   - Testing requirements
   - Package structure
   ```

3. **Create Reusable Workflow**
   ```yaml
   # .github/workflows/reusable-laravel-testing.yml
   name: Laravel Testing
   on:
     workflow_call:
       inputs:
         php-version:
           required: true
           type: string
         laravel-version:
           required: true
           type: string
   ```

4. **Test and Release**
   ```bash
   git tag -a v2.1.0 -m "feat: add Laravel framework support"
   ```

5. **Internal Adoption** (if needed)
   ```yaml
   # .github-private: Create enforcement for Laravel projects
   # Add to organization-wide validation
   ```

### Scenario 3: Security Requirement

**Situation**: New security scanning requirement

**Coordination Steps**:

1. **Update Public Documentation**
   ```markdown
   # docs/policy/security-scanning-standard.md
   ## New Requirement
   All projects must scan for [specific vulnerability type]
   ```

2. **Update Public Workflow Template**
   ```yaml
   # .github/workflows/reusable-ci-validation.yml
   - name: Security scan
     run: |
       # Add new scan command
       composer audit --locked
       npm audit --production
   ```

3. **Create Private Enforcement**
   ```yaml
   # .github-private/.github/workflows/enforce-security.yml
   # Mandatory security checks for all internal repos
   # Fail builds on critical vulnerabilities
   # Notify security team on high vulnerabilities
   ```

4. **Gradual Rollout**
   - Week 1: Warning only
   - Week 2: Blocking for new PRs
   - Week 3: Blocking for all branches

## Community Contribution Guidelines

### For External Contributors

External contributors can improve MokoStandards without organizational access:

#### What You Can Contribute

✅ **Bug fixes** in workflows or scripts
✅ **Documentation improvements**
✅ **New platform support** (e.g., Symfony, WordPress)
✅ **Tool updates** (newer PHP versions, updated tools)
✅ **Best practice suggestions**
✅ **Example configurations**

#### Contribution Process

**1. Fork Repository**
```bash
# Fork on GitHub UI, then clone
git clone https://github.com/YOUR-USERNAME/MokoStandards.git
cd MokoStandards
git remote add upstream https://github.com/mokoconsulting-tech/MokoStandards.git
```

**2. Create Feature Branch**
```bash
git checkout -b feature/add-symfony-support
```

**3. Make Changes**
```bash
# Add your contribution
# Follow existing patterns
# Include documentation
# Add tests if applicable
```

**4. Test Locally**
```bash
# Validate your changes
./scripts/validate_file_headers.py
./scripts/lint_workflows.py .github/workflows/

# Test workflow if possible
```

**5. Submit Pull Request**
```bash
git add .
git commit -m "feat: add Symfony framework support"
git push origin feature/add-symfony-support

# Create PR on GitHub
# Provide clear description
# Link related issues
```

**6. Respond to Review**
- Address feedback promptly
- Ask questions if unclear
- Update based on suggestions
- Maintain respectful communication

#### What Not to Contribute

❌ Organization-specific configurations
❌ Internal team references
❌ Proprietary automation logic
❌ Access control policies
❌ Deployment secrets or credentials

### For Organization Members

Internal members can contribute to both repositories:

#### Contributing to MokoStandards (Public)

Follow the same process as external contributors, ensuring no confidential information is included.

#### Contributing to Private Repositories

Internal contribution process follows organization-specific guidelines (not documented publicly).

## Version Coordination

### MokoStandards Versioning

MokoStandards uses semantic versioning:

```
MAJOR.MINOR.PATCH

Examples:
v1.0.0 - Initial release
v1.1.0 - New feature (Laravel support)
v1.1.1 - Bug fix
v2.0.0 - Breaking change (PHP 8.3 minimum)
```

### Version Pinning Strategy

**Recommended Approaches**:

**1. Pin to Major Version** (Recommended for most projects)
```yaml
uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@v1
# Gets latest v1.x.x, automatic minor/patch updates
```

**2. Pin to Minor Version** (For stability)
```yaml
uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@v1.2
# Gets latest v1.2.x, automatic patch updates
```

**3. Pin to Exact Version** (Maximum stability)
```yaml
uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@v1.2.3
# No automatic updates
```

**4. Use Main Branch** (Latest features, less stable)
```yaml
uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
# Always uses latest, may include breaking changes
```

### Update Strategy

**For Individual Projects**:
```bash
# Review changelog
curl https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/CHANGELOG.md

# Test new version in dev branch
git checkout -b update/mokostandards-v2
# Update workflow version references
# Test thoroughly
# Create PR
```

**For Organization-Wide Updates**:
```bash
# Use .github-private to update all repos
# Coordinate with teams
# Gradual rollout
# Monitor for issues
```

## Monitoring and Feedback

### Feedback Channels

**Public Feedback** (MokoStandards):
- GitHub Issues: Bug reports, feature requests
- GitHub Discussions: Questions, ideas, community support
- Pull Requests: Direct contributions

**Internal Feedback** (Organization):
- Internal issue tracker
- Team channels
- Regular sync meetings

### Metrics and Success

**Public Repository Metrics**:
- Adoption rate (stars, forks, clones)
- Contribution activity (PRs, issues)
- Community engagement (discussions)
- Usage across projects

**Internal Metrics**:
- Policy compliance rate
- Automated enforcement coverage
- Workflow execution success rate
- Time to detect/fix issues

## Troubleshooting Coordination

### Common Issues

#### Issue: Standard Updated But Enforcement Not Applied

**Cause**: Private enforcement still references old version

**Solution**:
```yaml
# Update .github-private workflow version reference
uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@v2.0.0
# ^-- Update to latest version
```

#### Issue: Breaking Change in Standard

**Cause**: Major version update with breaking changes

**Solution**:
1. Review CHANGELOG for breaking changes
2. Update project configurations
3. Test thoroughly before deploying
4. Coordinate rollout with teams
5. Provide migration support

#### Issue: Conflict Between Public Standard and Internal Policy

**Cause**: Organization requires stricter rules than public standard

**Solution**:
```yaml
# Use public standard as baseline
- uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main

# Add additional internal checks
- name: Additional internal checks
  uses: mokoconsulting-tech/.github-private/.github/actions/extra-validation@main
```

## Related Documentation

- [Two-Tier Architecture](docs/TWO_TIER_ARCHITECTURE.md) - Detailed architecture explanation
- [Repository Standards Application](docs/REPOSITORY_STANDARDS_APPLICATION.md) - How to apply standards
- [Contributing Guidelines](CONTRIBUTING.md) - How to contribute to MokoStandards
- [Private Repository Reference](docs/guide/PRIVATE_REPOSITORY_REFERENCE.md) - Reference to private content

## Support

### For Public Users

**Questions**: Open an issue in MokoStandards repository
**Bugs**: Report via GitHub Issues
**Feature Requests**: Submit via GitHub Issues or Discussions

### For Organization Members

**Internal Questions**: Contact via internal channels
**Access Issues**: Contact repository administrators
**Coordination Questions**: Reach out to standards team

---

## Metadata

| Field      | Value                                                                                                        |
| ---------- | ------------------------------------------------------------------------------------------------------------ |
| Document   | Standards Coordination                                                                                       |
| Path       | /STANDARDS_COORDINATION.md                                                                                   |
| Repository | [https://github.com/mokoconsulting-tech/MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards) |
| Owner      | Moko Consulting                                                                                              |
| Scope      | Coordination documentation                                                                                   |
| Status     | Published                                                                                                    |
| Effective  | 2026-01-17                                                                                                   |

## Revision History

| Date       | Change Description                                      | Author          |
| ---------- | ------------------------------------------------------- | --------------- |
| 2026-01-17 | Initial creation, standards coordination documentation  | Moko Consulting |
