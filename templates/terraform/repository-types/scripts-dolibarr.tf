# Dolibarr Script Library Definitions
# Defines all Dolibarr-specific script templates for module development and automation
# Version: 04.00.04

locals {
  dolibarr_scripts_metadata = {
    name              = "Dolibarr Script Library"
    version           = "04.00.04"
    description       = "Comprehensive Dolibarr module development and automation scripts"
    maintainer        = "MokoStandards Team"
    last_updated      = "2026-02-27"
    repository_url    = "https://github.com/mokoconsulting-tech/MokoStandards"
    documentation_url = "https://github.com/mokoconsulting-tech/MokoStandards/tree/main/templates/scripts/dolibarr"
  }
  
  # Script categories and their importance weighting
  dolibarr_script_categories = {
    release = {
      weight        = 10
      description   = "Release automation and packaging for Dolistore"
      required      = true
      health_impact = "critical"
    }
    validate = {
      weight        = 8
      description   = "Module validation and quality assurance"
      required      = true
      health_impact = "high"
    }
    fix = {
      weight        = 6
      description   = "Automated fixes and corrections"
      required      = false
      health_impact = "medium"
    }
    build = {
      weight        = 7
      description   = "Build automation and asset compilation"
      required      = true
      health_impact = "high"
    }
    test = {
      weight        = 9
      description   = "Testing and compatibility checks"
      required      = true
      health_impact = "critical"
    }
    dev = {
      weight        = 5
      description   = "Development tools and utilities"
      required      = false
      health_impact = "low"
    }
  }
  
  # Release automation scripts
  dolibarr_release_scripts = {
    package = {
      template_path     = "templates/scripts/dolibarr/release/package.template.php"
      target_path       = "scripts/release/package.php"
      description       = "Package Dolibarr module for Dolistore"
      required          = true
      health_points     = 5
      category          = "release"
      features          = [
        "module packaging",
        "descriptor validation",
        "ZIP creation",
        "checksum generation",
        "Dolistore formatting"
      ]
      dependencies      = ["CliBase"]
      dolibarr_versions = ["13.0", "14.0", "15.0", "16.0", "17.0"]
    }
    
    version_bump = {
      template_path     = "templates/scripts/dolibarr/release/version_bump.template.php"
      target_path       = "scripts/release/version_bump.php"
      description       = "Update version in module descriptor"
      required          = false
      health_points     = 2
      category          = "release"
      features          = ["version update", "descriptor update", "changelog sync"]
      dependencies      = ["CliBase"]
      dolibarr_versions = ["13.0", "14.0", "15.0", "16.0", "17.0"]
    }
    
    changelog_generator = {
      template_path     = "templates/scripts/dolibarr/release/changelog_generator.template.php"
      target_path       = "scripts/release/changelog_generator.php"
      description       = "Generate changelog from git commits"
      required          = false
      health_points     = 1
      category          = "release"
      features          = ["git integration", "changelog formatting", "Dolibarr style"]
      dependencies      = ["CliBase"]
      dolibarr_versions = ["13.0", "14.0", "15.0", "16.0", "17.0"]
    }
    
    github_release = {
      template_path     = "templates/scripts/dolibarr/release/github_release.template.php"
      target_path       = "scripts/release/github_release.php"
      description       = "Create GitHub release with module package"
      required          = false
      health_points     = 2
      category          = "release"
      features          = ["GitHub API", "asset upload", "release notes"]
      dependencies      = ["CliBase"]
      dolibarr_versions = ["13.0", "14.0", "15.0", "16.0", "17.0"]
    }
  }
  
  # Validation scripts
  dolibarr_validate_scripts = {
    module = {
      template_path     = "templates/scripts/dolibarr/validate/module.template.php"
      target_path       = "scripts/validate/module.php"
      description       = "Validate Dolibarr module structure and configuration"
      required          = true
      health_points     = 4
      category          = "validate"
      features          = ["structure validation", "descriptor checking", "file validation"]
      dependencies      = ["CliBase"]
      dolibarr_versions = ["13.0", "14.0", "15.0", "16.0", "17.0"]
    }
    
    module_descriptor = {
      template_path     = "templates/scripts/dolibarr/validate/module_descriptor.template.php"
      target_path       = "scripts/validate/module_descriptor.php"
      description       = "Validate module descriptor file"
      required          = true
      health_points     = 3
      category          = "validate"
      features          = ["descriptor validation", "module number checking", "dependency validation"]
      dependencies      = ["CliBase"]
      dolibarr_versions = ["13.0", "14.0", "15.0", "16.0", "17.0"]
    }
    
    permissions = {
      template_path     = "templates/scripts/dolibarr/validate/permissions.template.php"
      target_path       = "scripts/validate/permissions.php"
      description       = "Check Dolibarr permission configuration"
      required          = true
      health_points     = 2
      category          = "validate"
      features          = ["permission validation", "rights checking", "ACL validation"]
      dependencies      = ["CliBase"]
      dolibarr_versions = ["13.0", "14.0", "15.0", "16.0", "17.0"]
    }
    
    sql_files = {
      template_path     = "templates/scripts/dolibarr/validate/sql_files.template.php"
      target_path       = "scripts/validate/sql_files.php"
      description       = "Validate SQL scripts for Dolibarr"
      required          = true
      health_points     = 3
      category          = "validate"
      features          = ["SQL syntax", "migration validation", "table prefix checking"]
      dependencies      = ["CliBase"]
      dolibarr_versions = ["13.0", "14.0", "15.0", "16.0", "17.0"]
    }
    
    hooks = {
      template_path     = "templates/scripts/dolibarr/validate/hooks.template.php"
      target_path       = "scripts/validate/hooks.php"
      description       = "Validate hook implementations"
      required          = false
      health_points     = 2
      category          = "validate"
      features          = ["hook validation", "context checking", "parameter validation"]
      dependencies      = ["CliBase"]
      dolibarr_versions = ["13.0", "14.0", "15.0", "16.0", "17.0"]
    }
    
    language_files = {
      template_path     = "templates/scripts/dolibarr/validate/language_files.template.php"
      target_path       = "scripts/validate/language_files.php"
      description       = "Validate language files"
      required          = true
      health_points     = 2
      category          = "validate"
      features          = ["language file validation", "encoding check", "key validation"]
      dependencies      = ["CliBase"]
      dolibarr_versions = ["13.0", "14.0", "15.0", "16.0", "17.0"]
    }
    
    php_standards = {
      template_path     = "templates/scripts/dolibarr/validate/php_standards.template.php"
      target_path       = "scripts/validate/php_standards.php"
      description       = "Check Dolibarr coding standards"
      required          = true
      health_points     = 3
      category          = "validate"
      features          = ["coding standards", "PSR-12", "Dolibarr conventions"]
      dependencies      = ["CliBase"]
      dolibarr_versions = ["13.0", "14.0", "15.0", "16.0", "17.0"]
    }
    
    security = {
      template_path     = "templates/scripts/dolibarr/validate/security.template.php"
      target_path       = "scripts/validate/security.php"
      description       = "Security checks for Dolibarr modules"
      required          = true
      health_points     = 4
      category          = "validate"
      features          = ["security scanning", "SQL injection check", "XSS detection"]
      dependencies      = ["CliBase"]
      dolibarr_versions = ["13.0", "14.0", "15.0", "16.0", "17.0"]
    }
    
    compatibility = {
      template_path     = "templates/scripts/dolibarr/validate/compatibility.template.php"
      target_path       = "scripts/validate/compatibility.php"
      description       = "Test Dolibarr version compatibility"
      required          = false
      health_points     = 2
      category          = "validate"
      features          = ["version checking", "API compatibility", "deprecation detection"]
      dependencies      = ["CliBase"]
      dolibarr_versions = ["13.0", "14.0", "15.0", "16.0", "17.0"]
    }
  }
  
  # Fix/auto-correction scripts
  dolibarr_fix_scripts = {
    coding_standards = {
      template_path     = "templates/scripts/dolibarr/fix/coding_standards.template.php"
      target_path       = "scripts/fix/coding_standards.php"
      description       = "Auto-fix coding standard violations"
      required          = false
      health_points     = 2
      category          = "fix"
      features          = ["auto-fix", "PHPCBF", "formatting"]
      dependencies      = ["CliBase"]
      dolibarr_versions = ["13.0", "14.0", "15.0", "16.0", "17.0"]
    }
    
    permissions = {
      template_path     = "templates/scripts/dolibarr/fix/permissions.template.php"
      target_path       = "scripts/fix/permissions.php"
      description       = "Fix file permissions"
      required          = false
      health_points     = 1
      category          = "fix"
      features          = ["permission fixing", "recursive", "dry-run"]
      dependencies      = ["CliBase"]
      dolibarr_versions = ["13.0", "14.0", "15.0", "16.0", "17.0"]
    }
    
    module_descriptor = {
      template_path     = "templates/scripts/dolibarr/fix/module_descriptor.template.php"
      target_path       = "scripts/fix/module_descriptor.php"
      description       = "Fix common descriptor issues"
      required          = false
      health_points     = 2
      category          = "fix"
      features          = ["descriptor fixing", "formatting", "validation"]
      dependencies      = ["CliBase"]
      dolibarr_versions = ["13.0", "14.0", "15.0", "16.0", "17.0"]
    }
  }
  
  # Build automation scripts
  dolibarr_build_scripts = {
    compile_assets = {
      template_path     = "templates/scripts/dolibarr/build/compile_assets.template.php"
      target_path       = "scripts/build/compile_assets.php"
      description       = "Compile and minify assets"
      required          = false
      health_points     = 2
      category          = "build"
      features          = ["asset compilation", "minification", "optimization"]
      dependencies      = ["CliBase"]
      dolibarr_versions = ["13.0", "14.0", "15.0", "16.0", "17.0"]
    }
    
    create_package = {
      template_path     = "templates/scripts/dolibarr/build/create_package.template.php"
      target_path       = "scripts/build/create_package.php"
      description       = "Build module package"
      required          = true
      health_points     = 3
      category          = "build"
      features          = ["package creation", "ZIP building", "validation"]
      dependencies      = ["CliBase"]
      dolibarr_versions = ["13.0", "14.0", "15.0", "16.0", "17.0"]
    }
    
    generate_documentation = {
      template_path     = "templates/scripts/dolibarr/build/generate_documentation.template.php"
      target_path       = "scripts/build/generate_documentation.php"
      description       = "Generate module documentation"
      required          = false
      health_points     = 1
      category          = "build"
      features          = ["doc generation", "API docs", "user guide"]
      dependencies      = ["CliBase"]
      dolibarr_versions = ["13.0", "14.0", "15.0", "16.0", "17.0"]
    }
  }
  
  # Test scripts
  dolibarr_test_scripts = {
    install = {
      template_path     = "templates/scripts/dolibarr/test/install.template.php"
      target_path       = "scripts/test/install.php"
      description       = "Test module installation"
      required          = false
      health_points     = 2
      category          = "test"
      features          = ["install testing", "database setup", "error detection"]
      dependencies      = ["CliBase"]
      dolibarr_versions = ["13.0", "14.0", "15.0", "16.0", "17.0"]
    }
    
    upgrade = {
      template_path     = "templates/scripts/dolibarr/test/upgrade.template.php"
      target_path       = "scripts/test/upgrade.php"
      description       = "Test module upgrade"
      required          = false
      health_points     = 2
      category          = "test"
      features          = ["upgrade testing", "migration validation", "data integrity"]
      dependencies      = ["CliBase"]
      dolibarr_versions = ["13.0", "14.0", "15.0", "16.0", "17.0"]
    }
    
    compatibility = {
      template_path     = "templates/scripts/dolibarr/test/compatibility.template.php"
      target_path       = "scripts/test/compatibility.php"
      description       = "Test Dolibarr compatibility"
      required          = false
      health_points     = 3
      category          = "test"
      features          = ["version testing", "compatibility check", "report generation"]
      dependencies      = ["CliBase"]
      dolibarr_versions = ["13.0", "14.0", "15.0", "16.0", "17.0"]
    }
  }
  
  # Development tools
  dolibarr_dev_scripts = {
    symlink = {
      template_path     = "templates/scripts/dolibarr/dev/symlink.template.php"
      target_path       = "scripts/dev/symlink.php"
      description       = "Symlink module to Dolibarr installation"
      required          = false
      health_points     = 1
      category          = "dev"
      features          = ["symlink creation", "path detection", "auto-linking"]
      dependencies      = ["CliBase"]
      dolibarr_versions = ["13.0", "14.0", "15.0", "16.0", "17.0"]
    }
    
    module_id_reserve = {
      template_path     = "templates/scripts/dolibarr/dev/module_id_reserve.template.php"
      target_path       = "scripts/dev/module_id_reserve.php"
      description       = "Reserve module ID from registry"
      required          = false
      health_points     = 2
      category          = "dev"
      features          = ["ID reservation", "registry interaction", "conflict checking"]
      dependencies      = ["CliBase"]
      dolibarr_versions = ["13.0", "14.0", "15.0", "16.0", "17.0"]
    }
    
    generate_stub = {
      template_path     = "templates/scripts/dolibarr/dev/generate_stub.template.php"
      target_path       = "scripts/dev/generate_stub.php"
      description       = "Generate module boilerplate"
      required          = false
      health_points     = 1
      category          = "dev"
      features          = ["boilerplate generation", "template system", "customization"]
      dependencies      = ["CliBase"]
      dolibarr_versions = ["13.0", "14.0", "15.0", "16.0", "17.0"]
    }
  }
  
  # Aggregate all Dolibarr scripts
  dolibarr_all_scripts = merge(
    local.dolibarr_release_scripts,
    local.dolibarr_validate_scripts,
    local.dolibarr_fix_scripts,
    local.dolibarr_build_scripts,
    local.dolibarr_test_scripts,
    local.dolibarr_dev_scripts
  )
  
  # Calculate total health points for Dolibarr scripts
  dolibarr_scripts_total_points = sum([
    for script in local.dolibarr_all_scripts : script.health_points
  ])
  
  # Required scripts count
  dolibarr_required_scripts = {
    for key, script in local.dolibarr_all_scripts : key => script
    if script.required == true
  }
}

# Output for integration with health checks
output "dolibarr_scripts_summary" {
  description = "Summary of Dolibarr script library"
  value = {
    metadata          = local.dolibarr_scripts_metadata
    total_scripts     = length(local.dolibarr_all_scripts)
    required_scripts  = length(local.dolibarr_required_scripts)
    total_points      = local.dolibarr_scripts_total_points
    categories        = local.dolibarr_script_categories
    release_scripts   = length(local.dolibarr_release_scripts)
    validate_scripts  = length(local.dolibarr_validate_scripts)
    fix_scripts       = length(local.dolibarr_fix_scripts)
    build_scripts     = length(local.dolibarr_build_scripts)
    test_scripts      = length(local.dolibarr_test_scripts)
    dev_scripts       = length(local.dolibarr_dev_scripts)
  }
}
