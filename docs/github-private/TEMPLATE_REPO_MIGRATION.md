# Template Repository Migration Guide

## Overview

This document outlines the process for migrating template directories from `MokoStandards/templates/repos/` to standalone GitHub template repositories.

## Why Migrate to Standalone Template Repositories?

### Current State (Before Migration)

Templates live in `/templates/repos/` within MokoStandards:
- `templates/repos/crm/` - Dolibarr CRM module template
- `templates/repos/waas/` - Joomla WaaS component template  
- `templates/repos/generic/` - Generic project template

**Limitations:**
- ❌ Users must manually copy/paste template files
- ❌ No "Use this template" button on GitHub
- ❌ Templates not versioned independently
- ❌ Difficult to discover
- ❌ No automatic new repo initialization

### Target State (After Migration)

Standalone GitHub template repositories:
- `mokoconsulting-tech/template-crm-module`
- `mokoconsulting-tech/template-waas-component`
- `mokoconsulting-tech/template-generic-project`

**Benefits:**
- ✅ Click "Use this template" button to create new repo
- ✅ Automatic initialization with all template files
- ✅ Independent versioning and releases
- ✅ Better discoverability in organization
- ✅ GitHub automatically marks as template
- ✅ Included in GitHub's template search

---

## Template Repositories to Create

### 1. template-crm-module (Dolibarr)

**Purpose**: Dolibarr/MokoCRM module development

**Source**: `templates/repos/crm/`

**Target Repo**: `mokoconsulting-tech/template-crm-module`

**Structure**:
```
template-crm-module/
├── .gitignore                    # Dolibarr-specific patterns
├── .editorconfig                 # Code style config
├── sftp-config.json.example      # Sublime Text SFTP template
├── README.md                     # Module documentation template
├── LICENSE                       # GPL-3.0-or-later
├── CHANGELOG.md                  # Version history template
├── SECURITY.md                   # Security policy
├── CODE_OF_CONDUCT.md            # Community standards
├── CONTRIBUTING.md               # Contribution guidelines
├── src/                          # Deployment code
│   ├── core/                     # Module core logic
│   ├── langs/                    # Language files
│   └── sql/                      # Database scripts
├── docs/                         # Technical documentation
├── tests/                        # Unit tests
├── scripts/                      # Build and deployment scripts
│   └── .mokostandards-sync.yml   # Sync override config
└── .github/
    └── workflows/                # CI/CD workflows
        ├── ci.yml
        └── deploy.yml
```

**Key Files**:
- `.gitignore` from `templates/configs/.gitignore.dolibarr`
- `sftp-config.json.example` - NEW, SFTP configuration template
- Schema reference: `schemas/structures/crm-module.xml`

### 2. template-waas-component (Joomla)

**Purpose**: Joomla/MokoWaaS component development

**Source**: `templates/repos/waas/`

**Target Repo**: `mokoconsulting-tech/template-waas-component`

**Structure**:
```
template-waas-component/
├── .gitignore                    # Joomla-specific patterns
├── .editorconfig                 # Code style config
├── sftp-config.json.example      # Sublime Text SFTP template
├── README.md                     # Component documentation template
├── LICENSE                       # GPL-3.0-or-later
├── CHANGELOG.md                  # Version history template
├── SECURITY.md                   # Security policy
├── CODE_OF_CONDUCT.md            # Community standards
├── CONTRIBUTING.md               # Contribution guidelines
├── site/                         # Frontend (public) code
│   ├── controllers/
│   ├── models/
│   ├── views/
│   └── tmpl/                     # Templates
├── admin/                        # Backend (admin) code
│   ├── controllers/
│   ├── models/
│   ├── views/
│   ├── sql/                      # Database schemas
│   └── config.xml                # Component configuration
├── media/                        # CSS, JS, images
│   ├── css/
│   ├── js/
│   └── images/
├── language/                     # Translation files
│   ├── en-GB/
│   └── [other locales]/
├── tests/                        # Unit and integration tests
├── scripts/                      # Build scripts
│   └── .mokostandards-sync.yml   # Sync override config
└── .github/
    └── workflows/                # CI/CD workflows
```

**Key Files**:
- `.gitignore` from `templates/configs/.gitignore.joomla`
- `sftp-config.json.example` - NEW, SFTP configuration template
- Schema reference: `schemas/structures/waas-component.xml`

### 3. template-generic-project

**Purpose**: Generic projects, libraries, and applications

**Source**: `templates/repos/generic/`

**Target Repo**: `mokoconsulting-tech/template-generic-project`

**Structure**:
```
template-generic-project/
├── .gitignore                    # Generic patterns
├── .editorconfig                 # Code style config
├── sftp-config.json.example      # Sublime Text SFTP template (optional)
├── README.md                     # Project documentation template
├── LICENSE                       # GPL-3.0-or-later
├── CHANGELOG.md                  # Version history template
├── SECURITY.md                   # Security policy
├── CODE_OF_CONDUCT.md            # Community standards
├── CONTRIBUTING.md               # Contribution guidelines
├── src/                          # Source code
├── docs/                         # Documentation
├── tests/                        # Tests
├── scripts/                      # Utility scripts
│   └── .mokostandards-sync.yml   # Sync override config
└── .github/
    └── workflows/                # CI/CD workflows
        ├── ci.yml
        └── release.yml
```

**Key Files**:
- `.gitignore` from `templates/configs/.gitignore.generic`
- `sftp-config.json.example` - NEW, SFTP configuration template (optional)
- Schema reference: `schemas/structures/generic-repository.xml`

---

## SFTP Configuration Template (NEW REQUIREMENT)

### sftp-config.json.example

**All template repositories must include** an `sftp-config.json.example` file for Sublime Text SFTP plugin configuration.

**Location**: Root of each template repository

**Purpose**: 
- Provide pre-configured SFTP settings template
- Document required configuration fields
- Enable immediate remote development setup

**Template Content**:

```json
{
    "_comment": "Sublime Text SFTP Configuration Template",
    "_instructions": [
        "1. Copy this file to sftp-config.json",
        "2. Update host, user, and remote_path with your server details",
        "3. Configure authentication (ssh_key_file or password)",
        "4. Ensure sftp-config.json is in .gitignore (security!)",
        "5. See docs/development/sublime-text-setup.md for full guide"
    ],
    
    "type": "sftp",
    "save_before_upload": true,
    "upload_on_save": true,
    "sync_down_on_open": true,
    "sync_skip_deletes": true,
    "sync_same_age": true,
    "confirm_downloads": false,
    "confirm_sync": true,
    "confirm_overwrite_newer": true,
    
    "host": "dev.example.com",
    "user": "your-username",
    "port": "22",
    
    "remote_path": "/var/www/html/your-project",
    
    "ssh_key_file": "~/.ssh/id_rsa",
    "_ssh_key_file_comment": "Recommended: Use SSH key authentication",
    
    "_password": "YOUR_PASSWORD_HERE",
    "_password_comment": "NOT RECOMMENDED: Only use for testing, never commit",
    
    "ignore_regexes": [
        "\\.sublime-(project|workspace)",
        "sftp-config(-alt\\d?)?\\.json",
        "sftp-settings\\.json",
        "/venv/",
        "\\.git/",
        "\\.gitignore",
        "\\.editorconfig",
        "/node_modules/",
        "/vendor/",
        "__pycache__/",
        "\\.pyc$",
        "\\.log$",
        "\\.cache/",
        "/dist/",
        "/build/",
        "\\.DS_Store"
    ],
    
    "always-overwrite": false,
    "_always_overwrite_comment": "Set to false to prevent accidental overwrites",
    
    "file_permissions": "664",
    "dir_permissions": "775",
    
    "extra_list_connections": 0,
    
    "connect_timeout": 30,
    "keepalive": 120,
    "ftp_passive_mode": true,
    "ftp_obey_passive_host": false,
    "ssh_key_file_passphrase": "",
    
    "_platform_specific_paths": {
        "_comment": "Adjust paths based on platform",
        "dolibarr": "/var/www/html/dolibarr/htdocs/custom/your-module",
        "joomla": "/var/www/html/joomla/components/com_yourcomponent",
        "generic": "/var/www/html/your-project"
    }
}
```

**Platform-Specific Variations**:

**For Dolibarr (CRM) templates**:
```json
{
    "remote_path": "/var/www/html/dolibarr/htdocs/custom/[module-name]",
    "ignore_regexes": [
        "...existing patterns...",
        "/documents/",
        "/conf/conf.php"
    ]
}
```

**For Joomla (WaaS) templates**:
```json
{
    "remote_path": "/var/www/html/joomla/administrator/components/com_[component-name]",
    "ignore_regexes": [
        "...existing patterns...",
        "/configuration.php",
        "/images/",
        "/cache/"
    ]
}
```

**For Generic templates**:
```json
{
    "remote_path": "/var/www/html/[project-name]",
    "_comment": "Adjust based on your project type and server setup"
}
```

### Security Requirements

**Critical: SFTP config security**

1. **sftp-config.json MUST be in .gitignore**
   ```gitignore
   # Sublime Text SFTP
   sftp-config.json
   sftp-config-alt*.json
   ```

2. **Only commit sftp-config.json.example**
   - Never commit actual credentials
   - Example file should have placeholder values
   - Document clearly it's a template

3. **Documentation reference**
   - Include comment pointing to full setup guide
   - Link to `/docs/development/sublime-text-setup.md`

---

## Migration Process

### Phase 1: Preparation

**1. Create SFTP configuration templates**

```bash
# For each template directory
cd MokoStandards/templates/repos/crm
cat > sftp-config.json.example << 'EOF'
{
    "_comment": "Dolibarr CRM Module SFTP Configuration Template",
    "type": "sftp",
    "remote_path": "/var/www/html/dolibarr/htdocs/custom/[module-name]",
    ...
}
EOF

# Repeat for waas and generic
```

**2. Update .gitignore templates**

Ensure all platform-specific .gitignore files include:
```gitignore
# Sublime Text SFTP configuration (contains credentials)
sftp-config.json
sftp-config-alt*.json
```

**3. Validate template structure**

```bash
# Verify each template has required files
for template in crm waas generic; do
    echo "Checking templates/repos/$template/"
    required_files=(
        ".gitignore"
        ".editorconfig"
        "sftp-config.json.example"
        "README.md"
        "LICENSE"
        "CHANGELOG.md"
        "SECURITY.md"
        "CODE_OF_CONDUCT.md"
        "CONTRIBUTING.md"
        "scripts/.mokostandards-sync.yml"
    )
    for file in "${required_files[@]}"; do
        if [ ! -f "templates/repos/$template/$file" ]; then
            echo "  ❌ Missing: $file"
        else
            echo "  ✅ Present: $file"
        fi
    done
done
```

### Phase 2: Create Template Repositories

**For each template:**

**Step 1: Create GitHub repository**

```bash
# Create CRM module template
gh repo create mokoconsulting-tech/template-crm-module \
    --public \
    --description "Dolibarr CRM module template for MokoStandards-compliant development" \
    --add-readme

# Create WaaS component template
gh repo create mokoconsulting-tech/template-waas-component \
    --public \
    --description "Joomla component template for MokoStandards-compliant WaaS development" \
    --add-readme

# Create generic project template
gh repo create mokoconsulting-tech/template-generic-project \
    --public \
    --description "Generic project template following MokoStandards conventions" \
    --add-readme
```

**Step 2: Clone and populate**

```bash
# Clone new template repo
git clone https://github.com/mokoconsulting-tech/template-crm-module.git
cd template-crm-module

# Copy template files from MokoStandards
cp -r ../MokoStandards/templates/repos/crm/* .

# Ensure SFTP template is present
ls -la sftp-config.json.example

# Initialize git
git add .
git commit -m "Initial template structure with SFTP configuration"
git push origin main
```

**Step 3: Mark as template repository**

```bash
# Via GitHub CLI
gh repo edit mokoconsulting-tech/template-crm-module --enable-template

# Or via GitHub web UI:
# 1. Go to repository settings
# 2. Check "Template repository" under "Template repository"
# 3. Save changes
```

**Step 4: Add topics for discoverability**

```bash
gh repo edit mokoconsulting-tech/template-crm-module \
    --add-topic mokostandards \
    --add-topic dolibarr \
    --add-topic crm-module \
    --add-topic template \
    --add-topic php

gh repo edit mokoconsulting-tech/template-waas-component \
    --add-topic mokostandards \
    --add-topic joomla \
    --add-topic waas \
    --add-topic template \
    --add-topic php

gh repo edit mokoconsulting-tech/template-generic-project \
    --add-topic mokostandards \
    --add-topic template \
    --add-topic generic \
    --add-topic starter
```

**Step 5: Configure repository settings**

```bash
# Enable features
gh repo edit mokoconsulting-tech/template-crm-module \
    --enable-issues \
    --enable-projects \
    --enable-wiki

# Set default branch protections
gh api repos/mokoconsulting-tech/template-crm-module/branches/main/protection \
    -X PUT \
    --input <(cat <<EOF
{
  "required_status_checks": null,
  "enforce_admins": false,
  "required_pull_request_reviews": null,
  "restrictions": null
}
EOF
)
```

### Phase 3: Update MokoStandards

**1. Update documentation**

Update references in MokoStandards to point to new template repositories:

```markdown
# In docs/quickstart/new-project.md

## Using Template Repositories

### Dolibarr CRM Module
1. Go to https://github.com/mokoconsulting-tech/template-crm-module
2. Click "Use this template"
3. Name your repository
4. Clone and start developing

### Joomla WaaS Component
1. Go to https://github.com/mokoconsulting-tech/template-waas-component
2. Click "Use this template"
...
```

**2. Update README.md**

```markdown
# Template Repositories

MokoStandards provides ready-to-use template repositories:

- [template-crm-module](https://github.com/mokoconsulting-tech/template-crm-module) - Dolibarr CRM modules
- [template-waas-component](https://github.com/mokoconsulting-tech/template-waas-component) - Joomla WaaS components
- [template-generic-project](https://github.com/mokoconsulting-tech/template-generic-project) - Generic projects

Click "Use this template" to create a new repository with all standard files and structure.
```

**3. Keep templates/repos/ for reference (optional)**

```bash
# Option 1: Keep for backward compatibility
# Add note to templates/repos/README.md

# Option 2: Remove after migration
git rm -r templates/repos/crm
git rm -r templates/repos/waas
git rm -r templates/repos/generic

# Add redirect README
cat > templates/repos/README.md << 'EOF'
# Template Repositories Migrated

Template directories have been migrated to standalone GitHub template repositories.

Use these instead:
- https://github.com/mokoconsulting-tech/template-crm-module
- https://github.com/mokoconsulting-tech/template-waas-component
- https://github.com/mokoconsulting-tech/template-generic-project

See: docs/github-private/TEMPLATE_REPO_MIGRATION.md
EOF
```

### Phase 4: Testing

**Test template repository functionality:**

1. **Test "Use this template" button**
   ```bash
   # As a test user, click "Use this template" on each repo
   # Verify new repo created with all files
   ```

2. **Test SFTP configuration**
   ```bash
   # In new repo created from template
   cp sftp-config.json.example sftp-config.json
   # Update with test server credentials
   # Test sync with Sublime Text
   ```

3. **Test automation**
   ```bash
   # Verify CI/CD workflows run in new repo
   # Check MokoStandards sync works
   ```

4. **Test documentation links**
   ```bash
   # Verify all links in template README work
   # Check SFTP setup guide is accessible
   ```

---

## Post-Migration Tasks

### 1. Update Organization Documentation

- [ ] Update quickstart guides to reference template repos
- [ ] Update training materials
- [ ] Update onboarding documentation
- [ ] Notify teams of new template repo URLs

### 2. Deprecation Notice

Add notice to MokoStandards templates/repos/:

```markdown
# ⚠️ DEPRECATED: Use Template Repositories Instead

Template directories in this location are deprecated.

**New location:** Standalone GitHub template repositories

### Migration Guide

| Old Location | New Template Repository |
|--------------|------------------------|
| `templates/repos/crm/` | [template-crm-module](https://github.com/mokoconsulting-tech/template-crm-module) |
| `templates/repos/waas/` | [template-waas-component](https://github.com/mokoconsulting-tech/template-waas-component) |
| `templates/repos/generic/` | [template-generic-project](https://github.com/mokoconsulting-tech/template-generic-project) |

**How to use:**
1. Visit template repository URL
2. Click "Use this template" button
3. Name your new repository
4. Clone and start developing

See: [Template Repository Migration Guide](docs/github-private/TEMPLATE_REPO_MIGRATION.md)
```

### 3. Update Automation Scripts

Update scripts that reference template paths:

- `scripts/automation/create_repo_project.py`
- `scripts/automation/bulk_update_repos.py`
- Any CI/CD workflows referencing templates

### 4. Monitor Usage

Track adoption of new template repositories:

```bash
# Query GitHub API for template usage
gh api graphql -f query='
{
  repository(owner: "mokoconsulting-tech", name: "template-crm-module") {
    templateRepository
    usedAsTemplate {
      totalCount
    }
  }
}'
```

---

## Maintenance

### Updating Template Repositories

**When to update:**
- MokoStandards updates
- New best practices
- Security patches
- Feature additions

**Update process:**

1. **Test changes locally**
2. **Create update branch in template repo**
3. **Test with "Use this template"**
4. **Merge to main**
5. **Create release tag**
6. **Notify organization**

### Version Tagging

```bash
# Create release for template updates
cd template-crm-module
git tag -a v1.1.0 -m "Update to MokoStandards 5.1.0, add SFTP template"
git push origin v1.1.0

# Create GitHub release
gh release create v1.1.0 \
    --title "Template Update v1.1.0" \
    --notes "Updated to MokoStandards 5.1.0 conventions, added SFTP configuration template"
```

---

## Success Criteria

Migration is complete when:

- [ ] All 3 template repositories created and marked as templates
- [ ] SFTP configuration template included in all repos
- [ ] "Use this template" button functional
- [ ] All template files present and correct
- [ ] Documentation updated with new URLs
- [ ] Deprecation notice added to old locations
- [ ] Team notified of changes
- [ ] At least 1 successful test repo created from each template
- [ ] SFTP setup tested successfully
- [ ] All links validated

---

**Document Status**: Implementation Guide  
**Target Repositories**: 
- `mokoconsulting-tech/template-crm-module`
- `mokoconsulting-tech/template-waas-component`
- `mokoconsulting-tech/template-generic-project`

**Last Updated**: 2026-01-16  
**Maintained By**: @mokoconsulting-tech/admins

## Revision History

| Date | Change | Author |
|------|--------|--------|
| 2026-01-16 | Initial migration guide created | GitHub Copilot |
| 2026-01-16 | Added SFTP configuration template requirement | GitHub Copilot |
| 2026-01-16 | Added detailed SFTP template structure | GitHub Copilot |
