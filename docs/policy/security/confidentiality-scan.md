# Confidentiality Scan

## Overview

The Confidentiality Scan is a GitHub Actions workflow that automatically scans the repository for potential data leakage, sensitive information, and organization-specific references that should not be committed to public repositories.

This workflow helps maintain the security and confidentiality of organization-internal information while allowing the public repository to remain open source.

## Purpose

The confidentiality scan prevents:

- Organization-specific references from being exposed
- Sensitive credentials and secrets from being committed
- Internal documentation references that may confuse external users
- Proprietary information from leaking into public repositories

## Workflow Configuration

**File:** `.github/workflows/confidentiality-scan.yml`

**Triggers:**
- Pull requests to main, dev/**, rc/**, and version/** branches
- Pushes to main, dev/**, rc/**, and version/** branches
- Manual workflow dispatch

**Permissions:**
- `contents: read` - Read repository content
- `pull-requests: write` - Comment on pull requests
- `issues: write` - Create issues if violations found
- `checks: write` - Create check runs

## Scan Types

### 1. Organization-Specific References Scan

Scans for forbidden patterns that reference internal organization resources:

**Patterns detected:**
- `@mokoconsulting-tech/[team-name]` - Internal GitHub team mentions
- `.github-private` - Private repository references
- `CONFIDENTIAL` - Confidential markers
- `INTERNAL ONLY` - Internal-only markers
- `DO NOT SHARE` - Sharing restriction markers
- `ftp.[subdomain].mokoconsulting.tech` - Internal FTP servers
- `mokoconsulting-tech.slack.com` - Private Slack workspace
- `private.mokoconsulting.tech` - Private domain references

**Result:** Hard failure (❌) if any patterns are found

### 2. Potential Secrets Scan

Scans for potential credentials and secret keys:

**Patterns detected:**
- `password = "..."` - Password assignments
- `api_key = "..."` or `api-key = "..."` - API key assignments
- `secret_key = "..."` or `secret-key = "..."` - Secret key assignments
- `token = "..."` - Token assignments
- `-----BEGIN RSA PRIVATE KEY-----` - Private key headers (RSA, DSA, EC, OPENSSH)
- `AKIA[0-9A-Z]{16}` - AWS access keys
- `ghp_[a-zA-Z0-9]{36}` - GitHub personal access tokens
- `gho_[a-zA-Z0-9]{36}` - GitHub OAuth tokens
- `ghu_[a-zA-Z0-9]{36}` - GitHub user tokens

**Exclusions:**
- `*.md` files - Documentation examples
- `*.example` files - Example configurations
- `*.sample` files - Sample files
- `docs/*` directory - Documentation

**Result:** Hard failure (❌) if potential secrets are found

### 3. Internal Documentation References Scan

Scans for references to internal documentation that should be clarified:

**Patterns detected (case-insensitive):**
- "see internal documentation"
- "refer to internal wiki"
- "contact the team"
- "ask the maintainers"
- "internal process"
- "proprietary"

**Scope:** Only markdown (*.md) files

**Result:** Warning (⚠️) - does not fail the workflow

## Excluded Files

The following files are excluded from confidentiality scans:

- `.github/workflows/confidentiality-scan.yml` - The workflow file itself
- `docs/TWO_TIER_ARCHITECTURE.md` - Architecture documentation about public/private split (Note: This references a file path used in the workflow configuration. The actual file may be at `docs/policy/two-tier-architecture.md`)
- `docs/guide/PRIVATE_REPOSITORY_REFERENCE.md` - Documentation about private repository
- `STANDARDS_COORDINATION.md` - Standards coordination documentation
- `.github/PRIVATE_TEMPLATES.md` - Private templates reference
- `terraform/*.tfplan` - Terraform plan files (may contain computed values)
- `terraform/*.tfstate*` - Terraform state files
- `terraform/.terraform/*` - Terraform cache directory

**Note:** Terraform `*.tf` files ARE scanned for secrets (as they should be). Only Terraform state/plan/cache files are excluded.

## How It Works

1. **Checkout:** Fetches the full repository history
2. **Python Setup:** Prepares Python 3.11 environment
3. **Organization Scan:** Uses `git grep` to search for forbidden patterns
4. **Secret Scan:** Uses `git grep` to search for potential secrets
5. **Documentation Scan:** Uses `git grep` to search for internal doc references
6. **Report Creation:** Creates a detailed check run with findings
7. **PR Comment:** Adds a comment to the pull request with results (if applicable)

## Interpreting Results

### ✅ Pass

No violations found. The scan completed successfully.

### ❌ Fail

One or more forbidden patterns or secrets were detected. Review the detailed output to identify and fix the issues.

### ⚠️ Warning

Internal documentation references were found. Consider clarifying these references for external users.

## Fixing Violations

### Organization References

If organization-specific references are found:

1. **Remove the reference** - Replace with generic terminology
2. **Move to private repository** - If the content must reference internal resources
3. **Update exclusion list** - If the file legitimately needs the reference (rare)

### Potential Secrets

If potential secrets are found:

1. **Remove the secret** - Never commit secrets to source control
2. **Use environment variables** - Store secrets in GitHub Secrets or environment configuration
3. **Use secret management** - Implement proper secret management (e.g., HashiCorp Vault, AWS Secrets Manager)
4. **Rotate the secret** - If a real secret was committed, rotate it immediately

### Internal Documentation References

If internal documentation references are found:

1. **Add public documentation** - Create public documentation to replace internal references
2. **Clarify the reference** - Provide enough context for external users
3. **Remove the reference** - If not needed for external users

## Best Practices

1. **Run locally before committing** - Use `git grep` to check for patterns before pushing
2. **Review exclusion list** - Ensure excluded files are truly necessary
3. **Update patterns** - Add new forbidden patterns as needed for your organization
4. **Document exceptions** - If a file needs an exception, document why in the exclusion list
5. **Rotate secrets immediately** - If a secret is ever committed, rotate it before fixing the code

## Customization

To customize the confidentiality scan for your organization:

1. **Update patterns** - Modify the `FORBIDDEN_PATTERNS`, `SECRET_PATTERNS`, and `INTERNAL_DOC_PATTERNS` arrays
2. **Update exclusions** - Modify the `EXCLUDED_FILES` environment variable
3. **Change behavior** - Adjust whether scans fail or warn based on your needs
4. **Add notifications** - Add Slack/email notifications for violations

## Related Documentation

- [Two-Tier Architecture](../two-tier-architecture.md) - Public/private repository strategy
- [Security Scanning Policy](../security-scanning.md) - Overall security scanning approach
- [Data Classification](../data-classification.md) - Data classification and handling
- [Private Repository Reference](../../guide/PRIVATE_REPOSITORY_REFERENCE.md) - Private repository documentation

## Metadata

- **File:** `docs/policy/security/confidentiality-scan.md`
- **Workflow:** `.github/workflows/confidentiality-scan.yml`
- **Version:** 1.0.0
- **Last Updated:** 2026-01-28
- **Maintained by:** Security Team
