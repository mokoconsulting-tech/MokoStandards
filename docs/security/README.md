[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.01-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Security Documentation Index

This directory contains security documentation for MokoStandards repositories.

## Quick Start

- **[Security Scanning Guide](./security-scanning-guide.md)** - Implementation guide for deploying security scanning to repositories
- **[Security Scanning Usage](./SECURITY_SCANNING.md)** - Day-to-day usage of security scanning tools

## Documentation Files

### Implementation Guides

| Document | Purpose | Audience |
|----------|---------|----------|
| [security-scanning-guide.md](./security-scanning-guide.md) | Step-by-step guide for implementing security scanning | Repository administrators |
| [SECURITY_SCANNING.md](./SECURITY_SCANNING.md) | Daily usage guide for security scanning tools | Developers |

### Policy Documents

| Document | Location | Purpose |
|----------|----------|---------|
| [security-scanning.md](../policy/security-scanning.md) | Policy requirements | All teams |
| [confidentiality-scan.md](../policy/security/confidentiality-scan.md) | Confidentiality scanning | Development teams |

## Deployment Checklist

When deploying to a new repository, copy these files:

### Required Files

- [ ] `.github/workflows/codeql-analysis.yml` - CodeQL workflow
- [ ] `scripts/validate/security_scan.py` - Orchestration script
- [ ] `scripts/validate/no_secrets.py` - Secret scanner
- [ ] `scripts/validate/validate_codeql_config.py` - Config validator

### Documentation Files (Copy These!)

- [ ] `docs/security/security-scanning-guide.md` - Implementation guide
- [ ] `docs/security/SECURITY_SCANNING.md` - Usage guide
- [ ] `docs/policy/security-scanning.md` - Policy (if applicable)

## Quick Reference

```bash
# Copy workflows
cp templates/workflows/codeql-analysis.yml.template .github/workflows/codeql-analysis.yml

# Copy scripts
cp scripts/validate/{security_scan,no_secrets,validate_codeql_config}.py scripts/validate/

# Copy documentation
mkdir -p docs/security
cp docs/security/{security-scanning-guide,SECURITY_SCANNING}.md docs/security/

# Validate and test
python3 scripts/validate/validate_codeql_config.py
python3 scripts/validate/security_scan.py --verbose
```

## Related Documentation

- [Security Policy](../../SECURITY.md) - Overall security policy
- [Policy: Security Scanning](../policy/security-scanning.md) - Detailed requirements
- [Workflows](../workflows/README.md) - GitHub Actions workflows

## Metadata

| Field | Value |
|-------|-------|
| Document Type | Index |
| Path | /docs/security/README.md |
| Version | 01.00.00 |
| Last Updated | 2026-01-28 |
