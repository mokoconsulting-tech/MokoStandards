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
DEFGROUP: GitHub.Configuration
INGROUP: MokoStandards.Documentation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /.github/PRIVATE_TEMPLATES.md
VERSION: 01.00.00
BRIEF: Reference to private GitHub configuration templates
-->

# Private GitHub Templates

## Overview

This repository's **private GitHub configuration templates** (CODEOWNERS, issue templates, pull request templates) are maintained in a separate private repository for security and organizational reasons.

## Location

**Repository**: `mokoconsulting-tech/.github-private`

This private repository contains:

- **CODEOWNERS** - Code ownership and review assignments for internal teams
- **Issue Templates** - Internal issue templates for various workflows:
  - Architecture Decision Records (ADR)
  - Bug reports
  - Deployment plans
  - Documentation changes
  - Escalations
  - Feature requests
  - Incident reports
  - Migration plans
  - Risk register entries
  - Runbooks
  - Security reviews
- **Pull Request Template** - Internal PR checklist and review requirements

## Why Private?

These templates are kept private to:

1. **Protect Internal Information**: Team member names, email addresses, and organizational structure
2. **Maintain Confidentiality**: Internal processes, escalation procedures, and workflow details
3. **Security**: Sensitive operational information not suitable for public disclosure
4. **Flexibility**: Allow internal iterations without public visibility

## For Moko Consulting Internal Users

**Access**: Organization members can access the private repository at:
```
https://github.com/mokoconsulting-tech/.github-private
```

**Setup for New Repositories**:
1. Clone or reference the private template repository
2. Copy relevant templates to your repository's `.github/` directory
3. Customize for your specific project needs
4. Do not commit sensitive templates to public repositories

## For External Users

If you are adopting MokoStandards for your own organization:

1. **Create Your Own Templates**: Use this repository's public standards as a guide
2. **Customize**: Adapt templates to your organization's needs
3. **Keep Private**: Store sensitive templates in your own private repositories
4. **Reference**: See [File Header Standards](../docs/policy/file-header-standards.md) for template structure

## Public Templates

Public, reusable templates are available in this repository:

- **Workflow Templates**: [.github/workflows/templates/](workflows/templates/)
  - Joomla CI/CD workflows
  - Generic repository health workflows
  - Version branch automation

- **Documentation Templates**: [templates/docs/](../templates/docs/)
  - Policy document templates
  - Guide document templates
  - Checklist templates

## Creating Private Templates

To create templates for the private repository:

### CODEOWNERS Example

```
# CODEOWNERS for internal repositories

# Default owners for everything in the repo
* @your-org/maintainers

# Documentation owned by docs team
/docs/ @your-org/documentation

# Security-related files need security team approval
/SECURITY.md @your-org/security
/.github/workflows/ @your-org/security @your-org/devops
```

### Issue Template Example

```markdown
---
name: Bug Report
about: Report a bug in the system
title: '[BUG] '
labels: bug, needs-triage
assignees: ''
---

## Description
Brief description of the bug

## Steps to Reproduce
1. 
2. 
3. 

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- Version:
- Platform:
- Browser (if applicable):

## Additional Context
Any other relevant information
```

### Pull Request Template Example

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] No new warnings

## Testing
Describe testing performed

## Screenshots (if applicable)
Add screenshots of UI changes
```

## Related Documentation

- [Repository Split Plan](../docs/guide/repository-split-plan.md) - Detailed architecture for public/private separation
- [File Header Standards](../docs/policy/file-header-standards.md) - Standards for all files including templates
- [GitHub README](.github/README.md) - Overview of GitHub configuration

## Support

For questions about private templates:

**Internal Users**: Contact `@mokoconsulting-tech/maintainers` or email `dev@mokoconsulting.tech`

**External Users**: Use public GitHub issues for questions about adopting MokoStandards

---

## Metadata

| Field      | Value                                                                                                        |
| ---------- | ------------------------------------------------------------------------------------------------------------ |
| Document   | Private GitHub Templates Reference                                                                           |
| Path       | /.github/PRIVATE_TEMPLATES.md                                                                                |
| Repository | [https://github.com/mokoconsulting-tech/MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards) |
| Owner      | Moko Consulting                                                                                              |
| Scope      | GitHub configuration reference                                                                               |
| Status     | Published                                                                                                    |
| Effective  | 2026-01-04                                                                                                   |

## Revision History

| Date       | Change Description                                      | Author          |
| ---------- | ------------------------------------------------------- | --------------- |
| 2026-01-04 | Initial creation, reference to private template repo    | Moko Consulting |
