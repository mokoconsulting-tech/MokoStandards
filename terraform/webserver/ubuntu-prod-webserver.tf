# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# FILE INFORMATION
# DEFGROUP: Terraform.WebServer
# INGROUP: MokoStandards.Infrastructure
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: terraform/webserver/ubuntu-prod-webserver.tf
# VERSION: 04.00.01
# BRIEF: Terraform definition for Ubuntu production web server configuration
# ENTERPRISE: Includes audit logging, monitoring, and compliance features


locals {
  # Metadata for this configuration
  # Enterprise-ready: Includes audit logging, monitoring, and compliance features
  config_metadata = {
    name              = "Webserver Ubuntu Prod Webserver"
    description       = "Production Ubuntu webserver infrastructure configuration"
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
  ubuntu_prod_webserver_config = {
    metadata = {
      name          = "Ubuntu Production Web Server Configuration"
      version       = "1.0.0"
      description   = "Standardized configuration for Ubuntu production web servers"
      platform      = "linux"
      distribution  = "ubuntu"
      environment   = "production"
      last_updated  = "2026-01-27T00:00:00Z"
      maintainer    = "MokoStandards Team"
      documentation = "docs/infrastructure/ubuntu-prod-webserver.md"
    }

    # Server identification
    server = {
      role        = "web-server"
      environment = "production"
      tier        = "application"
    }

    # System information
    system = {
      os_family          = "debian"
      package_manager    = "apt"
      supported_versions = ["20.04", "22.04", "24.04"]
      architecture       = ["amd64", "arm64"]
      kernel_tuning      = true
    }

    # Nginx configuration (preferred for production)
    nginx = {
      install = true
      version = "latest"

      packages = [
        "nginx",
        "nginx-common",
        "nginx-extras" # Additional modules
      ]

      # Production settings
      prod_settings = {
        worker_processes      = "auto"
        worker_connections    = 4096
        worker_rlimit_nofile  = 65535
        keepalive_timeout     = 15
        keepalive_requests    = 100
        client_max_body_size  = "20M"
        client_body_timeout   = "12"
        client_header_timeout = "12"
        send_timeout          = "10"
        server_tokens         = "off" # Hide version

        # Gzip compression
        gzip = {
          enabled    = true
          vary       = true
          proxied    = "any"
          comp_level = 6
          types = [
            "text/plain",
            "text/css",
            "text/xml",
            "text/javascript",
            "application/json",
            "application/javascript",
            "application/xml+rss",
            "application/x-javascript"
          ]
        }
      }

      # SSL/TLS settings
      ssl = {
        protocols             = ["TLSv1.2", "TLSv1.3"]
        ciphers               = "ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384"
        prefer_server_ciphers = true
        session_cache         = "shared:SSL:10m"
        session_timeout       = "10m"
        stapling              = true
        stapling_verify       = true
      }

      # Rate limiting
      rate_limiting = {
        enabled   = true
        zone_name = "req_limit_per_ip"
        zone_size = "10m"
        rate      = "10r/s"
        burst     = 20
        nodelay   = true
      }

      # Sites
      sites = {
        production = {
          listen      = [80, 443]
          server_name = "example.com www.example.com"
          root        = "/var/www/html"
          index       = "index.php index.html"

          # SSL certificates
          ssl_certificate     = "/etc/letsencrypt/live/example.com/fullchain.pem"
          ssl_certificate_key = "/etc/letsencrypt/live/example.com/privkey.pem"

          # PHP-FPM
          php_fpm = {
            enabled = true
            socket  = "/run/php/php8.3-fpm.sock"
            timeout = 60
          }

          # Security headers
          headers = {
            "Strict-Transport-Security" = "max-age=31536000; includeSubDomains; preload"
            "X-Frame-Options"           = "SAMEORIGIN"
            "X-Content-Type-Options"    = "nosniff"
            "X-XSS-Protection"          = "1; mode=block"
            "Referrer-Policy"           = "strict-origin-when-cross-origin"
            "Content-Security-Policy"   = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
          }

          # Caching
          cache = {
            static_files = {
              enabled = true
              expires = "30d"
              types   = ["image/jpg", "image/jpeg", "image/png", "image/gif", "image/svg+xml", "image/webp", "text/css", "application/javascript"]
            }
          }

          error_log  = "/var/log/nginx/prod-error.log warn"
          access_log = "/var/log/nginx/prod-access.log"
        }
      }
    }

    # Apache configuration (alternative)
    apache = {
      install = false # Use Nginx by default
      version = "2.4"

      packages = [
        "apache2",
        "apache2-utils",
        "libapache2-mod-php8.3",
        "libapache2-mod-security2"
      ]

      # Production modules
      modules = [
        "rewrite",
        "ssl",
        "headers",
        "expires",
        "deflate",
        "http2",
        "security2",
        "evasive",
        "proxy",
        "proxy_fcgi",
        "php8.3"
      ]

      # Production settings
      prod_settings = {
        server_tokens          = "Prod" # Minimal info
        server_signature       = "Off"
        trace_enable           = "Off"
        keepalive              = "On"
        keepalive_timeout      = "5"
        max_keepalive_requests = "100"
        timeout                = "60"

        # MPM Event (for production)
        mpm = {
          module = "event"

          event = {
            start_servers             = 4
            min_spare_threads         = 75
            max_spare_threads         = 250
            threads_per_child         = 25
            max_request_workers       = 400
            max_connections_per_child = 1000
          }
        }
      }
    }

    # PHP configuration
    php = {
      version = "8.3"
      install = true

      packages = [
        "php8.3-cli",
        "php8.3-fpm",
        "php8.3-common",
        "php8.3-opcache",
        "php8.3-mysql",
        "php8.3-pgsql",
        "php8.3-curl",
        "php8.3-mbstring",
        "php8.3-intl",
        "php8.3-gd",
        "php8.3-zip",
        "php8.3-soap",
        "php8.3-xml",
        "php8.3-bcmath",
        "php8.3-imagick",
        "php8.3-apcu",
        "php8.3-redis"
      ]

      # PHP-FPM configuration for production
      fpm = {
        enabled = true

        pools = {
          www = {
            listen         = "/run/php/php8.3-fpm.sock"
            listen_owner   = "www-data"
            listen_group   = "www-data"
            listen_mode    = "0660"
            listen_backlog = 511

            # Production settings
            pm                      = "dynamic"
            pm_max_children         = 50
            pm_start_servers        = 5
            pm_min_spare_servers    = 5
            pm_max_spare_servers    = 35
            pm_process_idle_timeout = "10s"
            pm_max_requests         = 1000

            # Resource limits
            rlimit_files = 65536
            rlimit_core  = 0

            # Slow log
            slowlog                   = "/var/log/php8.3-fpm-slow.log"
            request_slowlog_timeout   = "5s"
            request_terminate_timeout = "60s"

            # Error logging
            catch_workers_output      = "yes"
            php_admin_value_error_log = "/var/log/php8.3-fpm-error.log"
            php_admin_flag_log_errors = "on"
          }
        }
      }

      # php.ini settings for production
      ini_settings = {
        display_errors         = "Off"
        display_startup_errors = "Off"
        error_reporting        = "E_ALL & ~E_DEPRECATED & ~E_STRICT"
        log_errors             = "On"
        error_log              = "/var/log/php/error.log"

        max_execution_time  = "60"
        max_input_time      = "60"
        memory_limit        = "256M"
        post_max_size       = "20M"
        upload_max_filesize = "20M"
        max_file_uploads    = "20"

        # Opcache settings (aggressive for production)
        "opcache.enable"                  = "1"
        "opcache.enable_cli"              = "0"
        "opcache.memory_consumption"      = "256"
        "opcache.interned_strings_buffer" = "16"
        "opcache.max_accelerated_files"   = "20000"
        "opcache.revalidate_freq"         = "60"
        "opcache.validate_timestamps"     = "1"
        "opcache.fast_shutdown"           = "1"
        "opcache.save_comments"           = "0"
        "opcache.enable_file_override"    = "1"

        # APCu settings
        "apc.enabled"    = "1"
        "apc.shm_size"   = "256M"
        "apc.ttl"        = "7200"
        "apc.enable_cli" = "0"

        # Session settings
        "session.save_handler"    = "redis"
        "session.save_path"       = "tcp://127.0.0.1:6379?weight=1&timeout=2.5"
        "session.gc_maxlifetime"  = "3600"
        "session.cookie_httponly" = "1"
        "session.cookie_secure"   = "1"
        "session.cookie_samesite" = "Lax"

        # Security settings
        "expose_php"        = "Off"
        "allow_url_fopen"   = "On"
        "allow_url_include" = "Off"
        "disable_functions" = "exec,passthru,shell_exec,system,proc_open,popen,curl_exec,curl_multi_exec,parse_ini_file,show_source"
        "open_basedir"      = "/var/www/html:/tmp:/var/lib/php/sessions"
      }

      # Composer (minimal in production)
      composer = {
        install         = true
        global_packages = []
      }
    }

    # Node.js configuration (for build tools)
    nodejs = {
      install = true
      version = "20" # LTS

      packages = ["nodejs", "npm"]

      # Minimal global packages for production
      npm_global_packages = [
        "pm2" # Process manager
      ]
    }

    # Database services
    databases = {
      mysql = {
        install = true
        version = "8.0"

        prod_settings = {
          bind_address    = "0.0.0.0" # Configure firewall separately
          port            = 3306
          max_connections = 500

          # Production settings
          general_log     = "OFF"
          slow_query_log  = "ON"
          long_query_time = 1

          # InnoDB settings (optimized)
          innodb_buffer_pool_size        = "2G"
          innodb_log_file_size           = "256M"
          innodb_flush_log_at_trx_commit = "1"
          innodb_flush_method            = "O_DIRECT"
          innodb_file_per_table          = "ON"

          # Performance
          query_cache_size    = "0" # Deprecated in MySQL 8.0
          table_open_cache    = "4000"
          tmp_table_size      = "64M"
          max_heap_table_size = "64M"
        }

        # Replication
        replication = {
          enabled = false
          role    = "master" # or "slave"
        }
      }

      postgresql = {
        install = false
        version = "15"

        prod_settings = {
          listen_addresses = "0.0.0.0"
          port             = 5432
          max_connections  = 200

          # Performance
          shared_buffers       = "2GB"
          effective_cache_size = "6GB"
          work_mem             = "16MB"
          maintenance_work_mem = "512MB"
        }
      }

      redis = {
        install = true
        version = "latest"

        prod_settings = {
          bind             = "127.0.0.1"
          port             = 6379
          maxmemory        = "2gb"
          maxmemory_policy = "allkeys-lru"

          # Persistence
          save        = ["900 1", "300 10", "60 10000"]
          appendonly  = "yes"
          appendfsync = "everysec"

          # Replication
          replication = {
            enabled = false
            role    = "master" # or "replica"
          }
        }
      }

      mongodb = {
        install = false
        version = "6.0"
      }
    }

    # File system configuration
    filesystem = {
      web_root = "/var/www/html"

      directories = {
        web_root = {
          path        = "/var/www/html"
          owner       = "www-data"
          group       = "www-data"
          permissions = "0755"
        }
        logs = {
          path        = "/var/log/webserver"
          owner       = "www-data"
          group       = "www-data"
          permissions = "0750"
        }
        uploads = {
          path        = "/var/www/html/uploads"
          owner       = "www-data"
          group       = "www-data"
          permissions = "0755"
          quota       = "20GB"
        }
        cache = {
          path        = "/var/www/html/cache"
          owner       = "www-data"
          group       = "www-data"
          permissions = "0755"
          quota       = "5GB"
        }
        sessions = {
          path        = "/var/lib/php/sessions"
          owner       = "www-data"
          group       = "www-data"
          permissions = "0700"
        }
      }
    }

    # SSL/TLS configuration
    ssl = {
      enable_ssl      = true
      require_ssl     = true
      use_self_signed = false

      certificate = {
        provider     = "lets-encrypt"
        auto_renewal = true
        common_name  = "example.com"
        san          = ["www.example.com"]
        email        = "admin@example.com"
        valid_days   = 90
      }

      # Certbot configuration
      certbot = {
        install    = true
        auto_renew = true
        renew_hook = "systemctl reload nginx"
      }
    }

    # Firewall configuration
    firewall = {
      ufw = {
        install        = true
        enabled        = true
        default_policy = "deny"

        allow_rules = [
          {
            port     = 22
            protocol = "tcp"
            from     = "" # Configure specific IPs
            comment  = "SSH - Restrict to admin IPs"
          },
          {
            port     = 80
            protocol = "tcp"
            comment  = "HTTP"
          },
          {
            port     = 443
            protocol = "tcp"
            comment  = "HTTPS"
          }
        ]

        deny_rules = [
          {
            port     = 3306
            protocol = "tcp"
            from     = "any"
            comment  = "MySQL - Deny external"
          },
          {
            port     = 5432
            protocol = "tcp"
            from     = "any"
            comment  = "PostgreSQL - Deny external"
          }
        ]
      }

      # Rate limiting at firewall level
      fail2ban = {
        install = true
        enabled = true

        jails = [
          {
            name     = "nginx-http-auth"
            enabled  = true
            maxretry = 5
            findtime = 600
            bantime  = 3600
          },
          {
            name     = "nginx-limit-req"
            enabled  = true
            maxretry = 10
            findtime = 600
            bantime  = 3600
          },
          {
            name     = "sshd"
            enabled  = true
            maxretry = 3
            findtime = 600
            bantime  = 7200
          }
        ]
      }
    }

    # Monitoring and alerting
    monitoring = {
      enable = true

      # System monitoring
      system_tools = [
        "sysstat",
        "htop",
        "iotop",
        "nethogs"
      ]

      # Application monitoring
      nginx_status = {
        enabled    = true
        location   = "/nginx_status"
        allow_from = ["127.0.0.1"]
      }

      php_fpm_status = {
        enabled    = true
        location   = "/php-fpm-status"
        allow_from = ["127.0.0.1"]
      }

      # Health checks
      health_checks = {
        enabled             = true
        endpoint            = "/health"
        interval            = 30
        timeout             = 10
        unhealthy_threshold = 3
      }

      # Metrics collection
      prometheus = {
        install        = false # Enable if using Prometheus
        node_exporter  = true
        nginx_exporter = true
      }

      # Log monitoring
      log_monitoring = {
        enabled = true
        tool    = "logwatch" # or "logrotate", "elk"

        logwatch = {
          install = true
          email   = "admin@example.com"
          detail  = "high"
        }
      }

      # Alerting
      alerts = {
        enabled = true

        thresholds = {
          cpu_percent      = 85
          memory_percent   = 90
          disk_percent     = 85
          load_average     = 10.0
          response_time_ms = 1000
        }

        notification = {
          email = ["admin@example.com"]
          sms   = []
          slack = ""
        }
      }
    }

    # Logging configuration
    logging = {
      enabled = true

      nginx_logs = {
        access_log_format = "combined"
        error_log_level   = "warn"

        rotation = {
          rotate         = 90
          frequency      = "daily"
          compress       = true
          delay_compress = true
          notifempty     = true
          create         = "0640 www-data adm"
        }
      }

      php_logs = {
        error_log = "/var/log/php/error.log"
        fpm_log   = "/var/log/php8.3-fpm.log"
        slow_log  = "/var/log/php/slow.log"

        rotation = {
          rotate    = 90
          frequency = "daily"
          compress  = true
        }
      }

      application_logs = {
        path = "/var/log/webserver"

        rotation = {
          rotate    = 90
          frequency = "daily"
          compress  = true
        }
      }

      # Centralized logging
      log_aggregation = {
        enabled = false     # Enable for centralized logging
        method  = "rsyslog" # or "filebeat", "fluentd"
        server  = "logs.example.com"
        port    = 514
      }
    }

    # Security hardening
    security = {
      # SELinux/AppArmor
      mandatory_access_control = {
        selinux = {
          enabled = false
        }
        apparmor = {
          enabled = true
          mode    = "enforce"
        }
      }

      # ModSecurity WAF
      modsecurity = {
        install  = true
        enabled  = true
        rule_set = "OWASP-CRS"

        settings = {
          detection_only  = false
          audit_logging   = true
          audit_log_parts = "ABIJDEFHZ"
        }
      }

      # File integrity monitoring
      aide = {
        install         = true
        enabled         = true
        check_frequency = "daily"
      }

      # ClamAV antivirus
      clamav = {
        install        = false # Enable if needed
        scan_frequency = "weekly"
      }

      # Rootkit detection
      rkhunter = {
        install         = true
        check_frequency = "daily"
      }
    }

    # Performance tuning
    performance = {
      # System limits
      limits = {
        "fs.file-max"                   = "2097152"
        "fs.inotify.max_user_watches"   = "524288"
        "net.core.somaxconn"            = "65536"
        "net.core.netdev_max_backlog"   = "5000"
        "net.ipv4.tcp_max_syn_backlog"  = "8192"
        "net.ipv4.tcp_tw_reuse"         = "1"
        "net.ipv4.ip_local_port_range"  = "1024 65000"
        "net.ipv4.tcp_fin_timeout"      = "15"
        "net.ipv4.tcp_keepalive_time"   = "300"
        "net.ipv4.tcp_keepalive_probes" = "5"
        "net.ipv4.tcp_keepalive_intvl"  = "15"
      }

      # Swappiness
      vm_swappiness = 10

      # Transparent huge pages
      transparent_hugepages = "madvise"
    }

    # Backup configuration
    backup = {
      enabled = true

      schedule = {
        full_backup = {
          frequency = "weekly"
          day       = "Sunday"
          time      = "02:00"
        }

        incremental_backup = {
          frequency = "daily"
          time      = "02:00"
        }
      }

      retention = {
        keep_daily   = 7
        keep_weekly  = 4
        keep_monthly = 12
        keep_yearly  = 2
      }

      backup_items = [
        "/var/www/html",
        "/etc/nginx",
        "/etc/php",
        "/var/lib/mysql",
        "/var/log/webserver"
      ]

      backup_location = "/mnt/backup" # or remote location

      backup_method = "rsync" # or "duplicity", "borg", "restic"
    }

    # Load balancing
    load_balancing = {
      enabled = false               # Enable when using multiple servers
      method  = "least-connections" # or "round-robin", "ip-hash"

      health_check = {
        enabled  = true
        interval = 10
        timeout  = 5
        path     = "/health"
      }

      session_persistence = {
        enabled = true
        method  = "ip-hash"
      }
    }

    # CDN configuration
    cdn = {
      enabled  = false # Enable if using CDN
      provider = ""    # cloudflare, cloudfront, etc.

      cache_rules = {
        static_assets = {
          path_pattern = "\\.(jpg|jpeg|png|gif|ico|css|js|woff|woff2|ttf|svg)$"
          cache_ttl    = 2592000 # 30 days
        }
      }
    }

    # Operations
    operations = {
      auto_start_services = true

      services = [
        "nginx",
        "php8.3-fpm",
        "mysql",
        "redis-server"
      ]

      # Deployment
      deployment = {
        method              = "blue-green" # or "rolling", "canary"
        automation          = true
        verification_tests  = true
        rollback_on_failure = true

        zero_downtime             = true
        graceful_shutdown_timeout = 300 # 5 minutes
      }

      # Maintenance window
      maintenance_window = {
        enabled              = true
        day                  = "Sunday"
        time                 = "02:00"
        duration             = "4 hours"
        notification_advance = "24 hours"
      }

      # Auto-scaling
      auto_scaling = {
        enabled       = false # Enable for cloud deployments
        min_instances = 2
        max_instances = 10
        target_cpu    = 70
        target_memory = 80
      }
    }
  }
}

# Output the configuration
output "ubuntu_prod_webserver_config" {
  description = "Ubuntu production web server configuration"
  value       = local.ubuntu_prod_webserver_config
}

# Output web server configuration
output "ubuntu_prod_nginx_config" {
  description = "Nginx-specific production configuration"
  value = {
    packages      = local.ubuntu_prod_webserver_config.nginx.packages
    prod_settings = local.ubuntu_prod_webserver_config.nginx.prod_settings
    ssl           = local.ubuntu_prod_webserver_config.nginx.ssl
    sites         = local.ubuntu_prod_webserver_config.nginx.sites
    rate_limiting = local.ubuntu_prod_webserver_config.nginx.rate_limiting
  }
}

# Output PHP configuration
output "ubuntu_prod_php_config" {
  description = "PHP configuration for Ubuntu prod server"
  value = {
    version      = local.ubuntu_prod_webserver_config.php.version
    packages     = local.ubuntu_prod_webserver_config.php.packages
    ini_settings = local.ubuntu_prod_webserver_config.php.ini_settings
    fpm          = local.ubuntu_prod_webserver_config.php.fpm
  }
}

# Output security configuration
output "ubuntu_prod_security_config" {
  description = "Security configuration for production"
  value = {
    ssl         = local.ubuntu_prod_webserver_config.ssl
    firewall    = local.ubuntu_prod_webserver_config.firewall
    modsecurity = local.ubuntu_prod_webserver_config.security.modsecurity
    hardening   = local.ubuntu_prod_webserver_config.security
  }
}

# Output monitoring configuration
output "ubuntu_prod_monitoring_config" {
  description = "Monitoring and alerting configuration"
  value = {
    health_checks  = local.ubuntu_prod_webserver_config.monitoring.health_checks
    alerts         = local.ubuntu_prod_webserver_config.monitoring.alerts
    log_monitoring = local.ubuntu_prod_webserver_config.monitoring.log_monitoring
  }
}
