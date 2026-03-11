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
DEFGROUP: MokoStandards.Policy
INGROUP: MokoStandards.Development
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/policy/scripting-standards.md
VERSION: 04.00.12
BRIEF: Standards and requirements for automation scripts and tooling
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.12-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Scripting Standards Policy

## Purpose

This policy establishes mandatory standards for all automation scripts, build tools, validation utilities, and development tooling across MokoStandards-governed repositories. It defines language requirements, coding standards, documentation expectations, and maintenance obligations to ensure consistent, maintainable, and secure automation.

## Scope

This policy applies to:

- All automation scripts in `scripts/` directory
- CI/CD pipeline scripts
- Build and deployment automation
- Validation and testing utilities
- Development tooling and helpers
- Code generation scripts
- Migration and setup scripts

This policy does not apply to:

- Application source code (governed by language-specific standards)
- Configuration files (YAML, JSON, etc.)
- Documentation markdown files
- Data files or static assets

## Responsibilities

### Script Authors

Responsible for:

- Writing scripts in approved languages
- Following coding standards and conventions
- Documenting script purpose and usage
- Testing scripts before committing
- Maintaining scripts they create

### Repository Maintainers

Responsible for:

- Reviewing script pull requests
- Enforcing scripting standards
- Testing scripts in CI/CD
- Approving exceptions to standards
- Archiving deprecated scripts

### Security Owner

Accountable for:

- Reviewing security implications of scripts
- Approving scripts with elevated privileges
- Ensuring secure coding practices
- Validating input sanitization

## Language Requirements

### Primary Language: PHP

**All new automation scripts MUST be written in PHP.**

PHP is the standard language across the entire Moko Consulting ecosystem. Using it for
automation scripts keeps the toolchain uniform, reduces the number of runtimes required
in CI/CD, and allows every developer to read and maintain every script without switching
mental context.

**Rationale**:
- **Single runtime**: PHP 8.1+ is already required by all governed repositories; no
  additional interpreter installation is needed
- **Consistency**: Application code, validation scripts, and automation all share one
  language and one set of coding standards
- **Existing libraries**: The MokoStandards Enterprise library (`api/lib/Enterprise/`) and
  all shared helpers are PHP — scripts can reuse them directly
- **Composer ecosystem**: Packages for HTTP, YAML, hashing, and other common needs are
  available via Composer
- **Type safety**: PHP 8.1 supports union types, enums, named arguments, and fibers;
  `declare(strict_types=1)` enforces strict type checking at runtime

**Version Requirements**:
- Minimum: PHP 8.1
- Recommended: PHP 8.2 or later
- All scripts must include `declare(strict_types=1)`
- Document minimum version in script header

**Example Header**:
```php
<?php
/**
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Scripts
 * INGROUP:  MokoStandards.Automation
 * REPO:     https://github.com/mokoconsulting-tech/MokoStandards
 * PATH:     /scripts/maintenance/my_script.php
 * VERSION:  04.00.12
 * BRIEF:    Brief description of what this script does
 */

declare(strict_types=1);
```

### Secondary Language: Python (Exception Only)

Python may only be used when **all** of the following conditions are met:

1. No PHP equivalent exists in the standard library or Composer ecosystem
2. The task is intrinsically tied to a Python-only tool (e.g., ML inference, specific
   data-science pipeline)
3. The exception is documented in the script header
4. Maintainer approval has been granted and recorded

> **Guideline**: If you are uncertain whether a PHP equivalent exists, ask before writing
> Python. In almost all cases a PHP solution is available.

**Migration obligation**: Existing Python scripts (`scripts/maintenance/*.py`) are
classified as legacy. They must be migrated to PHP when they are next modified for a
functional reason. Do not write new functionality in these files; open a migration ticket
instead.

### Prohibited Languages for New Scripts

The following languages are prohibited for new automation scripts without explicit
maintainer approval:

- **Python** (without approved exception — see above)
- **Shell scripts** (bash, sh, zsh): Platform-specific, poor error handling
- **Batch files** (.bat, .cmd): Windows-only, limited functionality
- **PowerShell** (.ps1): Windows-focused, inconsistent cross-platform
- **Perl**: Declining ecosystem, poor readability
- **Ruby**: Not part of the Moko Consulting tech stack

### Exceptions for Existing Scripts

**Legacy Python Scripts** in `scripts/maintenance/`:
- Existing Python scripts (`.py`) are **grandfathered**
- May remain as Python until their next functional modification
- When a functional change is required, migrate the entire script to PHP
- Do not add new functionality to existing Python scripts; migrate first

**Legacy Bash Validation Scripts** in `scripts/lib/validate/`:
- Existing bash scripts (`.sh`) are **grandfathered**
- May remain as bash for backward compatibility
- Should not be rewritten unless functional changes are needed
- New validation scripts must use PHP

**Minimal Wrapper Scripts**:
- Simple CI/CD entry points (< 10 lines) may use bash
- Must only call PHP scripts (`php script.php`) or system commands
- Require maintainer approval

**Exception Process**:
1. Document technical justification
2. Confirm no PHP equivalent exists
3. Get Security Owner approval for privileged operations
4. Get maintainer approval
5. Document exception and approval in script header
6. Set a migration target date

## PHP Coding Standards

### File Structure

```php
<?php
/**
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Scripts
 * INGROUP:  MokoStandards.Automation
 * REPO:     https://github.com/mokoconsulting-tech/MokoStandards
 * PATH:     /scripts/maintenance/my_script.php
 * VERSION:  04.00.12
 * BRIEF:    Script that does XYZ for ABC
 *
 * Usage:
 *   php scripts/maintenance/my_script.php [arguments]
 *
 * Examples:
 *   php scripts/maintenance/my_script.php --input file.txt
 *   php scripts/maintenance/my_script.php --verbose --output result.json
 *
 * Requirements:
 *   PHP 8.1+
 *   No external dependencies (or list them)
 */

declare(strict_types=1);

require_once __DIR__ . '/../../vendor/autoload.php';

// Constants
const DEFAULT_VALUE = 'value';
const MAX_RETRIES = 3;

function main(): void
{
	// main entry point
}

main();
```

### Naming Conventions

**Files**:
- Use `snake_case` for filenames: `sync_file_to_project.php`
- Use descriptive, action-oriented names: `validate_manifest.php`
- Avoid abbreviations unless widely understood

**Functions**:
- Use `camelCase`: `function processFile(string $path): void`
- Use verb-noun pattern: `createIssue()`, `updateProject()`
- Private methods prefix with underscore or use `private` visibility: `private function _internalHelper()`

**Classes**:
- Use `PascalCase`: `class ProjectManager`
- Use noun phrases: `GitHubClient`, `DocumentParser`

**Constants**:
- Use `UPPER_SNAKE_CASE`: `const DEFAULT_PROJECT_NUMBER = 7;`
- Define at class level or as top-level constants after the header block

**Variables**:
- Use `camelCase`: `$filePath`, `$issueCount`
- Use descriptive names; avoid single letters except loop counters
- Boolean variables use `is`, `has`, `should` prefix: `$isVerbose`, `$hasErrors`

### Type Declarations

**Type declarations are REQUIRED for all function signatures (`declare(strict_types=1)` is mandatory):**

```php
<?php
declare(strict_types=1);

/**
 * Process multiple files and return a count with any errors.
 *
 * @param  string[] $paths
 * @param  string   $outputDir
 * @param  bool     $verbose
 * @return array{count: int, errors: string[]}
 */
function processFiles(array $paths, string $outputDir, bool $verbose = false): array
{
	// implementation
	return ['count' => 0, 'errors' => []];
}

/**
 * Get configuration by name.
 *
 * @param  string $name
 * @return array<string,string>|null  Returns null if not found.
 */
function getConfig(string $name): ?array
{
	return null;
}
```

**Benefits**:
- Runtime type enforcement via `strict_types=1`
- Enables static analysis with PHPStan and Psalm
- Improves IDE autocomplete
- Self-documenting code
- Catches type bugs before production

### Documentation

**PHPDoc blocks are REQUIRED for all public functions:**

```php
/**
 * Sync a file or folder to GitHub Project.
 *
 * @param  string $filePath      Path to file or folder to sync.
 * @param  int    $projectNumber GitHub Project number (default: 7).
 * @param  bool   $isFolder      Whether path is a folder (default: false).
 * @return bool   True if sync successful, false otherwise.
 *
 * @throws \InvalidArgumentException If $filePath is invalid.
 * @throws \RuntimeException         If GitHub API fails.
 *
 * @example
 *   syncFileToProject('docs/policy/new.md');  // returns true
 */
function syncFileToProject(string $filePath, int $projectNumber = 7, bool $isFolder = false): bool
{
	// implementation
	return true;
}
```

**PHPDoc Format**: Follow PSR-5 / phpDocumentor conventions.

### Code Formatting

**Indentation**: Use tabs, not spaces (MokoStandards standard).

- Configure editor to use tabs with 2-space visual width
- Follow `.editorconfig` settings in repository root
- Be consistent throughout the script
- **Exception**: YAML configuration files must use spaces (YAML specification requirement)

**Line length**:
- Maximum 120 characters per line
- Break long lines at logical points

**Formatting tools**:
- Use `phpcs` (PHP_CodeSniffer) for style checking — ruleset `phpcs.xml` at repo root
- Use `phpstan` for static analysis — config `phpstan.neon` at repo root
- Use `psalm` for type checking — config `psalm.xml` at repo root

### Error Handling

**Proper error handling is REQUIRED:**

```php
<?php
declare(strict_types=1);

function loadFile(string $path): string
{
	if (!file_exists($path)) {
		fwrite(STDERR, "Error: File not found: {$path}" . PHP_EOL);
		exit(1);
	}

	if (!is_readable($path)) {
		fwrite(STDERR, "Error: Permission denied: {$path}" . PHP_EOL);
		exit(1);
	}

	$content = file_get_contents($path);
	if ($content === false) {
		fwrite(STDERR, "Error: Could not read file: {$path}" . PHP_EOL);
		exit(1);
	}

	return $content;
}
```

**Best Practices**:
- Throw typed exceptions (`\InvalidArgumentException`, `\RuntimeException`)
- Print errors to `STDERR` using `fwrite(STDERR, ...)`
- Exit with non-zero code on failure: `exit(1)`
- Exit with zero on success: `exit(0)`
- Provide helpful error messages with context

### Command-Line Arguments

**Use `getopt()` or a lightweight CLI helper for all command-line scripts:**

```php
<?php
declare(strict_types=1);

$shortopts = '';
$longopts = [
	'path:',     // required value
	'project::',  // optional value
	'folder',    // flag
	'verbose',   // flag
	'dry-run',   // flag
];
$opts = getopt($shortopts, $longopts, $restIndex);

$path      = $opts['path'] ?? null;
$project   = (int) ($opts['project'] ?? 7);
$isFolder  = isset($opts['folder']);
$verbose   = isset($opts['verbose']);
$dryRun    = isset($opts['dry-run']);

if ($path === null) {
	fwrite(STDERR, "Usage: php script.php --path <path> [--project N] [--folder] [--verbose] [--dry-run]" . PHP_EOL);
	exit(1);
}
```

**Benefits**:
- No extra dependency
- Standard PHP built-in
- Type-safe when combined with `strict_types=1`

### Dry-Run Support

**All scripts that modify files or system state MUST support `--dry-run` mode.**

**Requirements:**

```php
$dryRun = isset($opts['dry-run']);
```

**Implementation:**

```php
function processFiles(array $files, bool $dryRun = false): void
{
	foreach ($files as $file) {
		if ($dryRun) {
			echo "[DRY-RUN] Would process: {$file}" . PHP_EOL;
		} else {
			echo "Processing: {$file}" . PHP_EOL;
			// actual processing
		}
	}
}
```

**Dry-run best practices:**
- Use `[DRY-RUN]` prefix in all log messages during dry-run
- Validate all inputs and logic in dry-run mode
- Exit with same status codes as actual execution would
- Show what would be done, not just what would be checked
- Skip any operations that modify state (file writes, API calls, etc.)

**Scripts requiring dry-run:**
- ✅ File modification scripts
- ✅ Validation scripts that could fail builds
- ✅ Deployment or release scripts
- ✅ Scripts that interact with external systems

**Scripts exempt from dry-run:**
- ❌ Read-only analysis scripts
- ❌ Simple query scripts with no side effects
- ❌ Scripts that only display information

### Dependencies

**Minimize external dependencies:**

**Prefer built-in PHP functions and the existing Enterprise library**:
- ✅ Use `SplFileInfo`/`DirectoryIterator` for filesystem operations
- ✅ Use `exec()`/`proc_open()` for external commands (safely)
- ✅ Use `json_decode()`/`json_encode()` for JSON
- ✅ Use `getopt()` for CLI arguments
- ✅ Use `api/lib/Enterprise/` classes for MokoStandards operations

**Avoid unnecessary packages**:
- ❌ Don't add a Composer package if a PHP built-in works
- ❌ Don't use a full framework for a simple CLI script

**If external dependencies are required**:
1. Document in script PHPDoc header
2. Add to `composer.json` and run `composer require`
3. Pin versions for reproducibility
4. Get maintainer approval

## Security Requirements

### Input Validation

**All user input MUST be validated:**

```php
<?php
declare(strict_types=1);

function validateFilePath(string $path): string
{
	$realPath = realpath($path);

	// Check for path traversal
	if ($realPath === false || str_contains($path, '..')) {
		throw new \InvalidArgumentException("Path traversal not allowed: {$path}");
	}

	// Check file exists
	if (!file_exists($realPath)) {
		throw new \InvalidArgumentException("File not found: {$path}");
	}

	// Check file is within allowed directory
	$allowedDir = realpath(getcwd());
	if (!str_starts_with($realPath, $allowedDir)) {
		throw new \InvalidArgumentException("Access outside repository not allowed");
	}

	return $realPath;
}
```

**Requirements**:
- Validate all command-line arguments
- Sanitize file paths (prevent path traversal)
- Validate file types and extensions
- Check file sizes before processing
- Escape shell commands properly (use `escapeshellarg()`)

### Credentials and Secrets

**Credentials MUST NEVER be hardcoded:**

```php
<?php
declare(strict_types=1);

// ✅ Correct: Use environment variables — prefer GH_TOKEN (org secret), fall back to GITHUB_TOKEN
$githubToken = getenv('GH_TOKEN') ?: getenv('GITHUB_TOKEN') ?: null;
if ($githubToken === null) {
	fwrite(STDERR, "Error: GH_TOKEN environment variable not set" . PHP_EOL);
	exit(1);
}

// ❌ Incorrect: Hardcoded credentials
$githubToken = 'ghp_xxxxxxxxxxxx'; // NEVER DO THIS
```

**Best Practices**:
- Use environment variables for credentials
- Use GitHub Secrets in CI/CD
- Never log credentials
- Never commit credentials
- Document required environment variables

### Shell Command Execution

**Use `proc_open()` or `escapeshellarg()` safely:**

```php
<?php
declare(strict_types=1);

// ✅ Correct: Arguments escaped before shell execution
function runCommand(array $args): string
{
	$escapedArgs = array_map('escapeshellarg', $args);
	$cmd = implode(' ', $escapedArgs);
	$output = shell_exec($cmd);
	if ($output === null) {
		throw new \RuntimeException("Command failed: {$cmd}");
	}
	return $output;
}

// ❌ Incorrect: User input concatenated directly into command
function runCommandUnsafe(string $userInput): void
{
	shell_exec("echo {$userInput}"); // VULNERABLE
}
```

**Requirements**:
- Always use `escapeshellarg()` on user-supplied values
- Prefer an array of arguments via `proc_open()` for complex cases
- Validate all command arguments
- Check exit codes

### Privilege Management

**Scripts requiring elevated privileges need approval:**

**Requirements**:
- Document why elevated privileges needed
- Minimize scope of privileged operations
- Use principle of least privilege
- Get Security Owner approval
- Add security warning in documentation

## Testing Requirements

### Unit Tests

**Scripts with complex logic MUST have unit tests:**

```php
<?php
// In script: scripts/maintenance/my_script.php
declare(strict_types=1);

function calculatePriority(string $docType): string
{
	return $docType === 'policy' ? 'High' : 'Medium';
}

// In test: api/tests/ScriptTest.php
declare(strict_types=1);

use PHPUnit\Framework\TestCase;

class MyScriptTest extends TestCase
{
	public function testPolicyPriority(): void
	{
		$this->assertSame('High', calculatePriority('policy'));
	}

	public function testDefaultPriority(): void
	{
		$this->assertSame('Medium', calculatePriority('guide'));
	}
}
```

**Test Requirements**:
- Test all public functions
- Test error cases and edge cases
- Use PHPUnit (already a dev dependency via `composer.json`)
- Place tests in `api/tests/` directory
- Run tests in CI/CD with `composer run test`

### Manual Testing

**All scripts MUST be manually tested before commit:**

**Testing Checklist**:
- [ ] Test with valid inputs
- [ ] Test with invalid inputs
- [ ] Test with missing arguments
- [ ] Test `--help` output (if implemented)
- [ ] Test error messages
- [ ] Test in clean environment
- [ ] Test cross-platform (if applicable)

### CI/CD Validation

**Scripts MUST pass CI/CD checks:**

- Syntax validation: `php -l scripts/my_script.php`
- Static analysis: `phpstan analyse scripts/`
- Code style: `phpcs scripts/`
- Unit tests: `composer run test`
- Integration tests in workflow

## Documentation Requirements

### README Files

**Script directories MUST have an `index.md` in `docs/scripts/`:**

```markdown
## Available Scripts

### sync_file_to_project.php

Syncs documentation files and folders to GitHub Project.

**Usage**:
\`\`\`bash
php scripts/sync_file_to_project.php --path <path> [--project N] [--folder]
\`\`\`

**Examples**:
\`\`\`bash
php scripts/sync_file_to_project.php --path docs/policy/new.md
php scripts/sync_file_to_project.php --path docs/guide/ --folder
\`\`\`

**Requirements**:
- PHP 8.1+
- GitHub CLI (`gh`) installed and authenticated
```

### Inline Comments

**Use comments for complex logic only:**

```php
// ✅ Good: Explains non-obvious logic
// Priority is High for policy docs because governance requirements mandate
// immediate review by maintainers before other document types.
$priority = $docType === 'policy' ? 'High' : 'Medium';

// ❌ Bad: States the obvious
// Set priority to High
$priority = 'High';
```

**When to comment**:
- Explain "why", not "what"
- Document workarounds
- Explain complex algorithms
- Reference external documentation
- Note TODOs with issue numbers

### File Headers

**All scripts MUST have standard headers:**

```php
<?php
/**
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * This file is part of a Moko Consulting project.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * [Full license header...]
 *
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Scripts
 * INGROUP:  MokoStandards.Automation
 * REPO:     https://github.com/mokoconsulting-tech/MokoStandards
 * PATH:     /scripts/maintenance/my_script.php
 * VERSION:  04.00.12
 * BRIEF:    Brief description of script purpose
 */

declare(strict_types=1);
```

## Maintenance Requirements

### Version Control

**Scripts MUST follow version control best practices:**

- Commit scripts with descriptive messages
- Reference issue numbers in commits
- Use feature branches for changes
- Submit pull requests for review
- Tag releases when appropriate

### Deprecation Process

**Deprecated scripts MUST follow proper sunset process:**

1. **Mark as deprecated**:
   - Add deprecation warning to script
   - Update documentation
   - Announce in CHANGELOG

2. **Provide migration path**:
   - Document replacement script
   - Provide migration guide
   - Offer transition period

3. **Archive**:
   - Move to `scripts/deprecated/`
   - Keep for historical reference
   - Remove after 6 months

### Update Requirements

**Scripts MUST be kept up to date:**

- Update for PHP version changes
- Update for dependency changes
- Update for API changes
- Fix bugs promptly
- Improve based on feedback

## Compliance and Enforcement

### Code Review

**All scripts require code review:**

**Review Checklist**:
- [ ] Written in PHP (Python only with approved exception)
- [ ] `declare(strict_types=1)` present
- [ ] Follows naming conventions
- [ ] Has PHP type declarations
- [ ] Has PHPDoc blocks
- [ ] Has error handling
- [ ] Has unit tests (if complex)
- [ ] Validates inputs
- [ ] No hardcoded credentials
- [ ] Documentation complete
- [ ] Tested manually

### Automated Checks

**CI/CD MUST validate scripts:**

```yaml
# In .github/workflows/ci.yml
- name: Validate PHP scripts
  run: |
    find scripts -name "*.php" -type f -exec php -l {} \;

- name: Static analysis (phpstan)
  run: |
    ./vendor/bin/phpstan analyse scripts/

- name: Code style (phpcs)
  run: |
    ./vendor/bin/phpcs scripts/
```

### Exceptions and Waivers

**Exception requests require**:

1. Written justification
2. Technical rationale
3. Maintainer approval
4. Security Owner approval (if security relevant)
5. Documentation in script header
6. Expiration date for review

## Metrics and Reporting

### Quality Metrics

**Track script quality:**

- Number of scripts with tests
- Test coverage percentage
- Number of scripts with type hints
- Number of scripts with proper documentation
- Number of security findings

### Usage Metrics

**Track script usage:**

- Execution frequency in CI/CD
- Manual execution patterns
- Error rates
- Performance metrics

## Dependencies

This policy depends on:

- [Document Formatting Policy](document-formatting.md) - For file headers
- [Security Scanning Policy](security-scanning.md) - For security requirements
- [Dependency Management Policy](dependency-management.md) - For external dependencies
- PHP 8.1+ installed in development and CI/CD environments

## Acceptance Criteria

- [ ] All new scripts written in PHP
- [ ] All scripts have `declare(strict_types=1)`
- [ ] All scripts have proper headers
- [ ] All scripts have PHPDoc blocks
- [ ] All scripts use PHP type declarations
- [ ] All scripts handle errors properly
- [ ] All scripts validate inputs
- [ ] No hardcoded credentials
- [ ] Documentation complete
- [ ] CI/CD validation passes

## Metadata

| Field | Value |
| ----- | ----- |
| Document Type | Policy |
| Domain | Governance |
| Applies To | All Repositories |
| Jurisdiction | Tennessee, USA |
| Owner | Moko Consulting |
| Repo | https://github.com/mokoconsulting-tech/ |
| Path | /docs/policy/scripting-standards.md |
| Version | 04.00.12 |
| Status | Active |
| Last Reviewed | 2026-03-11 |
| Reviewed By | Moko Consulting |

## Revision History

| Date | Author | Change | Notes |
| ---- | ------ | ------ | ----- |
| 2026-03-11 | Moko Consulting | Established PHP as the primary scripting language; Python permitted only with approved exception; existing `.py` scripts classified as legacy pending migration | Supersedes Python-primary policy |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history | Updated to version 03.00.00 with all required fields |
