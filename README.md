<!--
 Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>

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
 (./LICENSE.md).

 # FILE INFORMATION
 DEFGROUP: MokoStandards.Standards
 INGROUP: MokoStandards
 REPO: https://github.com/mokoconsulting-tech/MokoStandards
 FILE: README.md
 VERSION: 04.01.00
 BRIEF: Coding standards hub and cross repository index for the MokoStandards ecosystem.
 PATH: /README.md
 NOTE: Repository rebaselined to standards first, decoupled from specific template or scaffold repositories.
-->

# MokoStandards (VERSION: 04.01.00)

MokoStandards is the authoritative control plane for coding standards across the Moko Consulting ecosystem. This repository defines how code is formatted, structured, reviewed, tested, packaged, and released.

## Scope

This repository is intentionally standards only.

Included:

* Language and framework conventions (PHP, JavaScript, CSS, XML, INI, Markdown)
* Git and GitHub operational standards (branching, commits, CI requirements, release rules)
* File header and metadata requirements
* Documentation standards that govern engineering docs

Excluded:

* Full project scaffolds
* Example extensions or templates
* Repo specific workflows that only make sense inside a given scaffold repo

## Ecosystem map

This repository defines standards independently of any specific downstream implementation. Companion repositories may exist, but are not enumerated or coupled here.

## Operating model

### Source of truth

* Standards live here.
* Templates and scaffolds live outside this repository and are not authoritative.
* Downstream projects adopt standards by referencing this repository and implementing its checks in CI.

### Adoption patterns

Recommended adoption patterns, in order of operational maturity:

1. Reference only
2. Vendored standards
3. Pinned submodule
4. CI enforced compliance

## Repository layout

This repository is organized to separate enforceable standards from reusable templates and reference material. The layout is intentionally opinionated to support auditability, automation, and long term governance.

### Top level folders

* [`docs/`](docs/index.md)

  * Canonical standards documentation.
  * Contains policy, guidance, checklist, and glossary documents.
  * Documents in this folder are authoritative and binding unless explicitly marked informational.
  * All policy documents must follow the mandatory metadata and revision history structure.
  * Entry point and catalog: [`docs/index.md`](docs/index.md).

  #### `docs/` hierarchy

  * [`docs/policy/`](docs/policy/index.md)

    * Binding policy documents.
    * Defines mandatory rules for repositories, CI, licensing, documentation, and governance.

  * [`docs/guidance/`](docs/guidance/index.md)

    * Non binding guidance and best practices.
    * Explains intent, rationale, and recommended implementation patterns.

  * [`docs/checklist/`](docs/checklist/index.md)

    * Compliance and review checklists.
    * Used for audits, PR validation, and release readiness.

  * [`docs/glossary/`](docs/glossary/index.md)

    * Canonical terminology definitions.
    * Ensures consistent language across standards and documentation.

  * [`docs/standards/`](docs/standards/index.md)

    * Domain specific standards grouped by subject area.
    * Intended long term home for language, platform, and tooling standards.

* [`templates/`](templates/index.md)

  * Non authoritative reference material.
  * Provides concrete examples of how standards may be implemented.
  * Content here may evolve faster than standards and must not be treated as requirements.

  #### `templates/` hierarchy

  * [`templates/docs/`](templates/docs/index.md)

    * Documentation templates aligned with standards in `docs/`.
    * Includes policy, guidance, checklist, glossary, and structural templates.

  * [`templates/scripts/`](templates/scripts/index.md)

    * Example validation, CI, and utility scripts.
    * Intended for reuse, vendoring, or adaptation.

  * [`templates/repos/`](templates/repos/index.md)

    * Reference repository layouts by platform or domain.

    * [`templates/repos/joomla/`](templates/repos/joomla/index.md)

      * Joomla specific reference layouts.

      * [`templates/repos/joomla/component/`](templates/repos/joomla/component/index.md)

        * Joomla component reference repository.
        * Demonstrates manifests, packaging, docs, and CI integration.

    * [`templates/repos/generic/`](templates/repos/generic/index.md)

      * Platform agnostic reference repository layout.
      * Used when no domain specific scaffold applies.

### Documentation templates

* [`templates/docs/`](templates/docs/index.md)

  * Markdown templates aligned with standards defined in `docs/`.
  * Includes policy templates, guidance templates, checklists, glossaries, and sample document structures.
  * Intended to accelerate creation of compliant documentation without redefining standards.

### Script templates

* [`templates/scripts/`](templates/scripts/index.md)

  * Example validation, CI, and utility scripts.
  * Scripts are designed to be portable and adaptable.
  * Downstream repositories may vendor, mirror, or reimplement these scripts as needed.

### GitHub templates and workflows

* **Public workflow templates**: [`.github/workflows/templates/`](.github/workflows/templates/README.md)

  * CI/CD workflow templates for Joomla and generic projects
  * Repository health monitoring workflows
  * Version branch automation

* **Private GitHub templates**: Maintained in separate repository `mokoconsulting-tech/MokoStandards-github-private`

  * CODEOWNERS files
  * Issue templates
  * Pull request templates
  * Internal workflow configurations
  * Separation ensures confidential organizational templates remain private

### Repository reference layouts

* [`templates/repos/joomla/component/`](templates/repos/joomla/component/index.md)

  * Reference repository layout for Joomla components.
  * Demonstrates expected folder structure, manifest placement, documentation layout, and CI integration points.
  * Does not replace Joomla specific standards documents.

* [`templates/repos/generic/`](templates/repos/generic/index.md)

  * Reference repository layout for non Joomla and non Dolibarr projects.
  * Serves as a baseline when no domain specific scaffold applies.
  * Emphasizes portability, minimal assumptions, and CI friendliness.

### Design principles

* Standards are defined once and referenced everywhere.
* Templates illustrate standards but never override them.
* Folder intent must be obvious without external documentation.
* Layout stability is prioritized over short term convenience.

## Minimum compliance requirements

### Repository structure

* Source code lives in `src/`.
* Documentation lives in `docs/`.
* Build and validation scripts live in `scripts/`.

### Formatting requirements

* Tabs are not permitted in files unless the language syntax requires it.
* Path separators must use `/` when represented in configuration, manifests, and documentation.
* CI should fail releases when compliance checks fail.

### Header and metadata requirements

All source and documentation files must meet the Moko Consulting header and file information standard unless explicitly exempted.

Exemptions:

* JSON files must not contain injected comment headers.

## How this repository should be used

Downstream repositories of any type must treat MokoStandards as the authoritative source for coding, documentation, governance, and CI requirements.

Key expectations:

* Standards are not redefined downstream.
* Deviations require explicit documentation and approval.
* CI enforcement is the preferred adoption mechanism.

## Roadmap

See the authoritative roadmap document: [`/docs/ROADMAP.md`](docs/ROADMAP.md).

---

## Metadata

* Document: README.md
* Repository: [https://github.com/mokoconsulting-tech/MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards)
* Owner: Moko Consulting
* Scope: Coding standards and cross repository index
* Lifecycle: Active
* Audience: Engineering, maintainers, reviewers

## Revision History

| Version  | Date       | Author                          | Notes                                                            |
| -------- | ---------- | ------------------------------- | ---------------------------------------------------------------- |
| 01.00.00 | 2025-12-17 | Jonathan Miller (@jmiller-moko) | Initial standards first rebaseline and ecosystem linking.        |
| 04.01.00 | 2026-01-03 | Jonathan Miller (@jmiller-moko) | Version alignment with current MokoStandards standards baseline. |
