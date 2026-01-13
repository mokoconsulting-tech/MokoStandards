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
INGROUP: MokoStandards.Workflows
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /.github/WORKFLOW_ARCHITECTURE.md
VERSION: 01.00.00
BRIEF: Workflow architecture, hierarchy, and design patterns
-->

# Workflow Architecture

## Overview

This document explains the workflow architecture used across Moko Consulting repositories, including the hierarchy, design patterns, reusable workflow patterns, and decision-making processes for workflow selection.

## Purpose

This architecture guide provides:

- **Understanding**: Clear mental model of workflow organization
- **Guidance**: Decision trees for workflow selection
- **Patterns**: Reusable patterns and best practices
- **Relationships**: How workflows interact and depend on each other
- **Evolution**: How to extend and improve the workflow architecture

## Three-Tier Workflow Architecture

Moko Consulting uses a three-tier architecture for GitHub Actions workflows:

```
┌─────────────────────────────────────────────────────────────┐
│ Tier 1: Organization-Wide Reusable Workflows               │
│ Location: .github-private repository                        │
│ Visibility: Private                                         │
│ Purpose: Shared across all organization repositories        │
│ Examples: Deployment, compliance audits, security scanning  │
└─────────────────────────────────────────────────────────────┘
                          ↓ (called by)
┌─────────────────────────────────────────────────────────────┐
│ Tier 2: Public Reusable Workflows                          │
│ Location: MokoStandards repository                          │
│ Visibility: Public                                          │
│ Purpose: Templates and patterns for community use           │
│ Examples: CI validation, build automation, health checks    │
└─────────────────────────────────────────────────────────────┘
                          ↓ (called by)
┌─────────────────────────────────────────────────────────────┐
│ Tier 3: Local Workflows                                    │
│ Location: Individual repository .github/workflows/         │
│ Visibility: Matches repository visibility                   │
│ Purpose: Repository-specific automation                    │
│ Examples: Project builds, tests, custom deployments        │
└─────────────────────────────────────────────────────────────┘
```

### Tier 1: Organization-Wide Reusable Workflows

**Location**: `mokoconsulting-tech/.github-private/.github/workflows/`

**Characteristics**:
- Private and secure
- Contains sensitive organizational logic
- Requires organization secrets
- Enforces organization-wide compliance
- Centrally maintained with high governance
- Performs cross-repository operations

**Examples**:
- `reusable-compliance-audit.yml` - Monthly compliance audits
- `reusable-standards-scan.yml` - Organization-wide standards scanning
- `reusable-branch-cleanup.yml` - Automated branch cleanup
- `reusable-auto-label.yml` - Automated issue/PR labeling
- `reusable-stale-management.yml` - Stale issue/PR management

**When to Use**:
- Workflow contains proprietary logic
- Workflow requires organization-level secrets
- Workflow performs cross-repository operations
- Workflow enforces organization-wide policies
- Workflow handles sensitive data or operations

### Tier 2: Public Reusable Workflows

**Location**: `mokoconsulting-tech/MokoStandards/.github/workflows/`

**Characteristics**:
- Public and community-accessible
- Demonstrates best practices
- Platform-agnostic where possible
- Well-documented with examples
- Follows standards defined in `/docs/policy/`
- Suitable for open-source sharing

**Examples**:
- `reusable-ci-validation.yml` - CI validation with project detection
- `reusable-build.yml` - Universal build workflow
- `reusable-deploy.yml` - Deployment workflow template
- `reusable-joomla-testing.yml` - Joomla-specific testing
- `reusable-php-quality.yml` - PHP code quality checks
- `reusable-project-detector.yml` - Automatic project type detection

**When to Use**:
- Workflow is a common pattern across repositories
- Workflow can be public and shared
- Workflow demonstrates best practices
- Workflow is platform-agnostic or extensible
- Workflow serves as template for community

### Tier 3: Local Workflows

**Location**: Individual repository `.github/workflows/`

**Characteristics**:
- Repository-specific
- Calls reusable workflows from Tier 1 or Tier 2
- Contains minimal logic (orchestration only)
- Easy to understand and maintain
- Project-specific configuration

**Examples**:
- `ci.yml` - Calls reusable CI validation workflow
- `release-pipeline.yml` - Orchestrates release process
- `repo-health.yml` - Repository health monitoring
- `standards-compliance.yml` - Standards validation

**When to Use**:
- Workflow is specific to one repository
- Workflow doesn't fit reusable pattern
- Workflow is experimental or temporary
- Workflow orchestrates multiple reusable workflows

## Workflow Design Patterns

### Pattern 1: Project Detection and Conditional Execution

Automatically detect project type and execute appropriate build/test strategy.

```yaml
jobs:
  detect:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-project-detector.yml@main
  
  build-joomla:
    needs: detect
    if: needs.detect.outputs.project-type == 'joomla'
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-joomla-testing.yml@main
  
  build-generic:
    needs: detect
    if: needs.detect.outputs.project-type == 'generic'
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-build.yml@main
```

**Benefits**:
- Single workflow supports multiple project types
- No manual configuration needed
- Easy to maintain and extend

### Pattern 2: Composition through Reusable Workflows

Build complex workflows by composing simple reusable workflows.

```yaml
jobs:
  # Step 1: Validate code
  validate:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
  
  # Step 2: Build if validation passes
  build:
    needs: validate
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-build.yml@main
  
  # Step 3: Deploy if build passes
  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-deploy.yml@main
    secrets: inherit
```

**Benefits**:
- Clear separation of concerns
- Reusable components
- Easy to test and debug
- Flexible composition

### Pattern 3: Matrix Strategy for Multi-Platform Testing

Test across multiple versions or platforms using matrix strategy.

```yaml
jobs:
  test:
    strategy:
      matrix:
        php-version: ['7.4', '8.0', '8.1', '8.2']
        os: [ubuntu-latest, windows-latest]
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-php-quality.yml@main
    with:
      php-version: ${{ matrix.php-version }}
```

**Benefits**:
- Comprehensive testing coverage
- Parallel execution
- Configurable test matrix

### Pattern 4: Conditional Deployment Based on Environment

Deploy to different environments based on branch or tag.

```yaml
jobs:
  deploy-staging:
    if: github.ref == 'refs/heads/dev'
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-deploy.yml@main
    with:
      environment: staging
  
  deploy-production:
    if: startsWith(github.ref, 'refs/tags/v')
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-deploy.yml@main
    with:
      environment: production
```

**Benefits**:
- Safe deployment practices
- Environment-specific configuration
- Clear deployment triggers

### Pattern 5: Workflow Dispatch with Manual Controls

Allow manual triggering with customizable inputs.

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deployment environment'
        required: true
        type: choice
        options:
          - staging
          - production
      dry-run:
        description: 'Perform dry run'
        required: false
        type: boolean
        default: true

jobs:
  deploy:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-deploy.yml@main
    with:
      environment: ${{ inputs.environment }}
      dry-run: ${{ inputs.dry-run }}
```

**Benefits**:
- Manual control when needed
- Safe defaults (dry-run)
- Clear input options

## Workflow Relationships

### Dependency Graph

```
repo-health.yml
    │
    └──> Uses: reusable-project-detector.yml
                │
                └──> Provides: project-type output

ci.yml
    │
    ├──> Uses: reusable-ci-validation.yml
    │         │
    │         ├──> Uses: reusable-project-detector.yml
    │         └──> Uses: reusable-php-quality.yml (if PHP)
    │
    └──> Uses: reusable-build.yml
              │
              └──> Uses: reusable-project-detector.yml

release-pipeline.yml
    │
    ├──> Uses: reusable-build.yml
    ├──> Uses: reusable-release.yml
    └──> Uses: reusable-deploy.yml
```

### Workflow Inheritance

Workflows inherit behavior through composition:

1. **Base Workflows**: Provide core functionality
   - `reusable-project-detector.yml`
   - `reusable-build.yml`

2. **Specialized Workflows**: Add domain-specific logic
   - `reusable-joomla-testing.yml` (extends base build)
   - `reusable-php-quality.yml` (extends base validation)

3. **Orchestration Workflows**: Combine multiple workflows
   - `ci.yml` (combines validation + build)
   - `release-pipeline.yml` (combines build + release + deploy)

## Decision Trees

### Choosing the Right Tier

```
Start: Need to create/modify workflow
    │
    ├──> Contains sensitive/proprietary logic?
    │    └──> YES: Use Tier 1 (.github-private)
    │
    ├──> Common pattern across repositories?
    │    └──> YES: Use Tier 2 (MokoStandards)
    │
    └──> Repository-specific?
         └──> YES: Use Tier 3 (local workflow)
```

### Choosing Between Reusable vs Local

```
Start: Creating new workflow
    │
    ├──> Used by multiple repositories?
    │    └──> YES: Create reusable workflow
    │
    ├──> Complex multi-step process?
    │    └──> YES: Break into reusable components
    │
    └──> Simple repository-specific task?
         └──> YES: Create local workflow
```

### Choosing Workflow Trigger

```
Start: When should workflow run?
    │
    ├──> On code changes?
    │    └──> Use: on.push, on.pull_request
    │
    ├──> On schedule?
    │    └──> Use: on.schedule (cron)
    │
    ├──> Manual trigger needed?
    │    └──> Use: on.workflow_dispatch
    │
    └──> Called by other workflows?
         └──> Use: on.workflow_call
```

## Workflow Evolution

### Adding New Workflows

1. **Identify Need**: What problem does this workflow solve?
2. **Check Existing**: Can existing workflow be extended?
3. **Design Interface**: Define inputs, outputs, secrets
4. **Choose Tier**: Public (Tier 2) or Private (Tier 1)?
5. **Implement**: Follow [Workflow Standards](../docs/policy/workflow-standards.md)
6. **Document**: Add to [REUSABLE_WORKFLOWS.md](./workflows/REUSABLE_WORKFLOWS.md)
7. **Test**: Validate in test repository
8. **Deploy**: Merge and communicate

### Refactoring Workflows

Signs a workflow needs refactoring:
- Duplicated logic across repositories
- Complex, hard-to-maintain workflow
- Frequent changes to same workflow across repos
- Lack of clear purpose or focus

Refactoring process:
1. Identify common patterns
2. Extract to reusable workflow
3. Define clear interface
4. Update calling workflows
5. Test thoroughly
6. Document changes
7. Deprecate old approach

### Deprecating Workflows

Process for deprecating workflows:
1. Add deprecation notice to workflow
2. Provide migration path
3. Update documentation
4. Communicate to users
5. Wait minimum 90 days
6. Move to `archived/` directory
7. Update inventories

## Best Practices

### Keep Workflows Focused

✅ **Good**: Single-purpose workflow
```yaml
# reusable-php-quality.yml - PHP quality checks only
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - name: Run PHP CodeSniffer
      - name: Run PHPStan
      - name: Run PHP Mess Detector
```

❌ **Bad**: Kitchen-sink workflow
```yaml
# mega-workflow.yml - Too many responsibilities
jobs:
  everything:
    steps:
      - name: Lint
      - name: Test
      - name: Build
      - name: Deploy
      - name: Notify
      - name: Update docs
```

### Use Composition Over Duplication

✅ **Good**: Compose from reusable workflows
```yaml
jobs:
  validate:
    uses: org/repo/.github/workflows/reusable-validate.yml@main
  build:
    uses: org/repo/.github/workflows/reusable-build.yml@main
```

❌ **Bad**: Duplicate logic
```yaml
jobs:
  validate-and-build:
    steps:
      - name: Checkout
      - name: Setup
      - name: Lint (duplicated across repos)
      - name: Test (duplicated across repos)
      - name: Build (duplicated across repos)
```

### Fail Fast

✅ **Good**: Quick feedback on failures
```yaml
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Quick syntax check
        run: |
          if ! php -l src/*.php; then
            echo "::error::PHP syntax errors found"
            exit 1
          fi
  
  test:
    needs: validate  # Only run if validation passes
```

❌ **Bad**: Slow feedback
```yaml
jobs:
  everything:
    steps:
      - name: Run all tests (30 minutes)
      - name: Then check syntax  # Should be first!
```

## Common Anti-Patterns

### Anti-Pattern 1: Monolithic Workflows

**Problem**: One huge workflow that does everything

**Solution**: Break into focused, composable workflows

### Anti-Pattern 2: Hardcoded Values

**Problem**: Hardcoded configuration in workflow files

**Solution**: Use inputs and variables

### Anti-Pattern 3: Insufficient Error Handling

**Problem**: Workflows fail silently or with unclear errors

**Solution**: Add error handling and clear error messages

### Anti-Pattern 4: Overly Broad Permissions

**Problem**: Workflows request more permissions than needed

**Solution**: Follow principle of least privilege

### Anti-Pattern 5: No Testing

**Problem**: Workflows deployed without testing

**Solution**: Test in feature branches first

## References

- [Workflow Standards Policy](../docs/policy/workflow-standards.md)
- [Reusable Workflows Documentation](./workflows/REUSABLE_WORKFLOWS.md)
- [Workflow Inventory](./WORKFLOW_INVENTORY.md)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Repository Organization Guide](../docs/guide/repository-organization.md)

## Metadata

* **Document**: .github/WORKFLOW_ARCHITECTURE.md
* **Repository**: [MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards)
* **Owner**: Moko Consulting Engineering Team
* **Scope**: Workflow architecture and design patterns
* **Lifecycle**: Active
* **Audience**: All engineers and workflow authors

## Revision History

| Version  | Date       | Author                          | Notes                                           |
| -------- | ---------- | ------------------------------- | ----------------------------------------------- |
| 01.00.00 | 2026-01-13 | GitHub Copilot                  | Initial workflow architecture documentation     |
