<!-- Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>

 This file is part of a Moko Consulting project.

 SPDX-LICENSE-IDENTIFIER: GPL-3.0-or-later

 This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

 You should have received a copy of the GNU General Public License (./LICENSE).

 # FILE INFORMATION
 DEFGROUP: MokoStandards
 INGROUP: Documentation
 REPO: https://github.com/mokoconsulting-tech/MokoStandards/
 VERSION: 04.00.00
 PATH: ./README.md
 BRIEF: Reference and packaging repo for the Moko Consulting coding ecosystem
-->

# MokoStandards (VERSION: 04.00.00)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Status](https://img.shields.io/badge/status-active-brightgreen)

## Introduction

## Summary

This repository provides the central governance, coding standards, scaffolding frameworks, and compliance defaults used across all Moko Consulting engineering initiatives. It acts as the authoritative source for headers, metadata formats, development workflows, CI integration, accessibility requirements, and module registries.

## Documentation Links

The full documentation suite is available within the `docs/` directory of this repository. Key documents include:

* [Documentation Index](./docs/docs-index.md)
* [Architecture Guide](./docs/docs-architecture.md)
* [Data Model Guide](./docs/docs-data-model.md)
* [Integrations Guide](./docs/docs-integrations.md)
* [Testing Guide](./docs/docs-testing.md)
* [Operations Guide](./docs/docs-operations.md)
* [Change Management Guide](./docs/docs-change-management.md)
* [Risk Register](./docs/docs-risk-register.md)
* [Compliance Guide](./docs/docs-compliance.md)
* [Governance Guide](./docs/docs-governance.md)
* [Security Guide](./docs/docs-security.md)
* [API Reference](./docs/docs-api-reference.md)
* [Runbooks](./docs/docs-runbooks.md)

MokoStandards serves as the authoritative reference for development standards across all Moko Consulting repositories. It centralizes coding conventions, governance rules, scaffolds, templates, CI policies, accessibility requirements, and module registries for Dolibarr, Joomla, and supporting ecosystems.
This repository is not a runtime codebase; it provides reusable standards intended to be applied across projects through submodules, overlays, or CI import.

## Features

* SPDX compliant headers with full metadata blocks
* Unified CI and quality gating patterns
* Editor configuration suites (EditorConfig, ESLint, Prettier, PHP-CS-Fixer)
* GitHub issue templates, PR templates, labels, and governance patterns
* Security hygiene standards, including CODEOWNERS and secret-prefix policy
* WCAG 2.1 AA accessibility quick-pass checklist
* Dolibarr module number registry (185050 through 185099)

## Install and Use

Recommended consumption methods:

### Submodule (preferred)

```bash
git submodule add https://github.com/mokoconsulting-tech/MokoStandards .moko/defaults
git submodule update --init --recursive
```

### Remote include via CI

```bash
curl -fsSL https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/.editorconfig -o .editorconfig
```

### Scaffold new projects

Use the scaffolds in this repository to bootstrap Dolibarr modules, Joomla templates, plugins, or generic Git projects.
Downstream repos may override standards through `.moko.local/`.

## Configuration Standards

* Code style and linting patterns must be adopted as defined unless exceptions are documented in `.moko.local/`.
* Git governance: protected `main` branch, required `dev` branch for all feature work, squash merges, required review, Conventional Commits.
* Feature development must target the `dev` branch; direct commits to `main` are prohibited except for release automation.
* Localization: provide both en_US and en_GB variants for user-facing strings.
* Accessibility: apply WCAG checklist during PR review.
* Headers: include SPDX and metadata in all files except JSON.

## Usage Guidelines

* Sync `FILE INFORMATION` with changelog entries during releases.
* Apply standardized commit messages and PR checks.
* Maintain consistency with semantic versioning across all projects.

## Overlays and Scaffolds

Apply in this order. After installing `generic-git`, the user must choose **either** the Dolibarr scaffold **or** the Joomla scaffold family. These paths are mutually exclusive and should not be combined. Dolibarr and Joomla defaults overwrite generic-git where definitions conflict:

1. [**generic-git**]
Baseline repo structure, issue templates, PR templates, labels, CI, and security defaults. Serves as the foundation layer.

	a. [**dolibarr-default**]
	Overrides generic‑git when Dolibarr standards differ. Provides Dolibarr-specific skeletons, rights management templates, language keys, idempotent SQL migrations, and Dolibarr constants patterns.
	
	b. [**joomla-template-default**]
	Overrides generic‑git for joomla template‑specific rules. Includes Cassiopeia‑based scaffolding, variable tokens, layout guidelines, and accessibility alignment.
	
	c. [**joomla-plugin-default**]
	Overrides generic‑git for joomla plugin‑specific behaviors. Includes manifest boilerplate, event hooks, language files, and lifecycle scripts.
	
	d. [**joomla-component-default**]
		Overrides generic‑git for joomla component plugin‑specific behaviors. Includes manifest boilerplate, event hooks, language files, and lifecycle scripts.

## Dolibarr Module Number Registry

Reserved range: **185050–185099**

| Numero | Module             | Status      | Notes |
| ------ | ------------------ | ----------- | ----- |
| 185051 | MokoDoliTools      | Production  |       |
| 185052 | MokoDoliSign       | Development |       |
| 185053 | MokoDoliForm       | Development |       |
| 185054 | MokoDoliUpdates    | Development |       |

Rule: reserve a module number before development begins.

## Roadmap

* Expand Dolibarr migration helpers and QA smoke-test scripts
* Add Playwright visual regression support
* Add GitHub Actions matrices for PHP 8.1 through 8.3 and Node LTS
* Expand accessibility and localization templates

## Header Requirements After Scaffolding

After copying any scaffold (generic-git, Dolibarr, or Joomla), users must update all file headers to match the established Moko Consulting header specification. Each file must include the full GPL block followed by the FILE INFORMATION block in this format:

```
<!--
 Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>

 This file is part of a Moko Consulting project.

 SPDX-LICENSE-IDENTIFIER: GPL-3.0-or-later

 This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

 You should have received a copy of the GNU General Public License (./LICENSE.md).

 # FILE INFORMATION
 DEFGROUP: <ProjectGroup>
 INGROUP: <Subgroup>
 REPO: <RepositoryURL>
 VERSION: <Version>
 PATH: <RelativePath>
 BRIEF: <ShortDescription>
 NOTE: <OptionalNotes>
-->
```

Users must update all placeholder fields when scaffolds are applied. JSON files are excluded from header insertion.


## Support

* Documentation and help desk: [https://mokoconsulting.tech/support](https://mokoconsulting.tech/support)
* Security reporting: see `SECURITY.md` for private contact route
* General inquiries: [hello@mokoconsulting.tech](mailto:hello@mokoconsulting.tech)

## License

GPL-3.0-or-later. See `LICENSE` for full text.

---

## Metadata

* MAINTAINER: Moko Consulting Engineering
* REPO: [https://github.com/mokoconsulting-tech/MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards)
* FILE: README.md
* VERSION: 04.00.00
* CLASSIFICATION: Public Open Source Standards
* COMPLIANCE SCOPE: All Moko Consulting repositories

## Revision History

| Version 	| Date       | Author          | Description 	|
| --------- | ---------- | --------------- | ------------ |
| 03.00.00 	| 2025-12-11 | Moko Consulting | Cleanup, consolidation |
| 2.1 			| 2025-11-25 | Moko Consulting | Cleanup, consolidation, removal of Discovery row |
| 2.0 			| 2025-11-25 | Moko Consulting | Full cleanup, metadata and revision history added |
| 1.0 			| 					 | Moko Consulting | Initial published version |
