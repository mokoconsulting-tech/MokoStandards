# Update .gitignore Patterns Script

**Script**: `update_gitignore_patterns.sh`  
**Version**: 01.00.00  
**Purpose**: Standardize .gitignore patterns across all repositories

## Overview

This script automatically adds or updates .gitignore patterns to exclude Sublime Text configuration files and SFTP sync configuration files from version control. It replaces old specific patterns with more general wildcard patterns for better maintainability.

## Patterns Managed

### Added Patterns
- `*.sublime*` - Matches all Sublime Text configuration files (*.sublime-project, *.sublime-workspace, *.sublime-settings, etc.)
- `sftp-config*.json` - Matches SFTP sync configuration files

### Removed Patterns
The script removes these old specific patterns and replaces them with the more general `*.sublime*` pattern:
- `*.sublime-project`
- `*.sublime-workspace`

## Usage

### Basic Usage

Update .gitignore in the current directory:
```bash
./scripts/update_gitignore_patterns.sh
```

### Update Specific Directory

Update .gitignore in a specific repository:
```bash
./scripts/update_gitignore_patterns.sh /path/to/repository
```

### Recursive Mode

Update all .gitignore files in multiple repositories:
```bash
./scripts/update_gitignore_patterns.sh -r /path/to/repositories
```

### Dry Run

Preview changes without modifying files:
```bash
./scripts/update_gitignore_patterns.sh -r -d /path/to/repositories
```

## Options

| Option | Description |
|--------|-------------|
| `-h, --help` | Show help message and usage examples |
| `-r, --recursive` | Process all .gitignore files recursively |
| `-d, --dry-run` | Preview changes without making modifications |
| `-v, --verbose` | Enable verbose output |

## Examples

### Example 1: Update MokoStandards Templates

Update all .gitignore files in the templates directory:
```bash
cd /path/to/MokoStandards
./scripts/update_gitignore_patterns.sh -r templates/
```

### Example 2: Bulk Update Organization Repositories

Update all repositories in an organization workspace:
```bash
# Clone all repos first
cd ~/workspace/mokoconsulting-tech/

# Update all .gitignore files
/path/to/MokoStandards/scripts/update_gitignore_patterns.sh -r .

# Review changes
git status

# Commit changes to each repo
for dir in */; do
  cd "$dir"
  if [ -n "$(git status --porcelain .gitignore)" ]; then
    git add .gitignore
    git commit -m "chore: standardize .gitignore patterns for Sublime Text and SFTP"
    git push
  fi
  cd ..
done
```

### Example 3: Test Changes First

Always test with dry-run before making changes:
```bash
# Dry run first
./scripts/update_gitignore_patterns.sh -r -d ~/repositories/

# If changes look good, run for real
./scripts/update_gitignore_patterns.sh -r ~/repositories/
```

## How It Works

1. **Pattern Detection**: Checks if patterns already exist in .gitignore
2. **Old Pattern Removal**: Removes `*.sublime-project` and `*.sublime-workspace` if found
3. **New Pattern Addition**: Adds `*.sublime*` and `sftp-config*.json` if not present
4. **Section Organization**: Adds patterns to "OS / Editor / IDE" section if it exists, or creates it
5. **Idempotent**: Safe to run multiple times - won't duplicate patterns

## Integration with Repo Health

This script is integrated into the repository health scoring system. The health check validates that repositories have the correct .gitignore patterns.

**Health Check**: `.gitignore patterns` (1 point)
- **Requirement**: .gitignore must contain both `*.sublime*` and `sftp-config*.json` patterns
- **Remediation**: Run this script to add missing patterns
- **Category**: Required Documentation
- **Impact**: Contributes to overall repository health score

See [health-scoring.md](../docs/policy/health-scoring.md) for more details on repository health scoring.

## Best Practices

1. **Backup First**: While the script is safe, always have backups or committed work
2. **Test with Dry Run**: Use `-d` flag to preview changes before applying
3. **Review Changes**: Check `git diff` after running to verify changes
4. **Commit Separately**: Commit .gitignore changes separately from code changes
5. **Run Recursively**: Use `-r` flag to update multiple repositories at once
6. **Regular Updates**: Run periodically to ensure all repositories stay standardized

## Troubleshooting

### Script Reports "No Changes Needed"

This means the patterns are already correctly configured in your .gitignore file.

### Patterns Added in Wrong Location

The script looks for "# OS / Editor / IDE" section marker. If your .gitignore uses different section headers, patterns will be added at the end. You can manually reorganize them after running the script.

### Permission Denied

Make sure the script is executable:
```bash
chmod +x scripts/update_gitignore_patterns.sh
```

Or run with bash explicitly:
```bash
bash scripts/update_gitignore_patterns.sh
```

## Contributing

If you encounter issues or have suggestions for improving this script:

1. Check if similar patterns are already handled
2. Test your changes with dry-run first
3. Update this documentation
4. Submit a pull request with your improvements

## See Also

- [Repository Health Scoring](../docs/policy/health-scoring.md)
- [.gitignore Templates](../templates/repos/)
- [Bulk Repository Updates Guide](../docs/guide/bulk-repository-updates.md)

## Metadata

| Field | Value |
|-------|-------|
| Script | update_gitignore_patterns.sh |
| Path | /scripts/update_gitignore_patterns.sh |
| Version | 01.00.00 |
| License | GPL-3.0-or-later |
| Repository | https://github.com/mokoconsulting-tech/MokoStandards |
