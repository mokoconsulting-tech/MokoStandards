#!/usr/bin/env python3
"""
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

FILE INFORMATION
DEFGROUP: MokoStandards.Automation
INGROUP: MokoStandards.Scripts
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /scripts/automation/install_terraform.py
VERSION: 03.02.00
BRIEF: Install Terraform CLI tool for infrastructure as code (Python version)
"""

import argparse
import hashlib
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path
from typing import Optional, Tuple

# Default configuration
DEFAULT_TERRAFORM_VERSION = "1.7.4"
DEFAULT_INSTALL_DIR = "/usr/local/bin"


class TerraformInstaller:
    """Terraform installation manager."""
    
    def __init__(self, version: str = DEFAULT_TERRAFORM_VERSION, 
                 install_dir: str = DEFAULT_INSTALL_DIR, verbose: bool = False):
        self.version = version
        self.install_dir = Path(install_dir)
        self.verbose = verbose
        self.temp_dir = None
        
    def log_info(self, message: str):
        """Log info message."""
        print(f"[INFO] {message}")
        
    def log_warn(self, message: str):
        """Log warning message."""
        print(f"[WARN] {message}", file=sys.stderr)
        
    def log_error(self, message: str):
        """Log error message."""
        print(f"[ERROR] {message}", file=sys.stderr)
        
    def detect_platform(self) -> str:
        """Detect OS and architecture."""
        system = platform.system().lower()
        machine = platform.machine().lower()
        
        # Map OS
        os_map = {
            'linux': 'linux',
            'darwin': 'darwin',
            'windows': 'windows'
        }
        
        # Map architecture
        arch_map = {
            'x86_64': 'amd64',
            'amd64': 'amd64',
            'arm64': 'arm64',
            'aarch64': 'arm64',
            'armv7l': 'arm'
        }
        
        os_name = os_map.get(system)
        arch_name = arch_map.get(machine)
        
        if not os_name or not arch_name:
            raise ValueError(f"Unsupported platform: {system}/{machine}")
            
        return f"{os_name}_{arch_name}"
        
    def check_existing_installation(self) -> bool:
        """Check if Terraform is already installed."""
        terraform_path = shutil.which("terraform")
        
        if not terraform_path:
            return False
            
        try:
            result = subprocess.run(
                ["terraform", "version", "-json"],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Extract version from JSON output
            import json
            version_data = json.loads(result.stdout)
            current_version = version_data.get('terraform_version', 'unknown')
            
            self.log_info(f"Terraform is already installed: version {current_version}")
            
            if current_version == self.version:
                self.log_info(f"Desired version ({self.version}) is already installed")
                return True
            else:
                self.log_warn(f"Current version ({current_version}) differs from desired ({self.version})")
                response = input("Do you want to upgrade/downgrade? (y/N): ")
                if response.lower() != 'y':
                    self.log_info("Keeping existing installation")
                    return True
                    
        except (subprocess.CalledProcessError, json.JSONDecodeError, FileNotFoundError):
            self.log_warn("Could not determine current Terraform version")
            
        return False
        
    def download_terraform(self, url: str, destination: Path) -> bool:
        """Download Terraform from URL."""
        self.log_info(f"Downloading Terraform {self.version}...")
        self.log_info(f"URL: {url}")
        
        try:
            with urllib.request.urlopen(url) as response:
                total_size = int(response.headers.get('content-length', 0))
                
                with open(destination, 'wb') as f:
                    downloaded = 0
                    chunk_size = 8192
                    
                    while True:
                        chunk = response.read(chunk_size)
                        if not chunk:
                            break
                            
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if self.verbose and total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"\rProgress: {percent:.1f}%", end='', flush=True)
                            
                if self.verbose:
                    print()  # New line after progress
                    
            return True
            
        except Exception as e:
            self.log_error(f"Failed to download: {e}")
            return False
            
    def install_terraform(self) -> bool:
        """Download and install Terraform."""
        platform_str = self.detect_platform()
        url = f"https://releases.hashicorp.com/terraform/{self.version}/terraform_{self.version}_{platform_str}.zip"
        
        # Create temp directory
        self.temp_dir = Path(tempfile.mkdtemp())
        zip_file = self.temp_dir / "terraform.zip"
        
        # Download
        if not self.download_terraform(url, zip_file):
            return False
            
        # Extract
        self.log_info("Extracting Terraform...")
        try:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(self.temp_dir)
        except Exception as e:
            self.log_error(f"Failed to extract: {e}")
            return False
            
        # Install binary
        terraform_binary = self.temp_dir / "terraform"
        if platform.system() == "Windows":
            terraform_binary = self.temp_dir / "terraform.exe"
            
        target_path = self.install_dir / terraform_binary.name
        
        self.log_info(f"Installing Terraform to {target_path}...")
        
        try:
            # Check if we need sudo
            if not os.access(self.install_dir, os.W_OK):
                self.log_info(f"Requires sudo to install to {self.install_dir}")
                subprocess.run(
                    ["sudo", "mv", str(terraform_binary), str(target_path)],
                    check=True
                )
                subprocess.run(
                    ["sudo", "chmod", "+x", str(target_path)],
                    check=True
                )
            else:
                shutil.move(str(terraform_binary), str(target_path))
                os.chmod(target_path, 0o755)
                
            self.log_info(f"Terraform {self.version} installed successfully!")
            return True
            
        except Exception as e:
            self.log_error(f"Failed to install: {e}")
            return False
            
    def verify_installation(self) -> bool:
        """Verify Terraform installation."""
        self.log_info("Verifying installation...")
        
        if not shutil.which("terraform"):
            self.log_error("Terraform command not found after installation")
            return False
            
        try:
            result = subprocess.run(
                ["terraform", "version", "-json"],
                capture_output=True,
                text=True,
                check=True
            )
            
            import json
            version_data = json.loads(result.stdout)
            installed_version = version_data.get('terraform_version', 'unknown')
            
            self.log_info(f"Terraform version: {installed_version}")
            
            if installed_version != self.version:
                self.log_warn(f"Installed version ({installed_version}) differs from expected ({self.version})")
            else:
                self.log_info("✓ Installation verified successfully")
                
            return True
            
        except Exception as e:
            self.log_error(f"Verification failed: {e}")
            return False
            
    def cleanup(self):
        """Clean up temporary files."""
        if self.temp_dir and self.temp_dir.exists():
            self.log_info("Cleaning up temporary files...")
            shutil.rmtree(self.temp_dir)
            
    def run(self) -> bool:
        """Run the installation process."""
        self.log_info("=== Terraform Installation Script ===")
        self.log_info(f"Target version: {self.version}")
        self.log_info(f"Install directory: {self.install_dir}")
        print()
        
        try:
            # Check existing installation
            if self.check_existing_installation():
                self.log_info("Installation check complete")
                return True
                
            # Install Terraform
            if not self.install_terraform():
                return False
                
            # Verify installation
            if not self.verify_installation():
                return False
                
            self.log_info("=== Installation Complete ===")
            self.log_info("Run 'terraform version' to verify")
            return True
            
        finally:
            self.cleanup()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Install Terraform CLI tool",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--version',
        default=DEFAULT_TERRAFORM_VERSION,
        help=f'Terraform version to install (default: {DEFAULT_TERRAFORM_VERSION})'
    )
    
    parser.add_argument(
        '--install-dir',
        default=DEFAULT_INSTALL_DIR,
        help=f'Installation directory (default: {DEFAULT_INSTALL_DIR})'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    installer = TerraformInstaller(
        version=args.version,
        install_dir=args.install_dir,
        verbose=args.verbose
    )
    
    success = installer.run()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
