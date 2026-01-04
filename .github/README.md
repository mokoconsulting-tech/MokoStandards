# GitHub Configuration

## Overview

This directory contains GitHub-specific configuration files for the MokoStandards repository.

## Private Repository Templates

**Note:** Private/internal GitHub templates (CODEOWNERS, issue templates, pull request templates) are maintained in a separate private repository: **mokoconsulting-tech/MokoStandards-github-private**

This separation ensures:
- Sensitive organizational information is not publicly exposed
- Internal workflow templates remain confidential
- Public repository focuses on coding standards and public-facing policies

Public workflow templates for CI/CD are available in `.github/workflows/templates/` in this repository.

## Files

### settings.yml

Configuration file for GitHub repository settings. This file defines:

* **Merge Strategy**: Squash merge only (merge commits and rebase merge are disabled)
* **Branch Protection**: Rules for the main branch
* **Automatic Cleanup**: Branches are automatically deleted after merge
* **Pull Request Settings**: Auto-merge, update branch, and review requirements

#### Usage

This file can be used with:

* [Probot Settings](https://probot.github.io/apps/settings/) app
* [GitHub Settings Sync](https://github.com/apps/settings) app
* Manual configuration reference for repository administrators

To apply these settings manually:

1. Go to repository Settings → General
2. Under "Pull Requests", configure:
   - Enable: Allow squash merging
   - Disable: Allow merge commits
   - Disable: Allow rebase merging
   - Enable: Automatically delete head branches
3. Go to Settings → Branches → Add rule for `main`
4. Configure branch protection as specified in settings.yml

#### Key Settings

**Merge Methods:**
* ✅ Squash merge enabled
* ❌ Merge commit disabled
* ❌ Rebase merge disabled

**Automatic Actions:**
* Branch deletion after merge
* Stale review dismissal
* Conversation resolution required

**Branch Protection (main):**
* Pull request reviews required
* Linear history enforced
* Status checks required
* Up-to-date branches required

## Related Documentation

* [Merge Strategy Policy](../docs/policy/merge-strategy.md) - Complete policy documentation
* [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
* [Change Management Policy](../docs/policy/change-management.md) - Change management framework

## Metadata

* Directory: .github/
* Purpose: GitHub-specific configuration and documentation
* Maintained by: Repository administrators
