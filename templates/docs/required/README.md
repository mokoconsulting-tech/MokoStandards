# Required Documentation Templates

## Purpose

This directory contains mandatory documentation templates that MUST be present in all repositories governed by MokoStandards documentation policies. These templates ensure baseline documentation compliance and organizational consistency.

## Intended Use

Use these templates when:

- Creating a new repository
- Establishing baseline repository documentation
- Ensuring compliance with documentation governance
- Meeting mandatory documentation requirements

## Instructions

### Mandatory Templates

All repositories MUST include these documentation files:

1. **README.md** - Repository overview and entry point
2. **CHANGELOG.md** - Change tracking and release history
3. **CONTRIBUTING.md** - Contribution guidelines and workflow
4. **LICENSE.md** - License terms and copyright information

### Template Usage

For each required template:

1. Copy the template file from this directory
2. Rename removing the `template-` prefix
3. Place in repository root directory
4. Complete all required sections
5. Replace all placeholder values
6. Customize for your repository context
7. Validate compliance with Document Formatting Policy
8. Create Project task for the document

### Compliance Requirements

Required documentation MUST:

- Exist at repository root level
- Follow template structure
- Include all mandatory sections
- Contain accurate, current information
- Be maintained per review cycle
- Have corresponding Project task entries

### Non-Compliance Consequences

Repositories without required documentation:

- Are considered non-compliant
- May not satisfy audit requirements
- Cannot be used for production purposes
- Must remediate before deployment approval

## Required Fields

All required templates must have these completed:

### README.md

- Repository name and purpose
- Installation and usage instructions
- License information
- Contribution guidelines reference
- Contact information

### CHANGELOG.md

- Structured change history
- Release information
- Breaking changes documentation
- Migration guidance where applicable

### CONTRIBUTING.md

- Contribution workflow
- Code of conduct reference
- Development guidelines
- Pull request requirements
- Testing requirements

### LICENSE.md

- License text
- Copyright information
- License terms
- Redistribution terms

## Example Usage

### New Repository Setup

```bash
# Create repository directory
mkdir my-new-repo
cd my-new-repo

# Initialize git
git init

# Copy required templates
cp /templates/docs/required/template-README.md ./README.md
cp /templates/docs/required/template-CHANGELOG.md ./CHANGELOG.md
cp /templates/docs/required/template-CONTRIBUTING.md ./CONTRIBUTING.md
cp /templates/docs/required/template-LICENSE.md ./LICENSE.md

# Edit each file to complete required fields
# Validate compliance
# Commit to repository
git add README.md CHANGELOG.md CONTRIBUTING.md LICENSE.md
git commit -m "Add required documentation"
```

### Existing Repository Compliance

```bash
# Check for missing required files
ls -1 README.md CHANGELOG.md CONTRIBUTING.md LICENSE.md

# Copy missing templates
# Complete required fields
# Commit to repository
```

## Template List

- **template-README.md** - Repository overview template
- **template-CHANGELOG.md** - Change log template
- **template-CONTRIBUTING.md** - Contribution guidelines template
- **template-LICENSE.md** - License document template

## Metadata

- **Document Type:** overview
- **Document Subtype:** catalog
- **Owner Role:** Documentation Owner
- **Approval Required:** No
- **Evidence Required:** Yes
- **Review Cycle:** Annual
- **Retention:** Indefinite
- **Compliance Tags:** Governance, Compliance
- **Status:** Published

## Revision History

- Initial required templates catalog established
- Mandatory template requirements defined
- Compliance and usage instructions documented
