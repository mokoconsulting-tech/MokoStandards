# Documentation Templates

## Purpose

This directory contains governed documentation templates for the MokoStandards organization. These templates ensure consistency, completeness, and compliance across all documentation artifacts.

## Intended Use

Use these templates when:

- Creating new documentation files
- Establishing documentation in new repositories
- Ensuring compliance with documentation standards
- Maintaining consistency across projects

## Instructions

### Template Categories

Templates are organized into two categories:

1. **Required Templates** - `/templates/docs/required/`
   - Mandatory documentation files for all repositories
   - Must be present and maintained
   - Subject to compliance review

2. **Extra Templates** - `/templates/docs/extra/`
   - Optional documentation files
   - Recommended for specific use cases
   - Enhance documentation quality

### Using Templates

To use a template:

1. Navigate to appropriate template category (required or extra)
2. Copy the template file to your target location
3. Rename the file removing the `template-` prefix
4. Replace all placeholder content with actual information
5. Complete all required fields
6. Remove example sections or mark them explicitly as examples
7. Follow the template instructions section
8. Validate against Document Formatting Policy

### Template Maintenance

Templates are governed assets and must:

- Follow Document Formatting Policy requirements
- Include all required sections for templates
- Contain no production data
- Use placeholder values only
- Be reviewed per governance schedule
- Have Project task entries

## Required Fields

When using templates, ensure these fields are completed:

- All section headers and content
- Metadata fields specific to the document
- Revision history
- Purpose and scope statements
- Responsibilities and governance rules (where applicable)

## Example Usage

### Creating a New Repository README

```bash
# Copy template to target location
cp /templates/docs/required/template-README.md /path/to/repo/README.md

# Edit the file
# - Replace "[Repository Name]" with actual repository name
# - Complete all sections
# - Update metadata
# - Customize content for your repository
```

### Creating a New Policy Document

```bash
# Use policy template structure
# Follow /docs/policy/ examples
# Ensure all mandatory policy sections included
# Obtain required approvals per policy
```

## Metadata

- **Document Type:** overview
- **Document Subtype:** catalog
- **Owner Role:** Documentation Owner
- **Approval Required:** No
- **Evidence Required:** Yes
- **Review Cycle:** Annual
- **Retention:** Indefinite
- **Compliance Tags:** Governance
- **Status:** Published

## Revision History

- Initial template catalog established
- Template categories and usage instructions defined
- Template maintenance requirements documented
