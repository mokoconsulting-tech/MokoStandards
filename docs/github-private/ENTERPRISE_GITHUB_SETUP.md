# Enterprise GitHub Organization Setup Guide

## Overview

This document provides comprehensive setup instructions for configuring Moko Consulting's GitHub organization with enterprise-ready security, compliance, and governance features.

## Prerequisites

- GitHub Enterprise Cloud or GitHub Team plan
- Organization owner access
- Admin access to identity provider (for SSO)

---

## Organization Settings

### Basic Configuration

**Location**: https://github.com/organizations/mokoconsulting-tech/settings/profile

**Settings**:
```yaml
Organization name: Moko Consulting
Display name: Moko Consulting
Email: hello@mokoconsulting.tech
URL: https://mokoconsulting.tech
Location: Global
Description: Enterprise software development and consulting
```

### Member Privileges

**Location**: Settings → Member privileges

**Configuration**:
```yaml
Base permissions: Read
  - Gives all members read access to organization repos
  - Write access granted per-team

Repository creation: 
  - Allow members to create public repositories: ✅
  - Allow members to create private repositories: ✅
  - Allow members to create internal repositories: ✅

Repository forking:
  - Allow forking of private repositories: ✅
  - Allow forking outside organization: ❌

Pages:
  - Allow members to publish sites: ✅ (for documentation)

GitHub Actions:
  - Allow all actions and reusable workflows: ✅
  - Allow organization actions and workflows: ✅
```

### Team Structure

**Recommended teams**:

```
@mokoconsulting-tech/admins
├── Role: Organization owners and administrators
├── Permissions: Admin on all repos
└── Members: Senior engineering leadership

@mokoconsulting-tech/maintainers
├── Role: Repository maintainers and code reviewers
├── Permissions: Maintain on core repos
└── Members: Senior developers, tech leads

@mokoconsulting-tech/developers
├── Role: Active development team
├── Permissions: Write on assigned repos
└── Members: All developers

@mokoconsulting-tech/reviewers
├── Role: Code review and quality assurance
├── Permissions: Triage on all repos
└── Members: QA team, senior developers

@mokoconsulting-tech/readonly
├── Role: Read-only access for stakeholders
├── Permissions: Read on selected repos
└── Members: Managers, product owners, stakeholders
```

**Create teams**:
```bash
gh api orgs/mokoconsulting-tech/teams -f name="admins" -f privacy="closed"
gh api orgs/mokoconsulting-tech/teams -f name="maintainers" -f privacy="closed"
gh api orgs/mokoconsulting-tech/teams -f name="developers" -f privacy="closed"
gh api orgs/mokoconsulting-tech/teams -f name="reviewers" -f privacy="closed"
gh api orgs/mokoconsulting-tech/teams -f name="readonly" -f privacy="closed"
```

---

## Security Configuration

### Security & Analysis

**Location**: Settings → Security & analysis

**Enable all features**:
```yaml
Dependency graph: ✅ Enabled
  - Automatic dependency tracking
  - Vulnerability alerts

Dependabot alerts: ✅ Enabled
  - Automatic security vulnerability detection
  - Email notifications

Dependabot security updates: ✅ Enabled
  - Automatic security patch PRs
  - Version updates for vulnerabilities

Dependabot version updates: ✅ Enabled
  - Automatic dependency updates
  - Configurable via .github/dependabot.yml

GitHub Advanced Security: ✅ Enabled (Enterprise only)
  - Code scanning (CodeQL)
  - Secret scanning
  - Push protection

Code scanning default setup: ✅ Enabled
  - Automatic CodeQL analysis
  - Default for all repos

Secret scanning: ✅ Enabled
  - Detect committed secrets
  - Partner patterns (AWS, Azure, etc.)
  - Custom patterns

Push protection: ✅ Enabled
  - Block pushes with detected secrets
  - Bypass requires admin approval
```

### Authentication & SSO

**For GitHub Enterprise Cloud**:

**Location**: Settings → Authentication security

**SAML SSO Configuration** (if applicable):
```yaml
Identity Provider: Okta / Azure AD / Google Workspace
SSO URL: https://your-idp.com/saml/sso
Entity ID: https://github.com/orgs/mokoconsulting-tech
Certificate: [Upload X.509 certificate]

Options:
  - Require SAML SSO: ✅
  - Enable SCIM provisioning: ✅
  - Require two-factor authentication: ✅
```

**Two-Factor Authentication**:
```yaml
Require two-factor authentication: ✅ Enabled
  - Mandatory for all organization members
  - Grace period: 7 days
  - Email reminders: Enabled
```

### IP Allow List (Optional)

**Location**: Settings → Security → IP allow list

**Configuration** (if using office/VPN IP restrictions):
```yaml
Allow list mode: Enabled

Allowed IPs:
  - Office IP: 203.0.113.0/24
  - VPN Gateway: 198.51.100.0/24
  - CI/CD runners: 192.0.2.0/24

Exemptions:
  - GitHub Actions: ✅ Allow
  - GitHub Apps: ✅ Allow
```

---

## Repository Defaults

### Default Branch Protection

**Apply to all repositories**:

**Settings** → Repositories → Rulesets

**Create ruleset: "Main Branch Protection"**

```yaml
Ruleset name: Main Branch Protection
Enforcement: Active
Targets: All repositories, main/master branches

Rules:
  Require pull request before merging: ✅
    - Required approvals: 1
    - Dismiss stale reviews: ✅
    - Require review from Code Owners: ✅
    - Allow specified actors to bypass: @mokoconsulting-tech/admins
  
  Require status checks to pass: ✅
    - Require branches to be up to date: ✅
    - Status checks:
      - CI / build
      - lint
      - test
      - CodeQL
  
  Require conversation resolution: ✅
  Require signed commits: ❌ (optional)
  Require linear history: ❌
  Block force pushes: ✅
  Block deletions: ✅
  
  Restrict updates: ✅
    - Allowed actors:
      - @mokoconsulting-tech/maintainers
      - @mokoconsulting-tech/admins
```

### Repository Templates

**Create default .github repository**:

```bash
# Create special .github repository
gh repo create mokoconsulting-tech/.github --public \
    --description "Default community health files for all repositories"

cd .github

# Add default files
mkdir -p .github/{ISSUE_TEMPLATE,PULL_REQUEST_TEMPLATE}
mkdir -p workflow-templates

# These files apply to ALL org repos without their own versions
touch CODE_OF_CONDUCT.md
touch CONTRIBUTING.md
touch SECURITY.md
touch SUPPORT.md
```

**Default files structure**:
```
.github/
├── CODE_OF_CONDUCT.md           # Applies to all repos
├── CONTRIBUTING.md               # Contribution guidelines
├── SECURITY.md                   # Security policy
├── SUPPORT.md                    # Support information
├── FUNDING.yml                   # Sponsorship info
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── request-license.md   # NEW: License request template
│   ├── PULL_REQUEST_TEMPLATE/
│   │   └── pull_request_template.md
│   └── dependabot.yml           # Default dependency updates
└── workflow-templates/          # Starter workflows
    ├── ci.yml
    ├── deploy.yml
    └── mokostandards-script-runner.yml
```

---

## GitHub Actions Configuration

### Actions Permissions

**Location**: Settings → Actions → General

**Configuration**:
```yaml
Actions permissions:
  - Allow all actions and reusable workflows: ✅
  
Fork pull request workflows:
  - Require approval for first-time contributors: ✅
  - Require approval for all outside collaborators: ✅
  
Workflow permissions:
  - Read repository contents: ✅
  - Read and write permissions: ❌ (per-workflow basis)
  - Allow GitHub Actions to create and approve pull requests: ❌

Artifact and log retention:
  - Days to keep artifacts and logs: 90 days
```

### Organization Secrets

**Location**: Settings → Secrets and variables → Actions

**Required organization secrets**:

```yaml
# GitHub Integration
GITHUB_ENTERPRISE_TOKEN:
  Description: GitHub PAT with org:read, repo:write
  Visibility: All repositories
  
PRIVATE_REPO_ACCESS_TOKEN:
  Description: Access token for .github-private repo
  Visibility: All repositories

# Sync and Automation
MOKOSTANDARDS_SYNC_TOKEN:
  Description: Token for syncing MokoStandards to org repos
  Visibility: All repositories

# Monitoring and Logging
SIEM_WEBHOOK_URL:
  Description: Webhook URL for security event forwarding
  Visibility: Selected repositories (security-critical only)

# Optional: Tool Licenses (if centrally managed)
SUBLIME_LICENSE_POOL:
  Description: JSON array of Sublime Text license keys
  Visibility: Private repositories only
```

**Create secrets**:
```bash
gh secret set GITHUB_ENTERPRISE_TOKEN \
    --org mokoconsulting-tech \
    --visibility all \
    --body "$TOKEN_VALUE"
```

### Organization Variables

**Location**: Settings → Secrets and variables → Actions → Variables

```yaml
ORGANIZATION_NAME: mokoconsulting-tech
MOKOSTANDARDS_REPO: mokoconsulting-tech/MokoStandards
PRIVATE_REPO: mokoconsulting-tech/.github-private
DEFAULT_BRANCH: main
```

---

## Compliance & Auditing

### Audit Log

**Location**: Settings → Audit log

**Configuration**:
```yaml
Audit log streaming: ✅ Enabled (Enterprise only)
  - Stream to SIEM: Splunk / Datadog / Custom
  - Retention: 180 days in GitHub
  - Extended retention: 7 years in SIEM

Events to monitor:
  - Member additions/removals
  - Team permission changes
  - Repository access changes
  - Secret access
  - Branch protection modifications
  - Organization settings changes
```

**Audit log streaming setup**:
```bash
# Configure audit log streaming (Enterprise Cloud)
gh api /orgs/mokoconsulting-tech/audit-log/streams \
    -X POST \
    -f name="SIEM Integration" \
    -f url="https://siem.mokoconsulting.tech/webhook" \
    -f authorization="Bearer $SIEM_TOKEN"
```

### Compliance Reports

**Automated compliance reporting**:

```yaml
SOC2 Compliance:
  - Access control reports: Monthly
  - Security scanning results: Continuous
  - Dependency audits: Weekly
  - Vulnerability remediation time: Track MTTR

GDPR Compliance:
  - Data access logs: Retained 7 years
  - User data deletion process: Documented
  - Right to access: Automated reports available

ISO 27001:
  - Asset inventory: All repos and secrets tracked
  - Risk assessments: Quarterly
  - Incident response: Documented procedures
```

---

## Webhooks & Integrations

### Organization Webhooks

**Location**: Settings → Webhooks

**Recommended webhooks**:

**1. Audit Log Webhook**
```yaml
Payload URL: https://siem.mokoconsulting.tech/github/audit
Content type: application/json
Secret: [Use strong secret]
Events:
  - Repository events
  - Team events
  - Member events
  - Organization events
```

**2. Security Event Webhook**
```yaml
Payload URL: https://security.mokoconsulting.tech/github/alerts
Events:
  - Security advisory
  - Dependabot alerts
  - Code scanning alerts
  - Secret scanning alerts
```

**3. Deployment Notification**
```yaml
Payload URL: https://monitoring.mokoconsulting.tech/deployments
Events:
  - Deployment
  - Deployment status
  - Release
```

### GitHub Apps

**Recommended installations**:

- **Dependabot** - Automatic dependency updates (built-in)
- **CodeQL** - Security scanning (built-in with Advanced Security)
- **Slack/Teams Integration** - Notifications
- **Datadog/New Relic** - Monitoring integration

---

## Cost Management

### Billing & Plans

**Location**: Settings → Billing and plans

**GitHub Enterprise Cloud Costs**:
```yaml
Base plan: $21/user/month
GitHub Advanced Security: $49/active committer/month
GitHub Copilot: $19/user/month
GitHub Actions minutes: $0.008/minute (after free tier)
GitHub Packages storage: $0.25/GB/month

Free tier:
  - GitHub Actions: 50,000 minutes/month
  - Packages storage: 50GB
  - Git LFS: 100GB
```

**Cost optimization**:
```yaml
Actions minutes:
  - Use self-hosted runners for heavy workloads
  - Cache dependencies
  - Optimize workflows

Packages storage:
  - Regular cleanup of old packages
  - Retention policies

Advanced Security:
  - Only enable for repositories with sensitive code
  - Committer-based billing (not all organization members)
```

---

## Repository Management

### Repository Naming Convention

**Standard format**:
```
[product]-[type]-[name]

Examples:
  mokocrm-module-inventory
  mokowaas-component-booking
  lib-validation-utils
  template-crm-module
```

### Repository Topics

**Required topics** for all repos:
```yaml
All repositories:
  - mokostandards (compliance marker)
  - [primary-language] (python, php, javascript)
  - [project-type] (crm-module, waas-component, library)

Optional topics:
  - dolibarr / joomla (platform)
  - internal / customer (visibility)
  - production / development (status)
```

### Default Repository Settings

**Apply to new repositories**:
```yaml
Features:
  - Issues: ✅
  - Projects: ✅
  - Wiki: ❌ (use docs/ instead)
  - Discussions: ❌ (use issues)

Security:
  - Vulnerability alerts: ✅
  - Automated security fixes: ✅
  - Code scanning: ✅
  - Secret scanning: ✅

Merge options:
  - Allow merge commits: ✅
  - Allow squash merging: ✅
  - Allow rebase merging: ❌
  - Automatically delete head branches: ✅
```

---

## Migration Checklist

### Initial Setup

- [ ] Create GitHub organization
- [ ] Configure basic settings (name, email, URL)
- [ ] Set up teams (@admins, @maintainers, @developers)
- [ ] Configure member privileges
- [ ] Enable two-factor authentication requirement

### Security Configuration

- [ ] Enable GitHub Advanced Security (if Enterprise)
- [ ] Configure Dependabot alerts and updates
- [ ] Enable secret scanning with push protection
- [ ] Set up code scanning default configuration
- [ ] Configure IP allow list (if applicable)
- [ ] Set up SAML SSO (if Enterprise with IdP)

### Repository Management

- [ ] Create .github repository with default files
- [ ] Configure default branch protection rulesets
- [ ] Set repository naming conventions
- [ ] Create template repositories
- [ ] Add sftp-config.json.example to templates

### Actions & Automation

- [ ] Configure Actions permissions
- [ ] Set up organization secrets
- [ ] Create organization variables
- [ ] Configure webhook integrations
- [ ] Set up audit log streaming

### Compliance

- [ ] Document compliance requirements
- [ ] Configure audit log retention
- [ ] Set up compliance reporting
- [ ] Create incident response procedures

### Documentation

- [ ] Complete LICENSE_MANAGEMENT.md
- [ ] Complete ORGANIZATION_SETTINGS.md
- [ ] Create onboarding documentation
- [ ] Document support procedures

---

## Maintenance

### Regular Reviews

**Weekly**:
- Review audit logs for anomalies
- Check security alerts
- Monitor Actions usage and costs

**Monthly**:
- Review team memberships
- Audit repository access
- Update organization secrets approaching expiration
- Cost analysis and optimization

**Quarterly**:
- Comprehensive security audit
- Access control review
- Compliance documentation update
- Update policies and procedures

**Annually**:
- Third-party security audit
- Disaster recovery testing
- Full compliance certification
- Strategic planning

---

## Support & Resources

### Internal Contacts

- **Organization admins**: @mokoconsulting-tech/admins
- **Security team**: security@mokoconsulting.tech
- **DevOps team**: devops@mokoconsulting.tech
- **Compliance**: compliance@mokoconsulting.tech

### External Resources

- GitHub Enterprise Support: https://support.github.com
- GitHub Status: https://www.githubstatus.com
- GitHub Documentation: https://docs.github.com/enterprise-cloud

---

**Document Status**: Implementation Guide  
**Target**: GitHub Organization `mokoconsulting-tech`  
**Last Updated**: 2026-01-16  
**Maintained By**: @mokoconsulting-tech/admins

## Revision History

| Date | Change | Author |
|------|--------|--------|
| 2026-01-16 | Initial enterprise setup guide | GitHub Copilot |
| 2026-01-16 | Added template repository configuration | GitHub Copilot |
| 2026-01-16 | Added license management integration | GitHub Copilot |
