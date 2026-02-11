[![MokoStandards](https://img.shields.io/badge/MokoStandards-03.02.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Security Considerations for Repository Health System

This document outlines security considerations and potential improvements for the XML-based repository health system.

## Current Implementation

### URL Handling in Scripts

**Files**: `scripts/validate/validate_repo_health.py`, `scripts/validate/check_repo_health.py`

**Current Behavior**: Scripts use `urllib.request.urlopen()` to fetch XML configurations from remote URLs without validation.

**Known Risks**:
- Potential Server-Side Request Forgery (SSRF) attacks
- No timeout limits on URL requests
- No size limits on downloaded content
- URLs are not validated against an allowlist

**Mitigations in Place**:
- Scripts are intended for use in trusted environments (CI/CD pipelines)
- Default configuration URL points to known-good MokoStandards repository
- Manual review required before adding to workflows

**Future Improvements** (tracked for follow-up):
1. Add URL validation against allowlist of trusted domains
2. Implement request timeouts (e.g., 10 seconds)
3. Add maximum file size limits (e.g., 5MB for XML configs)
4. Add URL scheme validation (only allow https://)
5. Consider adding certificate validation

**Example Implementation**:
```python
ALLOWED_DOMAINS = [
    'raw.githubusercontent.com',
    'github.com',
]

def is_url_allowed(url: str) -> bool:
    """Validate URL against allowlist."""
    parsed = urllib.parse.urlparse(url)
    return parsed.scheme == 'https' and any(
        parsed.netloc.endswith(domain) for domain in ALLOWED_DOMAINS
    )

def safe_url_fetch(url: str, timeout: int = 10, max_size: int = 5*1024*1024) -> bytes:
    """Safely fetch content from URL with validation."""
    if not is_url_allowed(url):
        raise SecurityError(f"URL not in allowlist: {url}")

    with urllib.request.urlopen(url, timeout=timeout) as response:
        content_length = response.headers.get('Content-Length')
        if content_length and int(content_length) > max_size:
            raise SecurityError(f"Content too large: {content_length} bytes")

        return response.read(max_size)
```

### Remote Script Downloading in Workflows

**File**: `templates/workflows/repo_health_xml.yml`

**Current Behavior**: Workflow downloads Python scripts from MokoStandards repository using `curl` and executes them.

**Known Risks**:
- Scripts could be modified if repository is compromised
- No checksum verification
- No version pinning

**Mitigations in Place**:
- Scripts downloaded from trusted MokoStandards repository
- Repository has branch protection and requires reviews
- Organization-level access controls

**Future Improvements** (tracked for follow-up):
1. Add checksum validation for downloaded scripts
2. Pin to specific commit SHA instead of branch
3. Cache scripts in organization artifacts
4. Sign scripts and verify signatures
5. Consider vendoring scripts in repositories

**Example Implementation with Checksum**:
```yaml
- name: Download and verify health checker
  run: |
    SCRIPT_URL="https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/scripts/validate/check_repo_health.py"
    EXPECTED_SHA256="abc123..." # Update when script changes

    curl -sSL "${SCRIPT_URL}" -o check_repo_health.py

    ACTUAL_SHA256=$(sha256sum check_repo_health.py | awk '{print $1}')
    if [ "${ACTUAL_SHA256}" != "${EXPECTED_SHA256}" ]; then
      echo "Checksum mismatch! Expected: ${EXPECTED_SHA256}, Got: ${ACTUAL_SHA256}"
      exit 1
    fi

    chmod +x check_repo_health.py
```

**Example with Pinned Version**:
```yaml
env:
  MOKOSTANDARDS_VERSION: "sha-abc123def"  # Pin to specific commit

- name: Download health checker
  run: |
    curl -sSL "https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/${MOKOSTANDARDS_VERSION}/scripts/validate/check_repo_health.py" -o check_repo_health.py
```

### Threshold Configuration Duplication

**Files**: `templates/workflows/repo_health_xml.yml`, `scripts/validate/check_repo_health.py`

**Current Behavior**: Health threshold (70.0) is defined in script constant but duplicated in workflow.

**Known Issue**: Values could diverge if one is updated without the other.

**Future Improvements**:
1. Make threshold configurable via command-line argument
2. Read threshold from XML configuration
3. Use shared environment variable

**Example Implementation**:
```python
parser.add_argument(
    '--threshold',
    type=float,
    default=DEFAULT_HEALTH_THRESHOLD,
    help=f'Health score threshold for pass/fail (default: {DEFAULT_HEALTH_THRESHOLD})'
)
```

## Security Best Practices for Users

### For Repository Administrators

1. **Review Remote Configurations**: Always review XML configurations before referencing them in workflows
2. **Use Private Configs for Sensitive Data**: Store organization-specific configurations in private repositories
3. **Monitor Workflow Runs**: Regularly review workflow execution logs
4. **Enable Branch Protection**: Require reviews for workflow changes
5. **Use Secrets Properly**: Never include secrets in XML configurations

### For Organization-Level Implementation

1. **Validate Custom Configs**: Always run validation script on custom configurations
2. **Test in Pilot Repos**: Test new configurations in pilot repositories before organization-wide deployment
3. **Implement Monitoring**: Set up alerts for health score changes
4. **Regular Audits**: Periodically audit health configurations and workflows
5. **Document Exceptions**: Clearly document any exemptions or custom configurations

### For Custom Check Implementations

1. **Input Validation**: Validate all parameters in custom check scripts
2. **Avoid Command Injection**: Never use unvalidated input in shell commands
3. **Limit Permissions**: Run checks with minimal required permissions
4. **Error Handling**: Implement proper error handling to avoid information disclosure
5. **Audit Logging**: Log all check executions for audit trails

## Reporting Security Issues

If you discover a security issue with the repository health system:

1. **Do NOT** open a public issue
2. Follow the security policy in SECURITY.md
3. Report to: security@mokoconsulting.tech
4. Provide details about the vulnerability and potential impact

## Updates and Improvements

This document will be updated as security improvements are implemented. Check the git history for changes.

---

**Last Updated**: 2026-01-08
**Review Frequency**: Quarterly
**Next Review**: 2026-04-08

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Report                                       |
| Domain         | Operations                                         |
| Applies To     | Specific Projects                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/reports/SECURITY_NOTES_REPO_HEALTH.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
