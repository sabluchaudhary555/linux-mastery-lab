#!/usr/bin/env python3
"""
Package Installation History Tracker
Tracks and analyzes package installation history across different package managers
"""

import subprocess
import sqlite3
import os
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import json


class PackageHistoryTracker:
    def __init__(self):
        self.db_path = Path.home() / '.package_history.db'
        self.distro = self.detect_distro()
        self.init_database()

    def detect_distro(self):
        """Detect Linux distribution"""
        if os.path.exists('/etc/debian_version'):
            return 'debian'
        elif os.path.exists('/etc/redhat-release'):
            return 'redhat'
        elif os.path.exists('/etc/arch-release'):
            return 'arch'
        elif os.path.exists('/etc/SuSE-release') or os.path.exists('/etc/SUSE-brand'):
            return 'suse'
        else:
            return 'unknown'

    def init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS package_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                action TEXT,
                package_name TEXT,
                version TEXT,
                dependencies TEXT,
                user TEXT,
                distro TEXT,
                size_kb INTEGER
            )
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_package_name 
            ON package_history(package_name)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON package_history(timestamp)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_action 
            ON package_history(action)
        ''')

        conn.commit()
        conn.close()

    def parse_debian_history(self):
        """Parse APT history logs"""
        history_log = '/var/log/apt/history.log'

        if not os.path.exists(history_log):
            print(f"Log file not found: {history_log}")
            return []

        entries = []
        current_entry = {}

        try:
            with open(history_log, 'r') as f:
                for line in f:
                    line = line.strip()

                    if line.startswith('Start-Date:'):
                        if current_entry:
                            entries.append(current_entry)
                        current_entry = {
                            'timestamp': line.split('Start-Date: ')[1],
                            'distro': 'debian'
                        }

                    elif line.startswith('Commandline:'):
                        current_entry['commandline'] = line.split('Commandline: ')[1]

                    elif line.startswith('Install:'):
                        packages = line.split('Install: ')[1]
                        current_entry['action'] = 'install'
                        current_entry['packages'] = self._parse_debian_packages(packages)

                    elif line.startswith('Upgrade:'):
                        packages = line.split('Upgrade: ')[1]
                        current_entry['action'] = 'upgrade'
                        current_entry['packages'] = self._parse_debian_packages(packages)

                    elif line.startswith('Remove:'):
                        packages = line.split('Remove: ')[1]
                        current_entry['action'] = 'remove'
                        current_entry['packages'] = self._parse_debian_packages(packages)

                if current_entry:
                    entries.append(current_entry)

        except PermissionError:
            print("Permission denied. Try running with sudo.")
            return []

        return entries

    def _parse_debian_packages(self, package_string):
        """Parse package string from apt history"""
        packages = []
        for pkg in package_string.split('), '):
            match = re.match(r'(.+?):(.+?) \((.+?)(?:, (.+?))?\)', pkg + ')')
            if match:
                name = match.group(1)
                arch = match.group(2)
                version = match.group(3)
                packages.append({
                    'name': name,
                    'version': version,
                    'arch': arch
                })
        return packages

    def parse_dnf_history(self):
        """Parse DNF/YUM history"""
        try:
            result = subprocess.run(['dnf', 'history', 'list'],
                                    capture_output=True, text=True)

            entries = []
            for line in result.stdout.split('\n')[2:]:  # Skip header
                if not line.strip():
                    continue

                parts = line.split()
                if len(parts) >= 5:
                    history_id = parts[0]

                    # Get detailed info for this transaction
                    detail_result = subprocess.run(
                        ['dnf', 'history', 'info', history_id],
                        capture_output=True, text=True
                    )

                    entry = self._parse_dnf_detail(detail_result.stdout)
                    if entry:
                        entries.append(entry)

            return entries

        except Exception as e:
            print(f"Error parsing DNF history: {str(e)}")
            return []

    def _parse_dnf_detail(self, detail_output):
        """Parse detailed DNF history entry"""
        entry = {'distro': 'redhat', 'packages': []}

        for line in detail_output.split('\n'):
            if 'Begin time' in line:
                entry['timestamp'] = line.split(':', 1)[1].strip()
            elif 'Command Line' in line:
                entry['commandline'] = line.split(':', 1)[1].strip()
            elif line.strip().startswith('Install'):
                entry['action'] = 'install'
                pkg_match = re.search(r'(\S+)-(\S+)\.', line)
                if pkg_match:
                    entry['packages'].append({
                        'name': pkg_match.group(1),
                        'version': pkg_match.group(2)
                    })
            elif line.strip().startswith('Upgrade'):
                entry['action'] = 'upgrade'
            elif line.strip().startswith('Erase'):
                entry['action'] = 'remove'

        return entry if entry['packages'] else None

    def parse_pacman_history(self):
        """Parse Pacman log"""
        log_file = '/var/log/pacman.log'

        if not os.path.exists(log_file):
            print(f"Log file not found: {log_file}")
            return []

        entries = []

        try:
            with open(log_file, 'r') as f:
                for line in f:
                    # Match: [2024-01-15T10:30:45+0000] [ALPM] installed firefox (120.0-1)
                    match = re.match(
                        r'\[(.+?)\] \[ALPM\] (installed|upgraded|removed) (.+?) \((.+?)\)',
                        line
                    )

                    if match:
                        entries.append({
                            'timestamp': match.group(1),
                            'action': match.group(2),
                            'packages': [{
                                'name': match.group(3),
                                'version': match.group(4)
                            }],
                            'distro': 'arch'
                        })

        except PermissionError:
            print("Permission denied. Try running with sudo.")
            return []

        return entries

    def parse_zypper_history(self):
        """Parse Zypper history"""
        history_dir = '/var/log/zypp/history'

        if not os.path.exists(history_dir):
            print(f"History directory not found: {history_dir}")
            return []

        entries = []

        try:
            for filename in os.listdir(history_dir):
                filepath = os.path.join(history_dir, filename)

                with open(filepath, 'r') as f:
                    for line in f:
                        if line.startswith('#'):
                            continue

                        # Format: 2024-01-15 10:30:45|install|firefox|120.0-1|x86_64|user
                        parts = line.strip().split('|')
                        if len(parts) >= 4:
                            entries.append({
                                'timestamp': parts[0],
                                'action': parts[1],
                                'packages': [{
                                    'name': parts[2],
                                    'version': parts[3]
                                }],
                                'distro': 'suse',
                                'user': parts[5] if len(parts) > 5 else 'unknown'
                            })

        except PermissionError:
            print("Permission denied. Try running with sudo.")
            return []

        return entries

    def import_history(self):
        """Import history from system logs into database"""
        print(f"Importing package history for {self.distro} system...")

        if self.distro == 'debian':
            entries = self.parse_debian_history()
        elif self.distro == 'redhat':
            entries = self.parse_dnf_history()
        elif self.distro == 'arch':
            entries = self.parse_pacman_history()
        elif self.distro == 'suse':
            entries = self.parse_zypper_history()
        else:
            print("Unsupported distribution")
            return

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        imported = 0
        for entry in entries:
            for package in entry.get('packages', []):
                cursor.execute('''
                    INSERT INTO package_history 
                    (timestamp, action, package_name, version, dependencies, user, distro, size_kb)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    entry.get('timestamp', ''),
                    entry.get('action', ''),
                    package.get('name', ''),
                    package.get('version', ''),
                    json.dumps(package.get('dependencies', [])),
                    entry.get('user', os.getenv('USER')),
                    entry.get('distro', self.distro),
                    package.get('size', 0)
                ))
                imported += 1

        conn.commit()
        conn.close()

        print(f"Imported {imported} package history entries")

    def search_package(self, package_name):
        """Search history for a specific package"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT timestamp, action, version, user 
            FROM package_history 
            WHERE package_name LIKE ?
            ORDER BY timestamp DESC
        ''', (f'%{package_name}%',))

        results = cursor.fetchall()
        conn.close()

        return results

    def get_recently_installed(self, days=7):
        """Get packages installed in last N days"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT package_name, version, timestamp, user
            FROM package_history
            WHERE action = 'install'
            AND datetime(timestamp) >= datetime('now', '-' || ? || ' days')
            ORDER BY timestamp DESC
        ''', (days,))

        results = cursor.fetchall()
        conn.close()

        return results

    def generate_report(self):
        """Generate comprehensive history report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        print("\n" + "=" * 60)
        print("PACKAGE INSTALLATION HISTORY REPORT")
        print("=" * 60 + "\n")

        # Total statistics
        cursor.execute('SELECT COUNT(*) FROM package_history')
        total = cursor.fetchone()[0]
        print(f"Total Operations: {total}")

        # By action
        print("\nOperations by Type:")
        cursor.execute('''
            SELECT action, COUNT(*) 
            FROM package_history 
            GROUP BY action
        ''')
        for action, count in cursor.fetchall():
            print(f"  {action.capitalize()}: {count}")

        # Most frequently installed
        print("\nTop 10 Most Installed/Updated Packages:")
        cursor.execute('''
            SELECT package_name, COUNT(*) as count
            FROM package_history
            WHERE action IN ('install', 'upgrade')
            GROUP BY package_name
            ORDER BY count DESC
            LIMIT 10
        ''')
        for pkg, count in cursor.fetchall():
            print(f"  {pkg}: {count} times")

        # Recent activity
        print("\nRecent Activity (Last 10 Operations):")
        cursor.execute('''
            SELECT timestamp, action, package_name, version
            FROM package_history
            ORDER BY timestamp DESC
            LIMIT 10
        ''')
        for timestamp, action, pkg, version in cursor.fetchall():
            print(f"  [{timestamp}] {action.upper()}: {pkg} {version}")

        conn.close()

    def export_to_json(self, output_file='package_history.json'):
        """Export history to JSON file"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM package_history')

        columns = [description[0] for description in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        conn.close()

        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"History exported to {output_file}")


def main():
    import sys

    tracker = PackageHistoryTracker()

    if len(sys.argv) < 2:
        print("Usage: python package_history_tracker.py [command]")
        print("\nCommands:")
        print("  import         - Import history from system logs")
        print("  search <name>  - Search for package history")
        print("  recent [days]  - Show recently installed (default: 7 days)")
        print("  report         - Generate comprehensive report")
        print("  export [file]  - Export to JSON file")
        return

    command = sys.argv[1]

    if command == 'import':
        tracker.import_history()

    elif command == 'search':
        if len(sys.argv) < 3:
            print("Please provide package name")
            return

        package_name = sys.argv[2]
        results = tracker.search_package(package_name)

        print(f"\nHistory for '{package_name}':")
        print("-" * 60)
        for timestamp, action, version, user in results:
            print(f"[{timestamp}] {action.upper()}: v{version} by {user}")

    elif command == 'recent':
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        results = tracker.get_recently_installed(days)

        print(f"\nPackages installed in last {days} days:")
        print("-" * 60)
        for pkg, version, timestamp, user in results:
            print(f"[{timestamp}] {pkg} {version} by {user}")

    elif command == 'report':
        tracker.generate_report()

    elif command == 'export':
        output = sys.argv[2] if len(sys.argv) > 2 else 'package_history.json'
        tracker.export_to_json(output)

    else:
        print(f"Unknown command: {command}")


if __name__ == '__main__':
    main()