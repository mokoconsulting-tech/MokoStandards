[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Reserve Dolibarr Module ID Workflow

**Status**: Active | **Version**: 04.00.00 | **Effective**: 2026-02-19

## Overview

The `reserve-dolibarr-module-id.yml` workflow automates the reservation of Dolibarr module IDs from the Moko Consulting reserved range (185064-185099). It simplifies the module ID reservation process by automatically updating the module registry table and creating a pull request for approval.

## Quick Links

- **[Module Registry](../development/crm/module-registry.md)** - Official Dolibarr module number registry
- **[Run Workflow](../../.github/workflows/reserve-dolibarr-module-id.yml)** - Reserve a module ID now
- **[Development Guide](../guide/crm/dolibarr-development-guide.md)** - CRM development guide
- **[Development Standards](../policy/crm/development-standards.md)** - Coding standards

### Key Features

- **Automatic Module Name Detection**: Extracts module name from repository name
- **Auto-Assignment or Manual ID Selection**: Automatically assigns next available ID or accepts manual specification
- **Conflict Detection**: Validates that the requested ID is not already in use
- **Registry Update**: Updates the [module registry](../development/crm/module-registry.md) in MokoStandards
- **Pull Request Creation**: Automatically creates PR with all changes
- **Optional Remote Push**: Can push `DOLIBARR_MODULE_ID.txt` to target repository

### Workflow Location

**File**: `.github/workflows/reserve-dolibarr-module-id.yml`  
**Trigger**: Manual (workflow_dispatch)  
**Permissions**: `contents: write`, `pull-requests: write`  
**Repository**: [https://github.com/mokoconsulting-tech/MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards)

## Architecture

### Workflow Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    WORKFLOW FLOW DIAGRAM                         │
└─────────────────────────────────────────────────────────────────┘

  TRIGGER: Manual Workflow Dispatch
       │
       ▼
  ┌──────────────────┐
  │ Extract Module   │
  │ Name from Repo   │───┐ github.repository → ModuleName
  └──────────────────┘   │
       │                 │
       ▼                 │
  ┌──────────────────┐   │
  │ Determine ID     │◀──┘ Manual or Auto-assign
  │ (185064-185099)  │
  └──────────────────┘
       │
       ▼
  ┌──────────────────┐
  │ Check for        │
  │ Conflicts        │───┐ Scan registry table
  └──────────────────┘   │
       │                 │
       ▼                 │
  ┌──────────────────┐   │
  │ Update Module    │◀──┘
  │ Registry Table   │
  └──────────────────┘
       │
       ▼
  ┌──────────────────┐
  │ Update Override  │───┐ Protect workflow file
  │ Configuration    │   │
  └──────────────────┘   │
       │                 │
       ▼                 │
  ┌──────────────────┐   │
  │ Create Branch    │◀──┘ reserve-module-id/<id>
  │ and Commit       │
  └──────────────────┘
       │
       ▼
  ┌──────────────────┐
  │ Create Pull      │───┐ Automated PR
  │ Request          │   │
  └──────────────────┘   │
       │                 │
       ├─────────────────┘
       │
       ▼
  ┌──────────────────┐
  │ Push to Remote   │ (Optional)
  │ Repository       │
  └──────────────────┘
```

### Module ID Range

**Reserved Range**: 185064-185099 (Moko Consulting)  
**Total Available**: 36 module IDs  
**Assignment**: Sequential, starting from 185064

The workflow uses regex pattern `1850(6[4-9]|[7-8][0-9]|9[0-9])` to precisely match IDs in this range.

## Usage

### Basic Usage (Auto-Assign)

When you want to reserve the next available module ID:

```yaml
# Trigger: Actions → Reserve Dolibarr Module ID → Run workflow

Inputs:
  description: "Advanced form builder and workflow module for Dolibarr"
  repository: (leave empty or provide URL)
  module_id: (leave empty for auto-assignment)
  push_to_remote: false
  remote_repository: (leave empty)
```

**Result**: Workflow will auto-assign next available ID (e.g., 185064) and create PR.

### Manual ID Assignment

When you need a specific module ID:

```yaml
Inputs:
  description: "Digital signature module for Dolibarr"
  repository: "https://github.com/mokoconsulting-tech/MokoDoliSign"
  module_id: 185070
  push_to_remote: false
  remote_repository: ""
```

**Result**: Workflow will validate and reserve ID 185070 (if available).

### With Remote Push

When you want to push the module ID to the target repository:

```yaml
Inputs:
  description: "Google Workspace integration for Dolibarr"
  repository: "https://github.com/mokoconsulting-tech/MokoDoliG"
  module_id: (auto-assign)
  push_to_remote: true
  remote_repository: "https://github.com/mokoconsulting-tech/MokoDoliG"
```

**Result**: 
- Reserves module ID in MokoStandards
- Creates `src/DOLIBARR_MODULE_ID.txt` in remote repository
- Detects and pushes to default branch (main/master)

## Workflow Inputs

### Required Inputs

| Input | Type | Description | Example |
|-------|------|-------------|---------|
| `description` | string | Brief description of the module | "MailChimp integration for Dolibarr" |

**Note**: The `developer` input was removed in version 04.00.00. Reservations are now attributed to the GitHub user who triggered the workflow.

### Optional Inputs

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `repository` | string | (current repo) | Repository URL for the module |
| `module_id` | number | (auto-assign) | Specific module ID to assign (185064-185099) |
| `push_to_remote` | boolean | false | Push DOLIBARR_MODULE_ID.txt to remote repository |
| `remote_repository` | string | "" | Remote repository URL (required if push_to_remote=true) |

## What the Workflow Does

### 1. Module Name Extraction

The workflow automatically extracts the module name from the repository name:

```bash
# Example transformations:
mokoconsulting-tech/MokoDoliExample → MokoDoliExample
mokoconsulting-tech/MokoDoliSign   → MokoDoliSign
username/MyModule                   → MyModule
```

### 2. Module ID Determination

**Auto-Assignment Mode** (default):
- Scans [module registry](../development/crm/module-registry.md) for used IDs in range 185064-185099
- Assigns first available ID sequentially
- Fails if all IDs are reserved

**Manual Assignment Mode**:
- Validates ID is in range 185064-185099
- Checks for conflicts
- Fails if ID is already in use

### 3. Registry Table Update

Updates [`docs/development/crm/module-registry.md`](../development/crm/module-registry.md):

```markdown
| Module Name | Module Number | Status | Description | Repository |
|-------------|---------------|--------|-------------|------------|
| MokoDoliExample | 185064 | Reserved | Example module | https://github.com/mokoconsulting-tech/repo |
```

**Insertion Point**: Before the "Available for Assignment" line.

### 4. Override Configuration Update

Updates `MokoStandards.override.tf` to protect the workflow file:

```hcl
{
  path   = ".github/workflows/reserve-dolibarr-module-id.yml"
  reason = "Dolibarr module ID reservation workflow"
},
```

**Purpose**: Prevents the workflow file from being overwritten during bulk sync operations.

### 5. Pull Request Creation

Creates a PR with:
- **Branch**: `reserve-module-id/<module_id>`
- **Title**: "Reserve Dolibarr Module ID {id} for {module_name}"
- **Labels**: `dolibarr`, `module-id-reservation`, `automated`
- **Description**: Comprehensive details about the reservation

### 6. Optional Remote Push

If `push_to_remote` is enabled, creates `src/DOLIBARR_MODULE_ID.txt` in the remote repository:

```
DOLIBARR_MODULE_ID=185064

This module ID has been officially reserved in MokoStandards.

Module Name: MokoDoliExample
Module ID: 185064
Reserved Range: 185064-185099 (Moko Consulting)
Description: Example module for Dolibarr

Reserved: 2026-02-19 16:30:00 UTC

DO NOT CHANGE THIS ID!

This ID is registered in the MokoStandards module registry:
https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/development/crm/module-registry.md
```
https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/policy/crm/development-standards.md
```

## Workflow Steps

### Detailed Step Breakdown

1. **Checkout repository** - Fetches MokoStandards repository
2. **Configure Git** - Sets up git credentials for commits
3. **Extract module name** - Parses repository name
4. **Determine module ID** - Auto-assigns or validates manual ID
5. **Check for conflicts** - Ensures ID is available
6. **Update registry table** - Adds new entry to registry
7. **Update override config** - Protects workflow file
8. **Create branch and commit** - Commits changes to new branch
9. **Create pull request** - Automated PR creation
10. **Add labels** - Tags PR with relevant labels
11. **Validate remote inputs** - (Optional) Validates remote push parameters
12. **Push to remote** - (Optional) Creates DOLIBARR_MODULE_ID.txt in remote repo
13. **Output summary** - Displays reservation summary

## Output

### GitHub Actions Summary

The workflow generates a summary with:

```markdown
## 🎉 Module ID Reservation Summary

**Module Name:** MokoDoliExample
**Reserved ID:** 185064
**Pull Request:** https://github.com/mokoconsulting-tech/MokoStandards/pull/123

### Next Steps
1. Review the pull request
2. Get approval from CRM Development Lead
3. Merge the PR to officially reserve the module ID
```

### Files Modified

**In MokoStandards Repository**:
- `docs/policy/crm/development-standards.md` - Registry table updated
- `MokoStandards.override.tf` - Workflow protection added

**In Remote Repository** (if push_to_remote=true):
- `src/DOLIBARR_MODULE_ID.txt` - Module ID file created

## Error Handling

### Common Errors and Solutions

#### Error: "Module ID already in use"

**Cause**: The requested module ID is already reserved in the registry.

**Solution**: 
- If auto-assigning: Workflow will try next available ID
- If manual: Choose a different ID or use auto-assignment

```bash
# Check available IDs
grep -E "185064|185065|185066" docs/policy/crm/development-standards.md
```

#### Error: "Module ID must be in range 185064-185099"

**Cause**: Manual module_id is outside the allowed range.

**Solution**: Use an ID between 185064 and 185099 (inclusive).

#### Error: "No available module IDs in range 185064-185099"

**Cause**: All 36 IDs in the range are already reserved.

**Solution**: Contact repository maintainers to discuss expanding the range or removing obsolete reservations.

#### Error: "push_to_remote is enabled but remote_repository is not provided"

**Cause**: Enabled remote push without providing repository URL.

**Solution**: Either disable `push_to_remote` or provide `remote_repository` URL.

#### Error: "Could not find 'Available for Assignment' line in registry"

**Cause**: Registry table structure has changed.

**Solution**: Verify `docs/policy/crm/development-standards.md` contains the "Available for Assignment" marker line.

## Best Practices

### Reservation Guidelines

1. **Use Descriptive Names**: Module name should clearly indicate purpose
2. **Provide Accurate Descriptions**: Help others understand the module
3. **Reserve Before Development**: Reserve ID before starting module development
4. **One ID Per Module**: Each module should have exactly one ID
5. **Update Status**: Change from "Reserved" to "Active" once deployed

### Module Naming Conventions

- **Prefix with "MokoDoli"**: Indicates Moko Consulting Dolibarr module
- **CamelCase**: Use PascalCase for module names
- **Descriptive**: Name should indicate functionality

**Examples**:
- ✅ `MokoDoliSign` - Clear, follows conventions
- ✅ `MokoDoliForm` - Concise, descriptive
- ❌ `my-module` - Not CamelCase, not descriptive
- ❌ `Test123` - Not descriptive

### Repository Structure

After reservation, structure your Dolibarr module repository:

```
MokoDoliExample/
├── src/
│   ├── DOLIBARR_MODULE_ID.txt       # Created by workflow (if push_to_remote)
│   └── modMokoDoliExample.class.php # Module descriptor
├── class/                            # Business logic
├── langs/                            # Translations
│   ├── en_US/
│   └── fr_FR/
├── sql/                              # Database scripts
├── admin/                            # Admin pages
├── README.md
└── CHANGELOG.md
```

## Integration with MokoStandards

### Module Registry

The workflow updates the official module registry at:
`docs/policy/crm/development-standards.md`

This registry is the single source of truth for all Moko Consulting Dolibarr module IDs.

### Override Protection

The workflow protects itself from being overwritten during bulk repository sync operations by adding an entry to `MokoStandards.override.tf`.

### Policy Compliance

This workflow follows the module ID reservation process defined in:
[CRM Development Standards](../policy/crm/development-standards.md#module-id-reservation-process)

## Advanced Usage

### Batch Reservations

For reserving multiple module IDs, run the workflow multiple times. Each run will auto-assign the next available ID.

```bash
# First run: Reserves 185064
# Second run: Reserves 185065
# Third run: Reserves 185066
```

### Checking Available IDs

To see which IDs are still available:

```bash
cd /home/runner/work/MokoStandards/MokoStandards
grep -oP '(?<=\| )1850(6[4-9]|[7-8][0-9]|9[0-9])(?= \|)' \
  docs/policy/crm/development-standards.md | sort -n
```

### Updating Reserved Status

Once a module is deployed, update its status from "Reserved" to "Active":

1. Edit `docs/policy/crm/development-standards.md`
2. Change status column from "Reserved" to "Active"
3. Update repository URL if needed
4. Create PR with changes

## Troubleshooting

### Workflow Run Failed

**Check the Actions tab**: Review the failed step for error messages.

**Common issues**:
- YAML syntax errors (validate with yamllint)
- Git configuration issues
- Permission errors
- Network connectivity to remote repository

### PR Creation Failed

**Possible causes**:
- Insufficient permissions
- Base branch doesn't exist
- Branch already exists

**Solution**: Check workflow permissions in repository settings.

### Remote Push Failed

**Causes**:
- Invalid repository URL
- No push permissions
- Default branch doesn't exist

**Solution**: 
- Verify repository URL is correct
- Ensure GitHub token has push permissions
- Check default branch name (main vs master)

### ID Conflict After Merge

If two PRs reserve the same ID simultaneously:

1. The first merged PR wins
2. The second PR will show conflicts
3. Close the second PR and re-run the workflow
4. The workflow will auto-assign the next available ID

## Maintenance

### Updating the Workflow

When updating the workflow:

1. Update the VERSION field in the file header
2. Update this documentation
3. Test with dry-run if possible
4. Update the workflow inventory

### Monitoring

Monitor the module registry regularly:

```bash
# Count reserved IDs
grep -c "| Reserved |" docs/policy/crm/development-standards.md

# Count active IDs
grep -c "| Active |" docs/policy/crm/development-standards.md

# Show available slots
echo $((36 - $(grep -cE "185064|185065|..." docs/policy/crm/development-standards.md)))
```

## Examples

### Example 1: Simple Reservation

```yaml
# Input
description: "WebAuthn authentication module"
developer: "Security Team"

# Result
Module ID: 185064 (auto-assigned)
Module Name: MokoDoliPasskey (from repository name)
PR Created: #123
```

### Example 2: Specific ID with Remote Push

```yaml
# Input
description: "Multi-entity management module"
developer: "John Doe"
module_id: 185070
push_to_remote: true
remote_repository: "https://github.com/mokoconsulting-tech/MokoDoliMulti"

# Result
Module ID: 185070 (manual)
Module Name: MokoDoliMulti
PR Created: #124
Remote File: src/DOLIBARR_MODULE_ID.txt created
```

### Example 3: Conflict Handling

```yaml
# First run - Success
module_id: 185065
Result: Reserved successfully

# Second run - Conflict
module_id: 185065
Error: "Module ID 185065 is already in use!"
```

## Security Considerations

### Token Permissions

The workflow requires:
- `contents: write` - To create branches and commits
- `pull-requests: write` - To create PRs

### Remote Repository Access

When using `push_to_remote`:
- Ensure GitHub token has push access to remote repository
- Remote repository must accept push from github-actions bot
- Consider using deploy keys for production repositories

### Protected Files

The workflow file itself is protected via `MokoStandards.override.tf` to prevent accidental deletion or modification during bulk sync operations.

## Related Documentation

- [CRM Development Standards](../policy/crm/development-standards.md) - Module ID reservation policy
- [Dolibarr Module Development Guide](../guide/crm/dolibarr-development-guide.md) - Complete development guide
- [Dolibarr Workflow Templates](../templates/workflows/dolibarr.md) - CI/CD templates for modules
- [Bulk Repository Sync](./bulk-repo-sync.md) - Understanding override protection
- [Workflow Architecture](./workflow-architecture.md) - Overall workflow design patterns

## Changelog

### Version 04.00.00 (2026-02-19)

**Changed**:
- Simplified from 866 to 450 lines (48% reduction)
- Removed module documentation generation
- Module name now auto-detected from repository name
- Added optional manual module ID assignment
- Focused on core functionality: ID assignment and registry update only

**Added**:
- `module_id` optional input for manual ID assignment
- Automatic module name extraction from repository

**Removed**:
- Module documentation creation (docs/modules/)
- Module README creation
- Module ID reference file creation
- Override protection for module docs (now only protects workflow)
- Module descriptor template creation in remote repos
- README creation in remote repos

### Version 03.00.00 (2026-02-16)

**Initial release**:
- Full documentation generation
- Registry table updates
- PR automation
- Remote push support

## Support

For issues or questions about this workflow:

1. Check this documentation
2. Review the [CRM Development Standards](../policy/crm/development-standards.md)
3. Open an issue in the MokoStandards repository
4. Contact the MokoStandards maintainers

---

**Last Updated**: 2026-02-19  
**Maintained By**: MokoStandards Team  
**Category**: Workflow Documentation

## Metadata

| Field | Value |
|-------|-------|
| Document Type | Workflow Documentation |
| Domain | Documentation |
| Applies To | MokoStandards Repository |
| Jurisdiction | Tennessee, USA |
| Owner | Moko Consulting |
| Repo | https://github.com/mokoconsulting-tech/MokoStandards |
| Path | /docs/workflows/reserve-dolibarr-module-id.md |
| Version | 04.00.00 |
| Status | Active |
| Last Reviewed | 2026-02-19 |
| Reviewed By | Documentation Team |

## Revision History

| Date | Author | Change | Notes |
|------|--------|--------|-------|
| 2026-02-19 | GitHub Copilot | Initial documentation creation | Comprehensive workflow documentation for v04.00.00 |
