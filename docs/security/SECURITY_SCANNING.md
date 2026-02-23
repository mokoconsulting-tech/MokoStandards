[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.03-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Security Scanning Guide

**Version**: 01.00.00 | **Status**: Active | **Last Updated**: 2026-01-28

## Overview

This guide provides instructions for implementing and using the comprehensive security scanning infrastructure required for all MokoStandards repositories.

## Quick Start

### 1. Install CodeQL Workflow

Copy the CodeQL workflow template to your repository:

```bash
# From your repository root
mkdir -p .github/workflows
cp templates/workflows/codeql-analysis.yml.template .github/workflows/codeql-analysis.yml
```

### 2. Configure Languages

Edit `.github/workflows/codeql-analysis.yml` and update the language matrix to match your repository:

```yaml
matrix:
  language: ['python']  # Adjust based on your codebase
```

**Supported languages**: `cpp`, `csharp`, `go`, `java`, `javascript`, `python`, `ruby`

Note: The template currently includes Python. Adjust based on your repository contents.

### 3. Validate Configuration

Run the validation script to ensure your CodeQL configuration matches your codebase:

```bash
python3 scripts/validate/validate_codeql_config.py --repo-path .
```

### 4. Run Complete Security Scan

Execute the comprehensive security scan:

```bash
python3 scripts/validate/security_scan.py
```

## Security Scan Components

The security scanning infrastructure includes four main components:

### 1. CodeQL Analysis

**Purpose**: Static Application Security Testing (SAST) for code vulnerabilities

**What it scans**:
- SQL injection vulnerabilities
- Cross-site scripting (XSS)
- Path traversal issues
- Command injection
- Authentication bypasses
- And 200+ other security patterns

**How to run**:
- Automatically runs on push to main/dev/rc branches
- Runs on all pull requests
- Weekly scheduled scan on Mondays at 6:00 AM UTC
- Manual trigger via Actions tab

### 2. Secret Scanning

**Purpose**: Detect accidentally committed credentials and API keys

**What it scans**:
- Private keys (RSA, DSA, EC, SSH)
- AWS access keys
- GitHub tokens
- Slack tokens
- Stripe API keys
- And other sensitive patterns

**How to run**:
```bash
python3 scripts/validate/no_secrets.py .
```

### 3. Dependency Checking

**Purpose**: Identify vulnerable third-party dependencies

**What it checks**:
- Python packages (requirements.txt, pyproject.toml)
- JavaScript packages (package.json)
- PHP packages (composer.json)
- Ruby gems (Gemfile)
- Go modules (go.mod)

**How to run** (requires pip-audit):
```bash
pip install pip-audit
pip-audit --desc
```

### 4. Configuration Validation

**Purpose**: Ensure CodeQL configuration matches repository contents

**What it validates**:
- CodeQL workflow exists
- Configured languages match source files
- No misconfigured languages that cause CI failures

**How to run**:
```bash
python3 scripts/validate/validate_codeql_config.py
```

## Comprehensive Security Scan

The `security_scan.py` script orchestrates all security checks:

### Basic Usage

```bash
# Scan current directory
python3 scripts/validate/security_scan.py

# Scan specific repository
python3 scripts/validate/security_scan.py --repo-path /path/to/repo

# Verbose output
python3 scripts/validate/security_scan.py --verbose

# Generate JSON report
python3 scripts/validate/security_scan.py --json-output security-report.json
```

### Exit Codes

- `0`: All scans passed (no critical issues)
- `1`: Security issues found

### Report Format

The script generates a comprehensive report showing:

```
======================================================================
🛡️  SECURITY SCAN REPORT
======================================================================

Status: PASS/FAIL
Total Issues: X
  Critical: X
  High: X

----------------------------------------------------------------------
SCAN RESULTS
----------------------------------------------------------------------

✓ CODEQL: configured
✓ CONFIG: passed
✓ SECRETS: passed
✓ DEPENDENCIES: passed

----------------------------------------------------------------------
RECOMMENDATIONS
----------------------------------------------------------------------
1. [Actionable recommendations if issues found]

======================================================================
```

## CI/CD Integration

### GitHub Actions

The security scanning workflows are automatically triggered:

**CodeQL Analysis** (`.github/workflows/codeql-analysis.yml`):
- On push to main, dev/**, rc/**, version/** branches
- On pull requests to main, dev/**, rc/** branches
- Weekly schedule: Mondays at 6:00 AM UTC
- Manual workflow dispatch

**Results**: Available in the Security tab → Code scanning alerts

### Pre-commit Hook

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Run secret scanning before commit
python3 scripts/validate/no_secrets.py . || exit 1
```

### Pre-push Hook

Add to `.git/hooks/pre-push`:

```bash
#!/bin/bash
# Run comprehensive security scan before push
python3 scripts/validate/security_scan.py || exit 1
```

## Vulnerability Response

When security issues are found:

### Critical/High Severity

1. **Immediate Action**: Stop and assess the issue
2. **Triage**: Within 4 hours
3. **Fix**: Within 7 days (critical) or 14 days (high)
4. **Notify**: Security owner and team

### Medium/Low Severity

1. **Triage**: Within 48 hours
2. **Fix**: Within 30 days (medium) or 60 days (low)
3. **Plan**: Include in next sprint/release

### Dismissing Alerts

Only dismiss alerts with:
- Clear justification
- Risk assessment
- Compensating controls documented
- Security owner approval

## Troubleshooting

### CodeQL: "No supported languages found"

**Problem**: CodeQL workflow fails because configured languages don't exist in repository

**Solution**: Run validation script and adjust language matrix:
```bash
python3 scripts/validate/validate_codeql_config.py
# Update .github/workflows/codeql-analysis.yml with detected languages
```

### Secret Scanner: False Positives

**Problem**: Secret scanner flags example code or test data

**Solution**: Add exclusion to `scripts/validate/no_secrets.py` or update patterns

### Dependency Scanner: Tool Not Found

**Problem**: `pip-audit` or other scanners not installed

**Solution**: Install required tools:
```bash
pip install pip-audit
npm install -g npm-audit
```

## Best Practices

### 1. Run Locally Before Pushing

Always run security scans locally before pushing:
```bash
python3 scripts/validate/security_scan.py --verbose
```

### 2. Keep Dependencies Updated

Regularly update dependencies:
```bash
# Python
pip list --outdated
pip-audit

# JavaScript
npm audit
npm update
```

### 3. Review Security Alerts Weekly

Check the Security tab weekly for new findings:
- GitHub → Security → Code scanning
- GitHub → Security → Dependabot

### 4. Use Branch Protection

Require security checks to pass before merge:
- Settings → Branches → Branch protection rules
- Enable "Require status checks to pass"
- Select: CodeQL, Dependency Review

### 5. Rotate Secrets Immediately

If secrets are detected:
1. Revoke exposed credentials immediately
2. Rotate all related secrets
3. Update applications using the credentials
4. Audit access logs for unauthorized use

## Additional Resources

- [Security Scanning Policy](../../docs/policy/security-scanning.md)
- [CodeQL Documentation](https://codeql.github.com/docs/)
- [GitHub Security Features](https://docs.github.com/en/code-security)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

## Support

For questions or issues with security scanning:
- Open an issue in this repository
- Contact: security@mokoconsulting.tech
- Slack: #security channel

---

**Metadata**

| Field | Value |
|-------|-------|
| Document | Security Scanning Guide |
| Path | /scripts/validate/SECURITY_SCANNING.md |
| Version | 01.00.00 |
| Status | Active |
| Last Updated | 2026-01-28 |
| Owner | Moko Consulting |
