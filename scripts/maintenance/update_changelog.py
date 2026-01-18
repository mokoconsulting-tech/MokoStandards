#!/usr/bin/env python3
"""
Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
DEFGROUP: MokoStandards
INGROUP: MokoStandards.Scripts
REPO: https://github.com/mokoconsulting-tech/MokoStandards/
VERSION: 05.00.00
PATH: ./scripts/update_changelog.py
BRIEF: Script to update CHANGELOG.md with entries to UNRELEASED section
NOTE: Follows Keep a Changelog format, supports Added/Changed/Deprecated/Removed/Fixed/Security
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional


class ChangelogUpdater:
    """Updates CHANGELOG.md following Keep a Changelog format."""

    VALID_CATEGORIES = ["Added", "Changed", "Deprecated", "Removed", "Fixed", "Security"]
    UNRELEASED_PATTERN = r"## \[UNRELEASED\]"

    def __init__(self, changelog_path: Path):
        """
        Initialize the changelog updater.

        Args:
            changelog_path: Path to CHANGELOG.md file
        """
        self.changelog_path = changelog_path
        self.lines: List[str] = []

    def read_changelog(self) -> bool:
        """
        Read the changelog file.

        Returns:
            True if successful, False otherwise
        """
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

    def find_unreleased_section(self) -> Optional[int]:
        """
        Find the UNRELEASED section in the changelog.

        Returns:
            Line index of UNRELEASED section, or None if not found
        """
        for i, line in enumerate(self.lines):
            if re.match(self.UNRELEASED_PATTERN, line):
                return i
        return None

    def find_next_version_section(self, start_index: int) -> Optional[int]:
        """
        Find the next version section after UNRELEASED.

        Args:
            start_index: Index to start searching from

        Returns:
            Line index of next version section, or None if not found
        """
        version_pattern = r"## \[\d+\.\d+\.\d+\]"
        for i in range(start_index + 1, len(self.lines)):
            if re.match(version_pattern, self.lines[i]):
                return i
        return None

    def get_category_index(self, unreleased_index: int, next_version_index: Optional[int],
                          category: str) -> Optional[int]:
        """
        Find the index of a specific category within UNRELEASED section.

        Args:
            unreleased_index: Index of UNRELEASED heading
            next_version_index: Index of next version section (or None)
            category: Category name (e.g., "Added", "Changed")

        Returns:
            Line index of category heading, or None if not found
        """
        end_index = next_version_index if next_version_index else len(self.lines)
        category_pattern = rf"### {category}"

        for i in range(unreleased_index + 1, end_index):
            if re.match(category_pattern, self.lines[i]):
                return i
        return None

    def add_entry(self, category: str, entry: str, subcategory: Optional[str] = None) -> bool:
        """
        Add an entry to the UNRELEASED section.

        Args:
            category: Category (Added/Changed/Deprecated/Removed/Fixed/Security)
            entry: Entry text to add
            subcategory: Optional subcategory/subheading

        Returns:
            True if successful, False otherwise
        """
        if category not in self.VALID_CATEGORIES:
            print(f"Error: Invalid category '{category}'. Must be one of: {', '.join(self.VALID_CATEGORIES)}",
                  file=sys.stderr)
            return False

        unreleased_index = self.find_unreleased_section()
        if unreleased_index is None:
            print("Error: UNRELEASED section not found in CHANGELOG.md", file=sys.stderr)
            return False

        next_version_index = self.find_next_version_section(unreleased_index)
        category_index = self.get_category_index(unreleased_index, next_version_index, category)

        # Format entry with proper indentation
        if subcategory:
            formatted_entry = f"  - **{subcategory}**: {entry}\n"
        else:
            formatted_entry = f"- {entry}\n"

        if category_index is None:
            # Category doesn't exist, create it
            # Find insertion point (after UNRELEASED heading, before next section)
            insert_index = unreleased_index + 1

            # Skip any blank lines after UNRELEASED
            while insert_index < len(self.lines) and self.lines[insert_index].strip() == "":
                insert_index += 1

            # Insert category heading and entry
            self.lines.insert(insert_index, f"### {category}\n")
            self.lines.insert(insert_index + 1, formatted_entry)
            self.lines.insert(insert_index + 2, "\n")
        else:
            # Category exists, add entry after the category heading
            insert_index = category_index + 1

            # Skip existing entries to add at the end of the category
            while insert_index < len(self.lines):
                line = self.lines[insert_index]
                # Stop if we hit another category or version section
                if line.startswith("###") or line.startswith("##"):
                    break
                # Stop if we hit a blank line followed by non-entry content
                if line.strip() == "" and insert_index + 1 < len(self.lines):
                    next_line = self.lines[insert_index + 1]
                    if next_line.startswith("###") or next_line.startswith("##"):
                        break
                insert_index += 1

            # Insert entry before any blank lines
            while insert_index > category_index + 1 and self.lines[insert_index - 1].strip() == "":
                insert_index -= 1

            self.lines.insert(insert_index, formatted_entry)

        return True

    def write_changelog(self) -> bool:
        """
        Write the updated changelog back to file.

        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.changelog_path, "w", encoding="utf-8") as f:
                f.writelines(self.lines)
            return True
        except Exception as e:
            print(f"Error writing CHANGELOG.md: {e}", file=sys.stderr)
            return False

    def display_unreleased(self) -> None:
        """Display the current UNRELEASED section."""
        unreleased_index = self.find_unreleased_section()
        if unreleased_index is None:
            print("UNRELEASED section not found")
            return

        next_version_index = self.find_next_version_section(unreleased_index)
        end_index = next_version_index if next_version_index else len(self.lines)

        print("Current UNRELEASED section:")
        print("=" * 60)
        for i in range(unreleased_index, end_index):
            print(self.lines[i], end="")
        print("=" * 60)


def main() -> int:
    """
    Main entry point for the changelog updater script.

    Returns:
        Exit code (0 for success, non-zero for error)
    """
    parser = argparse.ArgumentParser(
        description="Update CHANGELOG.md with entries to UNRELEASED section",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add a simple entry
  %(prog)s --category Added --entry "New feature X"

  # Add an entry with subcategory
  %(prog)s --category Changed --entry "Updated API endpoints" --subcategory "API"

  # Display current UNRELEASED section
  %(prog)s --show

Categories: Added, Changed, Deprecated, Removed, Fixed, Security
        """
    )

    parser.add_argument(
        "--changelog",
        type=Path,
        default=Path("CHANGELOG.md"),
        help="Path to CHANGELOG.md file (default: ./CHANGELOG.md)"
    )

    parser.add_argument(
        "--category",
        choices=ChangelogUpdater.VALID_CATEGORIES,
        help="Category for the entry"
    )

    parser.add_argument(
        "--entry",
        type=str,
        help="Entry text to add to the changelog"
    )

    parser.add_argument(
        "--subcategory",
        type=str,
        help="Optional subcategory/subheading for the entry"
    )

    parser.add_argument(
        "--show",
        action="store_true",
        help="Display the current UNRELEASED section"
    )

    args = parser.parse_args()

    # Resolve changelog path
    if not args.changelog.is_absolute():
        # Try to find repository root
        current_dir = Path.cwd()
        repo_root = current_dir
        while repo_root.parent != repo_root:
            if (repo_root / ".git").exists():
                break
            repo_root = repo_root.parent
        else:
            repo_root = current_dir

        changelog_path = repo_root / args.changelog
    else:
        changelog_path = args.changelog

    updater = ChangelogUpdater(changelog_path)

    if not updater.read_changelog():
        return 1

    if args.show:
        updater.display_unreleased()
        return 0

    if not args.category or not args.entry:
        parser.error("--category and --entry are required (or use --show)")

    if updater.add_entry(args.category, args.entry, args.subcategory):
        if updater.write_changelog():
            print(f"Successfully added entry to UNRELEASED section: [{args.category}] {args.entry}")
            return 0
        else:
            return 1
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
