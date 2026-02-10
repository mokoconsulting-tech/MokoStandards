#!/usr/bin/env python3
"""
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

FILE INFORMATION
DEFGROUP: MokoStandards.Scripts.Automation
INGROUP: MokoStandards.Scripts
REPO: https://github.com/mokoconsulting-tech/MokoStandards
FILE: scripts/automation/setup_dev_environment.py
VERSION: 03.01.04
BRIEF: Quick setup script for new contributors to set up their development environment
PATH: /scripts/automation/setup_dev_environment.py
"""

import argparse
import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


def run_command(cmd: List[str], check: bool = True) -> Optional[subprocess.CompletedProcess]:
    """
    Run a command and return the result.

    Args:
        cmd: Command and arguments to run
        check: Whether to raise exception on failure

    Returns:
        CompletedProcess object or None on failure
    """
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=check)
        return result
    except subprocess.CalledProcessError as e:
        if check:
            print(f"Error running command: {' '.join(cmd)}", file=sys.stderr)
            print(f"Error: {e.stderr}", file=sys.stderr)
        return None
    except FileNotFoundError:
        print(f"Command not found: {cmd[0]}", file=sys.stderr)
        return None


def check_command_exists(cmd: str) -> bool:
    """
    Check if a command exists in PATH.

    Args:
        cmd: Command name to check

    Returns:
        True if command exists
    """
    result = run_command(["which" if platform.system() != "Windows" else "where", cmd], check=False)
    return result is not None and result.returncode == 0


def check_prerequisites() -> bool:
    """
    Check if required tools are installed.

    Returns:
        True if all prerequisites are met
    """
    print("🔍 Checking prerequisites...")
    print("-" * 80)

    required = {
        "git": "Git version control",
        "python3": "Python 3.8+",
    }

    optional = {
        "gh": "GitHub CLI (optional)",
        "node": "Node.js (optional)",
        "npm": "npm package manager (optional)",
        "composer": "PHP Composer (optional)",
        "make": "Make build tool (optional)",
    }

    all_ok = True

    for cmd, desc in required.items():
        if check_command_exists(cmd):
            print(f"✅ {desc}: {cmd} found")
        else:
            print(f"❌ {desc}: {cmd} NOT found (required)")
            all_ok = False

    print()
    for cmd, desc in optional.items():
        if check_command_exists(cmd):
            print(f"✅ {desc}: {cmd} found")
        else:
            print(f"⚠️  {desc}: {cmd} NOT found (optional)")

    print()
    return all_ok


def check_python_version() -> bool:
    """
    Check if Python version is 3.8 or higher.

    Returns:
        True if version is sufficient
    """
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python version: {version.major}.{version.minor}.{version.micro} (need 3.8+)")
        return False


def setup_git_config() -> None:
    """Set up git configuration with commit message template."""
    print("\n📝 Setting up Git configuration...")
    print("-" * 80)

    # Check if .gitmessage exists
    gitmessage = Path(".gitmessage")
    if gitmessage.exists():
        result = run_command(["git", "config", "commit.template", ".gitmessage"], check=False)
        if result and result.returncode == 0:
            print("✅ Git commit message template configured")
        else:
            print("⚠️  Could not set git commit message template")
    else:
        print("⚠️  .gitmessage not found")

    # Check current git user
    name_result = run_command(["git", "config", "user.name"], check=False)
    email_result = run_command(["git", "config", "user.email"], check=False)

    if name_result and name_result.returncode == 0 and name_result.stdout.strip():
        print(f"✅ Git user.name: {name_result.stdout.strip()}")
    else:
        print("⚠️  Git user.name not configured (run: git config user.name 'Your Name')")

    if email_result and email_result.returncode == 0 and email_result.stdout.strip():
        print(f"✅ Git user.email: {email_result.stdout.strip()}")
    else:
        print("⚠️  Git user.email not configured (run: git config user.email 'you@example.com')")


def install_python_dependencies() -> bool:
    """
    Install Python dependencies if requirements.txt exists.

    Returns:
        True if successful or no dependencies to install
    """
    print("\n📦 Checking Python dependencies...")
    print("-" * 80)

    req_file = Path("requirements.txt")
    if not req_file.exists():
        print("ℹ️  No requirements.txt found, skipping Python dependencies")
        return True

    print("Installing Python dependencies...")
    result = run_command(["pip3", "install", "-r", "requirements.txt"], check=False)

    if result and result.returncode == 0:
        print("✅ Python dependencies installed successfully")
        return True
    else:
        print("⚠️  Could not install Python dependencies")
        return False


def setup_pre_commit_hooks() -> None:
    """Set up pre-commit hooks if available."""
    print("\n🪝 Setting up pre-commit hooks...")
    print("-" * 80)

    # Check if pre-commit is installed
    if not check_command_exists("pre-commit"):
        print("ℹ️  pre-commit not installed (optional)")
        print("   Install with: pip install pre-commit")
        return

    # Install pre-commit hooks
    result = run_command(["pre-commit", "install"], check=False)
    if result and result.returncode == 0:
        print("✅ pre-commit hooks installed")
    else:
        print("⚠️  Could not install pre-commit hooks")


def check_environment_variables() -> None:
    """Check for recommended environment variables."""
    print("\n🌍 Checking environment variables...")
    print("-" * 80)

    recommended = {
        "GH_PAT": "GitHub Personal Access Token (for automation scripts)",
        "GH_TOKEN": "GitHub Token (alternative to GH_PAT)",
    }

    found_any = False
    for var, desc in recommended.items():
        if os.environ.get(var):
            print(f"✅ {var}: configured")
            found_any = True
        else:
            print(f"ℹ️  {var}: not set ({desc})")

    if not found_any:
        print("\n💡 Tip: Some automation scripts require GitHub authentication.")
        print("   Set GH_PAT or GH_TOKEN, or use 'gh auth login'")


def print_next_steps() -> None:
    """Print recommended next steps."""
    print("\n" + "=" * 80)
    print("✨ NEXT STEPS")
    print("=" * 80)
    print("""
1. Review the CONTRIBUTING.md file for contribution guidelines
2. Read the README.md to understand the project structure
3. Set up your Git user config if not already done:
   git config user.name "Your Name"
   git config user.email "you@example.com"

4. If working with automation scripts, set up GitHub authentication:
   export GH_PAT="your_token"
   # or
   gh auth login

5. Create a new branch for your work:
   git checkout -b feature/your-feature-name

6. Start contributing! 🎉

For more information, see:
- ./CONTRIBUTING.md - Contribution guidelines
- ./docs/ - Full documentation
- ./scripts/README.md - Script documentation
""")


def main() -> int:
    """
    Main entry point for development environment setup.

    Returns:
        Exit code (0 for success)
    """
    parser = argparse.ArgumentParser(
        description="Quick setup script for new contributors"
    )
    parser.add_argument(
        "--skip-install",
        action="store_true",
        help="Skip installing dependencies"
    )

    args = parser.parse_args()

    print("\n" + "=" * 80)
    print("🚀 MOKOSTANDARDS DEVELOPMENT ENVIRONMENT SETUP")
    print("=" * 80)

    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Missing required prerequisites. Please install them and try again.")
        return 1

    # Check Python version
    if not check_python_version():
        print("\n❌ Python version is too old. Please upgrade to Python 3.8+")
        return 1

    # Set up Git configuration
    setup_git_config()

    # Install dependencies unless skipped
    if not args.skip_install:
        install_python_dependencies()
    else:
        print("\nℹ️  Skipping dependency installation (--skip-install)")

    # Set up pre-commit hooks
    setup_pre_commit_hooks()

    # Check environment variables
    check_environment_variables()

    # Print next steps
    print_next_steps()

    print("=" * 80)
    print("✅ Setup complete!")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())
