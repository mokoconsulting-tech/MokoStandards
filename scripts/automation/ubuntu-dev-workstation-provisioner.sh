#!/bin/bash
# =========================================================
# Ubuntu Dev Workstation Provisioner
# =========================================================
#
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This script provisions a standardized Ubuntu development workstation
# based on Terraform configuration at terraform/workstation/ubuntu-dev-workstation.tf

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TERRAFORM_DIR="$REPO_ROOT/terraform/workstation"
LOG_FILE="/tmp/ubuntu-dev-provisioner-$(date +%Y%m%d-%H%M%S).log"
VERBOSE=false

# Functions
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    echo "[$timestamp] [$level] $message" | tee -a "$LOG_FILE"
    
    case "$level" in
        INFO)
            echo -e "${BLUE}[INFO]${NC} $message"
            ;;
        SUCCESS)
            echo -e "${GREEN}[SUCCESS]${NC} $message"
            ;;
        WARN)
            echo -e "${YELLOW}[WARN]${NC} $message"
            ;;
        ERROR)
            echo -e "${RED}[ERROR]${NC} $message"
            ;;
    esac
}

check_root() {
    if [[ $EUID -eq 0 ]]; then
        log ERROR "This script should NOT be run as root (sudo will be used when needed)"
        exit 1
    fi
}

check_ubuntu() {
    if [[ ! -f /etc/os-release ]]; then
        log ERROR "Cannot detect OS. /etc/os-release not found."
        exit 1
    fi
    
    source /etc/os-release
    if [[ "$ID" != "ubuntu" ]]; then
        log ERROR "This script is designed for Ubuntu only. Detected: $ID"
        exit 1
    fi
    
    log INFO "Detected Ubuntu $VERSION_ID"
    
    # Check supported versions (20.04, 22.04, 24.04)
    if [[ ! "$VERSION_ID" =~ ^(20|22|24)\.04$ ]]; then
        log WARN "This Ubuntu version ($VERSION_ID) may not be fully supported"
        read -p "Continue anyway? [y/N] " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

check_internet() {
    log INFO "Checking internet connectivity..."
    if ! ping -c 1 -W 2 8.8.8.8 &>/dev/null; then
        log ERROR "No internet connectivity. Please check your network connection."
        exit 1
    fi
    log SUCCESS "Internet connectivity confirmed"
}

prompt_workspace() {
    local default_workspace="$HOME/Workspace"
    echo
    echo -e "${BLUE}Workspace Configuration${NC}"
    echo "========================================"
    read -p "Enter workspace directory [$default_workspace]: " workspace
    workspace="${workspace:-$default_workspace}"
    
    if [[ -d "$workspace" ]]; then
        log WARN "Directory $workspace already exists"
    else
        log INFO "Will create workspace at: $workspace"
    fi
    
    export WORKSPACE_DIR="$workspace"
}

prompt_git_config() {
    echo
    echo -e "${BLUE}Git Configuration${NC}"
    echo "========================================"
    read -p "Enter your Git user name: " git_name
    read -p "Enter your Git email: " git_email
    
    export GIT_USER_NAME="$git_name"
    export GIT_USER_EMAIL="$git_email"
}

prompt_ssh_key() {
    echo
    echo -e "${BLUE}SSH Key Configuration${NC}"
    echo "========================================"
    
    if [[ -f "$HOME/.ssh/id_ed25519" ]]; then
        log WARN "SSH key already exists at $HOME/.ssh/id_ed25519"
        read -p "Generate new SSH key? [y/N] " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            export GENERATE_SSH_KEY=false
            return
        fi
    fi
    
    export GENERATE_SSH_KEY=true
    read -p "Enter email for SSH key comment [$GIT_USER_EMAIL]: " ssh_email
    export SSH_KEY_EMAIL="${ssh_email:-$GIT_USER_EMAIL}"
}

prompt_optional_components() {
    echo
    echo -e "${BLUE}Optional Components${NC}"
    echo "========================================"
    
    read -p "Install Docker? [Y/n] " -n 1 -r
    echo
    export INSTALL_DOCKER=${REPLY:-Y}
    
    read -p "Install Node.js (LTS)? [Y/n] " -n 1 -r
    echo
    export INSTALL_NODEJS=${REPLY:-Y}
    
    read -p "Install database clients (MySQL, PostgreSQL, Redis)? [Y/n] " -n 1 -r
    echo
    export INSTALL_DB_CLIENTS=${REPLY:-Y}
    
    read -p "Configure UFW firewall? [Y/n] " -n 1 -r
    echo
    export CONFIGURE_UFW=${REPLY:-Y}
}

update_system() {
    log INFO "Updating package lists..."
    sudo apt update | tee -a "$LOG_FILE"
    log SUCCESS "Package lists updated"
}

install_essential_packages() {
    log INFO "Installing essential packages..."
    
    local packages=(
        build-essential
        git
        curl
        wget
        vim
        nano
        tmux
        htop
        tree
        jq
        unzip
        zip
        ca-certificates
        gnupg
        lsb-release
        software-properties-common
    )
    
    sudo apt install -y "${packages[@]}" | tee -a "$LOG_FILE"
    log SUCCESS "Essential packages installed"
}

install_php() {
    log INFO "Installing PHP 8.3..."
    
    # Add Ondrej PHP PPA
    if ! grep -q "^deb .*ondrej/php" /etc/apt/sources.list /etc/apt/sources.list.d/* 2>/dev/null; then
        log INFO "Adding Ondrej PHP PPA..."
        sudo add-apt-repository -y ppa:ondrej/php | tee -a "$LOG_FILE"
        sudo apt update | tee -a "$LOG_FILE"
    fi
    
    local php_packages=(
        php8.3-cli
        php8.3-common
        php8.3-opcache
        php8.3-mysql
        php8.3-curl
        php8.3-mbstring
        php8.3-intl
        php8.3-gd
        php8.3-zip
        php8.3-soap
        php8.3-xml
        php8.3-bcmath
        php8.3-imagick
        php8.3-apcu
        php8.3-imap
        php8.3-xdebug
    )
    
    sudo apt install -y "${php_packages[@]}" | tee -a "$LOG_FILE"
    
    # Enable PHP modules
    sudo phpenmod -v 8.3 -s cli \
        curl mbstring intl gd zip soap xml bcmath imagick \
        opcache mysqli pdo_mysql apcu imap xdebug | tee -a "$LOG_FILE"
    
    php -v | tee -a "$LOG_FILE"
    log SUCCESS "PHP 8.3 installed and configured"
}

install_composer() {
    log INFO "Installing Composer..."
    
    if command -v composer &>/dev/null; then
        log INFO "Composer already installed"
        composer --version | tee -a "$LOG_FILE"
        return
    fi
    
    cd /tmp
    curl -sS https://getcomposer.org/installer -o composer-setup.php
    sudo php composer-setup.php --install-dir=/usr/local/bin --filename=composer
    rm composer-setup.php
    
    composer --version | tee -a "$LOG_FILE"
    log SUCCESS "Composer installed"
}

install_python() {
    log INFO "Installing Python tools..."
    
    sudo apt install -y python3-pip python3-venv python3-dev | tee -a "$LOG_FILE"
    
    # Install Python development tools
    pip3 install --user --upgrade \
        virtualenv \
        pipenv \
        black \
        flake8 \
        pylint \
        mypy \
        pytest | tee -a "$LOG_FILE"
    
    # Add pip user bin to PATH if not already there
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    fi
    
    python3 --version | tee -a "$LOG_FILE"
    log SUCCESS "Python tools installed"
}

install_nodejs() {
    if [[ ! $INSTALL_NODEJS =~ ^[Yy]$ ]]; then
        log INFO "Skipping Node.js installation"
        return
    fi
    
    log INFO "Installing Node.js 20 LTS..."
    
    if command -v node &>/dev/null; then
        local node_version=$(node --version)
        log INFO "Node.js already installed: $node_version"
        read -p "Reinstall Node.js? [y/N] " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            return
        fi
    fi
    
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - | tee -a "$LOG_FILE"
    sudo apt install -y nodejs | tee -a "$LOG_FILE"
    
    # Install global packages
    sudo npm install -g typescript eslint prettier nodemon pm2 | tee -a "$LOG_FILE"
    
    node --version | tee -a "$LOG_FILE"
    npm --version | tee -a "$LOG_FILE"
    log SUCCESS "Node.js installed"
}

install_docker() {
    if [[ ! $INSTALL_DOCKER =~ ^[Yy]$ ]]; then
        log INFO "Skipping Docker installation"
        return
    fi
    
    log INFO "Installing Docker..."
    
    if command -v docker &>/dev/null; then
        log INFO "Docker already installed"
        docker --version | tee -a "$LOG_FILE"
        read -p "Reinstall Docker? [y/N] " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            return
        fi
    fi
    
    # Add Docker GPG key
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
        sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    
    # Add Docker repository
    echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
        https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) stable" | \
        sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    sudo apt update | tee -a "$LOG_FILE"
    sudo apt install -y \
        docker-ce \
        docker-ce-cli \
        containerd.io \
        docker-buildx-plugin \
        docker-compose-plugin | tee -a "$LOG_FILE"
    
    # Add user to docker group
    sudo usermod -aG docker "$USER"
    
    docker --version | tee -a "$LOG_FILE"
    log SUCCESS "Docker installed (group changes require logout/login)"
}

install_database_clients() {
    if [[ ! $INSTALL_DB_CLIENTS =~ ^[Yy]$ ]]; then
        log INFO "Skipping database client installation"
        return
    fi
    
    log INFO "Installing database clients..."
    
    sudo apt install -y \
        mysql-client \
        postgresql-client \
        redis-tools | tee -a "$LOG_FILE"
    
    log SUCCESS "Database clients installed"
}

configure_git() {
    log INFO "Configuring Git..."
    
    git config --global user.name "$GIT_USER_NAME"
    git config --global user.email "$GIT_USER_EMAIL"
    git config --global init.defaultBranch main
    git config --global pull.rebase false
    git config --global core.editor vim
    git config --global core.autocrlf input
    
    log SUCCESS "Git configured"
    git config --global --list | grep -E "^(user|init|pull|core)" | tee -a "$LOG_FILE"
}

generate_ssh_key() {
    if [[ "$GENERATE_SSH_KEY" != "true" ]]; then
        log INFO "Skipping SSH key generation"
        return
    fi
    
    log INFO "Generating SSH key..."
    
    mkdir -p "$HOME/.ssh"
    chmod 700 "$HOME/.ssh"
    
    ssh-keygen -t ed25519 -C "$SSH_KEY_EMAIL" -f "$HOME/.ssh/id_ed25519" -N "" | tee -a "$LOG_FILE"
    
    log SUCCESS "SSH key generated at $HOME/.ssh/id_ed25519"
    echo
    echo -e "${GREEN}Your public key:${NC}"
    cat "$HOME/.ssh/id_ed25519.pub"
    echo
}

create_workspace() {
    log INFO "Creating workspace directory..."
    
    mkdir -p "$WORKSPACE_DIR"/{scripts,logs,projects,tools}
    
    log SUCCESS "Workspace created at $WORKSPACE_DIR"
    tree -L 2 "$WORKSPACE_DIR" | tee -a "$LOG_FILE" || ls -la "$WORKSPACE_DIR"
}

configure_ufw() {
    if [[ ! $CONFIGURE_UFW =~ ^[Yy]$ ]]; then
        log INFO "Skipping UFW configuration"
        return
    fi
    
    log INFO "Configuring UFW firewall..."
    
    sudo apt install -y ufw | tee -a "$LOG_FILE"
    
    # Set default policies
    sudo ufw default deny incoming | tee -a "$LOG_FILE"
    sudo ufw default allow outgoing | tee -a "$LOG_FILE"
    
    # Allow SSH
    sudo ufw allow ssh | tee -a "$LOG_FILE"
    
    # Enable firewall
    echo "y" | sudo ufw enable | tee -a "$LOG_FILE"
    
    sudo ufw status | tee -a "$LOG_FILE"
    log SUCCESS "UFW firewall configured"
}

increase_system_limits() {
    log INFO "Increasing system limits..."
    
    # Increase inotify watches (for file watchers)
    if ! grep -q "fs.inotify.max_user_watches" /etc/sysctl.conf 2>/dev/null; then
        echo "fs.inotify.max_user_watches=524288" | sudo tee -a /etc/sysctl.conf
    fi
    
    # Increase file descriptor limit
    if ! grep -q "fs.file-max" /etc/sysctl.conf 2>/dev/null; then
        echo "fs.file-max=2097152" | sudo tee -a /etc/sysctl.conf
    fi
    
    sudo sysctl -p | tee -a "$LOG_FILE"
    log SUCCESS "System limits increased"
}

create_summary_script() {
    log INFO "Creating environment summary script..."
    
    cat > "$WORKSPACE_DIR/scripts/show-dev-env.sh" << 'EOF'
#!/bin/bash
echo "=== Development Environment Summary ==="
echo
echo "System:"
lsb_release -d
uname -r
echo
echo "PHP:"
php -v | head -n 1
echo
echo "Python:"
python3 --version
echo
echo "Node.js:"
node --version 2>/dev/null || echo "Not installed"
echo
echo "Docker:"
docker --version 2>/dev/null || echo "Not installed"
echo
echo "Git:"
git --version
git config --global user.name
git config --global user.email
echo
echo "Workspace: $HOME/Workspace"
EOF
    
    chmod +x "$WORKSPACE_DIR/scripts/show-dev-env.sh"
    log SUCCESS "Summary script created at $WORKSPACE_DIR/scripts/show-dev-env.sh"
}

print_summary() {
    echo
    echo "========================================"
    echo -e "${GREEN}Ubuntu Dev Workstation Provisioning Complete!${NC}"
    echo "========================================"
    echo
    echo "Summary:"
    echo "  ✓ Essential packages installed"
    echo "  ✓ PHP 8.3 with extensions"
    echo "  ✓ Composer"
    echo "  ✓ Python 3 with tools"
    [[ $INSTALL_NODEJS =~ ^[Yy]$ ]] && echo "  ✓ Node.js 20 LTS"
    [[ $INSTALL_DOCKER =~ ^[Yy]$ ]] && echo "  ✓ Docker"
    [[ $INSTALL_DB_CLIENTS =~ ^[Yy]$ ]] && echo "  ✓ Database clients"
    echo "  ✓ Git configured"
    [[ "$GENERATE_SSH_KEY" == "true" ]] && echo "  ✓ SSH key generated"
    echo "  ✓ Workspace: $WORKSPACE_DIR"
    [[ $CONFIGURE_UFW =~ ^[Yy]$ ]] && echo "  ✓ UFW firewall"
    echo
    echo "Next steps:"
    echo "  1. Log out and log back in (for Docker group changes)"
    echo "  2. Add your SSH key to GitHub/GitLab"
    echo "  3. Run: $WORKSPACE_DIR/scripts/show-dev-env.sh"
    echo
    echo "Log file: $LOG_FILE"
    echo
}

# Main execution
main() {
    echo "========================================"
    echo "Ubuntu Dev Workstation Provisioner"
    echo "========================================"
    echo
    
    check_root
    check_ubuntu
    check_internet
    
    prompt_workspace
    prompt_git_config
    prompt_ssh_key
    prompt_optional_components
    
    echo
    read -p "Ready to provision? [Y/n] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]?$ ]]; then
        log INFO "Provisioning cancelled"
        exit 0
    fi
    
    log INFO "Starting provisioning..."
    
    update_system
    install_essential_packages
    install_php
    install_composer
    install_python
    install_nodejs
    install_docker
    install_database_clients
    configure_git
    generate_ssh_key
    create_workspace
    configure_ufw
    increase_system_limits
    create_summary_script
    
    print_summary
}

# Run main function
main "$@"
