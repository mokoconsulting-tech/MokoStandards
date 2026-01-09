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

FILE INFORMATION
DEFGROUP: MokoStandards.Scripts
INGROUP: MokoStandards.Release
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /scripts/release/dolibarr_release.py
VERSION: 01.00.00
BRIEF: Script to create release packages for Dolibarr modules
NOTE: Builds ZIP packages following main > dev > rc > version > main release cycle
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Optional, Tuple


class DolibarrReleaser:
    """Creates release packages for Dolibarr modules."""

    def __init__(self, module_dir: Path, version: str, output_dir: Path):
        """
        Initialize the Dolibarr releaser.

        Args:
            module_dir: Path to module directory
            version: Version string (e.g., "1.0.0")
            output_dir: Path to output directory for packages
        """
        self.module_dir = module_dir.resolve()
        self.version = version
        self.output_dir = output_dir.resolve()
        self.module_name = self._detect_module_name()

    def _detect_module_name(self) -> str:
        """Detect module name from module descriptor."""
        modules_dir = self.module_dir / "core" / "modules"
        
        if modules_dir.exists():
            # Find mod*.class.php file
            for php_file in modules_dir.glob("mod*.class.php"):
                # Extract module name from filename (e.g., modMyModule.class.php -> MyModule)
                name = php_file.stem.replace("mod", "")
                if name:
                    return name
        
        # Fallback to directory name
        return self.module_dir.name.replace("MokoDoli", "").replace("dolibarr-", "")

    def update_version(self) -> bool:
        """Update version in module descriptor."""
        modules_dir = self.module_dir / "core" / "modules"
        
        if not modules_dir.exists():
            print(f"Warning: core/modules directory not found", file=sys.stderr)
            return False
        
        updated = False
        for php_file in modules_dir.glob("mod*.class.php"):
            try:
                content = php_file.read_text(encoding='utf-8')
                # Update $this->version = 'x.x.x'
                new_content = re.sub(
                    r"(\$this->version\s*=\s*['\"])[^'\"]*(['\"])",
                    f"\\1{self.version}\\2",
                    content
                )
                
                if new_content != content:
                    php_file.write_text(new_content, encoding='utf-8')
                    print(f"✅ Updated version in {php_file.name}")
                    updated = True
            except Exception as e:
                print(f"Error updating {php_file}: {e}", file=sys.stderr)
                return False
        
        return updated

    def create_package(self) -> Optional[Path]:
        """Create ZIP package for the module."""
        # Create build directory
        build_dir = self.output_dir / "build"
        package_dir = build_dir / "package"
        
        if package_dir.exists():
            shutil.rmtree(package_dir)
        package_dir.mkdir(parents=True, exist_ok=True)

        # Exclusions for development files
        exclusions = [
            'build', 'tests', '.git', '.github', '.gitignore', '.gitattributes',
            'composer.json', 'composer.lock', 'phpunit.xml', 'phpunit.xml.dist',
            'phpcs.xml', 'phpcs.xml.dist', 'phpstan.neon', 'psalm.xml',
            'node_modules', 'package.json', 'package-lock.json', '.DS_Store',
            '__pycache__', '*.pyc', '.pytest_cache', '.vscode', '.idea'
        ]

        print(f"📦 Creating package for {self.module_name} v{self.version}...")

        # Copy files to package directory
        try:
            for item in self.module_dir.iterdir():
                if item.name in exclusions:
                    continue
                
                dest = package_dir / item.name
                if item.is_dir():
                    shutil.copytree(item, dest, ignore=shutil.ignore_patterns(*exclusions))
                else:
                    shutil.copy2(item, dest)
            
            print(f"✅ Copied module files to package directory")
        except Exception as e:
            print(f"Error copying files: {e}", file=sys.stderr)
            return None

        # Create ZIP package
        zip_name = f"{self.module_name}-{self.version}.zip"
        zip_path = build_dir / zip_name

        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(package_dir):
                    # Filter out excluded directories
                    dirs[:] = [d for d in dirs if d not in exclusions]
                    
                    for file in files:
                        file_path = Path(root) / file
                        arcname = file_path.relative_to(package_dir)
                        zipf.write(file_path, arcname)
            
            print(f"✅ Created ZIP package: {zip_name}")
            print(f"   Size: {zip_path.stat().st_size / 1024:.2f} KB")
            
            return zip_path
        except Exception as e:
            print(f"Error creating ZIP: {e}", file=sys.stderr)
            return None

    def generate_checksums(self, zip_path: Path) -> bool:
        """Generate SHA256 and MD5 checksums for the package."""
        try:
            # SHA256
            sha256_path = zip_path.with_suffix(zip_path.suffix + '.sha256')
            subprocess.run(
                ['sha256sum', zip_path.name],
                cwd=zip_path.parent,
                check=True,
                capture_output=True,
                text=True,
                stdout=open(sha256_path, 'w')
            )
            print(f"✅ Generated SHA256 checksum")

            # MD5
            md5_path = zip_path.with_suffix(zip_path.suffix + '.md5')
            subprocess.run(
                ['md5sum', zip_path.name],
                cwd=zip_path.parent,
                check=True,
                capture_output=True,
                text=True,
                stdout=open(md5_path, 'w')
            )
            print(f"✅ Generated MD5 checksum")
            
            return True
        except Exception as e:
            print(f"Error generating checksums: {e}", file=sys.stderr)
            return False

    def release(self, update_version: bool = True) -> bool:
        """Create complete release package."""
        print(f"\n{'='*60}")
        print(f"Dolibarr Module Release")
        print(f"{'='*60}")
        print(f"Module: {self.module_name}")
        print(f"Version: {self.version}")
        print(f"Source: {self.module_dir}")
        print(f"Output: {self.output_dir}")
        print(f"{'='*60}\n")

        # Update version if requested
        if update_version:
            if not self.update_version():
                print("⚠️  Warning: Could not update version in module descriptor")

        # Create package
        zip_path = self.create_package()
        if not zip_path:
            print("❌ Failed to create package", file=sys.stderr)
            return False

        # Generate checksums
        if not self.generate_checksums(zip_path):
            print("⚠️  Warning: Could not generate checksums")

        print(f"\n{'='*60}")
        print(f"✅ Release package created successfully!")
        print(f"{'='*60}")
        print(f"Package: {zip_path}")
        print(f"SHA256: {zip_path}.sha256")
        print(f"MD5: {zip_path}.md5")
        print(f"{'='*60}\n")

        return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Create release package for Dolibarr module',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create release for current directory
  python dolibarr_release.py --version 1.0.0

  # Create release for specific module
  python dolibarr_release.py --module-dir /path/to/module --version 1.0.0

  # Create release without updating version
  python dolibarr_release.py --version 1.0.0 --no-update-version

  # Specify custom output directory
  python dolibarr_release.py --version 1.0.0 --output-dir /tmp/releases
        """
    )
    
    parser.add_argument(
        '--module-dir',
        type=Path,
        default=Path.cwd(),
        help='Path to module directory (default: current directory)'
    )
    parser.add_argument(
        '--version',
        required=True,
        help='Release version (e.g., 1.0.0)'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path.cwd(),
        help='Output directory for packages (default: current directory)'
    )
    parser.add_argument(
        '--no-update-version',
        action='store_true',
        help='Do not update version in module descriptor'
    )

    args = parser.parse_args()

    # Validate version format
    if not re.match(r'^\d+\.\d+\.\d+(-rc\d+)?$', args.version):
        print(f"Error: Invalid version format: {args.version}", file=sys.stderr)
        print(f"Expected format: X.Y.Z or X.Y.Z-rcN", file=sys.stderr)
        sys.exit(1)

    # Create releaser and run
    releaser = DolibarrReleaser(
        module_dir=args.module_dir,
        version=args.version,
        output_dir=args.output_dir
    )

    try:
        success = releaser.release(update_version=not args.no_update_version)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Release cancelled by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
