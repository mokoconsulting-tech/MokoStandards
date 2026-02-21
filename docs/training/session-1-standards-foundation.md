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
DEFGROUP: MokoStandards.Training
INGROUP: MokoStandards.Documentation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: docs/training/session-0-standards-foundation.md
VERSION: 04.00.03
BRIEF: Session 0 - Standards Foundation prerequisite training materials
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.03-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Session 0: Standards Foundation (Prerequisite)

**Duration**: 2 hours  
**Format**: Self-paced + Instructor Overview  
**Prerequisite**: None (foundational session)

---

## Session Objectives

By the end of this session, you will:
- ✅ Understand the complete MokoStandards policy framework (31 documents)
- ✅ Navigate the repository structure and locate standards efficiently
- ✅ Identify which standards apply to different development scenarios
- ✅ Understand compliance requirements and quality assurance principles
- ✅ Use the standards documentation effectively in daily work

---

## Agenda

| Time | Topic | Format |
|------|-------|--------|
| 0:00-0:30 | MokoStandards Overview & Repository Structure | Presentation |
| 0:30-1:00 | Standards Categories & Key Policies Review | Guided Tour |
| 1:00-1:30 | Standards Lookup & Application Exercises | Hands-on |
| 1:30-2:00 | Compliance Overview & Knowledge Check | Interactive |

---

## Part 1: MokoStandards Overview (30 minutes)

### What is MokoStandards?

MokoStandards is a comprehensive enterprise development framework that provides:
- ✅ **31 Policy Documents**: Complete governance and standards coverage
- ✅ **13 PHP Enterprise Libraries**: Production-ready reusable components
- ✅ **Standard Templates**: GitHub workflows, documentation, security files
- ✅ **Automation Scripts**: Repository management and compliance tools
- ✅ **Quality Assurance Framework**: Testing, scanning, and validation tools

### Repository Structure Overview

```
MokoStandards/
├── docs/                          # All documentation
│   ├── policy/                    # 31 policy documents (PRIMARY FOCUS)
│   │   ├── *.md                   # 31 top-level policy files
│   │   ├── security/              # Security-specific policies (10 files)
│   │   ├── quality/               # Quality assurance policies (3 files)
│   │   ├── governance/            # Governance policies
│   │   ├── operations/            # Operations policies
│   │   ├── legal/                 # Legal compliance
│   │   └── crm/waas/              # Specialized policies
│   ├── guide/                     # Implementation guides
│   ├── training/                  # Training materials (this file!)
│   ├── automation/                # Automation documentation
│   └── workflows/                 # Workflow documentation
├── src/Enterprise/                # 13 PHP enterprise libraries
├── templates/                     # Standard templates
│   ├── github/                    # GitHub templates (issues, PRs)
│   ├── docs/                      # Documentation templates
│   ├── workflows/                 # GitHub Actions workflows
│   └── security/                  # Security templates
├── scripts/                       # Automation scripts
└── tests/                         # Test suite

Total Documents: 221 markdown files
Core Policies: 31 policy documents in docs/policy/
```

### Why Standards Matter

**Consistency**: 
- All projects follow the same patterns
- Reduces learning curve when switching projects
- Enables code reuse and knowledge sharing

**Quality**:
- Enforces best practices automatically
- Catches issues early through automated checks
- Ensures enterprise-grade reliability

**Compliance**:
- Meets audit requirements
- Tracks all changes with proper governance
- Provides compliance evidence

**Efficiency**:
- Reduces decision fatigue
- Accelerates onboarding
- Enables faster code reviews

---

## Part 2: Standards Categories (30 minutes)

### The 31 Core Policy Documents

MokoStandards policies are organized into 6 major categories:

#### 1. **Code Standards** (7 policies)

| Policy | File | Purpose |
|--------|------|---------|
| Coding Style Guide | `coding-style-guide.md` | Universal coding conventions |
| Code Review Guidelines | `code-review-guidelines.md` | Review process and checklist |
| Scripting Standards | `scripting-standards.md` | Automation script requirements |
| File Header Standards | `file-header-standards.md` | Copyright and metadata headers |
| File Headers | `file-headers.md` | Header format specifications |
| Copilot Usage Policy | `copilot-usage-policy.md` | AI-assisted development rules |
| Copilot Pre-Merge Checklist | `copilot-pre-merge-checklist.md` | AI code review checklist |

**When to use**: Writing code, creating scripts, using AI tools, performing code reviews

#### 2. **Documentation Standards** (8 policies)

| Policy | File | Purpose |
|--------|------|---------|
| Documentation Governance | `documentation-governance.md` | Documentation management |
| Document Formatting | `document-formatting.md` | Markdown formatting standards |
| Changelog Standards | `changelog-standards.md` | Change documentation format |
| Roadmap Standards | `roadmap-standards.md` | Feature planning documentation |
| Metadata Standards | `metadata-standards.md` | File metadata requirements |
| Terraform Metadata Standards | `terraform-metadata-standards.md` | Infrastructure metadata |
| Directory Index Requirements | `directory-index-requirements.md` | Index file standards |
| Planning Guidance | `planning-guidance.md` | Project planning standards |

**When to use**: Writing documentation, updating changelogs, planning features, creating indexes

#### 3. **Security & Compliance** (11 policies)

| Policy | File | Purpose |
|--------|------|---------|
| Security Scanning | `security-scanning.md` | Security scan requirements |
| Data Classification | `data-classification.md` | Data handling standards |
| License Compliance | `license-compliance.md` | Open source licensing |
| Vendor Risk | `vendor-risk.md` | Third-party risk management |
| Risk Register | `risk-register.md` | Risk tracking and mitigation |
| **security/** subdirectory (10 additional policies) |  |  |
| ├─ Access Control & Identity | `security/access-control-identity-management.md` | Authentication/authorization |
| ├─ Audit Logging | `security/audit-logging-monitoring.md` | Logging requirements |
| ├─ Backup & Recovery | `security/backup-recovery.md` | Data backup standards |
| ├─ Confidentiality Scan | `security/confidentiality-scan.md` | Sensitive data detection |
| ├─ Data Privacy (GDPR) | `security/data-privacy-gdpr-compliance.md` | Privacy compliance |
| ├─ Directory Listing Prevention | `security/directory-listing-prevention.md` | Web security |
| ├─ Disaster Recovery | `security/disaster-recovery-business-continuity.md` | Business continuity |
| ├─ Encryption Standards | `security/encryption-standards.md` | Cryptography requirements |
| ├─ Vulnerability Management | `security/vulnerability-management.md` | Vulnerability handling |

**When to use**: Security reviews, handling sensitive data, compliance audits, risk assessments

#### 4. **Workflow & Repository Standards** (4 policies)

| Policy | File | Purpose |
|--------|------|---------|
| Workflow Standards | `workflow-standards.md` | GitHub Actions workflow standards |
| Branching Strategy | `branching-strategy.md` | Git branching model |
| Merge Strategy | `merge-strategy.md` | Pull request and merge process |
| Change Management | `change-management.md` | Change control process |

**When to use**: Creating workflows, managing branches, merging code, implementing changes

#### 5. **Quality Assurance** (4 policies)

| Policy | File | Purpose |
|--------|------|---------|
| Health Scoring | `health-scoring.md` | Repository health metrics |
| **quality/** subdirectory (3 additional policies) |  |  |
| ├─ Quality Gates | `quality/quality-gates.md` | Quality checkpoints |
| ├─ Technical Debt Management | `quality/technical-debt-management.md` | Debt tracking |
| ├─ Testing Strategy | `quality/testing-strategy-standards.md` | Testing requirements |

**When to use**: Setting up CI/CD, implementing tests, managing technical debt, quality reviews

#### 6. **Architecture & Governance** (7 policies)

| Policy | File | Purpose |
|--------|------|---------|
| Governance | `GOVERNANCE.md` | Overall governance framework |
| Core Structure | `core-structure.md` | Repository structure standards |
| Two-Tier Architecture | `two-tier-architecture.md` | Architecture model |
| Dependency Management | `dependency-management.md` | Dependency standards |
| Roadmap | `roadmap.md` | Product roadmap |
| **governance/** subdirectory | Additional governance policies |  |
| **operations/** subdirectory | Operational procedures |  |

**When to use**: Architecture decisions, dependency updates, governance reviews, strategic planning

### Quick Reference: Standards by Activity

| Activity | Required Standards | Priority |
|----------|-------------------|----------|
| **Writing Code** | Coding Style Guide, File Header Standards, Scripting Standards | CRITICAL |
| **Code Review** | Code Review Guidelines, Copilot Pre-Merge Checklist | CRITICAL |
| **Documentation** | Document Formatting, Changelog Standards, Directory Index Requirements | HIGH |
| **Security Review** | Security Scanning, Data Classification, All security/* policies | CRITICAL |
| **Creating PR** | Merge Strategy, Branching Strategy, Change Management | HIGH |
| **New Feature** | Planning Guidance, Roadmap Standards, Quality Gates | MEDIUM |
| **Adding Dependency** | Dependency Management, License Compliance, Vendor Risk | HIGH |
| **Testing** | Testing Strategy, Quality Gates | HIGH |
| **GitHub Actions** | Workflow Standards, Scripting Standards | MEDIUM |
| **Architecture Decision** | Two-Tier Architecture, Core Structure, Governance | HIGH |

---

## Part 3: Standards Lookup & Application (30 minutes)

### Exercise 1: Finding the Right Standard

For each scenario, identify which policy document(s) to consult:

1. **Scenario**: You need to add a new Python automation script to the repository.
   - **Answer**: `scripting-standards.md`, `file-header-standards.md`, `coding-style-guide.md`
   - **Location**: `docs/policy/`

2. **Scenario**: You're reviewing a pull request that adds a new external library.
   - **Answer**: `dependency-management.md`, `license-compliance.md`, `vendor-risk.md`, `code-review-guidelines.md`
   - **Location**: `docs/policy/`

3. **Scenario**: You need to add logging for sensitive data access.
   - **Answer**: `data-classification.md`, `security/audit-logging-monitoring.md`, `security/data-privacy-gdpr-compliance.md`
   - **Location**: `docs/policy/` and `docs/policy/security/`

4. **Scenario**: Your GitHub Actions workflow needs to pass quality checks.
   - **Answer**: `workflow-standards.md`, `quality/quality-gates.md`, `quality/testing-strategy-standards.md`
   - **Location**: `docs/policy/` and `docs/policy/quality/`

5. **Scenario**: You're documenting a new feature in the changelog.
   - **Answer**: `changelog-standards.md`, `document-formatting.md`
   - **Location**: `docs/policy/`

### Exercise 2: Standards Application

**Task**: Create a standards compliance checklist for a new PHP script that processes user data.

**Your Checklist Should Include**:

- [ ] File header with copyright notice (`file-header-standards.md`)
- [ ] Follows PHP coding style (`coding-style-guide.md`)
- [ ] Uses strict types declaration (`scripting-standards.md`)
- [ ] Implements data classification tagging (`data-classification.md`)
- [ ] Includes audit logging (`security/audit-logging-monitoring.md`)
- [ ] Validates and sanitizes inputs (`coding-style-guide.md`)
- [ ] Has error handling and recovery (`scripting-standards.md`)
- [ ] Includes unit tests (`quality/testing-strategy-standards.md`)
- [ ] Documents sensitive data handling (`security/data-privacy-gdpr-compliance.md`)
- [ ] Meets quality gates (`quality/quality-gates.md`)

### Exercise 3: Policy Navigation

Practice navigating the policy structure:

```bash
# Navigate to policy directory
cd docs/policy/

# List all top-level policies (31 files)
ls -1 *.md

# View security policies
ls -1 security/*.md

# View quality policies
ls -1 quality/*.md

# Search for specific policy content
grep -r "audit log" *.md

# View the policy index
cat index.md
```

**Practice Questions**:
1. How many policies are in the `security/` subdirectory? **Answer: 10**
2. Which policy covers GitHub Actions workflows? **Answer: workflow-standards.md**
3. Where do you find encryption requirements? **Answer: security/encryption-standards.md**
4. Which policy defines quality checkpoints? **Answer: quality/quality-gates.md**

---

## Part 4: Compliance Requirements (30 minutes)

### Understanding Compliance

**Compliance** in MokoStandards means:
- Following all applicable policies for your work
- Documenting decisions and changes
- Passing automated quality gates
- Meeting security requirements
- Maintaining audit trails

### Quality Assurance Principles

#### 1. **Prevention Over Detection**
- Use standards to prevent issues before they occur
- Automated checks in CI/CD catch problems early
- Code reviews enforce standards consistently

#### 2. **Continuous Compliance**
- Compliance is not a one-time check
- Every commit should meet standards
- Regular audits validate ongoing compliance

#### 3. **Documentation as Evidence**
- Well-documented code proves compliance
- Audit logs provide compliance trails
- Change logs track all modifications

#### 4. **Automated Enforcement**
- Linters enforce coding standards
- Security scanners detect vulnerabilities
- Quality gates prevent non-compliant merges

### Compliance Workflow

```
┌─────────────────┐
│  Start Work     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Review         │
│  Applicable     │
│  Standards      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Develop        │
│  Following      │
│  Standards      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Self-Review    │
│  Against        │
│  Checklist      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Automated      │
│  Checks Pass    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Peer Review    │
│  Validates      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Merge &        │
│  Document       │
└─────────────────┘
```

### Automated Compliance Checks

MokoStandards includes automated checks:

1. **Code Quality**:
   - PHPStan (static analysis)
   - Psalm (type checking)
   - PHPCS (code style)

2. **Security**:
   - Confidentiality scanning (secrets detection)
   - Directory listing prevention
   - Security vulnerability scanning

3. **Documentation**:
   - File header validation
   - Changelog format checking
   - Index file generation

4. **Testing**:
   - PHPUnit integration tests
   - Code coverage requirements
   - Quality gate enforcement

### Key Compliance Documents

These policies are CRITICAL for compliance:

1. **GOVERNANCE.md** - Overall governance framework
2. **code-review-guidelines.md** - Review requirements
3. **security-scanning.md** - Security validation
4. **quality/quality-gates.md** - Quality requirements
5. **change-management.md** - Change control

**Must Read First**: Start with these 5 policies to understand compliance basics.

---

## Knowledge Check Quiz

Test your understanding of MokoStandards:

### Question 1: Policy Count
How many top-level policy documents are in the `docs/policy/` directory?
- A) 25
- B) 31 ✅
- C) 40
- D) 50

### Question 2: Security Policies
Where are the detailed security policies located?
- A) docs/security/
- B) docs/policy/security/ ✅
- C) security/policy/
- D) templates/security/

### Question 3: Code Review
Which policy document defines the code review process?
- A) coding-style-guide.md
- B) code-review-guidelines.md ✅
- C) merge-strategy.md
- D) quality-gates.md

### Question 4: File Headers
What must every code file include according to standards?
- A) Author name only
- B) Date created only
- C) Copyright notice and metadata ✅
- D) Nothing required

### Question 5: Standards Application
You're adding a new GitHub Actions workflow. Which standards apply? (Select all)
- A) workflow-standards.md ✅
- B) scripting-standards.md ✅
- C) file-header-standards.md ✅
- D) changelog-standards.md ✅
- E) All of the above ✅

### Question 6: Compliance
When should you check applicable standards?
- A) After code is written
- B) During code review
- C) Before starting work ✅
- D) Only if asked

### Question 7: Quality Gates
Which subdirectory contains quality assurance policies?
- A) docs/qa/
- B) docs/policy/quality/ ✅
- C) quality/docs/
- D) docs/testing/

### Question 8: Data Handling
You're processing user personal information. Which policies must you review? (Select all)
- A) data-classification.md ✅
- B) security/data-privacy-gdpr-compliance.md ✅
- C) security/encryption-standards.md ✅
- D) coding-style-guide.md
- E) A, B, C ✅

### Question 9: Architecture
Which policy defines repository structure standards?
- A) core-structure.md ✅
- B) GOVERNANCE.md
- C) two-tier-architecture.md
- D) directory-index-requirements.md

### Question 10: Repository Navigation
What's the total number of markdown documentation files in MokoStandards?
- A) 100
- B) 150
- C) 221 ✅
- D) 300

**Passing Score**: 8/10 (80%)

---

## Quick Reference Guide

### Essential Commands

```bash
# Clone the repository
git clone https://github.com/mokoconsulting-tech/MokoStandards.git
cd MokoStandards

# Find a specific policy
find docs/policy -name "*security*"

# Search policy content
grep -r "audit" docs/policy/

# List all policies
ls -1 docs/policy/*.md

# View policy index
cat docs/policy/index.md

# Count policies
ls -1 docs/policy/*.md | wc -l  # Should show 31
```

### Policy Quick Access

| Need | Policy | Path |
|------|--------|------|
| Coding standards | Coding Style Guide | `docs/policy/coding-style-guide.md` |
| Code review | Code Review Guidelines | `docs/policy/code-review-guidelines.md` |
| Security | Security Scanning + security/* | `docs/policy/security-scanning.md` |
| Documentation | Document Formatting | `docs/policy/document-formatting.md` |
| Workflows | Workflow Standards | `docs/policy/workflow-standards.md` |
| Quality | Quality Gates | `docs/policy/quality/quality-gates.md` |
| Testing | Testing Strategy | `docs/policy/quality/testing-strategy-standards.md` |
| Git workflow | Branching + Merge Strategy | `docs/policy/branching-strategy.md` |
| Governance | Governance | `docs/policy/GOVERNANCE.md` |
| Architecture | Core Structure | `docs/policy/core-structure.md` |

### When to Consult Standards

- ✅ **Before starting new work** - Identify applicable standards
- ✅ **During development** - Follow standards continuously
- ✅ **Before committing** - Self-review against checklist
- ✅ **During code review** - Validate compliance
- ✅ **When unsure** - Consult policy documents
- ✅ **For architecture decisions** - Review governance policies

---

## Next Steps

After completing Session 0, you're ready for:

1. **Session 1**: [Enterprise Libraries Overview](session-1-libraries-overview.md)
   - Learn about the 13 PHP enterprise libraries
   - See how libraries implement these standards

2. **Session 2**: [Integration Workshop](session-2-integration-workshop.md)
   - Apply standards in practical scenarios
   - Build compliant automation scripts

3. **Session 3**: [Advanced Features](session-3-advanced-features.md)
   - Advanced compliance patterns
   - Enterprise security best practices

4. **Session 4**: [Standards Compliance (Capstone)](session-4-standards-compliance.md)
   - Complete policy deep dive
   - Real-world compliance scenarios
   - Certificate of completion

---

## Additional Resources

### Documentation
- **[Policy Directory](../policy/index.md)**: All 31 policy documents
- **[Security Policies](../policy/security/index.md)**: Security-specific standards
- **[Quality Policies](../policy/quality/index.md)**: Quality assurance standards
- **[Governance](../policy/GOVERNANCE.md)**: Overall governance framework

### Tools
- **[Automation Scripts](../../scripts/)**: Compliance automation tools
- **[Templates](../../templates/)**: Standard templates
- **[Enterprise Libraries](../../src/Enterprise/)**: PHP libraries implementing standards

### Support
- **GitHub Issues**: Report standards questions or issues
- **Pull Requests**: Suggest standards improvements
- **Documentation**: [docs/](../)

---

## Summary

You've completed the MokoStandards Foundation session! You should now:

✅ Understand the 31-policy framework  
✅ Navigate the repository structure  
✅ Identify applicable standards for different scenarios  
✅ Understand compliance requirements  
✅ Use the quick reference guide  

**Certification Requirement**: This session is a prerequisite for MokoStandards Certification.

---

**Ready for technical training?** → Continue with [Session 1: Enterprise Libraries Overview](session-1-libraries-overview.md)
