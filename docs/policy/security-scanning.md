<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

# FILE INFORMATION
DEFGROUP: MokoStandards.Policy
INGROUP: MokoStandards.Security
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/policy/security-scanning.md
VERSION: 04.00.01
BRIEF: Security scanning policy and automated vulnerability detection standards
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.01-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Security Scanning Policy

## Purpose

This policy establishes mandatory security scanning requirements for all repositories governed by MokoStandards. It defines the tools, processes, and response procedures for automated vulnerability detection, code analysis, and security compliance validation.

## Scope

This policy applies to:

- All source code repositories under MokoStandards governance
- All programming languages and frameworks in use
- Third-party dependencies and libraries
- GitHub Actions workflows and CI/CD pipelines
- Infrastructure as code and configuration files

This policy does not apply to:

- Repositories explicitly exempted by Security Owner
- Archived or read-only repositories
- Forks used solely for upstream contribution

## Responsibilities

### Security Owner

Accountable for:

- Defining security scanning standards
- Approving security tools and configurations
- Reviewing critical and high-severity findings
- Approving exceptions and risk acceptances
- Escalating unresolved vulnerabilities

### Repository Maintainers

Responsible for:

- Enabling required security scanning tools
- Responding to security alerts within SLA
- Fixing vulnerabilities per severity timeline
- Documenting risk acceptances with justification
- Maintaining up-to-date scanning configurations

### Contributors

Responsible for:

- Not introducing new vulnerabilities
- Running local security checks before committing
- Addressing security findings in pull requests
- Following secure coding practices

## Required Security Scanning Tools

### CodeQL Analysis (Mandatory)

**Purpose**: Static application security testing (SAST) for code vulnerabilities

**Configuration**:
- Must be enabled on all repositories with supported languages
- Runs on: push to main, pull requests, weekly schedule
- Languages supported: Python, JavaScript, TypeScript, Java, C/C++, C#, Go, Ruby
- Query sets: `security-extended` and `security-and-quality`
- **Language configuration must match repository contents**: Only languages with actual source files should be configured to avoid analysis failures

**Implementation**:
```yaml
# .github/workflows/codeql-analysis.yml
name: "CodeQL Security Scanning"
on:
  push:
    branches: [main, dev/**, rc/**]
  pull_request:
    branches: [main, dev/**, rc/**]
  schedule:
    - cron: '0 6 * * 1'  # Weekly Monday 6 AM UTC

jobs:
  analyze:
    strategy:
      matrix:
        # IMPORTANT: Only list languages that exist in your repository
        # Configuring non-existent languages will cause CI failures
        language: [ 'python' ]  # Adjust based on your actual codebase
```

**Language Configuration Validation**:

To prevent CI failures from misconfigured languages, validate your CodeQL configuration:

```bash
# Download and run the validation script
curl -sSL https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/scripts/validate/validate_codeql_config.py -o validate_codeql_config.py
python3 validate_codeql_config.py
```

The validation script will:
- Detect programming languages present in your repository
- Compare against configured CodeQL languages
- Report errors for configured languages with no source files
- Report warnings for detected languages not being scanned

**Common Configuration Errors**:
- ❌ **Incorrect**: Copying template with `['python', 'javascript', 'php']` when only Python exists
- ✅ **Correct**: Configure only `['python']` for Python-only repositories
- ✅ **Correct**: Configure `['python', 'javascript']` for repos with both languages

**Response Requirements**:
- Critical: Fix within 7 days
- High: Fix within 14 days
- Medium: Fix within 30 days
- Low: Fix within 60 days or next release

### Dependabot Security Updates (Mandatory)

**Purpose**: Automated dependency vulnerability detection and patching

**Configuration**:
- Must be enabled on all repositories
- Monitors: GitHub Actions, Python packages, npm packages, and ecosystem-specific dependencies
- Frequency: Weekly scans on Monday at 9:00 AM
- Auto-merge: Patch updates may be auto-merged after CI passes

**Implementation**:
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

**Response Requirements**:
- Critical vulnerabilities: Immediate patch or mitigation
- High vulnerabilities: Within 7 days
- Medium vulnerabilities: Within 14 days
- Low vulnerabilities: Within 30 days

### Secret Scanning (Mandatory)

**Purpose**: Prevent accidental commit of credentials and sensitive data

**Configuration**:
- Enabled by default on all repositories
- Scans for: API keys, tokens, passwords, certificates
- Push protection: Enabled to block commits with secrets
- Partner patterns: Enabled for third-party service detection

**Response Requirements**:
- Immediately revoke exposed credentials
- Rotate compromised secrets within 1 hour
- Update affected systems and services
- Document incident in security log

### Dependency Review (Required for PRs)

**Purpose**: Prevent introduction of vulnerable dependencies in pull requests

**Configuration**:
- Required status check for all pull requests
- Blocks merges that introduce known vulnerabilities
- Reviews license compatibility
- Flags deprecated or unmaintained packages

**Implementation**:
```yaml
# .github/workflows/dependency-review.yml
name: "Dependency Review"
on: [pull_request]
```

## Prohibited Practices

The following are explicitly prohibited:

- Disabling security scanning without Security Owner approval
- Ignoring or dismissing security alerts without documentation
- Committing secrets or credentials to version control
- Bypassing security checks in CI/CD pipelines
- Using deprecated or unmaintained dependencies without justification
- Disabling push protection for secret scanning

## Exception Process

Exceptions to security scanning requirements require:

1. **Written Justification**: Document why the exception is necessary
2. **Risk Assessment**: Quantify security impact and compensating controls
3. **Security Owner Approval**: Explicit approval in writing
4. **Expiration Date**: Exceptions expire and require renewal
5. **Regular Review**: Reassessed quarterly or after security incidents

**Exception Request Template**:
```markdown
## Security Scanning Exception Request

**Repository**: [repo name]
**Tool**: [CodeQL/Dependabot/Secret Scanning]
**Justification**: [why exception is needed]
**Risk Assessment**: [impact analysis]
**Compensating Controls**: [alternative protections]
**Requested Duration**: [expiration date]
**Approver**: [Security Owner name]
```

## Vulnerability Response Process

### Detection
- Automated alerts via GitHub Security tab
- Email notifications to repository maintainers
- Slack/Teams integration for critical findings

### Triage
1. Review alert details and affected code
2. Verify vulnerability is exploitable in context
3. Assign severity based on CVSS score and business impact
4. Determine if fix, mitigation, or risk acceptance is appropriate

### Remediation
1. Apply vendor-provided patches when available
2. Update dependencies to non-vulnerable versions
3. Implement code fixes for application vulnerabilities
4. Add compensating controls if immediate fix not possible
5. Document changes in pull request

### Verification
1. Confirm vulnerability is resolved
2. Re-run security scans to validate fix
3. Close security alert with resolution notes
4. Update documentation if process changes required

### Communication
- Critical/High: Notify Security Owner immediately
- Medium: Weekly security review meeting
- Low: Monthly security summary report

## Metrics and Reporting

### Required Metrics
- Open security alerts by severity
- Mean time to remediate (MTTR) by severity
- Percentage of automated vs manual fixes
- Number of exceptions granted
- Dependency update lag time

### Reporting Frequency
- Weekly: Critical and high-severity summary
- Monthly: Comprehensive security dashboard
- Quarterly: Trend analysis and policy review

## Integration with CI/CD

### Pull Request Requirements
All pull requests MUST:
- Pass CodeQL analysis (if language supported)
- Pass dependency review (no new vulnerable dependencies)
- Pass secret scanning (no exposed credentials)
- Have security findings addressed before merge

### Branch Protection
Main branch protection MUST include:
- Required status check: CodeQL (if applicable)
- Required status check: Dependency Review
- No bypassing for administrators on security checks

## Compliance and Audit

### Evidence Requirements
- Security scan results for each release
- Vulnerability remediation timeline
- Exception approvals and justifications
- Security incident response records

### Audit Trail
- All security alerts logged with timestamps
- All dismissals documented with rationale
- All exceptions recorded with approval chain
- All remediations linked to pull requests

## Dependencies

This policy depends on:

- [Security Policy](../../SECURITY.md) - Overall security framework
- [Change Management Policy](change-management.md) - Change approval process
- [Dependency Management Policy](dependency-management.md) - Dependency standards
- GitHub Security features enabled on repository

## Acceptance Criteria

- [ ] CodeQL enabled on all applicable repositories
- [ ] Dependabot configured with monthly scans
- [ ] Secret scanning with push protection enabled
- [ ] Dependency review required for all PRs
- [ ] Security alerts triaged within SLA
- [ ] Vulnerabilities remediated per timeline
- [ ] Metrics collected and reported monthly
- [ ] No unacknowledged critical alerts older than 7 days

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Policy                                       |
| Domain         | Governance                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/policy/security-scanning.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
