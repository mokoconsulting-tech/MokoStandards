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
DEFGROUP: MokoStandards.Guide
INGROUP: MokoStandards.Documentation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/guide/ai-client-setup.md
VERSION: XX.YY.ZZ
BRIEF: How to set up AI coding agent context files for all major AI clients in governed repositories
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.04-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# AI Coding Agent Setup Guide

Every major AI coding assistant reads a **context file** from your repository at session start. Without it the assistant guesses at your conventions and produces suggestions that violate standards, use the wrong language, or skip required headers. This guide explains where each client's context file lives, what to put in it, and provides copy-paste prompt templates tuned for this codebase.

## Table of Contents

1. [Why Context Files Matter](#why-context-files-matter)
2. [GitHub Copilot — `.github/copilot-instructions.md`](#github-copilot)
3. [Claude Code — `CLAUDE.md`](#claude-code)
4. [Cursor — `.cursor/rules`](#cursor)
5. [Aider — `.aider.conf.yml`](#aider)
6. [Other Clients](#other-clients)
7. [Suggested Prompts for This Codebase](#suggested-prompts-for-this-codebase)
8. [Keeping Context Files in Sync](#keeping-context-files-in-sync)

---

## Why Context Files Matter

AI clients have no memory between sessions. Without a context file they do not know:

- That `api/` is PHP-only and new scripts must extend `CliFramework`
- That `declare(strict_types=1)` and a FILE INFORMATION header are required on every PHP file
- That branch names must follow `prefix/MAJOR.MINOR.PATCH` format
- That version numbers belong only in the file header and badge, not body text
- That `docs/policy/` is for binding policy, `docs/guide/` is for how-to, and `templates/` syncs to other repos

A well-written context file eliminates these recurring review comments and speeds up contribution significantly.

---

## GitHub Copilot

### What Is the Copilot Coding Agent File?

GitHub Copilot reads **`.github/copilot-instructions.md`** at the start of every Copilot Chat session and Copilot coding agent task in your repository. It applies to:

- Copilot Chat in VS Code, JetBrains, and the GitHub web UI
- GitHub Copilot coding agent (automated PR work)
- Copilot Workspace

It is distinct from `.github/copilot.yml`, which controls allowed domains and file inclusion — `copilot-instructions.md` is the *behavioural* context.

### Where to Create It

```
your-repo/
└── .github/
    └── copilot-instructions.md   ← create this file
```

This repository already has one at [`.github/copilot-instructions.md`](../../.github/copilot-instructions.md). Use it as a reference or copy it as a starting point for governed repositories.

### Minimal Template for a Governed Repository

```markdown
# <RepoName> — GitHub Copilot Custom Instructions

## What This Repo Is
<One paragraph: what it does, what it is not, GitHub URL.>

## Primary Language
<e.g. "PHP 8.1+ — all new scripts in src/ must use declare(strict_types=1)">

## File Header — Always Required
<Paste the minimal header template for the dominant file type.>

## Script / Class Structure
<Paste the canonical class/script skeleton — e.g. extends CliFramework pattern.>

## Naming Conventions
| Context | Convention | Example |
|---------|-----------|---------|

## Commit Messages
Format: `<type>(<scope>): <subject>`
Types: feat · fix · docs · chore · ci · refactor · style · test · perf · revert · build

## Branch Naming
<Format and examples, e.g. prefix/MAJOR.MINOR.PATCH/description>

## Validation Commands
<Exact commands to run before committing.>

## Key Constraints
<Short bullet list of things Copilot must never do in this repo.>
```

### Tips for Writing Good Copilot Instructions

- **Be explicit about what NOT to do** — Copilot responds well to negative constraints.
- **Paste real skeletons** — give the exact class or script template, not a description of it.
- **List forbidden functions** — e.g. "Never use `var_dump`, `print_r`, `eval`."
- **Keep it under ~200 lines** — Copilot's context window processes the file fully; shorter is faster.
- **Use markdown tables** for naming conventions — they are compact and unambiguous.

---

## Claude Code

### What Is `CLAUDE.md`?

Claude Code (`claude` CLI) reads **`CLAUDE.md`** from the repository root (and from any subdirectory you run it from) at session start. It gives Claude a complete operational picture so it can contribute without asking basic questions about conventions.

This repository's `CLAUDE.md` lives at `.github/CLAUDE.md` — see [`.github/CLAUDE.md`](../../.github/CLAUDE.md).

### Where to Create It

```
your-repo/
├── .github/
│   ├── CLAUDE.md       ← primary context file, read at every session start
│   └── …
└── src/
    └── CLAUDE.md       ← optional subdirectory context (read when Claude runs from src/)
```

Claude Code also reads `~/.claude/CLAUDE.md` for user-level preferences, and any `CLAUDE.md` in parent directories up to the home directory.

### Precedence Order

1. `~/.claude/CLAUDE.md` — user-level (personal preferences, API keys style, etc.)
2. `.github/CLAUDE.md` — project-level ← **put repo conventions here**
3. Subdirectory `CLAUDE.md` — directory-level overrides

### Required Sections (per MokoStandards policy)

Every `CLAUDE.md` in a governed repository must include:

| Section | Content |
|---------|---------|
| **What This Repo Is** | One paragraph: purpose, audience, what it is NOT, GitHub URL |
| **Repo Structure** | Annotated two-level directory tree |
| **File Header Requirements** | Minimal and full header templates per language |
| **Coding Standards** | Indentation, line length, naming per language |
| **Commit Message Format** | Exact format from `.gitmessage` |
| **Running Validation** | Exact commands to run before committing |
| **Contribution Workflow** | Fork → branch → validate → commit → PR |
| **What NOT to Do** | Explicit prohibitions for this repo |

Omit sections that do not apply. Do not add generic advice.

### Minimal Template for a Governed Repository

````markdown
# What This Repo Is
<One paragraph.>

# Repo Structure
```
repo-root/
├── src/        # Application source
└── docs/       # Documentation
```

# File Header Requirements
<Templates per language.>

# Coding Standards
<From .editorconfig and linter configs.>

# Commit Message Format
<From .gitmessage.>

# Running Validation
```bash
# Exact commands here
```

# What NOT to Do
- Never …
````

---

## Cursor

### What Is the Cursor Rules File?

Cursor reads **`.cursor/rules`** (one file per rule set, stored in `.cursor/rules/`) or a legacy **`.cursorrules`** file at the repository root. Rules are applied to all AI interactions within the Cursor editor for that project.

### Where to Create It

**Current format (Cursor 0.43+):**
```
your-repo/
└── .cursor/
    └── rules/
        ├── general.mdc      ← always applied
        ├── php.mdc          ← applied when editing PHP files (set glob: **/*.php)
        └── docs.mdc         ← applied when editing Markdown files
```

**Legacy format (still supported):**
```
your-repo/
└── .cursorrules             ← single file, always applied
```

### Minimal Template (`.cursor/rules/general.mdc`)

```markdown
---
description: General coding rules for this repository
globs: ["**/*"]
alwaysApply: true
---

# <RepoName> Coding Rules

## Primary Language
<Language and version.>

## Required File Header
<Header template.>

## Naming Conventions
<Table.>

## Forbidden Patterns
- Never …
```

---

## Aider

### What Is the Aider Context File?

Aider reads **`CONVENTIONS.md`** (or any file you specify with `--read`) and its configuration from **`.aider.conf.yml`**. The most reliable approach is to add your conventions file to the persistent read list.

### Where to Create It

```
your-repo/
├── CONVENTIONS.md          ← conventions doc (can reuse CLAUDE.md content)
└── .aider.conf.yml         ← aider configuration
```

**`.aider.conf.yml`:**
```yaml
# Always load the conventions document
read:
  - CONVENTIONS.md
  - docs/policy/coding-style-guide.md

# Model preference
model: claude-3-5-sonnet-20241022

# Git integration
auto-commits: false
dirty-commits: false
```

For this repository, `.github/CLAUDE.md` already contains all conventions. Point Aider at it:

```bash
aider --read .github/CLAUDE.md --model claude-3-5-sonnet-20241022
```

---

## Other Clients

| Client | Context File | Location |
|--------|-------------|----------|
| **GitHub Copilot** | `.github/copilot-instructions.md` | Repo root → `.github/` |
| **Claude Code** | `CLAUDE.md` | `.github/` (and subdirectories) |
| **Cursor** | `.cursor/rules/*.mdc` or `.cursorrules` | Repo root |
| **Aider** | `CONVENTIONS.md` + `.aider.conf.yml` | Repo root |
| **Codeium / Windsurf** | `.windsurfrules` | Repo root |
| **Amazon Q Developer** | `.amazonq/rules.md` | Repo root → `.amazonq/` |
| **JetBrains AI Assistant** | Reads open files / project context | No dedicated context file; use comments |
| **Cody (Sourcegraph)** | Reads repository index | Configure via Sourcegraph site admin |

For clients without a dedicated context file, keep a prominent `CONTRIBUTING.md` and encourage developers to paste its key sections into the chat at session start.

---

## Suggested Prompts for This Codebase

These prompts are specific to MokoStandards. Copy them into any AI client.

### Add a New Validation Script

```
Create a new PHP validation script at api/validate/check_<name>.php for this
MokoStandards repository. It must:
- Use the minimal file header with DEFGROUP: MokoStandards.Scripts.Validate
- Declare strict_types=1
- Extend CliFramework from api/lib/Enterprise/CliFramework.php
- Accept --path (default '.'), --json, and --dry-run arguments via configure()
- Initialize AuditLogger in initialize()
- Implement all logic in run() returning an integer exit code
- Include PHPDoc on all public methods
- Never use var_dump, print_r, or eval
The script should check <describe what to check>.
```

### Add a New Policy Document

```
Create a new policy document at docs/policy/<topic>.md for this MokoStandards
repository. It must:
- Start with the full HTML comment header (with GPL warranty disclaimer) using
  DEFGROUP: MokoStandards.Policy and INGROUP: MokoStandards.Documentation
- Follow the full header with a blank line then the version badge:
  [![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.04-blue)](https://github.com/mokoconsulting-tech/MokoStandards)
- Use tabs for indentation (not spaces)
- Not include any hardcoded version numbers in body text
- End with a ## Metadata table and a ## Revision History table
The policy should cover <describe the topic>.
```

### Add a New PHP Enterprise Library Class

```
Create a new PHP class at api/lib/Enterprise/<ClassName>.php for this
MokoStandards repository. It must:
- Use the minimal file header with DEFGROUP: MokoStandards.Library
- Declare strict_types=1
- Use namespace MokoStandards\Enterprise
- Follow PSR-12 coding standards
- Use constructor property promotion where appropriate (PHP 8.1+)
- Include PHPDoc on all public methods with @param, @return, and @throws
- Throw typed exceptions — never swallow errors silently
- Be autoloadable via the existing composer.json PSR-4 mapping
The class should implement <describe the purpose>.
```

### Add a New GitHub Actions Workflow for This Repo

```
Create a new GitHub Actions workflow at .github/workflows/<name>.yml for this
MokoStandards repository. It must:
- Start with the YAML file header using # comments with DEFGROUP: MokoStandards.CI
- Use 2-space indentation (spaces, not tabs — YAML requirement)
- Reference actions using pinned SHAs, not floating tags
- Include the standard permissions block at the top (contents: read)
- Follow the naming convention: kebab-case.yml
The workflow should <describe the trigger and purpose>.
```

### Sync Standards to a Governed Repository

```
I need to check whether the repository at <path> complies with MokoStandards.
Run the following and explain every failure:

  php api/validate/check_repo_health.php --path <path>
  php api/validate/check_version_consistency.php --path <path>
  php api/validate/scan_drift.php --path <path>

For each failure, show exactly what needs to change and why it matters
according to docs/policy/file-header-standards.md and docs/enforcement-levels.md.
```

### Understand the Enforcement System

```
Read docs/enforcement-levels.md and explain the six tiers — OPTIONAL, SUGGESTED,
REQUIRED, FORCED, NOT_SUGGESTED, and NOT_ALLOWED — using concrete examples of
files that fall into each tier in this repository. Explain the processing order
and what happens when a repository's .github/override.tf conflicts with a FORCED
or NOT_ALLOWED rule.
```

### Write or Update a CLAUDE.md / copilot-instructions.md for a Governed Repo

```
Generate a CLAUDE.md (for Claude Code) and a .github/copilot-instructions.md
(for GitHub Copilot) for the repository at <path>. Follow the structure defined
in docs/guide/ai-client-setup.md in the MokoStandards repository. Read the
actual .editorconfig, phpcs.xml, phpstan.neon, .gitmessage, and CONTRIBUTING.md
in the target repo before writing anything — do not guess at conventions.
```

### Add a Version Badge to a New Markdown File

```
This markdown file is missing a version badge. After the closing --> of the
HTML comment file header (or at the top if there is no header), add:

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.04-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

Ensure there is a blank line before and after the badge. Do not add any version
number anywhere else in the file body.
```

---

## Keeping Context Files in Sync

Context files become stale when standards change. Treat them like documentation — update them in the same PR as the standard they describe.

### Checklist: When to Update Context Files

- [ ] New required file header field added to `docs/policy/file-header-standards.md`
- [ ] New primary language introduced to a repo
- [ ] Branch naming convention changed in `docs/policy/branching-strategy.md`
- [ ] New validation command added or renamed
- [ ] New "never do" constraint established in policy
- [ ] New library class pattern established in `api/lib/Enterprise/`

### MokoStandards Bulk Sync

The bulk-sync workflow (`api/automation/bulk_sync.php`) can propagate a base `copilot-instructions.md` template from `templates/github/` to governed repositories. If you want custom instructions synced organisation-wide, add the template to that directory and set its enforcement level in the relevant `.tf` definition file.

---

## Related Documentation

| Document | Purpose |
|----------|---------|
| [`.github/CLAUDE.md`](../../.github/CLAUDE.md) | Claude Code context file for this repository — use as a reference |
| [`.github/copilot-instructions.md`](../../.github/copilot-instructions.md) | Copilot coding agent context for this repository |
| [`docs/policy/file-header-standards.md`](../policy/file-header-standards.md) | Full copyright-header rules for every file type |
| [`docs/guide/copilot-usage-guide.md`](copilot-usage-guide.md) | General Copilot usage tips and IDE setup |
| [`docs/policy/copilot-usage-policy.md`](../policy/copilot-usage-policy.md) | Acceptable use policy for GitHub Copilot |
| [`docs/policy/copilot-pre-merge-checklist.md`](../policy/copilot-pre-merge-checklist.md) | What to check before merging AI-assisted PRs |
| [`docs/enforcement-levels.md`](../enforcement-levels.md) | Six-tier enforcement system reference |
