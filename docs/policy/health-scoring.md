[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Repository Health Scoring System

**Status**: Active | **Version**: 01.00.00 | **Effective**: 2026-01-07

## Overview

The MokoStandards Health Scoring System provides an objective 100-point assessment of repository quality, compliance, and operational readiness. This scoring system is used to evaluate all repositories in the Moko Consulting organization and track improvement over time.

## Score Calculation

The health score is calculated across 8 categories with a maximum possible score of 100 points:

| Category | Points | Description |
|---|---|---|
| CI/CD Status | 15 | Continuous integration and deployment health |
| Required Documentation | 16 | Core documentation files presence and quality |
| Required Folders | 10 | Standard directory structure compliance |
| Workflows | 12 | GitHub Actions workflow completeness |
| Issue Templates | 5 | Issue and PR template availability |
| Security | 15 | Security scanning and vulnerability management |
| Repository Settings | 10 | GitHub repository configuration compliance |
| Deployment Secrets | 20 | Deployment configuration and secrets management |

**Total Maximum Score**: 103 points

## Score Levels

Repositories are categorized into four health levels based on their total score:

| Level | Score Range | Indicator | Status |
|---|---|---|---|
| **Excellent** | 90-100% | ✅ | Production-ready, fully compliant |
| **Good** | 70-89% | ⚠️ | Minor improvements needed |
| **Fair** | 50-69% | 🟡 | Significant improvements required |
| **Poor** | 0-49% | ❌ | Critical issues, requires immediate attention |

## Detailed Scoring Criteria

### 1. CI/CD Status (15 points)

**Maximum**: 15 points

| Criteria | Points | Requirements |
|---|---|---|
| CI workflow present and enabled | 5 | `.github/workflows/ci.yml` exists and runs |
| CI workflow passing on main branch | 5 | Latest CI run successful |
| CI runs on all PRs | 3 | Configured for pull_request trigger |
| CI workflow up-to-date | 2 | Uses current MokoStandards template version |

**Automated Check**: Workflow status API query
**Manual Override**: N/A
**Remediation**: Add CI workflow from MokoStandards templates

### 2. Required Documentation (16 points)

**Maximum**: 16 points

| File | Points | Requirements |
|---|---|---|
| README.md | 3 | Present, >500 chars, contains project description |
| LICENSE | 3 | Present, contains GPL-3.0-or-later text |
| CONTRIBUTING.md | 2 | Present, contains contribution guidelines |
| SECURITY.md | 2 | Present, contains security policy |
| CHANGELOG.md | 3 | Present, follows Keep a Changelog format |
| .editorconfig | 2 | Present, defines coding style rules |
| .gitignore patterns | 1 | Contains *.sublime* and sftp-config*.json patterns |

**Automated Check**: File presence and content validation
**Manual Override**: Exceptional projects may substitute equivalent documentation
**Remediation**: Copy templates from `templates/docs/required/` or run `scripts/update_gitignore_patterns.sh`

### 3. Required Folders (10 points)

**Maximum**: 10 points

| Directory | Points | Requirements |
|---|---|---|
| docs/ | 3 | Present, contains project documentation |
| tests/ | 3 | Present, contains automated tests |
| scripts/ | 2 | Present, contains automation scripts |
| .github/ | 2 | Present, contains GitHub-specific files |

**Automated Check**: Directory existence
**Manual Override**: N/A for .github/, flexible for others based on project type
**Remediation**: Create directories per repository structure standards

### 4. Workflows (12 points)

**Maximum**: 12 points

| Workflow | Points | Requirements |
|---|---|---|
| CI workflow | 3 | `.github/workflows/ci.yml` present |
| CodeQL analysis | 3 | `.github/workflows/codeql-analysis.yml` present |
| Repo health | 2 | `.github/workflows/repo_health.yml` present |
| Platform-specific workflow | 2 | Joomla/Dolibarr-specific workflow if applicable |
| Flush Actions Cache workflow | 2 | `.github/workflows/flush-actions-cache.yml` present |

**Automated Check**: Workflow file presence and syntax validation
**Manual Override**: Equivalent workflows may substitute
**Remediation**: Copy workflows from MokoStandards `templates/workflows/`

### 5. Issue Templates (5 points)

**Maximum**: 5 points

| Template | Points | Requirements |
|---|---|---|
| Bug report template | 2 | `.github/ISSUE_TEMPLATE/bug_report.md` present |
| Feature request template | 2 | `.github/ISSUE_TEMPLATE/feature_request.md` present |
| Pull request template | 1 | `.github/pull_request_template.md` present |

**Automated Check**: Template file presence
**Manual Override**: N/A
**Remediation**: Copy templates from `templates/github/`

### 6. Security (15 points)

**Maximum**: 15 points

| Feature | Points | Requirements |
|---|---|---|
| Dependabot enabled | 5 | `.github/dependabot.yml` configured |
| Dependabot alerts enabled | 3 | Repository setting enabled |
| Secret scanning enabled | 3 | Repository setting enabled |
| CodeQL analysis running | 4 | Weekly scans completing successfully |

**Automated Check**: GitHub API queries for security features
**Manual Override**: N/A
**Remediation**: Enable in repository settings, add Dependabot config

### 7. Repository Settings (10 points)

**Maximum**: 10 points

| Setting | Points | Requirements |
|---|---|---|
| Branch protection on main | 3 | Require PR reviews, status checks |
| Require signed commits | 2 | GPG signature verification enabled |
| Delete head branches | 1 | Automatic branch deletion after merge |
| No direct push to main | 2 | Branch protection enforced |
| Squash merge enabled | 1 | Squash commits option available |
| Topics/tags configured | 1 | At least 3 relevant repository topics |

**Automated Check**: GitHub API repository settings query
**Manual Override**: Admin override for specific project requirements
**Remediation**: Configure in repository settings

### 8. Deployment Secrets (20 points)

**Maximum**: 20 points

For repositories with deployment workflows (web applications, extensions):

**Secret Configuration Levels**:
- **Organization-Level Secrets** (⭐ Preferred): `FTP_HOST`, `FTP_USERNAME`, `FTP_PASSWORD`, `FTP_PATH`, and `FTP_PORT` are configured at the organization level and automatically inherited by all repositories.
- **Repository-Level**: `FTP_PATH_SUFFIX` is repository-specific. `FTP_KEY` may be repository-specific if needed.

| Secret/Variable | Points | Requirements | Configuration Level |
|---|---|---|---|
| FTP_HOST | 3 | Configured and accessible | **Organization** (inherited) |
| FTP_USERNAME | 3 | Configured and accessible | **Organization** (inherited) |
| FTP_PASSWORD or FTP_KEY | 4 | Authentication method configured | **Organization** (inherited) |
| FTP_PATH | 3 | Base deployment path configured | **Organization** (inherited) |
| FTP_PORT | 3 | Port configured (default: 22) | **Organization** (inherited) |
| FTP_PATH_SUFFIX | 2 | Optional path suffix configured in variables | Repository (if needed) |
| SFTP connectivity validated | 2 | Repo health workflow verifies connection | Tested automatically |

**Important Notes**:
- Organization-level secrets (`FTP_HOST`, `FTP_USERNAME`, `FTP_PASSWORD`, `FTP_PATH`, `FTP_PORT`) count toward the score even though they're not configured in the repository itself - they're inherited automatically.
- Repositories automatically receive 16 points (out of 20) for organization secrets if they're accessible.
- Only repository-specific configuration (`FTP_PATH_SUFFIX`) needs to be set at the repository level.
- The remaining 4 points come from optional path suffix and connectivity validation.

**For non-deployment repositories**, this category awards points based on appropriate alternatives (e.g., package registry credentials, cloud provider keys).

**Automated Check**: Secret accessibility check (via workflow), connectivity test
**Manual Override**: N/A
**Remediation**:
- Organization secrets: Contact organization administrators (no repository action needed)
- Repository secrets: Configure in repository settings → Secrets and variables → Actions
- Run repo health workflow to verify configuration

## Score Calculation Example

**Example Repository**: JoomlaExtension

| Category | Max | Earned | Notes |
|---|---|---|---|
| CI/CD Status | 15 | 13 | CI present and passing, using older template |
| Required Documentation | 16 | 13 | Missing SECURITY.md and .gitignore patterns |
| Required Folders | 10 | 10 | All required folders present |
| Workflows | 10 | 8 | Missing repo_health workflow |
| Issue Templates | 5 | 5 | All templates present |
| Security | 15 | 11 | Dependabot not configured |
| Repository Settings | 10 | 8 | Signed commits not required |
| Deployment Secrets | 20 | 20 | All secrets properly configured |
| **TOTAL** | **101** | **88** | **Good (⚠️)** |

## Health Score Monitoring

### Automated Reporting

Health scores are calculated and reported through:

1. **Scheduled Workflow** - Runs weekly on all repositories
2. **On-Demand Checks** - Via workflow_dispatch
3. **PR Comments** - Scores included in PR summaries
4. **Organization Dashboard** - Aggregate view of all repository scores

### Score Tracking

Historical scores are tracked to measure improvement:
- Weekly snapshots stored in repository
- Trend analysis available in organization dashboard
- Alerts for score degradation >10 points

## Improvement Roadmap

Repositories scoring below "Good" (70%) should follow this improvement plan:

### Priority 1 (Critical - Week 1)
1. Add missing CI workflow
2. Create required documentation files
3. Enable Dependabot and secret scanning
4. Configure branch protection

### Priority 2 (High - Week 2)
5. Add required directories
6. Create issue templates
7. Configure deployment secrets (if applicable)
8. Add CodeQL workflow

### Priority 3 (Standard - Week 3)
9. Add repo health workflow
10. Configure remaining repository settings
11. Update CI workflow to latest template
12. Improve documentation quality

## Exemptions and Overrides

Certain repositories may receive exemptions:

### Automatic Exemptions

- **Archive repositories** - Scored but not penalized
- **Template repositories** - Different scoring criteria
- **Fork repositories** - May inherit parent scores

### Manual Exemptions

Repository owners can request exemptions for specific criteria through:
1. Adding `.github/health-exemptions.yml`
2. Documenting rationale
3. Admin approval required

Example exemption file:
```yaml
exemptions:
  - category: deployment_secrets
    reason: "Static documentation site, no deployment needed"
    approved_by: admin-user
    approved_date: 2026-01-07
```

## Integration with Workflows

Health scoring is integrated with existing workflows:

### repo_health.yml Workflow

The repository health workflow contributes to scoring:
- Validates required artifacts
- Tests SFTP connectivity (deployment category)
- Checks repository configuration
- Reports findings to dashboard

### CI Workflow

Contributes to CI/CD Status category:
- Success/failure status
- Presence and configuration
- Run frequency

### Security Workflows

Contribute to Security category:
- CodeQL analysis results
- Dependabot alert counts
- Secret scanning findings

## API Access

Health scores are available via API:

```bash
# Get score for specific repository
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/mokoconsulting-tech/REPO/properties/health-score

# Get all repository scores (requires org admin)
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/orgs/mokoconsulting-tech/properties/repository-health
```

## Best Practices for Maintaining High Scores

1. **Regular Updates** - Keep workflows and templates current
2. **Documentation First** - Write docs before code
3. **Security by Default** - Enable all security features
4. **Automation** - Use workflows for consistency
5. **Monitor Trends** - Track scores weekly
6. **Address Alerts** - Fix Dependabot alerts promptly
7. **Test Before Merge** - CI must pass
8. **Follow Standards** - Adhere to MokoStandards templates

## Frequently Asked Questions

**Q: How often are scores updated?**
A: Scores are recalculated weekly and on-demand via workflow dispatch.

**Q: Can I improve my score without making code changes?**
A: Yes! Many criteria involve configuration and documentation only.

**Q: What happens if my score drops below 50%?**
A: Automatic alerts are sent to repository owners and organization admins.

**Q: Are scores public?**
A: Scores are visible to organization members only by default.

**Q: How do I request an exemption?**
A: Create `.github/health-exemptions.yml` and request admin approval.

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Policy                                       |
| Domain         | Governance                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/policy/health-scoring.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Version History

| Version | Date | Changes |
|---|---|---|
| 01.00.00 | 2026-01-07 | Initial health scoring system documentation |

## See Also

- [Workflow Templates](workflows/README.md)
- [SFTP Deployment Guide](deployment/sftp.md)
- [Project Type Detection](../reference/project-types.md)
- [Repository Structure Standards](guide/repository-structure-schema.md)

## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
