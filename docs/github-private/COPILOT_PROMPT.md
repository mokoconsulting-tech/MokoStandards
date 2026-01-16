# .github-private Copilot Setup Prompt

## Overview

This document provides the complete prompt to set up GitHub Copilot for the `.github-private` repository, including context about the repository purpose, file organization, and automated setup process.

---

## Complete Setup Prompt for .github-private Repository

Copy and use this prompt with GitHub Copilot to set up the `.github-private` private repository:

```
I need to set up a new private repository called `.github-private` for the mokoconsulting-tech organization. This repository will store sensitive organizational information that should not be public.

**Context:**
- Organization: mokoconsulting-tech
- Repository name: .github-private
- Visibility: Private (organization members only)
- Purpose: Store sensitive documentation, license management, organization secrets inventory, and internal policies

**Source repository:**
- Public repository: mokoconsulting-tech/MokoStandards
- Contains preparation files in: /docs/github-private/
- Files are ready to be transferred to the new private repository

**What needs to be done:**

1. **Create repository structure** in .github-private with these directories:
   - /docs/internal/ - Internal documentation
   - /docs/policies/ - Policy documents
   - /.github/ISSUE_TEMPLATE/ - Private issue templates
   - /.github/workflows/ - Private workflows
   - /secrets/ - Encrypted secrets storage (with .gitkeep)
   - /licenses/ - License tracking (with .gitkeep)
   - /config/ - Configuration templates

2. **Transfer files from MokoStandards** /docs/github-private/ to appropriate locations:
   - README.md → root
   - LICENSE_MANAGEMENT.md → docs/policies/
   - TEMPLATE_REPO_MIGRATION.md → docs/internal/
   - ENTERPRISE_GITHUB_SETUP.md → docs/internal/
   - SETUP_GITHUB_PRIVATE.md → docs/internal/ (for reference)
   - ISSUE_TEMPLATES.md → docs/internal/

3. **Transfer from MokoStandards** /docs/:
   - EMAIL_DIRECTORY.md → docs/internal/

4. **Move issue template** from MokoStandards:
   - .github/ISSUE_TEMPLATE/request-license.md → .github/ISSUE_TEMPLATE/request-license.md

5. **Create new files** specific to .github-private:
   - .gitignore (protect secrets, license keys, credentials)
   - secrets/SECRETS_INVENTORY.md (organization secrets tracking)
   - secrets/README.md (usage guide)
   - licenses/README.md (license tracking guide)
   - config/github-org-settings.example.json
   - config/repository-defaults.yml

6. **Configure repository settings:**
   - Set visibility to Private
   - Enable GitHub Advanced Security (if available)
   - Configure branch protection for main branch
   - Require pull request reviews (1 approval minimum)
   - Enable secret scanning
   - Restrict access to organization members only
   - Add teams: @mokoconsulting-tech/admins (admin), @mokoconsulting-tech/maintainers (write)

**Key requirements:**
- All sensitive files (.key, .pem, *.secret, *.credentials) must be in .gitignore
- License tracking files must be encrypted or excluded
- Secrets directory must have .gitkeep but exclude actual secret files
- Configuration files should have .example versions that ARE committed
- Issue templates should only include internal/private processes

**Files that should NOT be in .github-private:**
- Public documentation (stays in MokoStandards)
- Open-source code standards (stays in MokoStandards)
- Public issue templates (bug reports, feature requests - stay in MokoStandards)
- Public workflows (stay in MokoStandards)

**After setup, the repository should:**
- Have a clear README explaining the repository purpose
- Contain complete license management documentation
- Include organization secrets inventory template
- Have internal policy documentation
- Provide private issue templates (license requests, etc.)
- Maintain clear separation from public MokoStandards repository

**Automation:**
Execute the setup script from SETUP_GITHUB_PRIVATE.md in MokoStandards which provides:
- Complete bash script to create structure
- File transfer commands
- Initial commit and push
- Post-setup checklist

**Security considerations:**
- Repository must be Private (never public)
- Access restricted to organization members
- Sensitive files protected by .gitignore
- Secrets encrypted at rest
- Audit trail enabled
- Branch protection enforced

Please create the repository structure, transfer all files from MokoStandards/docs/github-private/, set up .gitignore protection, create the secrets inventory, and configure repository settings following enterprise security best practices.
```

---

## Quick Reference: Key Files to Transfer

### From MokoStandards /docs/github-private/:
1. **README.md** (9.2KB) - Main repository documentation
2. **LICENSE_MANAGEMENT.md** (11KB) - License policy and procedures
3. **TEMPLATE_REPO_MIGRATION.md** (19.7KB) - Template repository migration guide
4. **ENTERPRISE_GITHUB_SETUP.md** (15.8KB) - GitHub organization configuration
5. **SETUP_GITHUB_PRIVATE.md** (13KB) - This setup guide (for reference)
6. **ISSUE_TEMPLATES.md** (3.6KB) - Template organization documentation

### From MokoStandards /docs/:
7. **EMAIL_DIRECTORY.md** (11KB) - Organizational email directory

### From MokoStandards /.github/ISSUE_TEMPLATE/:
8. **request-license.md** - License request template (MOVE to .github-private)

---

## Automated Setup Script

The complete automated setup script is available in `SETUP_GITHUB_PRIVATE.md` in the MokoStandards repository. It includes:

### Script Features:
- ✅ Creates complete directory structure
- ✅ Transfers all files from MokoStandards
- ✅ Generates .gitignore with security protections
- ✅ Creates secrets inventory template
- ✅ Sets up license tracking structure
- ✅ Initializes git repository
- ✅ Makes initial commit
- ✅ Pushes to remote

### Script Execution:
```bash
# 1. View the script
cat ~/repos/MokoStandards/docs/github-private/SETUP_GITHUB_PRIVATE.md

# 2. Copy the "Quick Start Prompt" section

# 3. Execute in terminal
# (Takes ~2 minutes)

# 4. Follow post-setup checklist
```

---

## Expected Repository Structure

After setup, .github-private should look like:

```
.github-private/
├── README.md                           # Main repository documentation
├── .gitignore                          # Security protections
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   └── request-license.md          # License request template
│   └── workflows/                      # Private workflows (future)
├── docs/
│   ├── internal/
│   │   ├── EMAIL_DIRECTORY.md          # Organization emails
│   │   ├── ENTERPRISE_GITHUB_SETUP.md  # GitHub org configuration
│   │   ├── TEMPLATE_REPO_MIGRATION.md  # Template migration
│   │   ├── SETUP_GITHUB_PRIVATE.md     # This setup guide
│   │   └── ISSUE_TEMPLATES.md          # Template organization
│   └── policies/
│       └── LICENSE_MANAGEMENT.md       # License policy
├── secrets/
│   ├── .gitkeep                        # Keep directory in git
│   ├── README.md                       # Usage instructions
│   └── SECRETS_INVENTORY.md            # Secrets tracking
├── licenses/
│   ├── .gitkeep                        # Keep directory in git
│   └── README.md                       # License tracking
└── config/
    ├── github-org-settings.example.json
    └── repository-defaults.yml
```

---

## Security Configuration

### .gitignore Protection

The .gitignore MUST include:
```gitignore
# Secrets and sensitive files
secrets/*.key
secrets/*.pem
secrets/*.p12
secrets/*.pfx
secrets/*.env
*.secret
*.credentials

# License keys
licenses/*.txt
licenses/*.key

# Temporary files
*.tmp
*.log

# Keep structure
!secrets/.gitkeep
!licenses/.gitkeep
!config/*.example
```

### Access Control

**Team permissions:**
- @mokoconsulting-tech/admins - Admin access
- @mokoconsulting-tech/maintainers - Write access
- @mokoconsulting-tech/developers - Read access (if needed)

**Repository settings:**
- Visibility: Private
- Base branch: main
- Branch protection: Enabled on main
- Required reviews: 1 approval minimum
- Require status checks
- Require conversation resolution
- Restrict pushes to admins/maintainers

### Security Features

**Enable:**
- ✅ GitHub Advanced Security (if available)
- ✅ Secret scanning
- ✅ Dependency review
- ✅ Code scanning (for scripts)
- ✅ Audit log streaming

**Disable:**
- ❌ Public visibility
- ❌ Fork permissions
- ❌ Wiki (use docs/ instead)
- ❌ Projects (use organization projects)

---

## Integration with MokoStandards

### Bidirectional Sync

**.github-private references MokoStandards:**
- Links to public coding standards
- References public workflows
- Inherits script documentation
- Uses public templates (where appropriate)

**MokoStandards references .github-private:**
- Links to internal policies (for members)
- Directs sensitive issues to private repo
- References email directory (duplicated)
- Points to license management

### Update Workflow

**When MokoStandards updates:**
1. Review changes in /docs/github-private/
2. Manually sync to .github-private repository
3. Update references if needed
4. Commit and push to .github-private

**When .github-private updates:**
1. Internal changes stay private
2. If changes affect public docs, update MokoStandards
3. Maintain separation of public/private concerns

---

## Post-Setup Actions

### Immediate (After Setup)

1. **Verify repository structure**
   ```bash
   cd ~/repos/.github-private
   tree -L 3
   ```

2. **Test issue template**
   - Navigate to: https://github.com/mokoconsulting-tech/.github-private/issues/new/choose
   - Verify "License Request" template appears
   - Test form submission (optional)

3. **Configure team access**
   - Settings → Manage access
   - Add @admins, @maintainers teams
   - Verify permissions

4. **Enable security features**
   - Settings → Security & analysis
   - Enable all available features

5. **Update MokoStandards references**
   - Update links pointing to .github-private
   - Remove /docs/github-private/ files from MokoStandards (after verification)
   - Update issue template references

### Short Term (Week 1)

1. **Populate secrets inventory**
   - Document all organization secrets
   - Add rotation schedules
   - Assign secret owners

2. **Add organization settings**
   - Export current GitHub org settings
   - Add to config/github-org-settings.json
   - Document repository defaults

3. **Create private workflows**
   - License audit workflow
   - Secrets rotation reminders
   - Compliance checks

4. **Train team members**
   - Share .github-private location
   - Explain private issue templates
   - Review license request process

### Ongoing Maintenance

1. **Monthly:**
   - Review secrets inventory
   - Update license tracking
   - Audit access permissions

2. **Quarterly:**
   - Sync updates from MokoStandards
   - Review and update policies
   - Archive old issues

3. **Annually:**
   - Comprehensive security audit
   - Update team access
   - Review all documentation

---

## Support and Contacts

### For .github-private Setup Issues

- **Email**: devops@mokoconsulting.tech (2 hour SLA)
- **Primary contact**: Infrastructure team
- **Escalation**: security@mokoconsulting.tech

### For License Requests

- **Process**: Open issue in .github-private using template
- **Email**: license-admin@mokoconsulting.tech (1 business day SLA)
- **Approval**: Manager + admin review

### For Documentation Updates

- **Email**: dev@mokoconsulting.tech (1 business day SLA)
- **Pull requests**: Welcome from organization members
- **Questions**: Use .github-private issues

---

## Troubleshooting

### Repository Already Exists

```bash
# If .github-private already exists, backup and reset
cd ~/repos/.github-private
git branch backup-$(date +%Y%m%d)
git checkout main
git pull origin main --rebase
# Then run setup script
```

### Permission Denied

```bash
# Ensure you have organization membership and proper access
gh auth status
gh auth login
# Request access from organization admin
```

### Files Not Copying

```bash
# Verify MokoStandards is up to date
cd ~/repos/MokoStandards
git pull origin main

# Check file existence
ls -la docs/github-private/

# Manual copy if needed
cp -v docs/github-private/*.md ~/repos/.github-private/docs/internal/
```

### Setup Script Fails

```bash
# Run commands individually from SETUP_GITHUB_PRIVATE.md
# Check each step output
# Common issues:
# - Repository not created on GitHub first
# - Missing organization permissions
# - Network/authentication issues
```

---

## Version History

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-01-16 | 1.0 | Initial Copilot prompt creation | GitHub Copilot |

---

## Related Documentation

### In MokoStandards (Public)
- `/docs/github-private/SETUP_GITHUB_PRIVATE.md` - Automated setup script
- `/docs/EMAIL_DIRECTORY.md` - Email contacts
- `/docs/development/sublime-text-setup.md` - IDE setup

### In .github-private (After Setup)
- `README.md` - Repository overview
- `docs/policies/LICENSE_MANAGEMENT.md` - License policy
- `docs/internal/ENTERPRISE_GITHUB_SETUP.md` - GitHub configuration

---

**Note**: This prompt is designed to be copied and pasted into GitHub Copilot or used as a reference for manual setup. The automated script in SETUP_GITHUB_PRIVATE.md is the recommended approach for consistency and speed.
