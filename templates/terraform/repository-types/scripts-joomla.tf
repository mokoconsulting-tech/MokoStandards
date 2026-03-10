# Joomla Script Library Definitions
# Defines all Joomla-specific script templates for repository health and automation
# Version: 04.00.04

locals {
  joomla_scripts_metadata = {
    name              = "Joomla Script Library"
    version           = "04.00.04"
    description       = "Comprehensive Joomla extension development and automation scripts"
    maintainer        = "MokoStandards Team"
    last_updated      = "2026-02-27"
    repository_url    = "https://github.com/mokoconsulting-tech/MokoStandards"
    documentation_url = "https://github.com/mokoconsulting-tech/MokoStandards/tree/main/templates/scripts/joomla"
  }
  
  # Script categories and their importance weighting
  joomla_script_categories = {
    release = {
      weight      = 10
      description = "Release automation and packaging"
      required    = true
      health_impact = "critical"
    }
    validate = {
      weight      = 8
      description = "Validation and quality assurance"
      required    = true
      health_impact = "high"
    }
    fix = {
      weight      = 6
      description = "Automated fixes and corrections"
      required    = false
      health_impact = "medium"
    }
    build = {
      weight      = 7
      description = "Build automation and asset compilation"
      required    = true
      health_impact = "high"
    }
    test = {
      weight      = 9
      description = "Testing and compatibility checks"
      required    = true
      health_impact = "critical"
    }
    dev = {
      weight      = 5
      description = "Development tools and utilities"
      required    = false
      health_impact = "low"
    }
  }
  
  # Release automation scripts
  joomla_release_scripts = {
    package = {
      template_path = "templates/scripts/joomla/release/package.template.php"
      target_path   = "scripts/release/package.php"
      description   = "Package Joomla extension with update.xml generation"
      required      = true
      health_points = 5
      category      = "release"
      features      = [
        "automatic packaging",
        "update.xml generation",
        "checksum generation (SHA256, SHA512, MD5)",
        "GitHub release integration",
        "version management",
        "manifest validation"
      ]
      dependencies = ["CliBase"]
      joomla_versions = ["3.10", "4.x", "5.x"]
    }
    
    version_bump = {
      template_path = "templates/scripts/joomla/release/version_bump.template.php"
      target_path   = "scripts/release/version_bump.php"
      description   = "Update version across manifest and extension files"
      required      = false
      health_points = 2
      category      = "release"
      features      = ["version update", "manifest update", "changelog update"]
      dependencies  = ["CliBase"]
      joomla_versions = ["3.10", "4.x", "5.x"]
    }
    
    changelog_generator = {
      template_path = "templates/scripts/joomla/release/changelog_generator.template.php"
      target_path   = "scripts/release/changelog_generator.php"
      description   = "Generate changelog from git commits"
      required      = false
      health_points = 1
      category      = "release"
      features      = ["git integration", "conventional commits", "markdown output"]
      dependencies  = ["CliBase"]
      joomla_versions = ["3.10", "4.x", "5.x"]
    }
    
    github_release = {
      template_path = "templates/scripts/joomla/release/github_release.template.php"
      target_path   = "scripts/release/github_release.php"
      description   = "Create GitHub release with assets"
      required      = false
      health_points = 2
      category      = "release"
      features      = ["GitHub API integration", "asset upload", "release notes"]
      dependencies  = ["CliBase"]
      joomla_versions = ["3.10", "4.x", "5.x"]
    }
  }
  
  # Validation scripts
  joomla_validate_scripts = {
    manifest = {
      template_path = "templates/scripts/joomla/validate/manifest.template.php"
      target_path   = "scripts/validate/manifest.php"
      description   = "Validate Joomla manifest XML structure and content"
      required      = true
      health_points = 3
      category      = "validate"
      features      = ["XML validation", "schema checking", "version validation"]
      dependencies  = ["CliBase"]
      joomla_versions = ["3.10", "4.x", "5.x"]
    }
    
    language_files = {
      template_path = "templates/scripts/joomla/validate/language_files.template.php"
      target_path   = "scripts/validate/language_files.php"
      description   = "Validate language file structure and keys"
      required      = true
      health_points = 2
      category      = "validate"
      features      = ["INI file validation", "key checking", "encoding validation"]
      dependencies  = ["CliBase"]
      joomla_versions = ["3.10", "4.x", "5.x"]
    }
    
    sql_files = {
      template_path = "templates/scripts/joomla/validate/sql_files.template.php"
      target_path   = "scripts/validate/sql_files.php"
      description   = "Validate SQL install/uninstall scripts"
      required      = true
      health_points = 3
      category      = "validate"
      features      = ["SQL syntax checking", "security validation", "migration validation"]
      dependencies  = ["CliBase"]
      joomla_versions = ["3.10", "4.x", "5.x"]
    }
    
    php_standards = {
      template_path = "templates/scripts/joomla/validate/php_standards.template.php"
      target_path   = "scripts/validate/php_standards.php"
      description   = "Check Joomla coding standards compliance"
      required      = true
      health_points = 3
      category      = "validate"
      features      = ["PSR-12 checking", "Joomla standards", "PHP_CodeSniffer integration"]
      dependencies  = ["CliBase"]
      joomla_versions = ["3.10", "4.x", "5.x"]
    }
    
    namespace_validation = {
      template_path = "templates/scripts/joomla/validate/namespace.template.php"
      target_path   = "scripts/validate/namespace.php"
      description   = "Validate PHP namespaces for Joomla 4+"
      required      = false
      health_points = 2
      category      = "validate"
      features      = ["namespace checking", "autoloading validation", "PSR-4 compliance"]
      dependencies  = ["CliBase"]
      joomla_versions = ["4.x", "5.x"]
    }
    
    update_server = {
      template_path = "templates/scripts/joomla/validate/update_server.template.php"
      target_path   = "scripts/validate/update_server.php"
      description   = "Validate update.xml structure and URLs"
      required      = false
      health_points = 2
      category      = "validate"
      features      = ["update.xml validation", "URL checking", "version validation"]
      dependencies  = ["CliBase", "UpdateXmlGenerator"]
      joomla_versions = ["3.10", "4.x", "5.x"]
    }
    
    security = {
      template_path = "templates/scripts/joomla/validate/security.template.php"
      target_path   = "scripts/validate/security.php"
      description   = "Security checks (SQL injection, XSS, etc.)"
      required      = true
      health_points = 4
      category      = "validate"
      features      = ["SQL injection detection", "XSS checking", "security best practices"]
      dependencies  = ["CliBase"]
      joomla_versions = ["3.10", "4.x", "5.x"]
    }
  }
  
  # Fix/auto-correction scripts
  joomla_fix_scripts = {
    coding_standards = {
      template_path = "templates/scripts/joomla/fix/coding_standards.template.php"
      target_path   = "scripts/fix/coding_standards.php"
      description   = "Auto-fix coding standard violations"
      required      = false
      health_points = 2
      category      = "fix"
      features      = ["PHPCBF integration", "auto-formatting", "style fixes"]
      dependencies  = ["CliBase"]
      joomla_versions = ["3.10", "4.x", "5.x"]
    }
    
    language_sort = {
      template_path = "templates/scripts/joomla/fix/language_sort.template.php"
      target_path   = "scripts/fix/language_sort.php"
      description   = "Sort language file keys alphabetically"
      required      = false
      health_points = 1
      category      = "fix"
      features      = ["key sorting", "formatting", "backup creation"]
      dependencies  = ["CliBase"]
      joomla_versions = ["3.10", "4.x", "5.x"]
    }
    
    permissions = {
      template_path = "templates/scripts/joomla/fix/permissions.template.php"
      target_path   = "scripts/fix/permissions.php"
      description   = "Fix file and directory permissions"
      required      = false
      health_points = 1
      category      = "fix"
      features      = ["permission fixing", "recursive operation", "dry-run mode"]
      dependencies  = ["CliBase"]
      joomla_versions = ["3.10", "4.x", "5.x"]
    }
  }
  
  # Build automation scripts
  joomla_build_scripts = {
    compile_assets = {
      template_path = "templates/scripts/joomla/build/compile_assets.template.php"
      target_path   = "scripts/build/compile_assets.php"
      description   = "Compile SCSS, minify JS/CSS"
      required      = false
      health_points = 2
      category      = "build"
      features      = ["SCSS compilation", "JS/CSS minification", "asset optimization"]
      dependencies  = ["CliBase"]
      joomla_versions = ["3.10", "4.x", "5.x"]
    }
    
    create_package = {
      template_path = "templates/scripts/joomla/build/create_package.template.php"
      target_path   = "scripts/build/create_package.php"
      description   = "Build installable package"
      required      = true
      health_points = 3
      category      = "build"
      features      = ["ZIP creation", "file filtering", "structure validation"]
      dependencies  = ["CliBase"]
      joomla_versions = ["3.10", "4.x", "5.x"]
    }
  }
  
  # Test scripts
  joomla_test_scripts = {
    install = {
      template_path = "templates/scripts/joomla/test/install.template.php"
      target_path   = "scripts/test/install.php"
      description   = "Test installation process"
      required      = false
      health_points = 2
      category      = "test"
      features      = ["installation testing", "database setup", "error detection"]
      dependencies  = ["CliBase"]
      joomla_versions = ["3.10", "4.x", "5.x"]
    }
    
    compatibility = {
      template_path = "templates/scripts/joomla/test/compatibility.template.php"
      target_path   = "scripts/test/compatibility.php"
      description   = "Test across Joomla versions"
      required      = false
      health_points = 3
      category      = "test"
      features      = ["multi-version testing", "compatibility checking", "report generation"]
      dependencies  = ["CliBase"]
      joomla_versions = ["3.10", "4.x", "5.x"]
    }
  }
  
  # Development tools
  joomla_dev_scripts = {
    symlink = {
      template_path = "templates/scripts/joomla/dev/symlink.template.php"
      target_path   = "scripts/dev/symlink.php"
      description   = "Symlink extension to Joomla installation"
      required      = false
      health_points = 1
      category      = "dev"
      features      = ["symlink creation", "path detection", "automatic linking"]
      dependencies  = ["CliBase"]
      joomla_versions = ["3.10", "4.x", "5.x"]
    }
    
    generate_stub = {
      template_path = "templates/scripts/joomla/dev/generate_stub.template.php"
      target_path   = "scripts/dev/generate_stub.php"
      description   = "Generate extension boilerplate"
      required      = false
      health_points = 1
      category      = "dev"
      features      = ["boilerplate generation", "template system", "customization"]
      dependencies  = ["CliBase"]
      joomla_versions = ["3.10", "4.x", "5.x"]
    }
  }
  
  # Aggregate all Joomla scripts
  joomla_all_scripts = merge(
    local.joomla_release_scripts,
    local.joomla_validate_scripts,
    local.joomla_fix_scripts,
    local.joomla_build_scripts,
    local.joomla_test_scripts,
    local.joomla_dev_scripts
  )
  
  # Calculate total health points for Joomla scripts
  joomla_scripts_total_points = sum([
    for script in local.joomla_all_scripts : script.health_points
  ])
  
  # Required scripts count
  joomla_required_scripts = {
    for key, script in local.joomla_all_scripts : key => script
    if script.required == true
  }
}

# Output for integration with health checks
output "joomla_scripts_summary" {
  description = "Summary of Joomla script library"
  value = {
    metadata          = local.joomla_scripts_metadata
    total_scripts     = length(local.joomla_all_scripts)
    required_scripts  = length(local.joomla_required_scripts)
    total_points      = local.joomla_scripts_total_points
    categories        = local.joomla_script_categories
    release_scripts   = length(local.joomla_release_scripts)
    validate_scripts  = length(local.joomla_validate_scripts)
    fix_scripts       = length(local.joomla_fix_scripts)
    build_scripts     = length(local.joomla_build_scripts)
    test_scripts      = length(local.joomla_test_scripts)
    dev_scripts       = length(local.joomla_dev_scripts)
  }
}
