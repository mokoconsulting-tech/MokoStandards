# .github-private Repository Setup Guide

## Quick Start Prompt

Use this prompt to quickly set up the `.github-private` repository and pull files from MokoStandards:

```bash
# === .github-private Repository Setup ===
# Execute these commands to initialize and configure the .github-private repository

# 1. Create the repository on GitHub (if not exists)
# Navigate to: https://github.com/organizations/mokoconsulting-tech/repositories/new
# Repository name: .github-private
# Visibility: Private
# DO NOT initialize with README (we'll pull from MokoStandards)

# 2. Clone both repositories
cd ~/repos
git clone https://github.com/mokoconsulting-tech/MokoStandards.git
git clone https://github.com/mokoconsulting-tech/.github-private.git

# 3. Set up .github-private repository structure
cd .github-private
git checkout -b main 2>/dev/null || git checkout main

# Create directory structure
mkdir -p docs/internal
mkdir -p docs/policies
mkdir -p .github/workflows
mkdir -p .github/ISSUE_TEMPLATE
mkdir -p secrets
mkdir -p config

# 4. Copy files from MokoStandards
cd ~/repos
cp MokoStandards/docs/github-private/README.md .github-private/README.md
cp MokoStandards/docs/github-private/LICENSE_MANAGEMENT.md .github-private/docs/policies/
cp MokoStandards/docs/github-private/TEMPLATE_REPO_MIGRATION.md .github-private/docs/internal/
cp MokoStandards/docs/github-private/ENTERPRISE_GITHUB_SETUP.md .github-private/docs/internal/
cp MokoStandards/docs/EMAIL_DIRECTORY.md .github-private/docs/internal/

# 5. Copy license request template
cp MokoStandards/.github/ISSUE_TEMPLATE/request-license.md .github-private/.github/ISSUE_TEMPLATE/

# 6. Create .github-private specific files
cd .github-private

# Create .gitignore
cat > .gitignore << 'EOF'
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
.DS_Store
Thumbs.db

# IDE files
.vscode/
.idea/
*.sublime-project
*.sublime-workspace

# Keep templates
!secrets/.gitkeep
!licenses/.gitkeep
!config/*.example
EOF

# Create secrets/.gitkeep
touch secrets/.gitkeep
echo "# Store encrypted secrets here" > secrets/README.md

# Create licenses/.gitkeep
touch licenses/.gitkeep
echo "# License tracking files (encrypted)" > licenses/README.md

# 7. Create organization secrets inventory
cat > secrets/SECRETS_INVENTORY.md << 'EOF'
# Organization Secrets Inventory

## GitHub Organization Secrets

Last updated: $(date +%Y-%m-%d)

### Required Secrets

| Secret Name | Purpose | Access Level | Rotation Schedule |
|-------------|---------|--------------|-------------------|
| GH_PAT | GitHub API automation | Organization | 90 days |
| GH_TOKEN | CI/CD workflows | Organization | Never (GitHub managed) |
| DOCKER_USERNAME | Container registry | Organization | Manual |
| DOCKER_PASSWORD | Container registry | Organization | 90 days |
| CODECOV_TOKEN | Code coverage | Organization | Annual |

### Repository-Specific Secrets

| Repository | Secret Name | Purpose | Rotation |
|------------|-------------|---------|----------|
| MokoWaaS | JOOMLA_DB_PASSWORD | Database access | 90 days |
| MokoCRM | DOLIBARR_DB_PASSWORD | Database access | 90 days |

### Secret Management

- **Storage**: GitHub Secrets (encrypted at rest)
- **Access**: Organization admins only
- **Rotation**: Automated via workflows where possible
- **Audit**: All access logged in GitHub audit log

### Adding New Secrets

1. Document in this inventory
2. Add to GitHub Organization Secrets
3. Update affected repositories
4. Test in non-production first
5. Update documentation

### Emergency Procedures

**Compromised Secret**:
1. Immediately rotate in GitHub
2. Notify security@mokoconsulting.tech
3. Review audit logs
4. Update all dependent systems
5. Document in incident log

## Encrypted Files

Sensitive files stored in `secrets/` directory are encrypted using:
- GPG with organization key
- 1Password for team sharing
- GitHub encrypted secrets for automation

**Never commit unencrypted secrets to this repository.**
EOF

# 8. Create config templates
cat > config/github-org-settings.example.json << 'EOF'
{
  "organization": "mokoconsulting-tech",
  "settings": {
    "two_factor_requirement": true,
    "members_can_create_repositories": false,
    "members_can_create_public_repositories": false,
    "members_can_fork_private_repositories": false,
    "default_repository_permission": "read",
    "members_can_create_pages": false
  },
  "security": {
    "advanced_security_enabled": true,
    "secret_scanning_enabled": true,
    "dependabot_enabled": true,
    "code_scanning_default_setup": "enabled"
  },
  "teams": {
    "admins": {
      "permission": "admin",
      "members": []
    },
    "maintainers": {
      "permission": "maintain",
      "members": []
    },
    "developers": {
      "permission": "write",
      "members": []
    }
  }
}
EOF

cat > config/repository-defaults.yml << 'EOF'
# Default settings for new repositories
default_branch: main

branch_protection:
  main:
    required_reviews: 1
    dismiss_stale_reviews: true
    require_code_owner_reviews: true
    required_status_checks:
      - "build"
      - "test"
      - "codeql"
    enforce_admins: false
    allow_force_pushes: false
    allow_deletions: false

security:
  enable_vulnerability_alerts: true
  enable_automated_security_fixes: true
  secret_scanning: true
  push_protection: true

features:
  wikis: false
  projects: true
  issues: true
  discussions: false

merge_settings:
  allow_merge_commit: true
  allow_squash_merge: true
  allow_rebase_merge: false
  delete_branch_on_merge: true
EOF

# 9. Create initial commit
git add .
git commit -m "Initial .github-private repository setup

- Imported documentation from MokoStandards
- Created secrets inventory
- Added configuration templates
- Set up directory structure
- Added license request template"

# 10. Push to GitHub
git push -u origin main

# 11. Configure repository settings via GitHub web UI
echo ""
echo "=== Manual Configuration Required ==="
echo ""
echo "1. Go to: https://github.com/mokoconsulting-tech/.github-private/settings"
echo ""
echo "2. General Settings:"
echo "   - Visibility: Private (verify)"
echo "   - Disable: Wikis, Projects (if not needed)"
echo "   - Enable: Issues, Discussions (optional)"
echo ""
echo "3. Collaborators and Teams:"
echo "   - Add @mokoconsulting-tech/admins (Admin)"
echo "   - Add @mokoconsulting-tech/maintainers (Write)"
echo "   - Review: Who has access?"
echo ""
echo "4. Branches:"
echo "   - Default branch: main"
echo "   - Branch protection: Require PR reviews (1 approval)"
echo "   - Status checks: None required (internal repo)"
echo ""
echo "5. Secrets and Variables:"
echo "   - Review organization secrets access"
echo "   - Add repository-specific secrets if needed"
echo ""
echo "6. GitHub Advanced Security:"
echo "   - Enable: Secret scanning"
echo "   - Enable: Push protection"
echo "   - Dependabot: Enable for dependencies"
echo ""
echo "=== Setup Complete ==="
echo ""
echo "Repository URL: https://github.com/mokoconsulting-tech/.github-private"
echo "Documentation: See README.md for usage"
echo ""
```

## What This Does

### Repository Structure Created
```
.github-private/
├── .gitignore                          # Protects sensitive files
├── README.md                           # Overview and integration guide
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   └── request-license.md          # License request template
│   └── workflows/                      # Future: automation workflows
├── docs/
│   ├── internal/                       # Internal documentation
│   │   ├── TEMPLATE_REPO_MIGRATION.md
│   │   ├── ENTERPRISE_GITHUB_SETUP.md
│   │   └── EMAIL_DIRECTORY.md
│   └── policies/                       # Organization policies
│       └── LICENSE_MANAGEMENT.md
├── secrets/
│   ├── README.md                       # Secret storage guidelines
│   ├── SECRETS_INVENTORY.md            # Complete secrets inventory
│   └── .gitkeep
├── licenses/
│   ├── README.md                       # License tracking
│   └── .gitkeep
└── config/
    ├── github-org-settings.example.json
    └── repository-defaults.yml
```

### Files Imported from MokoStandards
- ✅ LICENSE_MANAGEMENT.md - License policy and procedures
- ✅ TEMPLATE_REPO_MIGRATION.md - Template repository migration plan
- ✅ ENTERPRISE_GITHUB_SETUP.md - GitHub Enterprise configuration
- ✅ EMAIL_DIRECTORY.md - Organization email contacts
- ✅ request-license.md - License request issue template

### New Files Created
- ✅ SECRETS_INVENTORY.md - Organization secrets tracking
- ✅ .gitignore - Protects sensitive files
- ✅ github-org-settings.example.json - Organization settings template
- ✅ repository-defaults.yml - Default repository configuration

## After Setup

### Update MokoStandards References

In MokoStandards repository, update references to point to .github-private:

```bash
cd ~/repos/MokoStandards

# Update README.md
sed -i 's|/docs/github-private/LICENSE_MANAGEMENT.md|https://github.com/mokoconsulting-tech/.github-private/blob/main/docs/policies/LICENSE_MANAGEMENT.md|g' README.md
sed -i 's|/docs/github-private/|https://github.com/mokoconsulting-tech/.github-private/blob/main/docs/internal/|g' docs/**/*.md

# Update Sublime Text setup guide
sed -i 's|/docs/github-private/LICENSE_MANAGEMENT.md|https://github.com/mokoconsulting-tech/.github-private/blob/main/docs/policies/LICENSE_MANAGEMENT.md|g' docs/development/sublime-text-setup.md

# Commit updates
git add -A
git commit -m "Update references to .github-private repository"
git push
```

### Remove Migrated Files from MokoStandards

After verifying .github-private is set up correctly:

```bash
cd ~/repos/MokoStandards

# Remove the github-private documentation directory
git rm -r docs/github-private/

# Remove the license request template (now in .github-private)
git rm .github/ISSUE_TEMPLATE/request-license.md

# Commit removal
git commit -m "Remove files migrated to .github-private repository"
git push
```

## Syncing Future Updates

### Pull Updates from MokoStandards

When MokoStandards updates files that should be in .github-private:

```bash
cd ~/repos
cd MokoStandards && git pull
cd ../.github-private

# Copy updated files
cp ../MokoStandards/docs/development/sublime-text-setup.md docs/internal/ 2>/dev/null || true
# Add other files as needed

git add docs/
git commit -m "Sync updates from MokoStandards"
git push
```

### Automated Sync (Future Enhancement)

Create `.github/workflows/sync-from-mokostandards.yml` in .github-private:

```yaml
name: Sync from MokoStandards

on:
  workflow_dispatch:
  schedule:
    - cron: '0 0 * * 1'  # Weekly on Monday

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout .github-private
        uses: actions/checkout@v4
        with:
          path: private
          
      - name: Checkout MokoStandards
        uses: actions/checkout@v4
        with:
          repository: mokoconsulting-tech/MokoStandards
          path: standards
          
      - name: Sync files
        run: |
          # Copy relevant files (customize as needed)
          cp standards/docs/EMAIL_DIRECTORY.md private/docs/internal/ || true
          
      - name: Commit changes
        run: |
          cd private
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add .
          git diff --quiet && git diff --staged --quiet || \
            git commit -m "Sync updates from MokoStandards [automated]"
          git push
```

## Security Considerations

### Access Control
- **Private repository**: Only organization members
- **Admin access**: Organization admins only
- **Write access**: Maintainers team
- **Read access**: All organization members (optional)

### Sensitive Data
- **Never commit**: Unencrypted passwords, API keys, private keys
- **Use GitHub Secrets**: For automation secrets
- **Use GPG encryption**: For stored secrets in repo
- **Use 1Password**: For team password sharing

### Audit Trail
- All changes tracked in git history
- GitHub audit log for access
- Issue tracking for license requests

## Troubleshooting

### Repository Already Exists

If .github-private already exists:

```bash
cd ~/repos/.github-private
git pull
# Then copy files selectively instead of creating from scratch
```

### Permission Denied

Ensure you have admin access to the organization:
```bash
gh auth status
gh api orgs/mokoconsulting-tech/memberships/$(gh api user -q .login)
```

### Files Not Copying

Check file paths:
```bash
ls -la ~/repos/MokoStandards/docs/github-private/
ls -la ~/repos/MokoStandards/.github/ISSUE_TEMPLATE/
```

## Next Steps

After setup is complete:

1. ✅ Verify all files imported correctly
2. ✅ Configure GitHub repository settings
3. ✅ Add team access
4. ✅ Test license request workflow
5. ✅ Update MokoStandards references
6. ✅ Remove migrated files from MokoStandards
7. ✅ Document in organization wiki
8. ✅ Train team on new process

## Support

For issues with setup:
- Technical: dev@mokoconsulting.tech
- Access: devops@mokoconsulting.tech
- General: hello@mokoconsulting.tech
