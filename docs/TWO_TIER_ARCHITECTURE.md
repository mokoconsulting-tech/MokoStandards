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
PATH: /docs/TWO_TIER_ARCHITECTURE.md
VERSION: 01.00.00
BRIEF: Two-tier architecture documentation for public standards and private enforcement
-->

# Two-Tier Architecture

## Overview

Moko Consulting implements a **two-tier repository architecture** that separates public coding standards from private organizational enforcement. This architecture enables open-source collaboration while protecting sensitive organizational policies and automation.

### Architecture Components

**Tier 1: `.github-private` - Private Enforcement Layer**
- **Purpose**: Private repository for organizational policies and enforcement
- **Location**: `mokoconsulting-tech/.github-private` (internal access only)
- **Visibility**: Organization members only
- **Content**: Proprietary workflows, internal automation, access control policies

**Tier 2: `MokoStandards` - Public Standards Layer**
- **Purpose**: Public repository for coding standards and templates
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

## Related Documentation

- [Repository Standards Application](REPOSITORY_STANDARDS_APPLICATION.md) - How to apply standards from MokoStandards
- [Standards Coordination](../STANDARDS_COORDINATION.md) - Coordination between public and private tiers
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

| Field      | Value                                                                                                        |
| ---------- | ------------------------------------------------------------------------------------------------------------ |
| Document   | Two-Tier Architecture                                                                                        |
| Path       | /docs/TWO_TIER_ARCHITECTURE.md                                                                               |
| Repository | [https://github.com/mokoconsulting-tech/MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards) |
| Owner      | Moko Consulting                                                                                              |
| Scope      | Architecture documentation                                                                                   |
| Status     | Published                                                                                                    |
| Effective  | 2026-01-17                                                                                                   |

## Revision History

| Date       | Change Description                                      | Author          |
| ---------- | ------------------------------------------------------- | --------------- |
| 2026-01-17 | Initial creation, two-tier architecture documentation   | Moko Consulting |
