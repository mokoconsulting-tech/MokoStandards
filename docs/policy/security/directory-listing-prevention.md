# Directory Listing Security Policy

**Status**: Active | **Version**: 01.00.00 | **Effective**: 2026-01-16

## Overview

This policy requires all organization repositories to include redirect `index.html` files in source directories to prevent directory listing exposure on web servers.

## Policy Statement

All organization repositories **MUST** include an `index.html` redirect file in:

1. The `src/` directory (if present)
2. All subdirectories under `src/`
3. Any other directories that may be exposed via web servers

## Requirements

### Mandatory Redirect File

Each directory must contain an `index.html` file that:

- Redirects to the repository root URL (`/`)
- Uses meta refresh for automatic redirection
- Includes JavaScript fallback for redirect
- Contains `noindex, nofollow` meta tags
- Provides a manual link for accessibility

### Template Location

The standard redirect template is located at:
```
templates/security/index.html
```

### Implementation

When creating new repositories or directories:

```bash
# Copy index.html to all src subdirectories
find src -type d -exec cp templates/security/index.html {} \;
```

## Security Rationale

### Threat Mitigation

**Directory Listing Exposure**: Without an index file, web servers may expose directory contents, revealing:
- File names and structure
- Source code organization
- Configuration file locations
- Potential security vulnerabilities

**Information Disclosure**: Directory listings provide attackers with:
- Reconnaissance information
- Attack surface mapping
- Potential entry points

### Defense Mechanism

The redirect `index.html` file:
1. **Prevents enumeration**: No directory contents visible
2. **Reduces attack surface**: Limits information disclosure
3. **Maintains usability**: Redirects legitimate users to repository root
4. **SEO-safe**: Prevents search engines from indexing directories

## Scope

### Included Repositories

This policy applies to:
- All public repositories in the organization
- All private repositories with web server deployment
- Template repositories used for scaffolding

### Included Directories

Required in:
- `src/` and all subdirectories
- `public/` and all subdirectories (if present)
- `dist/` and all subdirectories (if present)
- Any directory served by a web server

### Excluded Directories

Not required in:
- `.git/` and version control directories
- `node_modules/` and dependency directories
- Build artifact directories (temporary)
- Directories not served via web servers

## Compliance

### Repository Setup Checklist

- [ ] `index.html` exists in `src/`
- [ ] `index.html` exists in all `src/` subdirectories
- [ ] All `index.html` files redirect to `/`
- [ ] Files include `noindex, nofollow` meta tags
- [ ] Files use standard template from `templates/security/index.html`

### Verification

Verify compliance with:

```bash
# Check for missing index.html files
find src -type d ! -exec test -e {}/index.html \; -print
```

Expected output: No directories listed (all have index.html)

### Enforcement

- **CI/CD Validation**: Automated checks verify presence of `index.html`
- **Repository Health Scoring**: Missing files reduce health score
- **Pull Request Reviews**: Reviewers verify compliance for new directories

## Implementation Guidelines

### New Repositories

When creating a new repository:

1. Copy template: `cp templates/security/index.html src/`
2. Replicate to subdirectories: `find src -type d -exec cp templates/security/index.html {} \;`
3. Commit files with source code
4. Verify in CI/CD pipeline

### Existing Repositories

For repositories without redirect files:

1. Review directory structure
2. Identify directories served by web servers
3. Apply template to all applicable directories
4. Test redirect functionality
5. Commit and deploy changes

### Maintenance

When adding new directories:

1. Copy `index.html` from parent directory or template
2. Verify redirect works correctly
3. Include in same commit as directory creation

## Template Specification

### Required Elements

The `index.html` template must include:

```html
<!-- Meta refresh redirect -->
<meta http-equiv="refresh" content="0;url=/">

<!-- SEO directives -->
<meta name="robots" content="noindex, nofollow">

<!-- JavaScript redirect -->
<script>
    window.location.href = '/';
</script>

<!-- Manual fallback link -->
<a href="/">click here</a>
```

### Customization

Templates may be customized for:
- Branding (styling)
- Alternative redirect targets (with approval)
- Additional security headers

Templates must NOT:
- Remove redirect functionality
- Change default target without security review
- Include executable code beyond redirect

## Related Policies

- [security-scanning](./security-scanning.md) - Automated security validation
- [workflow-standards](./workflow-standards.md) - CI/CD security checks
- [file-header-standards](./file-header-standards.md) - File metadata requirements

## Exceptions

Exceptions to this policy require:

1. Security team approval
2. Documented justification
3. Alternative mitigation controls
4. Annual review

Request exceptions via GitHub issue with `security-exception` label.

## Metadata

| Field | Value |
|-------|-------|
| Document Type | Policy |
| Policy ID | SEC-DIR-001 |
| Owner | Security Team |
| Approval Required | Yes |
| Evidence Required | Yes |
| Review Cycle | Annual |
| Compliance Tags | Security, Web Security |
| Status | Active |
| Effective Date | 2026-01-16 |

## Revision History

| Date | Version | Change Description | Author |
|------|---------|-------------------|--------|
| 2026-01-16 | 01.00.00 | Initial policy creation | GitHub Copilot |
