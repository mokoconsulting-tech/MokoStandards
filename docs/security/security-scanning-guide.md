<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

SPDX-License-Identifier: GPL-3.0-or-later

FILE INFORMATION
DEFGROUP: MokoStandards.Documentation
INGROUP: MokoStandards.Security
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/security/security-scanning-guide.md
VERSION: 03.01.01
BRIEF: Guide for implementing security scanning in org repositories
-->

# Security Scanning Implementation Guide

**Version**: 01.00.00 | **Status**: Active | **Last Updated**: 2026-01-28

## Overview

This guide provides instructions for implementing comprehensive security scanning in MokoStandards-governed repositories by copying the required scripts, workflows, and documentation.

## Quick Start

### Files to Copy to Your Repository

When implementing security scanning, copy these files from MokoStandards:

#### 1. Workflows
```bash
mkdir -p .github/workflows
cp templates/workflows/codeql-analysis.yml.template .github/workflows/codeql-analysis.yml
```

#### 2. Scripts
```bash
mkdir -p scripts/validate scripts/lib
cp scripts/validate/security_scan.py scripts/validate/
cp scripts/validate/no_secrets.py scripts/validate/
cp scripts/validate/validate_codeql_config.py scripts/validate/
chmod +x scripts/validate/*.py
```

#### 3. Documentation (IMPORTANT!)
```bash
mkdir -p docs/security docs/policy
cp docs/security/security-scanning-guide.md docs/security/
cp scripts/validate/SECURITY_SCANNING.md docs/security/
cp docs/policy/security-scanning.md docs/policy/  # If applicable
```

## Configuration

### Step 1: Update CodeQL Languages

Edit `.github/workflows/codeql-analysis.yml`:

```yaml
matrix:
  language: ['python']  # Adjust for your repository
```

### Step 2: Validate Configuration

```bash
python3 scripts/validate/validate_codeql_config.py
```

### Step 3: Test Security Scanning

```bash
python3 scripts/validate/security_scan.py --verbose
```

## Documentation Structure

After copying, your repository should have:

```
your-repo/
├── .github/
│   └── workflows/
│       └── codeql-analysis.yml
├── scripts/
│   └── validate/
│       ├── security_scan.py
│       ├── no_secrets.py
│       └── validate_codeql_config.py
└── docs/
    ├── security/
    │   ├── security-scanning-guide.md  # This file
    │   └── SECURITY_SCANNING.md        # Usage guide
    └── policy/
        └── security-scanning.md         # Policy (optional)
```

## Usage

See [SECURITY_SCANNING.md](./SECURITY_SCANNING.md) in your repository for:
- Complete usage instructions
- Troubleshooting
- Best practices
- CI/CD integration

## Quick Reference

```bash
# Run comprehensive scan
python3 scripts/validate/security_scan.py

# Validate CodeQL config
python3 scripts/validate/validate_codeql_config.py

# Scan for secrets
python3 scripts/validate/no_secrets.py .
```

## Maintenance

Update from MokoStandards periodically:

```bash
# Update scripts
cp /path/to/MokoStandards/scripts/validate/security_scan.py scripts/validate/

# Update workflows
cp /path/to/MokoStandards/templates/workflows/codeql-analysis.yml.template \
   .github/workflows/codeql-analysis.yml

# Update documentation
cp /path/to/MokoStandards/docs/security/security-scanning-guide.md docs/security/
cp /path/to/MokoStandards/scripts/validate/SECURITY_SCANNING.md docs/security/
```

## Support

- **Local Documentation**: See `docs/security/SECURITY_SCANNING.md` in your repository
- **MokoStandards**: https://github.com/mokoconsulting-tech/MokoStandards
- **Email**: security@mokoconsulting.tech

## Metadata

| Field | Value |
|-------|-------|
| Document | Security Scanning Implementation Guide |
| Version | 01.00.00 |
| Status | Active |
| Last Updated | 2026-01-28 |
