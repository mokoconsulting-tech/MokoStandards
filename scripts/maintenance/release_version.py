#!/usr/bin/env python3
"""
Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-LICENSE-IDENTIFIER: GPL-3.0-or-later

This program is free software; you can redistribute it and/or modify it under the terms
of the GNU General Public License as published by the Free Software Foundation; either
version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License (./LICENSE).

# FILE INFORMATION
DEFGROUP: MokoStandards
INGROUP: MokoStandards.Scripts
REPO: https://github.com/mokoconsulting-tech/MokoStandards/
VERSION: 05.00.00
PATH: ./scripts/release_version.py
BRIEF: Script to release a version by moving UNRELEASED items to versioned section
NOTE: Updates CHANGELOG.md and optionally updates VERSION in files
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple


class VersionReleaser:
    """Manages version releases in CHANGELOG.md and updates VERSION in files."""

    UNRELEASED_PATTERN = r"## \[Unreleased\]"  # Standard Keep a Changelog format
    VERSION_PATTERN = r"## \[(\d+\.\d+\.\d+)\]"
    VERSION_HEADER_PATTERN = r"VERSION:\s*(\d+\.\d+\.\d+)"
    CHANGELOG_H1_PATTERN = r"^# CHANGELOG - .+ \(VERSION: (\d+\.\d+\.\d+)\)"  # H1 format

    def __init__(self, changelog_path: Path, repo_root: Path):
        """
        Initialize the version releaser.

        Args:
            changelog_path: Path to CHANGELOG.md file
            repo_root: Path to repository root
        """
        self.changelog_path = changelog_path
        self.repo_root = repo_root
        self.lines: List[str] = []

    def read_changelog(self) -> bool:
        """Read the changelog file."""
        try:
            with open(self.changelog_path, "r", encoding="utf-8") as f:
                self.lines = f.readlines()
            return True
        except FileNotFoundError:
            print(f"Error: CHANGELOG.md not found at {self.changelog_path}", file=sys.stderr)
            return False
        except Exception as e:
            print(f"Error reading CHANGELOG.md: {e}", file=sys.stderr)
            return False

    def write_changelog(self) -> bool:
        """Write the updated changelog back to file."""
        try:
            with open(self.changelog_path, "w", encoding="utf-8") as f:
                f.writelines(self.lines)
            return True
        except Exception as e:
            print(f"Error writing CHANGELOG.md: {e}", file=sys.stderr)
            return False

    def find_unreleased_section(self) -> Optional[int]:
        """Find the UNRELEASED section in the changelog."""
        for i, line in enumerate(self.lines):
            if re.match(self.UNRELEASED_PATTERN, line):
                return i
        return None

    def find_next_version_section(self, start_index: int) -> Optional[int]:
        """Find the next version section after a given index."""
        for i in range(start_index + 1, len(self.lines)):
            if re.match(self.VERSION_PATTERN, self.lines[i]):
                return i
        return None

    def has_unreleased_content(self, unreleased_index: int, next_version_index: Optional[int]) -> bool:
        """Check if UNRELEASED section has any content."""
        end_index = next_version_index if next_version_index else len(self.lines)

        for i in range(unreleased_index + 1, end_index):
            line = self.lines[i].strip()
            # Skip empty lines and headers
            if line and not line.startswith("##"):
                return True
        return False

    def validate_version(self, version: str) -> bool:
        """Validate version format (XX.YY.ZZ)."""
        pattern = r"^\d{2}\.\d{2}\.\d{2}$"
        return bool(re.match(pattern, version))

    def release_version(self, version: str, date: Optional[str] = None) -> bool:
        """
        Move UNRELEASED content to a new version section.

        Args:
            version: Version number (XX.YY.ZZ format)
            date: Release date (YYYY-MM-DD format), defaults to today

        Returns:
            True if successful, False otherwise
        """
        if not self.validate_version(version):
            print(f"Error: Invalid version format '{version}'. Must be XX.YY.ZZ (e.g., 05.01.00)",
                  file=sys.stderr)
            return False

        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        unreleased_index = self.find_unreleased_section()
        if unreleased_index is None:
            print("Error: UNRELEASED section not found in CHANGELOG.md", file=sys.stderr)
            return False

        next_version_index = self.find_next_version_section(unreleased_index)

        # Check if UNRELEASED has content
        if not self.has_unreleased_content(unreleased_index, next_version_index):
            print("Warning: UNRELEASED section is empty. Nothing to release.", file=sys.stderr)
            return False

        # Get the content between UNRELEASED and next version
        if next_version_index:
            unreleased_content = self.lines[unreleased_index + 1:next_version_index]
        else:
            unreleased_content = self.lines[unreleased_index + 1:]

        # Remove the old UNRELEASED content
        if next_version_index:
            del self.lines[unreleased_index + 1:next_version_index]
        else:
            del self.lines[unreleased_index + 1:]

        # Insert new version section after UNRELEASED
        new_version_lines = [
            "\n",
            f"## [{version}] - {date}\n"
        ]
        new_version_lines.extend(unreleased_content)

        # Insert after UNRELEASED heading
        insert_index = unreleased_index + 1
        for line in reversed(new_version_lines):
            self.lines.insert(insert_index, line)

        # Update H1 header version
        self.update_changelog_h1_version(version)

        return True

    def update_changelog_h1_version(self, version: str) -> bool:
        """
        Update the version in the H1 header of CHANGELOG.
        
        Format: # CHANGELOG - RepoName (VERSION: X.Y.Z)
        
        Args:
            version: New version number
            
        Returns:
            True if updated, False otherwise
        """
        for i, line in enumerate(self.lines):
            if re.match(self.CHANGELOG_H1_PATTERN, line):
                # Extract repo name from current H1
                match = re.match(r"^# CHANGELOG - (.+) \(VERSION: \d+\.\d+\.\d+\)", line)
                if match:
                    repo_name = match.group(1)
                    self.lines[i] = f"# CHANGELOG - {repo_name} (VERSION: {version})\n"
                    return True
        return False

    def update_file_versions(self, version: str, dry_run: bool = False) -> List[Path]:
        """
        Update VERSION in all files in the repository.

        Args:
            version: New version number
            dry_run: If True, don't actually update files

        Returns:
            List of files that were (or would be) updated
        """
        updated_files = []

        # Find all markdown, Python, and text files
        patterns = ["**/*.md", "**/*.py", "**/*.txt", "**/*.yml", "**/*.yaml"]
        files_to_check = []

        for pattern in patterns:
            files_to_check.extend(self.repo_root.glob(pattern))

        for file_path in files_to_check:
            # Skip certain directories
            skip_dirs = [".git", "node_modules", "vendor", "__pycache__", ".venv"]
            if any(skip_dir in file_path.parts for skip_dir in skip_dirs):
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Check if file has VERSION header
                if re.search(self.VERSION_HEADER_PATTERN, content):
                    new_content = re.sub(
                        self.VERSION_HEADER_PATTERN,
                        f"VERSION: {version}",
                        content
                    )

                    if new_content != content:
                        if not dry_run:
                            with open(file_path, "w", encoding="utf-8") as f:
                                f.write(new_content)
                        updated_files.append(file_path.relative_to(self.repo_root))

            except (UnicodeDecodeError, PermissionError):
                # Skip binary files or files we can't read
                continue
            except Exception as e:
                print(f"Warning: Error processing {file_path}: {e}", file=sys.stderr)
                continue

        return updated_files

    def extract_release_notes(self, version: str) -> Optional[str]:
        """
        Extract release notes for a specific version from CHANGELOG.

        Args:
            version: Version number to extract notes for

        Returns:
            Release notes content or None if not found
        """
        version_pattern = rf"## \[{re.escape(version)}\]"
        notes_lines = []
        in_version = False

        for line in self.lines:
            if re.match(version_pattern, line):
                in_version = True
                continue
            elif in_version:
                # Stop at next version heading
                if line.startswith("## ["):
                    break
                notes_lines.append(line)

        if notes_lines:
            return "".join(notes_lines).strip()
        return None

    def create_github_release(self, version: str, dry_run: bool = False) -> bool:
        """
        Create a GitHub release using gh CLI.

        Args:
            version: Version number
            dry_run: If True, don't actually create release

        Returns:
            True if successful, False otherwise
        """
        # Check if gh CLI is available
        try:
            subprocess.run(["gh", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Warning: gh CLI not found. Skipping GitHub release creation.", file=sys.stderr)
            print("Install gh CLI: https://cli.github.com/", file=sys.stderr)
            return False

        # Extract release notes from changelog
        release_notes = self.extract_release_notes(version)
        if not release_notes:
            print(f"Warning: Could not extract release notes for version {version}", file=sys.stderr)
            release_notes = f"Release {version}"

        tag_name = f"v{version}"
        title = f"Release {version}"

        if dry_run:
            print(f"\n[DRY RUN] Would create GitHub release:")
            print(f"  Tag: {tag_name}")
            print(f"  Title: {title}")
            print(f"  Notes:\n{release_notes[:200]}...")
            return True

        try:
            # Create the release
            cmd = [
                "gh", "release", "create", tag_name,
                "--title", title,
                "--notes", release_notes
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"\nSuccessfully created GitHub release: {tag_name}")
            print(f"Release URL: {result.stdout.strip()}")
            return True

        except subprocess.CalledProcessError as e:
            print(f"Error creating GitHub release: {e.stderr}", file=sys.stderr)
            return False


def main() -> int:
    """Main entry point for the version release script."""
    parser = argparse.ArgumentParser(
        description="Release a version by moving UNRELEASED items to versioned section",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Release version 05.01.00 with today's date
  %(prog)s --version 05.01.00

  # Release version with specific date
  %(prog)s --version 05.01.00 --date 2026-01-15

  # Release and update VERSION in all files
  %(prog)s --version 05.01.00 --update-files

  # Release, update files, and create GitHub release
  %(prog)s --version 05.01.00 --update-files --create-release

  # Dry run to see what would be updated
  %(prog)s --version 05.01.00 --update-files --create-release --dry-run

Version format: XX.YY.ZZ (e.g., 05.01.00)
        """
    )

    parser.add_argument(
        "--version",
        type=str,
        required=True,
        help="Version number in XX.YY.ZZ format (e.g., 05.01.00)"
    )

    parser.add_argument(
        "--date",
        type=str,
        help="Release date in YYYY-MM-DD format (defaults to today)"
    )

    parser.add_argument(
        "--changelog",
        type=Path,
        default=Path("CHANGELOG.md"),
        help="Path to CHANGELOG.md file (default: ./CHANGELOG.md)"
    )

    parser.add_argument(
        "--update-files",
        action="store_true",
        help="Update VERSION header in all repository files"
    )

    parser.add_argument(
        "--create-release",
        action="store_true",
        help="Create a GitHub release using gh CLI"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )

    args = parser.parse_args()

    # Find repository root
    current_dir = Path.cwd()
    repo_root = current_dir
    while repo_root.parent != repo_root:
        if (repo_root / ".git").exists():
            break
        repo_root = repo_root.parent
    else:
        repo_root = current_dir

    # Resolve changelog path
    if not args.changelog.is_absolute():
        changelog_path = repo_root / args.changelog
    else:
        changelog_path = args.changelog

    releaser = VersionReleaser(changelog_path, repo_root)

    if not releaser.read_changelog():
        return 1

    # Release the version
    if args.dry_run:
        print(f"[DRY RUN] Would release version {args.version}")
    else:
        if releaser.release_version(args.version, args.date):
            if releaser.write_changelog():
                print(f"Successfully released version {args.version} in CHANGELOG.md")
            else:
                return 1
        else:
            return 1

    # Update file versions if requested
    if args.update_files:
        updated_files = releaser.update_file_versions(args.version, args.dry_run)

        if updated_files:
            if args.dry_run:
                print(f"\n[DRY RUN] Would update VERSION in {len(updated_files)} files:")
            else:
                print(f"\nUpdated VERSION to {args.version} in {len(updated_files)} files:")

            for file_path in sorted(updated_files):
                print(f"  - {file_path}")
        else:
            print("\nNo files with VERSION headers found to update.")

    # Create GitHub release if requested
    if args.create_release:
        if not releaser.create_github_release(args.version, args.dry_run):
            print("\nNote: GitHub release creation failed or was skipped.", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
