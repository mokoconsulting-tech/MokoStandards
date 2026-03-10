<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
DEFGROUP: MokoStandards.Guide.WaaS
INGROUP: MokoStandards.WaaS
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/guide/waas/update-server-guide.md
VERSION: 04.00.05
BRIEF: How-to guide for creating and maintaining the Joomla extension update.xml in MokoWaaS repos
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.05-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Joomla Update Server Guide

This guide explains how to set up and maintain the `update.xml` Joomla update-server manifest in any MokoWaaS (Joomla) extension repository.

For the governing policy see [update-server.md](../../policy/waas/update-server.md).

---

## What Is an Update Server?

The [Joomla extension update server](https://docs.joomla.org/Deploying_an_Update_Server) is a mechanism that allows Joomla sites to check for new versions of installed extensions. The site's Joomla installer polls a URL declared in the extension's `manifest.xml` and retrieves an XML document listing available releases.

In MokoWaaS repos, the update server is a plain `update.xml` file committed at the **repository root** and served via GitHub's raw content CDN.

---

## Initial Setup (new repository)

The bulk sync system creates `update.xml` from `templates/joomla/update.xml.template` on the first sync. You still need to:

### 1. Add the update server to manifest.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<extension type="component" version="4.0" method="upgrade">
	<name>COM_MYEXTENSION</name>
	<author>Moko Consulting</author>
	<version>01.00.00</version>

	<!-- … other elements … -->

	<updateservers>
		<server type="extension" priority="1" name="My Extension">
			https://raw.githubusercontent.com/mokoconsulting-tech/REPO_NAME/main/update.xml
		</server>
	</updateservers>
</extension>
```

Replace `REPO_NAME` with the actual repository name.

### 2. Edit the generated update.xml

After bulk sync creates `update.xml`, replace the template tokens with real values:

| Token | Replace with |
|-------|-------------|
| `{{EXTENSION_NAME}}` | e.g. `My Extension` |
| `{{EXTENSION_ELEMENT}}` | e.g. `com_myextension` |
| `{{EXTENSION_TYPE}}` | `component`, `module`, `plugin`, or `template` |
| `{{VERSION}}` | Current version (must match `README.md`) |
| `{{DOWNLOAD_URL}}` | GitHub Releases asset URL for this version |
| `{{REPO_URL}}` | Full repository URL |
| `{{MAINTAINER_URL}}` | `https://mokoconsulting.tech` |

Example `update.xml` after token replacement:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- … header comment … -->
<updates>
	<update>
		<name>My Extension</name>
		<description>My Extension — Moko Consulting Joomla component</description>
		<element>com_myextension</element>
		<type>component</type>
		<version>01.00.00</version>
		<infourl title="Release Information">
			https://github.com/mokoconsulting-tech/my-extension/releases/tag/01.00.00
		</infourl>
		<downloads>
			<downloadurl type="full" format="zip">
				https://github.com/mokoconsulting-tech/my-extension/releases/download/01.00.00/com_myextension-01.00.00.zip
			</downloadurl>
		</downloads>
		<targetplatform name="joomla" version="4\.[0-9]+" />
		<php_minimum>7.4</php_minimum>
		<maintainer>Moko Consulting</maintainer>
		<maintainerurl>https://mokoconsulting.tech</maintainerurl>
	</update>
</updates>
```

> **Regex note:** The backslash in `version="4\.[0-9]+"` is a **literal backslash character** in the XML attribute value. Joomla's update-server parser treats this value as a regular expression, so `\.` matches a literal dot and `[0-9]+` matches one or more version digits. Do not double-escape it.

When you publish a new release, update `update.xml` before or at the same time as tagging.

### Manual steps (if not using the release workflow)

1. **Bump the version** in `README.md` (e.g. `01.00.00` → `01.00.01`).
2. **Update `manifest.xml`** — set `<version>01.00.01</version>`.
3. **Prepend a new `<update>` block** to `update.xml`:

```xml
<updates>
	<!-- New release — prepend here -->
	<update>
		<name>My Extension</name>
		<element>com_myextension</element>
		<type>component</type>
		<version>01.00.01</version>
		<infourl title="Release Information">
			https://github.com/mokoconsulting-tech/my-extension/releases/tag/01.00.01
		</infourl>
		<downloads>
			<downloadurl type="full" format="zip">
				https://github.com/mokoconsulting-tech/my-extension/releases/download/01.00.01/com_myextension-01.00.01.zip
			</downloadurl>
		</downloads>
		<targetplatform name="joomla" version="4\.[0-9]+" />
		<php_minimum>7.4</php_minimum>
		<maintainer>Moko Consulting</maintainer>
		<maintainerurl>https://mokoconsulting.tech</maintainerurl>
	</update>
	<!-- Existing entries below — do not delete -->
	<update>
		<version>01.00.00</version>
		…
	</update>
</updates>
```

4. **Commit** all three files in the same commit or PR.
5. **Tag** the commit: `git tag 01.00.01`.
6. **Create a GitHub Release** and attach the `com_myextension-01.00.01.zip` asset. The download URL in `update.xml` must match the exact asset filename.

### Using the release workflow (recommended)

The `joomla/release.yml.template` workflow automates steps 2–6. Run it from the Actions tab after merging your release PR. It:
- Builds the installable `.zip` package
- Creates a GitHub Release with the asset
- Updates `update.xml` using `UpdateXmlGenerator`
- Commits the updated `update.xml` back to `main`

---

## Version Alignment Check

Three values must always match:

```bash
# Quick check (run from repo root)
readme_ver=$(grep -oP '(?<=VERSION: )[\d.]+' README.md | head -1)
manifest_ver=$(grep -oP '(?<=<version>)[\d.]+(?=</version>)' manifest.xml | head -1)
update_ver=$(grep -oP '(?<=<version>)[\d.]+(?=</version>)' update.xml | head -1)

echo "README.md:    $readme_ver"
echo "manifest.xml: $manifest_ver"
echo "update.xml:   $update_ver"

[ "$readme_ver" = "$manifest_ver" ] && [ "$readme_ver" = "$update_ver" ] \
  && echo "✅ Versions aligned" || echo "❌ Version mismatch — fix before releasing"
```

The CI `validate_manifest.sh` script runs this check on every PR.

---

## Testing update.xml

### Test with curl

```bash
curl -I https://raw.githubusercontent.com/mokoconsulting-tech/REPO_NAME/main/update.xml
# Expect: HTTP/2 200 with Content-Type: text/plain; charset=utf-8
```

### Test with Joomla

1. Install the extension on a Joomla 4.x test site.
2. Navigate to **System → Update → Extensions**.
3. Click **Find Updates**.
4. The extension should appear with the latest version if `update.xml` is reachable and valid.

### Validate XML structure

```bash
xmllint --noout update.xml && echo "✅ Valid XML" || echo "❌ XML syntax error"
```

---

## Common Mistakes

| Mistake | Effect | Fix |
|---------|--------|-----|
| Deleting old `<update>` entries | Joomla can't resolve upgrade from older versions | Always prepend, never delete |
| `<downloadurl>` points to a draft release | Joomla gets a 302 redirect to login page | Only use published release asset URLs |
| Forgetting to bump `<version>` in `manifest.xml` | Joomla sees no update (installed == server version) | Always update all three files in the same commit |
| Using `version="4"` without the regex | Only Joomla 4.x (not 4.1, 4.2 …) matches | Use `version="4\.[0-9]+"` |
| Using a relative URL in `manifest.xml` `<updateservers>` | Joomla rejects non-HTTPS URLs | Use the full `https://raw.githubusercontent.com/…` URL |

---

## Related Documentation

| Document | Purpose |
|----------|---------|
| [update-server.md](../../policy/waas/update-server.md) | Policy: requirements and enforcement |
| [joomla-development-guide.md](joomla-development-guide.md) | Full extension development guide |
| [development-standards.md](../../policy/waas/development-standards.md) | Coding and architecture standards |

## Metadata

| Field         | Value |
|---------------|-------|
| Document Type | Guide |
| Domain        | WaaS / Joomla |
| Applies To    | All MokoWaaS (Joomla) repositories |
| Owner         | Moko Consulting |
| Repo          | https://github.com/mokoconsulting-tech/MokoStandards |
| Path          | /docs/guide/waas/update-server-guide.md |
| Version       | 04.00.05 |
| Status        | Active |
| Last Reviewed | 2026-03-09 |
