[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# SHA-256 Auto-Update Automation

## Overview

This automation ensures that SHA-256 verification hashes in workflow files stay synchronized with the actual file contents. It prevents verification failures when scripts are updated but their hashes aren't.

## Components

### 1. Update Script: `scripts/maintenance/update_sha_hashes.py`

Python script that:
- Calculates SHA-256 hashes of tracked files
- Updates corresponding workflow files with new hashes
- Supports dry-run mode for safety
- Provides detailed logging

**Usage:**
```bash
# Check what would be updated (dry run)
python3 scripts/maintenance/update_sha_hashes.py --dry-run --verbose

# Actually update the hashes
python3 scripts/maintenance/update_sha_hashes.py

# Show detailed output
python3 scripts/maintenance/update_sha_hashes.py --verbose
```

**Configuration:**

The script uses the `SHA_MAPPINGS` configuration at the top of the file:

```python
SHA_MAPPINGS = [
    {
        'source_file': 'scripts/validate/validate_codeql_config.py',
        'workflow_file': '.github/workflows/standards-compliance.yml',
        'pattern': r'EXPECTED_SHA256="([a-f0-9]{64})"',
        'description': 'CodeQL configuration validator'
    }
]
```

To track additional files, add more entries to this list.

### 2. GitHub Workflow: `.github/workflows/auto-update-sha.yml`

Automated workflow that:
- Triggers on push to main (after merge)
- Only runs when tracked files change
- Calculates new SHA-256 hashes
- Commits and pushes updates automatically
- Can be triggered manually

**Trigger Conditions:**
- Automatic: When `scripts/validate/validate_codeql_config.py` changes
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
│ File changed?       │
│ validate_codeql_*   │
└──────────┬──────────┘
           │ Yes
           ▼
┌─────────────────────┐
│ Calculate SHA-256   │
│ of current file     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Update workflow     │
│ with new hash       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Commit & Push       │
│ [skip ci]           │
└─────────────────────┘
```

## Adding New Files to Track

To track additional files for SHA verification:

1. **Edit the script** (`scripts/maintenance/update_sha_hashes.py`):
   ```python
   SHA_MAPPINGS = [
       # ... existing entries ...
       {
           'source_file': 'path/to/your/script.py',
           'workflow_file': '.github/workflows/your-workflow.yml',
           'pattern': r'EXPECTED_SHA256="([a-f0-9]{64})"',
           'description': 'Your script description'
       }
   ]
   ```

2. **Update the workflow** (`.github/workflows/auto-update-sha.yml`):
   ```yaml
   on:
     push:
       branches:
         - main
       paths:
         - 'scripts/validate/validate_codeql_config.py'
         - 'path/to/your/script.py'  # Add here
   ```

3. **Test locally**:
   ```bash
   python3 scripts/maintenance/update_sha_hashes.py --dry-run --verbose
   ```

## Manual Updates

If you need to update hashes manually:

```bash
# Check current status
python3 scripts/maintenance/update_sha_hashes.py --dry-run

# Update all hashes
python3 scripts/maintenance/update_sha_hashes.py

# Commit the changes
git add .github/workflows/
git commit -m "chore: update SHA-256 hashes"
git push
```

## Troubleshooting

### Hash Mismatch After Update

If the hash still doesn't match after the script runs:

1. Check the file wasn't modified after the update
2. Verify the pattern regex matches the workflow file format
3. Run with `--verbose` to see detailed output

### Workflow Not Triggering

If the workflow doesn't run automatically:

1. Check that the file path is listed in `on.push.paths`
2. Verify the branch is `main`
3. Check workflow permissions are set correctly

### Script Errors

Common issues:

- **File not found**: Check paths are relative to repository root
- **Pattern not matching**: Verify regex pattern matches workflow format
- **Permission denied**: Ensure script is executable (`chmod +x`)

## Related Files

- `scripts/maintenance/update_sha_hashes.py` - Main update script
- `.github/workflows/auto-update-sha.yml` - Automation workflow
- `.github/workflows/standards-compliance.yml` - Uses SHA verification

## References

- [GitHub Actions: Workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [SHA-256 Hash Function](https://en.wikipedia.org/wiki/SHA-2)
- [Python hashlib documentation](https://docs.python.org/3/library/hashlib.html)
