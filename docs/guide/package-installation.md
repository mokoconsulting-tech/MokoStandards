<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
DEFGROUP: MokoStandards.Guide
INGROUP: MokoStandards
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/guide/package-installation.md
VERSION: 04.00.15
BRIEF: Guide for installing the MokoStandards enterprise library in governed PHP repositories
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.15-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Installing the MokoStandards Package

This guide explains how to add the `mokoconsulting/mokostandards` Composer package to any governed PHP repository so it can use the enterprise libraries (CliFramework, ApiClient, RepositoryHealthChecker, etc.).

---

## Prerequisites

- PHP ≥ 8.1
- Composer ≥ 2.x
- `GH_TOKEN` environment variable set to your GitHub Personal Access Token (org-level secret)

---

## Step 1 — Add the VCS Repository Source

Because `mokoconsulting/mokostandards` is a private GitHub package, Composer must be told where to find it before it can resolve it. Add the `repositories` block to `composer.json`:

```json
{
	"name": "mokoconsulting/my-project",
	"description": "My project",
	"require": {
		"php": ">=8.1",
		"mokoconsulting/mokostandards": "^4.0"
	},
	"repositories": [
		{
			"type": "vcs",
			"url": "https://github.com/mokoconsulting-tech/MokoStandards"
		}
	],
	"autoload": {
		"psr-4": {
			"MyProject\\": "src/"
		}
	}
}
```

---

## Step 2 — Authenticate Composer

Composer must be able to read the private repository. Provide the `GH_TOKEN` environment variable before running any Composer command:

```bash
# Local development — set in your shell
export GH_TOKEN=ghp_...yourtoken...

# CI — the token is already in secrets.GH_TOKEN; wire it to the environment:
env:
  GH_TOKEN: ${{ secrets.GH_TOKEN }}
```

Alternatively, use `composer config github-oauth.github.com "$GH_TOKEN"` to write it to the local Composer auth store (do not commit the resulting `auth.json`).

---

## Step 3 — Install

```bash
composer install
```

For production deployments (no dev dependencies, optimised autoloader):

```bash
composer install --no-dev --optimize-autoloader
```

---

## Step 4 — Update

To pull the latest patch release:

```bash
composer update mokoconsulting/mokostandards
```

To update all dependencies:

```bash
composer update
```

---

## Using the Library

After installation, the MokoStandards autoloader is available via `vendor/autoload.php`.

### CliFramework (PHP scripts)

```php
<?php
require_once __DIR__ . '/vendor/autoload.php';

use MokoStandards\Enterprise\CliFramework;

class MyScript extends CliFramework
{
	protected function configure(): void
	{
		$this->setDescription('Does something useful');
		$this->addArgument('--path', 'Repository root', '.');
	}

	protected function run(): int
	{
		$path = $this->getArgument('--path');
		$this->log('INFO', "Processing: {$path}");
		return 0;
	}
}

$script = new MyScript('my_script', 'Does something useful');
exit($script->execute());
```

### ApiClient (GitHub API)

```php
<?php
require_once __DIR__ . '/vendor/autoload.php';

use MokoStandards\Enterprise\ApiClient;

$token = getenv('GH_TOKEN') ?: getenv('GITHUB_TOKEN');
$client = new ApiClient($token);

$repo = $client->getRepository('mokoconsulting-tech', 'MokoStandards');
```

---

## GitHub Actions Integration

Add this step before any PHP step that needs the library:

```yaml
- name: Install PHP dependencies
  run: composer install --no-dev --optimize-autoloader
  env:
    GH_TOKEN: ${{ secrets.GH_TOKEN }}
    COMPOSER_AUTH: '{"github-oauth":{"github.com":"${{ secrets.GH_TOKEN }}"}}'
```

The `COMPOSER_AUTH` env variable is the most reliable way to pass GitHub OAuth credentials to Composer in CI without touching auth.json.

---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `Could not find a version of package mokoconsulting/mokostandards` | VCS source not in `composer.json` | Add the `repositories` block (Step 1) |
| `Failed to authenticate` / `401 Unauthorized` | Missing or expired token | Export `GH_TOKEN` before running Composer |
| `The requested package mokoconsulting/mokostandards could not be found` | Token lacks read access to the repo | Ensure the PAT has `repo` (private repos) or `read:packages` scope |
| `Allowed memory size exhausted` | Composer running with low memory | Run `php -d memory_limit=-1 $(which composer) install` |

---

## Related Documentation

| Document | Purpose |
|----------|---------|
| [scripting-standards.md](../policy/scripting-standards.md) | How to write PHP scripts using CliFramework |
| [coding-style-guide.md](../policy/coding-style-guide.md) | Naming and formatting conventions |
| [branching-strategy.md](../policy/branching-strategy.md) | Branch and release workflow |
| [repo-sync.md](repo-sync.md) | How bulk sync distributes files to governed repos |

---

## Metadata

| Field         | Value |
|---------------|-------|
| Document Type | Guide |
| Domain        | Development |
| Applies To    | All PHP repositories |
| Owner         | Moko Consulting |
| Repo          | https://github.com/mokoconsulting-tech/MokoStandards |
| Path          | /docs/guide/package-installation.md |
| Version       | 04.00.05 |
| Status        | Active |
| Last Reviewed | 2026-03-09 |
