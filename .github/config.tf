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
# PATH: /.github/config.tf
# VERSION: 04.00.03
# BRIEF: Repository-specific override configuration for bulk synchronization

# Repository Override Configuration
# This file (located at .github/config.tf) prevents the bulk_update_repos.php script from recreating
# "live" workflow files in the MokoStandards repository itself.
#
# MokoStandards is a template/standards repository, so it should only
# contain workflow templates and MokoStandards-specific automation,
# not the "live" versions of workflows that get synced TO other repos.

locals {
  # Standard metadata for this terraform file
  file_metadata = {
    name              = "Repository Override Configuration"
    description       = "Override configuration for bulk repository synchronization - located in .github/config.tf"
    version           = "04.00.03"
    last_updated      = "2026-02-21T00:00:00Z"
    maintainer        = "MokoStandards Team"
    schema_version    = "2.0"
    repository_url    = "https://github.com/mokoconsulting-tech/MokoStandards"
    file_type         = "override"
    terraform_version = ">= 1.0"
    file_location     = ".github/config.tf"
  }
  
  # Metadata about this override configuration
  # Standard metadata fields for all terraform configurations
  override_metadata = {
    name           = "MokoStandards Repository Override"
    description    = "Override configuration preventing sync of template files in the standards repository"
    version        = "04.00.03"
    last_updated   = "2026-02-21T00:00:00Z"
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
      reason = "Generic workflow - template exists at templates/workflows/code-quality.yml.template"
    },
    {
      path   = ".github/workflows/auto-update-changelog.yml"
      reason = "Generic workflow - template exists at templates/workflows/auto-update-changelog.yml.template"
    },
    {
      path   = ".github/workflows/enterprise-issue-manager.yml"
      reason = "Generic workflow - template exists at templates/workflows/enterprise-issue-manager.yml.template"
    },
    {
      path   = ".github/workflows/repo-health.yml"
      reason = "Generic reusable workflow - should be template for other repos"
    },
    {
      path   = ".github/workflows/auto-create-org-projects.yml"
      reason = "Generic org automation - not standards-specific"
    },
    {
      path   = ".github/workflows/bulk-label-deployment.yml"
      reason = "Generic label deployment - not standards-specific"
    },
    {
      path   = ".github/workflows/enterprise-firewall-setup.yml"
      reason = "Generic firewall config generator - not standards-specific"
    },
    {
      path   = ".github/workflows/codeql-analysis.yml"
      reason = "Generic security scanning - redundant with GitHub default CodeQL setup"
    },
    {
      path   = ".github/workflows/dependency-review.yml"
      reason = "Generic workflow - template exists at templates/workflows/generic/dependency-review.yml.template"
    },
    {
      path   = ".github/workflows/deploy-to-dev.yml"
      reason = "Generic deployment - not needed in MokoStandards (template only)"
    },
    {
      path   = ".github/workflows/release-cycle.yml"
      reason = "Not needed in template repo - actual file is release-cycle.yml.disabled"
    },
    {
      path   = ".github/workflows/unified-release.yml"
      reason = "Not needed in template repo - actual file is unified-release.yml.disabled"
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
      path   = "override.config.tf"
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
    # Keep new Week 1 enterprise workflows (MokoStandards-specific)
    {
      path   = ".github/workflows/audit-log-archival.yml"
      reason = "MokoStandards-specific enterprise audit workflow"
    },
    {
      path   = ".github/workflows/metrics-collection.yml"
      reason = "MokoStandards-specific enterprise metrics workflow"
    },
    {
      path   = ".github/workflows/health-check.yml"
      reason = "MokoStandards-specific enterprise health monitoring workflow"
    },
    {
      path   = ".github/workflows/security-scan.yml"
      reason = "MokoStandards-specific enhanced security workflow"
    },
    {
      path   = ".github/workflows/integration-tests.yml"
      reason = "MokoStandards-specific enterprise library integration tests"
    },
    {
      path   = ".github/workflows/auto-update-sha.yml"
      reason = "MokoStandards-specific workflow for updating script registry SHA hashes"
    },
    {
      path   = ".github/workflows/validate-script-integrity.yml"
      reason = "MokoStandards-specific workflow for validating script integrity"
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
