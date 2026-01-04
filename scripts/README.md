# GitHub Project v2 Automation Scripts

This directory contains automation scripts for managing the GitHub Project v2 "MokoStandards Documentation Control Register".

## Requirements

- Python 3.7+
- `requests` library (for API access with token)
- GitHub Personal Access Token with permissions:
  - `project` (read and write)
  - `read:org` (organization read)
  - `repo` (repository access)

## Available Scripts

### 1. `setup_github_project_v2.py` - Create New Project

Creates a brand new GitHub Project v2 and populates it with documentation tasks.

**Usage:**
```bash
export GH_PAT="your_personal_access_token"
python3 scripts/setup_github_project_v2.py
```

### 2. `populate_project_from_scan.py` - Populate Existing Project

Scans docs/ and templates/ directories and populates an existing project with tasks.

**Usage:**
```bash
export GH_PAT="your_personal_access_token"
python3 scripts/populate_project_from_scan.py --project-number 7
```

**Features:**
- Works with existing Project #7
- Lists all subdirectories in templates/
- Scans all .md files in docs/ and templates/
- Creates tasks for each document
- Does not create custom fields (uses existing)

### 3. `ensure_docs_and_project_tasks.py` - Enterprise Documentation Control

Ensures all canonical documents exist and have corresponding tasks in Project #7.

**Usage:**
```bash
export GH_PAT="your_personal_access_token"
python3 scripts/ensure_docs_and_project_tasks.py
```

**Features:**
- Validates against canonical document list
- Generates missing documents using enterprise standards
- Creates tasks in Project #7 for all canonical documents
- Uses strict enterprise field model
- Provides detailed summary report

### 4. `setup_project_views.py` - Configure Project Views

Sets up the required views for Project #7 according to enterprise specifications.

**Usage:**
```bash
export GH_PAT="your_personal_access_token"
python3 scripts/setup_project_views.py --project-number 7
```

**Features:**
- Documents 6 required project views
- Provides detailed configuration instructions for manual setup
- Views included:
  - Master Register (comprehensive table view)
  - Execution Kanban (board view for active work)
  - Governance Gate (items requiring approval)
  - Policy Register (policy-specific view)
  - WaaS Portfolio (WaaS-specific documentation)
  - High Risk and Blockers (executive dashboard)
- Links to `/docs/guide/project-views.md` for complete specifications
- Works in documentation mode without authentication

## Authentication

### Option 1: Using GH_PAT Repository Secret (Recommended)

```bash
export GH_PAT="your_personal_access_token"
```

### Option 2: Using GitHub CLI

```bash
gh auth login
```

## What setup_github_project_v2.py Does

The original setup script performs the following steps:

1. **Verifies Authentication** - Checks for GH_PAT token or gh CLI authentication
2. **Gets Organization ID** - Retrieves the mokoconsulting-tech organization ID
3. **Creates Project v2** - Creates "MokoStandards Documentation Control Register"
4. **Creates Custom Fields** - Defines 15 custom fields:
   - **Single-select fields**: Status, Priority, Risk Level, Document Type, Document Subtype, Owner Role, Approval Required, Evidence Required, Review Cycle, Retention
   - **Text fields**: Document Path, Dependencies, Acceptance Criteria, RACI, KPIs
5. **Scans Repository** - Finds all .md files in `docs/` and `templates/` directories
6. **Creates Project Items** - One item per document with inferred metadata
7. **Generates Summary** - Reports total items created and any errors

## Canonical Document List

The `ensure_docs_and_project_tasks.py` script validates the following mandatory documents:

### Repository-Level
- `/README.md`
- `/CHANGELOG.md`
- `/LICENSE.md`

### Documentation Root and Index
- `/docs/readme.md`
- `/docs/index.md`

### Core Policies
- `/docs/policy/document-formatting.md`
- `/docs/policy/change-management.md`
- `/docs/policy/risk-register.md`
- `/docs/policy/data-classification.md`
- `/docs/policy/vendor-risk.md`

### WaaS Policies
- `/docs/policy/waas/waas-security.md`
- `/docs/policy/waas/waas-provisioning.md`
- `/docs/policy/waas/waas-tenant-isolation.md`

### Core Guides
- `/docs/guide/audit-readiness.md`

### WaaS Guides
- `/docs/guide/waas/architecture.md`
- `/docs/guide/waas/operations.md`
- `/docs/guide/waas/client-onboarding.md`

### Checklists
- `/docs/checklist/release.md`

### Templates Catalog
- `/templates/docs/README.md`
- `/templates/docs/required/README.md`
- `/templates/docs/extra/README.md`

## Enterprise Project Field Model

All scripts use the following strict enterprise field model:

### Single-select Fields (10)
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

### Multi-select Fields (2)
- Compliance Tags
- Evidence Artifacts

### Text Fields (7)
- Document Path
- Dependencies
- Acceptance Criteria
- RACI
- KPIs

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
