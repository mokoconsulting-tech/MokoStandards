# Security Templates

This directory contains security-related templates for MokoStandards repositories.

## index.html - Directory Listing Prevention (Static)

**Purpose**: Prevents directory listing on static web servers for security purposes.

**Usage**: Copy this file to all `src/` directories and their subdirectories in organization repositories.

```bash
# Copy to src directory and all subdirectories
find src -type d -exec cp templates/security/index.html {} \;
```

**Policy**: All organization repositories must include an `index.html` redirect file in:
- `src/` directory (if it exists)
- All subdirectories under `src/`

**Security Rationale**: 
- Prevents web servers from exposing directory contents
- Redirects users to the repository root
- Uses `noindex, nofollow` meta tags to prevent search engine indexing
- Provides immediate redirect via both meta refresh and JavaScript

**Template Features**:
- Redirects to `/` (repository root)
- Minimal, clean design
- Works with and without JavaScript
- SEO-safe with noindex directive

## index.php - Directory Listing Prevention (PHP)

**Purpose**: Prevents directory listing on PHP-enabled web servers for security purposes.

**Usage**: Copy this file to all `src/` directories and their subdirectories in PHP-based organization repositories.

```bash
# Copy to src directory and all subdirectories
find src -type d -exec cp templates/security/index.php {} \;
```

**Policy**: All PHP-based organization repositories must include an `index.php` redirect file in:
- `src/` directory (if it exists)
- All subdirectories under `src/`

**Security Rationale**: 
- Provides server-side redirect before any HTML is rendered
- Prevents web servers from exposing directory contents
- Includes HTTP header redirect for immediate response
- Falls back to HTML/JavaScript redirect if needed
- Works with PHP-enabled web servers

**Template Features**:
- PHP header redirect (highest priority)
- HTML meta refresh fallback
- JavaScript redirect fallback
- `noindex, nofollow` meta tags
- GPL-3.0-or-later licensed
- Proper PHP security headers

## Usage Recommendation

**For PHP projects** (e.g., Dolibarr/MokoCRM):
- Use both `index.php` and `index.html`
- PHP will take precedence when available
- HTML provides fallback for static serving

**For non-PHP projects** (e.g., Node.js, static sites):
- Use `index.html` only

**Copy both files:**
```bash
# Copy both security templates to all src subdirectories
find src -type d -exec sh -c 'cp templates/security/index.html "$1" && cp templates/security/index.php "$1"' _ {} \;
```
