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
DEFGROUP: MokoStandards.Documentation
INGROUP: MokoStandards.Architecture
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/guide/repository-split-plan.md
VERSION: 03.01.03
BRIEF: Architecture plan for splitting public and private repository content
-->

# Repository Split Plan: MokoStandards Public vs Private

## Overview

This document defines the recommended split between the public **mokoconsulting-tech/MokoStandards** repository and the private **mokoconsulting-tech/MokoStandards-github-private** repository to properly separate public coding standards from private organizational configurations.

## Objectives

1. **Security**: Keep sensitive organizational information private
2. **Open Source**: Maximize public sharing of coding standards
3. **Reusability**: Allow external organizations to adopt standards
4. **Governance**: Maintain strict internal controls privately
5. **Simplicity**: Clear separation of concerns

## Repository Scope Definition

### Public Repository: mokoconsulting-tech/MokoStandards

**Purpose**: Public coding standards, policies, and reference implementations

**Target Audience**:
- External developers adopting MokoStandards
- Open source community
- Potential clients evaluating standards
- Industry peers and partners

**Content Classification**: Public, open-source, shareable

### Private Repository: mokoconsulting-tech/MokoStandards-github-private

**Purpose**: Internal GitHub configurations and organizational templates

**Target Audience**:
- Moko Consulting internal teams only
- Repository administrators
- Project maintainers

**Content Classification**: Confidential, internal use only

---

## Detailed Content Split

### Keep in PUBLIC Repository (MokoStandards)

#### Root Level Files
```
✅ README.md - Public repository overview
✅ LICENSE.md - GPL-3.0-or-later license
✅ CHANGELOG.md - Public version history
✅ SECURITY.md - Public security policy
✅ CONTRIBUTING.md - Public contribution guidelines
✅ CODE_OF_CONDUCT.md - Public code of conduct
✅ SUPPORT.md - Public support channels
✅ GOVERNANCE.md - Public governance model
✅ .gitignore - Standard Git ignore patterns
✅ .gitattributes - Standard Git attributes
✅ .editorconfig - Standard editor configuration
✅ .gitmessage - Commit message template
✅ .git-blame-ignore-revs - Blame ignore list
```

#### .github/ Directory
```
✅ .github/workflows/ - Public CI/CD workflows
   ✅ ci.yml - Public CI checks
   ✅ codeql-analysis.yml - Security scanning
   ✅ rebuild_docs_indexes.yml - Documentation automation
   ✅ repo_health.yml - Repository health checks

✅ templates/workflows/ - Reusable workflow templates (moved from .github/)
   ✅ joomla/ - Joomla-specific workflows
   ✅ generic/ - Platform-agnostic workflows
   ✅ README.md - Template documentation

✅ .github/dependabot.yml - Dependency scanning config
✅ .github/settings.yml - Repository settings template (anonymized)

❌ .github/CODEOWNERS - MOVE TO PRIVATE (contains internal team structure)
❌ .github/ISSUE_TEMPLATE/ - MOVE TO PRIVATE (internal issue workflows)
❌ .github/PULL_REQUEST_TEMPLATE.md - MOVE TO PRIVATE (internal PR checklist)
```

#### Documentation (docs/)
```
✅ docs/policy/ - All public policies
   ✅ document-formatting.md
   ✅ change-management.md
   ✅ risk-register.md
   ✅ data-classification.md
   ✅ vendor-risk.md
   ✅ security-scanning.md
   ✅ dependency-management.md
   ✅ merge-strategy.md
   ✅ documentation-governance.md

✅ docs/guide/ - All public guides
   ✅ audit-readiness.md
   ✅ conflict-resolution.md
   ✅ project-fields.md
   ✅ project-views.md
   ✅ repository-split-plan.md (this document)

✅ docs/checklist/ - Public checklists
   ✅ release.md

✅ docs/ROADMAP.md - Public roadmap
✅ docs/index.md - Documentation index
✅ docs/README.md - Documentation overview

❌ docs/policy/copilot-prompt-projectv2-joomla-template.md - MOVE TO PRIVATE (internal AI prompts)
❌ docs/guide/waas/ - EVALUATE (may contain client-specific information)
❌ docs/policy/waas/ - EVALUATE (may contain proprietary WaaS implementation details)
```

#### Templates (templates/)
```
✅ templates/docs/ - Public documentation templates
   ✅ required/ - Required document templates
   ✅ extra/ - Optional document templates

✅ templates/repos/ - Public repository structure templates
   ✅ joomla/ - Joomla extension templates
   ✅ generic/ - Generic project templates

✅ templates/scripts/ - Public validation scripts
   ✅ validate/ - Various validation scripts

❌ templates/.github/ - ALREADY REMOVED (consolidated to main .github/)
```

#### Scripts (scripts/)
```
✅ scripts/validate/ - Public validation scripts
✅ scripts/setup/ - Public setup scripts
✅ scripts/README.md - Public script documentation

❌ scripts/*project*.py - EVALUATE (may contain internal GitHub PAT usage)
   Consider: Keep if generalized, move if specific to internal projects
```

---

### Move to PRIVATE Repository (MokoStandards-github-private)

#### Recommended Structure
```
mokoconsulting-tech/MokoStandards-github-private/
├── README.md (private repo overview)
├── CODEOWNERS (internal team assignments)
├── .github/
│   └── workflows/
│       └── sync-to-repos.yml (automation to deploy templates)
├── issue-templates/
│   ├── adr.md
│   ├── bug_report.md
│   ├── deployment_plan.md
│   ├── documentation_change.md
│   ├── escalation.md
│   ├── feature_request.md
│   ├── incident_report.md
│   ├── migration_plan.md
│   ├── risk_register_entry.md
│   ├── runbook.md
│   └── security_review.md
├── pull-request-templates/
│   └── pull_request_template.md
├── project-automation/
│   ├── project_field_definitions.json
│   ├── project_view_definitions.json
│   └── automation_rules.yml
├── internal-policies/
│   ├── client-engagement.md
│   ├── internal-communication.md
│   ├── waas-pricing.md
│   └── staff-onboarding.md
├── copilot-prompts/
│   ├── projectv2-joomla-template.md
│   └── standards-enforcement.md
└── scripts/
    ├── setup_project_v2.py
    ├── populate_project_from_scan.py
    └── sync_private_templates.sh
```

#### Content to Move

**GitHub Templates**:
```
❌ .github/CODEOWNERS
   Reason: Exposes internal team structure and email addresses

❌ .github/ISSUE_TEMPLATE/*.md
   Reason: Internal workflow processes, client references, internal tools
   Files:
   - adr.md
   - bug_report.md
   - deployment_plan.md
   - documentation_change.md
   - escalation.md
   - feature_request.md
   - incident_report.md
   - migration_plan.md
   - risk_register_entry.md
   - runbook.md
   - security_review.md

❌ .github/PULL_REQUEST_TEMPLATE.md
   Reason: Internal checklist with references to internal systems
```

**Internal Documentation**:
```
❌ docs/policy/copilot-prompt-projectv2-joomla-template.md
   Reason: Proprietary AI prompt engineering for internal use

❌ docs/guide/waas/* (if contains client-specific details)
   Evaluate each file:
   - Keep: Generic architecture patterns
   - Move: Client lists, pricing, SLAs, internal processes

❌ docs/policy/waas/* (if contains proprietary implementation)
   Evaluate each file:
   - Keep: Security standards that could be public
   - Move: Proprietary provisioning processes, internal tooling
```

**Project Management**:
```
❌ scripts/setup_project_v2.py
   Reason: Uses internal GitHub PAT, references internal projects

❌ scripts/populate_project_from_scan.py
   Reason: Specific to internal Project #7 structure

❌ scripts/ensure_docs_and_project_tasks.py
   Reason: Internal task management automation

❌ scripts/setup_project_views.py
   Reason: Internal project view configurations
```

**Internal Implementation Details**:
```
❌ IMPLEMENTATION_SUMMARY.md
   Reason: Documents internal project setup process
   Alternative: Generalize and keep if valuable for public adoption

❌ MERGE_SUMMARY.md
   Reason: Internal merge process documentation

❌ CONFLICT_RESOLUTION_GUIDE.md
   Reason: Contains internal team communication details
   Alternative: Generalize to public guide without internal references
```

---

## Implementation Plan

### Phase 1: Create Private Repository

**Tasks**:
1. Create new repository: `mokoconsulting-tech/MokoStandards-github-private`
2. Set visibility: Private
3. Initialize with basic structure
4. Add CODEOWNERS with internal team members
5. Grant access to Moko Consulting organization members only

**Timeline**: 1 day

### Phase 2: Move Sensitive Content

**Tasks**:
1. Copy CODEOWNERS to private repo
2. Copy all issue templates to private repo under `issue-templates/`
3. Copy pull request template to private repo under `pull-request-templates/`
4. Copy internal automation scripts to private repo under `scripts/`
5. Move internal-only documentation to private repo under `internal-policies/`
6. Move AI prompts to private repo under `copilot-prompts/`

**Timeline**: 2 days

### Phase 3: Clean Public Repository

**Tasks**:
1. Remove CODEOWNERS from public .github/
2. Remove ISSUE_TEMPLATE/ directory from public .github/
3. Remove PULL_REQUEST_TEMPLATE.md from public .github/
4. Remove internal automation scripts from public scripts/
5. Update references in public documentation
6. Update README to reference private repo for internal use

**Timeline**: 1 day

### Phase 4: Update Documentation

**Tasks**:
1. Update public README with private repo reference
2. Create cross-reference guide for internal users
3. Update GOVERNANCE.md to clarify public/private split
4. Add section to CONTRIBUTING.md about internal vs public contributions
5. Document in .github/README.md that private templates are separate

**Timeline**: 1 day

### Phase 5: Test and Validate

**Tasks**:
1. Verify public repo contains no sensitive information
2. Verify private repo access controls are correct
3. Test that issue templates work from private repo
4. Update any automation that references moved files
5. Validate documentation links

**Timeline**: 2 days

---

## Usage After Split

### For Internal Moko Consulting Teams

**Public Repository Use**:
- Reference coding standards
- Adopt workflow templates
- Contribute to public standards
- Report issues with standards

**Private Repository Use**:
- Use issue templates for internal projects
- Access CODEOWNERS for team assignments
- Reference internal policies and procedures
- Use project automation scripts

**Workflow**:
1. Clone both repositories for internal projects
2. Apply standards from public repo
3. Use templates from private repo
4. Reference both in internal documentation

### For External Users

**Public Repository Use**:
- Adopt MokoStandards for own projects
- Fork and customize standards
- Contribute improvements via pull requests
- Reference in own documentation

**No Access Required to Private Repository**:
- Create own issue templates based on needs
- Create own CODEOWNERS for own organization
- Implement own project automation

---

## Cross-Repository References

### In Public README.md

Add section:
```markdown
## For Moko Consulting Internal Use

Internal teams should also reference the private repository for:
- GitHub issue and PR templates
- Project automation scripts
- Internal policies and procedures
- Copilot prompts and AI tooling

Repository: `mokoconsulting-tech/MokoStandards-github-private` (internal access only)
```

### In Private README.md

Add section:
```markdown
# MokoStandards GitHub Private

This repository contains internal GitHub configurations and organizational
templates for Moko Consulting. It complements the public MokoStandards
repository which contains our public coding standards.

## Public Standards
Coding standards, policies, and reference implementations are maintained in:
https://github.com/mokoconsulting-tech/MokoStandards

## This Repository Contains
- GitHub issue and pull request templates
- CODEOWNERS file with internal team assignments
- Project automation scripts
- Internal-only policies and procedures
- Copilot prompts and AI tooling
```

---

## Security Considerations

### Public Repository Security

**What to Keep**:
- Generic security policies
- Public security disclosure process
- CodeQL and scanning configurations
- Dependabot configurations

**What to Remove**:
- Internal team email addresses
- Internal project references
- Client names or identifying information
- Proprietary processes or implementations

### Private Repository Security

**Access Control**:
- Grant access only to Moko Consulting organization members
- Use GitHub teams for granular permissions
- Regular access audits
- Offboarding process to revoke access

**Content Classification**:
- CONFIDENTIAL: All content in private repo
- No secrets or credentials in either repo
- Use GitHub Secrets for automation credentials
- Document classification in each file header

---

## WaaS Documentation Decision

### Recommendation: Hybrid Approach

**Keep in Public** (docs/guide/waas/):
```
✅ waas-architecture.md (if generalized)
   - Generic multi-tenant architecture patterns
   - Security best practices
   - Technology stack overview (no proprietary details)
```

**Move to Private** (internal-policies/waas/):
```
❌ waas-operations.md (if contains client specifics)
   - Client onboarding procedures
   - Billing and provisioning details
   - Internal tooling and automation

❌ waas-client-onboarding.md
   - Specific to Moko Consulting clients
   - Contains proprietary processes

❌ waas-pricing.md (if exists)
   - Pricing models
   - Service tiers
   - Client agreements
```

**Keep in Public** (docs/policy/waas/):
```
✅ waas-security.md (if generalized)
   - Security requirements that could benefit industry
   - No proprietary implementation details

❓ waas-provisioning.md (evaluate)
   - Keep: Generic provisioning standards
   - Move: Proprietary automation and internal tools

❓ waas-tenant-isolation.md (evaluate)
   - Keep: Security isolation standards
   - Move: Implementation specifics
```

### WaaS Decision Matrix

| Document | Public | Private | Reason |
|----------|--------|---------|--------|
| Architecture patterns | ✅ | ❌ | Industry best practices, shareable |
| Security standards | ✅ | ❌ | Demonstrates security rigor |
| Client onboarding | ❌ | ✅ | Proprietary process |
| Provisioning automation | ❌ | ✅ | Internal tooling |
| Operations runbooks | ❌ | ✅ | Client-specific procedures |
| Pricing and SLAs | ❌ | ✅ | Commercial information |

---

## Maintenance and Governance

### Public Repository Governance

**Maintainers**:
- Public-facing team members
- Open to community contributions

**Review Process**:
- Public pull requests reviewed by maintainers
- Security review for policy changes
- Community feedback encouraged

**Release Cycle**:
- Regular updates with semantic versioning
- Public changelog
- GitHub releases with notes

### Private Repository Governance

**Maintainers**:
- Internal operations team
- Repository administrators only

**Review Process**:
- Internal-only pull requests
- Security Owner approval for sensitive changes
- No external contributions

**Sync Process**:
- Private repo changes pushed to consuming projects
- Automation to deploy templates
- Version control aligned with public repo

---

## Migration Checklist

### Pre-Migration
- [ ] Review all files for sensitive information
- [ ] Identify all cross-references between files
- [ ] Document current internal workflows using templates
- [ ] Backup current repository state

### During Migration
- [ ] Create private repository with proper access controls
- [ ] Move CODEOWNERS to private repo
- [ ] Move issue templates to private repo
- [ ] Move PR templates to private repo
- [ ] Move internal scripts to private repo
- [ ] Move internal documentation to private repo
- [ ] Update all file references
- [ ] Update README files in both repos

### Post-Migration
- [ ] Remove sensitive files from public repo history (if needed)
- [ ] Verify public repo has no sensitive information
- [ ] Test issue template usage from private repo
- [ ] Test automation scripts in private repo
- [ ] Update team documentation with new structure
- [ ] Communicate changes to all internal teams
- [ ] Update onboarding documentation

---

## Risks and Mitigations

### Risk: Accidental Public Exposure

**Mitigation**:
- Review all content before moving to public
- Use `.gitignore` patterns for sensitive files
- Enable secret scanning on public repo
- Regular audits of public repo content

### Risk: Broken References

**Mitigation**:
- Document all cross-references
- Update references during migration
- Test all links after migration
- Use relative paths where possible

### Risk: Workflow Disruption

**Mitigation**:
- Communicate changes in advance
- Provide transition documentation
- Maintain parallel access during transition
- Have rollback plan ready

### Risk: Access Management Complexity

**Mitigation**:
- Clear documentation of which repo for what
- Onboarding checklist updated
- Regular access reviews
- Automated notifications for access changes

---

## Success Criteria

### Public Repository
- [ ] Contains only publicly shareable content
- [ ] No internal team information exposed
- [ ] No client-specific information
- [ ] All standards and policies are generic and reusable
- [ ] External users can adopt standards without internal context

### Private Repository
- [ ] Contains all internal GitHub configurations
- [ ] Access limited to Moko Consulting organization
- [ ] All sensitive information protected
- [ ] Issue and PR templates functional
- [ ] Automation scripts operational

### Overall
- [ ] Clear separation of public and private content
- [ ] No broken links between repositories
- [ ] Internal teams can access both repos easily
- [ ] External users can use public repo independently
- [ ] Documentation clearly explains the split

---

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Guide                                       |
| Domain         | Documentation                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/guide/repository-split-plan.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
