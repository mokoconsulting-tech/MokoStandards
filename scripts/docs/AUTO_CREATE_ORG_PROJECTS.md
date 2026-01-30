# Auto-Create Organization Projects

## Overview

The `auto_create_org_projects.py` script automatically creates smart GitHub Projects for every repository in the mokoconsulting-tech organization. It intelligently detects project types (Joomla, Dolibarr, or Generic) and creates appropriate project structures with customized fields and views.

## Features

- **Automatic Project Type Detection**: Detects Joomla, Dolibarr, or generic projects
- **Smart Project Creation**: Creates projects with type-specific custom fields and views
- **Roadmap Generation**: Automatically generates roadmaps for repos that don't have one
- **Roadmap Push**: Pushes generated roadmaps directly to repository docs/ROADMAP.md
- **MokoStandards Integration**: Respects existing Project #7 for MokoStandards
- **Dry Run Mode**: Test without making actual changes
- **Verbose Logging**: Detailed output for debugging

## Requirements

### Authentication

One of the following authentication methods:

1. **GitHub Token** (Recommended for automation):
   ```bash
   export GH_PAT="your_personal_access_token"
   ```

2. **GitHub CLI**:
   ```bash
   gh auth login
   ```

### Token Permissions

The token needs the following scopes:
- `repo` - Full repository access
- `project` - Project read/write access
- `read:org` - Organization read access

### Python Dependencies

```bash
pip3 install requests
```

## Usage

### Basic Usage

```bash
# Dry run first to see what would happen
python3 scripts/auto_create_org_projects.py --dry-run

# Actually create projects and roadmaps
export GH_PAT="your_token"
python3 scripts/auto_create_org_projects.py
```

### With Verbose Logging

```bash
python3 scripts/auto_create_org_projects.py --verbose
```

### For a Different Organization

```bash
python3 scripts/auto_create_org_projects.py --org your-org-name
```

### Combined Options

```bash
python3 scripts/auto_create_org_projects.py --dry-run --verbose --org mokoconsulting-tech
```

## What It Does

### 1. Repository Discovery

- Fetches all repositories in the organization
- Filters out archived repositories
- Skips MokoStandards (Project #7 already exists)

### 2. Project Type Detection

Automatically detects project type based on repository contents:

**Joomla Projects:**
- Presence of `.xml` manifest files
- Joomla-specific directory structure (`administrator/`, `components/`, etc.)
- Manifest content contains "joomla" keywords

**Dolibarr Projects:**
- Module descriptor files (`mod*.class.php`)
- Dolibarr directory structure (`htdocs/`, `core/modules/`)
- Class files in standard Dolibarr structure

**Generic Projects:**
- Any repository not matching Joomla or Dolibarr patterns
- Default fallback type

### 3. Roadmap Management

For each repository:

1. **Check for Existing Roadmap**: Looks for `docs/ROADMAP.md`
2. **Generate if Missing**: Creates type-specific roadmap with:
   - Version-based milestone structure
   - Appropriate deliverables for project type
   - Metadata and revision history
3. **Push to Repository**: Commits roadmap directly to default branch

#### Roadmap Structure

**Joomla Projects:**
- Joomla version compatibility tracking
- Extension-specific milestones
- Marketplace considerations

**Dolibarr Projects:**
- Dolibarr version compatibility
- Module number and descriptor tracking
- Database migration planning

**Generic Projects:**
- Standard version milestones
- Core functionality tracking
- General development phases

### 4. Project Creation

Creates GitHub Project v2 with:

**Common Fields (All Types):**
- Status (Backlog, Todo, In Progress, etc.)
- Priority (Critical, High, Medium, Low)
- Size/Effort (XS, S, M, L, XL, XXL)
- Sprint
- Target Version
- Blocked Reason
- Acceptance Criteria

**Joomla-Specific Fields:**
- Joomla Version
- Extension Type
- Marketplace Status
- Update Server URL
- PHP Minimum Version
- Installation Type

**Dolibarr-Specific Fields:**
- Dolibarr Version
- Module Number
- Database Changes
- Module Descriptor Path
- Module Version
- Requires Sudo

**Generic Fields:**
- Technology Stack
- Environment
- Release Channel
- API Version
- Deployment Status

### 5. Project Views

Creates standard views for each project:

1. **Master Backlog** (Table) - All items by priority
2. **Sprint Board** (Board) - Kanban view by status
3. **Release Roadmap** (Roadmap) - Timeline by version
4. **Blocked Items** (Table) - Items needing attention

Plus type-specific views:
- **Joomla**: Extension Compatibility Matrix, Marketplace Pipeline
- **Dolibarr**: Module Compatibility Matrix, Database Migration Tracker
- **Generic**: Deployment Pipeline, Technology Stack View

## Example Output

```
==============================================================================
Auto-Create Smart Projects for Organization Repositories
==============================================================================

🔍 Fetching repositories from mokoconsulting-tech...
✅ Found 15 total repositories (12 active)

==============================================================================
Processing: MokoDoliTools
==============================================================================
  📦 Detected type: dolibarr
  ⚠️  No roadmap found, creating one...
  📋 Creating/updating roadmap for MokoDoliTools...
  ✅ Roadmap created/updated for MokoDoliTools

📁 Creating project for MokoDoliTools (dolibarr)...
  ✅ Project creation queued for MokoDoliTools

==============================================================================
Processing: MokoJoomlaExtension
==============================================================================
  📦 Detected type: joomla
  ✅ Roadmap already exists

📁 Creating project for MokoJoomlaExtension (joomla)...
  ✅ Project creation queued for MokoJoomlaExtension

==============================================================================
SUMMARY REPORT
==============================================================================

📊 Organization: mokoconsulting-tech
✅ Projects Created: 12
📋 Roadmaps Created: 8
⏭️  Repositories Skipped: 1

✅ Created Projects:
   - MokoDoliTools
   - MokoJoomlaExtension
   ...

📋 Created Roadmaps:
   - MokoDoliTools
   - MokoGenericProject
   ...

⏭️  Skipped Repositories:
   - MokoStandards (existing)

==============================================================================

✅ Processing complete!
```

## Integration with Existing Infrastructure

### Leverages Existing Templates

The script uses the project configuration templates from:
- `templates/projects/joomla-project-config.json`
- `templates/projects/dolibarr-project-config.json`
- `templates/projects/generic-project-config.json`

### Respects MokoStandards Project #7

The script explicitly skips MokoStandards repository since it already has Project #7 configured and operational.

### Uses GitHub GraphQL API

Leverages the same GraphQL API patterns as `setup_github_project_v2.py` for consistency.

## Dry Run Mode

Always test with `--dry-run` first:

```bash
python3 scripts/auto_create_org_projects.py --dry-run --verbose
```

This will show you:
- Which repositories would be processed
- What project types would be detected
- Which roadmaps would be created
- What projects would be created

No actual changes are made in dry run mode.

## Error Handling

The script handles errors gracefully:

- **Authentication Failures**: Clear messages about token requirements
- **API Errors**: Captured and reported at the end
- **Missing Configs**: Falls back to generic template
- **Repository Access Issues**: Skips and continues

All errors are collected and displayed in the summary report.

## Troubleshooting

### "requests library required"

```bash
pip3 install requests
```

### "GitHub token required"

```bash
export GH_PAT="your_token"
# OR
gh auth login
```

### "Permission denied"

Ensure your token has:
- `repo` scope
- `project` scope
- `read:org` scope

### "Failed to detect project type"

The script will fall back to "generic" type. You can manually adjust the project after creation.

### "Roadmap creation failed"

Check that:
- Token has write access to repository
- Default branch name is correct
- `docs/` directory exists or can be created

## Best Practices

1. **Always Dry Run First**: Test with `--dry-run` before making changes
2. **Use Verbose Mode**: Easier to debug with `--verbose`
3. **Check Token Permissions**: Ensure token has all required scopes
4. **Review Generated Roadmaps**: Customize roadmaps after automatic generation
5. **Monitor API Rate Limits**: Script may hit rate limits with many repos

## Next Steps After Running

After the script completes:

1. **Review Projects**: Check created projects in GitHub UI
2. **Customize Roadmaps**: Edit generated roadmaps for specific needs
3. **Configure Automations**: Set up GitHub Actions for project automation
4. **Add Initial Items**: Populate projects with issues and tasks
5. **Share with Team**: Notify team members about new project structure

## Integration with CI/CD

You can run this script in GitHub Actions:

```yaml
name: Auto-Create Projects

on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly
  workflow_dispatch:

jobs:
  create-projects:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - name: Install dependencies
        run: pip install requests
      - name: Create projects
        env:
          GH_PAT: ${{ secrets.GH_PAT }}
        run: python3 scripts/auto_create_org_projects.py --verbose
```

## See Also

- [setup_github_project_v2.py](./run/setup_github_project_v2.py) - Single project setup
- [sync_file_to_project.py](./automation/sync_file_to_project.py) - Sync documentation files to Project #7
- [templates/projects/README.md](../templates/projects/README.md) - Project templates documentation
- [bulk_update_repos.py](./bulk_update_repos.py) - Bulk repository updates

## Support

For issues or questions:
1. Check this documentation
2. Run with `--dry-run --verbose` for debugging
3. Review error messages in summary report
4. Open issue in MokoStandards repository
5. Contact development team

## Version History

| Version  | Date       | Changes                                          |
| -------- | ---------- | ------------------------------------------------ |
| 01.00.00 | 2026-01-12 | Initial release with auto-detection and roadmap generation |
