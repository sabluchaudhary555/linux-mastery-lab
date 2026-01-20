#!/usr/bin/env python3

import os
import shutil
import psutil
import time
from datetime import datetime
from collections import defaultdict


class SystemHealthDashboard:
    def __init__(self):
        self.monitored_dirs = {
            '/var/log': 'System Logs',
            '/tmp': 'Temporary Files',
            '/home': 'User Home Directories',
            '/var/cache': 'Cache Files',
            '/var/spool': 'Spool Files',
            '/etc': 'Configuration Files'
        }

    def get_directory_stats(self, path):
        """Get statistics for a directory"""
        try:
            total_size = 0
            file_count = 0
            dir_count = 0

            if not os.path.exists(path):
                return None

            # Walk through directory
            for root, dirs, files in os.walk(path):
                dir_count += len(dirs)
                for file in files:
                    try:
                        file_path = os.path.join(root, file)
                        if os.path.exists(file_path):
                            total_size += os.path.getsize(file_path)
                            file_count += 1
                    except (OSError, PermissionError):
                        continue

            return {
                'size': total_size,
                'files': file_count,
                'dirs': dir_count
            }
        except PermissionError:
            return None

    def format_bytes(self, bytes):
        """Convert bytes to human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024.0:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.2f} PB"

    def get_disk_usage(self):
        """Get overall disk usage"""
        try:
            usage = shutil.disk_usage('/')
            return {
                'total': usage.total,
                'used': usage.used,
                'free': usage.free,
                'percent': (usage.used / usage.total) * 100
            }
        except Exception:
            return None

    def get_recent_logs(self, log_dir='/var/log', limit=5):
        """Get recently modified log files"""
        try:
            log_files = []
            for file in os.listdir(log_dir):
                file_path = os.path.join(log_dir, file)
                if os.path.isfile(file_path):
                    try:
                        mtime = os.path.getmtime(file_path)
                        log_files.append((file, mtime))
                    except (OSError, PermissionError):
                        continue

            log_files.sort(key=lambda x: x[1], reverse=True)
            return log_files[:limit]
        except (OSError, PermissionError):
            return []

    def get_memory_usage(self):
        """Get system memory usage"""
        mem = psutil.virtual_memory()
        return {
            'total': mem.total,
            'used': mem.used,
            'free': mem.available,
            'percent': mem.percent
        }

    def get_cpu_usage(self):
        """Get CPU usage percentage"""
        return psutil.cpu_percent(interval=1)

    def create_progress_bar(self, percent, width=30):
        """Create a text-based progress bar"""
        filled = int(width * percent / 100)
        bar = '█' * filled + '░' * (width - filled)
        return f"[{bar}] {percent:.1f}%"

    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')

    def display_dashboard(self):
        """Display the complete dashboard"""
        self.clear_screen()

        # Header
        print("=" * 80)
        print("       SYSTEM HEALTH DASHBOARD - Linux FHS Monitor")
        print("=" * 80)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        print()

        # System Resources
        print("📊 SYSTEM RESOURCES")
        print("-" * 80)

        # CPU Usage
        cpu = self.get_cpu_usage()
        print(f"CPU Usage:    {self.create_progress_bar(cpu)}")

        # Memory Usage
        mem = self.get_memory_usage()
        print(f"Memory:       {self.create_progress_bar(mem['percent'])}")
        print(f"              {self.format_bytes(mem['used'])} / {self.format_bytes(mem['total'])}")

        # Disk Usage
        disk = self.get_disk_usage()
        if disk:
            print(f"Disk Usage:   {self.create_progress_bar(disk['percent'])}")
            print(f"              {self.format_bytes(disk['used'])} / {self.format_bytes(disk['total'])}")

        print()

        # Directory Monitoring
        print("📁 MONITORED DIRECTORIES (FHS)")
        print("-" * 80)
        print(f"{'Directory':<20} {'Description':<25} {'Size':<12} {'Files':<10}")
        print("-" * 80)

        for path, description in self.monitored_dirs.items():
            stats = self.get_directory_stats(path)
            if stats:
                size_str = self.format_bytes(stats['size'])
                files_str = f"{stats['files']}"
                print(f"{path:<20} {description:<25} {size_str:<12} {files_str:<10}")
            else:
                print(f"{path:<20} {description:<25} {'N/A':<12} {'N/A':<10}")

        print()

        # Recent Log Activity
        print("📝 RECENT LOG ACTIVITY (/var/log)")
        print("-" * 80)
        recent_logs = self.get_recent_logs()
        if recent_logs:
            for log_file, mtime in recent_logs:
                mod_time = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
                print(f"  • {log_file:<30} (Modified: {mod_time})")
        else:
            print("  No accessible log files found")

        print()
        print("=" * 80)
        print("Press Ctrl+C to exit | Refreshes every 5000 seconds")
        print("=" * 80)

    def run(self, refresh_interval=5):
        """Run the dashboard with auto-refresh"""
        print("Starting System Health Dashboard...")
        print("Gathering system information...")
        time.sleep(2)
        try:
            while True:
                self.display_dashboard()
                time.sleep(refresh_interval)
        except KeyboardInterrupt:
            self.clear_screen()
            print("\n✓ Dashboard stopped. Goodbye!")
            print()


def main():
    """Main entry point"""
    # Check if running with sufficient permissions (Linux/Unix only)
    if os.name == 'posix':
        try:
            if os.geteuid() != 0:
                print("⚠️  Warning: Running without root privileges.")
                print("   Some directories may not be accessible.")
                print("   Run with 'sudo' for full access.\n")
                time.sleep(2)
        except AttributeError:
            pass
    else:
        print("⚠️  Running on Windows - some Linux directories may not exist.")
        print("   This tool is designed for Linux systems.\n")
        time.sleep(2)

    dashboard = SystemHealthDashboard()
    dashboard.run(refresh_interval=5000)


if __name__ == "__main__":
    main()




    """
System Health Dashboard - Linux FHS Monitor
Developed by SSoft.in

"""
