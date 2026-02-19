# Validation Scripts

This directory contains comprehensive validation and verification scripts for code quality, security, and standards compliance.

## Core Validation Scripts

### check_enterprise_readiness.py
**NEW in v04.00.01** - Enterprise readiness validator that checks if a repository meets all enterprise compliance requirements.

**Features:**
- Validates 10 enterprise libraries presence
- Checks 5 enterprise workflows
- Verifies Terraform installation scripts
- Validates version badges in documentation
- Checks MokoStandards.override.tf configuration
- Validates enterprise metadata in configs
- Checks monitoring directory structure
- Returns 0-100% readiness score
- Provides actionable recommendations

**Usage:**
```bash
# Check current repository
python scripts/validate/check_enterprise_readiness.py

# Check specific repository
python scripts/validate/check_enterprise_readiness.py --path /path/to/repo

# Verbose output with details
python scripts/validate/check_enterprise_readiness.py --verbose

# JSON output for programmatic use
python scripts/validate/check_enterprise_readiness.py --json

# Check and get exit code
python scripts/validate/check_enterprise_readiness.py
echo $?  # 0 = ready (≥80%), 1 = not ready (<80%), 2 = error
```

**Exit Codes:**
- `0` - Repository is enterprise-ready (≥80% score)
- `1` - Repository is not enterprise-ready (<80% score)
- `2` - Error during checking

### check_repo_health.py
Comprehensive repository health check covering structure, documentation, workflows, and compliance.

**Usage:**
```bash
# Check current repository
./scripts/validate/check_repo_health.py

# Check specific repository
./scripts/validate/check_repo_health.py --repo /path/to/repo

# Output JSON report
./scripts/validate/check_repo_health.py --json

# Fail on warnings
./scripts/validate/check_repo_health.py --strict
```

### validate_repo_health.py
Enhanced validation with schema-aware checks and detailed reporting.

### schema_aware_health_check.py
Repository validation using schema definitions for structure and content verification.

### Invoke-RepoHealthCheckGUI.ps1
PowerShell GUI for repository health checks. Provides a Windows Forms interface for:
- Interactive repository selection
- Visual health check results
- Detailed issue reporting
- Export capabilities

**Usage:**
```powershell
.\scripts\validate\Invoke-RepoHealthCheckGUI.ps1
```

### Invoke-PlatformDetection.ps1
PowerShell utility for platform detection and validation on Windows systems.

## Structure and Standards

### validate_structure.py
Validate repository structure against MokoStandards requirements.

### validate_structure_v2.py
Enhanced structure validation with improved reporting.

### validate_structure_terraform.py
Terraform-specific structure validation and best practices checking.

### auto_detect_platform.py
Automatically detect and validate platform-specific requirements (Joomla, Dolibarr, etc.).

## Code Quality

### tabs.py
Validate indentation (tabs vs spaces) according to language-specific rules.

**Usage:**
```bash
# Check all files requiring spaces
./scripts/validate/tabs.py --type all

# Check Python files (should use 4 spaces)
./scripts/validate/tabs.py --type python

# Check YAML files (should use 2 spaces)
./scripts/validate/tabs.py --type yaml

# Check specific file
./scripts/validate/tabs.py --type python --file src/main.py
```

**Languages Checked:**
- YAML, Python, Haskell, F#, CoffeeScript, Nim, JSON, reStructuredText

### php_syntax.py
Validate PHP syntax using `php -l`.

### xml_wellformed.py
Validate XML files are well-formed.

### workflows.py
Validate GitHub Actions workflow files.

### manifest.py
Validate extension manifest files (Joomla, Dolibarr).

### validate_codeql_config.py
Validate CodeQL configuration files.

## Security

### security_scan.py
Comprehensive security scanning for vulnerabilities, hardcoded credentials, and unsafe patterns.

**Usage:**
```bash
# Run security scan
./scripts/validate/security_scan.py

# Scan specific directory
./scripts/validate/security_scan.py --dir src/

# Output JSON report
./scripts/validate/security_scan.py --json

# Fail on any findings
./scripts/validate/security_scan.py --strict
```

### no_secrets.py
Scan for hardcoded secrets, API keys, passwords, and credentials.

**Usage:**
```bash
# Scan current repository
./scripts/validate/no_secrets.py

# Scan specific files
./scripts/validate/no_secrets.py --files src/*.php

# Ignore specific patterns
./scripts/validate/no_secrets.py --ignore test_key
```

See [SECURITY_SCANNING.md](./SECURITY_SCANNING.md) for detailed security scanning documentation.

## Documentation and Metadata

### check_license_headers.py
Validate license headers in source files.

### check_markdown_links.py
Check for broken links in Markdown documentation.

### find_todos.py
Find TODO, FIXME, and other code comments requiring attention.

## Platform-Specific

### generate_stubs.py
Generate stub files for type checking and IDE support.

### paths.py
Validate path conventions (Windows vs Unix paths).

## Purpose

These scripts ensure:
- **Code Quality**: Standards compliance, syntax validation, proper formatting
- **Security**: No hardcoded secrets, safe coding patterns
- **Structure**: Proper repository organization
- **Documentation**: Complete and accurate documentation
- **Platform Compliance**: Platform-specific requirements met

## Typical Validation Workflow

```bash
# 1. Run comprehensive health check
./scripts/validate/check_repo_health.py

# 2. Check for security issues
./scripts/validate/security_scan.py

# 3. Validate code quality
./scripts/validate/tabs.py --type all
./scripts/validate/php_syntax.py

# 4. Check documentation
./scripts/validate/check_markdown_links.py

# 5. Platform-specific validation
./scripts/validate/auto_detect_platform.py
```

## Integration

These scripts are used in:
- GitHub Actions workflows (`.github/workflows/standards-compliance.yml`)
- Pre-commit hooks
- CI/CD pipelines
- Manual quality checks
