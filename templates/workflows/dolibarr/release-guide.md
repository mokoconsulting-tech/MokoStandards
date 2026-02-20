# Dolibarr Release Workflow

## Overview

The Dolibarr release workflow (`templates/workflows/dolibarr/release.yml`) automates the release process for Dolibarr modules following the standardized release cycle: **main > dev > rc > version > main**.

## Features

- **Automated Build**: Creates ZIP packages with proper module structure
- **Version Management**: Updates version in module descriptors
- **Development Version Support**: Automatically skips release builds when VERSION is set to "development" on main branch
- **Checksum Generation**: Creates SHA256 and MD5 checksums
- **GitHub Releases**: Automatically creates releases with artifacts
- **FTP/SFTP Upload**: Uploads RC and stable releases to FTP/SFTP servers (optional)
- **Pre-release Support**: RC releases are marked as pre-releases
- **Changelog Integration**: Extracts version-specific changelog entries

## Development Version

### Overview

For Dolibarr modules on the **main** branch, the VERSION field in README.md can be set to `development` instead of a specific version number. This indicates that the code is in active development and should not trigger automatic release builds.

### Benefits

- **Clear Intent**: Developers immediately know the code is in development
- **No Accidental Releases**: Prevents automatic release creation from main branch pushes
- **Explicit Releases**: Forces use of workflow_dispatch or version tags for releases

### Usage

1. **Set Development Version** in README.md:
   ```markdown
   VERSION: development
   ```

2. **Push to Main**: The workflow will detect "development" and skip building:
   ```bash
   git push origin main
   # Workflow will show: "Skipping release build for development version"
   ```

3. **Create Release**: Use one of these methods:
   - **Workflow Dispatch**: Manually trigger with specific version
   - **Version Tag**: Push a version tag (e.g., `v1.0.0`)

### Example Workflow

```markdown
# In README.md during development
VERSION: development

# When ready to release:
# 1. Update README.md
VERSION: 04.00.01

# 2. Commit and tag
git add README.md
git commit -m "chore: prepare v1.0.0 release"
git tag v1.0.0
git push origin main --tags

# 3. After release, set back to development
VERSION: development
git add README.md
git commit -m "chore: set version back to development"
git push origin main
```

## Release Cycle

The workflow supports the following release cycle:

1. **main**: Stable production releases (or development if VERSION: development)
2. **dev/\***: Development branches (no automatic releases)
3. **rc/\***: Release candidate branches (marked as pre-releases)
4. **version/\***: Version branches for maintenance
5. **Tags (v\*._.\_)**: Explicit version tags

### Pre-release Marking

- RC branches (`rc/**`) automatically marked as pre-release
- RC tags (e.g., `v1.0.0-rc1`) automatically marked as pre-release
- Manual workflow dispatch allows explicit pre-release flag

## Workflow Triggers

### Automatic Triggers

```yaml
on:
  push:
    branches:
      - 'main'          # Production releases (skipped if VERSION: development)
      - 'rc/**'         # Release candidates (pre-release)
    tags:
      - 'v*.*.*'        # Version tags
```

### Manual Trigger

```yaml
workflow_dispatch:
  inputs:
    version: 'Release version (e.g., 1.0.0)'
    prerelease: 'Mark as pre-release (use for RC releases)'
```

## Usage

### Automatic Release on Tag Push

```bash
# Create and push a version tag
git tag v1.0.0
git push origin v1.0.0

# For RC releases
git tag v1.0.0-rc1
git push origin v1.0.0-rc1  # Automatically marked as pre-release
```

### Manual Release via Workflow Dispatch

1. Go to Actions → Create Release
2. Click "Run workflow"
3. Enter version (e.g., `1.0.0`)
4. Check "prerelease" for RC releases
5. Click "Run workflow"

### RC Branch Workflow

```bash
# Create RC branch
git checkout -b rc/1.0.0
git push origin rc/1.0.0

# Pushes to rc/* branches trigger pre-release builds
```

## Package Structure

The workflow creates the following artifacts:

```
build/
├── ModuleName-1.0.0.zip         # Release package
├── ModuleName-1.0.0.zip.sha256  # SHA256 checksum
└── ModuleName-1.0.0.zip.md5     # MD5 checksum
```

### Excluded Files

The package excludes development and build artifacts:

- `build/`, `tests/`, `.git*`, `.github/`
- `composer.json`, `composer.lock`
- `phpunit.xml*`, `phpcs.xml*`, `phpstan.neon*`, `psalm.xml*`
- `node_modules/`, `package*.json`

## Module Name Detection

The workflow automatically detects the module name from:

1. Module descriptor file (`core/modules/mod*.class.php`)
2. Repository name (removes `MokoDoli` or `dolibarr-` prefix)

## Version Update

The workflow updates the version in:

- Module descriptor: `$this->version = 'X.Y.Z'` in `core/modules/mod*.class.php`

## Changelog Integration

If `CHANGELOG.md` exists, the workflow:

1. Extracts changelog section for the release version
2. Includes it in the GitHub release notes
3. Falls back to default message if section not found

Example `CHANGELOG.md` format:

```markdown
## [1.0.0] - 2026-01-09

### Added

- New QR code generation feature
- Enhanced PDF export

### Fixed

- Fixed encoding issue in QR codes
```

## GitHub Release

The workflow creates a GitHub release with:

- **Tag**: `v{version}` (e.g., `v1.0.0`)
- **Name**: `Release {version}`
- **Body**: Extracted from CHANGELOG.md
- **Assets**: ZIP package, SHA256, MD5
- **Pre-release**: Automatically set for RC releases
- **Draft**: Always false (published immediately)

## FTP/SFTP Upload

### Overview

RC and stable releases are automatically uploaded to Release System (RS) FTP/SFTP servers for distribution. This feature is optional and only activates when RS_FTP credentials are configured.

### Configuration

The workflow supports both password and SSH key authentication. Configure the following secrets and variables in your repository or organization settings:

**Required Secrets:**
- `RS_FTP_HOST` - SFTP server hostname (e.g., `sftp.example.com`)
- `RS_FTP_USER` - SFTP username
- `RS_FTP_PATH` - Base path on server (variable, e.g., `/var/www/releases`)

**Authentication (choose one):**
- `RS_FTP_PASSWORD` - Password authentication (simple)
- `RS_FTP_KEY` - SSH private key authentication (recommended)

**Optional:**
- `RS_FTP_PORT` - SFTP port (default: 22)
- `RS_FTP_PATH_SUFFIX` - Additional path suffix (variable, e.g., `/dolibarr`)

### Upload Behavior

The workflow automatically determines the upload channel:
- **RC releases** (`prerelease: true`) → uploaded to `{RS_FTP_PATH}/{RS_FTP_PATH_SUFFIX}/rc/`
- **Stable releases** (`prerelease: false`) → uploaded to `{RS_FTP_PATH}/{RS_FTP_PATH_SUFFIX}/stable/`

### Examples

**Password Authentication:**
```
RS_FTP_HOST: sftp.example.com
RS_FTP_USER: deploy-user
RS_FTP_PASSWORD: secure-password
RS_FTP_PATH: /var/www/releases (variable)
RS_FTP_PATH_SUFFIX: /dolibarr (variable)

# RC release uploads to: /var/www/releases/dolibarr/rc/
# Stable release uploads to: /var/www/releases/dolibarr/stable/
```

**SSH Key Authentication:**
```
RS_FTP_HOST: sftp.example.com
RS_FTP_USER: deploy-user
RS_FTP_KEY: -----BEGIN OPENSSH PRIVATE KEY-----...
RS_FTP_PATH: /var/www/releases (variable)

# Uploads to: /var/www/releases/rc/ or /var/www/releases/stable/
```

### Skipping FTP Upload

FTP upload is automatically skipped if:
- RS_FTP credentials are not configured
- RS_FTP_HOST secret is empty
- Required authentication credentials are missing

The workflow will continue and create the GitHub release even if FTP upload fails or is skipped.

## Command-Line Script

A companion Python script (`scripts/release/dolibarr_release.py`) allows local package creation:

### Installation

```bash
# Script is ready to use, no installation needed
chmod +x scripts/release/dolibarr_release.py
```

### Usage

```bash
# Create release for current directory
python scripts/release/dolibarr_release.py --version 1.0.0

# Create release for specific module
python scripts/release/dolibarr_release.py \
  --module-dir /path/to/module \
  --version 1.0.0

# Create release without updating version
python scripts/release/dolibarr_release.py \
  --version 1.0.0 \
  --no-update-version

# Specify custom output directory
python scripts/release/dolibarr_release.py \
  --version 1.0.0 \
  --output-dir /tmp/releases
```

### Script Features

- Detects module name from descriptor
- Updates version in module files
- Creates properly structured ZIP package
- Generates checksums (SHA256, MD5)
- Excludes development files
- Validates version format

## Configuration

### Required Secrets

None required for basic GitHub Releases.

### Optional Secrets

- `MARKETPLACE_TOKEN`: For Dolistore publishing (future enhancement)

## Best Practices

1. **Always use semantic versioning**: `X.Y.Z` format
2. **Update CHANGELOG.md**: Before creating releases
3. **Use RC branches**: For testing before production release
4. **Tag from main**: Ensure main branch is stable before tagging
5. **Test locally**: Use the script to test package creation

## Troubleshooting

### Module Name Not Detected

- Ensure `core/modules/mod*.class.php` exists
- Check repository name follows `MokoDoli*` or `dolibarr-*` convention

### Version Not Updated

- Verify module descriptor syntax: `$this->version = 'X.Y.Z'`
- Check file permissions and encoding

### Package Missing Files

- Review exclusion list in workflow
- Verify file paths are correct

## Example: Full Release Process

```bash
# 1. Update version and changelog
vim CHANGELOG.md  # Add [1.0.0] section
git add CHANGELOG.md
git commit -m "docs: prepare v1.0.0 release"

# 2. Create RC for testing
git checkout -b rc/1.0.0
git push origin rc/1.0.0  # Triggers pre-release build

# 3. Test RC release
# ... test the RC package ...

# 4. Merge to main and tag
git checkout main
git merge rc/1.0.0
git tag v1.0.0
git push origin main
git push origin v1.0.0  # Triggers production release

# 5. Verify release
# Check GitHub Releases page for artifacts
```

## Support

For issues or questions:

- Open issue in MokoStandards repository
- Tag with `workflow-template` label
- Include module name and error details
