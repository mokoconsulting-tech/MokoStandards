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
INGROUP: MokoStandards.Guide
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: docs/COPILOT_PROMPT_FOR_.GITHUB-PRIVATE.md
VERSION: 05.00.00
BRIEF: Reference documentation for GitHub Copilot prompts stored in private repository
-->

# GitHub Copilot Prompt Reference for .github-private

## Overview

This document provides guidance on GitHub Copilot prompt templates and configurations that have been moved to the private **mokoconsulting-tech/.github-private** repository for security and confidentiality reasons.

## Purpose

GitHub Copilot prompts contain proprietary AI prompt engineering, internal workflow templates, and organization-specific automation patterns that are specific to Moko Consulting's operations. These prompts are maintained privately to:

1. **Protect Intellectual Property**: Custom prompt engineering represents proprietary knowledge
2. **Maintain Security**: Prompts may reference internal systems, projects, or workflows
3. **Ensure Confidentiality**: Organization-specific patterns should not be publicly disclosed
4. **Enable Customization**: Internal teams can iterate on prompts without public visibility

## Private Repository Location

**Repository**: `https://github.com/mokoconsulting-tech/.github-private`

**Access**: Restricted to Moko Consulting organization members

**Path**: `/docs/policy/copilot-prompts/`

## Copilot Prompt Files Moved to Private Repository

### copilot-prompt-projectv2-joomla-template.md

**Original Location**: `docs/policy/copilot-prompt-projectv2-joomla-template.md` (public repo)

**Current Location**: `/docs/policy/copilot-prompts/projectv2-joomla-template.md` (private repo)

**Purpose**: Custom GitHub Copilot prompts for Joomla project automation and GitHub Projects v2 integration

**Contains**:
- AI prompt templates for Joomla component development
- GitHub Projects v2 field mappings and automation prompts
- Internal workflow patterns for WaaS components
- Organization-specific coding standards and conventions
- Custom validation rules for Moko Consulting projects

**Reason for Privacy**:
- Contains proprietary AI prompt engineering techniques
- References internal GitHub Project configurations
- Includes organization-specific development patterns
- Documents internal automation workflows

## Public Copilot Configuration

The public repository maintains general GitHub Copilot configuration in `.github/copilot.yml`:

**File**: `.github/copilot.yml`

**Purpose**: Configure allowed domains and general Copilot settings for the repository

**Contains**:
- Allowed domains for Copilot to access (license providers, documentation sites, package registries)
- File patterns to include/exclude from Copilot suggestions
- General repository-wide Copilot settings

**Scope**: Public configuration suitable for community contributors

## For Moko Consulting Internal Users

### Accessing Private Copilot Prompts

If you are a Moko Consulting team member and need access to the internal Copilot prompts:

1. **Ensure Repository Access**: Verify you have access to `mokoconsulting-tech/.github-private`
2. **Clone Private Repository**:
   ```bash
   git clone https://github.com/mokoconsulting-tech/.github-private.git
   ```
3. **Navigate to Prompts**:
   ```bash
   cd .github-private/docs/policy/copilot-prompts/
   ```
4. **Review Available Prompts**: Use `ls` to see all available prompt templates

### Using Internal Copilot Prompts

The private repository copilot prompts directory contains:

- **Project-specific prompt templates** for GitHub Copilot
- **AI automation patterns** for internal workflows
- **Custom field mappings** for GitHub Projects v2
- **Organization-specific coding conventions** for AI assistance

**Usage Example**:
```bash
# Navigate to private repo copilot prompts
cd .github-private/docs/policy/copilot-prompts/

# View available prompts
ls -la

# Reference prompts in your GitHub Copilot configuration
# or use them as templates for AI-assisted development
```

### Contributing New Copilot Prompts

To add new internal Copilot prompts:

1. **Create in Private Repo**: Add new prompt files to `.github-private/docs/policy/copilot-prompts/`
2. **Follow Naming Convention**: Use descriptive names like `copilot-prompt-{project-type}-{use-case}.md`
3. **Document Purpose**: Include header comments explaining the prompt's use case
4. **Reference Internal Projects**: It's safe to reference internal project numbers and configurations
5. **Submit PR**: Open a pull request in the private repository for review

## For External Users

If you are adopting MokoStandards for your own organization and want to create similar Copilot prompts:

### Creating Your Own Copilot Prompts

1. **Establish Private Storage**: Create your own private repository for sensitive prompts
2. **Define Prompt Structure**: Create a consistent format for your prompt templates
3. **Document Use Cases**: Clearly document when and how each prompt should be used
4. **Reference Your Projects**: Customize prompts to reference your own GitHub Projects and workflows

### Public Copilot Configuration

For public repositories, you can use the `.github/copilot.yml` configuration as a template:

**Example**:
```yaml
# .github/copilot.yml
allowed_domains:
  - "opensource.org"
  - "github.com"
  - "docs.github.com"
  
copilot:
  enabled: true
  include:
    - "**/*.py"
    - "**/*.js"
    - "**/*.md"
  exclude:
    - "**/node_modules/**"
    - "**/vendor/**"
```

### Prompt Template Example

For your own private prompts, consider this structure:

```markdown
# Copilot Prompt: [Purpose]

## Context
[Describe the context where this prompt applies]

## Prompt Template
[Your AI prompt template]

## Expected Output
[Description of expected AI behavior]

## Usage Notes
[When and how to use this prompt]
```

## Related Documentation

- [.github/copilot.yml](.github/copilot.yml) - Public Copilot configuration
- [docs/guide/PRIVATE_REPOSITORY_REFERENCE.md](guide/PRIVATE_REPOSITORY_REFERENCE.md) - Complete private file reference
- [docs/guide/repository-split-plan.md](guide/repository-split-plan.md) - Public/private architecture guide

## Migration History

### Moved on 2026-01-04

This separation was implemented as part of the enterprise readiness initiative to:

- Protect proprietary AI prompt engineering
- Maintain confidentiality of internal automation patterns
- Enable safe public sharing of general coding standards
- Provide clear boundaries between public and private configurations

**Related Changes**:
- Proprietary Copilot prompts moved to `.github-private/docs/policy/copilot-prompts/`
- Public Copilot configuration retained in `.github/copilot.yml`
- Internal project references removed from public repository

## Best Practices

### For Internal Prompts (Private Repository)

✅ **DO**:
- Reference internal GitHub Projects, team structures, and workflows
- Include proprietary coding patterns and conventions
- Document organization-specific AI assistance patterns
- Use detailed examples with internal project references

❌ **DON'T**:
- Include API keys, tokens, or credentials
- Expose customer or partner information
- Document security vulnerabilities or sensitive infrastructure

### For Public Configuration (Public Repository)

✅ **DO**:
- Configure general Copilot settings for community contributors
- List publicly accessible, trusted domains
- Define standard file patterns for inclusion/exclusion
- Provide general guidance suitable for public consumption

❌ **DON'T**:
- Reference internal projects or team structures
- Include proprietary prompt templates
- Expose organization-specific patterns

## Support

### For Internal Users

**Questions about private Copilot prompts**: Contact `@mokoconsulting-tech/maintainers` or email `dev@mokoconsulting.tech`

**Access issues**: Contact repository administrators

**New prompt requests**: Open an issue in the `.github-private` repository

### For External Users

**Questions about public Copilot configuration**: Open an issue in this repository

**Adoption guidance**: See [CONTRIBUTING.md](../CONTRIBUTING.md) and [docs/](.)

---

## Metadata

| Field      | Value                                                                                                        |
| ---------- | ------------------------------------------------------------------------------------------------------------ |
| Document   | GitHub Copilot Prompt Reference for .github-private                                                          |
| Path       | docs/COPILOT_PROMPT_FOR_.GITHUB-PRIVATE.md                                                                   |
| Repository | [https://github.com/mokoconsulting-tech/MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards) |
| Owner      | Moko Consulting                                                                                              |
| Scope      | Reference documentation                                                                                      |
| Status     | Published                                                                                                    |
| Effective  | 2026-01-17                                                                                                   |

## Revision History

| Date       | Change Description                                      | Author          |
| ---------- | ------------------------------------------------------- | --------------- |
| 2026-01-17 | Initial creation, documenting Copilot prompt reference  | Moko Consulting |
