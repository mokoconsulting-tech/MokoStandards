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
# VERSION: 02.00.00
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
  override_metadata = {
    name              = "MokoStandards Repository Override"
    repository_type   = "standards"
    compliance_level  = "strict"
    config_version    = "2.0"
    format            = "terraform"
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
      reason = "corresponds to templates/workflows/release-cycle.yml.template"
    },
    {
      path   = ".github/workflows/codeql-analysis.yml"
      reason = "corresponds to templates/workflows/generic/codeql-analysis.yml"
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
}
