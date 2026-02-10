#!/usr/bin/env python3
"""
Demo Data Loader for Joomla/Dolibarr (Remote)

This script loads SQL demo data into a MySQL/MariaDB database from a remote system.
It can parse Joomla or Dolibarr configuration files or accept manual server entry.

SECURITY WARNINGS:
    - Only execute SQL files from trusted sources
    - The script validates table prefix input to prevent SQL injection
    - Passwords are securely prompted using getpass (not echoed to terminal)
    - IP whitelisting is available via configuration file
    - Ensure proper database user permissions (avoid using root)

Usage:
    python3 load_demo_data.py --sql demo_data.sql
    python3 load_demo_data.py --sql demo_data.sql --config /path/to/joomla/configuration.php
    python3 load_demo_data.py --sql demo_data.sql --host localhost --user root --database mydb
    python3 load_demo_data.py --help-doc  # Show full documentation

METADATA:
    AUTHOR: Moko Consulting LLC
    COPYRIGHT: 2025-2026 Moko Consulting LLC
    LICENSE: MIT
    VERSION: 03.01.03
    CREATED: 2026-01-29
    UPDATED: 2026-01-30
"""

import argparse
import configparser
import getpass
import os
import re
import socket
import sys
from pathlib import Path
from typing import Optional, Tuple

# Add scripts/lib to path for doc_helper
sys.path.insert(0, str(Path(__file__).parent.parent / 'lib'))
try:
    from doc_helper import add_help_argument, handle_help_flags
    DOC_HELPER_AVAILABLE = True
except ImportError:
    DOC_HELPER_AVAILABLE = False

try:
    import pymysql
    PYMYSQL_AVAILABLE = True
except ImportError:
    PYMYSQL_AVAILABLE = False
    print("WARNING: pymysql not installed. Install with: pip install pymysql")


def get_client_ip() -> str:
    """Get the client's IP address."""
    try:
        # Get external IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "unknown"


def check_ip_whitelist(config_file: str) -> bool:
    """Check if client IP is in whitelist."""
    if not os.path.exists(config_file):
        print(f"WARNING: Config file not found: {config_file}")
        return True  # Allow if no config
    
    config = configparser.ConfigParser()
    config.read(config_file)
    
    if 'security' not in config or 'allowed_ips' not in config['security']:
        return True
    
    allowed_ips = [ip.strip() for ip in config['security']['allowed_ips'].split(',')]
    
    if '*' in allowed_ips:
        return True
    
    client_ip = get_client_ip()
    
    if client_ip in allowed_ips:
        return True
    
    print(f"ERROR: Access denied. Your IP ({client_ip}) is not authorized.")
    return False


def parse_joomla_config(config_path: str) -> Optional[dict]:
    """Parse Joomla configuration.php file."""
    if not os.path.exists(config_path):
        return None
    
    content = Path(config_path).read_text()
    
    config = {}
    
    patterns = {
        'host': r"public \$host = '([^']+)'",
        'user': r"public \$user = '([^']+)'",
        'password': r"public \$password = '([^']+)'",
        'db': r"public \$db = '([^']+)'",
        'dbprefix': r"public \$dbprefix = '([^']*)'",
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, content)
        if match:
            config[key] = match.group(1)
    
    return config if config else None


def parse_dolibarr_config(config_path: str) -> Optional[dict]:
    """Parse Dolibarr conf/conf.php file."""
    if not os.path.exists(config_path):
        return None
    
    content = Path(config_path).read_text()
    
    config = {}
    
    patterns = {
        'host': r"\$dolibarr_main_db_host\s*=\s*['\"]([^'\"]+)",
        'user': r"\$dolibarr_main_db_user\s*=\s*['\"]([^'\"]+)",
        'password': r"\$dolibarr_main_db_pass\s*=\s*['\"]([^'\"]+)",
        'db': r"\$dolibarr_main_db_name\s*=\s*['\"]([^'\"]+)",
        'dbprefix': r"\$dolibarr_main_db_prefix\s*=\s*['\"]([^'\"]*)",
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, content)
        if match:
            config[key] = match.group(1)
    
    return config if config else None


def load_from_ini_config(config_file: str) -> Optional[dict]:
    """Load database config from INI file."""
    if not os.path.exists(config_file):
        return None
    
    config = configparser.ConfigParser()
    config.read(config_file)
    
    if 'database' not in config:
        return None
    
    return {
        'host': config['database'].get('host', 'localhost'),
        'user': config['database'].get('user', ''),
        'password': config['database'].get('password', ''),
        'db': config['database'].get('name', ''),
        'dbprefix': config['database'].get('prefix', ''),
    }


def prompt_for_credentials() -> dict:
    """Prompt user for database credentials."""
    print("\nEnter database connection details:")
    return {
        'host': input("Host [localhost]: ").strip() or 'localhost',
        'user': input("Username: ").strip(),
        'password': getpass.getpass("Password: "),
        'db': input("Database name: ").strip(),
        'dbprefix': input("Table prefix (optional): ").strip(),
    }


def load_sql_file(connection, sql_file: str, db_prefix: str = ''):
    """Load SQL file into database.
    
    SECURITY NOTE: This function executes SQL statements from a file.
    Ensure the SQL file comes from a trusted source. The db_prefix
    parameter is validated to prevent injection attacks.
    
    Args:
        connection: Database connection object
        sql_file: Path to the SQL file to load
        db_prefix: Table prefix to replace {PREFIX} placeholder
        
    Returns:
        bool: True if successful, False otherwise
    """
    if not os.path.exists(sql_file):
        print(f"ERROR: SQL file not found: {sql_file}")
        return False
    
    # Validate db_prefix to prevent SQL injection
    # Only allow alphanumeric characters and underscores
    if db_prefix and not re.match(r'^[a-zA-Z0-9_]*$', db_prefix):
        print(f"ERROR: Invalid table prefix. Only alphanumeric characters and underscores are allowed.")
        return False
    
    print(f"Reading SQL file: {sql_file}")
    content = Path(sql_file).read_text()
    
    # Replace table prefix placeholder
    if db_prefix and '{PREFIX}' in content:
        content = content.replace('{PREFIX}', db_prefix)
        print(f"Replaced {{PREFIX}} with: {db_prefix}")
    
    # Split into statements
    statements = [
        stmt.strip()
        for stmt in content.split(';')
        if stmt.strip() and not stmt.strip().startswith('--')
    ]
    
    print(f"Executing {len(statements)} SQL statements...")
    
    cursor = connection.cursor()
    success = 0
    errors = 0
    
    for statement in statements:
        try:
            cursor.execute(statement)
            success += 1
        except Exception as e:
            errors += 1
            print(f"WARNING: {e}")
    
    connection.commit()
    cursor.close()
    
    print(f"\nDone! Success: {success}, Errors: {errors}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Load SQL demo data into MySQL/MariaDB database',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='For complete documentation, use: --help-doc'
    )
    
    parser.add_argument('--sql', required=True, help='Path to SQL file to load')
    parser.add_argument('--config', help='Path to Joomla/Dolibarr config file')
    parser.add_argument('--ini-config', default='demo_loader_config.ini',
                       help='Path to demo loader config file')
    parser.add_argument('--host', help='Database host')
    parser.add_argument('--port', type=int, default=3306, help='Database port')
    parser.add_argument('--user', help='Database user')
    parser.add_argument('--password', help='Database password')
    parser.add_argument('--database', help='Database name')
    parser.add_argument('--prefix', help='Table prefix')
    parser.add_argument('--no-ip-check', action='store_true',
                       help='Skip IP whitelist check')
    
    # Add documentation help flags
    if DOC_HELPER_AVAILABLE:
        add_help_argument(parser, __file__, 'demo/demo-data-loader.md')
    
    args = parser.parse_args()
    
    # Handle help flags
    if DOC_HELPER_AVAILABLE and handle_help_flags(args, __file__, 'demo/demo-data-loader.md'):
        return 0
    
    if not PYMYSQL_AVAILABLE:
        print("ERROR: pymysql module is required. Install with: pip install pymysql")
        return 1
    
    # Check IP whitelist
    if not args.no_ip_check and not check_ip_whitelist(args.ini_config):
        return 1
    
    # Determine database configuration
    db_config = None
    source = None
    
    # Try command-line arguments first
    if args.host and args.user and args.database:
        db_config = {
            'host': args.host,
            'user': args.user,
            'password': args.password or '',
            'db': args.database,
            'dbprefix': args.prefix or '',
        }
        source = "command-line"
    
    # Try specified config file
    elif args.config:
        if 'configuration.php' in args.config:
            db_config = parse_joomla_config(args.config)
            source = "Joomla"
        elif 'conf.php' in args.config:
            db_config = parse_dolibarr_config(args.config)
            source = "Dolibarr"
    
    # Try INI config file
    if not db_config:
        db_config = load_from_ini_config(args.ini_config)
        if db_config:
            source = "INI config"
    
    # Prompt for credentials
    if not db_config:
        db_config = prompt_for_credentials()
        source = "manual entry"
    
    if not db_config or not db_config.get('user'):
        print("ERROR: Database configuration incomplete")
        return 1
    
    print(f"Using database configuration from: {source}")
    
    # Connect to database
    try:
        connection = pymysql.connect(
            host=db_config['host'],
            port=args.port,
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['db'],
            charset='utf8mb4'
        )
        
        print(f"Connected to database: {db_config['db']}")
        
        # Load SQL file
        success = load_sql_file(connection, args.sql, db_config.get('dbprefix', ''))
        
        connection.close()
        
        return 0 if success else 1
        
    except Exception as e:
        # Sanitize error message to prevent password leakage
        error_msg = str(e)
        # Remove password from error message using regex
        sanitized_msg = re.sub(
            r"password['\"]?\s*[:=]\s*['\"]?[^'\"}\s,)]+",
            "password='***'",
            error_msg,
            flags=re.IGNORECASE
        )
        print(f"ERROR: Database connection failed: {sanitized_msg}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
