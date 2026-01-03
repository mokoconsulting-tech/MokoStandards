# Extra Documentation Templates

## Purpose

This directory contains optional documentation templates that enhance repository documentation quality and completeness. These templates are recommended but not mandatory, providing additional documentation capabilities beyond baseline requirements.

## Intended Use

Use these templates when:

- Enhanced documentation is beneficial
- Specific use cases require additional documentation
- Improving documentation beyond minimum requirements
- Addressing stakeholder needs for additional information
- Meeting specific project or compliance needs

## Instructions

### Optional Templates

Extra templates provide documentation for:

1. **Code of Conduct** - Community behavior guidelines
2. **Security Policy** - Security reporting and disclosure
3. **Support Documentation** - Support channels and procedures
4. **Governance Documents** - Decision-making and authority
5. **Additional Technical Documentation** - Architecture, design, API docs

### Template Selection

Choose extra templates based on:

- **Project Size** - Larger projects benefit from comprehensive documentation
- **Community Size** - Projects with external contributors need governance docs
- **Security Requirements** - Security-sensitive projects need security policy
- **Stakeholder Needs** - Specific stakeholder requirements
- **Compliance Requirements** - Regulatory or audit requirements

### Template Usage

For each extra template:

1. Determine if template is needed for your project
2. Copy the template file from this directory
3. Rename removing the `template-` prefix
4. Place in appropriate repository location
5. Complete all sections
6. Replace all placeholder values
7. Customize for your project context
8. Create Project task if document is critical
9. Maintain per appropriate review cycle

### When to Use Extra Templates

#### Code of Conduct

Use when:

- Repository accepts external contributions
- Community interactions expected
- Need to establish behavioral expectations
- Creating inclusive environment

#### Security Policy

Use when:

- Repository contains security-sensitive code
- Security vulnerabilities may be discovered
- Need coordinated disclosure process
- Compliance requires security documentation

#### Support Documentation

Use when:

- Users need support information
- Multiple support channels exist
- Support expectations must be clear
- SLA or support tiers defined

#### Governance Documents

Use when:

- Decision-making authority must be clear
- Multiple maintainers or teams involved
- Escalation procedures needed
- Organizational governance required

## Required Fields

When using extra templates, ensure these fields are completed:

- All section headers with appropriate content
- Purpose and scope clearly defined
- Contact information where applicable
- Procedures and processes clearly documented
- Metadata (for governed documents)
- Revision history

## Example Usage

### Adding Code of Conduct

```bash
# Copy template
cp /templates/docs/extra/template-CODE_OF_CONDUCT.md ./CODE_OF_CONDUCT.md

# Edit the file
# - Complete all sections
# - Add contact information for enforcement
# - Customize behavioral expectations
# - Add reporting procedures

# Commit to repository
git add CODE_OF_CONDUCT.md
git commit -m "Add Code of Conduct"
```

### Adding Security Policy

```bash
# Copy template
cp /templates/docs/extra/template-SECURITY.md ./SECURITY.md

# Edit the file
# - Define supported versions
# - Add vulnerability reporting procedures
# - Define disclosure timelines
# - Add security contact information

# Commit to repository
git add SECURITY.md
git commit -m "Add security policy"
```

### Adding Support Documentation

```bash
# Copy template
cp /templates/docs/extra/template-SUPPORT.md ./SUPPORT.md

# Edit the file
# - List support channels
# - Define response expectations
# - Add support tiers if applicable
# - Include escalation procedures

# Commit to repository
git add SUPPORT.md
git commit -m "Add support documentation"
```

## Template List

- **template-CODE_OF_CONDUCT.md** - Community behavior guidelines template
- Additional templates as needed for specific use cases

Note: Extra templates are created on-demand based on organizational needs. Check this directory for available templates or request new templates through governance channels.

## Best Practices

When using extra templates:

- Only use templates that add value to your project
- Keep documentation current and accurate
- Follow Document Formatting Policy
- Create Project tasks for critical documents
- Review and update per appropriate schedule
- Remove unused templates to reduce maintenance burden

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

- Initial extra templates catalog established
- Template selection guidance defined
- Usage instructions and best practices documented
