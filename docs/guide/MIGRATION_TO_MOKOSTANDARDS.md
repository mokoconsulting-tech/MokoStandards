# Migration to MokoStandards

This guide walks you through adopting MokoStandards in your project, providing consistent CI/CD pipelines, coding standards, and best practices.

## Overview

MokoStandards provides reusable GitHub Actions workflows and coding standards that you can adopt in your projects to improve code quality, automate testing, and enforce consistency.

## Benefits

- ✅ **Automated CI/CD** - Pre-configured workflows for testing, building, and deploying
- ✅ **Code Quality** - Automated linting, formatting, and security scanning
- ✅ **Consistency** - Standardized practices across all projects
- ✅ **Time Savings** - Don't reinvent the wheel for each project
- ✅ **Best Practices** - Battle-tested patterns and configurations
- ✅ **Community** - Contribute improvements back to MokoStandards

## Prerequisites

Before starting, ensure you have:

- [ ] A GitHub repository (public or private)
- [ ] Admin access to the repository
- [ ] Basic understanding of GitHub Actions
- [ ] Your project's language/framework identified

## Migration Steps

### Step 1: Assess Your Project

Identify your project type and needs:

```bash
# Check if you have a Joomla project
ls *.xml | grep -E "(mod_|plg_|com_|pkg_|tpl_)" && echo "Joomla project"

# Check if you have a Dolibarr project
ls dolibarr.xml 2>/dev/null && echo "Dolibarr project"

# Check technologies
[ -f "package.json" ] && echo "Node.js project"
[ -f "composer.json" ] && echo "PHP project"
[ -f "requirements.txt" ] && echo "Python project"
```

### Step 2: Add Required Files

Ensure your project has essential files:

```bash
# Create directory for workflows
mkdir -p .github/workflows

# Add essential documentation (if missing)
touch README.md
touch LICENSE
touch .gitignore
touch CHANGELOG.md
touch CONTRIBUTING.md
```

### Step 3: Create CI Workflow

Copy the template and customize for your project:

**Option A: Using curl (verify the content before use)**
```bash
# Download the template
curl -o .github/workflows/ci.yml https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/.github/workflows/ci-template.yml

# IMPORTANT: Review the downloaded file before using it
cat .github/workflows/ci.yml
```

**Option B: Using GitHub CLI (recommended - more secure)**
```bash
# Clone MokoStandards temporarily
gh repo clone mokoconsulting-tech/MokoStandards /tmp/mokostandards

# Copy the template
cp /tmp/mokostandards/.github/workflows/ci-template.yml .github/workflows/ci.yml

# Clean up
rm -rf /tmp/mokostandards
```

**Option C: Manual creation (most secure)**

```yaml
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
# SPDX-License-Identifier: GPL-3.0-or-later

name: Continuous Integration

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

permissions:
  contents: read
  pull-requests: write
  checks: write

jobs:
  ci:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      profile: full
      # Customize based on your project type:
      # validate-manifests: true    # For Joomla/Dolibarr
      # php-version: '8.2'          # For PHP projects
      # node-version: '20.x'        # For Node.js projects
    secrets: inherit
```

### Step 4: Configure Branch Protection

Set up branch protection rules:

1. Go to **Settings** → **Branches**
2. Click **Add rule**
3. Set **Branch name pattern**: `main`
4. Enable:
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
5. Add status check: **Repository Validation Pipeline**
6. Save changes

### Step 5: Test the Workflow

Create a test PR to verify the workflow:

```bash
# Create a test branch
git checkout -b test/mokostandards-migration

# Make a small change
echo "# Test" >> README.md

# Commit and push
git add README.md
git commit -m "test: Verify MokoStandards CI workflow"
git push -u origin test/mokostandards-migration
```

Open a pull request and verify that the CI workflow runs successfully.

### Step 6: Add EditorConfig

Copy the EditorConfig file for consistent code formatting:

```bash
curl -o .editorconfig https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/.editorconfig
```

Or create `.editorconfig` manually:

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = tab
tab_width = 2

[*.md]
trim_trailing_whitespace = false

[*.{json,yml,yaml}]
indent_style = tab
tab_width = 2
```

### Step 7: Add YAML Linting (Optional)

For projects with YAML files:

```bash
curl -o .yamllint https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/.yamllint
```

### Step 8: Customize for Your Project

#### For Joomla Extensions

```yaml
jobs:
  ci:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      profile: full
      validate-manifests: true
      validate-licenses: true
      php-version: '8.1'
    secrets: inherit
```

#### For Node.js Projects

```yaml
jobs:
  ci:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      profile: full
      validate-security: true
      node-version: '20.x'
    secrets: inherit
```

#### For PHP Libraries

```yaml
jobs:
  ci:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      profile: full
      validate-licenses: true
      validate-security: true
      php-version: '8.2'
    secrets: inherit
```

### Step 9: Add Repository Health Check (Optional)

Monitor your repository health:

```yaml
# .github/workflows/health.yml
name: Repository Health

on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday
  workflow_dispatch:

permissions:
  contents: read
  issues: write

jobs:
  health:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/repo-health.yml@main
    with:
      health-threshold: 70
      create-issue-on-failure: true
    secrets: inherit
```

### Step 10: Update Documentation

Update your README to mention MokoStandards:

```markdown
## Development

This project follows the [MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards) 
for consistent CI/CD pipelines and coding standards.

### CI/CD

The project uses automated workflows for:
- Code linting and formatting
- Security scanning
- Automated testing
- Build verification

See our [Contributing Guide](CONTRIBUTING.md) for development setup.
```

## Project-Specific Configurations

### Joomla Extensions

#### Component with Admin/Site Split

```yaml
jobs:
  ci:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      profile: strict
      validate-manifests: true
      validate-licenses: true
      validate-changelogs: true
      php-version: '8.1'
    secrets: inherit
```

#### Simple Module/Plugin

```yaml
jobs:
  ci:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      profile: full
      validate-manifests: true
      php-version: '8.1'
    secrets: inherit
```

### Dolibarr Modules

```yaml
jobs:
  ci:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      profile: full
      validate-licenses: true
      validate-security: true
      php-version: '8.0'
    secrets: inherit
```

### Multi-Language Projects

```yaml
jobs:
  ci:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      profile: full
      validate-security: true
      validate-licenses: true
      php-version: '8.2'
      node-version: '20.x'
    secrets: inherit
```

## Advanced Configuration

### Custom Validation Scripts

Add project-specific validation:

```yaml
jobs:
  mokostandards-ci:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      profile: full
    secrets: inherit

  custom-validation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - name: Custom checks
        run: |
          ./scripts/validate-custom.sh
```

### Environment-Specific Configuration

Different configs for different branches:

```yaml
jobs:
  ci:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      profile: ${{ github.ref == 'refs/heads/main' && 'strict' || 'full' }}
      fail-on-warnings: ${{ github.ref == 'refs/heads/main' }}
    secrets: inherit
```

### Matrix Testing

Test across multiple versions:

```yaml
jobs:
  test:
    strategy:
      matrix:
        php: ['8.1', '8.2', '8.3']
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      php-version: ${{ matrix.php }}
    secrets: inherit
```

## Troubleshooting

### Workflow Not Running

**Problem**: CI workflow doesn't trigger on PRs

**Solution**: 
1. Check workflow file is in `.github/workflows/`
2. Verify YAML syntax is valid
3. Ensure permissions are correct
4. Check branch names match trigger patterns

### Permission Denied Errors

**Problem**: Workflow fails with permission errors

**Solution**:
```yaml
permissions:
  contents: read
  pull-requests: write
  checks: write
```

### Validation Failures

**Problem**: Standards validation fails

**Solution**:
1. Review the workflow logs
2. Fix reported issues locally
3. Run validation locally before pushing
4. Adjust validation profile if too strict

### Manifest Validation Fails

**Problem**: XML manifest validation errors

**Solution**:
1. Validate XML syntax
2. Check required fields are present
3. Verify naming conventions
4. Review Joomla/Dolibarr manifest requirements

## Best Practices

### 1. Start with Basic Profile

Don't enable all validations immediately:

```yaml
# Week 1: Start simple
with:
  profile: basic

# Week 2: Add more checks
with:
  profile: full

# Week 3: Full compliance
with:
  profile: strict
  fail-on-warnings: true
```

### 2. Fix Issues Incrementally

Address validation issues gradually:

1. Fix critical security issues first
2. Address code quality issues
3. Improve documentation
4. Add missing files

### 3. Customize Thoughtfully

Only override defaults when necessary:

```yaml
# ❌ Over-configuration
with:
  profile: full
  validate-manifests: true
  validate-changelogs: true
  validate-licenses: true
  validate-security: true
  node-version: '20.x'
  php-version: '8.1'
  working-directory: '.'
  fail-on-warnings: false

# ✅ Minimal necessary configuration
with:
  profile: full
  php-version: '8.1'
```

### 4. Keep Workflows Updated

Pin to stable versions but update regularly:

```yaml
# Pin to major version for stability
uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@v1

# Or pin to specific version
uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@v1.2.3
```

### 5. Monitor Workflow Performance

Track and optimize workflow execution time:

- Review workflow duration in Actions tab
- Use caching for dependencies
- Run fast checks before slow ones
- Parallelize independent jobs

## Getting Help

### Documentation

- [Project Type Detection](PROJECT_TYPE_DETECTION.md)
- [Public Architecture](PUBLIC_ARCHITECTURE.md)
- [Health Scoring](../policy/health-scoring.md)
- [Reusable Workflows](../.github/workflows/REUSABLE_WORKFLOWS.md)

### Community Support

- **Issues**: [GitHub Issues](https://github.com/mokoconsulting-tech/MokoStandards/issues)
- **Discussions**: [GitHub Discussions](https://github.com/mokoconsulting-tech/MokoStandards/discussions)
- **Examples**: See example projects using MokoStandards

### Contributing Back

Found an improvement? Contribute back:

1. Fork MokoStandards
2. Create a feature branch
3. Implement improvement
4. Submit a pull request

## Migration Checklist

Use this checklist to track your migration:

- [ ] Project type identified (Joomla/Dolibarr/Generic)
- [ ] Essential files added (README, LICENSE, .gitignore)
- [ ] CI workflow created and tested
- [ ] Branch protection rules configured
- [ ] EditorConfig added
- [ ] Documentation updated
- [ ] Team trained on new workflow
- [ ] First successful CI run completed
- [ ] PR process documented
- [ ] Optional: Health check workflow added
- [ ] Optional: Advanced configurations applied

## Next Steps

After successful migration:

1. **Train Your Team** - Ensure everyone understands the new workflow
2. **Document Customizations** - Record any project-specific configurations
3. **Monitor and Iterate** - Continuously improve your setup
4. **Share Knowledge** - Help other projects migrate
5. **Contribute Improvements** - Share enhancements back to MokoStandards

## Success Stories

> "Migration to MokoStandards reduced our CI setup time from days to hours and gave us confidence in our code quality." - *Example Team*

> "Automated security scanning caught several issues we would have missed. The standardized workflows make onboarding new developers much easier." - *Example Developer*

---

**Version:** 1.0.0  
**Last Updated:** 2026-01-13  
**License:** GPL-3.0-or-later

**Need help?** Open an [issue](https://github.com/mokoconsulting-tech/MokoStandards/issues) or start a [discussion](https://github.com/mokoconsulting-tech/MokoStandards/discussions).
