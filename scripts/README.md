# GitHub Project v2 Setup

This directory contains automation for setting up the GitHub Project v2 "MokoStandards Documentation Control Register".

## Requirements

- Python 3.7+
- `requests` library (for API access with token)
- GitHub Personal Access Token with permissions:
  - `project` (read and write)
  - `read:org` (organization read)
  - `repo` (repository access)

## Usage

### Option 1: Using GH_PAT Repository Secret (Recommended)

The script will automatically use the `GH_PAT` environment variable if available:

```bash
export GH_PAT="your_personal_access_token"
python3 scripts/setup_github_project_v2.py
```

### Option 2: Using GitHub CLI

If you have `gh` CLI authenticated:

```bash
gh auth login
python3 scripts/setup_github_project_v2.py
```

## What the Script Does

The script performs the following steps:

1. **Verifies Authentication** - Checks for GH_PAT token or gh CLI authentication
2. **Gets Organization ID** - Retrieves the mokoconsulting-tech organization ID
3. **Creates Project v2** - Creates "MokoStandards Documentation Control Register"
4. **Creates Custom Fields** - Defines 15 custom fields:
   - **Single-select fields**: Status, Priority, Risk Level, Document Type, Document Subtype, Owner Role, Approval Required, Evidence Required, Review Cycle, Retention
   - **Text fields**: Document Path, Dependencies, Acceptance Criteria, RACI, KPIs
5. **Scans Repository** - Finds all .md files in `docs/` and `templates/` directories
6. **Creates Project Items** - One item per document with inferred metadata:
   - Document Type: Inferred from path (policy/guide/checklist/overview/index)
   - Document Subtype: Inferred from path (waas/catalog/core/guide/policy)
   - Approval Required: "Yes" for policies, "No" otherwise
   - Other fields: Set to conservative defaults (Status=Planned, Priority=Medium, etc.)
7. **Generates Summary** - Reports total items created and any errors

## Expected Results

- **Project Created**: GitHub Project v2 with project number
- **Custom Fields**: 15 fields created (10 single-select, 5 text)
- **Project Items**: ~62 items (38 docs + 24 templates)
- **Field Values**: Automatically set based on document location and type

## Notes

- Multi-select fields (Compliance Tags, Evidence Artifacts) must be created manually via UI
- The script uses conservative default values for all fields
- Duplicate items are skipped based on document path
- The script will stop immediately on critical failures (auth, project creation, field creation)

## Troubleshooting

### "Authentication required"
- Ensure GH_PAT is set: `echo $GH_PAT`
- Or authenticate gh CLI: `gh auth login`

### "Failed to get organization ID"
- Ensure token has `read:org` permission
- Verify you have access to mokoconsulting-tech organization

### "Failed to create project"
- Ensure token has `project` write permission
- Verify you have project creation rights in the organization

### "Failed to create field"
- This is a critical error - script will stop
- Check API response for specific error messages
- Verify project was created successfully
