# Auto-Update Changelog Workflow Template

This workflow automatically updates CHANGELOG.md when a pull request is merged to the main branch.

## Features

- ✅ Automatically extracts PR information (title, number, author, labels)
- ✅ Determines change type from PR labels or title keywords
- ✅ Parses PR description for detailed changelog content
- ✅ Updates CHANGELOG.md in UNRELEASED section
- ✅ Creates appropriate section (Added, Changed, Fixed, etc.)
- ✅ Commits changes with descriptive message
- ✅ Posts comment on PR confirming update
- ✅ Creates CHANGELOG.md if it doesn't exist
- ✅ Skips CI on changelog commits ([skip ci])

## Change Type Detection

The workflow determines the change type based on:

### From PR Labels
- `breaking` → Breaking Changes
- `security` → Security
- `deprecated` → Deprecated
- `bug` or `fix` → Fixed
- `removed` or `delete` → Removed
- `changed` or `update` → Changed
- Default → Added

### From PR Title Keywords
Same keywords as labels (case-insensitive)

## Usage

### Installation

1. Copy this file to `.github/workflows/auto-update-changelog.yml`
2. Ensure `CHANGELOG.md` follows Keep a Changelog format
3. Commit and push

### Configuration

#### Branch Names
```yaml
on:
  pull_request:
    types: [closed]
    branches:
      - main        # Adjust to your default branch
      - master      # Or add multiple branches
```

#### Permissions
```yaml
permissions:
  contents: write        # To commit changelog
  pull-requests: read    # To read PR info
```

### CHANGELOG.md Format

The workflow expects this structure:

```markdown
# Changelog

## [UNRELEASED]

### Added
- Feature descriptions

### Changed
- Change descriptions

### Fixed
- Bug fix descriptions

### Security
- Security fix descriptions

### Deprecated
- Deprecated feature notices

### Removed
- Removed feature notices

### Breaking Changes
- Breaking change descriptions
```

## PR Description Format

For best results, structure your PR description like this:

```markdown
## Summary

Brief description of changes.

### Changes Made

- Specific change 1
- Specific change 2
- Specific change 3

### Impact

How this affects the system.
```

The workflow will extract this content and add it to the changelog.

## Examples

### Example 1: Feature Addition

**PR Title**: "Add user authentication feature"
**PR Labels**: `enhancement`, `feature`
**Result**: Added to `### Added` section in CHANGELOG.md

```markdown
### Added
- **PR #123**: Add user authentication feature (by @developer)
  JWT-based authentication with refresh tokens
  Login and logout endpoints
  Password hashing with bcrypt
```

### Example 2: Bug Fix

**PR Title**: "Fix: Resolve null pointer exception in user service"
**PR Labels**: `bug`
**Result**: Added to `### Fixed` section

```markdown
### Fixed
- **PR #124**: Fix: Resolve null pointer exception in user service (by @developer)
  Added null checks in getUserById method
  Improved error handling for missing users
```

### Example 3: Breaking Change

**PR Title**: "BREAKING: Change API response format"
**PR Labels**: `breaking change`
**Result**: Added to `### Breaking Changes` section

```markdown
### Breaking Changes
- **PR #125**: BREAKING: Change API response format (by @developer)
  API responses now wrapped in { data, error, meta } structure
  Old format no longer supported
  Migration guide in docs/migration.md
```

## Customization

### Change Type Keywords

Modify the change type detection logic in the workflow:

```yaml
- name: Extract PR Information
  run: |
    # Add custom keywords or change priority
    if echo "$PR_TITLE" | grep -qi "YOUR_KEYWORD"; then
      echo "change_type=Your Type" >> $GITHUB_OUTPUT
    fi
```

### Changelog Entry Format

Modify the changelog entry format:

```yaml
- name: Update CHANGELOG.md with PR content
  run: |
    # Customize entry format
    ENTRY="- **PR #$PR_NUMBER**: $PR_TITLE (by @$PR_USER on $DATE)"
```

### Content Extraction

Modify how content is extracted from PR description:

```yaml
- name: Parse PR Description for Changelog Content
  run: |
    # Add custom parsing logic
    echo "$PR_BODY" | grep -A 50 "## Your Section" > /tmp/content.txt
```

## Integration with Pre-Merge Checklist

This workflow complements the pre-merge checklist:

1. **Developer** manually updates CHANGELOG during development (preferred)
2. **If missed**, this workflow adds entry automatically on merge
3. **Post-merge**, dev can edit changelog entry for more detail

### Recommended Practice

Use this workflow as **backup**, not replacement for manual updates:

- ✅ Manually update CHANGELOG.md in PR (best practice)
- ✅ Use this workflow to catch missed updates
- ✅ Review and enhance auto-generated entries post-merge

## Troubleshooting

### Workflow Not Triggering

Check:
- PR was actually merged (not just closed)
- Branch is in the `branches` list
- Workflow file in `.github/workflows/`
- Workflow has proper permissions

### Commit Fails

Check:
- `GITHUB_TOKEN` has write permissions
- No branch protection preventing bot commits
- No conflicts in CHANGELOG.md

### Wrong Change Type

- Add appropriate labels to PR
- Use keywords in PR title
- Modify change type detection logic

### Missing Content

- Structure PR description properly
- Include `## Summary` or similar headers
- Provide detailed description

## Related Documentation

- [Copilot Pre-Merge Checklist](../../docs/policy/copilot-pre-merge-checklist.md)
- [Change Management Policy](../../docs/policy/change-management.md)
- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)

## Workflow Details

### Triggers
- Pull request closed event on main/master branches
- Only runs if PR was merged (not just closed)

### Steps
1. Checkout repository with full history
2. Configure Git with bot credentials
3. Extract PR information (title, number, body, labels, user)
4. Determine change type from labels/title
5. Parse PR description for changelog content
6. Check if CHANGELOG.md exists (create if missing)
7. Update CHANGELOG.md in UNRELEASED section
8. Commit changes with descriptive message
9. Push to main branch
10. Comment on PR confirming update
11. Generate workflow summary

### Outputs
- Updated CHANGELOG.md file
- Git commit with changelog update
- Comment on merged PR
- Workflow summary

## Security Considerations

- Uses `GITHUB_TOKEN` with minimal required permissions
- Bot commits skip CI to avoid loops
- Read-only access to PR information
- Write access only to repository contents

## Performance

- Lightweight: completes in ~30 seconds
- No external dependencies
- Uses built-in GitHub Actions features
- Minimal resource usage

## Maintenance

Review and update:
- Change type keywords as project evolves
- Changelog format as standards change
- Content extraction logic for better parsing
- Error handling for edge cases

---

**Version**: 03.00.00
**Last Updated**: 2026-01-28
**Maintained By**: Development Team
