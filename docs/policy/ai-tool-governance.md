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
DEFGROUP: MokoStandards.Policy
INGROUP: MokoStandards.Governance
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/policy/ai-tool-governance.md
VERSION: 04.00.05
BRIEF: Governance policy for AI coding tools in all MokoStandards-governed repositories
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.05-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# AI Tool Governance Policy

## Purpose

This policy establishes the governance framework for AI coding assistants and generative-AI tools used in MokoStandards-governed repositories. It defines which tools are approved, what context files are required, how AI-generated code must be reviewed, and how compliance is enforced.

## Scope

This policy applies to:

- All Moko Consulting developers using AI coding tools in governed repositories
- All AI coding assistants and generative-AI tools used for code generation, documentation, or code review
- All AI-generated content committed to governed repositories
- Repository administrators configuring AI tool access

## Approved AI Tools

The following AI coding tools are approved for use in governed repositories:

| Tool | Approval Status | Context File | Notes |
|---|---|---|---|
| GitHub Copilot | ✅ Approved | `.github/copilot-instructions.md` | Org-level policy enforced via Copilot for Business |
| Claude (Anthropic) | ✅ Approved | `.github/CLAUDE.md` | Use Claude Code or API; context file required |
| Cursor | ✅ Approved | `.cursor/rules` | Must be configured with MokoStandards rules |
| Aider | ✅ Approved | `.aider.conf.yml` | Must reference project conventions |
| ChatGPT / GPT-4 | ⚠️ Conditional | N/A | Permitted for documentation drafts only; code must be manually reviewed before commit |
| GitHub Copilot Workspace | ✅ Approved | `.github/copilot-instructions.md` | Subject to same context-file requirements as Copilot |

Tools not listed above require written approval from the repository owner before use.

## Mandatory Context Files

Every governed repository **must** include the following context files. They are created automatically by the [bulk sync system](../guide/repo-sync.md) on first sync and must not be deleted. Once created, they are **never overwritten** by subsequent syncs so that project-specific customisations are preserved.

### `.github/copilot-instructions.md`

- **Enforcement level**: REQUIRED (created on first sync; never overwritten)
- **Source template**: platform-specific (see table below)
- **Purpose**: Provides GitHub Copilot with MokoStandards conventions, file-header requirements, naming rules, commit format, and token policies, plus platform-specific guidance (Joomla `update.xml`, Dolibarr module IDs, etc.).
- **Customisation**: Repositories may freely extend this file with project-specific sections. The file will not be overwritten by bulk sync after initial creation.

### `.github/CLAUDE.md`

- **Enforcement level**: REQUIRED (created on first sync; never overwritten)
- **Source template**: platform-specific (see table below)
- **Purpose**: Provides Claude (Anthropic) with the same MokoStandards context as `copilot-instructions.md`, plus platform-specific guidance, in the format Claude Code expects.
- **Customisation**: Same rules as `copilot-instructions.md`.

### Platform-Specific Templates

The bulk sync system selects the correct template based on the repository's platform definition. Each platform template extends the common baseline with platform-specific rules:

| Platform | `copilot-instructions.md` source | `CLAUDE.md` source | Used by |
|----------|----------------------------------|-------------------|---------|
| Generic / multi-platform | `templates/github/copilot-instructions.md.template` | `templates/github/CLAUDE.md.template` | `generic-repository.tf` |
| Joomla / MokoWaaS | `templates/github/copilot-instructions.joomla.md.template` | `templates/github/CLAUDE.joomla.md.template` | `waas-component.tf` |
| Dolibarr / MokoCRM | `templates/github/copilot-instructions.dolibarr.md.template` | `templates/github/CLAUDE.dolibarr.md.template` | `crm-module.tf` |

For full details on how platform templates are selected and what each adds, see [platform-ai-templates.md](../guide/platform-ai-templates.md).

### `.github/copilot.yml`

- **Enforcement level**: FORCED
- **Source**: `.github/copilot.yml` (synced verbatim from MokoStandards)
- **Purpose**: Restricts which domains GitHub Copilot may access when fetching context, limiting exposure to approved sources only.

## AI-Generated Code Requirements

All AI-generated code committed to governed repositories must comply with the following:

### 1. File Headers

Every AI-generated file must include the standard copyright and `FILE INFORMATION` block before commit. AI tools guided by the context files will generate these automatically; the developer must verify they are correct.

```php
<?php
/**
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * FILE INFORMATION
 * DEFGROUP: {repo}.{Module}
 * INGROUP: {repo}
 * REPO: {repo_url}
 * PATH: /{relative-path}
 * VERSION: {version}
 * BRIEF: {one-line description}
 */
```

See [file-header-standards.md](file-header-standards.md) for the complete list of per-file-type examples.

### 2. Code Review

AI-generated code is not exempt from code review. All PRs containing AI-generated code must:

- Pass the standard review checklist in [code-review-guidelines.md](code-review-guidelines.md)
- Have the PR description note which sections were AI-generated
- Be reviewed by at least one human developer with domain knowledge

The [copilot-pre-merge-checklist.md](copilot-pre-merge-checklist.md) provides a specific checklist for Copilot-assisted PRs.

### 3. Security

AI-generated code must pass the same security scans as human-written code:

- CodeQL analysis (enforced by `codeql-analysis.yml` workflow)
- Secret scanning (enforced by `security-scan.yml` workflow)
- Dependency review (enforced by `dependency-review.yml` workflow)

No exceptions are granted for AI-generated code.

### 4. Sensitive Data

AI tools must not be provided with:

- Secrets, API keys, tokens, or passwords
- Personally identifiable information (PII) of clients or employees
- Confidential business data classified as RESTRICTED or above per [data-classification.md](data-classification.md)
- Internal network topology or infrastructure details

Context files must not contain any of the above. The `copilot.yml` allow-list restricts outbound domain access to prevent inadvertent data exfiltration.

### 5. Licensing

AI-generated code may incorporate patterns from training data. Before committing:

- Review suggestions that closely replicate code from known open-source projects
- Ensure the repository licence is compatible with any incorporated patterns
- When in doubt, rewrite the suggestion from scratch

## Enforcement

### Automated Enforcement

| Control | Mechanism |
|---|---|
| Context files present | Bulk sync creates `copilot-instructions.md` and `CLAUDE.md` on first sync (never overwritten); `copilot.yml` always synced; health check validates presence |
| Domain allow-list | `copilot.yml` restricts Copilot's accessible domains to the approved list |
| Security scans | `codeql-analysis.yml` and `security-scan.yml` run on every PR |
| Standards compliance | `standards-compliance.yml` validates file headers, structure, and coding style |

### Manual Enforcement

- Repository owners are responsible for ensuring developers read and follow this policy
- PR reviewers must confirm that context files are present and have not been modified outside the MokoStandards template
- Audit reviews (see [audit-readiness.md](audit-readiness.md)) include a check for AI tool compliance

## Violations

| Violation | Consequence |
|---|---|
| Removing or disabling context files | PR blocked by health check; restore via bulk sync |
| Committing secrets via AI-generated code | Immediate rotation of all affected credentials; incident review |
| Using a non-approved AI tool | Written warning; code reviewed for policy violations |
| Providing sensitive data to AI tools | Security incident review per [incident-response-runbooks.md](operations/incident-response-runbooks.md) |

## Related Documentation

| Document | Purpose |
|---|---|
| [copilot-usage-policy.md](copilot-usage-policy.md) | Acceptable use policy for GitHub Copilot specifically |
| [copilot-pre-merge-checklist.md](copilot-pre-merge-checklist.md) | Pre-merge checklist for AI-assisted PRs |
| [code-review-guidelines.md](code-review-guidelines.md) | Standard code review requirements |
| [file-header-standards.md](file-header-standards.md) | Required copyright headers for all file types |
| [data-classification.md](data-classification.md) | Data classification tiers |
| [security-scanning.md](security-scanning.md) | Security scanning requirements |
| [docs/guide/ai-client-setup.md](../guide/ai-client-setup.md) | How to configure AI tools in a governed repository |
| [docs/guide/repo-sync.md](../guide/repo-sync.md) | How bulk sync pushes context files to governed repos |
| [docs/guide/platform-ai-templates.md](../guide/platform-ai-templates.md) | Platform-specific AI template selection and customisation |

## Metadata

| Field         | Value |
| ------------- | ----- |
| Document Type | Policy |
| Domain        | Governance |
| Applies To    | All Repositories |
| Jurisdiction  | Tennessee, USA |
| Owner         | Moko Consulting |
| Repo          | https://github.com/mokoconsulting-tech/ |
| Path          | /docs/policy/ai-tool-governance.md |
| Version       | 04.00.05 |
| Status        | Active |
| Last Reviewed | 2026-03-09 |
| Reviewed By   | Documentation Team |

## Revision History

| Date       | Author          | Change  | Notes |
| ---------- | --------------- | ------- | ----- |
| 2026-03-09 | Moko Consulting | Updated | Added platform-specific template section; Joomla and Dolibarr templates documented |
| 2026-03-08 | Moko Consulting | Created | Initial AI tool governance policy |
