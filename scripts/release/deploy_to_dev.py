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
DEFGROUP: MokoStandards.Release
INGROUP: MokoStandards.Scripts
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /scripts/release/deploy_to_dev.py
VERSION: 01.00.00
BRIEF: Deploy src directory to development server via FTP/SFTP
"""

import argparse
import ftplib
import os
import sys
from pathlib import Path
from typing import Optional

try:
    import paramiko
except ImportError:
    paramiko = None


def deploy_ftp(host: str, user: str, password: str, remote_path: str, 
               local_path: str, port: int = 21, use_tls: bool = False) -> bool:
    """Deploy files via FTP or FTPS."""
    try:
        # Connect to FTP server
        if use_tls:
            ftp = ftplib.FTP_TLS()
            print(f"Connecting to {host}:{port} (FTPS)...")
            ftp.connect(host, port)
            ftp.login(user, password)
            ftp.prot_p()  # Enable data encryption
        else:
            ftp = ftplib.FTP()
            print(f"Connecting to {host}:{port} (FTP)...")
            ftp.connect(host, port)
            ftp.login(user, password)
        
        print(f"✓ Connected to {host}")
        
        # Change to remote directory (create if it doesn't exist)
        try:
            ftp.cwd(remote_path)
        except ftplib.error_perm:
            print(f"Creating remote directory: {remote_path}")
            # Try to create parent directories recursively
            parts = remote_path.strip('/').split('/')
            current = ''
            for part in parts:
                current += '/' + part
                try:
                    ftp.cwd(current)
                except ftplib.error_perm:
                    ftp.mkd(current)
                    ftp.cwd(current)
        
        print(f"✓ Changed to remote directory: {remote_path}")
        
        # Upload files recursively
        local_path_obj = Path(local_path)
        if not local_path_obj.exists():
            print(f"✗ Local path does not exist: {local_path}", file=sys.stderr)
            return False
        
        uploaded_count = 0
        
        def upload_dir(local_dir: Path, remote_dir: str = ''):
            nonlocal uploaded_count
            
            for item in local_dir.iterdir():
                if item.name.startswith('.'):
                    continue  # Skip hidden files
                
                item_remote_path = f"{remote_dir}/{item.name}" if remote_dir else item.name
                
                if item.is_file():
                    print(f"  Uploading: {item.relative_to(local_path_obj)} → {item_remote_path}")
                    with open(item, 'rb') as f:
                        ftp.storbinary(f'STOR {item_remote_path}', f)
                    uploaded_count += 1
                elif item.is_dir():
                    # Create remote directory if it doesn't exist
                    try:
                        ftp.cwd(item_remote_path)
                        ftp.cwd('..')
                    except ftplib.error_perm:
                        ftp.mkd(item_remote_path)
                    
                    # Recursively upload directory contents
                    upload_dir(item, item_remote_path)
        
        print(f"\nUploading files from {local_path}...")
        upload_dir(local_path_obj)
        
        print(f"\n✓ Successfully uploaded {uploaded_count} files")
        ftp.quit()
        return True
        
    except Exception as e:
        print(f"✗ FTP deployment failed: {e}", file=sys.stderr)
        return False


def deploy_sftp(host: str, user: str, password: Optional[str], remote_path: str,
                local_path: str, port: int = 22, key_file: Optional[str] = None) -> bool:
    """Deploy files via SFTP."""
    if paramiko is None:
        print("✗ SFTP requires paramiko library. Install with: pip install paramiko", 
              file=sys.stderr)
        return False
    
    try:
        # Setup SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        print(f"Connecting to {host}:{port} (SFTP)...")
        
        # Connect with key or password
        if key_file:
            key = paramiko.RSAKey.from_private_key_file(key_file)
            ssh.connect(host, port=port, username=user, pkey=key)
        else:
            ssh.connect(host, port=port, username=user, password=password)
        
        print(f"✓ Connected to {host}")
        
        # Open SFTP session
        sftp = ssh.open_sftp()
        
        # Create remote directory if it doesn't exist
        def mkdir_p(sftp_client, remote_directory):
            dirs = []
            dir_path = str(remote_directory)
            while len(dir_path) > 1:
                try:
                    sftp_client.stat(dir_path)
                    break
                except IOError:
                    dirs.append(dir_path)
                    dir_path = str(Path(dir_path).parent)
            
            for dir_path in reversed(dirs):
                sftp_client.mkdir(dir_path)
        
        mkdir_p(sftp, remote_path)
        print(f"✓ Ensured remote directory exists: {remote_path}")
        
        # Upload files recursively
        local_path_obj = Path(local_path)
        if not local_path_obj.exists():
            print(f"✗ Local path does not exist: {local_path}", file=sys.stderr)
            return False
        
        uploaded_count = 0
        
        def upload_dir(local_dir: Path, remote_dir: str):
            nonlocal uploaded_count
            
            for item in local_dir.iterdir():
                if item.name.startswith('.'):
                    continue  # Skip hidden files
                
                item_remote_path = str(Path(remote_dir) / item.name)
                
                if item.is_file():
                    print(f"  Uploading: {item.relative_to(local_path_obj)} → {item_remote_path}")
                    sftp.put(str(item), item_remote_path)
                    uploaded_count += 1
                elif item.is_dir():
                    # Create remote directory
                    try:
                        sftp.stat(item_remote_path)
                    except IOError:
                        sftp.mkdir(item_remote_path)
                    
                    # Recursively upload directory contents
                    upload_dir(item, item_remote_path)
        
        print(f"\nUploading files from {local_path}...")
        upload_dir(local_path_obj, remote_path)
        
        print(f"\n✓ Successfully uploaded {uploaded_count} files")
        
        sftp.close()
        ssh.close()
        return True
        
    except Exception as e:
        print(f"✗ SFTP deployment failed: {e}", file=sys.stderr)
        return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Deploy src directory to development server via FTP/SFTP'
    )
    
    parser.add_argument('--host', required=True, help='FTP/SFTP host')
    parser.add_argument('--user', required=True, help='FTP/SFTP username')
    parser.add_argument('--password', help='FTP/SFTP password')
    parser.add_argument('--remote-path', required=True, help='Remote deployment path')
    parser.add_argument('--local-path', default='src', help='Local path to upload (default: src)')
    parser.add_argument('--port', type=int, help='FTP/SFTP port (default: 21 for FTP, 22 for SFTP)')
    parser.add_argument('--protocol', choices=['ftp', 'ftps', 'sftp'], default='sftp',
                        help='Transfer protocol (default: sftp)')
    parser.add_argument('--key-file', help='SSH private key file for SFTP')
    
    args = parser.parse_args()
    
    # Determine default port based on protocol
    if args.port is None:
        if args.protocol in ['ftp', 'ftps']:
            args.port = 21
        else:
            args.port = 22
    
    # Validate local path exists
    if not os.path.exists(args.local_path):
        print(f"✗ Local path does not exist: {args.local_path}", file=sys.stderr)
        sys.exit(1)
    
    print("=" * 60)
    print("Development Server Deployment")
    print("=" * 60)
    print(f"Protocol:     {args.protocol.upper()}")
    print(f"Host:         {args.host}:{args.port}")
    print(f"User:         {args.user}")
    print(f"Local Path:   {args.local_path}")
    print(f"Remote Path:  {args.remote_path}")
    print("=" * 60)
    print()
    
    # Deploy based on protocol
    if args.protocol == 'sftp':
        success = deploy_sftp(
            args.host, args.user, args.password, args.remote_path,
            args.local_path, args.port, args.key_file
        )
    else:
        use_tls = args.protocol == 'ftps'
        success = deploy_ftp(
            args.host, args.user, args.password, args.remote_path,
            args.local_path, args.port, use_tls
        )
    
    if success:
        print("\n" + "=" * 60)
        print("✓ Deployment completed successfully!")
        print("=" * 60)
        sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("✗ Deployment failed!")
        print("=" * 60)
        sys.exit(1)


if __name__ == '__main__':
    main()
