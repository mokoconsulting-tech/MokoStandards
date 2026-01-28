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
PATH: /docs/policy/dependency-management.md
VERSION: 02.00.00
BRIEF: Dependency management policy for third-party libraries and packages
-->

# Dependency Management Policy

## Purpose

This policy establishes the standards and controls for managing third-party dependencies across all MokoStandards-governed repositories. It defines requirements for dependency selection, updating, security monitoring, and lifecycle management to minimize supply chain risks.

## Scope

This policy applies to:

- All third-party libraries and packages
- All package managers (npm, pip, composer, Maven, Go modules, etc.)
- Direct and transitive dependencies
- Development dependencies and build tools
- GitHub Actions and workflow dependencies

This policy does not apply to:

- Operating system packages managed by infrastructure teams
- Platform-provided runtimes and frameworks
- Internal proprietary libraries (governed separately)

## Responsibilities

### Security Owner

Accountable for:

- Approving dependency management tools and processes
- Reviewing security vulnerabilities in dependencies
- Approving exceptions for vulnerable dependencies
- Escalating critical supply chain risks

### Repository Maintainers

Responsible for:

- Keeping dependencies up to date
- Responding to Dependabot alerts within SLA
- Documenting dependency rationale and selection criteria
- Testing dependency updates before merge
- Removing unused dependencies

### Contributors

Responsible for:

- Following dependency approval process for new packages
- Running security checks before adding dependencies
- Not introducing unnecessary dependencies
- Documenting dependency choices in pull requests

## Dependency Selection Criteria

### Before Adding a New Dependency

All new dependencies MUST be evaluated against:

1. **Necessity**: Is this dependency truly required? Can existing dependencies or standard library accomplish the goal?
2. **Maintenance**: Is the package actively maintained? When was the last release?
3. **Security**: Does the package have known vulnerabilities? What is the security track record?
4. **License**: Is the license compatible with project licensing? (See acceptable licenses below)
5. **Maturity**: Is the package stable and production-ready? What is the version number?
6. **Community**: Is there an active community? How many GitHub stars, downloads, and contributors?
7. **Size**: What is the package size and number of transitive dependencies?
8. **Alternatives**: Have alternative packages been considered? Why is this one preferred?

### Acceptable Licenses

The following license types are pre-approved for dependencies:

**Permissive Licenses** (Preferred):
- MIT
- Apache 2.0
- BSD (2-clause, 3-clause)
- ISC
- CC0 / Public Domain

**Copyleft Licenses** (Allowed with restrictions):
- LGPL (dynamically linked only)
- MPL 2.0

**Prohibited Licenses**:
- GPL (any version) for libraries
- AGPL
- Commercial licenses without legal review
- Licenses with field-of-use restrictions
- Custom/proprietary licenses without approval

Unknown or missing licenses require Security Owner approval.

## Dependency Update Policy

### Automated Updates (Dependabot)

**Configuration**:
- Dependabot MUST be enabled on all repositories
- Updates checked monthly
- Security updates: Immediate pull request creation
- Version updates: Grouped by update type

**Auto-Merge Criteria**:
Patch updates MAY be auto-merged if:
- All CI checks pass
- No breaking changes detected
- Security scanning passes
- Changes reviewed by maintainer within 48 hours

Major and minor updates MUST be manually reviewed.

### Manual Update Cadence

**Security Updates**: Immediate (within SLA per severity)

**Non-Security Updates**:
- Patch updates: Monthly or as available
- Minor updates: Quarterly or with feature releases
- Major updates: Annual or as strategic initiative

### Update Testing Requirements

Before merging dependency updates:

1. **Automated Testing**: All existing tests pass
2. **Build Verification**: Project builds successfully
3. **Security Scanning**: No new vulnerabilities introduced
4. **Functionality Check**: Core features validated
5. **Documentation Review**: Breaking changes documented

### Dependency Pinning

**Requirements**:
- Lock files MUST be committed to version control
- Direct dependencies: Pin to specific versions
- Transitive dependencies: Use lock file resolution
- GitHub Actions: Pin to specific commit SHA or version tag

**Lock Files by Ecosystem**:
- npm: `package-lock.json`
- pip: `requirements.txt` with `==` or `poetry.lock`
- composer: `composer.lock`
- Go: `go.sum`
- Maven: Explicit version numbers in `pom.xml`

## Security Monitoring

### Vulnerability Detection

**Dependabot Alerts**:
- Monitored continuously
- Email notifications to maintainers
- GitHub Security tab tracking
- Integrated with security scanning workflow

**Response SLA**:
- Critical: 24 hours (immediate fix or mitigation)
- High: 7 days
- Medium: 14 days
- Low: 30 days

### Supply Chain Security

**Best Practices**:
- Verify package integrity with checksums
- Use official package registries only
- Avoid dependencies from unverified sources
- Monitor for typosquatting attempts
- Review dependency source code for suspicious packages

**GitHub Actions Security**:
- Pin actions to specific commit SHA: `uses: actions/checkout@a81bbbf8298c0fa03ea29cdc473d45769f953675`
- Avoid third-party actions without security review
- Prefer verified creators and official actions
- Review action source code before use

## Dependency Lifecycle Management

### Adding Dependencies

1. **Proposal**: Document need and evaluation in issue or pull request
2. **Security Check**: Run `npm audit`, `pip-audit`, or equivalent
3. **License Verification**: Confirm compatible license
4. **Review**: Technical review by maintainer
5. **Approval**: Security Owner approval for security-sensitive or large dependencies
6. **Documentation**: Update CHANGELOG and dependency list

### Updating Dependencies

1. **Trigger**: Dependabot alert or scheduled update
2. **Review**: Check release notes and breaking changes
3. **Test**: Run full test suite and manual validation
4. **Security Scan**: Verify no new vulnerabilities
5. **Merge**: After approval and passing checks

### Removing Dependencies

Dependencies SHOULD be removed when:
- No longer used in codebase
- Replaced by alternative solution
- Security vulnerabilities cannot be remediated
- Package abandoned or unmaintained
- License becomes incompatible

**Process**:
1. Remove from package manifest
2. Update lock file
3. Verify build and tests pass
4. Document removal in CHANGELOG
5. Clean up unused code

### Deprecation Handling

When dependencies are deprecated:

1. **Assessment**: Evaluate impact and alternatives
2. **Planning**: Schedule migration to replacement
3. **Testing**: Validate replacement in non-production
4. **Migration**: Update codebase to new dependency
5. **Cleanup**: Remove deprecated dependency
6. **Documentation**: Update docs and examples

## Prohibited Practices

The following are explicitly prohibited:

- Adding dependencies without evaluation
- Ignoring Dependabot security alerts
- Using unvetted or unofficial package sources
- Committing dependencies to version control (except vendored with justification)
- Pinning to outdated versions without security review
- Using `npm audit fix --force` without review
- Bypassing dependency review in pull requests

## Exception Process

Exceptions to dependency management policy require:

1. **Documented Justification**: Why exception is necessary
2. **Risk Assessment**: Security and maintenance risks
3. **Compensating Controls**: How risks are mitigated
4. **Approval**: Security Owner and project maintainer
5. **Expiration**: Time-bound with renewal requirement
6. **Documentation**: Recorded in EXCEPTIONS.md file

## Metrics and Reporting

### Tracked Metrics
- Number of dependencies (direct vs transitive)
- Percentage of dependencies with known vulnerabilities
- Average age of dependencies
- Dependabot alert response time
- Dependency update frequency
- License compliance percentage

### Reporting
- Monthly: Dependency health dashboard
- Quarterly: Supply chain risk report
- Annually: Dependency audit and cleanup

## Tools and Automation

### Required Tools

**Dependabot**:
- Automated security and version updates
- Configuration in `.github/dependabot.yml`

**Dependency Review Action**:
- Pull request dependency impact analysis
- Blocks vulnerable dependencies in PRs

**Package Manager Security**:
- `npm audit` for Node.js
- `pip-audit` for Python
- `composer audit` for PHP
- Language-specific security tools

### Recommended Tools

- **Renovate**: Advanced dependency update automation
- **Snyk**: Comprehensive vulnerability scanning
- **WhiteSource/Mend**: License compliance and security
- **Dependabot Grouped Updates**: Batch related updates

## Compliance and Audit

### Evidence Requirements
- Dependency manifest and lock files in version control
- Dependabot configuration committed
- Security scan results for each release
- Exception approvals documented
- Dependency update history in pull requests

### Audit Checklist
- [ ] All dependencies have compatible licenses
- [ ] No critical vulnerabilities in dependencies
- [ ] Lock files committed and up to date
- [ ] Dependabot enabled and configured
- [ ] Dependencies updated within policy timelines
- [ ] Unused dependencies removed
- [ ] Exceptions properly documented and approved

## Dependencies

This policy depends on:

- [Security Scanning Policy](security-scanning.md) - Vulnerability detection
- [Change Management Policy](change-management.md) - Update approval process
- [Vendor Risk Policy](vendor-risk.md) - Third-party assessment
- GitHub Dependabot configuration
- Repository security settings

## Acceptance Criteria

- [ ] Dependabot enabled with monthly scans
- [ ] Dependency review action required for PRs
- [ ] All dependencies evaluated per selection criteria
- [ ] No dependencies with incompatible licenses
- [ ] No unresolved critical vulnerabilities older than 24 hours
- [ ] Lock files committed for all package managers
- [ ] Dependency documentation up to date

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Policy                                       |
| Domain         | Governance                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/policy/dependency-management.md                                      |
| Version        | 02.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 02.00.00 with all required fields |
