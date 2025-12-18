<!--	Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>

	This file is part of a Moko Consulting project.

	SPDX-LICENSE-IDENTIFIER: GPL-3.0-or-later

	This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

	This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

	You should have received a copy of the GNU General Public License (./LICENSE.md).

	# FILE INFORMATION
	DEFGROUP:  MokoStandards
	INGROUP:  Documentation
	REPO:  https://github.com/mokoconsulting-tech/MokoStandards
	FILE:  style-guide.md
	VERSION:  2.0
	BRIEF:  Style Guide
	PATH:  ./docs/style-guide.md
	-->

# Style Guide

## Navigation

**You are here:** Documentation -> Style Guide

Related documents:

* [Documentation Index](./index.md)
* [Contributor Guide](./contributing.md)
* [Architecture Guide](./architecture.md)
* [API Reference](./api-reference.md)
* [Templates Index](./templates/index.md)

## 1. Purpose

The Style Guide defines the required formatting, grammar, documentation rules, naming conventions, and semantic structures used throughout all Moko Consulting documentation, codebases, and communications.

Consistency improves clarity, reduces ambiguity, and ensures all teams present unified, predictable artifacts.

## 2. General Writing Standards

### 2.1 Tone

* Clear, direct, and professional
* Avoid unnecessary jargon
* Use active voice

### 2.2 Grammar & Formatting

* Use American English
* Avoid long, dense paragraphs
* One sentence per line in documentation where clarity matters
* Prefer lists when enumerating concepts

### 2.3 Markdown Conventions

* Use `#` for top-level headers
* Start subsections at `##`
* Avoid HTML except when necessary
* Prefer fenced code blocks

## 3. Code Style Standards

### 3.1 Naming Conventions

* Classes -> PascalCase
* Functions -> snake_case
* Constants -> UPPER_SNAKE_CASE
* Files -> lowercase-hyphenated

### 3.2 Formatting

* 4-space indentation
* UTF-8 encoding
* LF line endings

### 3.3 Comments & Documentation

* Use clear inline comments
* Use docblocks for functions, classes, modules
* Include SPDX headers in all source files

## 4. Repository Structure Standards

All repositories must include:

* `README.md`
* `LICENSE.md`
* `CONTRIBUTING.md`
* `.editorconfig`
* `.gitignore`
* `docs/` folder

### 4.1 Documentation File Naming

Documentation files must:

* Use lowercase, hyphenated file names
* Start with `` prefix
* Live inside `/docs/`

## 5. Formatting for Technical Documents

Every technical document must include:

* SPDX header
* Navigation block
* Structured headings beginning at `#`
* Metadata block
* Revision history table

## 6. Diagrams & Visual Standards

### 6.1 Diagram Guidelines

* Use consistent symbols and colors
* Include legends
* Store diagrams in `docs/diagrams/`

### 6.2 File Formats

* PNG for raster
* SVG for vector
* Draw.io source files included where relevant

## 7. Accessibility Requirements

Documentation must:

* Pass contrast checks
* Include descriptive alt text
* Use readable font sizes in diagrams

## Metadata

```
Owner: Documentation Lead (role not created yet)
Reviewers: Governance, Architecture
Status: Active
Last Updated: <YYYY-MM-DD>
```

## Revision History

| Date       | Version | Author | Notes        |
| ---------- | ------- | ------ | ------------ |
| 2025-11-23 | 2.0.0   | TBD    | Initial stub |
