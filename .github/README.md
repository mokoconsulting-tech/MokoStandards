# GitHub Configuration

## Overview

This directory contains GitHub-specific configuration files for the MokoStandards repository.

## Private Repository Templates

**Note:** Private/internal GitHub templates (CODEOWNERS, issue templates, pull request templates) are maintained in a separate private repository: **mokoconsulting-tech/.github-private**

See [PRIVATE_TEMPLATES.md](PRIVATE_TEMPLATES.md) for complete details on:
- Location and access to private templates
- Why templates are kept private
- How to create templates for private repository
- Examples of CODEOWNERS, issue templates, and PR templates

This separation ensures:
- Sensitive organizational information is not publicly exposed
- Internal workflow templates remain confidential
- Public repository focuses on coding standards and public-facing policies

Public workflow templates for CI/CD are available in `templates/workflows/` in this repository.

## Files

### PRIVATE_TEMPLATES.md

Reference document explaining where private GitHub templates (CODEOWNERS, issue templates, pull request templates) are located and how to create them.

See [PRIVATE_TEMPLATES.md](PRIVATE_TEMPLATES.md) for:
- Private repository location (`mokoconsulting-tech/.github-private`)
- Access instructions for internal users
- Guidance for external users adopting MokoStandards
- Template creation examples

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

### org-settings.yml

**Organization-level** branch protection configuration that applies to **all repositories** in the mokoconsulting-tech organization.

* **Scope**: Organization-wide (all repositories)
* **Protection**: Main/master branch protection rules
* **Enforcement**: Active ruleset with optional bypass actors
* **Method**: GitHub Rulesets (organization settings)

#### Usage

Apply organization-level branch protection using GitHub Rulesets:

1. Go to GitHub Organization Settings → Repository → Rules → Rulesets
2. Create new ruleset: "Protect main branch across all repositories"
3. Configure target: All repositories
4. Add branch patterns: `main`, `master`
5. Enable rules as specified in org-settings.yml

Alternatively, use GitHub API, CLI, or Terraform for automation.

**Key Differences from settings.yml:**
* `settings.yml` - Applied per-repository (synced via bulk update)
* `org-settings.yml` - Applied once at organization level (affects all repos)
* Organization rulesets override repository-level settings

#### Key Settings

**Repository-level (settings.yml):**
* ✅ Squash merge enabled
* ❌ Merge commit disabled
* ❌ Rebase merge disabled
* Branch deletion after merge
* Stale review dismissal
* Conversation resolution required
* Pull request reviews required
* Linear history enforced
* Status checks required
* Up-to-date branches required

**Organization-level (org-settings.yml):**
* 🌐 Applied to ALL organization repositories
* 🔒 Protects main/master branches organization-wide
* ✅ Requires pull requests (no direct pushes)
* ✅ Requires 1 approval minimum
* ✅ Enforces linear history
* ✅ Prevents force pushes and deletions
* ✅ Can be bypassed by designated users/teams if needed

## Related Documentation

* [Merge Strategy Policy](../docs/policy/merge-strategy.md) - Complete policy documentation
* [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
* [Change Management Policy](../docs/policy/change-management.md) - Change management framework

## Metadata

* Directory: .github/
* Purpose: GitHub-specific configuration and documentation
* Maintained by: Repository administrators
