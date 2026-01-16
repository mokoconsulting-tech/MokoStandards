# Issue Templates Organization

## Public Repository (MokoStandards)

The public MokoStandards repository includes the following issue templates:

### Available Templates

1. **bug_report.md** - Report bugs or issues
   - Script issues
   - Schema problems
   - Workflow failures
   - Documentation errors
   - Enterprise library bugs

2. **feature_request.md** - Suggest new features or enhancements
   - New scripts
   - Enterprise library enhancements
   - Schema improvements
   - Workflow enhancements
   - Documentation improvements

3. **documentation.md** - Report documentation issues
   - Missing documentation
   - Unclear/confusing docs
   - Incorrect/outdated content
   - Broken links
   - Missing examples

4. **security.md** - Report security vulnerabilities
   - **Use for low to medium severity only**
   - Critical vulnerabilities should use GitHub Private Vulnerability Reporting
   - Contact: security@mokoconsulting.tech for critical issues

5. **question.md** - Ask questions about usage
   - Script usage
   - Enterprise library integration
   - Best practices
   - Configuration help

## Private Repository (.github-private)

The private .github-private repository includes:

### Available Templates

1. **request-license.md** - Request organization licenses
   - Sublime Text licenses
   - SFTP plugin (personal purchase only)
   - Manager approval workflow
   - License tracking

**Note**: License requests are kept private to protect organizational budget information and license allocation details.

## Template Migration

### Migrated to .github-private

The following template has been moved to the private repository:

- ✅ **request-license.md** - Contains sensitive organizational information
  - License pool tracking (20 licenses)
  - Budget allocation details
  - Manager approval workflow
  - Employee purchase options

### Reason for Separation

**Public templates** (MokoStandards):
- Open-source collaboration
- Community contributions
- General technical issues
- Documentation improvements

**Private templates** (.github-private):
- Internal organizational processes
- Sensitive budget information
- License management
- Employee-only workflows

## Using Issue Templates

### For Public Issues

1. Go to https://github.com/mokoconsulting-tech/MokoStandards/issues/new/choose
2. Select appropriate template
3. Fill out all required sections
4. Submit issue

### For License Requests

1. Go to https://github.com/mokoconsulting-tech/.github-private/issues/new/choose
2. Select "License Request" template
3. Fill out justification and details
4. Await manager approval (1-2 business days)
5. Receive license key via encrypted email

## Template Maintenance

### Adding New Templates

**Public repository**:
```bash
# Create new template in .github/ISSUE_TEMPLATE/
# Follow existing template format
# Include proper labels and assignees
```

**Private repository**:
```bash
# Create in .github-private/.github/ISSUE_TEMPLATE/
# Keep sensitive organizational information private
# Document in this file
```

### Template Structure

All templates should include:
- Clear title format: `[TYPE] Brief description`
- Appropriate labels
- Checkbox lists for clarity
- Examples where helpful
- Checklist for completeness
- Admin-only sections (if needed)

## Support Contacts

For template issues:
- **Public templates**: Open issue in MokoStandards
- **Private templates**: Email dev@mokoconsulting.tech
- **License questions**: license-admin@mokoconsulting.tech
- **General support**: support@mokoconsulting.tech

See `/docs/EMAIL_DIRECTORY.md` for complete contact list.
