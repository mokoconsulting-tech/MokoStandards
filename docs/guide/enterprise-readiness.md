# Enterprise Readiness Guide

![Version](https://img.shields.io/badge/version-03.02.00-blue) ![Enterprise Ready](https://img.shields.io/badge/enterprise-ready-green)

**Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>**

**SPDX-License-Identifier: GPL-3.0-or-later**

This guide explains what makes a repository "enterprise-ready" and provides comprehensive instructions for achieving enterprise compliance across all MokoConsulting repositories.

---

## Table of Contents

1. [What is Enterprise Readiness?](#what-is-enterprise-readiness)
2. [Enterprise Readiness Checklist](#enterprise-readiness-checklist)
3. [Required Components](#required-components)
4. [Automated Setup](#automated-setup)
5. [Manual Setup](#manual-setup)
6. [Verification](#verification)
7. [Troubleshooting](#troubleshooting)
8. [Examples](#examples)
9. [Maintenance](#maintenance)

---

## What is Enterprise Readiness?

**Enterprise Readiness** is a comprehensive compliance framework that ensures repositories meet organizational standards for:

- **Audit Logging**: Comprehensive tracking of all operations for compliance
- **Security Validation**: Automated security scanning and vulnerability detection
- **Health Monitoring**: Continuous monitoring of repository health and performance
- **Error Recovery**: Robust error handling and transaction management
- **Configuration Management**: Centralized configuration with override capabilities
- **Standardization**: Consistent structure, metadata, and tooling across all repositories

### Benefits of Enterprise Readiness

- ✅ **Compliance**: Meet regulatory and organizational requirements
- ✅ **Security**: Automated security scanning and vulnerability management
- ✅ **Reliability**: Robust error handling and recovery mechanisms
- ✅ **Visibility**: Comprehensive logging and monitoring
- ✅ **Maintainability**: Standardized structure and tooling
- ✅ **Automation**: Reduced manual work through automated workflows

### Enterprise Readiness Score

Repositories are scored on a 0-100% scale based on:

| Score Range | Classification | Description |
|------------|----------------|-------------|
| 90-100% | **Fully Enterprise Ready** | All components present, excellent compliance |
| 80-89% | **Enterprise Ready** | Minor improvements recommended |
| 60-79% | **Partially Ready** | Several improvements needed |
| 40-59% | **Basic Features** | Significant work required |
| 0-39% | **Not Ready** | Major setup required |

**Minimum threshold for enterprise readiness: 80%**

---

## Enterprise Readiness Checklist

Use this checklist to assess and track enterprise readiness:

### Core Infrastructure (40 points)

- [ ] **Enterprise Libraries** (10 points)
  - [ ] `scripts/lib/enterprise_audit.py` - Audit logging framework
  - [ ] `scripts/lib/audit_logger.py` - Structured audit logs
  - [ ] `scripts/lib/validation_framework.py` - Validation infrastructure
  - [ ] `scripts/lib/unified_validation.py` - Unified validation APIs
  - [ ] `scripts/lib/config_manager.py` - Configuration management
  - [ ] `scripts/lib/security_validator.py` - Security validation
  - [ ] `scripts/lib/error_recovery.py` - Error handling and recovery
  - [ ] `scripts/lib/transaction_manager.py` - Transaction management
  - [ ] `scripts/lib/cli_framework.py` - CLI framework
  - [ ] `scripts/lib/common.py` - Common utilities

- [ ] **Enterprise Workflows** (10 points)
  - [ ] `.github/workflows/audit-log-archival.yml` - Audit log management
  - [ ] `.github/workflows/metrics-collection.yml` - Metrics collection
  - [ ] `.github/workflows/health-check.yml` - Health monitoring
  - [ ] `.github/workflows/security-scan.yml` - Security scanning
  - [ ] `.github/workflows/integration-tests.yml` - Integration testing

- [ ] **Terraform Scripts** (10 points)
  - [ ] `scripts/automation/install_terraform.sh` - Terraform installer (shell)
  - [ ] `scripts/automation/install_terraform.py` - Terraform installer (Python)

- [ ] **Version Documentation** (10 points)
  - [ ] README.md has version badge (03.02.00)
  - [ ] CHANGELOG.md exists and is current
  - [ ] Version badges use correct format

### Configuration & Metadata (30 points)

- [ ] **Override Configuration** (10 points)
  - [ ] `MokoStandards.override.tf` exists
  - [ ] Contains `override_metadata` block
  - [ ] Contains `sync_config` block
  - [ ] Version is 03.02.00 or later

- [ ] **Enterprise Metadata** (10 points)
  - [ ] Configuration files contain enterprise flags
  - [ ] `enterprise_ready = true` in configs
  - [ ] `monitoring_enabled = true` in configs
  - [ ] `audit_logging = true` in configs

- [ ] **Monitoring Setup** (10 points)
  - [ ] `logs/` directory exists
  - [ ] `logs/audit/` directory exists
  - [ ] `logs/metrics/` directory exists
  - [ ] Monitoring documentation present

### Documentation & Standards (30 points)

- [ ] **Core Documentation**
  - [ ] README.md with project overview
  - [ ] CHANGELOG.md with version history
  - [ ] CONTRIBUTING.md with contribution guidelines
  - [ ] LICENSE file present

- [ ] **Enterprise Documentation**
  - [ ] Enterprise readiness documentation
  - [ ] Architecture documentation
  - [ ] Deployment guides
  - [ ] Troubleshooting guides

---

## Required Components

### 1. Enterprise Libraries (10 Required)

Located in `scripts/lib/`, these provide core enterprise functionality:

#### `enterprise_audit.py`
Comprehensive audit logging with:
- Structured JSON logging
- Transaction ID tracking
- Security event logging
- Audit log rotation

```python
from scripts.lib.enterprise_audit import AuditLogger

logger = AuditLogger()
logger.log_event('user.login', {'user_id': 123})
```

#### `audit_logger.py`
Structured audit logging to database/files:
- Who, what, when, where tracking
- Compliance reporting
- Automated archival

#### `validation_framework.py`
Validation infrastructure for all checks:
- Consistent validation patterns
- Error collection and reporting
- Validation result aggregation

#### `unified_validation.py`
Unified validation APIs across all validators:
- Single interface for all validations
- Consistent error handling
- Validation orchestration

#### `config_manager.py`
Centralized configuration management:
- Environment-aware configuration
- Override support
- Secure credential handling

#### `security_validator.py`
Security validation and scanning:
- Credential detection
- Vulnerability scanning
- Security best practices

#### `error_recovery.py`
Robust error handling:
- Automatic retry logic
- Graceful degradation
- Transaction rollback

#### `transaction_manager.py`
Transaction management for atomic operations:
- ACID compliance
- Rollback support
- Transaction logging

#### `cli_framework.py`
CLI framework for consistent interfaces:
- Argument parsing
- Output formatting
- Error handling

#### `common.py`
Common utilities shared across scripts:
- File operations
- String utilities
- Data structures

### 2. Enterprise Workflows (5 Required)

Located in `.github/workflows/`, these automate enterprise operations:

#### `audit-log-archival.yml`
- Archives audit logs weekly
- Compresses and stores historical logs
- Maintains compliance with retention policies

#### `metrics-collection.yml`
- Collects repository metrics daily
- Tracks performance indicators
- Generates reports

#### `health-check.yml`
- Monitors repository health continuously
- Checks dependencies, workflows, and files
- Alerts on issues

#### `security-scan.yml`
- Runs comprehensive security scans
- Checks for vulnerabilities
- Enforces security policies

#### `integration-tests.yml`
- Tests enterprise library integration
- Validates cross-component functionality
- Ensures compatibility

### 3. Terraform Scripts (2 Required)

Located in `scripts/automation/`:

#### `install_terraform.sh`
Shell script for Terraform installation:
- Platform detection
- Version management
- Automated download and installation

#### `install_terraform.py`
Python script for Terraform installation:
- Cross-platform support
- Version verification
- Integration with enterprise workflows

### 4. Monitoring Infrastructure

Required directory structure:

```
logs/
├── README.md              # Logging documentation
├── audit/                 # Audit logs
│   ├── .gitkeep
│   └── *.json            # Audit log files
├── metrics/              # Performance metrics
│   ├── .gitkeep
│   └── *.json            # Metrics files
└── validation/           # Validation results
    ├── .gitkeep
    └── *.json            # Validation results
```

### 5. Configuration Files

#### `MokoStandards.override.tf`
Terraform configuration for sync behavior:

```hcl
locals {
  override_metadata = {
    name           = "Repository Override"
    version        = "03.02.00"
    enterprise_ready = true
    monitoring_enabled = true
    audit_logging = true
  }
  
  sync_config = {
    enabled = true
    cleanup_mode = "conservative"
  }
  
  exclude_files = [
    # Repository-specific exclusions
  ]
  
  protected_files = [
    # Files that should never be overwritten
  ]
}
```

---

## Automated Setup

The **fastest and recommended** way to achieve enterprise readiness is using the automated setup script.

### Prerequisites

- Python 3.8 or later
- Access to MokoStandards repository
- Write permissions to target repository

### Quick Start

```bash
# Clone or access MokoStandards
cd /path/to/MokoStandards

# Run automated setup on target repository
python scripts/automation/setup_enterprise_repo.py --path /path/to/target-repo
```

### Interactive Setup

The script will guide you through:

1. Creating required directories
2. Installing enterprise libraries
3. Installing enterprise workflows
4. Installing Terraform scripts
5. Creating override configuration
6. Adding version badges
7. Setting up monitoring

**Respond to prompts with `y` (yes) or `n` (no).**

### Non-Interactive Setup

For CI/CD or automation:

```bash
python scripts/automation/setup_enterprise_repo.py \
  --path /path/to/repo \
  --no-interactive \
  --source-path /path/to/MokoStandards
```

### Dry Run Mode

Preview changes without applying them:

```bash
python scripts/automation/setup_enterprise_repo.py \
  --path /path/to/repo \
  --dry-run \
  --verbose
```

### Selective Installation

Install only specific components:

```bash
# Install only libraries
python scripts/automation/setup_enterprise_repo.py --install-libraries

# Install only workflows
python scripts/automation/setup_enterprise_repo.py --install-workflows

# Create only directories
python scripts/automation/setup_enterprise_repo.py --create-dirs

# Create only override config
python scripts/automation/setup_enterprise_repo.py --create-override
```

---

## Manual Setup

For fine-grained control or learning purposes, you can set up components manually.

### Step 1: Create Directory Structure

```bash
mkdir -p scripts/lib
mkdir -p scripts/automation
mkdir -p scripts/validate
mkdir -p .github/workflows
mkdir -p logs/audit
mkdir -p logs/metrics
mkdir -p logs/validation
mkdir -p docs/guide

# Create .gitkeep files
touch logs/audit/.gitkeep
touch logs/metrics/.gitkeep
touch logs/validation/.gitkeep
```

### Step 2: Copy Enterprise Libraries

From MokoStandards repository:

```bash
# Copy all enterprise libraries
cp MokoStandards/scripts/lib/enterprise_audit.py scripts/lib/
cp MokoStandards/scripts/lib/audit_logger.py scripts/lib/
cp MokoStandards/scripts/lib/validation_framework.py scripts/lib/
cp MokoStandards/scripts/lib/unified_validation.py scripts/lib/
cp MokoStandards/scripts/lib/config_manager.py scripts/lib/
cp MokoStandards/scripts/lib/security_validator.py scripts/lib/
cp MokoStandards/scripts/lib/error_recovery.py scripts/lib/
cp MokoStandards/scripts/lib/transaction_manager.py scripts/lib/
cp MokoStandards/scripts/lib/cli_framework.py scripts/lib/
cp MokoStandards/scripts/lib/common.py scripts/lib/

# Make them executable
chmod +x scripts/lib/*.py
```

### Step 3: Copy Enterprise Workflows

```bash
# Copy all enterprise workflows
cp MokoStandards/.github/workflows/audit-log-archival.yml .github/workflows/
cp MokoStandards/.github/workflows/metrics-collection.yml .github/workflows/
cp MokoStandards/.github/workflows/health-check.yml .github/workflows/
cp MokoStandards/.github/workflows/security-scan.yml .github/workflows/
cp MokoStandards/.github/workflows/integration-tests.yml .github/workflows/
```

### Step 4: Copy Terraform Scripts

```bash
cp MokoStandards/scripts/automation/install_terraform.sh scripts/automation/
cp MokoStandards/scripts/automation/install_terraform.py scripts/automation/
chmod +x scripts/automation/install_terraform.*
```

### Step 5: Create Override Configuration

Create `MokoStandards.override.tf`:

```hcl
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
# SPDX-License-Identifier: GPL-3.0-or-later

locals {
  override_metadata = {
    name           = "Repository Override Configuration"
    description    = "Override configuration for repository"
    version        = "03.02.00"
    last_updated   = "2026-02-11T00:00:00Z"
    maintainer     = "MokoStandards Team"
    schema_version = "2.0"
    repository_url = "https://github.com/mokoconsulting-tech/repository-name"
    repository_type = "generic"
    enterprise_ready = true
    monitoring_enabled = true
    audit_logging = true
  }

  sync_config = {
    enabled = true
    cleanup_mode = "conservative"
  }

  exclude_files = []
  protected_files = [
    {
      path   = ".gitignore"
      reason = "Repository-specific ignore patterns"
    },
    {
      path   = "MokoStandards.override.tf"
      reason = "This override file itself"
    },
  ]
}
```

### Step 6: Add Version Badges

Add to the top of `README.md` (after the first heading):

```markdown
![Version](https://img.shields.io/badge/version-03.02.00-blue) ![Enterprise Ready](https://img.shields.io/badge/enterprise-ready-green)
```

### Step 7: Configure Package Metadata

#### For Python projects (`pyproject.toml`):

```toml
[tool.mokostandards]
enterprise_ready = true
monitoring_enabled = true
audit_logging = true
version = "03.02.00"
```

#### For Node.js projects (`package.json`):

```json
{
  "mokostandards": {
    "enterprise_ready": true,
    "monitoring_enabled": true,
    "audit_logging": true,
    "version": "03.02.00"
  }
}
```

#### For PHP projects (`composer.json`):

```json
{
  "extra": {
    "mokostandards": {
      "enterprise_ready": true,
      "monitoring_enabled": true,
      "audit_logging": true,
      "version": "03.02.00"
    }
  }
}
```

---

## Verification

After setup (automated or manual), verify enterprise readiness:

### Run Enterprise Readiness Checker

```bash
python scripts/validate/check_enterprise_readiness.py
```

**Expected output:**

```
======================================================================
              ENTERPRISE READINESS REPORT                
======================================================================

Repository: /path/to/repository

Overall Score: 100/100 (100.0%)

Summary: ✓ Repository is FULLY enterprise-ready with excellent compliance

Detailed Checks:

  ✓ Enterprise Libraries
    Score: 10/10
    Enterprise libraries: 10/10 present

  ✓ Enterprise Workflows
    Score: 5/5
    Enterprise workflows: 5/5 present

  ✓ Terraform Scripts
    Score: 2/2
    Terraform scripts: 2/2 present

  ✓ Version Badges
    Score: 3/3
    Version badges: 3/3 documents

  ✓ Override Configuration
    Score: 10/10
    MokoStandards.override.tf: PRESENT and up-to-date

  ✓ Enterprise Metadata
    Score: 10/10
    Enterprise metadata: present in configurations

  ✓ Monitoring Setup
    Score: 9/9
    Monitoring directories: 3/3 present

======================================================================
```

### Verbose Mode

For detailed information:

```bash
python scripts/validate/check_enterprise_readiness.py --verbose
```

### JSON Output

For programmatic use:

```bash
python scripts/validate/check_enterprise_readiness.py --json
```

### Exit Codes

- `0` - Repository is enterprise-ready (≥80% score)
- `1` - Repository is not enterprise-ready (<80% score)
- `2` - Error during checking

---

## Troubleshooting

### Issue: "MokoStandards source not found"

**Solution 1:** Specify source path explicitly:

```bash
python scripts/automation/setup_enterprise_repo.py \
  --source-path /path/to/MokoStandards
```

**Solution 2:** Clone MokoStandards to parent directory:

```bash
cd /path/to/parent
git clone https://github.com/mokoconsulting-tech/MokoStandards.git
cd target-repo
python ../MokoStandards/scripts/automation/setup_enterprise_repo.py
```

### Issue: "Permission denied" errors

**Solution:** Ensure you have write permissions:

```bash
# Check permissions
ls -la

# Fix ownership (if needed)
sudo chown -R $USER:$USER .

# Try again
python scripts/automation/setup_enterprise_repo.py
```

### Issue: Low enterprise readiness score

**Solution:** Run checker with verbose output:

```bash
python scripts/validate/check_enterprise_readiness.py --verbose
```

Review recommendations and address each issue:

1. Missing libraries → Run `--install-libraries`
2. Missing workflows → Run `--install-workflows`
3. Missing directories → Run `--create-dirs`
4. Missing override config → Run `--create-override`

### Issue: Version badges not recognized

**Solution:** Ensure correct format:

```markdown
![Version](https://img.shields.io/badge/version-03.02.00-blue)
```

Version **must** match pattern: `03.0[12].0[0-9]`

### Issue: Override config validation fails

**Solution:** Verify required sections:

```hcl
locals {
  override_metadata = {
    version = "03.02.00"  # Must be present
    enterprise_ready = true
    # ... other fields
  }
  
  sync_config = {
    enabled = true
    cleanup_mode = "conservative"
  }
}
```

---

## Examples

### Example 1: New Repository Setup

Setting up a brand new repository:

```bash
# Create repository structure
mkdir my-new-repo
cd my-new-repo
git init

# Create basic files
echo "# My New Repository" > README.md
echo "Initial version" > CHANGELOG.md
git add .
git commit -m "Initial commit"

# Run enterprise setup
python /path/to/MokoStandards/scripts/automation/setup_enterprise_repo.py

# Verify
python scripts/validate/check_enterprise_readiness.py
```

### Example 2: Upgrading Existing Repository

Upgrading an existing repository to enterprise-ready:

```bash
cd existing-repo

# Backup current state
git checkout -b enterprise-upgrade

# Run setup (dry-run first)
python /path/to/MokoStandards/scripts/automation/setup_enterprise_repo.py --dry-run

# Apply changes
python /path/to/MokoStandards/scripts/automation/setup_enterprise_repo.py

# Verify
python scripts/validate/check_enterprise_readiness.py

# Commit changes
git add .
git commit -m "chore: Upgrade to enterprise-ready status"
git push origin enterprise-upgrade
```

### Example 3: CI/CD Integration

Integrating checks into CI/CD pipeline (`.github/workflows/enterprise-check.yml`):

```yaml
name: Enterprise Readiness Check

on:
  push:
    branches: [main, develop]
  pull_request:

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Run enterprise readiness check
        run: |
          python scripts/validate/check_enterprise_readiness.py --json > report.json
          cat report.json
      
      - name: Verify minimum score
        run: |
          score=$(jq '.score.percentage' report.json)
          if (( $(echo "$score < 80" | bc -l) )); then
            echo "Enterprise readiness score $score% is below minimum 80%"
            exit 1
          fi
```

---

## Maintenance

### Regular Updates

Enterprise components should be updated regularly:

```bash
# Check for updates (from MokoStandards)
cd /path/to/MokoStandards
git pull

# Re-run setup to update components
cd /path/to/target-repo
python /path/to/MokoStandards/scripts/automation/setup_enterprise_repo.py
```

### Monitoring Health

Use enterprise workflows to monitor ongoing health:

- **Daily**: Metrics collection runs automatically
- **Weekly**: Audit log archival runs automatically
- **Continuous**: Health checks run on every push

Review logs in:
- `logs/audit/` - Audit events
- `logs/metrics/` - Performance metrics
- `logs/validation/` - Validation results

### Updating Version

When MokoStandards version changes:

1. Update `MokoStandards.override.tf` version
2. Update version badges in documentation
3. Update package metadata
4. Run enterprise readiness checker
5. Commit changes

```bash
# Update version in all files
find . -type f -name "*.md" -exec sed -i 's/03\.01\.00/03.02.00/g' {} +
find . -type f -name "*.tf" -exec sed -i 's/03\.01\.00/03.02.00/g' {} +

# Verify
python scripts/validate/check_enterprise_readiness.py
```

---

## Support

For questions or issues:

1. **Documentation**: Check this guide and other docs in `docs/`
2. **Issues**: Open an issue in MokoStandards repository
3. **Contact**: Reach out to hello@mokoconsulting.tech

---

## License

This guide is part of MokoStandards and is licensed under GPL-3.0-or-later.

Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

---

## Revision History

- **2026-02-11**: Initial version 03.02.00
- Added comprehensive enterprise readiness documentation
- Included automated and manual setup instructions
- Added troubleshooting and examples
