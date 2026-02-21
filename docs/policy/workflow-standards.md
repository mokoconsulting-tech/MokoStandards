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
INGROUP: MokoStandards.Workflows
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/policy/workflow-standards.md
VERSION: 04.00.03
BRIEF: Workflow governance and standards for GitHub Actions
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.03-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Workflow Standards Policy

## Purpose

This policy establishes mandatory standards for GitHub Actions workflows across all Moko Consulting repositories. It defines workflow architecture patterns, reusability requirements, security practices, and governance processes to ensure consistent, secure, and maintainable CI/CD automation.

## Scope

This policy applies to:

- All GitHub Actions workflows in `.github/workflows/`
- Reusable workflows in MokoStandards and .github-private
- Workflow templates in `templates/workflows/`
- Local workflows in individual repositories
- Composite actions and custom actions
- Workflow job definitions and steps

This policy does not apply to:

- Third-party actions (governed by dependency management policy)
- Local development scripts (governed by scripting standards)
- Build system configurations (governed by build system standards)

## Responsibilities

### Workflow Authors

Responsible for:

- Writing secure and maintainable workflows
- Following naming conventions and standards
- Documenting workflow purpose and usage
- Testing workflows before committing
- Using reusable workflows where applicable
- Keeping workflows up to date

### Repository Maintainers

Responsible for:

- Reviewing workflow pull requests
- Approving workflow changes
- Ensuring workflow security
- Managing workflow secrets
- Archiving deprecated workflows
- Enforcing standards compliance

### Security Team

Accountable for:

- Reviewing workflows with elevated permissions
- Auditing workflow secrets usage
- Approving external action usage
- Validating security best practices
- Monitoring workflow execution logs

## Workflow Architecture

### Three-Tier Workflow Architecture

Moko Consulting uses a three-tier workflow architecture:

```
Tier 1: Organization-Wide Reusable Workflows (.github-private)
         ↓ (called by)
Tier 2: Repository-Specific Reusable Workflows (MokoStandards)
         ↓ (called by)
Tier 3: Local Workflows (individual repositories)
```

**Tier 1: Organization-Wide Reusable Workflows**
- Location: `mokoconsulting-tech/.github-private/.github/workflows/`
- Purpose: Shared across all organization repositories
- Examples: Deployment, security scanning, compliance audits
- Visibility: Private, internal only
- Maintenance: Centralized, high governance

**Tier 2: Repository-Specific Reusable Workflows**
- Location: `mokoconsulting-tech/MokoStandards/.github/workflows/`
- Purpose: Public templates and patterns
- Examples: CI validation, build automation, release management
- Visibility: Public, community accessible
- Maintenance: Standards-driven, documented

**Tier 3: Local Workflows**
- Location: Individual repository `.github/workflows/`
- Purpose: Repository-specific automation
- Examples: Project builds, tests, deployments
- Visibility: Matches repository visibility
- Maintenance: Repository maintainers

### Workflow Selection Guidelines

**Use Tier 1 (Organization-Wide) When:**
- Workflow contains sensitive organizational logic
- Workflow requires organization secrets
- Workflow enforces organization-wide compliance
- Workflow performs cross-repository operations
- Examples: Monthly compliance audits, organization health reports

**Use Tier 2 (Repository-Specific) When:**
- Workflow is a common pattern across repositories
- Workflow can be public and reusable
- Workflow demonstrates best practices
- Workflow requires project detection
- Examples: CI validation, build automation, standards compliance

**Use Tier 3 (Local) When:**
- Workflow is specific to one repository
- Workflow doesn't fit reusable pattern
- Workflow is experimental or one-off
- Workflow requires repository-specific configuration
- Examples: Project-specific tests, custom deployments

## Workflow Naming Conventions

### Reusable Workflows

Must follow this naming pattern:

```
reusable-{purpose}.yml
```

Examples:
- `reusable-ci-validation.yml`
- `reusable-build.yml`
- `reusable-deploy.yml`
- `reusable-joomla-testing.yml`
- `reusable-compliance-audit.yml`

### Local Workflows

Must be descriptive and follow this pattern:

```
{action}-{target}.yml
```

Examples:
- `ci.yml` (standard continuous integration)
- `release-pipeline.yml`
- `repo-health.yml`
- `branch-cleanup.yml`
- `standards-compliance.yml`

### Deprecated Workflows

Workflows that are no longer used must be moved to:

```
.github/workflows/archived/{workflow-name}.yml
```

Do not delete workflows - archive them for historical reference.

## Workflow Structure Standards

### Required Workflow Header

All workflows must include a standardized file header:

```yaml
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# This file is part of a Moko Consulting project.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# FILE INFORMATION
# DEFGROUP: GitHub.Workflow
# INGROUP: {Repository}.CI
# REPO: https://github.com/mokoconsulting-tech/{repository}
# PATH: /.github/workflows/{workflow-name}.yml
# VERSION: XX.YY.ZZ
# BRIEF: {Brief description of workflow purpose}
# NOTE: {Additional context or usage notes}
```

### Workflow Metadata

Every workflow must define:

```yaml
name: "Descriptive Workflow Name"

on:
  # Clearly defined triggers

permissions:
  # Minimal required permissions (principle of least privilege)

jobs:
  # Well-named, focused jobs
```

### Reusable Workflow Interface

Reusable workflows must define clear interfaces:

```yaml
on:
  workflow_call:
    inputs:
      # Required and optional inputs with descriptions and defaults
      input-name:
        description: "Clear description of what this input does"
        required: true
        type: string
        default: "sensible-default"

    outputs:
      # Outputs that calling workflows can use
      output-name:
        description: "Clear description of what this output provides"
        value: ${{ jobs.job-id.outputs.output-name }}

    secrets:
      # Secrets required by this workflow
      SECRET_NAME:
        description: "Clear description of what this secret is for"
        required: true
```

## Workflow Security Standards

### Permission Management

**Principle of Least Privilege:**

All workflows must explicitly declare minimal required permissions:

```yaml
permissions:
  contents: read        # Default: read-only
  pull-requests: write  # Only if needed
  issues: write         # Only if needed
  # Never use: permissions: write-all
```

**Default Permissions:**
- `contents: read` - Read repository contents
- No other permissions unless explicitly required

**Justification Required For:**
- `contents: write` - Must document why write access needed
- `pull-requests: write` - Must document PR modification need
- `actions: write` - Must document workflow modification need
- Any `write` permission - Requires security review

### Secrets Management

**Organization Secrets:**
- Stored at organization level
- Inherited by all repositories
- Used with `secrets: inherit` in reusable workflows
- Never hardcoded or logged

**Repository Secrets:**
- Repository-specific credentials
- Not shared across repositories
- Used when organization secrets not applicable

**Secret Usage Rules:**

1. **Never Log Secrets:**
```yaml
# BAD - Logs secret value
- run: echo "Token: ${{ secrets.MY_TOKEN }}"

# GOOD - Secrets never in echo/debug
- run: |
    if [ -z "$TOKEN" ]; then
      echo "Token not provided"
      exit 1
    fi
  env:
    TOKEN: ${{ secrets.MY_TOKEN }}
```

2. **Use Environment Variables:**
```yaml
- name: Use secret safely
  run: some-command --token "$TOKEN"
  env:
    TOKEN: ${{ secrets.MY_TOKEN }}
```

3. **Mask Additional Secrets:**
```yaml
- name: Mask dynamic secret
  run: |
    echo "::add-mask::$DYNAMIC_SECRET"
    # Now safe to use
```

### Third-Party Action Security

**Approved Actions:**

Only use actions from these sources:
- Official GitHub actions: `actions/*`
- Vetted third-party actions (maintain approved list)
- Internal organization actions: `mokoconsulting-tech/*`

**Pin to Commit SHA:**

Always pin third-party actions to specific commit SHA:

```yaml
# BAD - Mutable tag
- uses: actions/checkout@v4

# GOOD - Immutable commit SHA with tag comment
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1
```

**Action Review Process:**

1. Identify need for new action
2. Search approved actions list first
3. If not approved, submit for security review
4. Document approval decision in ADR
5. Add to approved actions list
6. Pin to specific version/SHA

### Workflow Triggers

**Secure Trigger Configuration:**

```yaml
# GOOD - Limited and explicit
on:
  push:
    branches: [main, 'dev/**', 'rc/**', 'version/**']
  pull_request:
    branches: [main]
  workflow_dispatch:  # Manual trigger only

# BAD - Too permissive
on: [push, pull_request]  # Any branch, any PR
on: pull_request_target   # Dangerous with user code
```

**`pull_request_target` Warning:**

Never use `pull_request_target` unless:
- Absolutely necessary
- Reviewed by security team
- Does not execute untrusted code
- Minimal permissions granted

## Workflow Documentation

### Required Documentation

Every reusable workflow must be documented in `.github/workflows/REUSABLE_WORKFLOWS.md`:

```markdown
### workflow-name.yml

**Purpose**: Brief description of what this workflow does

**Usage**: How to call this workflow from another workflow

**Inputs**:
- `input-name` (required/optional): Description and default value

**Outputs**:
- `output-name`: Description of output

**Secrets**:
- `SECRET_NAME` (required/optional): Description of secret

**Example**:
\```yaml
jobs:
  use-workflow:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-example.yml@main
    with:
      input-name: value
    secrets: inherit
\```

**Maintenance**: Last updated date, maintainer contact
```

### Workflow Architecture Documentation

Create `.github/WORKFLOW_ARCHITECTURE.md` explaining:

- Workflow hierarchy and relationships
- Reusable workflow patterns
- Workflow inheritance and composition
- Decision tree for workflow selection
- Common patterns and anti-patterns

### Inline Documentation

Use comments within workflows:

```yaml
jobs:
  build:
    name: "Build Application"
    runs-on: ubuntu-latest

    steps:
      # Step 1: Checkout code
      # This step retrieves the repository code for building
      - name: Checkout code
        uses: actions/checkout@sha

      # Step 2: Setup Python
      # Configure Python environment with specified version
      - name: Setup Python
        uses: actions/setup-python@sha
        with:
          python-version: '3.11'
```

## Workflow Testing

### Testing Requirements

All workflows must be tested before merging:

1. **Local Testing**: Use `act` to test locally when possible
2. **Branch Testing**: Test on feature branches before PR
3. **PR Testing**: Validate in pull request workflow runs
4. **Integration Testing**: Verify with dependent workflows

### Test Checklist

- [ ] Workflow syntax is valid (GitHub validates YAML)
- [ ] All required inputs are provided
- [ ] All required secrets are available
- [ ] Permissions are minimal and sufficient
- [ ] Workflow runs successfully on test branch
- [ ] Workflow handles errors gracefully
- [ ] Workflow produces expected outputs
- [ ] Documentation is complete and accurate

### Dry-Run Best Practices

**Workflows that call validation or fix scripts should support dry-run mode for testing.**

**Example workflow with dry-run support:**

```yaml
name: Repository Health Check

on:
  workflow_dispatch:
    inputs:
      dry_run:
        description: 'Run in dry-run mode'
        required: false
        type: boolean
        default: false
  pull_request:
    branches: [main, develop]

jobs:
  health-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run health check
        run: |
          if [ "${{ github.event.inputs.dry_run }}" = "true" ]; then
            python3 scripts/validate/check_repo_health.py --dry-run
          else
            python3 scripts/validate/check_repo_health.py
          fi
```

**Benefits of dry-run in workflows:**
- Test validation logic without blocking builds
- Preview changes before applying them
- Faster feedback during development
- Safer experimentation with workflow changes

**When to use dry-run:**
- ✅ Testing new validation rules
- ✅ Previewing file modifications
- ✅ Debugging workflow issues
- ✅ Training and documentation

## Workflow Maintenance

### Version Management

Workflows follow semantic versioning in file header:

```yaml
# VERSION: XX.YY.ZZ
```

**Version Increment Rules:**
- **XX (Major)**: Breaking changes to workflow interface
- **YY (Minor)**: New features, backward compatible
- **ZZ (Patch)**: Bug fixes, documentation updates

### Deprecation Process

To deprecate a workflow:

1. Add deprecation notice to workflow documentation
2. Update workflow header with deprecation note
3. Set removal date (minimum 90 days notice)
4. Update dependent workflows to use replacement
5. After removal date, move to `archived/` directory
6. Update workflow inventory and documentation

### Workflow Review Cadence

**Monthly Review:**
- Check for outdated dependencies
- Review security advisories
- Update pinned action versions
- Verify documentation accuracy

**Quarterly Review:**
- Identify redundant or duplicate workflows
- Consolidate similar workflows
- Archive unused workflows
- Update reusable workflow patterns

## Workflow Governance

### Approval Process

**For Public Reusable Workflows (MokoStandards):**

1. Author creates workflow and documentation
2. Submit pull request with:
   - Workflow file
   - Documentation update
   - Test results
   - Security review (if needed)
3. Code review by maintainers
4. Security review (if elevated permissions)
5. Approval by repository maintainers
6. Merge to main branch

**For Organization-Wide Workflows (.github-private):**

1. Same as public workflow process
2. Additional security team review required
3. Approval by organization admin required
4. Testing in staging environment required
5. Gradual rollout to repositories

### Change Control

**Minor Changes:**
- Documentation updates
- Comment additions
- Non-functional improvements
- Standard review process

**Major Changes:**
- Interface changes (inputs/outputs)
- Security model changes
- Breaking changes
- Requires ADR documentation
- Requires migration plan
- Extended review period

## Compliance and Auditing

### Audit Requirements

Workflows must support auditing:

- All workflow runs logged and retained
- Security-sensitive actions logged separately
- Failed runs investigated
- Secrets usage audited quarterly

### Compliance Checks

The `standards-compliance.yml` workflow provides comprehensive validation across 10 areas:

**Critical Checks** (Must Pass):
1. **Repository Structure** - Required directories and files
2. **Documentation Quality** - README and documentation completeness
3. **Coding Standards** - Language-specific linting (Python, PHP, YAML)
4. **License Compliance** - License file and SPDX identifiers
5. **Git Repository Hygiene** - Commit messages, branch naming, .gitignore
6. **Workflow Configuration** - GitHub Actions validation
7. **Version Consistency** - All version numbers match across repository
8. **Script Integrity** - SHA-256 hash validation of critical scripts

**Informational Checks** (Non-Blocking):
9. **Enterprise Readiness** - Enterprise patterns and best practices
10. **Repository Health** - Overall quality metrics and recommendations

**Usage**:
```yaml
# Automatically runs on:
# - Push to main, dev/*, rc/*
# - Pull requests to main, dev/*, rc/*
# - Manual trigger

# Local validation before pushing:
php scripts/validate/check_version_consistency.php --verbose
python3 scripts/maintenance/validate_script_registry.py --priority critical
php scripts/validate/check_enterprise_readiness.php --verbose
php scripts/validate/check_repo_health.php --verbose
```

**Compliance Scoring**:
- **100%** = ✅ COMPLIANT (all critical checks pass)
- **80-99%** = ⚠️ MOSTLY COMPLIANT (minor issues)
- **50-79%** = ⚠️ PARTIALLY COMPLIANT (significant issues)
- **0-49%** = ❌ NON-COMPLIANT (major violations)

Informational checks provide recommendations but do not affect compliance status.

**Documentation**: See [Standards Compliance Workflow](../workflows/standards-compliance.md) for detailed information.

## Best Practices

### General Best Practices

1. **Single Responsibility**: Each workflow should have one clear purpose
2. **Composability**: Use reusable workflows to build complex automation
3. **Idempotency**: Workflows should be safe to re-run
4. **Fast Feedback**: Fail fast on errors
5. **Clear Outputs**: Provide helpful error messages and logs
6. **Resource Efficiency**: Don't waste CI minutes
7. **Cache Appropriately**: Cache dependencies to speed up builds

### Common Patterns

**Pattern 1: Conditional Job Execution**
```yaml
jobs:
  deploy:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: ./deploy.sh
```

**Pattern 2: Matrix Builds**
```yaml
jobs:
  test:
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-python@sha
        with:
          python-version: ${{ matrix.python-version }}
```

**Pattern 3: Reusable Workflow with Outputs**
```yaml
jobs:
  detect:
    uses: ./.github/workflows/reusable-project-detector.yml

  build:
    needs: detect
    if: needs.detect.outputs.project-type == 'joomla'
    runs-on: ubuntu-latest
```

### Anti-Patterns to Avoid

1. **Monolithic Workflows**: Single workflow doing too much
2. **Duplicated Logic**: Copy-paste instead of reusable workflows
3. **Hardcoded Values**: Use inputs and variables instead
4. **Insufficient Error Handling**: Workflows that fail silently
5. **Overly Broad Permissions**: More permissions than needed
6. **Unmaintained Workflows**: Workflows that haven't been updated
7. **Missing Documentation**: Workflows without usage examples

## Migration Guide

### Migrating to Reusable Workflows

1. Identify repeated workflow patterns across repositories
2. Extract common logic into reusable workflow
3. Define clear inputs, outputs, and secrets
4. Document the reusable workflow
5. Test thoroughly
6. Update calling workflows
7. Remove duplicated code

### Example Migration

**Before (duplicated in multiple repos):**
```yaml
# repo1/.github/workflows/ci.yml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@sha
      - name: Setup Python
        uses: actions/setup-python@sha
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest
```

**After (reusable workflow):**
```yaml
# MokoStandards/.github/workflows/reusable-python-ci.yml
on:
  workflow_call:
    inputs:
      python-version:
        type: string
        default: '3.11'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@sha
      - name: Setup Python
        uses: actions/setup-python@sha
        with:
          python-version: ${{ inputs.python-version }}
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest

# repo1/.github/workflows/ci.yml (simplified)
jobs:
  ci:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-python-ci.yml@main
    with:
      python-version: '3.11'
```

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Actions Security Hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [MokoStandards Workflow Inventory](../../.github/WORKFLOW_INVENTORY.md)
- [Reusable Workflows Documentation](../../.github/workflows/REUSABLE_WORKFLOWS.md)
- [Workflow Architecture](../../.github/WORKFLOW_ARCHITECTURE.md)

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Policy                                       |
| Domain         | Governance                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/policy/workflow-standards.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
