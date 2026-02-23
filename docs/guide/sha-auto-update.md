[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.03-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# SHA-256 Auto-Update Automation

## Overview

This automation ensures that SHA-256 verification hashes in workflow files stay synchronized with the actual file contents. It prevents verification failures when scripts are updated but their hashes aren't.

## Components

### 1. Update Script: `scripts/maintenance/update_sha_hashes.php`

PHP script that:
- Calculates SHA-256 hashes of tracked files in the script registry
- Updates `scripts/.script-registry.json` with new hashes
- Supports dry-run mode for safety
- Provides detailed logging

**Usage:**
```bash
# Check what would be updated (dry run)
php scripts/maintenance/update_sha_hashes.php --dry-run --verbose

# Actually update the hashes
php scripts/maintenance/update_sha_hashes.php

# Show detailed output
php scripts/maintenance/update_sha_hashes.php --verbose

# Show help
php scripts/maintenance/update_sha_hashes.php --help
```

**How It Works:**

The script reads the script registry at `scripts/.script-registry.json`, calculates the current SHA-256 hash for each tracked script file, and updates the registry if any hashes have changed. It automatically updates the generation timestamp when changes are made.

### 2. GitHub Workflow: `.github/workflows/auto-update-sha.yml`

Automated workflow that:
- Triggers on push to main (after merge)
- Only runs when tracked script files change
- Calculates new SHA-256 hashes using PHP
- Commits and pushes updates automatically
- Can be triggered manually

**Trigger Conditions:**
- Automatic: When any script file (*.py, *.sh, *.ps1) or the registry changes
- Manual: Via workflow_dispatch with optional force flag

**Permissions:**
- `contents: write` - Required to commit and push changes

## How It Works

### On Merge to Main

1. **File Change Detection**: Workflow triggers when tracked files are modified
2. **Hash Calculation**: Script calculates current SHA-256 of tracked files
3. **Comparison**: Compares with hash stored in workflow file
4. **Update**: If different, updates the workflow file
5. **Commit**: Auto-commits changes with `[skip ci]` tag
6. **Push**: Pushes to main branch

### Security Features

- **Hash Verification**: Ensures downloaded scripts match expected content
- **Automated Updates**: No manual intervention needed
- **Audit Trail**: All changes are committed with detailed messages
- **Skip CI**: Updates don't trigger additional workflow runs

## Workflow Diagram

```
┌─────────────────────┐
│ Push to main branch │
│ (after merge)       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Script file changed?│
│ *.py, *.sh, *.ps1   │
└──────────┬──────────┘
           │ Yes
           ▼
┌─────────────────────┐
│ Calculate SHA-256   │
│ using PHP           │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Update registry     │
│ .script-registry.   │
│ json                │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Commit & Push       │
│ [skip ci]           │
└─────────────────────┘
```

## Adding New Files to Track

The script automatically tracks all files listed in `scripts/.script-registry.json`. To add new scripts to track:

1. **Add the script to the repository** in the appropriate `scripts/` subdirectory

2. **Regenerate the registry** (if a registry generator script exists), or manually add the entry:
   ```json
   {
     "path": "scripts/your-category/your-script.sh",
     "sha256": "calculated-hash-here",
     "category": "your-category",
     "priority": "medium",
     "size_bytes": 12345
   }
   ```

3. **Test the update script**:
   ```bash
   php scripts/maintenance/update_sha_hashes.php --dry-run --verbose
   ```

## Manual Updates

If you need to update hashes manually:

```bash
# Check current status
php scripts/maintenance/update_sha_hashes.php --dry-run

# Update all hashes
php scripts/maintenance/update_sha_hashes.php

# Commit the changes
git add scripts/.script-registry.json
git commit -m "chore: update SHA-256 hashes"
git push
```

## Troubleshooting

### Hash Mismatch After Update

If the hash still doesn't match after the script runs:

1. Check the file wasn't modified after the update
2. Verify the file path in the registry is correct
3. Run with `--verbose` to see detailed output

### Workflow Not Triggering

If the workflow doesn't run automatically:

1. Check that the file path matches the patterns in `on.push.paths`
2. Verify the branch is `main`
3. Check workflow permissions are set correctly

### Script Errors

Common issues:

- **File not found**: Check paths are relative to repository root
- **Registry not found**: Ensure `scripts/.script-registry.json` exists
- **JSON parse error**: Validate the registry JSON syntax

## Related Files

- `scripts/maintenance/update_sha_hashes.php` - Main update script
- `.github/workflows/auto-update-sha.yml` - Automation workflow
- `scripts/.script-registry.json` - Script registry with SHA-256 hashes
- `.github/workflows/validate-script-integrity.yml` - Validates script hashes

## References

- [GitHub Actions: Workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [SHA-256 Hash Function](https://en.wikipedia.org/wiki/SHA-2)
- [PHP hash_file documentation](https://www.php.net/manual/en/function.hash-file.php)
