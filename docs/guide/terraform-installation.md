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
DEFGROUP: MokoStandards.Guide
INGROUP: MokoStandards.Documentation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: docs/guide/terraform-installation.md
VERSION: 04.00.00
BRIEF: Guide for installing and using Terraform across organization repositories
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Terraform Installation Guide

**Version**: 1.0.0  
**Status**: Active  
**Last Updated**: 2026-02-11

## Table of Contents

- [Overview](#overview)
- [Why Terraform in All Repositories?](#why-terraform-in-all-repositories)
- [Installation Methods](#installation-methods)
- [Automated Distribution](#automated-distribution)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

---

## Overview

As part of the enterprise transformation (version 03.02.00), Terraform is now distributed to all organization repositories to enable Infrastructure as Code (IaC) capabilities across the organization.

### Key Benefits

✅ **Infrastructure as Code** - Version-controlled infrastructure definitions  
✅ **Consistent Environments** - Reproducible deployments across teams  
✅ **Automated Provisioning** - Streamlined infrastructure setup  
✅ **GitOps Workflows** - Infrastructure changes through pull requests  
✅ **Multi-Cloud Support** - AWS, Azure, GCP, GitHub, and more

---

## Why Terraform in All Repositories?

### Enterprise Requirements

1. **Repository Management**
   - Automated repository setup and configuration
   - Consistent standards enforcement via Terraform
   - Dynamic file distribution system

2. **Infrastructure Consistency**
   - Standardized infrastructure patterns
   - Reusable modules and configurations
   - Centralized state management

3. **Compliance & Audit**
   - Infrastructure changes tracked in Git
   - Automated compliance checking
   - Audit trail for all infrastructure modifications

4. **Development Workflows**
   - Infrastructure setup in CI/CD pipelines
   - Automated testing environments
   - Preview deployments for pull requests

---

## Installation Methods

### Method 1: Bash Script (Linux/macOS)

```bash
# Navigate to your repository
cd /path/to/your/repo

# Run the installation script
./scripts/automation/install_terraform.sh

# Verify installation
terraform version
```

**Features:**
- Automatic platform detection (Linux/macOS/Windows)
- Architecture detection (amd64/arm64)
- Version checking and upgrade prompts
- Clean installation with proper permissions

### Method 2: Python Script (Cross-platform)

```bash
# Using Python script
./scripts/automation/install_terraform.py

# With custom version
./scripts/automation/install_terraform.py --version 1.7.5

# With custom install directory
./scripts/automation/install_terraform.py --install-dir ~/bin

# Verbose output
./scripts/automation/install_terraform.py --verbose
```

**Features:**
- Pure Python implementation (no shell dependencies)
- Progress bars for downloads
- JSON version detection
- Cross-platform compatibility

### Method 3: GitHub Actions (Automated)

Use the reusable workflow in your CI/CD:

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on: [push, pull_request]

jobs:
  terraform-check:
    uses: ./.github/workflows/terraform-setup.yml
    with:
      terraform_version: '1.7.4'
      working_directory: './terraform'
```

**Features:**
- Automatic setup in GitHub Actions
- Cached installations for faster builds
- Validation and formatting checks
- Reusable across workflows

### Method 4: Manual Installation

Download directly from HashiCorp:

1. Visit https://www.terraform.io/downloads
2. Download for your platform
3. Extract and move to `/usr/local/bin/` (or add to PATH)
4. Verify: `terraform version`

---

## Automated Distribution

### How Distribution Works

Terraform installation scripts are automatically distributed to all organization repositories via the bulk repository sync system:

1. **Files Distributed:**
   - `scripts/automation/install_terraform.sh` - Bash installation script
   - `scripts/automation/install_terraform.py` - Python installation script
   - `.github/workflows/terraform-setup.yml` - Reusable workflow

2. **Distribution Mechanism:**
   - Defined in `terraform/repository-management/main.tf`
   - Synced monthly via `bulk-repo-sync.yml` workflow
   - Can be manually triggered for immediate deployment

3. **Repository Control:**
   - Repositories can opt-out via `MokoStandards.override.tf`
   - Custom Terraform versions supported
   - Local modifications preserved

### Checking Distribution Status

```bash
# Check if Terraform installation files exist
ls -la scripts/automation/install_terraform.*
ls -la .github/workflows/terraform-setup.yml

# If files are missing, trigger bulk sync
# (from MokoStandards repository)
gh workflow run bulk-repo-sync.yml -f target_repos="your-repo-name"
```

---

## Usage

### Basic Terraform Commands

```bash
# Initialize Terraform (downloads providers)
terraform init

# Validate configuration
terraform validate

# Plan changes (dry-run)
terraform plan

# Apply changes
terraform apply

# Show current state
terraform show

# Format Terraform files
terraform fmt -recursive

# Destroy infrastructure (be careful!)
terraform destroy
```

### Repository Setup Example

```bash
# 1. Create terraform directory
mkdir -p terraform
cd terraform

# 2. Create main.tf
cat > main.tf <<'EOF'
terraform {
  required_version = ">= 1.7.0"
  
  required_providers {
    github = {
      source  = "integrations/github"
      version = "~> 6.0"
    }
  }
}

provider "github" {
  token = var.github_token
  owner = "mokoconsulting-tech"
}

variable "github_token" {
  description = "GitHub token"
  type        = string
  sensitive   = true
}
EOF

# 3. Initialize
terraform init

# 4. Validate
terraform validate
```

### Using in CI/CD

```yaml
name: Infrastructure Check

on:
  push:
    paths:
      - 'terraform/**'
  pull_request:
    paths:
      - 'terraform/**'

jobs:
  terraform:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Terraform
        uses: ./.github/workflows/terraform-setup.yml
        with:
          terraform_version: '1.7.4'
      
      - name: Terraform Format Check
        working-directory: ./terraform
        run: terraform fmt -check
      
      - name: Terraform Validate
        working-directory: ./terraform
        run: |
          terraform init -backend=false
          terraform validate
```

---

## Troubleshooting

### Common Issues

#### 1. Permission Denied During Installation

**Problem:** Cannot write to `/usr/local/bin/`

**Solution:**
```bash
# Use custom install directory
./scripts/automation/install_terraform.py --install-dir ~/bin

# Or run with sudo (Bash script will prompt)
sudo ./scripts/automation/install_terraform.sh
```

#### 2. Terraform Command Not Found

**Problem:** Terraform installed but command not found

**Solution:**
```bash
# Check if Terraform is in PATH
which terraform

# Add to PATH if needed (add to ~/.bashrc or ~/.zshrc)
export PATH="$PATH:$HOME/bin"

# Or create symlink
sudo ln -s ~/bin/terraform /usr/local/bin/terraform
```

#### 3. Version Mismatch

**Problem:** Wrong Terraform version installed

**Solution:**
```bash
# Check current version
terraform version

# Reinstall specific version
./scripts/automation/install_terraform.sh
# Answer 'y' when prompted to upgrade/downgrade

# Or specify version explicitly
export TERRAFORM_VERSION=1.7.4
./scripts/automation/install_terraform.sh
```

#### 4. Download Fails

**Problem:** Cannot download from HashiCorp

**Solution:**
```bash
# Check internet connectivity
ping releases.hashicorp.com

# Try with curl manually
curl -L https://releases.hashicorp.com/terraform/1.7.4/terraform_1.7.4_linux_amd64.zip -o terraform.zip

# Check firewall/proxy settings
# You may need to configure HTTP_PROXY environment variables
```

#### 5. Script Files Missing

**Problem:** Installation scripts not found in repository

**Solution:**
```bash
# Trigger bulk sync from MokoStandards
# (requires access to MokoStandards repository)
gh workflow run bulk-repo-sync.yml -f target_repos="$(basename $(pwd))"

# Or manually copy files from MokoStandards
cp /path/to/MokoStandards/scripts/automation/install_terraform.* scripts/automation/
cp /path/to/MokoStandards/.github/workflows/terraform-setup.yml .github/workflows/
```

---

## Best Practices

### 1. Version Management

```bash
# Use consistent version across team
# Define in .terraform-version or environment variable
echo "1.7.4" > .terraform-version

# Or use environment variable
export TERRAFORM_VERSION=1.7.4
```

### 2. State Management

```hcl
# Use remote state for team collaboration
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "repository-name/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

### 3. Security

```bash
# Never commit sensitive data
# Use .gitignore
cat >> .gitignore <<'EOF'
# Terraform
.terraform/
*.tfstate
*.tfstate.*
.terraform.lock.hcl
terraform.tfvars
EOF

# Use environment variables or secret managers
export TF_VAR_github_token="${GITHUB_TOKEN}"
terraform apply
```

### 4. Code Organization

```
repository/
├── terraform/
│   ├── modules/           # Reusable modules
│   │   ├── network/
│   │   └── compute/
│   ├── environments/      # Environment-specific configs
│   │   ├── dev/
│   │   ├── staging/
│   │   └── prod/
│   ├── main.tf           # Main configuration
│   ├── variables.tf      # Input variables
│   ├── outputs.tf        # Output values
│   └── versions.tf       # Provider versions
└── scripts/
    └── automation/
        ├── install_terraform.sh
        └── install_terraform.py
```

### 5. CI/CD Integration

```yaml
# Always validate in CI
- name: Terraform Checks
  run: |
    terraform fmt -check -recursive
    terraform init -backend=false
    terraform validate
    
# Use plan for PRs
- name: Terraform Plan
  if: github.event_name == 'pull_request'
  run: terraform plan -no-color
  
# Apply only on main branch
- name: Terraform Apply
  if: github.ref == 'refs/heads/main'
  run: terraform apply -auto-approve
```

---

## Additional Resources

### Documentation
- [Official Terraform Docs](https://www.terraform.io/docs)
- [Terraform GitHub Provider](https://registry.terraform.io/providers/integrations/github/latest/docs)
- [MokoStandards Terraform Guide](./terraform-override-files.md)

### Internal Resources
- [Terraform Repository Management](../../terraform/repository-management/)
- [Terraform Repository Types](../../terraform/repository-types/)
- [Enterprise Transformation Guide](../planning/README.md)

### Support
- **Issues**: Report problems via GitHub Issues
- **Questions**: Use GitHub Discussions
- **Training**: See [docs/training/](../training/)

---

**Last Updated**: 2026-02-11  
**Document Owner**: MokoStandards Team  
**Status**: Active  
**Review Schedule**: Quarterly
