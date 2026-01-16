#!/usr/bin/env python3
"""
Auto-Detect Repository Platform and Validate

This script automatically detects whether a repository is a:
- Joomla/WaaS component (by finding Joomla manifest files)
- Dolibarr/CRM module (by finding Dolibarr module structure)
- Generic repository (fallback)

Then loads the appropriate schema from schemas/structures/ and validates
the repository structure, generating documentation files for any issues found.

Usage:
    python3 auto_detect_platform.py [--repo-path PATH] [--output-dir DIR] [--verbose]

Examples:
    # Auto-detect current repository
    python3 auto_detect_platform.py
    
    # Auto-detect specific repository
    python3 auto_detect_platform.py --repo-path /path/to/repo
    
    # Generate documentation files in specific directory
    python3 auto_detect_platform.py --output-dir ./validation-reports

Exit codes:
    0: Success (platform detected and validation passed)
    1: Validation errors found
    2: Validation warnings only
    3: Platform detection failed or configuration error
"""

import sys
import os
import argparse
import xml.etree.ElementTree as ET
import json
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from datetime import datetime
import subprocess


class PlatformType:
    """Repository platform types"""
    JOOMLA = "joomla"
    DOLIBARR = "dolibarr"
    GENERIC = "generic"


class PlatformDetector:
    """Detects the platform type of a repository"""
    
    def __init__(self, repo_path: str = "."):
        """
        Initialize platform detector
        
        Args:
            repo_path: Path to repository to analyze
        """
        self.repo_path = Path(repo_path).resolve()
        
    def detect(self) -> Tuple[str, Dict[str, any]]:
        """
        Detect the platform type of the repository
        
        Returns:
            Tuple of (platform_type, detection_details)
        """
        # Check for Joomla manifest
        joomla_result = self._detect_joomla()
        if joomla_result:
            return PlatformType.JOOMLA, joomla_result
        
        # Check for Dolibarr module structure
        dolibarr_result = self._detect_dolibarr()
        if dolibarr_result:
            return PlatformType.DOLIBARR, dolibarr_result
        
        # Default to generic
        return PlatformType.GENERIC, {
            "reason": "No platform-specific markers found",
            "checked": ["Joomla manifest", "Dolibarr module structure"]
        }
    
    def _detect_joomla(self) -> Optional[Dict[str, any]]:
        """
        Detect Joomla component by looking for manifest files
        
        Joomla components typically have:
        - A component XML manifest file (e.g., com_example.xml or componentname.xml)
        - site/ and admin/ directories
        - manifest.xml in root or subdirectories
        
        Returns:
            Detection details if Joomla component found, None otherwise
        """
        detection_info = {
            "platform": "Joomla/WaaS Component",
            "confidence": 0,
            "indicators": []
        }
        
        # Look for Joomla-specific XML manifest patterns
        manifest_patterns = [
            "**/*.xml",
            "**/manifest.xml",
            "**/com_*.xml",
            "**/mod_*.xml",
            "**/plg_*.xml"
        ]
        
        for pattern in manifest_patterns:
            for xml_file in self.repo_path.glob(pattern):
                if xml_file.name in ['.git', 'vendor', 'node_modules']:
                    continue
                    
                try:
                    tree = ET.parse(xml_file)
                    root = tree.getroot()
                    
                    # Check for Joomla-specific XML elements
                    if root.tag in ['extension', 'install']:
                        # Check for type attribute (component, module, plugin)
                        ext_type = root.get('type', '')
                        if ext_type in ['component', 'module', 'plugin', 'library', 'template']:
                            detection_info["confidence"] += 50
                            detection_info["indicators"].append(f"Joomla manifest: {xml_file.relative_to(self.repo_path)} (type={ext_type})")
                            detection_info["manifest_file"] = str(xml_file.relative_to(self.repo_path))
                            detection_info["extension_type"] = ext_type
                        
                        # Check for Joomla version
                        for child in root:
                            if child.tag in ['version', 'joomla']:
                                detection_info["confidence"] += 10
                                
                except (ET.ParseError, OSError):
                    pass
        
        # Check for Joomla directory structure
        joomla_dirs = ['site', 'admin', 'administrator']
        for dir_name in joomla_dirs:
            if (self.repo_path / dir_name).is_dir():
                detection_info["confidence"] += 15
                detection_info["indicators"].append(f"Joomla directory: {dir_name}/")
        
        # Check for Joomla-specific files
        joomla_files = ['index.html', 'language/en-GB']
        for file_pattern in joomla_files:
            if list(self.repo_path.glob(f"**/{file_pattern}")):
                detection_info["confidence"] += 5
        
        # Require at least 50% confidence
        if detection_info["confidence"] >= 50:
            return detection_info
        
        return None
    
    def _detect_dolibarr(self) -> Optional[Dict[str, any]]:
        """
        Detect Dolibarr module by looking for module structure
        
        Dolibarr modules typically have:
        - A core/modules/ directory structure
        - Module descriptor files (modModule.class.php)
        - Dolibarr-specific PHP patterns
        - SQL files in sql/ directory
        
        Returns:
            Detection details if Dolibarr module found, None otherwise
        """
        detection_info = {
            "platform": "Dolibarr/CRM Module",
            "confidence": 0,
            "indicators": []
        }
        
        # Look for Dolibarr module descriptor files
        descriptor_patterns = [
            "**/mod*.class.php",
            "**/core/modules/**/*.php"
        ]
        
        for pattern in descriptor_patterns:
            for php_file in self.repo_path.glob(pattern):
                if any(skip in str(php_file) for skip in ['.git', 'vendor', 'node_modules']):
                    continue
                    
                try:
                    content = php_file.read_text(encoding='utf-8', errors='ignore')
                    
                    # Check for Dolibarr-specific patterns
                    dolibarr_patterns = [
                        'extends DolibarrModules',
                        'class mod',
                        '$this->numero',
                        '$this->rights_class',
                        'DolibarrModules',
                        'dol_include_once'
                    ]
                    
                    pattern_matches = sum(1 for p in dolibarr_patterns if p in content)
                    if pattern_matches >= 2:
                        detection_info["confidence"] += 60
                        detection_info["indicators"].append(f"Dolibarr module descriptor: {php_file.relative_to(self.repo_path)}")
                        detection_info["descriptor_file"] = str(php_file.relative_to(self.repo_path))
                        break
                        
                except (OSError, UnicodeDecodeError):
                    pass
        
        # Check for Dolibarr directory structure
        dolibarr_dirs = ['core/modules', 'sql', 'class', 'lib', 'langs']
        for dir_name in dolibarr_dirs:
            if (self.repo_path / dir_name).exists():
                detection_info["confidence"] += 10
                detection_info["indicators"].append(f"Dolibarr directory: {dir_name}/")
        
        # Check for Dolibarr-specific SQL files
        if (self.repo_path / 'sql').is_dir():
            sql_files = list((self.repo_path / 'sql').glob('*.sql'))
            if sql_files:
                detection_info["confidence"] += 10
                detection_info["indicators"].append(f"Dolibarr SQL files: {len(sql_files)} files in sql/")
        
        # Require at least 50% confidence
        if detection_info["confidence"] >= 50:
            return detection_info
        
        return None


class ValidationDocumentationGenerator:
    """Generates documentation files from validation results"""
    
    def __init__(self, output_dir: str = "./validation-reports"):
        """
        Initialize documentation generator
        
        Args:
            output_dir: Directory to write documentation files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(self, platform: str, detection_details: Dict, validation_output: str, exit_code: int):
        """
        Generate documentation files for validation results
        
        Args:
            platform: Detected platform type
            detection_details: Platform detection details
            validation_output: Output from validation script
            exit_code: Exit code from validation
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Generate detection report
        self._generate_detection_report(platform, detection_details, timestamp)
        
        # Generate validation report
        self._generate_validation_report(platform, validation_output, exit_code, timestamp)
        
        # Generate summary
        self._generate_summary(platform, detection_details, exit_code, timestamp)
    
    def _generate_detection_report(self, platform: str, details: Dict, timestamp: str):
        """Generate platform detection report"""
        report_file = self.output_dir / f"detection_report_{timestamp}.md"
        
        content = f"""# Platform Detection Report

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Repository:** {os.getcwd()}

## Detection Results

**Detected Platform:** {platform.upper()}

### Confidence: {details.get('confidence', 'N/A')}%

### Detection Indicators

"""
        
        if 'indicators' in details:
            for indicator in details['indicators']:
                content += f"- ✓ {indicator}\n"
        
        if 'manifest_file' in details:
            content += f"\n**Manifest File:** `{details['manifest_file']}`\n"
        if 'extension_type' in details:
            content += f"**Extension Type:** {details['extension_type']}\n"
        if 'descriptor_file' in details:
            content += f"\n**Descriptor File:** `{details['descriptor_file']}`\n"
        
        content += f"""

## Schema Mapping

Based on detection, the following schema will be used:

- **Platform:** {platform}
- **Schema File:** `schemas/structures/{self._get_schema_filename(platform)}`

## Next Steps

1. Review the validation report for any issues
2. Address any ERRORS (required items missing)
3. Consider addressing WARNINGS (suggested items missing)
4. Commit any fixes and re-run validation

---
*Generated by auto_detect_platform.py*
"""
        
        report_file.write_text(content)
        print(f"✓ Detection report: {report_file}")
    
    def _generate_validation_report(self, platform: str, output: str, exit_code: int, timestamp: str):
        """Generate validation report"""
        report_file = self.output_dir / f"validation_report_{timestamp}.md"
        
        status = "✓ PASSED" if exit_code == 0 else "✗ FAILED" if exit_code == 1 else "⚠ WARNINGS"
        
        content = f"""# Repository Validation Report

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Platform:** {platform.upper()}
**Status:** {status}
**Exit Code:** {exit_code}

## Validation Output

```
{output}
```

## Status Codes

- **Exit Code 0:** All validations passed
- **Exit Code 1:** Validation errors (required items missing or not-allowed items present)
- **Exit Code 2:** Validation warnings (suggested items missing)
- **Exit Code 3:** Configuration error

---
*Generated by auto_detect_platform.py*
"""
        
        report_file.write_text(content)
        print(f"✓ Validation report: {report_file}")
    
    def _generate_summary(self, platform: str, details: Dict, exit_code: int, timestamp: str):
        """Generate summary report"""
        summary_file = self.output_dir / f"SUMMARY_{timestamp}.md"
        
        status_emoji = "✓" if exit_code == 0 else "✗" if exit_code == 1 else "⚠"
        
        content = f"""# Validation Summary

{status_emoji} **Overall Status:** {"PASSED" if exit_code == 0 else "FAILED" if exit_code == 1 else "WARNINGS"}

## Quick Facts

| Item | Value |
|------|-------|
| **Platform** | {platform.upper()} |
| **Confidence** | {details.get('confidence', 'N/A')}% |
| **Exit Code** | {exit_code} |
| **Timestamp** | {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} |

## Generated Reports

- `detection_report_{timestamp}.md` - Platform detection details
- `validation_report_{timestamp}.md` - Full validation output
- `SUMMARY_{timestamp}.md` - This file

## Action Items

"""
        
        if exit_code == 0:
            content += "✓ No action required - all validations passed!\n"
        elif exit_code == 1:
            content += """✗ **ERRORS FOUND** - Action required:
1. Review validation_report for specific errors
2. Add missing required files/directories
3. Remove not-allowed files/directories
4. Re-run validation after fixes
"""
        elif exit_code == 2:
            content += """⚠ **WARNINGS FOUND** - Recommended actions:
1. Review validation_report for suggestions
2. Consider adding suggested files/directories
3. Improve repository health score
"""
        else:
            content += "✗ **CONFIGURATION ERROR** - Check validation_report for details\n"
        
        content += "\n---\n*Generated by auto_detect_platform.py*\n"
        
        summary_file.write_text(content)
        print(f"✓ Summary: {summary_file}")
    
    def _get_schema_filename(self, platform: str) -> str:
        """Get schema filename for platform"""
        schema_map = {
            PlatformType.JOOMLA: "waas-component.xml",
            PlatformType.DOLIBARR: "crm-module.xml",
            PlatformType.GENERIC: "default-repository.xml"
        }
        return schema_map.get(platform, "default-repository.xml")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Auto-detect repository platform and validate structure"
    )
    parser.add_argument(
        "--repo-path",
        default=".",
        help="Path to repository to analyze (default: current directory)"
    )
    parser.add_argument(
        "--output-dir",
        default="./validation-reports",
        help="Directory for documentation output (default: ./validation-reports)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--schema-dir",
        default=None,
        help="Directory containing schema files (default: auto-detect)"
    )
    
    args = parser.parse_args()
    
    # Find schema directory
    if args.schema_dir:
        schema_dir = Path(args.schema_dir)
    else:
        # Try to find schema directory relative to script location
        script_dir = Path(__file__).parent.parent.parent
        schema_dir = script_dir / "schemas" / "structures"
        
        if not schema_dir.exists():
            # Try relative to current directory
            schema_dir = Path("schemas/structures")
    
    if not schema_dir.exists():
        print(f"✗ Error: Schema directory not found: {schema_dir}", file=sys.stderr)
        print("  Use --schema-dir to specify the location", file=sys.stderr)
        return 3
    
    print("=" * 70)
    print("Repository Platform Auto-Detection and Validation")
    print("=" * 70)
    print()
    
    # Detect platform
    print(f"📁 Analyzing repository: {Path(args.repo_path).resolve()}")
    print()
    
    detector = PlatformDetector(args.repo_path)
    platform, details = detector.detect()
    
    print(f"🔍 Platform Detection Results:")
    print(f"   Platform: {platform.upper()}")
    if 'confidence' in details:
        print(f"   Confidence: {details['confidence']}%")
    if args.verbose and 'indicators' in details:
        print(f"   Indicators:")
        for indicator in details['indicators']:
            print(f"      - {indicator}")
    print()
    
    # Determine schema file
    schema_map = {
        PlatformType.JOOMLA: "waas-component.xml",
        PlatformType.DOLIBARR: "crm-module.xml",
        PlatformType.GENERIC: "default-repository.xml"
    }
    schema_file = schema_dir / schema_map[platform]
    
    if not schema_file.exists():
        print(f"✗ Error: Schema file not found: {schema_file}", file=sys.stderr)
        return 3
    
    print(f"📋 Using schema: {schema_file.name}")
    print()
    
    # Run validation
    print("🔬 Running validation...")
    print("-" * 70)
    
    validator_script = Path(__file__).parent / "validate_structure_v2.py"
    if not validator_script.exists():
        print(f"✗ Error: Validator script not found: {validator_script}", file=sys.stderr)
        return 3
    
    try:
        result = subprocess.run(
            [sys.executable, str(validator_script), "--schema", str(schema_file), "--repo-path", args.repo_path],
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        exit_code = result.returncode
        
    except Exception as e:
        print(f"✗ Error running validation: {e}", file=sys.stderr)
        exit_code = 3
        result = type('obj', (object,), {'stdout': str(e), 'stderr': ''})()
    
    print("-" * 70)
    print()
    
    # Generate documentation
    print("📄 Generating documentation files...")
    doc_generator = ValidationDocumentationGenerator(args.output_dir)
    doc_generator.generate(platform, details, result.stdout, exit_code)
    print()
    
    # Final status
    print("=" * 70)
    if exit_code == 0:
        print("✓ SUCCESS: All validations passed!")
    elif exit_code == 1:
        print("✗ FAILURE: Validation errors found (see reports)")
    elif exit_code == 2:
        print("⚠ WARNING: Validation warnings found (see reports)")
    else:
        print("✗ ERROR: Configuration or execution error")
    print("=" * 70)
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
