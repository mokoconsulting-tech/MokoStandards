# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# FILE INFORMATION
# DEFGROUP: Terraform.WebServer
# INGROUP: MokoStandards.Infrastructure
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: terraform/webserver/windows-prod-webserver.tf
# VERSION: 03.02.00
# BRIEF: Terraform definition for Windows production web server configuration
# ENTERPRISE: Includes audit logging, monitoring, and compliance features


locals {
  # Metadata for this configuration
  # Enterprise-ready: Includes audit logging, monitoring, and compliance features
  config_metadata = {
    name              = "Webserver Windows Prod Webserver"
    description       = "Production Windows webserver infrastructure configuration"
    version           = "04.00.00"
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
  windows_prod_webserver_config = {
    metadata = {
      name          = "Windows Production Web Server Configuration"
      version       = "1.0.0"
      description   = "Standardized configuration for Windows production web servers"
      platform      = "windows"
      environment   = "production"
      last_updated  = "2026-01-27T00:00:00Z"
      maintainer    = "MokoStandards Team"
      documentation = "docs/infrastructure/windows-prod-webserver.md"
    }

    # Server identification
    server = {
      role        = "web-server"
      environment = "production"
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
        "Web-Http-Tracing",
        "Web-Performance",
        "Web-Stat-Compression",
        "Web-Dyn-Compression",
        "Web-Security",
        "Web-Filtering",
        "Web-Basic-Auth",
        "Web-Windows-Auth",
        "Web-IP-Security",
        "Web-Url-Auth",
        "Web-App-Dev",
        "Web-Net-Ext45",
        "Web-Asp-Net45",
        "Web-ISAPI-Ext",
        "Web-ISAPI-Filter",
        "Web-Mgmt-Tools",
        "Web-Mgmt-Console",
        "Web-Scripting-Tools"
      ]

      # Production settings
      production_settings = {
        detailed_errors        = false
        directory_browsing     = false
        custom_errors_mode     = "DetailedLocalOnly"
        debug_mode             = false
        request_tracing        = true # For troubleshooting
        failed_request_tracing = true
        auto_start             = true
        server_header_removal  = true # Security best practice
      }

      # Application pools
      application_pools = {
        default = {
          name                    = "ProductionAppPool"
          runtime_version         = "v4.0"
          pipeline_mode           = "Integrated"
          managed_runtime_version = "v4.0"
          identity_type           = "ApplicationPoolIdentity"

          # Production settings - optimized
          idle_timeout  = "00:05:00" # 5 minutes
          max_processes = 4          # For multi-core systems
          start_mode    = "AlwaysRunning"

          # Resource limits
          cpu_limit            = 90      # Percentage
          memory_limit         = 2097152 # 2GB in KB
          private_memory_limit = 1048576 # 1GB in KB

          # Recycling
          periodic_restart = "29:00:00" # Daily at 5 AM
          recycling = {
            private_memory        = 1800000 # KB - 1.8GB
            regular_time_interval = "29:00:00"
            requests              = 0 # Disabled
            specific_time         = ["05:00:00"]
          }
        }

        php = {
          name            = "PHPAppPool"
          runtime_version = "No Managed Code"
          pipeline_mode   = "Classic"
          identity_type   = "ApplicationPoolIdentity"
          idle_timeout    = "00:05:00"
          max_processes   = 4
          memory_limit    = 2097152
        }
      }

      # Sites configuration
      sites = {
        default = {
          name             = "ProductionSite"
          physical_path    = "C:\\inetpub\\wwwroot"
          application_pool = "ProductionAppPool"

          bindings = [
            {
              protocol    = "http"
              ip_address  = "*"
              port        = 80
              host_header = ""
            },
            {
              protocol    = "https"
              ip_address  = "*"
              port        = 443
              host_header = ""
              ssl_flags   = "Sni"
            }
          ]

          # Production features
          auto_start      = true
          preload_enabled = true # Warm up on start
        }
      }

      # URL Rewrite module
      url_rewrite = {
        install = true
        version = "2.1"

        # Production rules
        rules = {
          force_https      = true # Redirect HTTP to HTTPS
          www_redirect     = true # Standardize on www or non-www
          trailing_slash   = true
          security_headers = true
        }
      }

      # ARR (Application Request Routing) for load balancing
      arr = {
        install      = true
        version      = "3.0"
        enable_proxy = true

        # Load balancing
        server_farms = {
          enabled               = true
          health_check_interval = 30
          health_check_timeout  = 30
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
        max_instances    = 16 # Higher for production
        instance_timeout = 300
        activity_timeout = 300
        request_timeout  = 300
        protocol         = "NamedPipe"
      }

      packages = [
        "php",
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
        "php-apcu"
      ]

      # php.ini settings for production
      ini_settings = {
        display_errors         = "Off"
        display_startup_errors = "Off"
        error_reporting        = "E_ALL & ~E_DEPRECATED & ~E_STRICT"
        log_errors             = "On"
        error_log              = "C:\\logs\\php\\php-error.log"

        max_execution_time  = "60"
        max_input_time      = "60"
        memory_limit        = "256M"
        post_max_size       = "20M"
        upload_max_filesize = "20M"

        # Opcache settings (aggressive for production)
        "opcache.enable"                  = "1"
        "opcache.enable_cli"              = "0"
        "opcache.memory_consumption"      = "256"
        "opcache.interned_strings_buffer" = "16"
        "opcache.max_accelerated_files"   = "10000"
        "opcache.revalidate_freq"         = "60" # Check every 60 seconds
        "opcache.validate_timestamps"     = "1"
        "opcache.fast_shutdown"           = "1"
        "opcache.save_comments"           = "0"

        # APCu settings
        "apc.enabled"    = "1"
        "apc.shm_size"   = "128M"
        "apc.ttl"        = "7200"
        "apc.enable_cli" = "0"

        # Session settings
        "session.save_handler"   = "redis"
        "session.save_path"      = "tcp://localhost:6379"
        "session.gc_maxlifetime" = "3600"

        # Security settings
        "expose_php"        = "Off"
        "allow_url_fopen"   = "On"
        "allow_url_include" = "Off"
        "disable_functions" = "exec,passthru,shell_exec,system,proc_open,popen"
      }

      # Composer (for deployment only)
      composer = {
        install         = true
        global_packages = [] # Minimal in production
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

      # Production settings
      environment_variables = {
        ASPNETCORE_ENVIRONMENT = "Production"
        ASPNETCORE_URLS        = "http://*:5000"
        DOTNET_ENVIRONMENT     = "Production"
      }

      # Kestrel settings for production
      kestrel = {
        listen_any_ip = false # Specific IPs only
        http_port     = 5000
        https_port    = 5001
        limits = {
          max_concurrent_connections          = 1000
          max_concurrent_upgraded_connections = 100
          max_request_body_size               = 30000000 # 30MB
          min_request_body_data_rate          = 240      # bytes/second
        }
      }
    }

    # Database connectivity
    databases = {
      mysql = {
        install_client     = true
        odbc_driver        = true
        default_port       = 3306
        connection_pooling = true
        max_pool_size      = 100
      }

      postgresql = {
        install_client     = true
        odbc_driver        = true
        default_port       = 5432
        connection_pooling = true
        max_pool_size      = 100
      }

      sql_server = {
        install_tools      = true
        default_port       = 1433
        connection_pooling = true
        max_pool_size      = 200
      }

      redis = {
        install          = true
        port             = 6379
        windows_service  = true
        max_memory       = "2GB"
        maxmemory_policy = "allkeys-lru"
      }
    }

    # File system configuration
    filesystem = {
      web_root = "C:\\inetpub\\wwwroot"

      directories = {
        logs = {
          path        = "C:\\logs\\webserver"
          permissions = "Read,Write" # Limited permissions
        }
        uploads = {
          path        = "C:\\inetpub\\wwwroot\\uploads"
          permissions = "Read,Write"
          quota       = "20GB"
        }
        cache = {
          path        = "C:\\inetpub\\wwwroot\\cache"
          permissions = "Read,Write"
          quota       = "5GB"
        }
        temp = {
          path        = "C:\\temp\\webserver"
          permissions = "Read,Write"
        }
      }

      # Storage quotas
      quotas = {
        uploads_max = "20GB"
        logs_max    = "50GB"
        cache_max   = "5GB"
      }
    }

    # SSL/TLS configuration
    ssl = {
      enable_ssl      = true
      require_ssl     = true
      use_self_signed = false
      protocols       = ["TLS 1.2", "TLS 1.3"]

      certificate = {
        provider     = "lets-encrypt" # or "commercial-ca"
        auto_renewal = true
        common_name  = "example.com"
        san          = ["www.example.com"]
        organization = "Moko Consulting"
        valid_days   = 90
      }

      # Cipher suites (modern, secure)
      cipher_suites = [
        "TLS_AES_256_GCM_SHA384",
        "TLS_AES_128_GCM_SHA256",
        "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
        "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256"
      ]

      # HSTS (HTTP Strict Transport Security)
      hsts = {
        enabled            = true
        max_age            = 31536000 # 1 year
        include_subdomains = true
        preload            = true
      }
    }

    # Firewall rules
    firewall = {
      enable_rules = true

      inbound_rules = [
        {
          name     = "HTTP-Prod"
          protocol = "TCP"
          port     = 80
          action   = "Allow"
          source   = "Any" # Or specific IP ranges
        },
        {
          name     = "HTTPS-Prod"
          protocol = "TCP"
          port     = 443
          action   = "Allow"
          source   = "Any"
        }
      ]

      # Block common attack ports
      blocked_ports = [3389, 445, 139, 135, 22]
    }

    # Logging configuration
    logging = {
      enabled = true

      iis_logs = {
        path           = "C:\\inetpub\\logs\\LogFiles"
        format         = "W3C"
        fields         = ["date", "time", "s-ip", "cs-method", "cs-uri-stem", "cs-uri-query", "s-port", "cs-username", "c-ip", "cs(User-Agent)", "cs(Referer)", "sc-status", "sc-substatus", "sc-win32-status", "time-taken"]
        rollover       = "Hourly"
        retention_days = 90
      }

      php_logs = {
        path           = "C:\\logs\\php"
        error_log      = "php-error.log"
        slow_log       = "php-slow.log"
        retention_days = 90
      }

      application_logs = {
        path           = "C:\\logs\\webserver"
        retention_days = 90
      }

      # Centralized logging
      log_aggregation = {
        enabled = true
        method  = "syslog" # or "elk", "splunk"
        server  = "logs.example.com"
        port    = 514
      }

      # Production log level
      log_level = "Warning" # Only warnings and errors
    }

    # Performance monitoring
    monitoring = {
      enable_perfmon      = true
      enable_app_insights = true

      # Application Insights
      app_insights = {
        instrumentation_key      = "" # Set from environment
        sampling_percentage      = 100
        enable_adaptive_sampling = true
      }

      # Windows Performance Counters
      performance_counters = [
        "\\Processor(_Total)\\% Processor Time",
        "\\Memory\\Available MBytes",
        "\\Memory\\Pages/sec",
        "\\PhysicalDisk(_Total)\\Disk Reads/sec",
        "\\PhysicalDisk(_Total)\\Disk Writes/sec",
        "\\Web Service(_Total)\\Current Connections",
        "\\Web Service(_Total)\\Bytes Total/sec",
        "\\ASP.NET\\Requests Current",
        "\\ASP.NET\\Requests Queued",
        "\\ASP.NET Applications(__Total__)\\Requests/Sec"
      ]

      # Health checks
      health_checks = {
        enabled             = true
        endpoint            = "/health"
        interval            = 30 # seconds
        timeout             = 10
        unhealthy_threshold = 3
      }

      # Alerting
      alerts = {
        enabled = true

        thresholds = {
          cpu_percent        = 80
          memory_percent     = 85
          disk_percent       = 90
          response_time_ms   = 2000
          error_rate_percent = 5
        }

        notification_channels = [
          "email",
          "sms",
          "slack"
        ]
      }
    }

    # Security settings (hardened for production)
    security = {
      # Authentication
      authentication = {
        anonymous_enabled    = false
        windows_auth_enabled = true
        basic_auth_enabled   = false
        certificate_auth     = false
      }

      # CORS (restrictive)
      cors = {
        enabled           = true
        allow_origins     = ["https://example.com", "https://www.example.com"]
        allow_methods     = ["GET", "POST", "PUT", "DELETE"]
        allow_headers     = ["Content-Type", "Authorization"]
        allow_credentials = true
        max_age           = 86400
      }

      # Request filtering
      request_filtering = {
        max_content_length    = "20971520" # 20MB
        max_url_length        = "2048"
        max_query_string      = "2048"
        allow_double_escaping = false
        allow_high_bit_chars  = false

        # Deny extensions
        deny_extensions = [".exe", ".bat", ".cmd", ".ps1", ".vbs"]

        # Deny request sequences
        deny_sequences = ["../", "..\\", "<script"]
      }

      # Rate limiting
      rate_limiting = {
        enabled             = true
        requests_per_ip     = 100 # per minute
        concurrent_requests = 10
        throttle_bandwidth  = false
      }

      # IP restrictions
      ip_security = {
        enabled    = false # Enable if needed
        allow_list = []
        deny_list  = []
      }

      # Security headers
      headers = {
        "X-Frame-Options"         = "SAMEORIGIN"
        "X-Content-Type-Options"  = "nosniff"
        "X-XSS-Protection"        = "1; mode=block"
        "Referrer-Policy"         = "strict-origin-when-cross-origin"
        "Content-Security-Policy" = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
        "Permissions-Policy"      = "geolocation=(), microphone=(), camera=()"
      }
    }

    # Backup configuration
    backup = {
      enabled = true

      schedule = {
        frequency       = "daily"
        time            = "02:00"
        full_backup_day = "Sunday"
      }

      retention = {
        keep_daily   = 7
        keep_weekly  = 4
        keep_monthly = 12
      }

      backup_items = [
        "C:\\inetpub\\wwwroot",
        "C:\\logs\\webserver",
        "IIS Configuration"
      ]

      backup_location = "\\\\backup-server\\webserver-backups"
    }

    # Load balancing
    load_balancing = {
      enabled = true
      method  = "least-connections" # or "round-robin", "weighted"

      health_check = {
        enabled  = true
        interval = 30
        timeout  = 10
        path     = "/health"
      }

      session_affinity = {
        enabled     = true
        method      = "cookie"
        cookie_name = "ARRAffinity"
      }
    }

    # Caching
    caching = {
      # Output caching
      output_cache = {
        enabled = true
        profiles = {
          default = {
            duration       = 300 # 5 minutes
            vary_by_param  = "*"
            vary_by_header = "Accept-Encoding"
          }
          static = {
            duration = 86400 # 24 hours
            location = "any"
          }
        }
      }

      # Compression
      compression = {
        static_enabled    = true
        dynamic_enabled   = true
        compression_level = 9
        mime_types = [
          "text/plain",
          "text/html",
          "text/css",
          "text/javascript",
          "application/javascript",
          "application/json",
          "application/xml"
        ]
      }
    }

    # Operations
    operations = {
      auto_start_services = true
      restart_on_failure  = true

      maintenance_window = {
        enabled  = true
        day      = "Sunday"
        time     = "02:00"
        duration = "4 hours"
      }

      # Graceful shutdown for zero-downtime deployments
      graceful_shutdown_timeout = 300 # 5 minutes

      # Deployment
      deployment = {
        method              = "blue-green" # or "rolling", "canary"
        verification_tests  = true
        rollback_on_failure = true
      }
    }
  }
}

# Output the configuration
output "windows_prod_webserver_config" {
  description = "Windows production web server configuration"
  value       = local.windows_prod_webserver_config
}

# Output IIS configuration for scripts
output "windows_prod_iis_config" {
  description = "IIS-specific production configuration"
  value = {
    features          = local.windows_prod_webserver_config.iis.features
    application_pools = local.windows_prod_webserver_config.iis.application_pools
    sites             = local.windows_prod_webserver_config.iis.sites
    production_mode   = local.windows_prod_webserver_config.iis.production_settings
    arr_config        = local.windows_prod_webserver_config.iis.arr
  }
}

# Output security configuration
output "windows_prod_security_config" {
  description = "Security configuration for production"
  value = {
    ssl           = local.windows_prod_webserver_config.ssl
    firewall      = local.windows_prod_webserver_config.firewall
    security      = local.windows_prod_webserver_config.security
    rate_limiting = local.windows_prod_webserver_config.security.rate_limiting
  }
}
