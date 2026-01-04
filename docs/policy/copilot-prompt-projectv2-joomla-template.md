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
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
(./LICENSE.md).

# FILE INFORMATION
DEFGROUP: Governance.GitHub
INGROUP: MokoStandards
REPO: https://github.com/mokoconsulting-tech/MokoStandards
FILE: copilot-prompt-projectv2-joomla-template.md
VERSION: 01.00.00
BRIEF: GitHub Copilot prompt to provision a GitHub Projects V2 template for Joomla template repositories.
PATH: /docs/policy/copilot-prompt-projectv2-joomla-template.md
NOTE:
-->

# GitHub Copilot Prompt: ProjectV2 Template Provisioning for Joomla Extension Projects (mokoconsulting-tech)

## Purpose

This document provides a comprehensive GitHub Copilot prompt for provisioning GitHub Projects V2 templates tailored to Joomla extension development within the **mokoconsulting-tech** organization. The objective is to establish standardized project management structures that support consistent tracking, reporting, and governance across all Joomla extension types.

## Scope

This prompt applies to the following Joomla extension types:

* Templates
* Components
* Modules
* Plugins
* Libraries

Each extension type requires a dedicated ProjectV2 template with shared baseline schemas and type-specific customizations to ensure coherent org-level reporting while accommodating the unique characteristics of each extension type.

## Role and Operating Constraints

You are GitHub Copilot acting as a repository automation engineer for the GitHub organization **mokoconsulting-tech**.

Operate with these guardrails:

* Do not overwrite compliant existing artifacts.
* Prefer additive changes and minimal diffs.
* Treat **MokoStandards** as the authoritative governance and standards baseline for structure, headers, versioning, and CI conventions.
* Use **GPL-3.0-or-later** SPDX compliance for all generated files that are eligible for headers.
* When generating markdown policy documents, include a copyright header and FILE INFORMATION block as an HTML comment at the top, and include **Metadata** and **Revision History** sections at the bottom.

## Objective

Provision **separate GitHub Projects V2 templates per Joomla extension type** in **mokoconsulting-tech**, using a shared baseline schema and consistent governance controls.

Extension types in scope:

* Templates
* Components
* Modules
* Plugins
* Libraries

Each extension type must have:

* A dedicated ProjectV2 template (name, fields, views, automations).
* Consistent reporting semantics across templates (so org-level rollups remain coherent).
* A repeatable implementation pattern (so the org can apply it to new repos consistently).

## Inputs

Assume the target repo is a Joomla template repository with conventions similar to:

* Repository name: `moko-cassiopeia` (or similar `moko-*` naming)
* Source path: `/src/`
* Packaging outputs: `/dist/` (if present)
* Documentation root: `/docs/`
* GitHub workflows: `/.github/workflows/`

## Deliverables

Produce:

1. A **ProjectV2 template specification** (as a markdown document) that includes:

   * Custom fields, their types, allowed values, and default behaviors.
   * Views and their filters, grouping, and sort rules.
   * Automation rules.
   * Naming standards.

2. A **GitHub CLI implementation guide** (commands and steps) to:

   * Create the project.
   * Create custom fields.
   * Create views.
   * Apply defaults.

3. A **repository adoption checklist** that maps:

   * Common work items in Joomla template repos to the project fields.
   * How to link Issues and PRs.

## Project Template Naming

Create **one ProjectV2 template per extension type**, using this naming and short code standard:

* Templates

  * Project name: `Delivery: Joomla Templates (Standard)`
  * Short code: `joomla-template-standard`

* Components

  * Project name: `Delivery: Joomla Components (Standard)`
  * Short code: `joomla-component-standard`

* Modules

  * Project name: `Delivery: Joomla Modules (Standard)`
  * Short code: `joomla-module-standard`

* Plugins

  * Project name: `Delivery: Joomla Plugins (Standard)`
  * Short code: `joomla-plugin-standard`

* Libraries

  * Project name: `Delivery: Joomla Libraries (Standard)`
  * Short code: `joomla-library-standard`

Project naming requirements:

* Names must be stable and reused exactly as the template identity.
* Short code must be unique per template and used in automation scripts, documentation, and repo onboarding.

## Shared Baseline vs Type-Specific Customization

All templates must use the **Shared Baseline Fields** and **Shared Views** below.

Then, each extension type must apply its own **Type-Specific Fields**, **Type-Specific Views**, and **Type-Specific Seed Items**.

## Joomla Extension Types (Scope)

This ProjectV2 template **must support all Joomla extension types**:

* Template
* Component
* Module
* Plugin
* Library

The project schema and views must remain generic and reusable across all extension types.

## Custom Fields (Required)

### Shared Baseline Fields (apply to all extension-type templates)

#### 1) Status

* Type: Single select
* Options (in this order):

  * Triage
  * Ready
  * In Progress
  * Blocked
  * In Review
  * QA
  * Released
  * Done
* Default: `Triage`

#### 2) Priority

* Type: Single select
* Options:

  * P0
  * P1
  * P2
  * P3
* Default: `P2`

#### 3) Work Type

* Type: Single select
* Options:

  * Bug
  * Enhancement
  * Task
  * Refactor
  * Documentation
  * Compliance
  * Release
* Default: `Task`

#### 4) Scope

* Type: Single select
* Options:

  * Repo
  * Cross-Repo
  * Org
* Default: `Repo`

#### 5) Repo

* Type: Text
* Value rule: store `owner/repo` (example: `mokoconsulting-tech/moko-cassiopeia`)

#### 6) Path

* Type: Text
* Value rule: filesystem path relevant to the item (example: `/src/templateDetails.xml`)

#### 7) Version Target

* Type: Text
* Value rule: `XX.YY.ZZ` (example: `03.05.00`)

#### 8) Release Channel

* Type: Single select
* Options:

  * Dev
  * RC
  * Prod
* Default: `Dev`

#### 9) Effort

* Type: Number
* Meaning: abstract points for throughput tracking (1 to 13)

#### 10) Risk

* Type: Single select
* Options:

  * Low
  * Medium
  * High
* Default: `Low`

#### 11) Compliance Impact

* Type: Single select
* Options:

  * None
  * License
  * Security
  * Privacy
  * Audit
* Default: `None`

#### 12) Owner

* Type: People

#### 13) Due Date

* Type: Date

#### 14) Milestone

* Type: Text
* Meaning: sprint, release, or initiative label (example: `Q1-Release`, `Sprint-07`)

### Type-Specific Fields (apply per extension-type template)

#### Templates: Component Area

* Field name: `Component Area`
* Type: Single select
* Options:

  * Template
  * Language
  * Assets
  * Build
  * CI
  * Packaging
  * Docs
  * Governance
* Default: `Template`

#### Components: Component Area

* Field name: `Component Area`
* Type: Single select
* Options:

  * Admin
  * Site
  * API
  * Database
  * Migrations
  * Language
  * Assets
  * Build
  * CI
  * Packaging
  * Docs
  * Governance
* Default: `Site`

#### Modules: Component Area

* Field name: `Component Area`
* Type: Single select
* Options:

  * Module
  * Layouts
  * Language
  * Assets
  * Build
  * CI
  * Packaging
  * Docs
  * Governance
* Default: `Module`

#### Plugins: Component Area

* Field name: `Component Area`
* Type: Single select
* Options:

  * Plugin
  * Group
  * Events
  * Language
  * Assets
  * Build
  * CI
  * Packaging
  * Docs
  * Governance
* Default: `Plugin`

#### Libraries: Component Area

* Field name: `Component Area`
* Type: Single select
* Options:

  * Library
  * Autoloading
  * Dependencies
  * API Surface
  * Tests
  * Build
  * CI
  * Packaging
  * Docs
  * Governance
* Default: `Library`

#### Plugins: Plugin Group

* Field name: `Plugin Group`
* Type: Text
* Value rule: Joomla plugin group (example: `system`, `content`, `user`)

#### Modules: Position

* Field name: `Position`
* Type: Text
* Value rule: typical module position(s) if relevant

#### Components: Install Surface

* Field name: `Install Surface`
* Type: Single select
* Options:

  * Fresh Install
  * Update
  * Both
* Default: `Both`

#### Libraries: Dependency Mode

* Field name: `Dependency Mode`
* Type: Single select
* Options:

  * Bundled
  * Composer
  * Mixed
* Default: `Composer`

## Views (Required)

### Shared Views (apply to all extension-type templates)

#### View A: Delivery Board

* Layout: Board
* Group by: Status
* Filter: `Status != Done`
* Sort: Priority ascending (P0 first), then Due Date ascending
* Visible fields: Priority, Work Type, Component Area, Version Target, Owner, Due Date

#### View B: Release Readiness

* Layout: Table
* Filter:

  * `Work Type = Release OR Status = Released OR Status = QA OR Component Area = Packaging`
* Sort: Version Target ascending, then Status
* Visible fields: Status, Version Target, Release Channel, Risk, Compliance Impact, Owner

#### View C: Compliance and Governance

* Layout: Table
* Filter:

  * `Work Type = Compliance OR Component Area = Governance OR Compliance Impact != None`
* Group: Compliance Impact
* Sort: Risk descending, then Status
* Visible fields: Status, Compliance Impact, Risk, Repo, Path, Owner

#### View D: Engineering Backlog

* Layout: Table
* Filter: `Status = Triage OR Status = Ready`
* Sort: Priority ascending, then Effort ascending
* Visible fields: Priority, Effort, Work Type, Component Area, Repo, Owner

#### View E: Cross-Repo Portfolio

* Layout: Roadmap
* Scope: multi-repo
* Group: Repo
* Date field: Due Date
* Filter: `Scope != Repo`

### Type-Specific Views (apply per extension-type template)

#### Templates: Theme Quality Gate

* Layout: Table
* Filter:

  * `Component Area = Assets OR Component Area = Template OR Component Area = Accessibility`
* Visible fields: Status, Priority, Component Area, Path, Owner

#### Components: DB and Migrations

* Layout: Table
* Filter:

  * `Component Area = Database OR Component Area = Migrations OR Work Type = Compliance`
* Visible fields: Status, Install Surface, Risk, Version Target, Owner

#### Modules: Positions and Layouts

* Layout: Table
* Filter:

  * `Component Area = Module OR Component Area = Layouts`
* Visible fields: Status, Position, Version Target, Owner

#### Plugins: Events and Grouping

* Layout: Table
* Filter:

  * `Component Area = Plugin OR Component Area = Events OR Plugin Group != ""`
* Visible fields: Status, Plugin Group, Version Target, Owner

#### Libraries: API Surface and Dependencies

* Layout: Table
* Filter:

  * `Component Area = API Surface OR Component Area = Dependencies OR Dependency Mode != ""`
* Visible fields: Status, Dependency Mode, Version Target, Owner

## Automation Rules (Required)

Configure these automation behaviors for **each extension-type template**.

### Shared Automation (apply to all templates)

1. New Issue intake

* When an Issue is added to the project:

  * Set Status to `Triage`.
  * If label contains `bug`, set Work Type to `Bug`.
  * If label contains `docs`, set Work Type to `Documentation`.
  * If label contains `compliance`, set Work Type to `Compliance`.

2. PR lifecycle

* When a PR is linked to an item:

  * Set Status to `In Review`.
* When a PR is merged:

  * Set Status to `QA`.

3. Release closure

* When label `released` is applied:

  * Set Status to `Released`.
* When label `done` is applied:

  * Set Status to `Done`.

### Type-Specific Automation (apply per template)

* Templates

  * If label contains `a11y` or `accessibility`, set Component Area to `Assets`.

* Components

  * If label contains `db` or `migration`, set Component Area to `Migrations`.
  * If label contains `admin`, set Component Area to `Admin`.

* Modules

  * If label contains `layout`, set Component Area to `Layouts`.

* Plugins

  * If label contains `group:`, set Plugin Group from the label suffix when possible.

* Libraries

  * If label contains `composer`, set Dependency Mode to `Composer`.

## Standard Work Item Patterns (for Joomla Extensions)

Seed each template with a **detailed, copy-ready task library**. These items are intended to be duplicated into active work and tracked through delivery.

### Shared Tasks (all extension types)

* Bootstrap repository from MokoStandards repo template

  * Work Type: Task
  * Component Area: Governance
  * Compliance Impact: Audit
  * Tasks:

    * Copy the appropriate repo scaffold from `MokoStandards/templates/repo/joomla/` for the extension type
    * If the repository uses the `templates/repos/joomla/` directory structure, use that canonical path instead
    * Confirm required top-level files exist: README.md, CHANGELOG.md, LICENSE.md, CONTRIBUTING.md, GOVERNANCE.md, CODE_OF_CONDUCT.md, CODEOWNERS
    * Confirm docs index files exist and are linked: `/docs/index.md` and folder index files where applicable
    * Confirm workflows exist under `/.github/workflows/` and align to MokoStandards validation scripts
    * Commit with a message that identifies the scaffold source path and version

* Validate manifest XML structure and metadata

  * Work Type: Compliance
  * Component Area: Governance
  * Compliance Impact: Audit
  * Tasks:

    * Confirm manifest XML wellformed and schema-compliant
    * Verify name, version, creationDate, author, and license fields
    * Confirm version alignment with CHANGELOG and CI variables

* Enforce SPDX license headers

  * Work Type: Compliance
  * Component Area: Governance
  * Compliance Impact: License
  * Tasks:

    * Scan PHP, XML, JS, CSS files for GPL-3.0-or-later headers
    * Validate FILE INFORMATION blocks where required
    * Confirm no forbidden comment styles are used

* CI validation coverage

  * Work Type: Compliance
  * Component Area: CI
  * Compliance Impact: Audit
  * Tasks:

    * XML wellformed validation
    * PHP syntax and lint checks
    * Version alignment validation
    * Secret scanning and path validation

* Release packaging verification

  * Work Type: Task
  * Component Area: Packaging
  * Tasks:

    * Validate ZIP root structure
    * Confirm no nested src/ paths in artifacts
    * Verify install and uninstall behavior in clean Joomla instance

### Templates: Detailed Tasks

* Template accessibility audit

  * Work Type: Compliance
  * Component Area: Assets
  * Compliance Impact: Accessibility
  * Tasks:

    * Validate WCAG color contrast
    * Confirm semantic HTML usage
    * Verify keyboard navigation support

* Asset pipeline integrity

  * Work Type: Task
  * Component Area: Assets
  * Tasks:

    * Validate compiled CSS and JS outputs
    * Confirm source maps excluded from production packages
    * Verify media assets paths and licensing

* Language override validation

  * Work Type: Task
  * Component Area: Language
  * Tasks:

    * Confirm en-GB baseline language files
    * Validate overrides load correctly
    * Verify no untranslated strings remain

### Components: Detailed Tasks

* Install and update SQL verification

  * Work Type: Compliance
  * Component Area: Database
  * Compliance Impact: Audit
  * Tasks:

    * Validate install.sql and update scripts
    * Confirm idempotent migrations
    * Test upgrades from previous minor and patch versions

* Admin and site permission checks

  * Work Type: Task
  * Component Area: Admin
  * Tasks:

    * Validate ACL definitions
    * Confirm admin menu visibility
    * Verify site routes respect permissions

* API surface stability review

  * Work Type: Compliance
  * Component Area: API
  * Compliance Impact: Audit
  * Tasks:

    * Identify public methods and services
    * Validate backward compatibility
    * Document breaking changes if any

### Modules: Detailed Tasks

* Module position validation

  * Work Type: Task
  * Component Area: Module
  * Tasks:

    * Confirm documented module positions
    * Validate rendering in common templates
    * Test caching behavior

* Layout override compatibility

  * Work Type: Task
  * Component Area: Layouts
  * Tasks:

    * Validate layout overrides load correctly
    * Confirm compatibility with core Joomla templates

### Plugins: Detailed Tasks

* Plugin group and event coverage

  * Work Type: Task
  * Component Area: Events
  * Tasks:

    * Validate plugin group registration
    * Confirm subscribed events fire correctly
    * Verify graceful failure when dependencies are missing

* Update and uninstall safety

  * Work Type: Compliance
  * Component Area: Plugin
  * Compliance Impact: Audit
  * Tasks:

    * Confirm no orphaned records remain on uninstall
    * Validate update scripts execute safely

### Libraries: Detailed Tasks

* Dependency strategy validation

  * Work Type: Compliance
  * Component Area: Dependencies
  * Compliance Impact: License
  * Tasks:

    * Confirm Composer dependencies and versions
    * Validate bundled dependencies licensing
    * Ensure no duplicate class loading

* Autoloading and namespace audit

  * Work Type: Task
  * Component Area: Autoloading
  * Tasks:

    * Validate PSR-4 mappings
    * Confirm namespaces match directory structure

* Backward compatibility contract

  * Work Type: Compliance
  * Component Area: API Surface
  * Compliance Impact: Audit
  * Tasks:

    * Identify public API boundaries
    * Validate semantic versioning adherence
    * Document deprecated APIs

## Implementation Guidance

### GitHub CLI Commands

To provision a ProjectV2 template using the GitHub CLI (`gh`), follow these steps:

1. Create the project:

   ```bash
   gh project create --org mokoconsulting-tech --title "Delivery: Joomla Templates (Standard)"
   ```

2. Create custom fields:

   ```bash
   # Single select fields
   gh project field-create <project-number> --name "Status" --data-type "SINGLE_SELECT" --single-select-options "Triage,Ready,In Progress,Blocked,In Review,QA,Released,Done"
   
   gh project field-create <project-number> --name "Priority" --data-type "SINGLE_SELECT" --single-select-options "P0,P1,P2,P3"
   
   # Text fields
   gh project field-create <project-number> --name "Repo" --data-type "TEXT"
   
   gh project field-create <project-number> --name "Path" --data-type "TEXT"
   
   # Number fields
   gh project field-create <project-number> --name "Effort" --data-type "NUMBER"
   
   # Date fields
   gh project field-create <project-number> --name "Due Date" --data-type "DATE"
   ```

3. Create views with filters and sorting through the GitHub web interface, as the CLI has limited support for view configuration.

4. Configure automation rules through the GitHub Projects web interface under project settings.

### Repository Adoption Checklist

For repositories adopting this ProjectV2 template:

1. Link the repository to the appropriate ProjectV2 template based on extension type.
2. Configure automatic issue and PR linking in repository settings.
3. Apply appropriate labels to issues to trigger automation rules.
4. Seed initial work items from the Standard Work Item Patterns section.
5. Customize Component Area field options if needed for specific extension requirements.
6. Train team members on project field usage and workflow transitions.

## Compliance and Enforcement

ProjectV2 templates must be consistently applied across all Joomla extension repositories in the **mokoconsulting-tech** organization. Deviations require explicit approval and documented justification. Regular audits should verify template compliance and field usage consistency.

## Metadata

| Field         | Value                                                                                                        |
| ------------- | ------------------------------------------------------------------------------------------------------------ |
| Document Name | GitHub Copilot Prompt: ProjectV2 Template Provisioning for Joomla Extension Projects                        |
| Path          | /docs/policy/copilot-prompt-projectv2-joomla-template.md                                                    |
| Repo          | [https://github.com/mokoconsulting-tech/MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards) |
| Owner         | Moko Consulting                                                                                              |
| Status        | Active                                                                                                       |
| Last Reviewed | 2026-01-04                                                                                                   |

## Revision History

| Date       | Description                           | Author          |
| ---------- | ------------------------------------- | --------------- |
| 2026-01-04 | Initial policy creation and structure | Moko Consulting |
