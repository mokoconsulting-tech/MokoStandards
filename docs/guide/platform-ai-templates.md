<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
DEFGROUP: MokoStandards.Guide
INGROUP: MokoStandards
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/guide/platform-ai-templates.md
VERSION: 04.00.15
BRIEF: Guide to the platform-specific AI template system — how Joomla, Dolibarr, and generic templates are selected and synced
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.15-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Platform-Specific AI Templates

AI coding assistants (GitHub Copilot, Claude) work better when they have accurate, platform-specific context. A generic "PHP project" template is less useful for a Joomla component developer than one that explains `manifest.xml`, `update.xml`, and Joomla MVC conventions.

MokoStandards therefore ships three sets of AI instruction templates, one for each managed platform.

---

## Template Sets

| Platform | Copilot template | Claude template | Used by definition |
|----------|-----------------|-----------------|-------------------|
| **Generic** (multi-platform) | `templates/github/copilot-instructions.md.template` | `templates/github/CLAUDE.md.template` | `generic-repository.tf` |
| **Joomla / MokoWaaS** | `templates/github/copilot-instructions.joomla.md.template` | `templates/github/CLAUDE.joomla.md.template` | `waas-component.tf` |
| **Dolibarr / MokoCRM** | `templates/github/copilot-instructions.dolibarr.md.template` | `templates/github/CLAUDE.dolibarr.md.template` | `crm-module.tf` |

---

## What Each Template Adds

### All templates (common baseline)

- File header requirements for PHP, Markdown, YAML, Shell
- Version management rules (`README.md` as single source of truth, patch-bump-every-PR)
- GitHub Actions token policy (`secrets.GH_TOKEN`, never `secrets.GITHUB_TOKEN`)
- Commit message format (`feat`, `fix`, `docs`, …)
- Branch naming convention (`dev/`, `rc/`, `version/`, `patch/`, `copilot/`)
- Keeping documentation current table
- MokoStandards policy reference table

### Joomla / MokoWaaS additions

- `update.xml` requirement at the repository root and `manifest.xml` `<updateservers>` block
- Three-way version alignment: `README.md` ↔ `manifest.xml` ↔ `update.xml`
- Joomla extension structure (`site/`, `admin/`, `language/`, `media/`)
- `defined('_JEXEC') or die;` guard rule for web-accessible PHP files
- Reference to [joomla-development-guide.md](waas/joomla-development-guide.md)

### Dolibarr / MokoCRM additions

- Module descriptor class pattern (`mod{MODULE_CLASS}.class.php`)
- Module ID rules: globally unique, registered in [module-registry.md](../development/crm/module-registry.md), never change
- Two-way version alignment: `README.md` ↔ `$this->version` in module descriptor
- Dolibarr source directory structure (`src/core/`, `src/langs/`, `src/sql/`)
- References to [module-registry.md](../development/crm/module-registry.md) and [crm/development-standards.md](../policy/crm/development-standards.md)

---

## How Templates Are Selected

The bulk sync system reads `api/definitions/default/{platform}.tf` for each repository. The `template` field on the `copilot-instructions.md` and `CLAUDE.md` entries points to the correct platform template:

```hcl
# waas-component.tf (Joomla repos)
{
  name                 = "copilot-instructions.md"
  always_overwrite     = false
  template             = "templates/github/copilot-instructions.joomla.md.template"
}

# crm-module.tf (Dolibarr repos)
{
  name                 = "copilot-instructions.md"
  always_overwrite     = false
  template             = "templates/github/copilot-instructions.dolibarr.md.template"
}

# generic-repository.tf (everything else)
{
  name                 = "copilot-instructions.md"
  always_overwrite     = false
  template             = "templates/github/copilot-instructions.md.template"
}
```

The sync system replaces `{{REPO_NAME}}`, `{{REPO_URL}}`, `{{EXTENSION_NAME}}`, etc. at sync time using values from the repository's `.moko-standards` attachment file.

---

## always_overwrite = false

All AI template files use `always_overwrite = false`. This means:

- **First sync**: the template is rendered with the repository's tokens and committed to `.github/copilot-instructions.md` (or `CLAUDE.md`).
- **Subsequent syncs**: the file is **not overwritten**, preserving any project-specific customisations developers have added.

If a repository's AI instructions become badly outdated, a developer can manually delete the file and trigger bulk sync to recreate it from the current template.

---

## Customising AI Instructions in a Governed Repository

After bulk sync creates `.github/copilot-instructions.md` and `.github/CLAUDE.md`, developers may freely extend them with project-specific sections. Guidelines:

- **Do not remove the standard sections** (File Header, Version Management, Token Usage, MokoStandards Reference) — these are enforced by the AI tool governance policy.
- **Add project-specific sections after the standard content** — e.g. domain model glossary, third-party API conventions, custom CI steps.
- The files will not be overwritten by subsequent syncs, so extensions are permanent unless manually removed.

---

## Adding a New Platform

To add a fourth platform (e.g. WordPress):

1. Create `templates/github/copilot-instructions.wordpress.md.template` and `templates/github/CLAUDE.wordpress.md.template`.
2. Add a new platform definition at `api/definitions/default/wordpress-repository.tf`.
3. Set `template = "templates/github/copilot-instructions.wordpress.md.template"` in the `.github` files block.
4. Update this guide, `docs/policy/ai-tool-governance.md`, and the `waas/index.md` or equivalent directory index.

---

## Related Documentation

| Document | Purpose |
|----------|---------|
| [ai-tool-governance.md](../policy/ai-tool-governance.md) | Policy: required context files and enforcement |
| [repo-sync.md](repo-sync.md) | How bulk sync distributes templates to governed repos |
| [joomla-development-guide.md](waas/joomla-development-guide.md) | Joomla extension development guide |
| [dolibarr-development-guide.md](crm/dolibarr-development-guide.md) | Dolibarr module development guide |

## Metadata

| Field         | Value |
|---------------|-------|
| Document Type | Guide |
| Domain        | Governance |
| Applies To    | All repositories |
| Owner         | Moko Consulting |
| Repo          | https://github.com/mokoconsulting-tech/MokoStandards |
| Path          | /docs/guide/platform-ai-templates.md |
| Version       | 04.00.05 |
| Status        | Active |
| Last Reviewed | 2026-03-09 |
