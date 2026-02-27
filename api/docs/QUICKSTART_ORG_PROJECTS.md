# Quick Start: Auto-Create Organization Projects

This guide provides a quick start for automatically creating smart GitHub Projects for all repositories in the mokoconsulting-tech organization.

## Prerequisites

- GitHub Personal Access Token with permissions:
  - `repo` (full repository access)
  - `project` (read and write)
  - `read:org` (organization read)
- Python 3.7+ with `requests` library installed

## Option 1: GitHub Actions (Recommended)

### Run via GitHub UI

1. Go to **Actions** tab in the MokoStandards repository
2. Select **"Auto-Create Organization Projects"** workflow
3. Click **"Run workflow"**
4. Configure options:
   - **Dry run**: Check to preview without making changes (recommended first time)
   - **Verbose**: Check to enable detailed logging
5. Click **"Run workflow"**
6. Review the workflow logs and summary

### Scheduled Runs

The workflow automatically runs quarterly (every 3 months) in dry-run mode to detect new repositories and changes.

## Option 2: Command Line

### Dry Run First (Recommended)

```bash
# Preview what would be created
python3 scripts/auto_create_org_projects.py --dry-run --verbose
```

### Create Projects and Roadmaps

```bash
# Set your GitHub token
export GH_PAT="your_github_token"

# Run the script
python3 scripts/auto_create_org_projects.py

# Or with verbose logging
python3 scripts/auto_create_org_projects.py --verbose
```

## What Gets Created

### For Each Repository

1. **Project Type Detection**
   - Joomla: Detects `.xml` manifests and Joomla directory structure
   - Dolibarr: Detects `mod*.class.php` descriptors and Dolibarr structure
   - Generic: Default for everything else

2. **Roadmap Generation** (if missing)
   - Creates `docs/ROADMAP.md` in the repository
   - Type-specific content with version milestones
   - Committed directly to default branch

3. **GitHub Project Creation**
   - Project with repository-specific name
   - Custom fields based on project type
   - Standard views (Master Backlog, Sprint Board, Release Roadmap, Blocked Items)
   - Type-specific views

### Custom Fields by Type

**All Projects:**
- Status, Priority, Size/Effort, Sprint, Target Version
- Blocked Reason, Acceptance Criteria

**Joomla Projects Add:**
- Joomla Version, Extension Type, Marketplace Status
- Update Server URL, Extension Version, PHP Minimum
- Installation Type, Has Frontend/Backend/API

**Dolibarr Projects Add:**
- Dolibarr Version, Module Number, Database Changes
- Module Descriptor, Module Version, PHP Minimum
- Requires Sudo, Module Family, Has Triggers/Hooks/Widgets

**Generic Projects Add:**
- Technology Stack, Environment, Release Channel
- API Version, Deployment Status, Infrastructure
- Database Type

## Quick Workflow

```bash
# 1. Test with dry run
python3 scripts/auto_create_org_projects.py --dry-run --verbose

# 2. Review the output
#    - Check detected project types
#    - Verify roadmaps to be created
#    - Confirm projects to be created

# 3. Run for real
export GH_PAT="your_token"
python3 scripts/auto_create_org_projects.py --verbose

# 4. Review created projects
#    Visit: https://github.com/orgs/mokoconsulting-tech/projects
```

## Single Repository Mode

To create a project for a specific repository:

```bash
python3 scripts/create_repo_project.py REPO_NAME --type joomla
python3 scripts/create_repo_project.py REPO_NAME --type dolibarr
python3 scripts/create_repo_project.py REPO_NAME --type generic
```

## Troubleshooting

### "GitHub token required"

Set the `GH_PAT` environment variable:
```bash
export GH_PAT="ghp_your_token_here"
```

### "Permission denied"

Verify your token has these scopes:
- `repo` - Full repository access
- `project` - Project read/write
- `read:org` - Organization read

### "Failed to detect project type"

The script defaults to "generic" type. Manually specify type when creating:
```bash
python3 scripts/create_repo_project.py REPO_NAME --type joomla
```

### "Rate limit exceeded"

GitHub API has rate limits. Wait a few minutes and try again, or use a token with higher limits.

## Best Practices

1. **Always dry-run first** to preview changes
2. **Use verbose mode** for better visibility
3. **Review generated roadmaps** and customize as needed
4. **Check created projects** and adjust fields/views
5. **Configure automations** after project creation
6. **Add initial issues** to populate the project

## Next Steps After Creation

1. **Review Projects**: Visit each project and verify configuration
2. **Customize Roadmaps**: Edit generated roadmaps for specific needs
3. **Add Issues**: Populate projects with existing issues
4. **Configure Automations**: Set up workflow automations
5. **Share with Team**: Notify team members about new project boards

## Documentation

- [Full Documentation](./AUTO_CREATE_ORG_PROJECTS.md)
- [Project Templates](../templates/projects/README.md)
- [GitHub Projects v2 Standard](../templates/projects/README.md)

## Support

For issues:
1. Check logs with `--verbose` flag
2. Review error messages
3. Consult [AUTO_CREATE_ORG_PROJECTS.md](./AUTO_CREATE_ORG_PROJECTS.md)
4. Open issue in MokoStandards repository
