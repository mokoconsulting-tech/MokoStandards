# Layered Documentation Guide

## Purpose

This guide explains the layered documentation framework used in MokoStandards. It defines the hierarchy of documentation requirements, from mandatory baseline documentation to optional enhancement documentation, helping teams understand what documentation is required versus recommended for their repositories.

## Scope

This guide applies to:

- All repositories governed by MokoStandards
- Documentation planning and compliance
- New repository setup
- Documentation audits and reviews
- Repository health scoring

This guide does not apply to:

- Code comments and inline documentation
- Third-party documentation
- Temporary or draft documentation

## Overview

MokoStandards uses a **layered documentation approach** that organizes documentation into tiers based on requirement level and purpose. This approach ensures baseline compliance while allowing flexibility for additional documentation based on project needs.

## Documentation Layers by Repository Type

### Layer 1: Required Documentation (Mandatory)

**Location:** `/templates/docs/required/`

**Purpose:** Establishes baseline documentation compliance for all repositories.

**Compliance:** Mandatory for all repositories. Non-compliance blocks production deployment.

#### Required Files for All Repository Types

These files are **REQUIRED** for all repositories regardless of type:

| File | Purpose | Template Location |
|------|---------|------------------|
| **README.md** | Repository overview and entry point | `/templates/docs/required/template-README.md` |
| **LICENSE** | License terms (GPL-3.0-or-later) | `/templates/licenses/GPL-3.0` |
| **CHANGELOG.md** | Change tracking and release history | `/templates/docs/required/template-CHANGELOG.md` |
| **CONTRIBUTING.md** | Contribution guidelines and workflow | `/templates/docs/required/template-CONTRIBUTING.md` |
| **SECURITY.md** | Security vulnerability reporting | `/templates/docs/required/template-SECURITY.md` |
| **.gitignore** | Git ignore patterns | Platform-specific templates |
| **.gitattributes** | Git attributes configuration | Copy from MokoStandards |
| **.editorconfig** | Editor configuration | Copy from MokoStandards |

**README.md Requirements:**
- Purpose and scope
- Installation instructions
- Usage examples
- License information
- Contact information

**CHANGELOG.md Requirements:**
- Versioned change history
- Release notes
- Breaking changes
- Migration guidance

**CONTRIBUTING.md Requirements:**
- How to contribute
- Code standards
- Pull request process
- Testing requirements
- Code of conduct reference

**LICENSE Requirements:**
- License text (GPL-3.0-or-later)
- Copyright information
- Redistribution terms
- Warranty disclaimers
- **Note:** LICENSE file must NOT have an extension (use `LICENSE`, not `LICENSE.md` or `LICENSE.txt`)

**SECURITY.md Requirements:**
- Supported versions
- Reporting process
- Response timeline
- Security best practices

#### Additional Required Files by Repository Type

**Joomla Repositories (WaaS Components):**

| File | Purpose | Required |
|------|---------|----------|
| **CODE_OF_CONDUCT.md** | Community code of conduct | ✅ Required |
| **Makefile** | Build automation using MokoStandards | ✅ Required |
| **site/controller.php** | Main site controller | ✅ Required |
| **site/manifest.xml** | Component manifest | ✅ Required |
| **admin/controller.php** | Main admin controller | ✅ Required |
| **language/** | Language translation files | ✅ Required |
| **docs/index.md** | Documentation index | ✅ Required |
| **scripts/** | Build and maintenance scripts | ✅ Required |
| **tests/unit/** | Unit tests directory | ✅ Required |

**Dolibarr Repositories (CRM Modules):**

| File | Purpose | Required |
|------|---------|----------|
| **Makefile** | Build automation using MokoStandards | ✅ Required |
| **src/README.md** | End-user documentation | ✅ Required |
| **src/core/modules/mod{ModuleName}.class.php** | Main module descriptor | ✅ Required |
| **src/core/** | Core module files | ✅ Required |
| **src/langs/** | Language translation files | ✅ Required |
| **docs/index.md** | Documentation index | ✅ Required |
| **scripts/** | Build and maintenance scripts | ✅ Required |
| **tests/unit/** | Unit tests directory | ✅ Required |

**Generic Repositories:**

| File | Purpose | Required |
|------|---------|----------|
| **CODE_OF_CONDUCT.md** | Community code of conduct | ✅ Required |
| **docs/** | Documentation directory | ✅ Required |
| **scripts/** | Build and automation scripts | ✅ Required |

**Enforcement:**

- Repository Health Scoring deducts points for missing required documentation
- CI/CD workflows validate presence of required files
- Compliance audits flag repositories lacking required documentation
- Production deployment blocked until required documentation present

**When to Use:**

- ✅ Creating any new repository
- ✅ Establishing baseline compliance
- ✅ Preparing for production deployment
- ✅ Meeting organizational standards
- ✅ Passing repository health checks

### Layer 2: Suggested Documentation (Recommended)

**Location:** `/templates/docs/extra/`

**Purpose:** Provides suggested documentation that enhances repository quality, improves collaboration, and supports specific use cases.

**Compliance:** Suggested but not mandatory. Improves repository health score.

#### Suggested Files for All Repository Types

| File | Purpose | Applies To | Priority |
|------|---------|------------|----------|
| **GOVERNANCE.md** | Project governance structure | Open source projects | Medium |
| **SUPPORT.md** | Support channels and resources | Public projects | Medium |
| **DEVELOPMENT.md** | Development environment setup | Projects with contributors | High |

**GOVERNANCE.md Contents:**
- Decision-making process
- Leadership roles
- Contribution tiers
- Voting procedures

**SUPPORT.md Contents:**
- Where to get help
- Community forums
- Commercial support options
- Documentation links

**DEVELOPMENT.md Contents:**
- Development prerequisites
- Local setup instructions
- Development workflow
- Testing procedures
- Debugging tips

#### Suggested Files by Repository Type

**Joomla Repositories (WaaS Components):**

| File/Directory | Purpose | Priority |
|----------------|---------|----------|
| **site/views/** | Site views directory | ✅ High |
| **admin/views/** | Admin views directory | ✅ High |
| **site/controllers/** | Site controllers | Suggested |
| **site/models/** | Site models | Suggested |
| **admin/controllers/** | Admin controllers | Suggested |
| **admin/models/** | Admin models | Suggested |
| **admin/sql/** | Database schema files | Suggested |
| **media/css/** | Stylesheets | Suggested |
| **media/js/** | JavaScript files | Suggested |
| **media/images/** | Image files | Suggested |
| **tests/integration/** | Integration tests | Suggested |
| **.github/workflows/** | GitHub Actions workflows | ✅ High |

**Dolibarr Repositories (CRM Modules):**

| File/Directory | Purpose | Priority |
|----------------|---------|----------|
| **src/sql/** | Database schema files | Suggested |
| **src/css/** | Stylesheets | Suggested |
| **src/js/** | JavaScript files | Suggested |
| **src/class/** | PHP class files | Suggested |
| **src/lib/** | Library files | Suggested |
| **templates/** | Code generation templates | Suggested |
| **tests/integration/** | Integration tests | Suggested |
| **.github/workflows/** | GitHub Actions workflows | ✅ High |

**Generic Repositories:**

| File/Directory | Purpose | Priority |
|----------------|---------|----------|
| **Makefile** | Build automation | Suggested |
| **src/** | Source code directory | Suggested |
| **tests/** | Test files directory | Suggested |
| **.github/workflows/** | GitHub Actions workflows | ✅ High |
| **.github/ISSUE_TEMPLATE/** | GitHub issue templates | Suggested |

### Layer 3: Optional Documentation (Enhancement)

**Purpose:** Provides optional documentation for specific contexts that may not apply to all projects.

**Compliance:** Optional. Adds capability but not required for baseline compliance.

#### Optional Files for All Repository Types

| File/Directory | Purpose | When to Use |
|----------------|---------|-------------|
| **API.md** | API documentation | Libraries and services with public APIs |
| **ARCHITECTURE.md** | Architecture overview | Complex systems requiring design documentation |
| **DEPLOYMENT.md** | Deployment procedures | Projects with complex deployment requirements |
| **TROUBLESHOOTING.md** | Common issues and solutions | Projects with known troubleshooting scenarios |
| **PERFORMANCE.md** | Performance tuning guide | Performance-sensitive applications |

#### Optional Files by Repository Type

**Joomla Repositories (WaaS Components):**

| File/Directory | Purpose | When to Use |
|----------------|---------|-------------|
| **scripts/.mokostandards-sync.yml** | Sync override configuration | Custom sync requirements |
| **.github/** | GitHub configuration | Using GitHub Actions or templates |

**Dolibarr Repositories (CRM Modules):**

| File/Directory | Purpose | When to Use |
|----------------|---------|-------------|
| **scripts/.mokostandards-sync.yml** | Sync override configuration | Custom sync requirements |

**Generic Repositories:**

| File/Directory | Purpose | When to Use |
|----------------|---------|-------------|
| **scripts/.mokostandards-sync.yml** | Sync override configuration | Custom sync requirements |

### Layer 4: Policy Documentation (Context-Specific)

**Location:** `/docs/policy/`

**Purpose:** Defines binding policies, standards, and requirements for specific contexts (security, compliance, operations).

**Compliance:** Required when context applies (e.g., WaaS projects must have WaaS policies).

**Common Policy Types:**

- Security policies
- Data classification policies
- Compliance policies
- Operational policies
- Development standards
- Deployment procedures

**When to Use:**

- ✅ Enterprise or regulated environments
- ✅ Multi-tenant platforms (WaaS, CRM)
- ✅ Security-sensitive applications
- ✅ Compliance-required projects (SOC 2, ISO 27001)
- ✅ Projects with specific operational requirements

## Summary Tables

### All Repositories - Common File Requirements

This table shows files that are common across all repository types, with their specific requirement level per type:

| File | Generic Repos | Joomla | Dolibarr | Notes |
|------|---------------|--------|----------|-------|
| **README.md** | ✅ Required | ✅ Required | ✅ Required | Repository root |
| **LICENSE** | ✅ Required | ✅ Required | ✅ Required | GPL-3.0-or-later |
| **CHANGELOG.md** | ✅ Required | ✅ Required | ✅ Required | Version history |
| **CONTRIBUTING.md** | ✅ Required | ✅ Required | ✅ Required | Contribution guidelines |
| **SECURITY.md** | ✅ Required | ✅ Required | ✅ Required | Security policy |
| **CODE_OF_CONDUCT.md** | ✅ Required | ✅ Required | Suggested | Community guidelines |
| **.gitignore** | ✅ Required | ✅ Required | ✅ Required | Platform-specific |
| **.gitattributes** | ✅ Required | ✅ Required | ✅ Required | Git configuration |
| **.editorconfig** | ✅ Required | ✅ Required | ✅ Required | Editor configuration |
| **Makefile** | Suggested | ✅ Required | ✅ Required | Build automation |
| **docs/** | ✅ Required | ✅ Required | ✅ Required | Documentation directory |
| **scripts/** | ✅ Required | ✅ Required | ✅ Required | Build/automation scripts |

### Joomla Repositories - Specific Requirements

| File/Directory | Status | Purpose |
|----------------|--------|---------|
| **site/controller.php** | ✅ Required | Main site controller |
| **site/manifest.xml** | ✅ Required | Component manifest |
| **site/views/** | ✅ Suggested (High Priority) | Site views |
| **site/controllers/** | Suggested | Site controllers |
| **site/models/** | Suggested | Site models |
| **admin/controller.php** | ✅ Required | Main admin controller |
| **admin/views/** | ✅ Suggested (High Priority) | Admin views |
| **admin/controllers/** | Suggested | Admin controllers |
| **admin/models/** | Suggested | Admin models |
| **admin/sql/** | Suggested | Database schema |
| **language/** | ✅ Required | Translation files |
| **media/css/** | Suggested | Stylesheets |
| **media/js/** | Suggested | JavaScript |
| **media/images/** | Suggested | Images |
| **tests/unit/** | ✅ Required | Unit tests |
| **tests/integration/** | Suggested | Integration tests |

### Dolibarr Repositories - Specific Requirements

| File/Directory | Status | Purpose |
|----------------|--------|---------|
| **src/README.md** | ✅ Required | End-user documentation |
| **src/core/modules/mod{Name}.class.php** | ✅ Required | Module descriptor |
| **src/core/** | ✅ Required | Core module files |
| **src/langs/** | ✅ Required | Translation files |
| **src/sql/** | Suggested | Database schema |
| **src/css/** | Suggested | Stylesheets |
| **src/js/** | Suggested | JavaScript |
| **src/class/** | Suggested | PHP classes |
| **src/lib/** | Suggested | Libraries |
| **tests/unit/** | ✅ Required | Unit tests |
| **tests/integration/** | Suggested | Integration tests |
| **templates/** | Suggested | Code generation templates |

### GitHub Configuration - All Repository Types

| File/Directory | Status | Purpose |
|----------------|--------|---------|
| **.github/workflows/** | ✅ Suggested (High Priority) | GitHub Actions |
| **.github/ISSUE_TEMPLATE/** | Suggested | Issue templates |
| **.github/CODEOWNERS** | Suggested | Code ownership |

### Layer 5: Specialized Documentation (Project-Specific)

**Purpose:** Addresses unique requirements for specific project types or contexts.

**Examples:**

- API documentation (for libraries and services)
- Architecture Decision Records (ADRs)
- Deployment guides
- Migration guides
- Troubleshooting guides
- Performance tuning guides
- Integration documentation

**When to Use:**

- ✅ Complex architectural decisions need documentation
- ✅ Multiple deployment environments exist
- ✅ API consumers need integration guidance
- ✅ Performance optimization is critical
- ✅ Troubleshooting requires specialized knowledge

## Layered Approach Benefits

### For Repository Owners

- **Clear Priorities:** Know exactly what documentation is mandatory versus optional
- **Compliance Confidence:** Understand requirements for passing audits and health checks
- **Flexible Enhancement:** Add documentation incrementally as project matures
- **Efficient Resource Allocation:** Focus efforts on required documentation first

### For Contributors

- **Consistent Structure:** Find expected documentation in standard locations
- **Quick Onboarding:** Required documentation ensures baseline information availability
- **Clear Expectations:** Understand contribution requirements from CONTRIBUTING.md
- **Safe Reporting:** Know how to report security issues via SECURITY.md

### For Auditors

- **Objective Criteria:** Clear distinction between required and optional documentation
- **Automated Validation:** Repository health scoring enforces required documentation
- **Remediation Guidance:** Templates provide path to compliance
- **Scalable Reviews:** Standard structure enables efficient audits across repositories

## Implementation Guide

### For New Repositories - All Types

**Step 1: Layer 1 (Required) - MUST COMPLETE FIRST**

#### All Repository Types - Base Requirements

```bash
# Navigate to repository root
cd /path/to/new-repo

# Copy all required templates (common to all types)
cp /path/to/MokoStandards/templates/docs/required/template-README.md ./README.md
cp /path/to/MokoStandards/templates/docs/required/template-CHANGELOG.md ./CHANGELOG.md
cp /path/to/MokoStandards/templates/docs/required/template-CONTRIBUTING.md ./CONTRIBUTING.md
cp /path/to/MokoStandards/templates/licenses/GPL-3.0 ./LICENSE
cp /path/to/MokoStandards/templates/docs/required/template-SECURITY.md ./SECURITY.md

# Copy configuration files
cp /path/to/MokoStandards/.editorconfig ./
cp /path/to/MokoStandards/.gitattributes ./

# Create required directories
mkdir -p docs scripts tests

# Complete all required fields in each file
# Validate compliance
git add README.md CHANGELOG.md CONTRIBUTING.md LICENSE SECURITY.md .editorconfig .gitattributes
git commit -m "Add required documentation (Layer 1)"
```

#### Joomla Repository - Additional Requirements

```bash
# After completing base requirements above

# Copy CODE_OF_CONDUCT (required for Joomla)
cp /path/to/MokoStandards/templates/docs/extra/template-CODE_OF_CONDUCT.md ./CODE_OF_CONDUCT.md

# Copy Joomla-specific .gitignore
cp /path/to/MokoStandards/templates/configs/.gitignore.joomla ./.gitignore

# Copy Makefile for Joomla
cp /path/to/MokoStandards/Makefiles/Makefile.joomla ./Makefile

# Create Joomla-specific directory structure
mkdir -p site/controllers site/models site/views
mkdir -p admin/controllers admin/models admin/views admin/sql
mkdir -p language media/css media/js media/images
mkdir -p tests/unit tests/integration

# Create required files
touch site/controller.php
touch site/manifest.xml
touch admin/controller.php
touch docs/index.md

git add CODE_OF_CONDUCT.md .gitignore Makefile site/ admin/ language/ media/ tests/
git commit -m "Add Joomla-specific required structure"
```

#### Dolibarr Repository - Additional Requirements

```bash
# After completing base requirements above

# Copy Dolibarr-specific .gitignore
cp /path/to/MokoStandards/templates/configs/.gitignore.dolibarr ./.gitignore

# Copy Makefile for Dolibarr
cp /path/to/MokoStandards/Makefiles/Makefile.dolibarr ./Makefile

# Create Dolibarr-specific directory structure
mkdir -p src/core/modules
mkdir -p src/langs
mkdir -p tests/unit tests/integration

# Create required files
touch src/README.md
touch docs/index.md
# Note: Module descriptor file will be created based on module name

git add .gitignore Makefile src/ tests/
git commit -m "Add Dolibarr-specific required structure"
```

#### Generic Repository - Requirements

```bash
# After completing base requirements above

# Copy CODE_OF_CONDUCT (required for generic repos)
cp /path/to/MokoStandards/templates/docs/extra/template-CODE_OF_CONDUCT.md ./CODE_OF_CONDUCT.md

# Copy generic .gitignore
cp /path/to/MokoStandards/templates/configs/.gitignore.generic ./.gitignore

# Optional: Add Makefile for generic repos
cp /path/to/MokoStandards/Makefiles/Makefile.generic ./Makefile

git add CODE_OF_CONDUCT.md .gitignore
git commit -m "Add generic repository required structure"
```

**Step 2: Layer 2 (Suggested) - ADD HIGH PRIORITY ITEMS**

#### All Repository Types

```bash
# Add GitHub workflows (high priority suggested)
mkdir -p .github/workflows
cp /path/to/MokoStandards/.github/workflow-templates/build-universal.yml .github/workflows/
cp /path/to/MokoStandards/.github/workflow-templates/codeql-analysis.yml .github/workflows/
cp /path/to/MokoStandards/.github/workflow-templates/dependency-review.yml .github/workflows/

git add .github/
git commit -m "Add GitHub workflows (Layer 2 suggested)"
```

#### Joomla Repository - Suggested Additions

```bash
# Add high priority suggested directories
mkdir -p site/views/default
mkdir -p admin/views/dashboard

# Add suggested directories as needed
mkdir -p admin/sql

git add site/views/ admin/views/
git commit -m "Add Joomla suggested view structure"
```

#### Dolibarr Repository - Suggested Additions

```bash
# Add suggested directories as project needs dictate
mkdir -p src/sql
mkdir -p src/css
mkdir -p src/js
mkdir -p src/class
mkdir -p src/lib

git add src/sql src/css src/js src/class src/lib
git commit -m "Add Dolibarr suggested directories"
```

**Step 3: Validate Compliance**

```bash
# Run repository health check
# Confirms Layer 1 requirements met
# Shows Layer 2 opportunities

# Example output for Joomla:
# ✅ Required Documentation: 16/16 points (all required files present)
# ✅ Required Structure: 10/10 points (Joomla structure complete)
# ⚠️  Suggested Enhancements: 3/5 points (workflows present, views partial)

# Example output for Dolibarr:
# ✅ Required Documentation: 16/16 points (all required files present)
# ✅ Required Structure: 10/10 points (Dolibarr structure complete)
# ⚠️  Suggested Enhancements: 3/5 points (workflows present, optional dirs missing)
```

### For Existing Repositories

**Assessment:**

```bash
# Check for missing required documentation
ls -1 README.md CHANGELOG.md CONTRIBUTING.md LICENSE SECURITY.md

# Identify missing files
# Plan remediation
```

**Remediation:**

1. **Critical Priority:** Add missing Layer 1 (required) documentation
2. **High Priority:** Enhance existing required documentation if incomplete
3. **Medium Priority:** Add Layer 2 (extra) documentation for high-impact improvements
4. **Low Priority:** Add specialized documentation as project needs evolve

## Documentation Quality Standards

Regardless of layer, all documentation must:

- Follow [Document Formatting Policy](/docs/policy/document-formatting.md)
- Include required metadata sections
- Maintain revision history
- Be reviewed per governance schedule
- Contain accurate, current information
- Use clear, accessible language

## Validation and Enforcement

### Automated Validation

**Repository Health Scoring:**

- Required Documentation category: 16 points maximum
- Deductions for missing required files
- Bonus points for extra documentation
- See [Repository Health Scoring Policy](/docs/policy/health-scoring.md)

**CI/CD Workflows:**

- `standards-compliance.yml` validates required documentation presence
- Build workflows may fail if required documentation missing
- Security workflows reference SECURITY.md for vulnerability reporting

### Manual Validation

**Compliance Audits:**

- Quarterly reviews verify required documentation completeness
- Annual reviews assess documentation quality and currency
- Remediation plans required for non-compliant repositories

## Exceptions and Waivers

### Allowed Exceptions

Certain repository types may have modified requirements:

- **Archive repositories:** May have reduced requirements
- **Internal tooling:** May skip certain extra documentation
- **Experimental repositories:** May defer Layer 2 documentation

### Requesting Waivers

To request a documentation requirement waiver:

1. Document justification in repository README.md
2. Submit waiver request to Governance Owner
3. Obtain documented approval
4. Note waiver in Project register
5. Review waiver annually

## Troubleshooting

### "Required documentation missing" error

**Cause:** One or more Layer 1 required files absent from repository root.

**Solution:**
1. Identify missing files using repository health check
2. Determine repository type (Generic, Joomla, or Dolibarr)
3. Copy corresponding templates from `/templates/docs/required/`
4. For Joomla: Also ensure CODE_OF_CONDUCT.md and Makefile present
5. For Dolibarr: Also ensure Makefile present
6. Complete all required fields
7. Commit to repository
8. Re-run validation

### "Required structure missing" error

**Cause:** Required directories or files for specific repository type missing.

**Solution for Joomla:**
1. Ensure `site/` and `admin/` directories exist
2. Verify `site/controller.php` and `site/manifest.xml` present
3. Verify `admin/controller.php` present
4. Ensure `language/` directory exists
5. Create `docs/index.md` and `tests/unit/` directory

**Solution for Dolibarr:**
1. Ensure `src/` directory exists
2. Verify `src/README.md` present
3. Verify `src/core/` and `src/langs/` directories exist
4. Create module descriptor in `src/core/modules/`
5. Create `docs/index.md` and `tests/unit/` directory

### "Documentation non-compliant" error

**Cause:** Required documentation present but incomplete or improperly formatted.

**Solution:**
1. Review [Document Formatting Policy](/docs/policy/document-formatting.md)
2. Validate all required sections present
3. Ensure metadata fields complete
4. Check revision history included
5. Re-run validation

### "Low repository health score" warning

**Cause:** Missing suggested (Layer 2) documentation reducing score.

**Solution:**
1. Review repository health report details
2. Prioritize high-impact suggested documentation
3. For all types: Add GitHub workflows in `.github/workflows/`
4. For Joomla: Add view directories in `site/views/` and `admin/views/`
5. For Dolibarr: Add optional directories like `src/sql/`, `src/class/`
6. Add GOVERNANCE.md, SUPPORT.md, or DEVELOPMENT.md as appropriate
7. Re-run health check

## Quick Reference

### File Priority Matrix

| Priority | All Repos (Generic) | Joomla | Dolibarr |
|----------|---------------------|--------|----------|
| **Critical (Required)** | README, LICENSE, CHANGELOG, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, .gitignore, .gitattributes, .editorconfig, docs/, scripts/ | + Makefile, site/*, admin/*, language/, tests/unit/ | + Makefile, src/README, src/core/*, src/langs/, tests/unit/ |
| **High (Suggested)** | .github/workflows/ | site/views/, admin/views/ | src/sql/, src/class/ |
| **Medium (Suggested)** | GOVERNANCE, SUPPORT | site/controllers/, admin/controllers/, media/ | src/css/, src/js/, templates/ |
| **Low (Optional)** | Makefile, src/, tests/ | scripts/.mokostandards-sync.yml | scripts/.mokostandards-sync.yml |

### Setup Command Quick Reference

**All Repositories (Base):**
```bash
cp template-README.md README.md
cp template-CHANGELOG.md CHANGELOG.md
cp template-CONTRIBUTING.md CONTRIBUTING.md
cp ../licenses/GPL-3.0 LICENSE
cp template-SECURITY.md SECURITY.md
mkdir -p docs scripts tests
```

**Add for Joomla:**
```bash
cp template-CODE_OF_CONDUCT.md CODE_OF_CONDUCT.md
cp Makefile.joomla Makefile
mkdir -p site/controllers site/models site/views admin/controllers admin/models admin/views language tests/unit
```

**Add for Dolibarr:**
```bash
cp Makefile.dolibarr Makefile
mkdir -p src/core/modules src/langs tests/unit
touch src/README.md
```

**Add for Generic:**
```bash
cp template-CODE_OF_CONDUCT.md CODE_OF_CONDUCT.md
```

### Validation Checklist

**Before First Commit:**
- [ ] All required files from Layer 1 present
- [ ] Repository type identified (Generic/Joomla/Dolibarr)
- [ ] Type-specific required files present
- [ ] All required directories created
- [ ] Required fields in templates completed
- [ ] License file contains GPL-3.0-or-later text
- [ ] README.md has project-specific content (not template placeholders)

**Before Production Deployment:**
- [ ] Repository health score ≥ 80/100
- [ ] All required documentation complete and current
- [ ] SECURITY.md has accurate vulnerability reporting process
- [ ] CHANGELOG.md reflects all releases
- [ ] Tests directory has actual tests
- [ ] GitHub workflows configured (if using GitHub)

**Quarterly Review:**
- [ ] Documentation reviewed for accuracy
- [ ] New suggested enhancements evaluated
- [ ] Repository health score assessed
- [ ] Missing optional documentation prioritized
- [ ] Obsolete documentation removed or archived

## Related Documentation

- [Documentation Governance Policy](/docs/policy/documentation-governance.md) - Overall governance framework
- [Document Formatting Policy](/docs/policy/document-formatting.md) - Formatting standards
- [Repository Health Scoring](/docs/policy/health-scoring.md) - Scoring methodology
- [Required Templates Catalog](/templates/docs/required/README.md) - Layer 1 templates
- [Extra Templates Catalog](/templates/docs/extra/README.md) - Layer 2 templates

## Metadata

- **Document Type:** guide
- **Document Subtype:** implementation
- **Owner Role:** Documentation Owner
- **Approval Required:** No
- **Evidence Required:** No
- **Review Cycle:** Annual
- **Retention:** Indefinite
- **Compliance Tags:** Documentation, Governance
- **Status:** Published

## Revision History

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 01.00.00 | 2026-01-16 | GitHub Copilot | Initial layered documentation guide created. Defines five-layer documentation hierarchy: required, suggested, optional, policy, and specialized documentation. |
| 01.01.00 | 2026-01-16 | GitHub Copilot | Enhanced with repository-type-specific requirements. Added comprehensive tables for Generic, Joomla (WaaS), and Dolibarr (CRM) repositories. Includes required, suggested, and optional file lists for each repository type. Added quick reference section and expanded implementation guide with type-specific examples. |
