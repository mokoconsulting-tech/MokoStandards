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
INGROUP: MokoStandards.Standards
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/REPOSITORY_STANDARDS_APPLICATION.md
VERSION: 01.00.00
BRIEF: Guidance on applying MokoStandards to repositories
-->

# Repository Standards Application

## Overview

This document provides comprehensive guidance on applying standards from the MokoStandards repository to your projects. MokoStandards provides reusable workflows, quality checks, and platform-specific guidelines that can be adopted by any repository.

## Table of Contents

- [Quick Start](#quick-start)
- [Standards Application Workflow](#standards-application-workflow)
- [Platform-Specific Standards](#platform-specific-standards)
- [Repository Configuration](#repository-configuration)
- [Quality Checks and Validation](#quality-checks-and-validation)
- [Continuous Integration Setup](#continuous-integration-setup)
- [Best Practices](#best-practices)

## Quick Start

### 1. Identify Your Project Type

MokoStandards supports multiple project types:

- **Joomla Extensions** - Components, modules, plugins
- **Dolibarr Modules** - Custom modules and integrations
- **Generic PHP Projects** - Libraries, applications, scripts
- **Multi-Platform Projects** - Projects spanning multiple technologies

### 2. Basic Configuration

Create a `.github/workflows/ci.yml` in your repository:

```yaml
name: Continuous Integration

on:
  push:
    branches: [main, dev/**, rc/**]
  pull_request:
    branches: [main]

jobs:
  validate:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      profile: standard
```

### 3. Apply Quality Standards

Add quality checks to your workflow:

```yaml
jobs:
  quality:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-php-quality.yml@main
    with:
      php-version: '8.1'
      coding-standard: PSR-12
```

## Standards Application Workflow

### Step-by-Step Process

#### Step 1: Repository Assessment

Evaluate your repository's current state:

```bash
# Clone your repository
git clone https://github.com/your-org/your-repo.git
cd your-repo

# Check current structure
tree -L 2 -a

# Review existing workflows
ls -la .github/workflows/

# Check for existing standards
find . -name "phpcs.xml*" -o -name ".php-cs-fixer.php"
```

#### Step 2: Create Workflow Directory

```bash
# Create workflows directory if it doesn't exist
mkdir -p .github/workflows

# Create basic CI workflow
cat > .github/workflows/ci.yml << 'EOF'
# Copyright (C) 2026 Your Organization <email@example.com>
# SPDX-License-Identifier: GPL-3.0-or-later

name: Continuous Integration

on:
  push:
    branches: [main, dev/**]
  pull_request:
    branches: [main]

permissions:
  contents: read
  pull-requests: write
  checks: write

jobs:
  ci-validation:
    name: CI Validation
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      profile: standard
EOF
```

#### Step 3: Add Platform-Specific Standards

Choose the appropriate standard for your project type:

**For Joomla Projects:**
```yaml
jobs:
  joomla-testing:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-joomla-testing.yml@main
    with:
      joomla-version: '4.4'
      php-version: '8.1'
      extension-type: component
```

**For PHP Quality Checks:**
```yaml
jobs:
  php-quality:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-php-quality.yml@main
    with:
      php-version: '8.1'
      phpcs-standard: PSR-12
      phpstan-level: 6
```

#### Step 4: Configure Local Tools

Create configuration files for local development:

```bash
# PHP CodeSniffer configuration
cat > phpcs.xml << 'EOF'
<?xml version="1.0"?>
<ruleset name="Project Coding Standard">
    <description>Project coding standard based on PSR-12</description>
    
    <file>src</file>
    <file>tests</file>
    
    <exclude-pattern>*/vendor/*</exclude-pattern>
    <exclude-pattern>*/node_modules/*</exclude-pattern>
    
    <rule ref="PSR12"/>
    
    <arg name="colors"/>
    <arg value="sp"/>
</ruleset>
EOF

# PHPStan configuration
cat > phpstan.neon << 'EOF'
parameters:
    level: 6
    paths:
        - src
        - tests
    excludePaths:
        - vendor
        - node_modules
EOF
```

#### Step 5: Test Locally

Before committing, test standards locally:

```bash
# Install dependencies
composer install

# Run PHP CodeSniffer
vendor/bin/phpcs

# Run PHPStan
vendor/bin/phpstan analyse

# Run PHPUnit tests
vendor/bin/phpunit
```

#### Step 6: Commit and Push

```bash
# Stage changes
git add .github/workflows/ci.yml phpcs.xml phpstan.neon

# Commit with conventional commit message
git commit -m "ci: add MokoStandards CI validation workflow"

# Push to repository
git push origin main
```

#### Step 7: Verify Workflow Execution

1. Navigate to your repository on GitHub
2. Click on "Actions" tab
3. Verify the workflow runs successfully
4. Review any validation failures and fix them

## Platform-Specific Standards

### Joomla Development Standards

#### Requirements

MokoStandards provides Joomla-specific guidelines for:

- Extension structure and organization
- Joomla coding standards compliance
- Database schema management
- Language file standards
- Update server configuration

#### Configuration Example

```yaml
# .github/workflows/joomla-ci.yml
name: Joomla Extension CI

on:
  push:
    branches: [main, dev/**]
  pull_request:

jobs:
  joomla-validation:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-joomla-testing.yml@main
    with:
      joomla-version: '4.4'
      php-version: '8.1'
      extension-type: component
      extension-name: com_example
      
  code-quality:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-php-quality.yml@main
    with:
      php-version: '8.1'
      phpcs-standard: Joomla
```

#### Local Setup

```bash
# Install Joomla coding standard
composer require --dev joomla/coding-standards

# Create Joomla-specific phpcs.xml
cat > phpcs.xml << 'EOF'
<?xml version="1.0"?>
<ruleset name="Joomla Extension Standard">
    <description>Joomla extension coding standard</description>
    
    <file>administrator/components/com_example</file>
    <file>components/com_example</file>
    
    <rule ref="Joomla"/>
    
    <arg name="colors"/>
    <arg value="sp"/>
</ruleset>
EOF
```

#### Key Standards

- Follow Joomla naming conventions
- Use Joomla framework components
- Implement proper MVC structure
- Include language strings for all user-facing text
- Provide XML manifest files
- Follow Joomla security best practices

**Reference**: See `docs/policy/joomla-development-standard.md` for complete guidelines.

### Dolibarr Module Standards

#### Requirements

MokoStandards provides Dolibarr-specific guidelines for:

- Module structure and organization
- Dolibarr API integration
- Database table naming conventions
- Module descriptor configuration
- Permissions and access control

#### Configuration Example

```yaml
# .github/workflows/dolibarr-ci.yml
name: Dolibarr Module CI

on:
  push:
    branches: [main, dev/**]
  pull_request:

jobs:
  dolibarr-validation:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-php-quality.yml@main
    with:
      php-version: '7.4'
      phpcs-standard: PSR-12
      
  module-structure:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Validate module structure
        run: |
          # Check required files exist
          test -f core/modules/modExample.class.php
          test -f core/boxes/box_example.php
          test -f sql/llx_example.sql
          test -f sql/llx_example.key.sql
```

#### Local Setup

```bash
# Create Dolibarr module structure
mkdir -p core/modules
mkdir -p core/boxes
mkdir -p sql
mkdir -p langs/en_US

# Create module descriptor
cat > core/modules/modExample.class.php << 'EOF'
<?php
/**
 * Module descriptor class
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

require_once DOL_DOCUMENT_ROOT.'/core/modules/DolibarrModules.class.php';

class modExample extends DolibarrModules
{
    // Module descriptor implementation
}
EOF
```

#### Key Standards

- Follow Dolibarr file naming conventions
- Use Dolibarr database abstraction layer
- Implement proper permission checks
- Include translation files
- Provide SQL installation scripts
- Follow Dolibarr hook system

**Reference**: See `docs/policy/dolibarr-module-standard.md` for complete guidelines.

### Generic PHP Projects

#### Requirements

For non-platform-specific PHP projects:

- PSR-12 coding standards
- PHPStan level 6+ static analysis
- PHPUnit test coverage
- Dependency security scanning

#### Configuration Example

```yaml
# .github/workflows/php-ci.yml
name: PHP Project CI

on:
  push:
    branches: [main, dev/**]
  pull_request:

jobs:
  php-quality:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-php-quality.yml@main
    with:
      php-version: '8.2'
      phpcs-standard: PSR-12
      phpstan-level: 8
      coverage-threshold: 80
      
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Dependency security scan
        run: composer audit
```

#### Local Setup

```bash
# Install quality tools
composer require --dev \
  squizlabs/php_codesniffer \
  phpstan/phpstan \
  phpunit/phpunit

# Create composer scripts
cat >> composer.json << 'EOF'
{
    "scripts": {
        "check": "phpcs",
        "fix": "phpcbf",
        "analyse": "phpstan analyse",
        "test": "phpunit",
        "quality": [
            "@check",
            "@analyse",
            "@test"
        ]
    }
}
EOF
```

#### Key Standards

- Use PSR-4 autoloading
- Follow PSR-12 coding style
- Implement comprehensive tests
- Use semantic versioning
- Document public APIs
- Handle errors properly

**Reference**: See `docs/policy/generic-php-standard.md` for complete guidelines.

## Repository Configuration

### Branch Protection

Configure branch protection to enforce standards:

```yaml
# Example: .github/branch-protection.yml (requires GitHub App)
main:
  required_status_checks:
    strict: true
    contexts:
      - CI Validation
      - PHP Quality Checks
  required_pull_request_reviews:
    required_approving_review_count: 1
  enforce_admins: false
  restrictions: null
```

### Required Checks

Define required checks in workflow:

```yaml
jobs:
  required-checks:
    name: Required Quality Checks
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: File header validation
        run: |
          git clone https://github.com/mokoconsulting-tech/MokoStandards.git
          python3 MokoStandards/scripts/validate_file_headers.py
          
      - name: Documentation check
        run: python3 MokoStandards/scripts/check_documentation.py
```

### Workflow Permissions

Set appropriate permissions for workflows:

```yaml
permissions:
  contents: read        # Read repository contents
  pull-requests: write  # Comment on PRs
  checks: write         # Create check runs
  issues: write         # Create issues (optional)
```

## Quality Checks and Validation

### File Header Validation

Ensure all files have proper copyright headers:

```bash
# Download validation script
curl -O https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/scripts/validate_file_headers.py

# Run validation
python3 validate_file_headers.py

# Auto-fix headers (if supported)
python3 validate_file_headers.py --fix
```

### Documentation Completeness

Check that documentation is complete:

```bash
# Download documentation checker
curl -O https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/scripts/check_documentation.py

# Run check
python3 check_documentation.py

# Generate missing documentation templates
python3 check_documentation.py --generate
```

### Workflow Linting

Validate workflow files:

```bash
# Download workflow linter
curl -O https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/scripts/lint_workflows.py

# Run linter
python3 lint_workflows.py .github/workflows/

# Auto-fix issues
python3 lint_workflows.py --fix .github/workflows/
```

### Security Scanning

Run security scans on dependencies:

```yaml
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Composer security scan
        run: composer audit
        
      - name: NPM security scan
        if: hashFiles('package-lock.json')
        run: npm audit --production
```

## Continuous Integration Setup

### Minimal CI Configuration

Minimal setup for basic validation:

```yaml
name: Minimal CI

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with:
          php-version: '8.1'
      - run: composer install
      - run: composer test
```

### Standard CI Configuration

Standard setup with quality checks:

```yaml
name: Standard CI

on:
  push:
    branches: [main, dev/**]
  pull_request:

permissions:
  contents: read
  pull-requests: write
  checks: write

jobs:
  ci-validation:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      profile: standard
      
  php-quality:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-php-quality.yml@main
    with:
      php-version: '8.1'
      phpcs-standard: PSR-12
      phpstan-level: 6
```

### Full CI Configuration

Comprehensive setup with all checks:

```yaml
name: Full CI Pipeline

on:
  push:
    branches: [main, dev/**, rc/**]
  pull_request:
    branches: [main]

permissions:
  contents: read
  pull-requests: write
  checks: write
  security-events: write

jobs:
  ci-validation:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
    with:
      profile: full
      
  php-quality:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-php-quality.yml@main
    with:
      php-version: '8.1'
      phpcs-standard: PSR-12
      phpstan-level: 8
      coverage-threshold: 80
      
  joomla-testing:
    if: contains(github.repository, 'joomla')
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-joomla-testing.yml@main
    with:
      joomla-version: '4.4'
      php-version: '8.1'
      
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Dependency scan
        run: composer audit
```

## Best Practices

### 1. Start Small, Iterate

Begin with minimal validation and gradually add checks:

**Phase 1: Basic Validation**
- File header validation
- Basic lint checks
- Syntax validation

**Phase 2: Code Quality**
- Coding standard enforcement (PHPCS)
- Static analysis (PHPStan)
- Basic test execution

**Phase 3: Comprehensive**
- Full test coverage requirements
- Security scanning
- Performance testing
- Documentation generation

### 2. Use Workflow Inputs for Flexibility

Make workflows configurable:

```yaml
on:
  workflow_call:
    inputs:
      php-version:
        description: 'PHP version to test against'
        required: false
        type: string
        default: '8.1'
      coverage-threshold:
        description: 'Minimum code coverage percentage'
        required: false
        type: number
        default: 80
```

### 3. Cache Dependencies

Speed up workflows with caching:

```yaml
steps:
  - uses: actions/cache@v3
    with:
      path: vendor
      key: ${{ runner.os }}-composer-${{ hashFiles('**/composer.lock') }}
      restore-keys: |
        ${{ runner.os }}-composer-
```

### 4. Provide Clear Feedback

Ensure workflow failures are actionable:

```yaml
steps:
  - name: Run PHPCS
    run: vendor/bin/phpcs --report=full --report=summary
    
  - name: Comment on PR
    if: failure() && github.event_name == 'pull_request'
    uses: actions/github-script@v7
    with:
      script: |
        github.rest.issues.createComment({
          issue_number: context.issue.number,
          owner: context.repo.owner,
          repo: context.repo.repo,
          body: 'Coding standard violations found. Run `composer fix` to auto-fix.'
        })
```

### 5. Document Your Configuration

Include clear documentation in your repository:

```markdown
# Development Setup

## Quality Standards

This project uses MokoStandards for quality validation.

### Local Testing

```bash
# Install dependencies
composer install

# Run quality checks
composer check       # Run PHPCS
composer analyse     # Run PHPStan
composer test        # Run PHPUnit
composer quality     # Run all checks
```

### CI Pipeline

The CI pipeline runs automatically on push and PR. It includes:
- File header validation
- Coding standard checks (PSR-12)
- Static analysis (PHPStan level 6)
- Unit tests with coverage
```

### 6. Monitor and Adjust

Regularly review workflow performance:

- Check workflow execution times
- Identify bottlenecks
- Adjust caching strategies
- Update tool versions
- Review failure patterns

### 7. Keep Standards Updated

Stay current with MokoStandards:

```yaml
# Use version tags for stability
uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@v1.2.3

# Or use main for latest (less stable)
uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-ci-validation.yml@main
```

## Troubleshooting

### Common Issues

#### Workflow Not Running

**Problem**: Workflow doesn't execute on push/PR

**Solution**:
```bash
# Check workflow syntax
cat .github/workflows/ci.yml

# Verify trigger configuration
grep -A 5 "^on:" .github/workflows/ci.yml

# Check repository permissions
# Settings > Actions > General > Workflow permissions
```

#### Failed Quality Checks

**Problem**: PHPCS or PHPStan failures

**Solution**:
```bash
# Run locally to see detailed errors
vendor/bin/phpcs --standard=PSR-12 src/

# Auto-fix coding standard issues
vendor/bin/phpcbf --standard=PSR-12 src/

# Run PHPStan with verbose output
vendor/bin/phpstan analyse --level=6 --verbose src/
```

#### Missing Dependencies

**Problem**: Workflow fails with missing dependencies

**Solution**:
```yaml
steps:
  - uses: actions/checkout@v4
  
  - uses: shivammathur/setup-php@v2
    with:
      php-version: '8.1'
      extensions: mbstring, xml, pdo_mysql
      
  - name: Validate composer.json
    run: composer validate
    
  - name: Install dependencies
    run: composer install --prefer-dist --no-progress
```

## Related Documentation

- [Two-Tier Architecture](TWO_TIER_ARCHITECTURE.md) - Understanding the public/private separation
- [Standards Coordination](../STANDARDS_COORDINATION.md) - How standards are coordinated
- [Joomla Development Standard](policy/joomla-development-standard.md) - Joomla-specific guidelines
- [Security Scanning Standard](policy/security-scanning-standard.md) - Security requirements
- [Contributing Guidelines](../CONTRIBUTING.md) - How to contribute to MokoStandards

## Support

### For Questions

- Open an issue in the MokoStandards repository
- Check existing issues for similar problems
- Review workflow documentation

### For Contributions

- Submit improvements via pull requests
- Suggest new standards or workflows
- Report bugs or inconsistencies

---

## Metadata

| Field      | Value                                                                                                        |
| ---------- | ------------------------------------------------------------------------------------------------------------ |
| Document   | Repository Standards Application                                                                             |
| Path       | /docs/REPOSITORY_STANDARDS_APPLICATION.md                                                                    |
| Repository | [https://github.com/mokoconsulting-tech/MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards) |
| Owner      | Moko Consulting                                                                                              |
| Scope      | Standards application guide                                                                                  |
| Status     | Published                                                                                                    |
| Effective  | 2026-01-17                                                                                                   |

## Revision History

| Date       | Change Description                                      | Author          |
| ---------- | ------------------------------------------------------- | --------------- |
| 2026-01-17 | Initial creation, standards application documentation   | Moko Consulting |
