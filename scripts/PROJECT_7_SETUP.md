# GitHub Project #7 Setup Guide

This guide explains how to use the `setup_project_7.py` script to create or update GitHub Project #7 with version tracking capabilities.

## Overview

The `setup_project_7.py` script is a specialized version of the generic project setup script that:
- Targets Project #7 specifically
- Adds a "Target Version Number" field for tracking documentation versions
- Checks for existing projects to avoid duplicates
- Tags all items with a specified version number

## Features

### Core Capabilities

1. **Project Number Targeting**: Specifically creates or updates Project #7
2. **Version Tracking**: Adds "Target Version Number" custom field
3. **Duplicate Prevention**: Checks for existing Project #7 before creating
4. **Document Scanning**: Scans docs/ and templates/ directories
5. **Custom Fields**: Creates 16 custom fields (15 standard + version field)
6. **View Documentation**: Documents required views for manual setup
7. **Verbose Error Handling**: Detailed logging for debugging

### Custom Fields Created

**Single-select fields (10):**
- Status
- Priority
- Risk Level
- Document Type
- Document Subtype
- Owner Role
- Approval Required
- Evidence Required
- Review Cycle
- Retention

**Text fields (6):**
- Document Path
- Dependencies
- Acceptance Criteria
- RACI
- KPIs
- **Target Version Number** ⭐ (new)

## Usage

### Basic Usage

```bash
export GH_PAT="your_personal_access_token"
python3 scripts/setup_project_7.py --target-version "1.0.0"
```

### With Verbose Logging

```bash
python3 scripts/setup_project_7.py --verbose --target-version "1.0.0"
```

### Skip View Documentation

```bash
python3 scripts/setup_project_7.py --skip-views --target-version "1.0.0"
```

### Using GitHub CLI

```bash
gh auth login
python3 scripts/setup_project_7.py --target-version "1.0.0"
```

## Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--target-version` | Version number for documentation items | `1.0.0` |
| `--verbose` | Enable detailed error logging | `false` |
| `--skip-views` | Skip view documentation | `false` |

## GitHub Actions Workflow

You can also use the GitHub Actions workflow for automated setup:

### Steps:

1. Go to **Actions** tab in GitHub
2. Select **"Setup Project 7"** workflow
3. Click **"Run workflow"**
4. Fill in the inputs:
   - **target_version**: e.g., "1.0.0" (required)
   - **verbose**: Check to enable verbose logging (optional)
   - **skip_views**: Check to skip view documentation (optional)
5. Click **"Run workflow"**

### Workflow Features:

- Automated execution via GitHub Actions
- Workflow summary with configuration details
- Error reporting with debugging tips
- Uses repository `GH_PAT` secret for authentication

## What the Script Does

The script performs the following steps:

1. **Verifies Authentication** - Checks for GH_PAT token or gh CLI
2. **Gets Organization ID** - Retrieves mokoconsulting-tech org ID
3. **Checks Existing Project** - Looks for existing Project #7
4. **Creates/Updates Project** - Creates if not exists, uses existing otherwise
5. **Creates Custom Fields** - Including "Target Version Number"
6. **Scans Repository** - Finds all .md files in docs/ and templates/
7. **Creates Project Items** - One item per document with version tag
8. **Documents Views** - Provides configuration for Board, Table, Roadmap views
9. **Generates Summary** - Comprehensive report with errors and statistics

## Target Version Number Field

The "Target Version Number" field allows you to:

- Track which documentation is planned for specific releases
- Filter and group documents by target version
- Plan documentation releases alongside code releases
- Maintain version history for documentation changes

**Example use cases:**
- Planning documentation for v1.0.0 release
- Tracking which docs need updates for v2.0.0
- Coordinating documentation with software releases

## Expected Results

After running the script, you should have:

- **Project #7** created or updated
- **16 custom fields** (10 single-select, 6 text)
- **~59 project items** (from docs + templates scan)
- **3 documented views** (Board, Table, Roadmap)
- **All items tagged** with your specified version number

## Differences from Generic Setup

| Feature | Generic Setup | Project #7 Setup |
|---------|---------------|------------------|
| Project Number | Auto-assigned | Specifically #7 |
| Target Version Field | ❌ No | ✅ Yes |
| Existing Project Check | ❌ No | ✅ Yes |
| Version in Item Body | ❌ No | ✅ Yes |
| Version Field Populated | N/A | ✅ Automatic |

## Troubleshooting

### "Project #7 already exists"

**Solution:** The script will use the existing Project #7 and continue with field and item creation. This is expected behavior.

### "Failed to create field 'Target Version Number'"

**Possible causes:**
- Token lacks `project` write permission
- Project wasn't created successfully
- Network or API issues

**Solution:** 
- Verify token permissions
- Use `--verbose` for detailed error information
- Check GitHub API status

### Target Version Not Set on Items

**Possible causes:**
- Field creation failed
- Field ID wasn't captured correctly

**Solution:**
- Check that "Target Version Number" field was created successfully
- Use `--verbose` to see field creation details
- Manually set field values in GitHub UI if needed

### Debugging with Verbose Mode

Use `--verbose` to see:
- GraphQL query details and responses
- Field creation results and IDs
- Item creation progress
- Detailed error messages with stack traces
- API request/response information

## Best Practices

1. **Version Naming**: Use semantic versioning (e.g., "1.0.0", "2.1.0")
2. **Regular Updates**: Re-run script with new versions for each release cycle
3. **Backup**: Keep track of project number and field IDs
4. **Documentation**: Update this guide with project-specific customizations
5. **Testing**: Test with `--verbose` first to catch issues early

## See Also

- [Generic Project Setup](README.md) - For creating projects with auto-assigned numbers
- [GitHub Projects v2 Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [GitHub GraphQL API](https://docs.github.com/en/graphql)

## Support

For issues or questions:
1. Check this documentation first
2. Run with `--verbose` for debugging
3. Review error messages and stack traces
4. Check GitHub API status
5. Consult GitHub Projects v2 documentation
