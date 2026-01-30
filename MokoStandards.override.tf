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
# VERSION: 02.01.00
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
    version        = "2.1.0"
    last_updated   = "2026-01-30T04:38:00Z"
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
  }

  # Files to exclude from sync
  # These are "live" workflows that should NOT exist in MokoStandards
  # because they are templates that get synced TO other repos
  exclude_files = [
    {
      path   = ".github/workflows/build.yml"
      reason = "corresponds to templates/workflows/build-universal.yml.template"
    },
    {
      path   = ".github/workflows/ci.yml"
      reason = "corresponds to templates/workflows/unified-ci.yml.template"
    },
    {
      path   = ".github/workflows/code-quality.yml"
      reason = "corresponds to templates/workflows/code-quality.yml.template"
    },
    {
      path   = ".github/workflows/codeql-analysis.yml"
      reason = "corresponds to templates/workflows/generic/codeql-analysis.yml"
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
      reason = "corresponds to templates/workflows/release-cycle.yml.template"
    },
    {
      path   = ".github/workflows/terraform-ci.yml"
      reason = "corresponds to templates/workflows/terraform/ci.yml"
    },
    {
      path   = ".github/workflows/terraform-deploy.yml"
      reason = "corresponds to templates/workflows/terraform/deploy.yml.template"
    },
    {
      path   = ".github/workflows/terraform-drift.yml"
      reason = "corresponds to templates/workflows/terraform/drift-detection.yml.template"
    },
  ]

  # Files that should never be overwritten (always preserved)
  protected_files = [
    # Repository configuration files
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
    {
      path   = "README.md"
      reason = "MokoStandards-specific documentation"
    },
    {
      path   = "CONTRIBUTING.md"
      reason = "MokoStandards-specific contribution guidelines"
    },
    
    # GitHub configuration files
    {
      path   = ".github/copilot.yml"
      reason = "MokoStandards-specific Copilot configuration"
    },
    {
      path   = ".github/org-settings.yml"
      reason = "MokoStandards organization settings"
    },
    {
      path   = ".github/issue-management-config.yml"
      reason = "MokoStandards issue management configuration"
    },
    
    # MokoStandards-specific workflows (repository maintenance)
    {
      path   = ".github/workflows/auto-create-dev-branch.yml"
      reason = "MokoStandards branch management workflow"
    },
    {
      path   = ".github/workflows/auto-create-org-projects.yml"
      reason = "MokoStandards project automation workflow"
    },
    {
      path   = ".github/workflows/auto-release-on-version-bump.yml"
      reason = "MokoStandards release automation workflow"
    },
    {
      path   = ".github/workflows/auto-release.yml"
      reason = "MokoStandards release workflow"
    },
    {
      path   = ".github/workflows/auto-update-changelog.yml"
      reason = "MokoStandards changelog automation workflow"
    },
    {
      path   = ".github/workflows/bulk-label-deployment.yml"
      reason = "MokoStandards label management workflow"
    },
    {
      path   = ".github/workflows/bulk-repo-sync.yml"
      reason = "MokoStandards sync workflow - CRITICAL for repo sync operations"
    },
    {
      path   = ".github/workflows/confidentiality-scan.yml"
      reason = "MokoStandards security scanning workflow"
    },
    {
      path   = ".github/workflows/enterprise-firewall-setup.yml"
      reason = "MokoStandards enterprise setup workflow"
    },
    {
      path   = ".github/workflows/enterprise-issue-manager.yml"
      reason = "MokoStandards issue management workflow"
    },
    {
      path   = ".github/workflows/flush-actions-cache.yml"
      reason = "MokoStandards maintenance workflow"
    },
    {
      path   = ".github/workflows/repo-health.yml"
      reason = "MokoStandards health check workflow"
    },
    {
      path   = ".github/workflows/standards-compliance.yml"
      reason = "MokoStandards compliance checking workflow"
    },
    {
      path   = ".github/workflows/sync-changelogs.yml"
      reason = "MokoStandards changelog sync workflow"
    },
    
    # Reusable workflows (callable by other workflows)
    {
      path   = ".github/workflows/reusable-build.yml"
      reason = "Reusable workflow template - callable by other workflows"
    },
    {
      path   = ".github/workflows/reusable-ci-validation.yml"
      reason = "Reusable workflow template - callable by other workflows"
    },
    {
      path   = ".github/workflows/reusable-deploy.yml"
      reason = "Reusable workflow template - callable by other workflows"
    },
    {
      path   = ".github/workflows/reusable-php-quality.yml"
      reason = "Reusable workflow template - callable by other workflows"
    },
    {
      path   = ".github/workflows/reusable-platform-testing.yml"
      reason = "Reusable workflow template - callable by other workflows"
    },
    {
      path   = ".github/workflows/reusable-project-detector.yml"
      reason = "Reusable workflow template - callable by other workflows"
    },
    {
      path   = ".github/workflows/reusable-release.yml"
      reason = "Reusable workflow template - callable by other workflows"
    },
    {
      path   = ".github/workflows/reusable-script-executor.yml"
      reason = "Reusable workflow template - callable by other workflows"
    },
    
    # Template directories and critical scripts
    {
      path   = "templates/"
      reason = "Template files repository - source of truth for synced files"
    },
    {
      path   = "scripts/automation/bulk_update_repos.py"
      reason = "Core sync script - critical for bulk repository updates"
    },
    {
      path   = "scripts/"
      reason = "MokoStandards scripts directory"
    },
    {
      path   = "docs/"
      reason = "MokoStandards documentation"
    },
    {
      path   = "terraform/"
      reason = "MokoStandards Terraform configurations"
    },
  ]
}
