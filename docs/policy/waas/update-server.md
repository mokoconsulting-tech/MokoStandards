<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
DEFGROUP: MokoStandards.Policy.WaaS
INGROUP: MokoStandards.WaaS
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/policy/waas/update-server.md
VERSION: 04.00.05
BRIEF: Policy for the Joomla extension update server (update.xml) in all MokoWaaS repositories
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.05-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Joomla Extension Update Server Policy

## Purpose

This policy establishes requirements for implementing and maintaining the Joomla extension update server (`update.xml`) in all MokoWaaS repositories. The update server enables Joomla installations to detect and install new versions of Moko Consulting extensions automatically.

## Scope

This policy applies to:

- All MokoWaaS (Joomla) extension repositories governed by MokoStandards
- All Joomla extension types: components, modules, plugins, and templates

## Why update.xml Is Required

Joomla provides a built-in extension update mechanism. When a site administrator navigates to **System → Update → Extensions**, Joomla polls the update server URLs declared in each extension's `manifest.xml`. Without a valid `update.xml`, site administrators cannot receive automatic update notifications and must manually upload new packages — creating a security and maintenance risk.

All governed MokoWaaS extensions must therefore:
1. Declare an update server URL in `manifest.xml`
2. Maintain a valid `update.xml` file at that URL
3. Keep `update.xml` synchronised with every release

## Requirements

### 1. File Location

`update.xml` **must be placed at the repository root** (`/update.xml`). The bulk sync system creates it from `templates/joomla/update.xml.template` on first sync.

The publicly accessible URL (raw GitHub content) is used as the update server URL:

```
https://raw.githubusercontent.com/mokoconsulting-tech/{REPO_NAME}/main/update.xml
```

### 2. manifest.xml Declaration

Every extension `manifest.xml` **must** include an `<updateservers>` block pointing to the repository's `update.xml`:

```xml
<updateservers>
	<server type="extension" priority="1" name="{EXTENSION_NAME}">
		https://raw.githubusercontent.com/mokoconsulting-tech/{REPO_NAME}/main/update.xml
	</server>
</updateservers>
```

The `<server>` element attributes:

| Attribute | Required | Value |
|-----------|----------|-------|
| `type` | Yes | `extension` (use `collection` only for update-collections) |
| `priority` | Yes | `1` (single server) |
| `name` | Yes | Human-readable extension name |

### 3. update.xml Structure

Each `<update>` block **must** contain:

| Element | Required | Description |
|---------|----------|-------------|
| `<name>` | Yes | Human-readable extension name |
| `<description>` | No | Short description |
| `<element>` | Yes | Extension element (e.g. `com_example`, `mod_example`) |
| `<type>` | Yes | `component`, `module`, `plugin`, or `template` |
| `<version>` | Yes | Release version matching `manifest.xml` and `README.md` |
| `<infourl>` | No | GitHub Releases page URL |
| `<downloads>` → `<downloadurl>` | Yes | GitHub Releases asset download URL (direct .zip) |
| `<targetplatform>` | Yes | `name="joomla" version="4\.[0-9]+"` |
| `<php_minimum>` | No | Minimum PHP version (default `7.4`) |
| `<maintainer>` | No | `Moko Consulting` |
| `<maintainerurl>` | No | `https://mokoconsulting.tech` |

### 4. Version Alignment

Three artefacts **must always carry the same version string**:

| Artefact | Location |
|----------|----------|
| `README.md` | `FILE INFORMATION VERSION` field + badge |
| `manifest.xml` | `<version>` element |
| `update.xml` | `<version>` element in the most recent `<update>` block |

These are validated by the `standards-compliance.yml` workflow check `validate_manifest`.

### 5. Prepend-Only Policy for Releases

When a new release is published, a new `<update>` block **must be prepended** to `update.xml` — older entries must be **preserved** below it. This ensures that Joomla installations running older versions can still resolve their version and detect the upgrade path.

```xml
<updates>
	<!-- newest release first -->
	<update>
		<version>01.02.04</version>
		…
	</update>
	<!-- older releases below — do not delete -->
	<update>
		<version>01.02.03</version>
		…
	</update>
</updates>
```

### 6. Download URL Requirements

- The `<downloadurl>` must be a **publicly accessible** HTTPS URL.
- Use GitHub Releases asset URLs: `https://github.com/mokoconsulting-tech/{REPO}/releases/download/{VERSION}/{element}-{VERSION}.zip`
- Pre-release or draft URLs are not acceptable (they are not publicly accessible).
- URLs must return HTTP 200 with `Content-Type: application/zip`.

### 7. always_overwrite = false

`update.xml` is marked `always_overwrite = false` in the platform definition because:
- Each release prepends extension-specific download URLs that the bulk sync system cannot generate.
- Overwriting would destroy the release history.

The initial template is created by bulk sync; subsequent updates are the responsibility of the release workflow (`make release`) or the `joomla/release.yml.template` workflow.

## Enforcement

| Check | Workflow | Failure consequence |
|-------|----------|---------------------|
| `update.xml` exists at repo root | `standards-compliance.yml` check #18 | PR blocked |
| `<version>` in `update.xml` matches `manifest.xml` | `validate_manifest.sh` | PR blocked |
| `<version>` in `manifest.xml` matches `README.md` | `sync-version-on-merge.yml` | Version mismatch warning |
| `<downloadurl>` is reachable | Post-release integration test | Slack alert |

## Violations

| Violation | Consequence |
|-----------|-------------|
| Missing `update.xml` | `standards-compliance` workflow fails; PR blocked |
| Version mismatch between `update.xml`, `manifest.xml`, and `README.md` | `validate_manifest` check fails; PR blocked |
| Deleting historical `<update>` entries | PR review rejection |
| Inaccessible `<downloadurl>` | Post-release integration test failure; hotfix required |

## Related Documentation

| Document | Purpose |
|----------|---------|
| [update-server-guide.md](../../guide/waas/update-server-guide.md) | How-to: creating and maintaining update.xml |
| [joomla-development-guide.md](../../guide/waas/joomla-development-guide.md) | Full MokoWaaS extension development guide |
| [development-standards.md](development-standards.md) | Joomla/WaaS coding and architecture standards |
| [baseline-versioning.md](baseline-versioning.md) | Versioning policy for WaaS repositories |

## Metadata

| Field         | Value |
|---------------|-------|
| Document Type | Policy |
| Domain        | WaaS / Joomla |
| Applies To    | All MokoWaaS (Joomla) repositories |
| Owner         | Moko Consulting |
| Repo          | https://github.com/mokoconsulting-tech/MokoStandards |
| Path          | /docs/policy/waas/update-server.md |
| Version       | 04.00.05 |
| Status        | Active |
| Last Reviewed | 2026-03-09 |
| Reviewed By   | WaaS Development Lead |

## Revision History

| Date       | Author          | Change  | Notes |
|------------|-----------------|---------|-------|
| 2026-03-09 | Moko Consulting | Created | Initial policy — update.xml required in all MokoWaaS repos; waas-component.tf updated |
