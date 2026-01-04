# MokoStandards Scripts

This directory contains automation scripts for MokoStandards repository management and documentation maintenance.

## Directory Structure

The scripts are organized according to MokoStandards governance policy:

- **`docs/`** - Documentation generation and maintenance scripts
  - `rebuild_indexes.py` - Generates index.md files for documentation folders
- **`run/`** - Operational scripts for repository setup and maintenance
  - `setup_github_project_v2.py` - Sets up GitHub Project v2 for documentation control
- **`lib/`** - Shared library code (reserved for future use)
- **`fix/`** - Repository repair scripts (reserved for future use)
- **`release/`** - Release automation scripts (reserved for future use)
- **`validate/`** - Validation and linting scripts (reserved for future use)

## Scripts Overview

### Documentation Scripts (`docs/`)

#### rebuild_indexes.py

Automatically generates `index.md` files for each folder in the documentation directory.

**Usage:**
```bash
# Generate indexes
python3 scripts/docs/rebuild_indexes.py

# Check mode (CI/CD)
python3 scripts/docs/rebuild_indexes.py --check

# Custom root directory
python3 scripts/docs/rebuild_indexes.py --root path/to/docs
```

**What it does:**
- Scans documentation folders recursively
- Creates/updates index.md files with links to documents and subfolders
- Maintains consistent structure across documentation
- Supports check mode for CI/CD validation

### Operational Scripts (`run/`)

#### setup_github_project_v2.py

Sets up GitHub Project v2 "MokoStandards Documentation Control Register" with custom fields and items.

**Requirements:**
- Python 3.7+
- `requests` library (for API access with token)
- GitHub Personal Access Token with permissions:
  - `project` (read and write)
  - `read:org` (organization read)
  - `repo` (repository access)

**Usage:**

Option 1: Using GH_PAT environment variable (Recommended)
```bash
export GH_PAT="your_personal_access_token"
python3 scripts/run/setup_github_project_v2.py
```

Option 2: Using GitHub CLI
```bash
gh auth login
python3 scripts/run/setup_github_project_v2.py
```

**What it does:**
1. Verifies authentication (GH_PAT token or gh CLI)
2. Gets organization ID for mokoconsulting-tech
3. Creates "MokoStandards Documentation Control Register" project
4. Creates 15 custom fields (10 single-select, 5 text)
5. Scans repository for .md files in `docs/` and `templates/`
6. Creates project items with inferred metadata
7. Generates summary report

**Expected Results:**
- Project created with project number
- 15 custom fields (Status, Priority, Risk Level, etc.)
- ~62 project items (38 docs + 24 templates)
- Field values automatically set based on document paths

**Troubleshooting:**

Authentication issues:
- Ensure GH_PAT is set: `echo $GH_PAT`
- Or authenticate gh CLI: `gh auth login`

Organization access:
- Ensure token has `read:org` permission
- Verify access to mokoconsulting-tech organization

Project creation:
- Ensure token has `project` write permission
- Verify project creation rights in organization

Field creation failures:
- Check API response for error messages
- Verify project was created successfully

## Integration with Workflows

These scripts are integrated with GitHub Actions workflows:

- `.github/workflows/rebuild_docs_indexes.yml` - Runs `docs/rebuild_indexes.py` on documentation changes
- Template workflows in `templates/repos/` demonstrate CI/CD integration patterns

## Governance Compliance

This scripts directory structure complies with MokoStandards Scripts Governance Policy, which defines:

- **Required directories**: (none currently enforced)
- **Allowed directories**: `scripts`, `scripts/fix`, `scripts/lib`, `scripts/release`, `scripts/run`, `scripts/validate`, `scripts/docs`
- **Enforcement mode**: Advisory (scripts folder is optional)

For more details, see `.github/workflows/repo_health.yml`

## Contributing

When adding new scripts:

1. Place scripts in the appropriate subdirectory based on their purpose
2. Add documentation to this README
3. Follow Python coding standards (PEP 8)
4. Include SPDX license headers
5. Add error handling and user-friendly messages
6. Update workflows if scripts need CI/CD integration

## Notes

- Multi-select fields in GitHub Projects v2 must be created manually via UI
- Scripts use conservative default values for safety
- All scripts include comprehensive error handling and logging
- Scripts stop immediately on critical failures to prevent partial states
