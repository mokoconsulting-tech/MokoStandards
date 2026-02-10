# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# FILE INFORMATION
# DEFGROUP: Terraform.DevWorkstation
# INGROUP: MokoStandards.Infrastructure
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: terraform/workstation/ubuntu-dev-workstation.tf
# VERSION: 03.01.03
# BRIEF: Terraform definition for Ubuntu development workstation provisioning configuration


locals {
  # Metadata for this configuration
  config_metadata = {
    name            = "Workstation Ubuntu Dev Workstation"
    description     = "Development Ubuntu workstation configuration"
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
  ubuntu_dev_workstation_config = {
    metadata = {
      name            = "Ubuntu Developer Workstation Configuration"
      version         = "1.0.0"
      description     = "Standardized configuration for Ubuntu development workstations"
      platform        = "linux"
      distribution    = "ubuntu"
      last_updated    = "2026-01-27T00:00:00Z"
      maintainer      = "MokoStandards Team"
      documentation   = "docs/scripts/automation/ubuntu-dev-workstation.md"
    }

    # System information
    system = {
      os_family          = "debian"
      package_manager    = "apt"
      supported_versions = ["20.04", "22.04", "24.04"]
      architecture       = ["amd64", "arm64"]
    }

    # Workspace configuration
    workspace = {
      default_path      = "$HOME/Workspace"
      create_if_missing = true
      permissions       = "0755"
      artifacts = [
        "scripts",
        "logs",
        "projects",
        "tools"
      ]
    }

    # APT package configuration
    apt = {
      update_on_provision = true
      upgrade_on_provision = false
      
      # Essential development tools
      essential_packages = [
        "build-essential",
        "git",
        "curl",
        "wget",
        "vim",
        "nano",
        "tmux",
        "htop",
        "tree",
        "jq",
        "unzip",
        "zip",
        "ca-certificates",
        "gnupg",
        "lsb-release"
      ]

      # Development tools
      dev_tools = [
        "gcc",
        "g++",
        "make",
        "cmake",
        "gdb",
        "valgrind",
        "strace"
      ]
    }

    # PHP configuration
    php = {
      version = "8.3"
      
      packages = [
        "php8.3-cli",
        "php8.3-common",
        "php8.3-opcache",
        "php8.3-mysql",
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
        "php8.3-xdebug"
      ]

      enabled_modules = [
        "curl",
        "mbstring",
        "intl",
        "gd",
        "zip",
        "soap",
        "xml",
        "bcmath",
        "imagick",
        "opcache",
        "mysqli",
        "pdo_mysql",
        "apcu",
        "imap",
        "xdebug"
      ]

      composer = {
        install         = true
        global_packages = [
          "phpunit/phpunit",
          "squizlabs/php_codesniffer",
          "phpstan/phpstan"
        ]
      }
    }

    # Python configuration
    python = {
      versions = ["3.10", "3.11", "3.12"]
      default_version = "3.11"
      
      packages = [
        "python3-pip",
        "python3-venv",
        "python3-dev"
      ]

      pip_packages = [
        "virtualenv",
        "pipenv",
        "black",
        "flake8",
        "pylint",
        "mypy",
        "pytest"
      ]
    }

    # Node.js configuration
    nodejs = {
      install = true
      version = "20"  # LTS version
      
      npm_global_packages = [
        "typescript",
        "eslint",
        "prettier",
        "nodemon",
        "pm2"
      ]
    }

    # Docker configuration
    docker = {
      install         = true
      add_user_to_group = true
      
      components = [
        "docker-ce",
        "docker-ce-cli",
        "containerd.io",
        "docker-buildx-plugin",
        "docker-compose-plugin"
      ]
    }

    # Git configuration
    git = {
      configure_global = true
      
      default_config = {
        user_email = ""  # Set during provisioning
        user_name  = ""  # Set during provisioning
        
        core = {
          editor     = "vim"
          autocrlf   = "input"
          filemode   = true
        }
        
        pull = {
          rebase = false
        }
        
        init = {
          defaultBranch = "main"
        }
      }
    }

    # SSH configuration
    ssh = {
      generate_key    = true
      key_type        = "ed25519"
      key_comment     = ""  # Set during provisioning
      key_location    = "$HOME/.ssh/id_ed25519"
    }

    # Database tools
    databases = {
      mysql_client = {
        install = true
        packages = ["mysql-client"]
      }
      
      postgresql_client = {
        install = true
        packages = ["postgresql-client"]
      }
      
      redis_cli = {
        install = true
        packages = ["redis-tools"]
      }
    }

    # Shell configuration
    shell = {
      default_shell = "bash"
      
      bash_enhancements = {
        install_bash_completion = true
        custom_bashrc_additions = true
      }

      zsh = {
        install     = false
        oh_my_zsh   = false
      }
    }

    # System tweaks
    system_tweaks = {
      increase_inotify_watches = true
      increase_file_descriptors = true
      
      sysctl_params = {
        "fs.inotify.max_user_watches" = 524288
        "fs.file-max" = 2097152
      }
    }

    # Security configuration
    security = {
      ufw_firewall = {
        install = true
        default_policy = "deny"
        allow_ssh = true
        allow_http = false
        allow_https = false
      }

      fail2ban = {
        install = false
        protect_ssh = true
      }
    }

    # Development server configuration
    dev_servers = {
      nginx = {
        install = false
        enable_on_boot = false
      }
      
      apache = {
        install = false
        enable_on_boot = false
      }
    }

    # Provisioning script
    provisioning_script = <<-BASH
      #!/bin/bash
      set -euo pipefail
      
      echo "=== Ubuntu Developer Workstation Provisioning ==="
      
      # Update package list
      sudo apt update
      
      # Install essential packages
      sudo apt install -y \
        build-essential git curl wget vim nano tmux htop tree jq \
        unzip zip ca-certificates gnupg lsb-release
      
      # Install PHP 8.3
      sudo apt install -y software-properties-common
      sudo add-apt-repository -y ppa:ondrej/php
      sudo apt update
      sudo apt install -y \
        php8.3-cli php8.3-common php8.3-opcache php8.3-mysql \
        php8.3-curl php8.3-mbstring php8.3-intl php8.3-gd php8.3-zip \
        php8.3-soap php8.3-xml php8.3-bcmath php8.3-imagick \
        php8.3-apcu php8.3-imap php8.3-xdebug
      
      # Install Composer
      curl -sS https://getcomposer.org/installer | php
      sudo mv composer.phar /usr/local/bin/composer
      
      # Install Python tools
      sudo apt install -y python3-pip python3-venv python3-dev
      pip3 install --user virtualenv pipenv black flake8 pylint
      
      # Install Node.js 20 LTS
      curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
      sudo apt install -y nodejs
      
      # Install Docker
      curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
      echo "deb [arch=\$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
      sudo apt update
      sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
      sudo usermod -aG docker \$USER
      
      # Configure Git
      git config --global init.defaultBranch main
      git config --global pull.rebase false
      
      # Create workspace directory
      mkdir -p \$HOME/Workspace/{scripts,logs,projects,tools}
      
      echo "=== Provisioning Complete ==="
      echo "Please log out and log back in for group changes to take effect"
    BASH
  }
}

# Output the configuration
output "ubuntu_dev_workstation_config" {
  description = "Ubuntu developer workstation configuration"
  value       = local.ubuntu_dev_workstation_config
}

# Output provisioning script
output "ubuntu_provisioning_script" {
  description = "Bash provisioning script for Ubuntu workstation"
  value       = local.ubuntu_dev_workstation_config.provisioning_script
}

# Output package lists
output "ubuntu_package_lists" {
  description = "Package lists for Ubuntu provisioning"
  value = {
    essential = local.ubuntu_dev_workstation_config.apt.essential_packages
    dev_tools = local.ubuntu_dev_workstation_config.apt.dev_tools
    php       = local.ubuntu_dev_workstation_config.php.packages
    python    = local.ubuntu_dev_workstation_config.python.packages
    nodejs    = local.ubuntu_dev_workstation_config.nodejs.npm_global_packages
    docker    = local.ubuntu_dev_workstation_config.docker.components
  }
}
