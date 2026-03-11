[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.04-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# MokoStandards Templates Documentation

## Overview

This directory contains comprehensive documentation for all templates provided by MokoStandards. Templates are organized by category and provide standardized starting points for files, configurations, and workflows across the organization.

## Template Categories

### [Workflow Templates](./workflows/index.md)
GitHub Actions workflow templates for CI/CD automation
- [Generic Workflows](./workflows/generic.md) - Platform-agnostic CI/CD
- [Joomla Workflows](./workflows/joomla.md) - Joomla extension workflows
- [Dolibarr Workflows](./workflows/dolibarr.md) - Dolibarr module workflows

### [Image Assets](./images/index.md)
Brand, favicon, and background image assets
- `primary/logo.png` — README logo (referenced by all governed repo READMEs)
- `primary/favicon_256.png` — Canonical favicon; sync template for Dolibarr `img/` directories (deployed as `object_favicon_256.png`)
- Full favicon set (SVG, ICO, 96 px, 120 px, 256 px), PWA manifest icons, apple-touch-icon

### [Font Assets](./fonts/index.md)
Locally bundled typefaces for offline, print, and native use cases
- `osaka-re.ttf` — Osaka Re display typeface (TrueType)
- Web projects must use Google Fonts; see [Google Fonts Policy](../policy/google-fonts.md)

### License Templates
Authoritative license files for organizational compliance
- See [templates/licenses/](../../templates/licenses/)

### Schema Templates
Repository structure definition templates
- See [templates/schemas/](../../templates/schemas/)

### Script Templates
Build, validation, and automation script templates
- See [scripts/lib/](../../scripts/lib/)

### Documentation Templates
Documentation file templates for consistency
- See [templates/docs/](../../templates/docs/)

## Quick Start

See individual template category documentation for detailed usage instructions.

---

**Last Updated**: 2026-01-16
**Maintained By**: MokoStandards Team
