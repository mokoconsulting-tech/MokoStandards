# GitHub Workflow Templates

This directory contains reusable GitHub Actions workflow templates for MokoStandards-compliant repositories.

## Available Templates

### ci-joomla.yml
Continuous Integration workflow for Joomla component repositories.

**Features:**
- Validates Joomla manifests
- Checks XML well-formedness
- Runs PHP syntax validation
- Validates CHANGELOG structure
- Checks license headers
- Validates version alignment
- Tab and path separator checks
- Secret scanning

**Usage:**
Copy to your repository as `.github/workflows/ci.yml` and customize as needed.

### repo_health.yml
Repository health and governance validation workflow.

**Features:**
- Admin-only execution gate
- Scripts governance (directory structure validation)
- Repository artifact validation (required files and directories)
- Content heuristics (CHANGELOG, LICENSE, README validation)
- Extended checks:
  - CODEOWNERS presence
  - Workflow pinning advisory
  - Documentation link integrity
  - ShellCheck validation
  - SPDX header compliance
  - Git hygiene (stale branches)

**Profiles:**
- `all` - Run all checks
- `scripts` - Scripts governance only
- `repo` - Repository health only

**Usage:**
Copy to your repository as `.github/workflows/repo_health.yml`. Requires admin permissions to run.

### version_branch.yml
Automated version branching and version bumping workflow.

**Features:**
- Creates `dev/<version>` branches from base branch
- Updates version numbers across all governed files
- Updates manifest dates
- Updates CHANGELOG with version entry
- Enterprise policy gates:
  - Required governance artifacts check
  - Branch namespace collision defense
  - Control character guard
  - Update feed enforcement

**Inputs:**
- `new_version` (required) - Version in format NN.NN.NN (e.g., 03.01.00)
- `version_text` (optional) - Version label (e.g., LTS, RC1, hotfix)
- `report_only` (optional) - Dry run mode without branch creation
- `commit_changes` (optional) - Whether to commit and push changes

**Usage:**
Copy to your repository as `.github/workflows/version_branch.yml`. Run manually via workflow_dispatch.

## Integration with MokoStandards

These workflows are designed to work with:

- **Script templates** in `templates/scripts/`
- **Documentation standards** in `docs/policy/`
- **Repository layout standards** defined in README.md

## Customization

When copying templates to your repository:

1. **Update FILE INFORMATION headers** with correct paths
2. **Adjust branch patterns** to match your branching strategy
3. **Modify validation scripts** based on available scripts in your repository
4. **Customize required artifacts** in repo_health.yml
5. **Update allowed script directories** to match your structure

## Workflow Dependencies

### ci-joomla.yml requires:
- `scripts/validate/manifest.sh`
- `scripts/validate/xml_wellformed.sh`
- Optional validation scripts in `scripts/validate/`

### repo_health.yml requires:
- Python 3.x (for JSON processing)
- ShellCheck (installed automatically if needed)

### version_branch.yml requires:
- Python 3.x (for version bumping logic)
- Governance artifacts: LICENSE, CONTRIBUTING.md, CODE_OF_CONDUCT.md, etc.

## Standards Compliance

All workflows follow MokoStandards requirements:

- SPDX license headers
- GPL-3.0-or-later license
- Proper error handling and reporting
- Step summaries for GitHub Actions UI
- Audit trail generation

## Trigger Patterns

### CI Workflows
- Push to main, dev/**, rc/**, version/** branches
- Pull requests to same branches

### Repo Health
- Manual workflow_dispatch with profile selection
- Push to main (workflows, scripts, docs paths)
- Pull requests (workflows, scripts, docs paths)

### Version Branch
- Manual workflow_dispatch only (admin-level operation)

## Best Practices

1. **Pin action versions** - Use specific versions (@v4) not @main/@master
2. **Test workflows** in development branches before merging to main
3. **Review step summaries** in GitHub Actions UI after runs
4. **Use workflow concurrency** to prevent simultaneous runs
5. **Set appropriate timeouts** for long-running operations

## Support

For issues or questions about these workflows:

1. Review the workflow logs in GitHub Actions UI
2. Check the step summaries for detailed error reports
3. Validate your scripts locally before CI runs
4. Refer to MokoStandards documentation in `docs/`

## Version History

| Version  | Date       | Changes                                      |
| -------- | ---------- | -------------------------------------------- |
| 01.00.00 | 2026-01-04 | Initial workflow templates for MokoStandards |
