# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# This file is part of a Moko Consulting project.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# FILE INFORMATION
# DEFGROUP: MokoStandards.Override
# INGROUP: MokoStandards.Configuration
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: /MokoStandards.override.tf
# VERSION: 02.02.00
# BRIEF: MokoStandards Sync Override Configuration for the Standards Repository

# MokoStandards Repository Override Configuration
# This file prevents the bulk_update_repos.py script from recreating
# "live" workflow files in the MokoStandards repository itself.
#
# MokoStandards is a template/standards repository, so it should only
# contain workflow templates and MokoStandards-specific automation,
# not the "live" versions of workflows that get synced TO other repos.

locals {
  # Metadata about this override configuration
  # Standard metadata fields for all terraform configurations
  override_metadata = {
    name           = "MokoStandards Repository Override"
    description    = "Override configuration preventing sync of template files in the standards repository"
    version        = "2.2.0"
    last_updated   = "2026-02-08T07:45:00Z"
    maintainer     = "MokoStandards Team"
    schema_version = "2.0"
    repository_url = "https://github.com/mokoconsulting-tech/MokoStandards"
    
    # Context-specific fields
    repository_type  = "standards"
    compliance_level = "strict"
    format           = "terraform"
  }

  # Sync configuration
  sync_config = {
    enabled = true
    
    # Cleanup configuration for obsolete files
    # cleanup_mode options:
    #   - "none": No cleanup, only copy/update files
    #   - "conservative": Remove only obsolete .yml/.py files from managed directories
    #   - "aggressive": Remove all files in managed directories not in sync list
    cleanup_mode = "conservative"
  }

  # Files to exclude from sync
  # These are "live" workflows that should NOT exist in MokoStandards
  # because they are templates that get synced TO other repos
  # Note: MokoStandards is a template/standards repository and does not
  # require build or release workflows for itself
  exclude_files = [
    {
      path   = ".github/workflows/build.yml"
      reason = "MokoStandards does not require build workflow - disabled as build.yml.disabled"
    },
    {
      path   = ".github/workflows/reusable-build.yml"
      reason = "Reusable workflow not needed in template repo - disabled as reusable-build.yml.disabled"
    },
    {
      path   = ".github/workflows/reusable-project-detector.yml"
      reason = "Reusable workflow not needed in template repo - disabled as reusable-project-detector.yml.disabled"
    },
    {
      path   = ".github/workflows/reusable-release.yml"
      reason = "Reusable workflow not needed in template repo - disabled as reusable-release.yml.disabled"
    },
    {
      path   = ".github/workflows/reusable-php-quality.yml"
      reason = "Reusable workflow not needed in template repo - disabled as reusable-php-quality.yml.disabled"
    },
    {
      path   = ".github/workflows/reusable-platform-testing.yml"
      reason = "Reusable workflow not needed in template repo - disabled as reusable-platform-testing.yml.disabled"
    },
    {
      path   = ".github/workflows/code-quality.yml"
      reason = "corresponds to templates/workflows/code-quality.yml.template"
    },
    {
      path   = ".github/workflows/dependency-review.yml"
      reason = "corresponds to templates/workflows/generic/dependency-review.yml.template"
    },
    {
      path   = ".github/workflows/deploy-to-dev.yml"
      reason = "template only, not active in MokoStandards"
    },
    {
      path   = ".github/workflows/release-cycle.yml"
      reason = "MokoStandards does not require release workflow - disabled as release-cycle.yml.disabled"
    },
    {
      path   = ".github/workflows/unified-release.yml"
      reason = "MokoStandards does not require unified release workflow - disabled as unified-release.yml.disabled"
    },
    {
      path   = ".github/workflows/codeql-analysis.yml"
      reason = "corresponds to templates/workflows/generic/codeql-analysis.yml"
    },
  ]

  # Explicitly mark files as obsolete for removal during sync
  # These files will be deleted from target repos during sync
  # Use this to remove deprecated workflows or scripts
  obsolete_files = [
    {
      path   = "templates/workflows/build-universal.yml.template"
      reason = "Duplicate of build.yml.template - consolidated"
    },
    {
      path   = "templates/workflows/release-cycle-simple.yml.template"
      reason = "Superseded by release-cycle.yml.template v2.0 - consolidated"
    },
  ]

  # Files that should never be overwritten (always preserved)
  protected_files = [
    {
      path   = ".gitignore"
      reason = "Repository-specific ignore patterns"
    },
    {
      path   = ".editorconfig"
      reason = "Repository-specific editor config"
    },
    {
      path   = "MokoStandards.override.tf"
      reason = "This override file itself"
    },
    # Keep MokoStandards-specific workflows
    {
      path   = ".github/workflows/standards-compliance.yml"
      reason = "MokoStandards-specific workflow"
    },
    {
      path   = ".github/workflows/changelog_update.yml"
      reason = "MokoStandards-specific workflow"
    },
    {
      path   = ".github/workflows/bulk-repo-sync.yml"
      reason = "MokoStandards-specific workflow"
    },
    {
      path   = ".github/workflows/confidentiality-scan.yml"
      reason = "MokoStandards-specific workflow"
    },
    {
      path   = ".github/workflows/repo-health.yml"
      reason = "MokoStandards-specific workflow"
    },
    {
      path   = ".github/workflows/auto-create-org-projects.yml"
      reason = "MokoStandards-specific workflow"
    },
    {
      path   = ".github/workflows/sync-changelogs.yml"
      reason = "MokoStandards-specific workflow"
    },
    # Keep reusable workflows (these are meant to be called, not synced)
    {
      path   = ".github/workflows/reusable-build.yml"
      reason = "Reusable workflow template"
    },
    {
      path   = ".github/workflows/reusable-ci-validation.yml"
      reason = "Reusable workflow template"
    },
    {
      path   = ".github/workflows/reusable-release.yml"
      reason = "Reusable workflow template"
    },
    {
      path   = ".github/workflows/reusable-php-quality.yml"
      reason = "Reusable workflow template"
    },
    {
      path   = ".github/workflows/reusable-platform-testing.yml"
      reason = "Reusable workflow template"
    },
    {
      path   = ".github/workflows/reusable-project-detector.yml"
      reason = "Reusable workflow template"
    },
    # Keep enterprise firewall setup workflow
    {
      path   = ".github/workflows/enterprise-firewall-setup.yml"
      reason = "MokoStandards-specific workflow"
    },
  ]

  # Files available for sync from templates/
  # Issue templates are available at templates/github/ISSUE_TEMPLATE/
  # Target repos should copy these to .github/ISSUE_TEMPLATE/
  sync_templates = {
    issue_templates = {
      source_dir = "templates/github/ISSUE_TEMPLATE"
      target_dir = ".github/ISSUE_TEMPLATE"
      files = [
        "bug_report.md",
        "feature_request.md",
        "documentation.md",
        "question.md",
        "config.yml"
      ]
      description = "Standard issue templates for consistent issue reporting across repositories"
    }
    
    github_templates = {
      source_dir = "templates/github"
      target_dir = ".github"
      files = [
        "CODEOWNERS.template",
        "PULL_REQUEST_TEMPLATE.md",
        "README.md"
      ]
      description = "GitHub configuration templates for repository setup"
    }
  }
}
