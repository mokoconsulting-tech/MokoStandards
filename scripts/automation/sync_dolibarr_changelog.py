#!/usr/bin/env python3
"""
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
along with this program. If not, see <https://www.gnu.org/licenses/>.

# FILE INFORMATION
DEFGROUP: MokoStandards.Scripts
INGROUP: MokoStandards.Dolibarr
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /scripts/automation/sync_dolibarr_changelog.py
VERSION: 03.01.03
BRIEF: Synchronizes CHANGELOG.md from root to src/ChangeLog for Dolibarr modules

DESCRIPTION:
    This script automatically copies the CHANGELOG.md file from the repository
    root to the src/ChangeLog location required by Dolibarr modules. It can be
    run manually or automatically via Git hooks or CI/CD pipelines.

USAGE:
    # Sync changelog
    python3 scripts/automation/sync_dolibarr_changelog.py

    # Dry run mode (preview changes without modifying files)
    python3 scripts/automation/sync_dolibarr_changelog.py --dry-run

    # Specify custom paths
    python3 scripts/automation/sync_dolibarr_changelog.py \
        --source CHANGELOG.md \
        --destination src/ChangeLog

    # Verbose output
    python3 scripts/automation/sync_dolibarr_changelog.py --verbose

    # Force sync even if source is older
    python3 scripts/automation/sync_dolibarr_changelog.py --force

EXAMPLES:
    # Basic sync
    python3 scripts/automation/sync_dolibarr_changelog.py

    # Preview what would be synced
    python3 scripts/automation/sync_dolibarr_changelog.py --dry-run --verbose

    # Use in pre-commit hook
    #!/bin/sh
    python3 scripts/automation/sync_dolibarr_changelog.py
    git add src/ChangeLog

GIT HOOK INTEGRATION:
    To automatically sync on commit, create .git/hooks/pre-commit:

    #!/bin/sh
    # Sync Dolibarr changelog
    if [ -f "CHANGELOG.md" ]; then
        python3 scripts/automation/sync_dolibarr_changelog.py
        if [ $? -eq 0 ]; then
            git add src/ChangeLog
        fi
    fi

CI/CD INTEGRATION:
    Add to GitHub Actions workflow:

    - name: Sync Dolibarr changelog
      run: |
        python3 scripts/automation/sync_dolibarr_changelog.py
        if [ -f src/ChangeLog ]; then
          git add src/ChangeLog
          git commit -m "chore: sync changelog to src/ChangeLog" || true
        fi
"""

import argparse
import hashlib
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple


class ChangelogSyncError(Exception):
    """Custom exception for changelog sync errors."""
    pass


class DolibarrChangelogSync:
    """Synchronizes CHANGELOG.md to Dolibarr's src/ChangeLog format."""

    def __init__(
        self,
        source_path: str = "CHANGELOG.md",
        destination_path: str = "src/ChangeLog",
        verbose: bool = False,
        dry_run: bool = False,
        force: bool = False
    ):
        """
        Initialize the changelog synchronizer.

        Args:
            source_path: Path to source CHANGELOG.md (default: CHANGELOG.md)
            destination_path: Path to destination ChangeLog (default: src/ChangeLog)
            verbose: Enable verbose output
            dry_run: Preview changes without modifying files
            force: Force sync even if source is older than destination
        """
        self.source_path = Path(source_path)
        self.destination_path = Path(destination_path)
        self.verbose = verbose
        self.dry_run = dry_run
        self.force = force

    def log(self, message: str, level: str = "INFO") -> None:
        """
        Log a message if verbose mode is enabled.

        Args:
            message: Message to log
            level: Log level (INFO, WARNING, ERROR)
        """
        if self.verbose or level in ["WARNING", "ERROR"]:
            prefix = {
                "INFO": "ℹ",
                "WARNING": "⚠",
                "ERROR": "✗",
                "SUCCESS": "✓"
            }.get(level, "•")
            print(f"{prefix} {message}")

    def validate_source(self) -> None:
        """
        Validate that the source CHANGELOG.md exists and is readable.

        Raises:
            ChangelogSyncError: If source file is invalid
        """
        if not self.source_path.exists():
            raise ChangelogSyncError(
                f"Source file not found: {self.source_path}"
            )

        if not self.source_path.is_file():
            raise ChangelogSyncError(
                f"Source path is not a file: {self.source_path}"
            )

        if not os.access(self.source_path, os.R_OK):
            raise ChangelogSyncError(
                f"Source file is not readable: {self.source_path}"
            )

        self.log(f"Source file validated: {self.source_path}")

    def check_destination_directory(self) -> None:
        """
        Check if destination directory exists, create if needed.

        Raises:
            ChangelogSyncError: If directory cannot be created
        """
        dest_dir = self.destination_path.parent

        if not dest_dir.exists():
            if self.dry_run:
                self.log(
                    f"Would create directory: {dest_dir}",
                    "INFO"
                )
            else:
                try:
                    dest_dir.mkdir(parents=True, exist_ok=True)
                    self.log(f"Created directory: {dest_dir}", "SUCCESS")
                except Exception as e:
                    raise ChangelogSyncError(
                        f"Failed to create directory {dest_dir}: {e}"
                    )
        else:
            self.log(f"Destination directory exists: {dest_dir}")

    def calculate_checksum(self, file_path: Path) -> str:
        """
        Calculate SHA-256 checksum of a file.

        Args:
            file_path: Path to file

        Returns:
            SHA-256 checksum as hexadecimal string
        """
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()

    def files_are_identical(self) -> bool:
        """
        Check if source and destination files are identical.

        Returns:
            True if files have same content, False otherwise
        """
        if not self.destination_path.exists():
            return False

        source_checksum = self.calculate_checksum(self.source_path)
        dest_checksum = self.calculate_checksum(self.destination_path)

        return source_checksum == dest_checksum

    def should_sync(self) -> Tuple[bool, str]:
        """
        Determine if sync should proceed.

        Returns:
            Tuple of (should_sync: bool, reason: str)
        """
        # Check if destination exists
        if not self.destination_path.exists():
            return True, "Destination file does not exist"

        # Check if files are identical
        if self.files_are_identical():
            return False, "Files are already identical"

        # Check modification times
        source_mtime = self.source_path.stat().st_mtime
        dest_mtime = self.destination_path.stat().st_mtime

        if source_mtime > dest_mtime:
            return True, "Source is newer than destination"
        elif self.force:
            return True, "Force sync enabled"
        else:
            return False, "Source is older than destination (use --force to override)"

    def sync_changelog(self) -> bool:
        """
        Perform the changelog synchronization.

        Returns:
            True if sync was performed, False if skipped

        Raises:
            ChangelogSyncError: If sync fails
        """
        # Validate source file
        self.validate_source()

        # Check if sync is needed
        should_sync, reason = self.should_sync()
        self.log(f"Sync decision: {reason}")

        if not should_sync:
            self.log("Sync not needed, skipping", "INFO")
            return False

        # Check/create destination directory
        self.check_destination_directory()

        # Perform sync
        if self.dry_run:
            self.log(
                f"Would copy {self.source_path} -> {self.destination_path}",
                "INFO"
            )
            self.log("Dry run mode: no files modified", "INFO")
            return False
        else:
            try:
                # Copy file
                shutil.copy2(self.source_path, self.destination_path)
                self.log(
                    f"Synced: {self.source_path} -> {self.destination_path}",
                    "SUCCESS"
                )

                # Verify sync
                if self.files_are_identical():
                    self.log("Verification: Files are identical", "SUCCESS")
                    return True
                else:
                    raise ChangelogSyncError("Verification failed: Files differ after sync")

            except Exception as e:
                raise ChangelogSyncError(f"Sync failed: {e}")

    def get_sync_status(self) -> dict:
        """
        Get current sync status information.

        Returns:
            Dictionary with sync status details
        """
        status = {
            "source_exists": self.source_path.exists(),
            "destination_exists": self.destination_path.exists(),
            "source_path": str(self.source_path),
            "destination_path": str(self.destination_path),
            "files_identical": False,
            "source_size": None,
            "destination_size": None,
            "source_modified": None,
            "destination_modified": None,
        }

        if status["source_exists"]:
            stat = self.source_path.stat()
            status["source_size"] = stat.st_size
            status["source_modified"] = datetime.fromtimestamp(stat.st_mtime).isoformat()

        if status["destination_exists"]:
            stat = self.destination_path.stat()
            status["destination_size"] = stat.st_size
            status["destination_modified"] = datetime.fromtimestamp(stat.st_mtime).isoformat()

        if status["source_exists"] and status["destination_exists"]:
            status["files_identical"] = self.files_are_identical()

        return status


def main() -> int:
    """
    Main entry point for the script.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = argparse.ArgumentParser(
        description="Sync CHANGELOG.md to Dolibarr's src/ChangeLog",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic sync
  %(prog)s

  # Preview changes
  %(prog)s --dry-run --verbose

  # Force sync
  %(prog)s --force

  # Custom paths
  %(prog)s --source CHANGELOG.md --destination modules/mymodule/ChangeLog

For more information, see:
  https://github.com/mokoconsulting-tech/MokoStandards
        """
    )

    parser.add_argument(
        "--source",
        default="CHANGELOG.md",
        help="Source CHANGELOG.md path (default: CHANGELOG.md)"
    )

    parser.add_argument(
        "--destination",
        default="src/ChangeLog",
        help="Destination ChangeLog path (default: src/ChangeLog)"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    parser.add_argument(
        "-n", "--dry-run",
        action="store_true",
        help="Preview changes without modifying files"
    )

    parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="Force sync even if source is older than destination"
    )

    parser.add_argument(
        "--status",
        action="store_true",
        help="Show sync status and exit"
    )

    args = parser.parse_args()

    try:
        syncer = DolibarrChangelogSync(
            source_path=args.source,
            destination_path=args.destination,
            verbose=args.verbose,
            dry_run=args.dry_run,
            force=args.force
        )

        if args.status:
            # Show status and exit
            status = syncer.get_sync_status()
            print("Changelog Sync Status:")
            print(f"  Source: {status['source_path']}")
            print(f"    Exists: {status['source_exists']}")
            if status['source_exists']:
                print(f"    Size: {status['source_size']} bytes")
                print(f"    Modified: {status['source_modified']}")
            print(f"  Destination: {status['destination_path']}")
            print(f"    Exists: {status['destination_exists']}")
            if status['destination_exists']:
                print(f"    Size: {status['destination_size']} bytes")
                print(f"    Modified: {status['destination_modified']}")
            if status['source_exists'] and status['destination_exists']:
                print(f"  Files Identical: {status['files_identical']}")
            return 0

        # Perform sync
        synced = syncer.sync_changelog()

        if synced:
            print("✓ Changelog synchronized successfully")
            return 0
        else:
            print("• No sync performed (files already in sync or dry-run mode)")
            return 0

    except ChangelogSyncError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n⚠ Interrupted by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
