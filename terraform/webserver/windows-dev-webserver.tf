# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# FILE INFORMATION
# DEFGROUP: Terraform.WebServer
# INGROUP: MokoStandards.Infrastructure
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: terraform/webserver/windows-dev-webserver.tf
# VERSION: 04.00.01
# BRIEF: Terraform definition for Windows development web server configuration
# ENTERPRISE: Includes audit logging, monitoring, and compliance features


locals {
  # Metadata for this configuration
  # Enterprise-ready: Includes audit logging, monitoring, and compliance features
  config_metadata = {
    name              = "Webserver Windows Dev Webserver"
    description       = "Development Windows webserver infrastructure configuration"
    version           = "04.00.01"
    last_updated      = "2026-02-11"
    maintainer        = "MokoStandards Team"
    schema_version    = "2.0"
    repository_url    = "https://github.com/mokoconsulting-tech/MokoStandards"
    repository_type   = "standards"
    format            = "terraform"
    enterprise_ready  = true
    monitoring_enabled = true
    audit_logging     = true
  }
}

locals {
  windows_dev_webserver_config = {
    metadata = {
      name          = "Windows Development Web Server Configuration"
      version       = "1.0.0"
      description   = "Standardized configuration for Windows development web servers"
      platform      = "windows"
      environment   = "development"
      last_updated  = "2026-01-27T00:00:00Z"
      maintainer    = "MokoStandards Team"
      documentation = "docs/infrastructure/windows-dev-webserver.md"
    }

    # Server identification
    server = {
      role        = "web-server"
      environment = "development"
      tier        = "application"
    }

    # IIS (Internet Information Services) configuration
    iis = {
      version = "10.0" # Windows Server 2019/2022
      install = true

      features = [
        "Web-Server",
        "Web-WebServer",
        "Web-Common-Http",
        "Web-Default-Doc",
        "Web-Dir-Browsing",
        "Web-Http-Errors",
        "Web-Static-Content",
        "Web-Http-Redirect",
        "Web-Health",
        "Web-Http-Logging",
        "Web-Log-Libraries",
        "Web-Request-Monitor",
        "Web-Performance",
        "Web-Stat-Compression",
        "Web-Dyn-Compression",
        "Web-Security",
        "Web-Filtering",
        "Web-Basic-Auth",
        "Web-Windows-Auth",
        "Web-App-Dev",
        "Web-Net-Ext45",
        "Web-Asp-Net45",
        "Web-ISAPI-Ext",
        "Web-ISAPI-Filter",
        "Web-Mgmt-Tools",
        "Web-Mgmt-Console",
        "Web-Scripting-Tools"
      ]

      # Development-specific settings
      development_settings = {
        detailed_errors        = true
        directory_browsing     = true
        custom_errors_mode     = "Off" # Show detailed error pages
        debug_mode             = true
        request_tracing        = true
        failed_request_tracing = true
        auto_start             = true
      }

      # Application pools
      application_pools = {
        default = {
          name                    = "DefaultAppPool"
          runtime_version         = "v4.0"
          pipeline_mode           = "Integrated"
          managed_runtime_version = "v4.0"
          identity_type           = "ApplicationPoolIdentity"

          # Development settings
          idle_timeout  = "00:20:00" # 20 minutes
          max_processes = 1
          start_mode    = "AlwaysRunning"

          # Resource limits (relaxed for dev)
          cpu_limit    = 0 # No limit
          memory_limit = 0 # No limit

          # Recycling
          periodic_restart    = "00:00:00" # No periodic restart in dev
          idle_timeout_action = "Terminate"
        }

        php = {
          name            = "PHPAppPool"
          runtime_version = "No Managed Code"
          pipeline_mode   = "Classic"
          identity_type   = "ApplicationPoolIdentity"
          idle_timeout    = "00:20:00"
          max_processes   = 1
        }
      }

      # Sites configuration
      sites = {
        default = {
          name             = "DevelopmentSite"
          physical_path    = "C:\\inetpub\\wwwroot"
          application_pool = "DefaultAppPool"

          bindings = [
            {
              protocol    = "http"
              ip_address  = "*"
              port        = 80
              host_header = ""
            },
            {
              protocol    = "http"
              ip_address  = "*"
              port        = 8080
              host_header = ""
            }
          ]

          # Development features
          auto_start      = true
          preload_enabled = false # Not needed in dev
        }
      }

      # URL Rewrite module
      url_rewrite = {
        install = true
        version = "2.1"

        # Common development rules
        rules = {
          force_https    = false # Don't force HTTPS in dev
          www_redirect   = false
          trailing_slash = false
        }
      }
    }

    # PHP configuration
    php = {
      version = "8.3"
      install = true

      # PHP via FastCGI
      fastcgi = {
        enabled          = true
        max_instances    = 4 # Reduced for dev
        instance_timeout = 600
        activity_timeout = 600
        request_timeout  = 600
        protocol         = "NamedPipe"
      }

      packages = [
        "php",
        "php-devel",
        "php-mysql",
        "php-pgsql",
        "php-curl",
        "php-mbstring",
        "php-intl",
        "php-gd",
        "php-zip",
        "php-soap",
        "php-xml",
        "php-bcmath",
        "php-opcache",
        "php-redis",
        "php-xdebug"
      ]

      # php.ini settings for development
      ini_settings = {
        display_errors         = "On"
        display_startup_errors = "On"
        error_reporting        = "E_ALL"
        log_errors             = "On"
        error_log              = "C:\\logs\\php\\php-error.log"

        max_execution_time  = "300"
        max_input_time      = "300"
        memory_limit        = "512M"
        post_max_size       = "100M"
        upload_max_filesize = "100M"

        # Opcache settings (moderate for dev)
        "opcache.enable"              = "1"
        "opcache.enable_cli"          = "1"
        "opcache.memory_consumption"  = "128"
        "opcache.revalidate_freq"     = "2" # Check for changes every 2 seconds
        "opcache.validate_timestamps" = "1" # Enable in dev

        # Xdebug settings for development
        "xdebug.mode"               = "debug,develop"
        "xdebug.start_with_request" = "trigger"
        "xdebug.client_host"        = "localhost"
        "xdebug.client_port"        = "9003"
        "xdebug.log"                = "C:\\logs\\php\\xdebug.log"
      }

      # Composer
      composer = {
        install = true
        global_packages = [
          "phpunit/phpunit",
          "squizlabs/php_codesniffer",
          "phpstan/phpstan",
          "friendsofphp/php-cs-fixer"
        ]
      }
    }

    # ASP.NET Core configuration
    aspnet_core = {
      version = "8.0"
      install = true

      hosting_bundle = {
        install = true
        version = "8.0"
      }

      # Development settings
      environment_variables = {
        ASPNETCORE_ENVIRONMENT = "Development"
        ASPNETCORE_URLS        = "http://*:5000;http://*:5001"
        DOTNET_ENVIRONMENT     = "Development"
      }

      # Kestrel settings for dev
      kestrel = {
        listen_any_ip           = true
        http_port               = 5000
        https_port              = 5001
        development_certificate = true
      }
    }

    # Database connectivity
    databases = {
      mysql = {
        install_client = true
        odbc_driver    = true
        default_port   = 3306
      }

      postgresql = {
        install_client = true
        odbc_driver    = true
        default_port   = 5432
      }

      sql_server = {
        install_tools   = true
        default_port    = 1433
        express_edition = true # For local dev database
      }

      redis = {
        install = true
        port    = 6379
        # Run as Windows service for dev
        windows_service = true
      }
    }

    # File system configuration
    filesystem = {
      web_root = "C:\\inetpub\\wwwroot"

      directories = {
        logs = {
          path        = "C:\\logs\\webserver"
          permissions = "Full"
        }
        uploads = {
          path        = "C:\\inetpub\\wwwroot\\uploads"
          permissions = "Full"
        }
        cache = {
          path        = "C:\\inetpub\\wwwroot\\cache"
          permissions = "Full"
        }
        temp = {
          path        = "C:\\temp\\webserver"
          permissions = "Full"
        }
      }

      # Storage quotas (generous for dev)
      quotas = {
        uploads_max = "50GB"
        logs_max    = "20GB"
        cache_max   = "10GB"
      }
    }

    # SSL/TLS configuration
    ssl = {
      # Self-signed certificates for dev
      enable_ssl      = true
      require_ssl     = false
      use_self_signed = true
      protocols       = ["TLS 1.2", "TLS 1.3"]

      certificate = {
        provider     = "self-signed"
        common_name  = "localhost"
        organization = "Development"
        valid_days   = 365
      }
    }

    # Firewall rules
    firewall = {
      enable_rules = true

      inbound_rules = [
        {
          name     = "HTTP-Dev"
          protocol = "TCP"
          port     = 80
          action   = "Allow"
        },
        {
          name     = "HTTP-Alt-Dev"
          protocol = "TCP"
          port     = 8080
          action   = "Allow"
        },
        {
          name     = "HTTPS-Dev"
          protocol = "TCP"
          port     = 443
          action   = "Allow"
        },
        {
          name     = "ASP.NET-Dev"
          protocol = "TCP"
          port     = 5000
          action   = "Allow"
        },
        {
          name     = "ASP.NET-HTTPS-Dev"
          protocol = "TCP"
          port     = 5001
          action   = "Allow"
        }
      ]
    }

    # Logging configuration
    logging = {
      enabled = true

      iis_logs = {
        path           = "C:\\inetpub\\logs\\LogFiles"
        format         = "W3C"
        fields         = ["date", "time", "s-ip", "cs-method", "cs-uri-stem", "cs-uri-query", "s-port", "cs-username", "c-ip", "cs(User-Agent)", "cs(Referer)", "sc-status", "sc-substatus", "sc-win32-status", "time-taken"]
        rollover       = "Daily"
        retention_days = 30 # Keep logs for 30 days in dev
      }

      php_logs = {
        path           = "C:\\logs\\php"
        error_log      = "php-error.log"
        slow_log       = "php-slow.log"
        retention_days = 30
      }

      application_logs = {
        path           = "C:\\logs\\webserver"
        retention_days = 30
      }

      # Verbose logging for development
      log_level = "Verbose"
    }

    # Performance monitoring
    monitoring = {
      # Development monitoring (basic)
      enable_perfmon      = true
      enable_app_insights = false # Not needed in dev

      # Windows Performance Counters
      performance_counters = [
        "\\Processor(_Total)\\% Processor Time",
        "\\Memory\\Available MBytes",
        "\\Web Service(_Total)\\Current Connections",
        "\\ASP.NET\\Requests Current",
        "\\ASP.NET\\Requests Queued"
      ]

      # Health checks
      health_checks = {
        enabled  = true
        endpoint = "/health"
        interval = 60 # seconds
      }
    }

    # Development tools
    dev_tools = {
      # Install helpful development tools
      install = true

      tools = [
        "Visual Studio Code",
        "Postman",
        "Git for Windows",
        "Windows Terminal",
        "Notepad++",
        "7-Zip"
      ]

      # Browser developer tools
      browsers = [
        "Google Chrome",
        "Mozilla Firefox",
        "Microsoft Edge"
      ]
    }

    # Security settings (relaxed for development)
    security = {
      # Authentication
      authentication = {
        anonymous_enabled    = true
        windows_auth_enabled = false
        basic_auth_enabled   = false
      }

      # CORS (permissive for dev)
      cors = {
        enabled           = true
        allow_origins     = ["*"]
        allow_methods     = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
        allow_headers     = ["*"]
        allow_credentials = true
      }

      # Request filtering (relaxed)
      request_filtering = {
        max_content_length    = "104857600" # 100MB
        max_url_length        = "4096"
        max_query_string      = "2048"
        allow_double_escaping = true
        allow_high_bit_chars  = true
      }

      # Rate limiting (disabled in dev)
      rate_limiting = {
        enabled = false
      }
    }

    # Backup configuration (minimal for dev)
    backup = {
      enabled = false # Usually not needed in dev

      # If enabled, backup configuration
      schedule = {
        frequency = "weekly"
        time      = "02:00"
        day       = "Sunday"
      }

      retention = {
        keep_daily  = 7
        keep_weekly = 4
      }
    }

    # Operations
    operations = {
      auto_start_services = true
      restart_on_failure  = true

      maintenance_window = {
        enabled = false # No maintenance windows in dev
      }

      # Quick restart for development
      graceful_shutdown_timeout = 30 # seconds
    }
  }
}

# Output the configuration
output "windows_dev_webserver_config" {
  description = "Windows development web server configuration"
  value       = local.windows_dev_webserver_config
}

# Output IIS configuration for scripts
output "windows_dev_iis_config" {
  description = "IIS-specific configuration"
  value = {
    features          = local.windows_dev_webserver_config.iis.features
    application_pools = local.windows_dev_webserver_config.iis.application_pools
    sites             = local.windows_dev_webserver_config.iis.sites
    development_mode  = local.windows_dev_webserver_config.iis.development_settings
  }
}

# Output PHP configuration
output "windows_dev_php_config" {
  description = "PHP configuration for Windows dev server"
  value = {
    version      = local.windows_dev_webserver_config.php.version
    packages     = local.windows_dev_webserver_config.php.packages
    ini_settings = local.windows_dev_webserver_config.php.ini_settings
    fastcgi      = local.windows_dev_webserver_config.php.fastcgi
  }
}
