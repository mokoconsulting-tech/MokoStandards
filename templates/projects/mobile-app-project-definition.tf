/**
 * Mobile App Project Template
 * Standard project configuration for mobile application development
 * 
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 * SPDX-License-Identifier: GPL-3.0-or-later
 * Version: 1.0.0
 */

locals {
  project_config = {
    project = {
      name        = "Mobile App Project"
      description = "Standard project template for mobile application development (React Native, Flutter, Native)"
      visibility  = "private"
      readme      = "https://github.com/mokoconsulting-tech/MokoStandards/blob/main/templates/projects/README.md"
      type        = "mobile"
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
        name        = "Platform"
        type        = "single_select"
        description = "Target mobile platform"
        options     = ["iOS Only", "Android Only", "Both (iOS + Android)", "Cross-Platform"]
      },
      {
        name        = "Framework"
        type        = "single_select"
        description = "Mobile development framework"
        options     = ["React Native", "Flutter", "Native iOS (Swift)", "Native iOS (Obj-C)", "Native Android (Kotlin)", "Native Android (Java)", "Ionic", "Xamarin", "Cordova", "Other"]
      },
      {
        name        = "iOS Minimum"
        type        = "single_select"
        description = "Minimum iOS version"
        options     = ["13.0", "14.0", "15.0", "16.0", "17.0", "N/A"]
      },
      {
        name        = "Android Minimum"
        type        = "single_select"
        description = "Minimum Android API level"
        options     = ["API 23 (6.0)", "API 24 (7.0)", "API 26 (8.0)", "API 28 (9.0)", "API 29 (10)", "API 30 (11)", "API 31 (12)", "API 33 (13)", "API 34 (14)", "N/A"]
      },
      {
        name        = "App Store Status"
        type        = "single_select"
        description = "Apple App Store submission status"
        options     = ["Not Submitted", "In Review", "Pending Release", "Published", "Rejected", "Removed", "N/A"]
      },
      {
        name        = "Play Store Status"
        type        = "single_select"
        description = "Google Play Store submission status"
        options     = ["Not Submitted", "In Review", "Pending Release", "Published", "Rejected", "Suspended", "N/A"]
      },
      {
        name        = "Build Number"
        type        = "text"
        description = "Current build number"
      },
      {
        name        = "Version Code"
        type        = "text"
        description = "Current version code/number"
      },
      {
        name        = "TestFlight/Beta"
        type        = "single_select"
        description = "Beta testing availability"
        options     = ["TestFlight Active", "Google Play Beta", "Both", "None"]
      },
      {
        name        = "Distribution Type"
        type        = "single_select"
        description = "App distribution method"
        options     = ["Public Store", "Enterprise", "Beta Only", "Private", "Multi-Channel"]
      },
      {
        name        = "Push Notifications"
        type        = "single_select"
        description = "Push notification support"
        options     = ["FCM", "APNs", "Both", "None"]
      },
      {
        name        = "Analytics"
        type        = "single_select"
        description = "Analytics platform used"
        options     = ["Firebase", "App Center", "Mixpanel", "Amplitude", "Custom", "Multiple", "None"]
      },
      {
        name        = "Offline Support"
        type        = "single_select"
        description = "Offline functionality"
        options     = ["Full Offline", "Partial Offline", "Online Only"]
      },
      {
        name        = "App Size"
        type        = "text"
        description = "Approximate app size (MB)"
      },
      {
        name        = "License Type"
        type        = "single_select"
        description = "Software license"
        options     = ["Proprietary", "MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause", "Other"]
      },
    ]

    views = [
      {
        name        = "Master Backlog"
        type        = "table"
        description = "All items ordered by priority"
        columns     = ["Title", "Status", "Priority", "Size/Effort", "Platform", "Assignee", "Sprint"]
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
        name        = "Platform Matrix"
        type        = "table"
        description = "Platform compatibility overview"
        columns     = ["Title", "Platform", "iOS Minimum", "Android Minimum", "Framework", "Status"]
      },
      {
        name        = "Store Submission Tracker"
        type        = "table"
        description = "App store submission pipeline"
        columns     = ["Title", "App Store Status", "Play Store Status", "Version Code", "Build Number", "TestFlight/Beta"]
      },
      {
        name        = "iOS Pipeline"
        type        = "board"
        description = "Apple App Store workflow"
        group_by    = "App Store Status"
        columns     = ["Not Submitted", "In Review", "Pending Release", "Published"]
      },
      {
        name        = "Android Pipeline"
        type        = "board"
        description = "Google Play Store workflow"
        group_by    = "Play Store Status"
        columns     = ["Not Submitted", "In Review", "Pending Release", "Published"]
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
        name    = "Store approval notification"
        trigger = "field_changed"
        field   = "App Store Status"
        condition = {
          operator = "equals"
          value    = "Published"
        }
        actions = [
          {
            notify    = "team"
            add_label = "ios-live"
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

output "mobile_app_project_config" {
  description = "Mobile App project template configuration"
  value       = local.project_config
}
