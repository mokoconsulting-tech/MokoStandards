# Security Templates

This directory contains security-related templates for MokoStandards repositories.

## index.html - Directory Listing Prevention

**Purpose**: Prevents directory listing on web servers for security purposes.

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
