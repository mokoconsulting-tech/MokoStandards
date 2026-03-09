#!/usr/bin/env bash
# create-doc-gap-issues.sh
# Creates all 39 documentation gap issues for mokoconsulting-tech/MokoStandards
# Run with: bash create-doc-gap-issues.sh
# Requires: gh CLI authenticated with issues:write scope
# Usage: GH_TOKEN=<your-token> bash create-doc-gap-issues.sh

set -euo pipefail
REPO="mokoconsulting-tech/MokoStandards"
LABEL="documentation"

create_issue() {
  local title="$1"
  local body="$2"
  echo "Creating: $title"
  number=$(gh issue create --repo "$REPO" --label "$LABEL" --title "$title" --body "$body" | grep -oP 'issues/\K[0-9]+')
  echo "  → Issue #$number"
}

# ============================================================
# BATCH 1 — Missing Files Referenced in Code
# ============================================================

create_issue \
  "[Doc Gap] Create docs/guide/architecture.md — system architecture overview" \
  '## Documentation Gap: Missing Referenced File

**Path:** `docs/guide/architecture.md`
**Gap Type:** Missing reference — cited in `api/validate/check_enterprise_readiness.php` but the file does not exist.
**Priority:** 🔴 High

### Why This Matters
The enterprise readiness checker explicitly validates that an architecture document exists. Without it, every repository fails this check. Enterprise governance requires a documented system architecture to communicate design decisions to new contributors and auditors.

### Suggested Sections
- [ ] System Overview — purpose, scope, stakeholders
- [ ] Component Architecture — diagram and description of major components (API, Enterprise libs, definitions, templates, workflows)
- [ ] Data Flow — how repositories are synced, validated, and governed
- [ ] Technology Stack — PHP 8.1+, Composer, GitHub Actions, Terraform HCL
- [ ] Integration Points — GitHub API, bulk sync, platform definitions
- [ ] Repository Taxonomy — standards, waas-component, crm-module, generic types

### Acceptance Criteria
- [ ] File created at `docs/guide/architecture.md`
- [ ] Includes standard Markdown copyright / FILE INFORMATION header
- [ ] `check_enterprise_readiness.php` passes the architecture check
- [ ] `docs/guide/index.md` updated to list the new document'

create_issue \
  "[Doc Gap] Create docs/policy/security.md — top-level security policy overview" \
  '## Documentation Gap: Missing Referenced File

**Path:** `docs/policy/security.md`
**Gap Type:** Missing reference — cited in validation scripts but the file does not exist.
**Priority:** 🔴 High

### Why This Matters
The `docs/policy/security/` subdirectory contains nine individual security policies, but there is no top-level `security.md` that serves as an executive summary and navigation hub. Without it, readers have no entry point into the security policy framework, and any cross-reference from code or other documents leads to a 404.

### Suggested Sections
- [ ] Security Principles — CIA triad, least privilege, defence-in-depth
- [ ] Scope — systems, repositories, personnel, third parties in scope
- [ ] Responsibilities — security owner, developers, operations
- [ ] Policy Index — links to all nine subdirectory policies with one-line descriptions
- [ ] Compliance Requirements — relevant regulations and frameworks (GDPR, SOC 2-readiness)
- [ ] Review Cycle — how and when these policies are reviewed

### Acceptance Criteria
- [ ] File created at `docs/policy/security.md`
- [ ] Includes standard copyright / FILE INFORMATION header
- [ ] All nine `docs/policy/security/*.md` documents are cross-referenced
- [ ] `docs/policy/index.md` updated'

create_issue \
  "[Doc Gap] Create docs/policy/file-formatting.md — file formatting policy" \
  '## Documentation Gap: Missing Referenced File

**Path:** `docs/policy/file-formatting.md`
**Gap Type:** Missing reference — cited in `.github/workflows/standards-compliance.yml` comment but the file does not exist.
**Priority:** 🔴 High

### Why This Matters
The standards-compliance workflow references this policy as the authority for file formatting rules. Developers and AI coding agents need a single canonical document explaining encoding, line endings, whitespace, and file naming requirements. Currently only `.editorconfig` and scattered comments provide this information.

### Suggested Sections
- [ ] Encoding — UTF-8, no BOM
- [ ] Line Endings — LF (Unix-style), not CRLF
- [ ] Indentation Rules — tabs for PHP/Bash/PowerShell, 2-space YAML, 4-space Python (reference .editorconfig)
- [ ] Maximum Line Length — 120 chars hard limit, 150 hard-stop for PHP
- [ ] File Naming Conventions — kebab-case for docs, snake_case for PHP scripts
- [ ] File Structure — copyright header first, then content
- [ ] Trailing Whitespace and EOF Newline requirements

### Acceptance Criteria
- [ ] File created at `docs/policy/file-formatting.md`
- [ ] Consistent with `.editorconfig` rules
- [ ] Cross-referenced from `docs/policy/coding-style-guide.md`
- [ ] `docs/policy/index.md` updated'

# ============================================================
# BATCH 2 — Empty Legal Directory
# ============================================================

create_issue \
  "[Doc Gap] Create docs/policy/legal/acceptable-use-policy.md" \
  '## Documentation Gap: Empty Section — Legal Directory

**Path:** `docs/policy/legal/acceptable-use-policy.md`
**Gap Type:** The `docs/policy/legal/` directory exists but contains only an auto-generated `index.md`. No legal policies have been written.
**Priority:** 🔴 High

### Why This Matters
An Acceptable Use Policy (AUP) is a foundational legal document required in any enterprise governance framework. It defines what employees and contractors may and may not do with organizational systems, tools, GitHub repositories, AI coding assistants, and cloud infrastructure.

### Suggested Sections
- [ ] Purpose and Scope
- [ ] Acceptable Use — authorized activities on Moko Consulting systems and repositories
- [ ] Prohibited Activities — data exfiltration, unauthorized access, use of non-approved AI tools, etc.
- [ ] System Access — GitHub org access, SSH keys, personal access tokens
- [ ] AI Tool Usage — governed by `docs/policy/ai-tool-governance.md`, summarize here
- [ ] Monitoring Notice — systems may be monitored
- [ ] Violations and Consequences
- [ ] Reporting Violations

### Acceptance Criteria
- [ ] File created at `docs/policy/legal/acceptable-use-policy.md`
- [ ] Reviewed by or coordinated with appropriate legal/management stakeholder
- [ ] Cross-referenced from `docs/policy/legal/index.md`'

create_issue \
  "[Doc Gap] Create docs/policy/legal/intellectual-property-policy.md" \
  '## Documentation Gap: Empty Section — Legal Directory

**Path:** `docs/policy/legal/intellectual-property-policy.md`
**Gap Type:** `docs/policy/legal/` directory has only an auto-generated index.
**Priority:** 🟡 Medium

### Why This Matters
Moko Consulting produces proprietary software (WaaS platform, CRM modules, MokoStandards libraries) alongside GPL-licensed open-source code. An IP policy clarifies ownership of work produced by employees and contractors, governs contributions to open-source projects, and ensures clients understand their rights to custom-built modules.

### Suggested Sections
- [ ] Purpose and Scope
- [ ] Ownership of Work — who owns code written during employment / engagement
- [ ] Contractor Work — assignment clauses and requirements
- [ ] Client-Specific Customizations — ownership vs. licensing back to Moko
- [ ] Third-Party Components — obligations for dependencies used in products
- [ ] Open-Source Contributions — process for contributing Moko code upstream
- [ ] Confidential Information — protecting proprietary code and algorithms
- [ ] Exceptions and Waivers Process

### Acceptance Criteria
- [ ] File created at `docs/policy/legal/intellectual-property-policy.md`
- [ ] Cross-referenced from `docs/policy/legal/index.md`
- [ ] Cross-references `docs/policy/license-compliance.md`'

create_issue \
  "[Doc Gap] Create docs/policy/legal/open-source-license-policy.md" \
  '## Documentation Gap: Empty Section — Legal Directory

**Path:** `docs/policy/legal/open-source-license-policy.md`
**Gap Type:** `docs/policy/legal/` directory has only an auto-generated index.
**Priority:** 🟡 Medium

### Why This Matters
MokoStandards is GPL-3.0-or-later licensed. CRM modules and WaaS components may have mixed licensing. A formal open-source license policy prevents accidental GPL contamination of proprietary code and documents which open-source licenses are approved for use as dependencies.

### Suggested Sections
- [ ] Purpose
- [ ] Approved Licenses — permissive licenses approved without legal review (MIT, Apache-2.0, BSD)
- [ ] Copyleft Licenses — use restrictions for GPL, LGPL, AGPL and review requirements
- [ ] Prohibited Licenses — licenses incompatible with our products
- [ ] Dependency Review Process — how new open-source dependencies are approved
- [ ] Contributing to Open Source — requirements for upstream contributions
- [ ] License Headers — reference to `docs/policy/file-header-standards.md`
- [ ] Exceptions Process

### Acceptance Criteria
- [ ] File created at `docs/policy/legal/open-source-license-policy.md`
- [ ] Consistent with SPDX identifiers used throughout the codebase
- [ ] Cross-references `docs/policy/license-compliance.md`'

# ============================================================
# BATCH 3 — Empty Development Guide Directory
# ============================================================

create_issue \
  "[Doc Gap] Create docs/guide/development/getting-started.md" \
  '## Documentation Gap: Empty Section — Development Guide Directory

**Path:** `docs/guide/development/getting-started.md`
**Gap Type:** `docs/guide/development/` exists but has no content documents — only an auto-generated `index.md`.
**Priority:** 🔴 High

### Why This Matters
There is no guide explaining how to start working with the MokoStandards codebase. New contributors — including AI coding agents — have no starting point beyond the README.

### Suggested Sections
- [ ] Prerequisites — PHP 8.1+, Composer, Git, GitHub CLI
- [ ] Repository Setup — clone, `composer install`, verify with `composer run check`
- [ ] Directory Tour — `api/`, `docs/`, `templates/`, `.github/`
- [ ] Key Concepts — platform types, enforcement levels, definition files, bulk sync
- [ ] Running the Validation Scripts — `check_repo_health.php`, `auto_detect_platform.php`
- [ ] Making Your First Change — branch naming, commit conventions, PR checklist
- [ ] Where to Get Help — SUPPORT.md, discussion channels

### Acceptance Criteria
- [ ] File created at `docs/guide/development/getting-started.md`
- [ ] Commands verified to work on a clean clone
- [ ] `docs/guide/development/index.md` updated'

create_issue \
  "[Doc Gap] Create docs/guide/development/contributing.md — contributor guide" \
  '## Documentation Gap: Empty Section — Development Guide Directory

**Path:** `docs/guide/development/contributing.md`
**Gap Type:** `docs/guide/development/` has no content documents.
**Priority:** 🔴 High

### Why This Matters
There is no formal contributing guide. Enterprise governance and open-source best practices both require a contributor guide that documents the PR workflow, code standards, testing requirements, and review process.

### Suggested Sections
- [ ] How to Contribute — issue types, discussion first vs. PR first
- [ ] Branch Naming — reference `docs/policy/branching-strategy.md`
- [ ] Commit Message Convention — conventional commits, `.gitmessage` template
- [ ] PHP Coding Standards — PSR-12, strict types, line length, forbidden functions
- [ ] File Headers — reference `docs/policy/file-header-standards.md`
- [ ] Testing Requirements — what tests to add/update, how to run
- [ ] Pull Request Process — labels, PR template, required checks, review requirements
- [ ] Code Review Standards — reference `docs/policy/code-review-guidelines.md`
- [ ] Documentation Requirements — update docs/ when changing api/

### Acceptance Criteria
- [ ] File created at `docs/guide/development/contributing.md`
- [ ] Consistent with existing policies referenced above
- [ ] Root CONTRIBUTING.md (or docs/guide/index.md) links to this guide'

create_issue \
  "[Doc Gap] Create docs/guide/development/local-dev-setup.md — local development environment setup" \
  '## Documentation Gap: Empty Section — Development Guide Directory

**Path:** `docs/guide/development/local-dev-setup.md`
**Gap Type:** `docs/guide/development/` has no content documents.
**Priority:** 🟡 Medium

### Why This Matters
Contributors need step-by-step instructions for setting up a local development environment including PHP, Composer, the test fixtures, and IDE configuration.

### Suggested Sections
- [ ] System Requirements — OS, PHP version, Composer version, Git
- [ ] Required Tools — PHP 8.1+, Composer 2.x, GitHub CLI, yamllint, markdownlint
- [ ] Optional Tools — phpstan, psalm, phpcs (or use `composer run check`)
- [ ] Repository Clone and Bootstrap — step-by-step commands
- [ ] IDE Setup — VS Code extensions, PHPStorm config, .editorconfig integration
- [ ] Test Fixtures — creating `tests/sample/` fixture directory
- [ ] Verifying Your Setup — run `composer run check`, expected output
- [ ] Troubleshooting Common Issues

### Acceptance Criteria
- [ ] File created at `docs/guide/development/local-dev-setup.md`
- [ ] All commands verified on a clean environment
- [ ] `docs/guide/development/index.md` updated'

# ============================================================
# BATCH 4 — Empty Onboarding Directory
# ============================================================

create_issue \
  "[Doc Gap] Create docs/guide/onboarding/new-developer-onboarding.md" \
  '## Documentation Gap: Empty Section — Onboarding Guide Directory

**Path:** `docs/guide/onboarding/new-developer-onboarding.md`
**Gap Type:** `docs/guide/onboarding/` exists but contains only an auto-generated `index.md`.
**Priority:** 🔴 High

### Why This Matters
There is no onboarding guide for new developers joining the Moko Consulting engineering team. New hires have no documented path from zero to productive contributor.

### Suggested Sections
- [ ] Day 1 Checklist — accounts to create, access to request
- [ ] GitHub Organization Access — joining mokoconsulting-tech org, required 2FA
- [ ] Required Tool Installations — reference `docs/guide/development/local-dev-setup.md`
- [ ] Codebase Orientation — purpose of MokoStandards, where things live
- [ ] Key Policies to Read — security, AUP, AI tool governance, branching strategy
- [ ] First Week Goals — first issue, first PR, first review
- [ ] Team Contacts and Communication Channels
- [ ] Compliance Training — data classification, security awareness

### Acceptance Criteria
- [ ] File created at `docs/guide/onboarding/new-developer-onboarding.md`
- [ ] `docs/guide/onboarding/index.md` updated
- [ ] References the local-dev-setup guide and key policies'

create_issue \
  "[Doc Gap] Create docs/guide/onboarding/toolchain-setup.md — required toolchain setup" \
  '## Documentation Gap: Empty Section — Onboarding Guide Directory

**Path:** `docs/guide/onboarding/toolchain-setup.md`
**Gap Type:** `docs/guide/onboarding/` has no content documents.
**Priority:** 🟡 Medium

### Why This Matters
New team members need explicit toolchain setup instructions covering PHP, Composer, GitHub CLI, Terraform, Joomla local environment, and Dolibarr local dev. A centralized toolchain setup guide prevents tribal knowledge.

### Suggested Sections
- [ ] PHP and Composer Setup — version requirements, installation, configuration
- [ ] Git Configuration — username, email, signing keys, .gitmessage template
- [ ] GitHub CLI — installation, auth (`gh auth login`), org access
- [ ] Terraform — installation, version, authentication for IaC work
- [ ] YAML and Markdown Linters — yamllint, markdownlint-cli
- [ ] IDE and Editor Setup — recommended extensions per editor
- [ ] Docker / Local Containers — for WaaS and CRM local dev (if applicable)
- [ ] Verification Checklist — commands to confirm each tool is correctly installed

### Acceptance Criteria
- [ ] File created at `docs/guide/onboarding/toolchain-setup.md`
- [ ] All installation commands tested and verified
- [ ] Cross-referenced from `docs/guide/onboarding/new-developer-onboarding.md`'

# ============================================================
# BATCH 5 — Enterprise Standard Gaps
# ============================================================

create_issue \
  "[Doc Gap] Create docs/policy/secrets-management.md — secrets and credentials management policy" \
  '## Documentation Gap: Enterprise Standard Missing

**Path:** `docs/policy/secrets-management.md`
**Gap Type:** Document does not exist; required by enterprise security standards.
**Priority:** 🔴 High

### Why This Matters
The codebase uses GitHub Actions secrets (GH_TOKEN), .env files, API keys, SSH keys, and other credentials extensively. There is no policy governing how these are stored, rotated, accessed, or handled when compromised.

### Suggested Sections
- [ ] Secret Classification — API tokens, PATs, SSH keys, database passwords, webhook secrets
- [ ] Approved Storage Locations — GitHub Actions Secrets (org-level), .env files (gitignored), never plaintext in code
- [ ] Prohibited Practices — no secrets in commit history, no secrets in issue comments, no hardcoded tokens
- [ ] Secret Naming Conventions — GH_TOKEN, GITHUB_TOKEN fallback, other token naming
- [ ] Rotation Policy — rotation schedule by secret type and sensitivity
- [ ] Access Controls — who can read/write which secrets, org vs repo level
- [ ] Compromise Response — steps when a secret is exposed
- [ ] Audit and Monitoring — how secret usage is logged

### Acceptance Criteria
- [ ] File created at `docs/policy/secrets-management.md`
- [ ] Covers all secret types currently in use across the org
- [ ] Consistent with `docs/policy/security/access-control-identity-management.md`
- [ ] `docs/policy/index.md` updated'

create_issue \
  "[Doc Gap] Create docs/policy/patch-management.md — dependency and patch management policy" \
  '## Documentation Gap: Enterprise Standard Missing

**Path:** `docs/policy/patch-management.md`
**Gap Type:** Document does not exist; required by enterprise security standards.
**Priority:** 🟡 Medium

### Why This Matters
The repository uses Composer dependencies, pinned GitHub Actions SHAs, and Terraform providers. There is no policy governing how dependencies are kept up to date or how security patches are applied.

### Suggested Sections
- [ ] Scope — PHP/Composer packages, GitHub Actions, Terraform providers, npm (if applicable)
- [ ] Vulnerability Severity Definitions — critical/high/medium/low and timelines
- [ ] Patch Response Timelines by Severity — critical: 24h, high: 72h, medium: 2 weeks, low: next sprint
- [ ] Automated Patching — Dependabot / `auto-update-sha.yml` workflow coverage
- [ ] Manual Patch Process — how to update pinned SHAs, Composer packages
- [ ] Testing Requirements Before Applying Patches
- [ ] Emergency Patch Process — hotfix branch, expedited review
- [ ] Exceptions and Deferral Process

### Acceptance Criteria
- [ ] File created at `docs/policy/patch-management.md`
- [ ] References `docs/policy/dependency-management.md` and `docs/policy/security/vulnerability-management.md`
- [ ] Consistent with the `pin-action-shas.yml` and `auto-update-sha.yml` workflows'

create_issue \
  "[Doc Gap] Create docs/policy/access-review-policy.md — periodic access review policy" \
  '## Documentation Gap: Enterprise Standard Missing

**Path:** `docs/policy/access-review-policy.md`
**Gap Type:** Document does not exist; required by enterprise security governance.
**Priority:** 🟡 Medium

### Why This Matters
Enterprise security standards (SOC 2, ISO 27001) require periodic reviews of who has access to organization systems. There is no documented process for quarterly access reviews of GitHub org members, repository collaborators, or external service integrations.

### Suggested Sections
- [ ] Review Frequency — quarterly for GitHub org, annually for external integrations
- [ ] Scope — GitHub org members, repository collaborators, GitHub Apps, PATs, SSH keys, third-party service access
- [ ] Review Responsibilities — who conducts the review, who approves changes
- [ ] Review Process — how to enumerate access, how to verify continued need
- [ ] Remediation — timeline for removing excess access after review
- [ ] Documentation Requirements — access review records, sign-off
- [ ] New Joiner / Leaver Procedures — immediate revocation on offboarding
- [ ] Exception Process

### Acceptance Criteria
- [ ] File created at `docs/policy/access-review-policy.md`
- [ ] Cross-references `docs/policy/security/access-control-identity-management.md`
- [ ] Includes concrete review schedule and responsible roles'

create_issue \
  "[Doc Gap] Create docs/guide/release-process.md — step-by-step release process guide" \
  '## Documentation Gap: Enterprise Standard Missing

**Path:** `docs/guide/release-process.md`
**Gap Type:** No how-to guide for the release process exists; only policy (`docs/policy/governance/release-management.md`) which is itself a stub.
**Priority:** 🟡 Medium

### Why This Matters
There is no practical guide explaining the actual steps to cut a release — covering version bumps, changelog updates, tagging, and post-release verification for MokoStandards itself and governed repositories.

### Suggested Sections
- [ ] Release Types — patch (pp), minor (mm), major (MM) and when to use each
- [ ] Pre-Release Checklist — all tests passing, security scan clean, changelog updated
- [ ] Version Bump — which files to update (VERSION in headers, README badge, CHANGELOG)
- [ ] Branch Management — `rc/` branch, merge to `main`, tagging
- [ ] Changelog Update — format reference `docs/policy/changelog-standards.md`
- [ ] Tagging and Publishing — git tag format, GitHub Release creation
- [ ] Post-Release — verify auto-release workflow, update version on `dev/`
- [ ] Hotfix Release Process — expedited path for critical fixes

### Acceptance Criteria
- [ ] File created at `docs/guide/release-process.md`
- [ ] Consistent with `docs/policy/governance/release-management.md`
- [ ] Consistent with `docs/workflows/release-system.md`
- [ ] `docs/guide/index.md` updated'

create_issue \
  "[Doc Gap] Create docs/guide/development/testing-guide.md — practical testing guide" \
  '## Documentation Gap: Enterprise Standard Missing

**Path:** `docs/guide/development/testing-guide.md`
**Gap Type:** No practical testing guide exists.
**Priority:** 🟡 Medium

### Why This Matters
There is a `docs/policy/quality/testing-strategy-standards.md` (a stub) but no practical guide for developers on how to write, organize, and run tests for MokoStandards scripts and Enterprise libraries.

### Suggested Sections
- [ ] Testing Philosophy — what we test, what we do not, test pyramid
- [ ] Test Types — `test_enterprise_libraries.php`, integration tests in `.github/workflows/integration-tests.yml`
- [ ] Running Tests — `composer run test`, individual test scripts
- [ ] Writing a New Test — structure, naming conventions, assertions
- [ ] Test Fixtures — `tests/sample/` structure, reference `docs/api/tests/sample/index.md`
- [ ] Mocking and Stubs — how to stub `ApiClient`, `AuditLogger` etc.
- [ ] Coverage Expectations — what needs to be covered before a PR merges
- [ ] CI Test Pipeline — how tests run in `.github/workflows/integration-tests.yml`

### Acceptance Criteria
- [ ] File created at `docs/guide/development/testing-guide.md`
- [ ] Commands in the guide are verified to work
- [ ] `docs/guide/development/index.md` updated'

# ============================================================
# BATCH 6 — Stub Security Policies
# ============================================================

create_issue \
  "[Doc Gap] Complete stub: docs/policy/security/access-control-identity-management.md" \
  '## Documentation Gap: Stub Policy Needing Completion

**Path:** `docs/policy/security/access-control-identity-management.md`
**Gap Type:** File exists as a stub with "To be defined" placeholders throughout. Status: DRAFT, ~350 words.
**Priority:** 🔴 High (CRITICAL tier)

### Current State
The document has correct structure and headings but every policy section reads "**To be defined:**" with a bullet list of topics. There is no actual policy content.

### Sections That Need Real Content
- [ ] **RBAC** — define actual roles (Owner, Admin, Developer, ReadOnly), permission matrices per role
- [ ] **Authentication Standards** — require GitHub 2FA org-wide, approved authentication methods
- [ ] **Multi-Factor Authentication** — MFA mandatory for all org members, approved methods (TOTP, hardware key)
- [ ] **Access Review Procedures** — reference new `docs/policy/access-review-policy.md`
- [ ] **Service Accounts** — PAT naming conventions, scope restrictions, expiry requirements
- [ ] **Privileged Access** — owner-level access approval process, minimum owner count

### Acceptance Criteria
- [ ] All "To be defined" sections replaced with actual policy statements
- [ ] Stub warning removed
- [ ] Version field updated (currently shows 03.00.00)
- [ ] Status changed from DRAFT to Active'

create_issue \
  "[Doc Gap] Complete stub: docs/policy/security/vulnerability-management.md" \
  '## Documentation Gap: Stub Policy Needing Completion

**Path:** `docs/policy/security/vulnerability-management.md`
**Gap Type:** File exists as a stub with "To be defined" placeholders. Status: DRAFT, ~330 words.
**Priority:** 🔴 High (CRITICAL security tier)

### Current State
Structure exists but all substantive sections are "To be defined." The CodeQL and Dependabot workflows exist and generate alerts, but there is no policy governing how those alerts are triaged and resolved.

### Sections That Need Real Content
- [ ] **Vulnerability Identification** — tools in use: CodeQL, Dependabot, `check_no_secrets.php`, `security-scan.yml`
- [ ] **Severity Classification** — map GitHub severity levels to response timelines; reference CVSS scoring
- [ ] **Response Timelines** — Critical: 24h; High: 72h; Medium: 2 weeks; Low: next sprint
- [ ] **Responsible Disclosure** — how external researchers report vulnerabilities
- [ ] **False Positive Process** — how to dismiss CodeQL alerts with justification
- [ ] **Dependency Vulnerabilities** — Dependabot alert triage process

### Acceptance Criteria
- [ ] All "To be defined" sections replaced with actual policy
- [ ] Consistent with `docs/policy/patch-management.md` (to be created)
- [ ] Stub warning removed; Status set to Active'

create_issue \
  "[Doc Gap] Complete stub: docs/policy/security/backup-recovery.md" \
  '## Documentation Gap: Stub Policy Needing Completion

**Path:** `docs/policy/security/backup-recovery.md`
**Gap Type:** Stub with "To be defined" placeholders. Status: DRAFT, ~340 words.
**Priority:** 🔴 High (CRITICAL security tier)

### Current State
Structure and headings are correct. All policy sections are empty "To be defined" placeholders. The `docs/guide/operations/backup-restore-procedures.md` guide also has stub markers — both need to be completed together.

### Sections That Need Real Content
- [ ] **Backup Requirements** — what must be backed up: code (GitHub), configuration, Dolibarr DB, WaaS site files, definitions
- [ ] **Backup Frequency** — per asset type (daily DB backups, continuous for code via Git)
- [ ] **Retention Policy** — how long backups are kept by type
- [ ] **Backup Testing** — frequency of restore tests; quarterly minimum
- [ ] **Recovery Time Objectives (RTO)** — per service tier
- [ ] **Recovery Point Objectives (RPO)** — per service tier
- [ ] **Offsite/Redundant Storage** — where backups are stored, geographic redundancy

### Acceptance Criteria
- [ ] All "To be defined" sections replaced with actual policy
- [ ] RTO/RPO targets defined per service tier
- [ ] Stub warning removed; Status set to Active'

create_issue \
  "[Doc Gap] Complete stub: docs/policy/security/data-privacy-gdpr-compliance.md" \
  '## Documentation Gap: Stub Policy Needing Completion

**Path:** `docs/policy/security/data-privacy-gdpr-compliance.md`
**Gap Type:** Stub with "To be defined" placeholders. Status: DRAFT, ~355 words.
**Priority:** 🔴 High (CRITICAL — legal/regulatory)

### Current State
All policy sections are placeholders. Given that Moko Consulting serves clients across the EU and handles client data through WaaS and CRM platforms, a real GDPR compliance policy is legally required.

### Sections That Need Real Content
- [ ] **Data Controller vs Processor** — Moko Consulting'"'"'s role for each product line
- [ ] **Personal Data Inventory** — categories of personal data processed
- [ ] **Legal Basis for Processing** — per data category (contract, legitimate interest, consent)
- [ ] **Data Subject Rights** — process for access requests, deletion, portability; 30-day response
- [ ] **Data Retention** — cross-reference `docs/policy/waas/data-retention.md`
- [ ] **Breach Notification** — 72-hour supervisory authority notification
- [ ] **Data Protection by Design** — requirements for new feature development

### Acceptance Criteria
- [ ] All sections populated with actual policy statements
- [ ] Legal review recommended before marking Active
- [ ] Cross-references `docs/policy/waas/data-retention.md` and `docs/policy/data-classification.md`'

create_issue \
  "[Doc Gap] Complete stub: docs/policy/security/disaster-recovery-business-continuity.md" \
  '## Documentation Gap: Stub Policy Needing Completion

**Path:** `docs/policy/security/disaster-recovery-business-continuity.md`
**Gap Type:** Stub with "To be defined" placeholders. Status: DRAFT, ~352 words.
**Priority:** 🔴 High (CRITICAL security tier)

### Sections That Need Real Content
- [ ] **Business Continuity Scope** — services covered: WaaS hosting, CRM, MokoStandards governance
- [ ] **Recovery Tiers** — classify services by criticality (Tier 1: WaaS; Tier 2: CRM; Tier 3: internal tooling)
- [ ] **RTO by Tier** — maximum tolerable downtime
- [ ] **RPO by Tier** — maximum acceptable data loss
- [ ] **DR Testing** — annual full DR test requirement; tabletop exercise schedule
- [ ] **Communication Plan** — who notifies whom during an incident
- [ ] **Key Dependencies** — GitHub, hosting provider, DNS, CDN; alternatives if unavailable
- [ ] **Plan Review Cycle** — annual review; review after any major incident

### Acceptance Criteria
- [ ] RTO/RPO defined per service tier
- [ ] DR test schedule defined
- [ ] Stub warning removed; Status set to Active'

create_issue \
  "[Doc Gap] Complete stub: docs/policy/security/encryption-standards.md" \
  '## Documentation Gap: Stub Policy Needing Completion

**Path:** `docs/policy/security/encryption-standards.md`
**Gap Type:** Stub with "To be defined" placeholders. Status: DRAFT, ~346 words.
**Priority:** 🔴 High

### Sections That Need Real Content
- [ ] **Data at Rest** — encryption requirements for databases, backup storage, developer workstations
- [ ] **Data in Transit** — TLS 1.2+ minimum; TLS 1.3 preferred; no plaintext protocols for sensitive data
- [ ] **Algorithm Standards** — AES-256 for symmetric, RSA-4096 or ECDSA for asymmetric, SHA-256+ for hashing
- [ ] **Key Management** — key generation, storage (never in code), rotation schedule, destruction
- [ ] **GitHub Secrets Encryption** — GitHub'"'"'s encryption of Actions secrets
- [ ] **SSH Key Standards** — minimum key size (Ed25519 or RSA-4096), passphrase requirements
- [ ] **Code Signing** — requirements for signing releases/commits (if applicable)

### Acceptance Criteria
- [ ] All sections populated with actual standards
- [ ] Consistent with industry standards (NIST 800-57, OWASP)
- [ ] Stub warning removed; Status set to Active'

create_issue \
  "[Doc Gap] Complete stub: docs/policy/security/audit-logging-monitoring.md" \
  '## Documentation Gap: Stub Policy Needing Completion

**Path:** `docs/policy/security/audit-logging-monitoring.md`
**Gap Type:** Stub with "To be defined" placeholders. Status: DRAFT, ~334 words.
**Priority:** 🔴 High

### Current State
The `AuditLogger` Enterprise class exists and is used by many scripts, but there is no policy governing what must be logged, how long logs must be retained, or how they must be protected.

### Sections That Need Real Content
- [ ] **Audit Log Requirements** — which events must be logged: authentication, authorization changes, bulk sync operations, script execution
- [ ] **Log Content Standards** — required fields: timestamp (UTC), actor, action, resource, outcome
- [ ] **Log Retention** — minimum 90 days online; 1 year archive for security events
- [ ] **Log Protection** — tamper-evident storage; access controls on log files
- [ ] **Log Review** — who reviews logs; frequency; alerting thresholds
- [ ] **Integration with AuditLogger** — reference to the Enterprise library; log file locations (`logs/`)
- [ ] **GitHub Audit Log** — org-level GitHub audit log retention and review

### Acceptance Criteria
- [ ] All sections populated
- [ ] Consistent with `AuditLogger` Enterprise class capabilities
- [ ] Stub warning removed; Status set to Active'

# ============================================================
# BATCH 7 — Stub Operations Policies
# ============================================================

create_issue \
  "[Doc Gap] Complete stub: docs/policy/operations/sla-policy.md" \
  '## Documentation Gap: Stub Policy Needing Completion

**Path:** `docs/policy/operations/sla-policy.md`
**Gap Type:** Stub with "To be defined" placeholders. Status: DRAFT, ~343 words.
**Priority:** 🔴 High (CRITICAL — client-facing)

### Sections That Need Real Content
- [ ] **Service Tiers** — Standard WaaS, Enterprise WaaS, CRM managed service; features and SLAs per tier
- [ ] **Availability Targets** — uptime % per tier (e.g., 99.5% Standard, 99.9% Enterprise)
- [ ] **Response Times** — initial response by severity (P1: 1h, P2: 4h, P3: next business day)
- [ ] **Resolution Time Targets** — per severity and service tier
- [ ] **Scheduled Maintenance Windows** — when maintenance can occur without SLA penalty
- [ ] **SLA Exclusions** — force majeure, client-caused outages, third-party dependencies
- [ ] **SLA Credits** — compensation mechanism when targets are missed
- [ ] **Measurement and Reporting** — how SLA performance is measured and reported to clients

### Acceptance Criteria
- [ ] SLA targets defined per service tier
- [ ] Credit mechanism defined
- [ ] Stub warning removed; Status set to Active'

create_issue \
  "[Doc Gap] Complete stub: docs/policy/operations/monitoring-alerting-standards.md" \
  '## Documentation Gap: Stub Policy Needing Completion

**Path:** `docs/policy/operations/monitoring-alerting-standards.md`
**Gap Type:** Stub with "To be defined" placeholders. Status: DRAFT, ~338 words.
**Priority:** 🔴 High

### Sections That Need Real Content
- [ ] **Monitoring Scope** — what must be monitored: WaaS site uptime, CRM availability, GitHub Actions workflow success rates
- [ ] **Monitoring Tools** — Panopticon (WaaS), GitHub Actions status, external uptime monitoring service
- [ ] **Alert Severity Levels** — mapping from monitoring alert to incident severity (P1-P4)
- [ ] **Alert Response Requirements** — who is notified per alert level; response time SLAs per level
- [ ] **Alerting Thresholds** — uptime %, error rate %, disk usage %, response time
- [ ] **On-Call Requirements** — is 24/7 on-call required? For which service tiers?
- [ ] **Runbook Requirements** — every alert must have a runbook reference
- [ ] **Reporting** — weekly/monthly availability reports for clients

### Acceptance Criteria
- [ ] Monitoring tools named and justified
- [ ] Alert severity mapping defined
- [ ] Stub warning removed; Status set to Active'

create_issue \
  "[Doc Gap] Complete stub: docs/policy/operations/capacity-planning-scaling.md" \
  '## Documentation Gap: Stub Policy Needing Completion

**Path:** `docs/policy/operations/capacity-planning-scaling.md`
**Gap Type:** Stub with "To be defined" placeholders. Status: DRAFT, ~326 words.
**Priority:** 🟡 Medium

### Sections That Need Real Content
- [ ] **Capacity Metrics** — server CPU/RAM/disk, database size, GitHub API rate limits, GitHub Actions concurrency limits
- [ ] **Review Frequency** — quarterly capacity reviews; triggers for ad-hoc review (> 80% utilization)
- [ ] **Growth Forecasting** — how to project 3-6 month capacity needs
- [ ] **Scaling Triggers** — thresholds that trigger scaling actions (e.g., 85% disk)
- [ ] **Scaling Procedures** — how to scale WaaS infrastructure; GitHub Actions runner scaling
- [ ] **Cost Management** — capacity decisions must consider cost implications
- [ ] **Infrastructure as Code** — all capacity changes tracked via IaC / Terraform

### Acceptance Criteria
- [ ] Capacity metrics defined per platform
- [ ] Scaling triggers and procedures documented
- [ ] Stub warning removed; Status set to Active'

create_issue \
  "[Doc Gap] Complete stub: docs/policy/operations/infrastructure-as-code-standards.md" \
  '## Documentation Gap: Stub Policy Needing Completion

**Path:** `docs/policy/operations/infrastructure-as-code-standards.md`
**Gap Type:** Stub with "To be defined" placeholders. Status: DRAFT, ~328 words.
**Priority:** 🔴 High

### Sections That Need Real Content
- [ ] **IaC Tools** — Terraform (definition files in `api/definitions/`), GitHub Actions (`.github/workflows/`)
- [ ] **Version Control Requirements** — all IaC in Git; no manual infrastructure changes without code change
- [ ] **Code Review Requirements** — all IaC changes require PR review; no direct pushes to `main`
- [ ] **Terraform Standards** — file naming, HCL formatting, module structure
- [ ] **Secrets in IaC** — never commit secrets; use GitHub Secrets
- [ ] **Testing IaC** — drift detection via `terraform-drift.yml`; validation scripts
- [ ] **Approved Providers/Registries** — only approved Terraform providers and GitHub Actions sources

### Acceptance Criteria
- [ ] All sections populated with actual standards
- [ ] Cross-references `docs/policy/terraform-file-standards.md`
- [ ] Stub warning removed; Status set to Active'

create_issue \
  "[Doc Gap] Complete stub: docs/policy/operations/environment-management.md" \
  '## Documentation Gap: Stub Policy Needing Completion

**Path:** `docs/policy/operations/environment-management.md`
**Gap Type:** Stub with "To be defined" placeholders. Status: DRAFT, ~332 words.
**Priority:** 🟡 Medium

### Sections That Need Real Content
- [ ] **Environment Definitions** — list all environments: local dev, staging, production WaaS, production CRM, demo/baseline
- [ ] **Environment Parity** — requirements for dev/staging/prod parity; which differences are permitted
- [ ] **Promotion Process** — how changes move from dev → rc → main → production
- [ ] **Environment Access Controls** — who can access production; break-glass procedures
- [ ] **Configuration Management** — how environment-specific config is managed (GitHub Secrets, .env, override.tf)
- [ ] **Demo and Baseline Environments** — reference `docs/policy/waas/demo-baseline.md`
- [ ] **Environment Decommissioning** — reference `docs/policy/waas/decommissioning.md`

### Acceptance Criteria
- [ ] All environments named and described
- [ ] Promotion process defined
- [ ] Stub warning removed; Status set to Active'

create_issue \
  "[Doc Gap] Complete stub: docs/policy/operations/database-management.md" \
  '## Documentation Gap: Stub Policy Needing Completion

**Path:** `docs/policy/operations/database-management.md`
**Gap Type:** Stub with "To be defined" placeholders. Status: DRAFT, ~352 words.
**Priority:** 🟡 Medium

### Sections That Need Real Content
- [ ] **Database Inventory** — list all databases: Dolibarr MySQL/MariaDB, WaaS per-client Joomla DBs
- [ ] **Access Controls** — DB user accounts, principle of least privilege, no shared root passwords
- [ ] **Backup Requirements** — cross-reference `docs/policy/security/backup-recovery.md`
- [ ] **Change Management** — how schema changes are approved and deployed; migration scripts in version control
- [ ] **Performance Monitoring** — slow query logging, index monitoring, query review
- [ ] **Data Retention** — cross-reference `docs/policy/waas/data-retention.md`
- [ ] **Sensitive Data** — encryption of PII fields; cross-reference GDPR policy

### Acceptance Criteria
- [ ] All databases named
- [ ] Change management process defined
- [ ] Cross-references backup and GDPR policies
- [ ] Stub warning removed; Status set to Active'

create_issue \
  "[Doc Gap] Complete stub: docs/policy/operations/api-standards-versioning.md" \
  '## Documentation Gap: Stub Policy Needing Completion

**Path:** `docs/policy/operations/api-standards-versioning.md`
**Gap Type:** Stub with "To be defined" placeholders. Status: DRAFT, ~382 words.
**Priority:** 🔴 High

### Sections That Need Real Content
- [ ] **Versioning Scheme** — `MM.mm.pp` format; breaking vs non-breaking change definitions
- [ ] **API Design Standards** — for Enterprise library classes: method naming, return types, exception handling
- [ ] **Backward Compatibility** — policy on breaking changes: major version bump required; deprecation notice period
- [ ] **Deprecation Process** — `@deprecated` annotation, migration guide, minimum deprecation period
- [ ] **API Documentation** — PHPDoc requirements for all public methods; docs/api/ mirror structure
- [ ] **External API Integration** — standards for consuming external APIs (GitHub API, rate limits, circuit breaker)
- [ ] **Changelog Requirements** — every breaking change must be in CHANGELOG.md

### Acceptance Criteria
- [ ] Versioning scheme documented and consistent with current `MM.mm.pp` usage
- [ ] Backward compatibility policy defined
- [ ] Stub warning removed; Status set to Active'

create_issue \
  "[Doc Gap] Complete stub: docs/policy/operations/performance-testing-standards.md" \
  '## Documentation Gap: Stub Policy Needing Completion

**Path:** `docs/policy/operations/performance-testing-standards.md`
**Gap Type:** Stub with "To be defined" placeholders. Status: DRAFT, ~319 words.
**Priority:** 🟡 Medium

### Sections That Need Real Content
- [ ] **Performance Testing Scope** — WaaS page load times, bulk sync script performance, API rate limit headroom
- [ ] **Performance Benchmarks** — WaaS: target page load < 3s; bulk sync: < 60s per repo; API client: < 5s per call
- [ ] **Test Types** — load testing for WaaS, timing benchmarks for PHP scripts, GitHub API rate limit testing
- [ ] **Tools** — specify tools (e.g., k6, Apache Bench for WaaS; PHP microtime for scripts)
- [ ] **CI Integration** — which performance tests run in CI; acceptable regression thresholds
- [ ] **Baseline and Regression** — how performance baselines are established and protected

### Acceptance Criteria
- [ ] Benchmarks defined per system type
- [ ] CI integration path identified
- [ ] Stub warning removed; Status set to Active'

# ============================================================
# BATCH 8 — Stub Quality Policies
# ============================================================

create_issue \
  "[Doc Gap] Complete stub: docs/policy/quality/quality-gates.md" \
  '## Documentation Gap: Stub Policy Needing Completion

**Path:** `docs/policy/quality/quality-gates.md`
**Gap Type:** Stub with "To be defined" placeholders. Status: DRAFT, ~327 words.
**Priority:** 🔴 High

### Current State
All policy sections are "To be defined." Quality gates directly determine what can merge to `main`, so this is a high-impact policy gap.

### Sections That Need Real Content
- [ ] **Code Quality Metrics** — PHP: PSR-12 compliance required, PHPStan level 5+ required, no `eval`/`var_dump`; test coverage target
- [ ] **Security Scanning Gates** — CodeQL must pass (0 critical/high alerts); `check_no_secrets.php` must pass
- [ ] **Documentation Gates** — file headers must be present; `docs/` updated for any API change
- [ ] **PR Approval Requirements** — minimum 1 reviewer approval; all automated checks must pass before merge
- [ ] **Branch Protection** — `main` branch: no direct pushes, required status checks
- [ ] **Exceptions** — emergency hotfix gate bypass process; documentation required

### Acceptance Criteria
- [ ] All gates defined with specific, measurable thresholds
- [ ] Consistent with existing CI workflow check names
- [ ] Stub warning removed; Status set to Active'

create_issue \
  "[Doc Gap] Complete stub: docs/policy/quality/testing-strategy-standards.md" \
  '## Documentation Gap: Stub Policy Needing Completion

**Path:** `docs/policy/quality/testing-strategy-standards.md`
**Gap Type:** Stub with "To be defined" placeholders. Status: DRAFT, ~360 words.
**Priority:** 🔴 High

### Sections That Need Real Content
- [ ] **Testing Requirements** — unit tests required for all new Enterprise library methods; integration tests required for all new workflows
- [ ] **Test Coverage Targets** — define minimum coverage % per component
- [ ] **Test Types Required** — unit (PHPUnit), integration (workflow tests), smoke tests (`test_enterprise_libraries.php`)
- [ ] **Test Isolation** — no network calls in unit tests; stub external dependencies
- [ ] **Test Data** — test fixtures must not contain real credentials or PII; `tests/sample/` is the canonical fixture
- [ ] **CI Requirements** — all tests must pass in CI before merge; no skipping tests in `main`

### Acceptance Criteria
- [ ] Coverage targets defined per component
- [ ] Required test types listed per change type
- [ ] Stub warning removed; Status set to Active'

create_issue \
  "[Doc Gap] Complete stub: docs/policy/quality/technical-debt-management.md" \
  '## Documentation Gap: Stub Policy Needing Completion

**Path:** `docs/policy/quality/technical-debt-management.md`
**Gap Type:** Stub with "To be defined" placeholders. Status: DRAFT, ~325 words.
**Priority:** 🟡 Medium

### Sections That Need Real Content
- [ ] **Technical Debt Definition** — categories: code debt, documentation debt (stub docs), test debt, infrastructure debt
- [ ] **Debt Tracking** — use GitHub Issues with a `technical-debt` label; high-level summary in `docs/TODO_TRACKING.md`
- [ ] **Debt Budget** — how much new debt is acceptable per sprint/release
- [ ] **Debt Reduction Targets** — quarterly debt reduction goals; stub policies must be completed within defined timeframe
- [ ] **Prioritization** — critical security debt: immediate; high functional debt: current sprint; medium: next quarter
- [ ] **Refactoring Policy** — CLIApp → CliFramework migration; no new code extending deprecated CLIApp

### Acceptance Criteria
- [ ] Debt categories defined
- [ ] Tracking and resolution process documented
- [ ] CLIApp deprecation timeline established
- [ ] Stub warning removed; Status set to Active'

# ============================================================
# BATCH 9 — Stub Governance Policy + Partially Stub Guides
# ============================================================

create_issue \
  "[Doc Gap] Complete stub: docs/policy/governance/incident-management.md" \
  '## Documentation Gap: Stub Policy Needing Completion

**Path:** `docs/policy/governance/incident-management.md`
**Gap Type:** Stub with "To be defined" placeholders. Status: DRAFT, ~360 words.
**Priority:** 🔴 High (CRITICAL tier)

### Sections That Need Real Content
- [ ] **Incident Severity Levels** — define P0/P1/P2/P3/P4 with criteria: user impact, data at risk, revenue impact
- [ ] **Escalation Path** — per severity: who gets notified, by whom, within what timeframe
- [ ] **Response Timelines** — P0: < 15 min; P1: < 1 hour; P2: < 4 hours; P3: next business day
- [ ] **War Room / Incident Commander** — roles during an active incident
- [ ] **Communication Templates** — internal and client-facing status update templates
- [ ] **Post-Incident Review (PIR)** — required for P0/P1; timeline for PIR completion
- [ ] **Integration with WaaS Policy** — incorporate and reference `docs/policy/waas/incident-response.md`
- [ ] **Runbook Index** — link to `docs/guide/operations/incident-response-runbooks.md`

### Acceptance Criteria
- [ ] P0-P4 severity definitions documented
- [ ] Escalation paths and response timelines defined
- [ ] Stub warning removed; Status set to Active'

create_issue \
  "[Doc Gap] Complete partial stub: docs/guide/operations/disaster-recovery-procedures.md" \
  '## Documentation Gap: Partially-Stub Guide Needing Completion

**Path:** `docs/guide/operations/disaster-recovery-procedures.md`
**Gap Type:** Guide exists (155 lines) but contains "To be defined" placeholder sections.
**Priority:** 🔴 High

### Sections That Need Completion
- [ ] **Recovery Procedures per Scenario** — step-by-step procedures for: WaaS server failure, database corruption, GitHub Actions outage, DNS failure, credential compromise
- [ ] **Recovery Verification Steps** — how to confirm recovery was successful for each scenario
- [ ] **Contact List** — key contacts for each recovery scenario
- [ ] **Tool Access** — what tools are needed and where to find credentials during a DR event
- [ ] **Communication Templates** — what to communicate and to whom during different DR scenarios

### Acceptance Criteria
- [ ] All "To be defined" sections replaced with actual procedures
- [ ] Procedures are step-by-step and actionable
- [ ] Cross-references `docs/policy/security/disaster-recovery-business-continuity.md`'

create_issue \
  "[Doc Gap] Complete partial stub: docs/guide/operations/backup-restore-procedures.md" \
  '## Documentation Gap: Partially-Stub Guide Needing Completion

**Path:** `docs/guide/operations/backup-restore-procedures.md`
**Gap Type:** Guide exists (158 lines) but contains "To be defined" placeholder sections.
**Priority:** 🔴 High

### Sections That Need Completion
- [ ] **Backup Execution Procedures** — step-by-step instructions for: Dolibarr database backup, WaaS site file backup, WaaS database backup, GitHub repository archive
- [ ] **Backup Verification** — how to verify backup integrity; checksum verification; test restore steps
- [ ] **Restore Procedures** — step-by-step restore for each asset type with expected restore times
- [ ] **Backup Storage Locations** — where backups are stored; access credentials location
- [ ] **Failure Handling** — what to do when a backup job fails; alerting and escalation

### Acceptance Criteria
- [ ] All "To be defined" sections replaced with actual procedures
- [ ] Restore procedures tested and verified to work
- [ ] Cross-references `docs/policy/security/backup-recovery.md`'

create_issue \
  "[Doc Gap] Complete partial stub: docs/guide/operations/database-administration-guide.md" \
  '## Documentation Gap: Partially-Stub Guide Needing Completion

**Path:** `docs/guide/operations/database-administration-guide.md`
**Gap Type:** Guide exists (196 lines) but contains "To be defined" placeholder sections.
**Priority:** 🟡 Medium

### Sections That Need Completion
- [ ] **Common Administrative Tasks** — user management, schema changes, index optimization, query analysis
- [ ] **Performance Tuning** — slow query log analysis; common optimization patterns for Dolibarr and Joomla
- [ ] **Database Monitoring** — what metrics to watch; how to access monitoring; alert thresholds
- [ ] **Schema Change Process** — how to safely apply schema migrations; rollback procedures
- [ ] **Troubleshooting Guide** — common database issues and resolution steps

### Acceptance Criteria
- [ ] All "To be defined" sections replaced with actual procedures
- [ ] Commands/SQL examples verified against actual Dolibarr/Joomla databases
- [ ] Cross-references `docs/policy/operations/database-management.md`'

# ============================================================
# BATCH 10 — Final missing enterprise standard
# ============================================================

create_issue \
  "[Doc Gap] Create docs/guide/operations/deployment-guide.md — deployment process guide" \
  '## Documentation Gap: Enterprise Standard Missing

**Path:** `docs/guide/operations/deployment-guide.md`
**Gap Type:** No deployment guide exists for the operations/ guide section.
**Priority:** 🟡 Medium

### Why This Matters
The `docs/guide/operations/` directory has runbooks for incidents, backup/restore, DR, firewall, and DB admin — but nothing on standard deployment. Developers and ops team members need a guide for deploying WaaS site updates, CRM module updates, and standards infrastructure updates.

### Suggested Sections
- [ ] **Deployment Scope** — WaaS site updates via Panopticon, CRM module deployments, MokoStandards-governed repo updates via bulk sync
- [ ] **Pre-Deployment Checklist** — code reviewed and merged, tests passing, changelog updated, backup taken
- [ ] **WaaS Site Deployment** — using Panopticon for updates; manual SFTP fallback (reference `docs/deployment/sftp.md`)
- [ ] **CRM Module Deployment** — Dolibarr module update steps; compatibility verification
- [ ] **MokoStandards Bulk Sync** — deploying governance changes via `bulk_sync.php`; reference `docs/guide/bulk-repository-updates.md`
- [ ] **Rollback Procedures** — how to roll back each deployment type
- [ ] **Post-Deployment Verification** — smoke tests per deployment type

### Acceptance Criteria
- [ ] File created at `docs/guide/operations/deployment-guide.md`
- [ ] Covers all three deployment types
- [ ] Cross-references `docs/guide/bulk-repository-updates.md` and `docs/deployment/sftp.md`
- [ ] `docs/guide/operations/index.md` updated'

echo ""
echo "✅ All 39 documentation gap issues created successfully."
echo "Repository: $REPO"
