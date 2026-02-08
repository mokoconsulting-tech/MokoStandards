#!/usr/bin/env python3
"""
Unified Release Tool - Consolidates all release functionality.

Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program (./LICENSE.md).

FILE INFORMATION
DEFGROUP: Script.Release
INGROUP: Release.Unified
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /scripts/release/unified_release.py
VERSION: 03.01.01
BRIEF: Unified release tool consolidating all release scripts
USAGE: ./scripts/release/unified_release.py <command> [options]
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Add lib directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

try:
    import common
    import extension_utils
except ImportError:
    print("ERROR: Cannot import required libraries", file=sys.stderr)
    print("Ensure scripts/lib/common.py and extension_utils.py exist", file=sys.stderr)
    sys.exit(1)


class ReleaseType(Enum):
    """Release type enumeration."""
    STABLE = "stable"
    RC = "rc"
    BETA = "beta"
    ALPHA = "alpha"
    DEV = "dev"


class VersionInfo:
    """Version information container."""
    
    def __init__(self, version_string: str):
        """
        Initialize version info from string.
        
        Args:
            version_string: Version string (e.g., "1.2.3-rc1")
        """
        self.full_version = version_string.lstrip('v')
        self._parse()
    
    def _parse(self):
        """Parse version string into components."""
        # Match semver pattern
        pattern = r'^(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9.-]+))?$'
        match = re.match(pattern, self.full_version)
        
        if not match:
            raise ValueError(f"Invalid version format: {self.full_version}")
        
        self.major = int(match.group(1))
        self.minor = int(match.group(2))
        self.patch = int(match.group(3))
        self.prerelease = match.group(4) or ""
        self.base_version = f"{self.major}.{self.minor}.{self.patch}"
        
        # Determine release type
        if not self.prerelease:
            self.release_type = ReleaseType.STABLE
        elif self.prerelease.startswith('rc'):
            self.release_type = ReleaseType.RC
        elif self.prerelease.startswith('beta'):
            self.release_type = ReleaseType.BETA
        elif self.prerelease.startswith('alpha'):
            self.release_type = ReleaseType.ALPHA
        elif self.prerelease.startswith('dev'):
            self.release_type = ReleaseType.DEV
        else:
            self.release_type = ReleaseType.STABLE
    
    def __str__(self):
        return self.full_version
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "full_version": self.full_version,
            "base_version": self.base_version,
            "major": self.major,
            "minor": self.minor,
            "patch": self.patch,
            "prerelease": self.prerelease,
            "release_type": self.release_type.value,
            "is_prerelease": bool(self.prerelease)
        }


class UnifiedRelease:
    """Unified release tool."""
    
    def __init__(self, working_dir: str = "."):
        """
        Initialize unified release tool.
        
        Args:
            working_dir: Working directory
        """
        self.working_dir = Path(working_dir).resolve()
        self.repo_root = common.get_repo_root()
    
    def detect_version_from_files(self) -> Optional[str]:
        """
        Detect version from version files.
        
        Returns:
            Version string or None if not found
        """
        # Try CITATION.cff
        citation_file = self.repo_root / "CITATION.cff"
        if citation_file.exists():
            try:
                import yaml
                with open(citation_file) as f:
                    data = yaml.safe_load(f)
                    if 'version' in data:
                        return data['version']
            except Exception as e:
                common.log_debug(f"Failed to read version from CITATION.cff: {e}")
        
        # Try pyproject.toml
        pyproject_file = self.repo_root / "pyproject.toml"
        if pyproject_file.exists():
            try:
                import tomli
                with open(pyproject_file, 'rb') as f:
                    data = tomli.load(f)
                    if 'project' in data and 'version' in data['project']:
                        return data['project']['version']
                    if 'tool' in data and 'poetry' in data['tool'] and 'version' in data['tool']['poetry']:
                        return data['tool']['poetry']['version']
            except Exception as e:
                common.log_debug(f"Failed to read version from pyproject.toml: {e}")
        
        # Try package.json
        package_file = self.repo_root / "package.json"
        if package_file.exists():
            try:
                with open(package_file) as f:
                    data = json.load(f)
                    if 'version' in data:
                        return data['version']
            except Exception as e:
                common.log_debug(f"Failed to read version from package.json: {e}")
        
        return None
    
    def get_last_tag(self) -> Optional[str]:
        """
        Get last git tag.
        
        Returns:
            Last tag or None
        """
        try:
            result = subprocess.run(
                ['git', 'describe', '--tags', '--abbrev=0'],
                cwd=self.repo_root,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return result.stdout.strip().lstrip('v')
        except Exception as e:
            common.log_debug(f"Failed to get last git tag: {e}")
        return None
    
    def bump_version(self, bump_type: str = "patch") -> str:
        """
        Bump version from last tag.
        
        Args:
            bump_type: Type of bump (major, minor, patch)
        
        Returns:
            New version string
        """
        last_version = self.get_last_tag() or "0.0.0"
        version_info = VersionInfo(last_version)
        
        if bump_type == "major":
            version_info.major += 1
            version_info.minor = 0
            version_info.patch = 0
        elif bump_type == "minor":
            version_info.minor += 1
            version_info.patch = 0
        else:  # patch
            version_info.patch += 1
        
        return f"{version_info.major}.{version_info.minor}.{version_info.patch}"
    
    def update_version_files(self, version: str) -> List[str]:
        """
        Update version in all version files.
        
        Args:
            version: New version string
        
        Returns:
            List of updated files
        """
        updated_files = []
        
        common.log_info(f"Updating version to: {version}")
        
        # Update CITATION.cff
        citation_file = self.repo_root / "CITATION.cff"
        if citation_file.exists():
            content = citation_file.read_text()
            new_content = re.sub(
                r'^version:.*$',
                f'version: {version}',
                content,
                flags=re.MULTILINE
            )
            if content != new_content:
                citation_file.write_text(new_content)
                updated_files.append(str(citation_file))
                common.log_success(f"Updated {citation_file.name}")
        
        # Update pyproject.toml
        pyproject_file = self.repo_root / "pyproject.toml"
        if pyproject_file.exists():
            content = pyproject_file.read_text()
            new_content = re.sub(
                r'^version\s*=\s*["\'].*["\']',
                f'version = "{version}"',
                content,
                flags=re.MULTILINE
            )
            if content != new_content:
                pyproject_file.write_text(new_content)
                updated_files.append(str(pyproject_file))
                common.log_success(f"Updated {pyproject_file.name}")
        
        # Update package.json
        package_file = self.repo_root / "package.json"
        if package_file.exists():
            try:
                with open(package_file) as f:
                    data = json.load(f)
                data['version'] = version
                with open(package_file, 'w') as f:
                    json.dump(data, f, indent=2)
                    f.write('\n')
                updated_files.append(str(package_file))
                common.log_success(f"Updated {package_file.name}")
            except Exception as e:
                common.log_warning(f"Failed to update {package_file.name}: {e}")
        
        return updated_files
    
    def create_package(self, version: str, output_dir: str = "dist") -> Optional[Path]:
        """
        Create release package.
        
        Args:
            version: Version string
            output_dir: Output directory
        
        Returns:
            Path to created package
        """
        # Detect platform
        ext_info = extension_utils.get_extension_info(str(self.working_dir))
        
        if ext_info:
            # Use package_extension.py for Joomla/Dolibarr
            common.log_info("Creating extension package")
            from package_extension import create_package
            return create_package(
                src_dir=str(self.working_dir),
                output_dir=output_dir,
                version=version
            )
        else:
            # Generic package
            common.log_info("Creating generic package")
            output_path = Path(output_dir)
            common.ensure_directory(output_path)
            
            repo_name = self.repo_root.name
            package_name = f"{repo_name}-{version}.tar.gz"
            package_path = output_path / package_name
            
            # Create tarball
            subprocess.run(
                ['tar', '-czf', str(package_path), '--exclude=.git', '--exclude=node_modules', '.'],
                cwd=self.repo_root,
                check=True
            )
            
            common.log_success(f"Created package: {package_path.name}")
            return package_path
    
    def cmd_version(self, args) -> int:
        """
        Handle version command.
        
        Args:
            args: Command arguments
        
        Returns:
            Exit code
        """
        if args.detect:
            version = self.detect_version_from_files()
            if version:
                print(version)
                return 0
            else:
                common.log_error("No version found in version files")
                return 1
        
        elif args.bump:
            version = self.bump_version(args.bump)
            print(version)
            if args.update:
                self.update_version_files(version)
            return 0
        
        elif args.set:
            version_info = VersionInfo(args.set)
            if args.update:
                self.update_version_files(str(version_info))
            print(json.dumps(version_info.to_dict(), indent=2))
            return 0
        
        else:
            # Show current version
            version = self.detect_version_from_files() or self.get_last_tag() or "unknown"
            version_info = VersionInfo(version) if version != "unknown" else None
            
            if version_info:
                print(json.dumps(version_info.to_dict(), indent=2))
            else:
                print(f"Version: {version}")
            return 0
    
    def cmd_package(self, args) -> int:
        """
        Handle package command.
        
        Args:
            args: Command arguments
        
        Returns:
            Exit code
        """
        version = args.version
        if not version:
            version = self.detect_version_from_files()
            if not version:
                common.log_error("No version specified and could not auto-detect")
                return 1
        
        try:
            package_path = self.create_package(version, args.output_dir)
            if package_path:
                return 0
            else:
                return 1
        except Exception as e:
            common.log_error(f"Package creation failed: {e}")
            return 1
    
    def cmd_release(self, args) -> int:
        """
        Handle release command (full workflow).
        
        Args:
            args: Command arguments
        
        Returns:
            Exit code
        """
        version = args.version
        if not version:
            if args.bump:
                version = self.bump_version(args.bump)
                common.log_info(f"Bumped version to: {version}")
            else:
                version = self.detect_version_from_files()
                if not version:
                    common.log_error("No version specified and could not auto-detect")
                    return 1
        
        version_info = VersionInfo(version)
        
        common.log_info(f"Release workflow for version {version_info}")
        common.log_info(f"Release type: {version_info.release_type.value}")
        
        # Update version files
        if not args.skip_version_update:
            updated_files = self.update_version_files(str(version_info))
            if updated_files:
                common.log_info(f"Updated {len(updated_files)} version file(s)")
        
        # Create package
        if not args.skip_package:
            package_path = self.create_package(str(version_info), args.output_dir)
            if not package_path:
                return 1
        
        common.log_success("Release workflow completed")
        return 0


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Unified release tool for version management and packaging",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  version    Manage versions (detect, bump, set)
  package    Create release package
  release    Full release workflow (version + package)

Examples:
  # Detect current version
  %(prog)s version --detect
  
  # Bump version and update files
  %(prog)s version --bump minor --update
  
  # Set specific version
  %(prog)s version --set 1.2.3-rc1 --update
  
  # Create package
  %(prog)s package --version 1.2.3
  
  # Full release workflow
  %(prog)s release --version 1.2.3
  %(prog)s release --bump patch
"""
    )
    
    parser.add_argument(
        '-d', '--working-dir',
        default='.',
        help='Working directory (default: current)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Version command
    version_parser = subparsers.add_parser('version', help='Version management')
    version_parser.add_argument('--detect', action='store_true', help='Detect version from files')
    version_parser.add_argument('--bump', choices=['major', 'minor', 'patch'], help='Bump version')
    version_parser.add_argument('--set', help='Set specific version')
    version_parser.add_argument('--update', action='store_true', help='Update version files')
    
    # Package command
    package_parser = subparsers.add_parser('package', help='Create package')
    package_parser.add_argument('--version', help='Version to package')
    package_parser.add_argument('-o', '--output-dir', default='dist', help='Output directory')
    
    # Release command
    release_parser = subparsers.add_parser('release', help='Full release workflow')
    release_parser.add_argument('--version', help='Release version')
    release_parser.add_argument('--bump', choices=['major', 'minor', 'patch'], help='Bump version instead')
    release_parser.add_argument('-o', '--output-dir', default='dist', help='Output directory')
    release_parser.add_argument('--skip-version-update', action='store_true', help='Skip version file updates')
    release_parser.add_argument('--skip-package', action='store_true', help='Skip package creation')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        tool = UnifiedRelease(args.working_dir)
        
        if args.command == 'version':
            return tool.cmd_version(args)
        elif args.command == 'package':
            return tool.cmd_package(args)
        elif args.command == 'release':
            return tool.cmd_release(args)
        else:
            parser.print_help()
            return 1
    
    except Exception as e:
        common.log_error(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
