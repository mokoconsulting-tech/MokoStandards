#!/usr/bin/env python3
"""Auto-Detect Repository Platform v02.00.00 - Critical Validator Infrastructure.

This script automatically detects repository platform types with confidence scoring
and provides JSON/CLI output for automation workflows.

Platform detection capabilities:
    - Joomla/WaaS components (manifest patterns, version detection)
    - Dolibarr/CRM modules (module.php, core/ structure)
    - Generic repositories (fallback with confidence scoring)

Usage:
    python3 auto_detect_platform.py [--repo-path PATH] [--json] [--verbose] [--cache]

Examples:
    # Auto-detect current repository with JSON output
    python3 auto_detect_platform.py --json
    
    # Detect specific repository with caching
    python3 auto_detect_platform.py --repo-path /path/to/repo --cache --verbose
    
    # JSON output for CI/CD automation
    python3 auto_detect_platform.py --json | jq '.platform_type'

Exit codes:
    0: Success (platform detected successfully)
    1: Detection failed (no platform could be determined)
    2: Configuration error (invalid arguments or paths)
"""

import argparse
import hashlib
import json
import os
import pickle
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# Version
__version__ = "02.00.00"


class PlatformType(Enum):
    """Repository platform types enumeration."""
    
    JOOMLA = "joomla"
    DOLIBARR = "dolibarr"
    GENERIC = "generic"


@dataclass
class DetectionResult:
    """Platform detection result with confidence scoring.
    
    Attributes:
        platform_type: Detected platform type enum value.
        confidence: Confidence score from 0-100.
        indicators: List of detection indicators found.
        metadata: Additional platform-specific metadata.
    """
    
    platform_type: PlatformType
    confidence: int
    indicators: List[str]
    metadata: Dict[str, str]
    
    def to_dict(self) -> Dict[str, any]:
        """Convert detection result to dictionary for JSON serialization.
        
        Returns:
            Dictionary representation with platform_type as string value.
        """
        return {
            "platform_type": self.platform_type.value,
            "confidence": self.confidence,
            "indicators": self.indicators,
            "metadata": self.metadata
        }


class DetectionCache:
    """Simple file-based cache for platform detection results.
    
    Caches detection results based on repository path hash to avoid
    re-scanning the same repository repeatedly.
    """
    
    def __init__(self, cache_dir: Optional[Path] = None) -> None:
        """Initialize detection cache.
        
        Args:
            cache_dir: Directory for cache files. Defaults to ~/.cache/mokostudios.
        """
        if cache_dir is None:
            cache_dir = Path.home() / ".cache" / "mokostudios" / "platform_detection"
        
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_cache_key(self, repo_path: Path) -> str:
        """Generate cache key from repository path.
        
        Args:
            repo_path: Absolute path to repository.
            
        Returns:
            SHA256 hash of the repository path as hex string.
        """
        return hashlib.sha256(str(repo_path).encode()).hexdigest()
    
    def get(self, repo_path: Path) -> Optional[DetectionResult]:
        """Retrieve cached detection result.
        
        Args:
            repo_path: Path to repository.
            
        Returns:
            Cached DetectionResult if available, None otherwise.
        """
        cache_file = self.cache_dir / f"{self._get_cache_key(repo_path)}.pkl"
        
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        except (pickle.PickleError, OSError, EOFError):
            return None
    
    def set(self, repo_path: Path, result: DetectionResult) -> None:
        """Store detection result in cache.
        
        Args:
            repo_path: Path to repository.
            result: Detection result to cache.
        """
        cache_file = self.cache_dir / f"{self._get_cache_key(repo_path)}.pkl"
        
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(result, f)
        except (pickle.PickleError, OSError):
            pass
    
    def clear(self) -> None:
        """Clear all cached detection results."""
        for cache_file in self.cache_dir.glob("*.pkl"):
            try:
                cache_file.unlink()
            except OSError:
                pass


class PlatformDetector:
    """Detects repository platform type with enhanced detection algorithms.
    
    Provides platform detection for Joomla, Dolibarr, and generic repositories
    with confidence scoring and detailed indicators.
    """
    
    def __init__(self, repo_path: Path, use_cache: bool = False) -> None:
        """Initialize platform detector.
        
        Args:
            repo_path: Path to repository to analyze.
            use_cache: Enable caching for performance optimization.
        """
        self.repo_path = Path(repo_path).resolve()
        self.use_cache = use_cache
        self.cache = DetectionCache() if use_cache else None
        
        if not self.repo_path.exists():
            raise ValueError(f"Repository path does not exist: {self.repo_path}")
    
    def detect(self) -> DetectionResult:
        """Detect repository platform type.
        
        Executes platform-specific detection methods in order:
        1. Joomla detection (manifest patterns, directory structure)
        2. Dolibarr detection (module.php, core/ structure)
        3. Generic fallback (confidence-based scoring)
        
        Returns:
            DetectionResult with platform type and confidence score.
        """
        if self.use_cache and self.cache:
            cached_result = self.cache.get(self.repo_path)
            if cached_result:
                return cached_result
        
        joomla_result = self._detect_joomla()
        if joomla_result.confidence >= 50:
            if self.use_cache and self.cache:
                self.cache.set(self.repo_path, joomla_result)
            return joomla_result
        
        dolibarr_result = self._detect_dolibarr()
        if dolibarr_result.confidence >= 50:
            if self.use_cache and self.cache:
                self.cache.set(self.repo_path, dolibarr_result)
            return dolibarr_result
        
        generic_result = self._detect_generic()
        if self.use_cache and self.cache:
            self.cache.set(self.repo_path, generic_result)
        return generic_result
    
    def _detect_joomla(self) -> DetectionResult:
        """Detect Joomla component with enhanced manifest pattern matching.
        
        Detection criteria:
            - XML manifest files with <extension> or <install> root tags
            - Extension type attribute (component, module, plugin, etc.)
            - Joomla version tags in manifest
            - Directory structure (site/, admin/, administrator/)
            - Language directories (language/en-GB/)
        
        Returns:
            DetectionResult for Joomla platform with confidence score.
        """
        confidence = 0
        indicators: List[str] = []
        metadata: Dict[str, str] = {}
        
        manifest_patterns = ["**/*.xml"]
        skip_dirs = {".git", "vendor", "node_modules", ".github"}
        
        for xml_file in self.repo_path.glob("**/*.xml"):
            if any(skip_dir in xml_file.parts for skip_dir in skip_dirs):
                continue
            
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                
                if root.tag in ["extension", "install"]:
                    ext_type = root.get("type", "")
                    
                    if ext_type in ["component", "module", "plugin", "library", "template", "file"]:
                        confidence += 50
                        rel_path = xml_file.relative_to(self.repo_path)
                        indicators.append(f"Joomla manifest: {rel_path} (type={ext_type})")
                        metadata["manifest_file"] = str(rel_path)
                        metadata["extension_type"] = ext_type
                        
                        version_elem = root.find("version")
                        if version_elem is not None and version_elem.text:
                            confidence += 10
                            metadata["version"] = version_elem.text.strip()
                            indicators.append(f"Joomla version tag: {version_elem.text.strip()}")
                        
                        name_elem = root.find("name")
                        if name_elem is not None and name_elem.text:
                            metadata["extension_name"] = name_elem.text.strip()
                        
                        break
                        
            except (ET.ParseError, OSError):
                continue
        
        joomla_dirs = ["site", "admin", "administrator"]
        for dir_name in joomla_dirs:
            if (self.repo_path / dir_name).is_dir():
                confidence += 15
                indicators.append(f"Joomla directory structure: {dir_name}/")
        
        if (self.repo_path / "language" / "en-GB").exists():
            confidence += 10
            indicators.append("Joomla language directory: language/en-GB/")
        
        media_dir = self.repo_path / "media"
        if media_dir.is_dir() and list(media_dir.glob("**/*.css")):
            confidence += 5
            indicators.append("Joomla media directory with assets")
        
        confidence = min(confidence, 100)
        
        return DetectionResult(
            platform_type=PlatformType.JOOMLA,
            confidence=confidence,
            indicators=indicators,
            metadata=metadata
        )
    
    def _detect_dolibarr(self) -> DetectionResult:
        """Detect Dolibarr module with enhanced structure analysis.
        
        Detection criteria:
            - Module descriptor files (mod*.class.php)
            - DolibarrModules class extension patterns
            - core/modules/ directory structure
            - SQL migration files in sql/
            - Class and lib directories
        
        Returns:
            DetectionResult for Dolibarr platform with confidence score.
        """
        confidence = 0
        indicators: List[str] = []
        metadata: Dict[str, str] = {}
        
        descriptor_patterns = ["**/mod*.class.php", "**/core/modules/**/*.php"]
        skip_dirs = {".git", "vendor", "node_modules"}
        
        for pattern in descriptor_patterns:
            for php_file in self.repo_path.glob(pattern):
                if any(skip_dir in php_file.parts for skip_dir in skip_dirs):
                    continue
                
                try:
                    content = php_file.read_text(encoding="utf-8", errors="ignore")
                    
                    dolibarr_patterns = [
                        "extends DolibarrModules",
                        "class mod",
                        "$this->numero",
                        "$this->rights_class",
                        "DolibarrModules",
                        "dol_include_once"
                    ]
                    
                    pattern_matches = sum(1 for p in dolibarr_patterns if p in content)
                    
                    if pattern_matches >= 3:
                        confidence += 60
                        rel_path = php_file.relative_to(self.repo_path)
                        indicators.append(f"Dolibarr module descriptor: {rel_path}")
                        metadata["descriptor_file"] = str(rel_path)
                        
                        if "class mod" in content:
                            import re
                            match = re.search(r'class\s+(mod\w+)', content)
                            if match:
                                metadata["module_class"] = match.group(1)
                        
                        break
                        
                except (OSError, UnicodeDecodeError):
                    continue
        
        dolibarr_dirs = ["core/modules", "sql", "class", "lib", "langs"]
        for dir_name in dolibarr_dirs:
            dir_path = self.repo_path / dir_name
            if dir_path.exists():
                confidence += 8
                indicators.append(f"Dolibarr directory structure: {dir_name}/")
        
        sql_dir = self.repo_path / "sql"
        if sql_dir.is_dir():
            sql_files = list(sql_dir.glob("*.sql"))
            if sql_files:
                confidence += 10
                indicators.append(f"Dolibarr SQL files: {len(sql_files)} migration scripts")
                metadata["sql_files_count"] = str(len(sql_files))
        
        confidence = min(confidence, 100)
        
        return DetectionResult(
            platform_type=PlatformType.DOLIBARR,
            confidence=confidence,
            indicators=indicators,
            metadata=metadata
        )
    
    def _detect_generic(self) -> DetectionResult:
        """Fallback detection for generic repositories with confidence scoring.
        
        Provides baseline detection when no specific platform is identified.
        Confidence score based on standard repository structure indicators.
        
        Returns:
            DetectionResult for generic platform with confidence score.
        """
        confidence = 50
        indicators: List[str] = ["No platform-specific markers found"]
        metadata: Dict[str, str] = {
            "checked_platforms": "Joomla, Dolibarr",
            "detection_reason": "Generic repository fallback"
        }
        
        standard_files = ["README.md", "LICENSE", ".gitignore", "composer.json", "package.json"]
        found_files = []
        
        for file_name in standard_files:
            if (self.repo_path / file_name).exists():
                found_files.append(file_name)
                confidence += 5
        
        if found_files:
            indicators.append(f"Standard repository files: {', '.join(found_files)}")
        
        standard_dirs = ["src", "tests", "docs", ".github"]
        found_dirs = []
        
        for dir_name in standard_dirs:
            if (self.repo_path / dir_name).is_dir():
                found_dirs.append(dir_name)
                confidence += 3
        
        if found_dirs:
            indicators.append(f"Standard directory structure: {', '.join(found_dirs)}")
        
        confidence = min(confidence, 100)
        
        return DetectionResult(
            platform_type=PlatformType.GENERIC,
            confidence=confidence,
            indicators=indicators,
            metadata=metadata
        )


def main() -> int:
    """Main entry point for platform detection CLI.
    
    Returns:
        Exit code: 0 for success, 1 for detection failure, 2 for config error.
    """
    parser = argparse.ArgumentParser(
        description=f"Auto-detect repository platform v{__version__}",
        epilog="For more information, see docs/scripts/validate/"
    )
    parser.add_argument(
        "--repo-path",
        type=str,
        default=".",
        help="Path to repository to analyze (default: current directory)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format for automation"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output with detailed indicators"
    )
    parser.add_argument(
        "--cache",
        action="store_true",
        help="Enable caching for performance (stores results in ~/.cache/mokostudios)"
    )
    parser.add_argument(
        "--clear-cache",
        action="store_true",
        help="Clear detection cache and exit"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    
    args = parser.parse_args()
    
    if args.clear_cache:
        cache = DetectionCache()
        cache.clear()
        if not args.json:
            print("✓ Detection cache cleared")
        return 0
    
    try:
        repo_path = Path(args.repo_path).resolve()
        
        if not repo_path.exists():
            if args.json:
                print(json.dumps({"error": "Repository path does not exist", "path": str(repo_path)}))
            else:
                print(f"✗ Error: Repository path does not exist: {repo_path}", file=sys.stderr)
            return 2
        
        detector = PlatformDetector(repo_path, use_cache=args.cache)
        result = detector.detect()
        
        if args.json:
            output = result.to_dict()
            output["repo_path"] = str(repo_path)
            output["version"] = __version__
            print(json.dumps(output, indent=2))
        else:
            print("=" * 70)
            print(f"Platform Auto-Detection v{__version__}")
            print("=" * 70)
            print()
            print(f"📁 Repository: {repo_path}")
            print(f"🔍 Platform: {result.platform_type.value.upper()}")
            print(f"📊 Confidence: {result.confidence}%")
            print()
            
            if args.verbose and result.indicators:
                print("Detection Indicators:")
                for indicator in result.indicators:
                    print(f"   • {indicator}")
                print()
            
            if args.verbose and result.metadata:
                print("Metadata:")
                for key, value in result.metadata.items():
                    print(f"   {key}: {value}")
                print()
            
            if args.cache:
                print("💾 Result cached for future runs")
                print()
            
            print("=" * 70)
        
        return 0
        
    except ValueError as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"✗ Error: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        if args.json:
            print(json.dumps({"error": f"Unexpected error: {str(e)}"}))
        else:
            print(f"✗ Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
