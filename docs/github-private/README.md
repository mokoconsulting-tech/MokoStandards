# .github-private Repository Preparation Guide

## Overview

This directory contains preparation files and documentation that will be transferred to the **separate private repository** `mokoconsulting-tech/.github-private`. 

**Important:** `.github-private` is a standalone private repository, NOT a directory within MokoStandards.

The `.github-private` repository serves as the secure centralization point for proprietary workflows, sensitive automation, and organization-specific configurations.

## Purpose

The `.github-private` repository enables:

- **Secure workflow centralization** - Reusable workflows with organization secrets
- **Proprietary automation** - Internal scripts and tools not suitable for public sharing
- **Enterprise configurations** - Organization-wide settings and policies
- **Sensitive credentials management** - Secure handling of API keys, tokens, and licenses
- **Internal documentation** - Confidential processes and procedures

## Architecture

```
MokoStandards (Public Repo)              .github-private (Private Repo)
├── Standards & Templates           →    ├── Proprietary Implementations
├── Public Documentation            →    ├── Internal Documentation
├── Open Source Scripts             →    ├── Secure Automation Scripts
└── Generic Workflows               →    └── Organization-Specific Workflows

Location: github.com/mokoconsulting-tech/MokoStandards
Access: Public                           Location: github.com/mokoconsulting-tech/.github-private
                                         Access: Organization members only
```

## Files in This Directory

### Preparation Files

| File | Purpose | Target Location in .github-private |
|------|---------|-----------------------------------|
| `README.md` | Integration overview | `/docs/integration/` |
| `ENTERPRISE_GITHUB_SETUP.md` | GitHub Enterprise configuration | `/docs/setup/` |
| `ORGANIZATION_SETTINGS.md` | Organization-level settings | `/docs/setup/` |
| `LICENSE_MANAGEMENT.md` | License key management for tools | `/docs/internal/` |
| `SECRETS_INVENTORY.md` | Required secrets and credentials | `/docs/security/` |
| `TEMPLATE_REPO_MIGRATION.md` | Template repository migration guide | `/docs/migration/` |

## Integration Process

### Phase 1: Repository Setup

1. **Create .github-private repository** (if not exists)
   ```bash
   gh repo create mokoconsulting-tech/.github-private --private \
     --description "Private centralization for workflows and automation" \
     --add-readme
   ```

2. **Initialize structure**
   ```bash
   cd .github-private
   mkdir -p docs/{setup,security,internal,workflows,migration}
   mkdir -p scripts/{setup,automation,validation}
   mkdir -p licenses/{sublime-text,jetbrains,other}
   mkdir -p .github/workflows
   ```

3. **Configure organization secrets**
   - See `SECRETS_INVENTORY.md` for required secrets
   - Configure at: https://github.com/organizations/mokoconsulting-tech/settings/secrets/actions

### Phase 2: Content Migration

1. **Transfer preparation files to .github-private repository**
   ```bash
   # Clone both repositories
   cd ~/repos
   git clone https://github.com/mokoconsulting-tech/MokoStandards.git
   git clone https://github.com/mokoconsulting-tech/.github-private.git
   
   # Copy preparation files from MokoStandards to .github-private
   cp MokoStandards/docs/github-private/*.md .github-private/docs/internal/
   
   cd .github-private
   git add docs/internal/*.md
   git commit -m "Add preparation files from MokoStandards"
   git push
   ```

2. **Migrate template repositories**
   - See `TEMPLATE_REPO_MIGRATION.md` for detailed steps
   - Create standalone template repositories
   - Mark as GitHub template repositories

3. **Migrate sensitive workflows**
   - Move workflows containing organization secrets
   - Update workflow references in organization repositories

4. **Transfer internal scripts**
   - Move scripts containing credentials/tokens
   - Update paths in automation

### Phase 3: Integration & Testing

1. **Test reusable workflows**
   - Verify private workflows are accessible to org repos
   - Test secret propagation

2. **Validate automation**
   - Run validation scripts
   - Check audit logs

3. **Update documentation**
   - Update references in public repo
   - Create internal documentation in private repo

## Enterprise Readiness Features

### GitHub Organization Settings

The preparation includes enterprise-ready configurations for:

- **Security policies** - Branch protection, required reviews, security scanning
- **Access controls** - Team permissions, repository access levels
- **Audit logging** - Comprehensive activity tracking
- **Compliance** - GDPR, SOC2, security standards alignment
- **Template repositories** - Standalone repos marked as templates

### GitHub Enterprise Features

Configurations for GitHub Enterprise Cloud/Server:

- **SAML SSO** - Single sign-on integration
- **IP allowlisting** - Network security
- **Advanced auditing** - Enhanced audit log retention
- **Enterprise managed users** - Centralized identity management
- **GitHub Advanced Security** - CodeQL, secret scanning, dependency review

### License Management

Organization and personal tool licenses:

- **Sublime Text** - Organization pool OR personal purchase option
- **Sublime SFTP** - Personal purchase (recommended, $16 USD)
- **CodeQL** - Included with GitHub Advanced Security
- **GitHub Copilot** - Automatic for organization members

See `LICENSE_MANAGEMENT.md` for full details.

## Required Secrets

The following organization secrets must be configured:

| Secret Name | Purpose | Required By |
|-------------|---------|-------------|
| `MOKOSTANDARDS_SYNC_TOKEN` | Sync public→private content | Sync automation |
| `PRIVATE_REPO_ACCESS_TOKEN` | Access .github-private | All org workflows |
| `GITHUB_ENTERPRISE_TOKEN` | Enterprise API access | Admin automation |
| `SIEM_WEBHOOK_URL` | Security event forwarding | Audit logging |

See `SECRETS_INVENTORY.md` for complete list and setup instructions.

## Security Considerations

### Access Control

- **Repository visibility**: .github-private must remain PRIVATE
- **Template repositories**: Can be public if no sensitive data
- **Team access**: Only grant to necessary teams
- **Secret access**: Limit secret access to specific workflows
- **Audit regularly**: Review access logs monthly

### Sensitive Content Guidelines

Content that should be in `.github-private`:

✅ **Should be private:**
- Internal automation using organization-specific tokens
- Proprietary algorithms or business logic
- Customer/project-specific configurations
- Organization-managed license keys (if applicable)
- Internal team documentation with personal information
- Security configurations and policies

❌ **Should remain public (MokoStandards):**
- Generic coding standards
- Open-source best practices
- Public workflow templates
- Community documentation
- Educational content
- Template repositories (unless contain sensitive data)

## Template Repository Migration

### Overview

Template repositories from `/templates/repos/` will be migrated to standalone GitHub template repositories:

- `mokoconsulting-tech/template-crm-module` (Dolibarr)
- `mokoconsulting-tech/template-waas-component` (Joomla)
- `mokoconsulting-tech/template-generic-project` (Generic)

See `TEMPLATE_REPO_MIGRATION.md` for complete migration guide.

### Benefits of Standalone Templates

- **Direct "Use this template" button** on GitHub
- **Automatic initialization** of new repositories
- **Version tracking** for template updates
- **Independent maintenance** from standards repo
- **Better discoverability** in organization

## Maintenance

### Regular Tasks

- **Weekly**: Review audit logs for anomalies
- **Monthly**: Update secrets approaching expiration
- **Quarterly**: Review and update access controls
- **Annually**: Comprehensive security audit

### Updating Workflows

When updating workflows in .github-private:

1. Test in a sandbox repository first
2. Update version tags in organization repositories
3. Document changes in changelog
4. Notify affected teams

## Support

### For Organization Members

**Access issues**: Contact `@mokoconsulting-tech/admins`

**License requests**: 
- Organization licenses: Open issue using `.github/ISSUE_TEMPLATE/request-license.md`
- Personal licenses: Purchase directly (see LICENSE_MANAGEMENT.md)

**Template repositories**: Use "Use this template" button on template repos

**Documentation**: Internal docs in `.github-private/docs/`

### For Repository Administrators

**Setup assistance**: See `ENTERPRISE_GITHUB_SETUP.md`

**Security incidents**: Follow security policy in `SECURITY.md`

**Audit requirements**: See `ORGANIZATION_SETTINGS.md`

**Template management**: See `TEMPLATE_REPO_MIGRATION.md`

## Related Documentation

- [PRIVATE_REPOSITORY_REFERENCE.md](/docs/PRIVATE_REPOSITORY_REFERENCE.md) - Overview of public/private separation
- [CI_MIGRATION_GUIDE.md](/.github/CI_MIGRATION_GUIDE.md) - CI workflow migration guide
- [Enterprise Readiness Strategy](/docs/ENTERPRISE_READINESS_SCRIPTS.md) - Overall enterprise strategy
- [Sublime Text Setup](/docs/development/sublime-text-setup.md) - IDE configuration guide

## Quick Start Checklist

For administrators setting up .github-private integration:

- [ ] Create .github-private repository
- [ ] Configure organization secrets (see SECRETS_INVENTORY.md)
- [ ] Initialize directory structure
- [ ] Copy preparation files from this directory
- [ ] Migrate template repositories (see TEMPLATE_REPO_MIGRATION.md)
- [ ] Migrate sensitive workflows
- [ ] Update organization repository settings
- [ ] Test reusable workflow access
- [ ] Configure license management (optional)
- [ ] Set up audit logging
- [ ] Update team documentation
- [ ] Notify organization members

---

**Document Status**: Preparation Complete  
**Target Repository**: `mokoconsulting-tech/.github-private`  
**Last Updated**: 2026-01-16  
**Maintained By**: @mokoconsulting-tech/admins
