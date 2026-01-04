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
DEFGROUP: MokoStandards
INGROUP: MokoStandards.Documentation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /SECURITY.md
VERSION: 04.01.00
BRIEF: Security vulnerability reporting and handling policy
-->

# Security Policy

## Purpose and Scope

This document defines the security vulnerability reporting, response, and disclosure policy for MokoStandards and all repositories governed by these standards. It establishes the authoritative process for responsible disclosure, assessment, remediation, and communication of security issues.

## Supported Versions

Security updates are provided for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 04.x.x  | :white_check_mark: |
| < 04.0  | :x:                |

Only the current major version receives security updates. Users should upgrade to the latest supported version to receive security patches.

## Reporting a Vulnerability

### Where to Report

**DO NOT** create public GitHub issues for security vulnerabilities.

Report security vulnerabilities privately to:

**Email**: `security@mokoconsulting.tech`

**Subject Line**: `[SECURITY] Brief Description`

### What to Include

A complete vulnerability report should include:

1. **Description**: Clear explanation of the vulnerability
2. **Impact**: Potential security impact and severity assessment
3. **Affected Versions**: Which versions are vulnerable
4. **Reproduction Steps**: Detailed steps to reproduce the issue
5. **Proof of Concept**: Code, configuration, or demonstration (if applicable)
6. **Suggested Fix**: Proposed remediation (if known)
7. **Disclosure Timeline**: Your expectations for public disclosure

### Response Timeline

* **Initial Response**: Within 3 business days
* **Assessment Complete**: Within 7 business days
* **Fix Timeline**: Depends on severity (see below)
* **Disclosure**: Coordinated with reporter

## Severity Classification

Vulnerabilities are classified using the following severity levels:

### Critical
* Remote code execution
* Authentication bypass
* Data breach or exposure of sensitive information
* **Fix Timeline**: 7 days

### High
* Privilege escalation
* SQL injection or command injection
* Cross-site scripting (XSS) with significant impact
* **Fix Timeline**: 14 days

### Medium
* Information disclosure (limited scope)
* Denial of service
* Security misconfigurations with moderate impact
* **Fix Timeline**: 30 days

### Low
* Security best practice violations
* Minor information leaks
* Issues requiring user interaction or complex preconditions
* **Fix Timeline**: 60 days or next release

## Remediation Process

1. **Acknowledgment**: Security team confirms receipt and begins investigation
2. **Assessment**: Vulnerability is validated, severity assigned, and impact analyzed
3. **Development**: Security patch is developed and tested
4. **Review**: Patch undergoes security review and validation
5. **Release**: Fixed version is released with security advisory
6. **Disclosure**: Public disclosure follows coordinated timeline

## Security Advisories

Security advisories are published via:

* GitHub Security Advisories
* Release notes and CHANGELOG.md
* Security mailing list (when established)

Advisories include:

* CVE identifier (if applicable)
* Severity rating
* Affected versions
* Fixed versions
* Mitigation steps
* Attribution (with reporter consent)

## Security Best Practices

For repositories adopting MokoStandards:

### Required Controls

* Enable GitHub security features (Dependabot, code scanning)
* Implement branch protection on `main`
* Require code review for all changes
* Enforce signed commits (recommended)
* Use secrets management (never commit credentials)
* Maintain security documentation
* Follow secure coding standards defined in `/docs/policy/`

### CI/CD Security

* Validate all inputs
* Sanitize outputs
* Use least privilege access
* Pin dependencies with hash verification
* Scan for vulnerabilities in dependencies
* Audit third-party actions and tools

#### Automated Security Scanning

All repositories MUST implement:

**CodeQL Analysis**:
* Enabled for all supported languages (Python, JavaScript, TypeScript, Java, C/C++, C#, Go, Ruby)
* Runs on: push to main, pull requests, weekly schedule
* Query sets: `security-extended` and `security-and-quality`
* Configuration: `.github/workflows/codeql-analysis.yml`

**Dependabot Security Updates**:
* Weekly scans for vulnerable dependencies
* Automated pull requests for security patches
* Configuration: `.github/dependabot.yml`

**Secret Scanning**:
* Enabled by default with push protection
* Prevents accidental credential commits
* Partner patterns enabled

**Dependency Review**:
* Required for all pull requests
* Blocks introduction of known vulnerable dependencies
* Automatic license compliance checking

See [Security Scanning Policy](docs/policy/security-scanning.md) for detailed requirements.

### Dependency Management

* Keep dependencies up to date
* Monitor security advisories for dependencies
* Remove unused dependencies
* Audit new dependencies before adoption
* Document security-critical dependencies

## Compliance and Governance

This security policy is binding for all repositories governed by MokoStandards. Deviations require documented justification and approval from the Security Owner.

Security policies are reviewed and updated at least annually or following significant security incidents.

## Attribution and Recognition

We acknowledge and appreciate responsible disclosure. With your permission, we will:

* Credit you in security advisories
* List you in CHANGELOG.md for the fix release
* Recognize your contribution publicly (if desired)

## Contact and Escalation

* **Security Team**: security@mokoconsulting.tech
* **Primary Contact**: dev@mokoconsulting.tech
* **Escalation**: For urgent matters requiring immediate attention, contact the maintainer directly via GitHub

## Out of Scope

The following are explicitly out of scope:

* Issues in third-party dependencies (report directly to maintainers)
* Social engineering attacks
* Physical security issues
* Denial of service via resource exhaustion without amplification
* Issues requiring physical access to systems
* Theoretical vulnerabilities without proof of exploitability

---

## Metadata

| Field        | Value                                                                                                        |
| ------------ | ------------------------------------------------------------------------------------------------------------ |
| Document     | Security Policy                                                                                              |
| Path         | /SECURITY.md                                                                                                 |
| Repository   | [https://github.com/mokoconsulting-tech/MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards) |
| Owner        | Moko Consulting                                                                                              |
| Scope        | Security vulnerability handling                                                                              |
| Applies To   | All repositories governed by MokoStandards                                                                   |
| Status       | Active                                                                                                       |
| Effective    | 2026-01-04                                                                                                   |

## Revision History

| Date       | Change Description                                | Author          |
| ---------- | ------------------------------------------------- | --------------- |
| 2026-01-04 | Initial creation for enterprise readiness         | Moko Consulting |
