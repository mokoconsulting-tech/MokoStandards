/**
 * WordPress Plugin/Theme Project Template
 * Standard project configuration for WordPress plugin and theme development
 * 
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 * SPDX-License-Identifier: GPL-3.0-or-later
 * Version: 1.0.0
 */

locals {
  project_config = {
    project = {
      name        = "WordPress Plugin/Theme Project"
      description = "Standard project template for WordPress plugin and theme development"
      visibility  = "private"
      readme      = "https://github.com/mokoconsulting-tech/MokoStandards/blob/main/templates/projects/README.md"
      type        = "wordpress"
    }

    custom_fields = [
      {
        name        = "Status"
        type        = "single_select"
        description = "Current lifecycle state of the task"
        options     = ["Backlog", "Todo", "In Progress", "In Review", "Testing", "Done", "Blocked", "Cancelled"]
      },
      {
        name        = "Priority"
        type        = "single_select"
        description = "Urgency and importance of the task"
        options     = ["Critical", "High", "Medium", "Low"]
      },
      {
        name        = "Size/Effort"
        type        = "single_select"
        description = "Estimated complexity and work effort"
        options     = ["XS - 1-2 hours", "S - 2-4 hours", "M - 1-2 days", "L - 3-5 days", "XL - 1-2 weeks", "XXL - 2+ weeks"]
      },
      {
        name        = "Sprint"
        type        = "text"
        description = "Sprint or iteration identifier"
      },
      {
        name        = "Target Version"
        type        = "text"
        description = "Target release version (semantic versioning)"
      },
      {
        name        = "Blocked Reason"
        type        = "text"
        description = "Description of what is blocking progress"
      },
      {
        name        = "Acceptance Criteria"
        type        = "text"
        description = "List of criteria for task completion"
      },
      {
        name        = "WordPress Version"
        type        = "single_select"
        description = "Minimum WordPress version required"
        options     = ["6.0", "6.1", "6.2", "6.3", "6.4", "6.5", "Latest"]
      },
      {
        name        = "Extension Type"
        type        = "single_select"
        description = "Type of WordPress extension"
        options     = ["Plugin", "Theme", "Block", "MU Plugin", "Drop-in"]
      },
      {
        name        = "PHP Minimum"
        type        = "single_select"
        description = "Minimum PHP version required"
        options     = ["7.4", "8.0", "8.1", "8.2", "8.3"]
      },
      {
        name        = "WP.org Status"
        type        = "single_select"
        description = "WordPress.org repository status"
        options     = ["Not Submitted", "In Review", "Approved", "Published", "Rejected", "Closed", "Private"]
      },
      {
        name        = "Plugin Slug"
        type        = "text"
        description = "WordPress.org plugin slug"
      },
      {
        name        = "Plugin Version"
        type        = "text"
        description = "Current plugin/theme version"
      },
      {
        name        = "Tested Up To"
        type        = "single_select"
        description = "Tested up to WordPress version"
        options     = ["6.0", "6.1", "6.2", "6.3", "6.4", "6.5", "Latest"]
      },
      {
        name        = "License Type"
        type        = "single_select"
        description = "Software license"
        options     = ["GPL-2.0", "GPL-3.0", "MIT", "Proprietary", "Other"]
      },
      {
        name        = "Requires Plugins"
        type        = "text"
        description = "Required plugin dependencies"
      },
      {
        name        = "Block Editor"
        type        = "single_select"
        description = "Gutenberg/Block Editor support"
        options     = ["Full Support", "Partial Support", "Classic Only", "N/A"]
      },
      {
        name        = "Multisite Compatible"
        type        = "single_select"
        description = "WordPress multisite compatibility"
        options     = ["Yes", "No", "Partial", "Untested"]
      },
      {
        name        = "Translation Ready"
        type        = "single_select"
        description = "Internationalization (i18n) support"
        options     = ["Yes - Complete", "Yes - Partial", "No"]
      },
      {
        name        = "Active Installs"
        type        = "text"
        description = "Approximate active installations (WP.org)"
      },
      {
        name        = "WP.org Rating"
        type        = "text"
        description = "WordPress.org rating (1-5 stars)"
      },
      {
        name        = "Premium Version"
        type        = "single_select"
        description = "Has premium/pro version?"
        options     = ["Yes", "No", "Planned"]
      },
    ]

    views = [
      {
        name        = "Master Backlog"
        type        = "table"
        description = "All items ordered by priority"
        columns     = ["Title", "Status", "Priority", "Size/Effort", "Extension Type", "Assignee", "Sprint"]
        sort = [
          {
            field     = "Priority"
            direction = "asc"
          }
        ]
      },
      {
        name        = "Sprint Board"
        type        = "board"
        description = "Current sprint work board"
        group_by    = "Status"
        filter = {
          field    = "Sprint"
          operator = "equals"
          value    = "current"
        }
        columns = ["Backlog", "Todo", "In Progress", "In Review", "Testing", "Done"]
      },
      {
        name        = "Release Roadmap"
        type        = "roadmap"
        description = "Timeline view of planned releases"
        group_by    = "Target Version"
        date_field  = "Target Date"
      },
      {
        name        = "Blocked Items"
        type        = "table"
        description = "Tasks currently blocked"
        filter = {
          field    = "Status"
          operator = "equals"
          value    = "Blocked"
        }
        columns = ["Title", "Priority", "Blocked Reason", "Assignee", "Days Blocked"]
      },
      {
        name        = "Compatibility Matrix"
        type        = "table"
        description = "WordPress version compatibility"
        columns     = ["Title", "WordPress Version", "Tested Up To", "PHP Minimum", "Block Editor", "Multisite Compatible", "Status"]
      },
      {
        name        = "WP.org Pipeline"
        type        = "board"
        description = "WordPress.org submission workflow"
        group_by    = "WP.org Status"
        columns     = ["Not Submitted", "In Review", "Approved", "Published"]
      },
      {
        name        = "Extension Type Overview"
        type        = "table"
        description = "Projects by extension type"
        group_by    = "Extension Type"
        columns     = ["Title", "Extension Type", "Plugin Version", "WP.org Status", "Active Installs"]
      },
      {
        name        = "Quality Metrics"
        type        = "table"
        description = "Quality and localization tracking"
        columns     = ["Title", "Translation Ready", "WP.org Rating", "Active Installs", "Premium Version", "Status"]
      },
    ]

    workflows = [
      {
        name    = "Auto-status on PR"
        trigger = "pull_request_opened"
        actions = [
          {
            set_field = "Status"
            value     = "In Review"
          }
        ]
      },
      {
        name    = "Auto-status on merge"
        trigger = "pull_request_merged"
        actions = [
          {
            set_field = "Status"
            value     = "Testing"
          }
        ]
      },
      {
        name    = "Version release notification"
        trigger = "field_changed"
        field   = "Plugin Version"
        actions = [
          {
            notify  = "team"
            message = "New version released"
          }
        ]
      },
      {
        name    = "WP.org approval notification"
        trigger = "field_changed"
        field   = "WP.org Status"
        condition = {
          operator = "in"
          values   = ["Approved", "Published"]
        }
        actions = [
          {
            notify    = "team"
            add_label = "wp-org-live"
          }
        ]
      },
      {
        name    = "Low rating alert"
        trigger = "field_changed"
        field   = "WP.org Rating"
        condition = {
          operator = "less_than"
          value    = "3.5"
        }
        actions = [
          {
            add_label = "needs-improvement"
            notify    = "support_team"
          }
        ]
      },
    ]

    metadata = {
      version = "1.0.0"
      created = "2026-02-27"
      author  = "Moko Consulting"
      license = "GPL-3.0-or-later"
    }
  }
}

output "wordpress_project_config" {
  description = "WordPress Plugin/Theme project template configuration"
  value       = local.project_config
}
