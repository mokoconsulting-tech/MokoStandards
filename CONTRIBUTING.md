<!--
 Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>

 This file is part of a Moko Consulting project.

 SPDX-LICENSE-IDENTIFIER: GPL-3.0-or-later

 This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

 You should have received a copy of the GNU General Public License (./LICENSE).
 
 # FILE INFORMATION
 DEFGROUP: MokoStandards
 INGROUP: MokoStandards.Documentation
 REPO: https://github.com/mokoconsulting-tech/MokoStandards/
 VERSION: 05.00.00
 PATH: ./CONTRIBUTING.md
 BRIEF: How to contribute; commit, PR, testing and security policies
 NOTE: Short and practical; see README for overview
 -->
# Contributing

Thank you for your interest in contributing. This document defines the baseline expectations, workflows, and quality gates for any change entering this repository.

The objective is to keep contributions predictable, reviewable, and compliant with MokoStandards while enabling a sustainable delivery pipeline.

## Governance and scope

This CONTRIBUTING file operates alongside the following governance assets:

* `README.md` for project overview and onboarding
* `LICENSE` for legal terms and reuse constraints
* `CODE_OF_CONDUCT.md` for behavioral expectations
* `GOVERNANCE.md` (where present) for decision making, ownership, and escalation

In case of conflict, legal terms in `LICENSE` take precedence, followed by `GOVERNANCE.md` and then this document.

## Alignment with MokoStandards

All Moko Consulting projects are expected to comply with the shared standards defined in the `MokoStandards` repository.

* Source of truth: [https://github.com/mokoconsulting-tech/MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards)
* Areas covered: headers, licensing, coding style, documentation layout, and CI expectations

Per project policy, this file should reference standards rather than redefining them. Any deviation must be explicitly documented in `GOVERNANCE.md` or an architecture decision record (ADR).

## Ways to contribute

Contributions are welcome across multiple workstreams:

* Bug reports and defect reproduction scenarios
* Feature requests aligned with the project roadmap
* Code changes, including refactors and technical debt reduction
* Documentation improvements and clarifications
* Test coverage (unit, integration, and regression scenarios)
* Operational assets such as runbooks, deployment notes, and incident templates

Before investing significant effort, contributors are encouraged to review the open issues and roadmap documents to avoid misalignment.

## Communication channels

Typical communication paths include:

* GitHub Issues for bug reports, feature requests, and questions
* GitHub Discussions or equivalent for design conversations (where enabled)
* Pull Requests for change proposals

Project maintainers may document additional channels (for example, email, chat, or ticketing) in `README.md` or `GOVERNANCE.md`.

## Issue workflow

Use GitHub Issues as the system of record for all work.

When opening an issue:

1. Search existing issues to avoid duplication.
2. Select the appropriate issue template if available.
3. Provide a concise, action oriented title.
4. Supply a clear description including:

	* Expected behavior
	* Actual behavior
	* Minimal steps to reproduce
	* Environment details (version, platform, configuration)
5. Attach logs, screenshots, or configuration snippets as needed, after removing sensitive data.

Maintainers will triage issues based on impact, risk, and alignment with the roadmap. Not all requests will be accepted, but all will be reviewed in good faith.

## Pull request workflow

Pull Requests (PRs) are the primary integration path for changes.

Standard workflow:

1. Open or reference an issue describing the problem or enhancement.
2. Fork the repository or create a feature branch from the canonical default branch (commonly `main` or `master`).
3. Implement changes aligned with the coding standards and file header requirements.
4. Add or update tests to validate the behavior.
5. Update documentation where behavior, configuration, or interfaces change.
6. Run the full test and linting suite locally before opening the PR.
7. Open a PR with:

	* A precise, descriptive title
	* A summary of changes
	* Explicit linkage to the corresponding issue
	* Notes on testing performed and any known limitations

PRs must pass automated checks before they will be considered for review. The maintainer team reserves the right to request revisions, split changes, or defer work that does not align with the current release plan.

## Merge strategy

This repository uses **squash merge** as the only permitted merge method for pull requests to the main branch. This ensures a clean, linear git history where each commit represents a complete, reviewed change.

Key implications for contributors:

* **PR Title is Important**: The PR title becomes the commit message subject. Make it clear and descriptive.
* **PR Description is Important**: The PR description becomes the commit message body. Include rationale and summary of changes.
* **Automatic Cleanup**: Branches are automatically deleted after merge.
* **No Merge Commits**: Regular merge commits and rebase merges are disabled.

For complete details, see the [Merge Strategy Policy](docs/policy/merge-strategy.md).

## Branching and versioning

Unless specified otherwise in `GOVERNANCE.md` or a dedicated versioning policy:

* Default development branch: `main`
* Feature work: short lived feature branches named using a predictable convention, for example `feature/<short-description>` or `fix/<short-description>`
* Releases: tagged using semantic versioning (`MAJOR.MINOR.PATCH`)

Release specific branching, hotfix flows, and environment promotion rules should be documented in a separate Versioning and Branching Policy document when applicable.

## Coding standards and file headers

This project adheres to the coding conventions and header rules defined in MokoStandards. At a minimum:

* All source and configuration files must include the standard SPDX compatible header where applicable.
* Language specific style guides (for example PHP, JavaScript, Python) must be followed.
* INI files must use `;` for comments.
* CSS files must begin with `@charset "utf-8";`.
* JSON files must not include license headers, but must remain valid JSON.

Where a project introduces additional conventions, they should reference MokoStandards and document only the incremental rules.

## Commit message guidelines

Commit messages are part of the project audit trail. They should be structured and descriptive.

Recommended format:

* Short subject line in the imperative mood, for example `Add`, `Fix`, `Refactor`
* Optional body that explains the rationale, constraints, and side effects
* Reference to related issues using `Fixes #<id>` or `Refs #<id>` as appropriate

Avoid bundling unrelated changes into a single commit. Small, logically grouped commits improve traceability and rollback options.

## Testing expectations

Before opening a PR, contributors are expected to:

* Run all available automated tests (unit, integration, and other configured checks)
* Ensure linting and static analysis pass without new violations
* Confirm that documentation builds or site generation steps complete successfully, where applicable

For new features or non trivial fixes, please include tests that:

* Reproduce the defect, or
* Demonstrate the new behavior

If tests are not included, the PR should clearly state why (for example, infrastructure limitations, complex external dependencies, or pure documentation changes).

## Documentation contributions

Documentation is a first class asset in this ecosystem.

When contributing documentation:

* Align with the established docs hierarchy (for example `docs/` and `docs-extended/` where used)
* Apply the shared template structure for new documents
* Include appropriate navigation, metadata, and revision history sections when required by the documentation standards

Minor corrections such as typo fixes are welcome, but larger structural changes should be coordinated via an issue or design note first.

## Security and responsible disclosure

Security sensitive issues must not be reported in public issues.

If this repository defines a security contact channel (for example `SECURITY.md` or a dedicated email address), use that channel to share details.

Provide enough information for maintainers to reproduce and understand the impact. The team will coordinate fixes and disclosure timelines as appropriate.

## License and contributor agreement

Unless stated otherwise, contributions to this repository are accepted under the same license as the project, typically GPL 3.0 or later.

By submitting a contribution, you confirm that:

* You have the right to contribute the code or content.
* You agree that your contribution will be licensed under the project license.
* You will not submit content that infringes third party rights.

If the project later adopts a formal contributor license agreement (CLA) or additional terms, those requirements will be documented in `GOVERNANCE.md` or a dedicated `CLA` reference file.

## Escalation and decision making

If you disagree with a review decision or prioritization decision:

1. Engage constructively in the PR discussion and request clarification.
2. Reference any relevant governance rules or design records.
3. Where needed, request maintainer arbitration as documented in `GOVERNANCE.md`.

The objective is to maintain a collaborative, predictable contribution environment that supports long term maintainability and stakeholder trust.
