#!/usr/bin/env bash
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# This file is part of a Moko Consulting project.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# FILE INFORMATION
# DEFGROUP: MokoStandards.Automation
# INGROUP: MokoStandards.Scripts
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: /scripts/automation/install_terraform.sh
# VERSION: 03.02.00
# BRIEF: Install Terraform CLI tool for infrastructure as code

set -euo pipefail

# Default Terraform version
TERRAFORM_VERSION="${TERRAFORM_VERSION:-1.7.4}"
INSTALL_DIR="${INSTALL_DIR:-/usr/local/bin}"
TEMP_DIR=$(mktemp -d)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $*"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $*"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*"
}

# Detect OS and architecture
detect_platform() {
    local os=""
    local arch=""
    
    # Detect OS
    case "$(uname -s)" in
        Linux*)     os="linux";;
        Darwin*)    os="darwin";;
        MINGW*)     os="windows";;
        MSYS*)      os="windows";;
        CYGWIN*)    os="windows";;
        *)          log_error "Unsupported OS: $(uname -s)"; exit 1;;
    esac
    
    # Detect architecture
    case "$(uname -m)" in
        x86_64)     arch="amd64";;
        amd64)      arch="amd64";;
        arm64)      arch="arm64";;
        aarch64)    arch="arm64";;
        armv7l)     arch="arm";;
        *)          log_error "Unsupported architecture: $(uname -m)"; exit 1;;
    esac
    
    echo "${os}_${arch}"
}

# Check if Terraform is already installed
check_existing_installation() {
    if command -v terraform &> /dev/null; then
        local current_version=$(terraform version -json | grep -o '"terraform_version":"[^"]*' | cut -d'"' -f4 || echo "unknown")
        log_info "Terraform is already installed: version ${current_version}"
        
        if [[ "${current_version}" == "${TERRAFORM_VERSION}" ]]; then
            log_info "Desired version (${TERRAFORM_VERSION}) is already installed"
            return 0
        else
            log_warn "Current version (${current_version}) differs from desired version (${TERRAFORM_VERSION})"
            read -p "Do you want to upgrade/downgrade? (y/N): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                log_info "Keeping existing installation"
                return 0
            fi
        fi
    fi
    return 1
}

# Download and install Terraform
install_terraform() {
    local platform=$(detect_platform)
    local download_url="https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_${platform}.zip"
    local zip_file="${TEMP_DIR}/terraform.zip"
    
    log_info "Downloading Terraform ${TERRAFORM_VERSION} for ${platform}..."
    log_info "URL: ${download_url}"
    
    # Download with curl or wget
    if command -v curl &> /dev/null; then
        curl -fsSL "${download_url}" -o "${zip_file}" || {
            log_error "Failed to download Terraform"
            exit 1
        }
    elif command -v wget &> /dev/null; then
        wget -q "${download_url}" -O "${zip_file}" || {
            log_error "Failed to download Terraform"
            exit 1
        }
    else
        log_error "Neither curl nor wget is available"
        exit 1
    fi
    
    log_info "Extracting Terraform..."
    unzip -q "${zip_file}" -d "${TEMP_DIR}" || {
        log_error "Failed to extract Terraform"
        exit 1
    }
    
    # Install Terraform binary
    log_info "Installing Terraform to ${INSTALL_DIR}..."
    
    if [[ -w "${INSTALL_DIR}" ]]; then
        mv "${TEMP_DIR}/terraform" "${INSTALL_DIR}/terraform" || {
            log_error "Failed to move Terraform binary"
            exit 1
        }
    else
        log_info "Requires sudo to install to ${INSTALL_DIR}"
        sudo mv "${TEMP_DIR}/terraform" "${INSTALL_DIR}/terraform" || {
            log_error "Failed to move Terraform binary (sudo)"
            exit 1
        }
    fi
    
    # Make executable
    if [[ -w "${INSTALL_DIR}/terraform" ]]; then
        chmod +x "${INSTALL_DIR}/terraform"
    else
        sudo chmod +x "${INSTALL_DIR}/terraform"
    fi
    
    log_info "Terraform ${TERRAFORM_VERSION} installed successfully!"
}

# Verify installation
verify_installation() {
    log_info "Verifying installation..."
    
    if ! command -v terraform &> /dev/null; then
        log_error "Terraform command not found after installation"
        exit 1
    fi
    
    local installed_version=$(terraform version -json | grep -o '"terraform_version":"[^"]*' | cut -d'"' -f4)
    log_info "Terraform version: ${installed_version}"
    
    if [[ "${installed_version}" != "${TERRAFORM_VERSION}" ]]; then
        log_warn "Installed version (${installed_version}) differs from expected (${TERRAFORM_VERSION})"
    else
        log_info "✓ Installation verified successfully"
    fi
}

# Cleanup
cleanup() {
    log_info "Cleaning up temporary files..."
    rm -rf "${TEMP_DIR}"
}

# Main execution
main() {
    log_info "=== Terraform Installation Script ==="
    log_info "Target version: ${TERRAFORM_VERSION}"
    log_info "Install directory: ${INSTALL_DIR}"
    echo
    
    # Check existing installation
    if check_existing_installation; then
        log_info "Installation check complete"
        exit 0
    fi
    
    # Install Terraform
    install_terraform
    
    # Verify installation
    verify_installation
    
    # Cleanup
    cleanup
    
    log_info "=== Installation Complete ==="
    log_info "Run 'terraform version' to verify"
}

# Trap cleanup on exit
trap cleanup EXIT

# Run main function
main "$@"
