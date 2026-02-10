# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# FILE INFORMATION
# DEFGROUP: Terraform.WebServer
# INGROUP: MokoStandards.Infrastructure
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: terraform/webserver/ubuntu-dev-webserver.tf
# VERSION: 03.01.03
# BRIEF: Terraform definition for Ubuntu development web server configuration


locals {
  # Metadata for this configuration
  config_metadata = {
    name            = "Webserver Ubuntu Dev Webserver"
    description     = "Development Ubuntu webserver infrastructure configuration"
    version         = "2.0.0"
    last_updated    = "2026-01-28"
    maintainer      = "MokoStandards Team"
    schema_version  = "2.0"
    repository_url  = "https://github.com/mokoconsulting-tech/MokoStandards"
    repository_type = "standards"
    format          = "terraform"
  }
}

locals {
  ubuntu_dev_webserver_config = {
    metadata = {
      name          = "Ubuntu Development Web Server Configuration"
      version       = "1.0.0"
      description   = "Standardized configuration for Ubuntu development web servers"
      platform      = "linux"
      distribution  = "ubuntu"
      environment   = "development"
      last_updated  = "2026-01-27T00:00:00Z"
      maintainer    = "MokoStandards Team"
      documentation = "docs/infrastructure/ubuntu-dev-webserver.md"
    }

    # Server identification
    server = {
      role        = "web-server"
      environment = "development"
      tier        = "application"
    }

    # System information
    system = {
      os_family          = "debian"
      package_manager    = "apt"
      supported_versions = ["20.04", "22.04", "24.04"]
      architecture       = ["amd64", "arm64"]
    }

    # Apache configuration
    apache = {
      install = true
      version = "2.4"

      packages = [
        "apache2",
        "apache2-utils",
        "libapache2-mod-php8.3"
      ]

      # Development modules
      modules = [
        "rewrite",
        "ssl",
        "headers",
        "proxy",
        "proxy_http",
        "proxy_fcgi",
        "setenvif",
        "php8.3"
      ]

      # Development settings
      dev_settings = {
        server_tokens          = "Full" # Show full version in dev
        server_signature       = "On"
        trace_enable           = "On"
        keepalive              = "On"
        keepalive_timeout      = "5"
        max_keepalive_requests = "100"
        timeout                = "300"
      }

      # Virtual hosts
      vhosts = {
        default = {
          server_name   = "localhost"
          document_root = "/var/www/html"
          port          = 80

          directory_options = {
            options        = ["Indexes", "FollowSymLinks", "MultiViews"]
            allow_override = "All"
            require        = "all granted"
          }

          # Development features
          directory_index = "index.php index.html index.htm"
          error_log       = "/var/log/apache2/dev-error.log"
          custom_log      = "/var/log/apache2/dev-access.log"
          log_level       = "debug"
        }

        dev_ssl = {
          server_name   = "localhost"
          document_root = "/var/www/html"
          port          = 443
          ssl_enabled   = true

          ssl_certificate     = "/etc/ssl/certs/ssl-cert-snakeoil.pem"
          ssl_certificate_key = "/etc/ssl/private/ssl-cert-snakeoil.key"

          directory_options = {
            options        = ["Indexes", "FollowSymLinks", "MultiViews"]
            allow_override = "All"
            require        = "all granted"
          }
        }
      }

      # MPM (Multi-Processing Module)
      mpm = {
        module = "prefork" # For mod_php compatibility

        prefork = {
          start_servers             = 2
          min_spare_servers         = 1
          max_spare_servers         = 3
          max_request_workers       = 150
          max_connections_per_child = 0
        }
      }
    }

    # Nginx configuration (alternative to Apache)
    nginx = {
      install = false # Use Apache by default, set to true for Nginx
      version = "latest"

      packages = [
        "nginx",
        "nginx-common"
      ]

      # Development settings
      dev_settings = {
        worker_processes     = "auto"
        worker_connections   = 768
        keepalive_timeout    = 65
        client_max_body_size = "100M"
        server_tokens        = "on" # Show version in dev
      }

      # Sites
      sites = {
        default = {
          listen      = 80
          server_name = "localhost"
          root        = "/var/www/html"
          index       = "index.php index.html index.htm"

          php_fpm = {
            enabled = true
            socket  = "/run/php/php8.3-fpm.sock"
          }

          error_log  = "/var/log/nginx/dev-error.log"
          access_log = "/var/log/nginx/dev-access.log"
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
        "php8.3-imap",
        "php8.3-redis",
        "php8.3-xdebug"
      ]

      # PHP-FPM configuration
      fpm = {
        enabled = true

        pools = {
          www = {
            listen       = "/run/php/php8.3-fpm.sock"
            listen_owner = "www-data"
            listen_group = "www-data"
            listen_mode  = "0660"

            # Development settings
            pm                      = "dynamic"
            pm_max_children         = 10
            pm_start_servers        = 2
            pm_min_spare_servers    = 1
            pm_max_spare_servers    = 3
            pm_process_idle_timeout = "10s"
            pm_max_requests         = 500

            # Error logging
            catch_workers_output      = "yes"
            php_admin_value_error_log = "/var/log/php8.3-fpm-error.log"
            php_admin_flag_log_errors = "on"
          }
        }
      }

      # php.ini settings for development
      ini_settings = {
        display_errors         = "On"
        display_startup_errors = "On"
        error_reporting        = "E_ALL"
        log_errors             = "On"
        error_log              = "/var/log/php/error.log"

        max_execution_time  = "300"
        max_input_time      = "300"
        memory_limit        = "512M"
        post_max_size       = "100M"
        upload_max_filesize = "100M"

        # Opcache settings (moderate for dev)
        "opcache.enable"                = "1"
        "opcache.enable_cli"            = "1"
        "opcache.memory_consumption"    = "128"
        "opcache.revalidate_freq"       = "2"
        "opcache.validate_timestamps"   = "1"
        "opcache.max_accelerated_files" = "10000"

        # Xdebug settings
        "xdebug.mode"               = "debug,develop,coverage"
        "xdebug.start_with_request" = "trigger"
        "xdebug.client_host"        = "localhost"
        "xdebug.client_port"        = "9003"
        "xdebug.log"                = "/var/log/php/xdebug.log"
        "xdebug.log_level"          = "7"

        # Development features
        "html_errors"    = "On"
        "short_open_tag" = "Off"
        "expose_php"     = "On"
      }

      # Composer
      composer = {
        install = true
        version = "latest"
        global_packages = [
          "phpunit/phpunit",
          "squizlabs/php_codesniffer",
          "phpstan/phpstan",
          "friendsofphp/php-cs-fixer",
          "laravel/installer",
          "symfony/cli"
        ]
      }
    }

    # Node.js configuration
    nodejs = {
      install = true
      version = "20" # LTS

      packages = ["nodejs", "npm"]

      npm_global_packages = [
        "typescript",
        "ts-node",
        "eslint",
        "prettier",
        "nodemon",
        "pm2",
        "webpack",
        "webpack-cli",
        "vite",
        "@vue/cli",
        "create-react-app"
      ]

      # Development server ports
      dev_ports = [3000, 3001, 5173, 8080]
    }

    # Python configuration
    python = {
      install         = true
      versions        = ["3.10", "3.11", "3.12"]
      default_version = "3.11"

      packages = [
        "python3-pip",
        "python3-venv",
        "python3-dev",
        "python3-setuptools",
        "python3-wheel"
      ]

      pip_packages = [
        "flask",
        "django",
        "fastapi",
        "uvicorn",
        "gunicorn",
        "requests",
        "pytest",
        "black",
        "flake8",
        "pylint"
      ]
    }

    # Database services
    databases = {
      mysql = {
        install = true
        version = "8.0"

        dev_settings = {
          bind_address    = "127.0.0.1"
          port            = 3306
          max_connections = 150

          # Development settings
          general_log     = "ON"
          slow_query_log  = "ON"
          long_query_time = 2

          # InnoDB settings
          innodb_buffer_pool_size = "256M"
          innodb_log_file_size    = "48M"
        }

        # Development database
        databases = [{
          name      = "dev_db"
          charset   = "utf8mb4"
          collation = "utf8mb4_unicode_ci"
        }]

        users = [{
          name       = "dev_user"
          password   = "dev_password" # Change in actual deployment
          privileges = "ALL"
        }]
      }

      postgresql = {
        install = false # Enable if needed
        version = "15"

        dev_settings = {
          listen_addresses = "localhost"
          port             = 5432
          max_connections  = 100
        }
      }

      redis = {
        install = true
        version = "latest"

        dev_settings = {
          bind             = "127.0.0.1"
          port             = 6379
          maxmemory        = "512mb"
          maxmemory_policy = "allkeys-lru"
          save             = [] # Disable persistence in dev
        }
      }

      mongodb = {
        install = false # Enable if needed
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
          permissions = "0755"
        }
        uploads = {
          path        = "/var/www/html/uploads"
          owner       = "www-data"
          group       = "www-data"
          permissions = "0777" # Permissive for dev
        }
        cache = {
          path        = "/var/www/html/cache"
          owner       = "www-data"
          group       = "www-data"
          permissions = "0777"
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
      require_ssl     = false
      use_self_signed = true

      certificate = {
        self_signed = true
        common_name = "localhost"
        valid_days  = 365
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
            comment  = "SSH"
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
          },
          {
            port     = 3000
            protocol = "tcp"
            comment  = "Node.js Dev Server"
          },
          {
            port     = 3306
            protocol = "tcp"
            from     = "127.0.0.1"
            comment  = "MySQL (local only)"
          }
        ]
      }
    }

    # Development tools
    dev_tools = {
      install = true

      tools = [
        "git",
        "curl",
        "wget",
        "vim",
        "nano",
        "htop",
        "tree",
        "jq",
        "unzip",
        "zip",
        "tmux",
        "screen",
        "build-essential",
        "net-tools",
        "iputils-ping",
        "telnet",
        "dnsutils"
      ]

      # Database management tools
      db_tools = [
        "mysql-client",
        "postgresql-client",
        "redis-tools",
        "mycli",
        "pgcli"
      ]
    }

    # Git configuration
    git = {
      install = true

      config = {
        core = {
          editor   = "vim"
          autocrlf = "input"
          filemode = true
        }
        init = {
          defaultBranch = "main"
        }
        pull = {
          rebase = false
        }
      }
    }

    # Docker configuration
    docker = {
      install = true

      packages = [
        "docker-ce",
        "docker-ce-cli",
        "containerd.io",
        "docker-buildx-plugin",
        "docker-compose-plugin"
      ]

      # Add web server user to docker group
      add_user_to_group = true

      # Development settings
      dev_settings = {
        log_driver = "json-file"
        log_opts = {
          max_size = "10m"
          max_file = "3"
        }
      }
    }

    # Logging configuration
    logging = {
      enabled = true

      apache_logs = {
        error_log_level   = "debug"
        access_log_format = "combined"
        rotation = {
          rotate    = 14
          frequency = "daily"
          compress  = true
        }
      }

      php_logs = {
        error_log = "/var/log/php/error.log"
        fpm_log   = "/var/log/php8.3-fpm.log"
        slow_log  = "/var/log/php/slow.log"
        rotation = {
          rotate    = 14
          frequency = "daily"
        }
      }

      application_logs = {
        path = "/var/log/webserver"
        rotation = {
          rotate    = 14
          frequency = "daily"
        }
      }
    }

    # Monitoring configuration
    monitoring = {
      # Basic development monitoring
      enable = true

      tools = [
        "htop",
        "iotop",
        "nethogs",
        "sysstat"
      ]

      # Apache status module
      apache_status = {
        enabled    = true
        location   = "/server-status"
        allow_from = ["127.0.0.1", "::1"]
      }

      # PHP-FPM status
      php_fpm_status = {
        enabled  = true
        location = "/php-fpm-status"
      }
    }

    # Security settings (relaxed for development)
    security = {
      # SELinux/AppArmor
      mandatory_access_control = {
        selinux = {
          enabled = false
        }
        apparmor = {
          enabled = true
          mode    = "complain" # Don't enforce in dev
        }
      }

      # Fail2ban
      fail2ban = {
        install = false # Usually not needed in dev
      }

      # ModSecurity (WAF)
      modsecurity = {
        install = false # Usually disabled in dev
      }

      # File permissions
      umask = "0022"
    }

    # Performance tuning (moderate for dev)
    performance = {
      # System limits
      limits = {
        "fs.file-max"                  = "65536"
        "fs.inotify.max_user_watches"  = "524288"
        "net.core.somaxconn"           = "1024"
        "net.ipv4.tcp_max_syn_backlog" = "2048"
      }

      # Swappiness
      vm_swappiness = 10
    }

    # Backup configuration (minimal for dev)
    backup = {
      enabled = false # Usually not needed in dev
    }

    # Operations
    operations = {
      auto_start_services = true

      services = [
        "apache2",
        "php8.3-fpm",
        "mysql",
        "redis-server",
        "docker"
      ]

      # Hot reload for development
      hot_reload = {
        php_fpm = true
        apache  = true
      }
    }
  }
}

# Output the configuration
output "ubuntu_dev_webserver_config" {
  description = "Ubuntu development web server configuration"
  value       = local.ubuntu_dev_webserver_config
}

# Output web server configuration
output "ubuntu_dev_apache_config" {
  description = "Apache-specific development configuration"
  value = {
    packages = local.ubuntu_dev_webserver_config.apache.packages
    modules  = local.ubuntu_dev_webserver_config.apache.modules
    vhosts   = local.ubuntu_dev_webserver_config.apache.vhosts
    mpm      = local.ubuntu_dev_webserver_config.apache.mpm
  }
}

# Output PHP configuration
output "ubuntu_dev_php_config" {
  description = "PHP configuration for Ubuntu dev server"
  value = {
    version      = local.ubuntu_dev_webserver_config.php.version
    packages     = local.ubuntu_dev_webserver_config.php.packages
    ini_settings = local.ubuntu_dev_webserver_config.php.ini_settings
    fpm          = local.ubuntu_dev_webserver_config.php.fpm
  }
}

# Output database configuration
output "ubuntu_dev_database_config" {
  description = "Database configuration for development"
  value = {
    mysql      = local.ubuntu_dev_webserver_config.databases.mysql
    redis      = local.ubuntu_dev_webserver_config.databases.redis
    postgresql = local.ubuntu_dev_webserver_config.databases.postgresql
  }
}
