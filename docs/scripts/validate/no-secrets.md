[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# no_secrets.py Script Guide

## Overview

The `no_secrets.py` script scans source code repositories for accidentally committed secrets and credentials using high-signal pattern detection. It helps prevent credential exposure by identifying common secret patterns before they reach production.

## Location

- **Path**: `/scripts/validate/no_secrets.py`
- **Type**: Python script
- **Category**: Validation / Security

## Version Requirements

- **Python**: 3.7+ (3.9+ recommended)
- **PowerShell**: 7.0+ (PowerShell Core) - Future PowerShell version planned
- **Dependencies**: Standard library only (no external packages required)

## Purpose

This script performs security validation by detecting potentially sensitive information that may have been accidentally committed to the repository. It uses pattern matching to identify:

- Private keys (RSA, DSA, EC, OpenSSH formats)
- AWS access keys (AKIA, ASIA prefixes)
- GitHub personal access tokens (ghp_, gho_, github_pat_ prefixes)
- Slack tokens (xox* patterns)
- Stripe API keys (sk_live_, pk_live_ prefixes)
- Generic secret patterns (API keys, passwords in code)

## Usage

### Basic Usage

```bash
# Scan default 'src' directory
python3 scripts/validate/no_secrets.py

# Scan specific directory
python3 scripts/validate/no_secrets.py --src-dir /path/to/source

# Scan current directory
python3 scripts/validate/no_secrets.py --src-dir .
```

### Options and Arguments

- `-s, --src-dir <path>`: Source directory to scan (default: `src` or value of `$src` environment variable)

### Examples

```bash
# Example 1: Scan entire project
python3 scripts/validate/no_secrets.py --src-dir .

# Example 2: Scan specific module
python3 scripts/validate/no_secrets.py --src-dir src/authentication

# Example 3: Set source directory via environment variable
export src=/path/to/code
python3 scripts/validate/no_secrets.py

# Example 4: Use in Git pre-commit hook
python3 scripts/validate/no_secrets.py --src-dir $(git rev-parse --show-toplevel)
```

## Requirements

### Python Version
- Python 3.7 or higher
- Uses type hints (requires Python 3.5+)
- pathlib for cross-platform path handling

### Dependencies
- **Standard Library Only:**
  - `argparse` - Command-line interface
  - `json` - JSON output formatting
  - `os`, `sys` - System operations
  - `re` - Regular expression matching
  - `pathlib` - Path manipulation
  - `typing` - Type hints

### Custom Libraries
- `scripts/lib/common.py` - Logging and error handling utilities

### Required Permissions
- Read access to source directory
- No special elevated permissions required

## Configuration

### Environment Variables

- `src`: Default source directory (overridden by `--src-dir` argument)
- `DEBUG`: Enable debug logging if set to any value

### Excluded Directories

The script automatically excludes common build and dependency directories:
- `vendor/` - PHP/Ruby dependencies
- `node_modules/` - Node.js dependencies
- `dist/` - Distribution/build output
- `build/` - Build artifacts
- `.git/` - Git repository metadata

### Secret Patterns Detected

**Pattern Priority:** High-signal patterns only (minimal false positives)

1. **Private Keys:**
   - `-----BEGIN RSA PRIVATE KEY-----`
   - `-----BEGIN DSA PRIVATE KEY-----`
   - `-----BEGIN EC PRIVATE KEY-----`
   - `-----BEGIN OPENSSH PRIVATE KEY-----`

2. **AWS Credentials:**
   - `AKIA[0-9A-Z]{16}` - AWS Access Key ID
   - `ASIA[0-9A-Z]{16}` - AWS Session Token

3. **GitHub Tokens:**
   - `ghp_[a-zA-Z0-9]{36}` - Personal access token
   - `gho_[a-zA-Z0-9]{36}` - OAuth token
   - `github_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59}` - Fine-grained PAT

4. **Slack Tokens:**
   - `xox[baprs]-[0-9a-zA-Z-]+` - Various Slack token types

5. **Stripe Keys:**
   - `sk_live_[0-9a-zA-Z]{24,}` - Secret keys
   - `pk_live_[0-9a-zA-Z]{24,}` - Public keys

## How It Works

### Step-by-Step Process

1. **Initialization:**
   - Parses command-line arguments
   - Imports common library utilities
   - Validates source directory exists

2. **Directory Traversal:**
   - Recursively walks source directory tree
   - Skips excluded directories (vendor, node_modules, etc.)
   - Identifies text files only (skips binary files)

3. **File Scanning:**
   - Opens each file and reads content
   - Detects binary files (contains null bytes) and skips them
   - Applies regex patterns to file content
   - Records matches with file path and line number

4. **Results Aggregation:**
   - Collects all matches (limited to first 50)
   - Groups by pattern type
   - Tracks affected files

5. **Output Generation:**
   - JSON format for machine parsing
   - Human-readable summary for console
   - Shows first 10 matches in detail
   - Provides total counts

### Detection Algorithm

```python
# High-level pattern matching
for file_path in walk_directory(src_dir):
    if is_binary(file_path) or is_excluded(file_path):
        continue

    content = read_file(file_path)

    for pattern_name, pattern_regex in SECRET_PATTERNS:
        matches = pattern_regex.findall(content)
        if matches:
            record_secret_found(file_path, pattern_name, matches)
```

## Exit Codes

- `0`: **Success** - No secrets found, scan completed successfully
- `1`: **Failure** - Secrets detected OR source directory does not exist

### Interpreting Exit Codes

```bash
# Check exit code in shell
python3 scripts/validate/no_secrets.py
if [ $? -eq 0 ]; then
    echo "✅ No secrets found"
else
    echo "❌ Secrets detected or error occurred"
fi
```

## Integration

### CI/CD Workflows

**GitHub Actions Example:**

```yaml
name: Security Scan

on: [push, pull_request]

jobs:
  scan-secrets:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Scan for secrets
        run: python3 scripts/validate/no_secrets.py --src-dir .
```

**Integration in MokoStandards:**
- Used in `.github/workflows/code-quality.yml`
- Pre-commit validation in standards compliance workflow

### Other Scripts

**Related Validation Scripts:**
- `validate/no_secrets.py` (this script)
- `validate/validate_structure.py` - Repository structure validation
- `validate/check_repo_health.py` - Comprehensive health checks

**Workflow Integration:**
```bash
# Complete security validation
python3 scripts/validate/no_secrets.py --src-dir src
python3 scripts/validate/validate_file_headers.py --path src
python3 scripts/validate/check_repo_health.py --repo-path .
```

### Pre-commit Hooks

**.pre-commit-config.yaml:**
```yaml
repos:
  - repo: local
    hooks:
      - id: no-secrets
        name: Check for secrets
        entry: python3 scripts/validate/no_secrets.py --src-dir
        language: system
        pass_filenames: false
        always_run: true
```

## Error Handling

### Common Errors and Solutions

**1. Source Directory Not Found**
```
ERROR: Source directory does not exist: /path/to/src
```
**Solution:** Verify the path exists or omit `--src-dir` to use default

**2. Permission Denied**
```
ERROR: Cannot read file: /path/to/file.py
```
**Solution:** Ensure read permissions on source directory

**3. Binary File Handling**
```
# Automatically skipped (not an error)
Skipping binary file: image.png
```
**Solution:** No action needed, binary files are safely skipped

**4. Too Many Results**
```
WARNING: Truncated results to first 50 matches
```
**Solution:** Fix detected secrets, then re-scan

### Debugging

Enable debug mode:
```bash
DEBUG=1 python3 scripts/validate/no_secrets.py --src-dir .
```

## Best Practices

### 1. Regular Scanning
- Run before every commit (use pre-commit hooks)
- Include in CI/CD pipeline
- Schedule weekly scans for long-running branches

### 2. False Positive Handling
- Review all matches before dismissing
- Use `.gitignore` for legitimate test fixtures
- Document exceptions in security policy

### 3. Secret Remediation
If secrets are found:
1. **Immediately rotate** the exposed credential
2. **Remove from history** using `git filter-branch` or BFG Repo-Cleaner
3. **Investigate exposure window** - who had access?
4. **Update security procedures** to prevent recurrence

### 4. Prevention
- Use environment variables for secrets
- Store credentials in secret managers (AWS Secrets Manager, Azure Key Vault)
- Never commit `.env` files
- Use secret scanning tools continuously

### 5. Integration Strategy
```bash
# Fail fast in CI
set -e
python3 scripts/validate/no_secrets.py --src-dir .
python3 scripts/validate/validate_structure.py structure.xml .
# Continue with build only if validation passes
```

## Related Scripts

### Validation Family
- [validate/validate_structure.py](validate-structure-py.md) - Repository structure validation
- [validate/check_repo_health.py](check-repo-health-py.md) - Health scoring
- [validate/xml_wellformed.py](xml-wellformed-py.md) - XML validation
- [validate/validate_file_headers.py](../maintenance/validate-file-headers-py.md) - Header compliance

### Security Tools
- [validate/validate_codeql_config.py](validate-codeql-config-py.md) - CodeQL configuration
- `.github/workflows/codeql-analysis.yml` - Static analysis workflow

## Output Format

### JSON Output
```json
{
  "status": "failed",
  "secrets_found": 2,
  "patterns_matched": {
    "GitHub Token": 1,
    "AWS Access Key": 1
  },
  "affected_files": [
    "src/config/aws.py",
    "src/auth/github.py"
  ],
  "matches": [
    {
      "file": "src/config/aws.py",
      "pattern": "AWS Access Key",
      "line": 15,
      "context": "AWS_KEY = 'AKIAIOSFODNN7EXAMPLE'"
    }
  ]
}
```

### Console Output
```
🔍 Scanning for secrets in: /path/to/src
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ SECRETS DETECTED

📁 Affected Files: 2
🔑 Secret Patterns Matched: 2

Detailed Results (showing first 10):

1. AWS Access Key in src/config/aws.py:15
   Context: AWS_KEY = 'AKIAIOSFODNN7EXAMPLE'

2. GitHub Token in src/auth/github.py:8
   Context: token = 'ghp_1234567890abcdefghijklmnopqrstuvwxyz'

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  CRITICAL: Rotate these credentials immediately!
```

## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
