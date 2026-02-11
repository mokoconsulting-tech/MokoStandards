# Directory Listing Security Policy

**Status**: Active | **Version**: 01.01.00 | **Effective**: 2026-01-16

## Overview

This policy requires all organization repositories to include redirect files (`index.html` and `index.php`) in source directories to prevent directory listing exposure on web servers.

## Policy Statement

All organization repositories **MUST** include redirect files in:

1. The `src/` directory (if present)
2. All subdirectories under `src/`
3. Any other directories that may be exposed via web servers

### File Requirements by Project Type

**PHP-based projects** (e.g., Dolibarr/MokoCRM):
- `index.php` - Primary redirect (server-side)
- `index.html` - Fallback redirect (client-side)

**Non-PHP projects** (e.g., Node.js, static sites):
- `index.html` - Primary redirect (client-side)

## Requirements

### Mandatory Redirect Files

#### index.html (Required for all projects)

Each directory must contain an `index.html` file that:

- Redirects to the repository root URL (`/`)
- Uses meta refresh for automatic redirection
- Includes JavaScript fallback for redirect
- Contains `noindex, nofollow` meta tags
- Provides a manual link for accessibility

#### index.php (Required for PHP projects)

PHP-based projects must also include an `index.php` file that:

- Uses PHP header redirect (highest priority)
- Redirects to the repository root URL (`/`)
- Includes HTML/JavaScript fallback
- Contains `noindex, nofollow` meta tags
- Prevents direct file access

### Template Location

The standard redirect templates are located at:
```
templates/security/index.html
templates/security/index.php
```

### Implementation

When creating new repositories or directories:

**For PHP projects:**
```bash
# Copy both templates to all src subdirectories
find src -type d -exec sh -c 'cp templates/security/index.html "$1" && cp templates/security/index.php "$1"' _ {} \;
```

**For non-PHP projects:**
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

**For all projects:**
- [ ] `index.html` exists in `src/`
- [ ] `index.html` exists in all `src/` subdirectories
- [ ] All `index.html` files redirect to `/`
- [ ] Files include `noindex, nofollow` meta tags
- [ ] Files use standard template from `templates/security/index.html`

**Additional for PHP projects:**
- [ ] `index.php` exists in `src/`
- [ ] `index.php` exists in all `src/` subdirectories
- [ ] All `index.php` files use header redirect
- [ ] Files use standard template from `templates/security/index.php`

### Verification

Verify compliance with:

**Check for missing index.html files:**
```bash
find src -type d ! -exec test -e {}/index.html \; -print
```

**Check for missing index.php files (PHP projects):**
```bash
find src -type d ! -exec test -e {}/index.php \; -print
```

Expected output: No directories listed (all have required index files)

### Enforcement

- **CI/CD Validation**: Automated checks verify presence of `index.html`
- **Repository Health Scoring**: Missing files reduce health score
- **Pull Request Reviews**: Reviewers verify compliance for new directories

## Implementation Guidelines

### New Repositories

When creating a new repository:

**For PHP projects:**
1. Copy templates: `cp templates/security/index.* src/`
2. Replicate to subdirectories: `find src -type d -exec sh -c 'cp templates/security/index.html "$1" && cp templates/security/index.php "$1"' _ {} \;`
3. Commit files with source code
4. Verify in CI/CD pipeline

**For non-PHP projects:**
1. Copy template: `cp templates/security/index.html src/`
2. Replicate to subdirectories: `find src -type d -exec cp templates/security/index.html {} \;`
3. Commit files with source code
4. Verify in CI/CD pipeline

### Existing Repositories

For repositories without redirect files:

1. Review directory structure
2. Identify directories served by web servers
3. Determine if project is PHP-based
4. Apply appropriate templates to all applicable directories
5. Test redirect functionality
6. Commit and deploy changes

### Maintenance

When adding new directories:

1. Copy appropriate index files from parent directory or templates
2. Verify redirect works correctly
3. Include in same commit as directory creation

## Template Specification

### Required Elements - index.html

The `index.html` template must include:

```html
<!-- Meta refresh redirect -->
[![MokoStandards](https://img.shields.io/badge/MokoStandards-03.02.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

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

### Required Elements - index.php

The `index.php` template must include:

```php
<?php
// PHP header redirect (highest priority)
header('Location: /');
exit;
?>
<!-- HTML fallback (same as index.html) -->
```

### Customization

Templates may be customized for:
- Branding (styling)
- Alternative redirect targets (with approval)
- Additional security headers (PHP)

Templates must NOT:
- Remove redirect functionality
- Change default target without security review
- Include executable code beyond redirect (except header redirect in PHP)

### PHP-Specific Requirements

The `index.php` template must:
- Use PHP header redirect as primary mechanism
- Exit immediately after header redirect
- Prevent execution without proper context
- Include HTML fallback for edge cases

## Related Policies

- [security-scanning](./security-scanning.md) - Automated security validation
- [workflow-standards](./workflow-standards.md) - CI/CD security checks
- [file-header-standards](./file-header-standards.md) - File metadata requirements
- [crm/development-standards](../crm/development-standards.md) - PHP/Dolibarr standards

## Exceptions

Exceptions to this policy require:

1. Security team approval
2. Documented justification
3. Alternative mitigation controls
4. Annual review

Request exceptions via GitHub issue with `security-exception` label.

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Policy                                       |
| Domain         | Governance                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/policy/security/directory-listing-prevention.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
