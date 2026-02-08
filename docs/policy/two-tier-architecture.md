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
INGROUP: MokoStandards.Architecture
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/policy/two-tier-architecture.md
VERSION: 03.01.01
BRIEF: Two-tier architecture documentation for public standards and private enforcement
-->

# Two-Tier Architecture

## Overview

Moko Consulting implements a **two-tier repository architecture** that separates public coding standards from private organizational enforcement. This architecture enables open-source collaboration while protecting sensitive organizational policies and automation.

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                 TWO-TIER ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Tier 1: .github-private (PRIVATE)                         │
│  ├─ Organization-internal policies and procedures          │
│  ├─ Proprietary workflows with secrets and credentials     │
│  ├─ Sensitive deployment scripts and automation            │
│  ├─ Enterprise compliance and audit frameworks             │
│  ├─ Internal access control policies                       │
│  └─ Calls reusable workflows from MokoStandards (Tier 2) → │
│                                                             │
│  Tier 2: MokoStandards (PUBLIC - SOURCE OF TRUTH)          │
│  ├─ Open-source best practices and coding standards        │
│  ├─ Community-shareable templates and workflows            │
│  ├─ Generic CI/CD patterns (reusable workflows)            │
│  ├─ Platform-specific standards (Joomla, Dolibarr)         │
│  ├─ Public contribution guidelines                         │
│  └─ Schema definitions and Terraform configurations        │
│                                                             │
│  Organization Repositories                                 │
│  └─ Inherit from appropriate tier based on type            │
│     ├─ Public projects → Use Tier 2 (MokoStandards)       │
│     └─ Private projects → Use Tier 1 (.github-private)    │
└─────────────────────────────────────────────────────────────┘
```

### Architecture Components

**Tier 1: `.github-private` - Private Enforcement Layer**
- **Purpose**: Private repository for organizational policies and enforcement
- **Authority**: Highest for internal/private projects
- **Location**: `mokoconsulting-tech/.github-private` (internal access only)
- **Visibility**: Organization members only
- **Content**: Proprietary workflows, internal automation, access control policies

**Tier 2: `MokoStandards` - Public Standards Layer**
- **Purpose**: Public repository for coding standards and templates (SOURCE OF TRUTH)
- **Authority**: Highest for public/open-source projects
- **Location**: `mokoconsulting-tech/MokoStandards` (publicly accessible)
- **Visibility**: Open source community
- **Content**: Coding standards, quality guidelines, public templates, documentation

## Tier 1: .github-private Repository

### Purpose and Scope

The `.github-private` repository serves as the organization's **private enforcement and policy layer**. It contains sensitive automation and proprietary processes that should not be publicly disclosed.

### What Belongs in .github-private

#### 1. Organization-Wide Workflow Enforcement
```yaml
# Example: Mandatory security scanning for all repositories
.github/workflows/
  ├── enforce-security-scan.yml          # Mandatory vulnerability scanning
  ├── enforce-branch-protection.yml      # Branch protection enforcement
  ├── enforce-code-review.yml            # Required review policies
  └── enforce-deployment-approval.yml    # Deployment approval workflows
```

#### 2. Access Control and Team Management
- CODEOWNERS definitions with internal team references
- Team-specific automation scripts
- Internal approval matrices
- Role-based access control configurations

#### 3. Proprietary Deployment Automation
```yaml
# Example: Internal deployment pipeline
.github/workflows/
  ├── deploy-to-production.yml           # Production deployment with secrets
  ├── deploy-to-staging.yml              # Staging environment deployment
  └── rollback-automation.yml            # Automated rollback procedures
```

#### 4. Internal Project Automation
- GitHub Projects automation with internal field mappings
- Custom issue templates with internal team references
- Proprietary AI prompts and Copilot configurations
- Internal documentation generation scripts

#### 5. Sensitive Configuration
- Organization-specific environment variables
- Internal API endpoints and service configurations
- Proprietary integration credentials (encrypted)
- Internal monitoring and alerting configurations

### When to Use .github-private

Use the `.github-private` repository when content includes:

✅ **Internal team structure** (team names, member assignments)
✅ **Proprietary automation** (custom deployment pipelines)
✅ **Access control policies** (who can approve, merge, deploy)
✅ **Sensitive integrations** (internal services, proprietary APIs)
✅ **Organization-specific workflows** (unique to your business)
✅ **Confidential project references** (internal project numbers, names)

### Configuration Example: .github-private

```yaml
# .github-private/.github/workflows/enforce-standards.yml
name: Enforce Organization Standards

on:
  workflow_call:
    inputs:
      repository:
        required: true
        type: string

jobs:
  enforce:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      checks: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          repository: ${{ inputs.repository }}

      - name: Apply mandatory security scanning
        uses: mokoconsulting-tech/.github-private/.github/actions/security-scan@main
        with:
          scan-level: mandatory

      - name: Validate branch protection
        run: |
          # Internal script that checks branch protection rules
          python3 .github-private/scripts/validate-branch-protection.py

      - name: Notify compliance team
        if: failure()
        uses: mokoconsulting-tech/.github-private/.github/actions/notify-compliance@main
        with:
          team: compliance
          severity: high
```

## Tier 2: MokoStandards Repository

### Purpose and Scope

The `MokoStandards` repository serves as the organization's **public standards and guidelines repository**. It provides reusable coding standards, templates, and best practices that can be shared with the open-source community.

⚠️ **CRITICAL: Source of Truth**

**MokoStandards is the SOURCE OF TRUTH** for:
- All schema definitions (repository structure, metadata formats)
- Terraform configurations and infrastructure standards
- Validation logic and compliance rules
- Coding standards and best practices

The `.github-private` repository and all organization repositories are **CONSUMERS** of these standards. They extend (not duplicate) definitions with organization-specific customizations only.

### What Belongs in MokoStandards

#### 1. Coding Standards and Guidelines
```
docs/policy/
  ├── security-scanning-standard.md      # Security scanning requirements
  ├── dependency-management-standard.md  # Dependency update policies
  ├── scripting-standards.md             # Script development standards
  └── file-header-standard.md            # File header requirements
```

#### 2. Reusable Workflow Templates
```yaml
# Example: Generic quality check workflow
.github/workflows/
  ├── reusable-ci-validation.yml         # CI validation template
  ├── reusable-php-quality.yml           # PHP quality checks
  ├── reusable-joomla-testing.yml        # Joomla extension testing
  └── reusable-release.yml               # Release automation template
```

#### 3. Platform-Specific Standards
```
docs/policy/
  ├── joomla-development-standard.md     # Joomla-specific guidelines
  ├── dolibarr-module-standard.md        # Dolibarr module standards
  └── generic-php-standard.md            # Generic PHP standards
```

#### 4. Quality Validation Scripts
```
scripts/
  ├── validate_file_headers.py           # File header validation
  ├── check_documentation.py             # Documentation completeness check
  └── lint_workflows.py                  # Workflow file linting
```

#### 5. Public Documentation
- Architecture decision records (ADRs)
- Development guides and tutorials
- Onboarding documentation
- Community contribution guidelines

### When to Use MokoStandards

Use the `MokoStandards` repository when content is:

✅ **General coding standards** (applicable across projects)
✅ **Reusable workflow templates** (no secrets or internal references)
✅ **Public documentation** (safe for community consumption)
✅ **Quality validation tools** (generic, non-proprietary)
✅ **Platform-specific guidelines** (Joomla, Dolibarr, PHP best practices)
✅ **Open-source templates** (issue templates, PR templates without internal teams)

### Configuration Example: MokoStandards

```yaml
# MokoStandards/.github/workflows/reusable-ci-validation.yml
name: Reusable CI Validation

on:
  workflow_call:
    inputs:
      profile:
        description: 'Validation profile (minimal, standard, full)'
        required: false
        type: string
        default: 'standard'

jobs:
  validate:
    runs-on: ubuntu-latest
    permissions:
      contents: read

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run file header validation
        run: python3 scripts/validate_file_headers.py

      - name: Check documentation completeness
        run: python3 scripts/check_documentation.py

      - name: Lint workflow files
        if: inputs.profile == 'full'
        run: python3 scripts/lint_workflows.py

      - name: Run security baseline scan
        run: |
          # Generic security checks (no secrets)
          npm audit --production
```

## Decision Matrix: Which Tier?

| Content Type | .github-private (Tier 1) | MokoStandards (Tier 2) |
|--------------|--------------------------|------------------------|
| Coding standards | ❌ | ✅ |
| Team member names | ✅ | ❌ |
| Reusable workflows (generic) | ❌ | ✅ |
| Deployment workflows (with secrets) | ✅ | ❌ |
| CODEOWNERS file | ✅ | ❌ |
| File header validation script | ❌ | ✅ |
| Internal project automation | ✅ | ❌ |
| Security scanning standard | ❌ | ✅ |
| Access control policies | ✅ | ❌ |
| Platform-specific guidelines | ❌ | ✅ |
| AI prompts (internal) | ✅ | ❌ |
| Public documentation | ❌ | ✅ |

## Integration Between Tiers

### How Repositories Use Both Tiers

Individual project repositories can reference both tiers based on their needs:

```yaml
# project-repo/.github/workflows/ci.yml
name: Project CI Pipeline

on:
  push:
    branches: [main, dev/**]
  pull_request:
    branches: [main]

jobs:
  # Use public standards from MokoStandards
  quality-check:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      profile: full

  # Use private enforcement from .github-private
  security-enforcement:
    needs: quality-check
    uses: mokoconsulting-tech/.github-private/.github/workflows/enforce-security.yml@main
    secrets: inherit
```

### Standards Application Workflow

1. **Public repositories** use MokoStandards for:
   - Coding quality standards
   - Documentation templates
   - Generic CI/CD validation

2. **Internal repositories** use both:
   - MokoStandards for quality standards
   - .github-private for enforcement and deployment

3. **External contributors** interact with:
   - MokoStandards only (public-facing)
   - No access to .github-private

### Coordination Process

#### Updating Public Standards (MokoStandards)
```bash
# 1. Update coding standard in MokoStandards
git clone https://github.com/mokoconsulting-tech/MokoStandards.git
cd MokoStandards
git checkout -b update/php-standard
# ... make changes ...
git commit -m "docs: update PHP coding standard"
git push origin update/php-standard
# ... create PR, review, merge ...
```

#### Updating Private Enforcement (.github-private)
```bash
# 2. Update enforcement workflow to use new standard
git clone https://github.com/mokoconsulting-tech/.github-private.git
cd .github-private
git checkout -b update/php-enforcement
# ... update workflow to reference updated standard ...
git commit -m "feat: enforce updated PHP standard"
git push origin update/php-enforcement
# ... create PR, review, merge ...
```

## Repository Structure Comparison

### .github-private Structure
```
.github-private/
├── .github/
│   ├── workflows/
│   │   ├── enforce-security-scan.yml
│   │   ├── enforce-branch-protection.yml
│   │   └── deploy-to-production.yml
│   ├── actions/
│   │   ├── security-scan/
│   │   ├── notify-compliance/
│   │   └── deploy-internal/
│   └── CODEOWNERS
├── scripts/
│   ├── project-automation/
│   │   ├── setup_project.py
│   │   └── populate_project.py
│   └── deployment/
│       └── deploy_internal.sh
└── docs/
    └── internal/
        ├── deployment-procedures.md
        └── access-control-policy.md
```

### MokoStandards Structure
```
MokoStandards/
├── .github/
│   └── workflows/
│       ├── reusable-ci-validation.yml
│       ├── reusable-php-quality.yml
│       └── reusable-release.yml
├── scripts/
│   ├── validate_file_headers.py
│   ├── check_documentation.py
│   └── lint_workflows.py
├── docs/
│   ├── policy/
│   │   ├── security-scanning-standard.md
│   │   └── joomla-development-standard.md
│   └── guide/
│       ├── onboarding.md
│       └── contributing.md
└── templates/
    ├── .github/
    │   ├── ISSUE_TEMPLATE/
    │   └── PULL_REQUEST_TEMPLATE.md
    └── project-templates/
```

## Best Practices

### For .github-private

1. **Never reference internal teams in commit messages** that might be synchronized
2. **Encrypt all secrets** using GitHub encrypted secrets
3. **Document internal procedures** in private docs folder
4. **Regular access audits** of who has repository access
5. **Use workflow dispatch** for sensitive automation requiring approval

### For MokoStandards

1. **No organization-specific references** in any files
2. **Generic examples only** - parameterize organization-specific values
3. **Public-safe documentation** - assume public scrutiny
4. **Community-friendly** - accept external contributions
5. **Clear separation** - reference private tier only in architecture docs

### Common Pitfalls to Avoid

❌ **Don't** put team names in MokoStandards
❌ **Don't** reference internal project numbers in public docs
❌ **Don't** include secrets or credentials in either repository
❌ **Don't** hard-code organization-specific URLs in MokoStandards
❌ **Don't** duplicate standards between tiers - keep single source of truth

✅ **Do** parameterize organization-specific values
✅ **Do** use workflow variables for configuration
✅ **Do** document the relationship between tiers
✅ **Do** keep standards in MokoStandards, enforcement in .github-private
✅ **Do** review PRs for confidentiality before merging

## Migration Guidelines

### Moving Content from MokoStandards to .github-private

If you discover content in MokoStandards that should be private:

1. **Identify the content** requiring confidentiality
2. **Create equivalent file** in .github-private
3. **Update references** in project repositories
4. **Remove from MokoStandards** after migration complete
5. **Document the move** in PRIVATE_REPOSITORY_REFERENCE.md

### Moving Content from .github-private to MokoStandards

To open-source previously private content:

1. **Review for confidentiality** - ensure no sensitive data
2. **Generalize examples** - remove organization-specific references
3. **Create in MokoStandards** with public-safe content
4. **Update internal workflows** to reference new public location
5. **Deprecate private version** after transition period

## Support and Maintenance

### For Internal Users

**Repository**: Access via organization membership
**Support**: Contact `dev@mokoconsulting.tech`
**Documentation**: See both repositories for complete picture

### For External Users

**Repository**: Public access to MokoStandards
**Support**: Open issues in MokoStandards repository
**Documentation**: All public docs in MokoStandards

### Maintenance Responsibilities

| Responsibility | Tier 1 (.github-private) | Tier 2 (MokoStandards) |
|----------------|--------------------------|------------------------|
| Code owners | Internal maintainers team | Public maintainers + community |
| PR approval | Internal team only | Public review process |
| Release cadence | As needed (internal) | Versioned releases |
| Documentation | Internal wiki + repo | Public documentation |
| Issue tracking | Private issue tracker | Public issues |

## Standards Coordination and Update Process

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

- [Repository Standards Application](../guide/repository-standards-application.md) - How to apply standards from MokoStandards
- [Private Repository Reference](guide/PRIVATE_REPOSITORY_REFERENCE.md) - Reference to private content
- [Repository Split Plan](guide/repository-split-plan.md) - Technical implementation details

## Frequently Asked Questions

### Q: Can external contributors access .github-private?
**A:** No, `.github-private` is restricted to organization members only.

### Q: Should I reference .github-private in public documentation?
**A:** Only in architecture documentation explaining the relationship. Never include specific internal details.

### Q: How do I know if content belongs in Tier 1 or Tier 2?
**A:** Use the decision matrix above. If unsure, default to private and migrate to public later if appropriate.

### Q: Can I use MokoStandards workflows without .github-private?
**A:** Yes! MokoStandards workflows are fully functional standalone public templates.

### Q: What if I accidentally commit sensitive data to MokoStandards?
**A:** Immediately contact repository administrators. Use `git filter-repo` to remove from history. Rotate any exposed credentials.

---

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Policy                                       |
| Domain         | Governance                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/policy/two-tier-architecture.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
