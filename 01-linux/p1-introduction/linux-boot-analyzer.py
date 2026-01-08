#!/usr/bin/env python3
"""
Linux Boot Process Analyzer
Traces and visualizes the Linux boot sequence with performance metrics
"""

import os
import subprocess
import re
from datetime import datetime, timedelta
from collections import defaultdict


class LinuxBootAnalyzer:
    def __init__(self):
        self.boot_stages = {
            1: {"name": "BIOS/UEFI", "color": "95", "icon": "⚡"},
            2: {"name": "Bootloader (GRUB)", "color": "94", "icon": "🔧"},
            3: {"name": "Kernel", "color": "92", "icon": "🐧"},
            4: {"name": "Init System (systemd)", "color": "93", "icon": "⚙️"},
            5: {"name": "Services", "color": "96", "icon": "🔄"},
            6: {"name": "Login Ready", "color": "91", "icon": "✓"}
        }

    def colorize(self, text, color_code):
        """Add color to terminal output"""
        return f"\033[{color_code}m{text}\033[0m"

    def print_header(self):
        """Print analyzer header"""
        print("\n" + "=" * 80)
        print(self.colorize("         LINUX BOOT PROCESS ANALYZER", "1;96"))
        print("=" * 80)
        print()

    def get_boot_time(self):
        """Get system boot time"""
        try:
            result = subprocess.run(['uptime', '-s'], capture_output=True, text=True)
            boot_time_str = result.stdout.strip()
            boot_time = datetime.strptime(boot_time_str, '%Y-%m-%d %H:%M:%S')
            return boot_time
        except Exception as e:
            print(f"Error getting boot time: {e}")
            return None

    def get_kernel_boot_time(self):
        """Get kernel boot time from /proc/uptime"""
        try:
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.read().split()[0])
            return uptime_seconds
        except Exception as e:
            print(f"Error reading uptime: {e}")
            return None

    def analyze_dmesg(self):
        """Analyze kernel messages from dmesg"""
        print(self.colorize("\n📋 KERNEL BOOT MESSAGES (dmesg)", "1;93"))
        print("-" * 80)

        try:
            result = subprocess.run(['dmesg', '-T'], capture_output=True, text=True)
            lines = result.stdout.split('\n')[:20]  # First 20 lines

            for line in lines:
                if line.strip():
                    print(f"  {line}")

            print(f"\n  ... (showing first 20 lines, use 'dmesg' for full log)")
        except Exception as e:
            print(f"  Error: Unable to read dmesg. Try running with sudo.")
            print(f"  {e}")

    def analyze_systemd_boot(self):
        """Analyze systemd boot performance"""
        print(self.colorize("\n⚙️  SYSTEMD BOOT ANALYSIS", "1;93"))
        print("-" * 80)

        try:
            # Get systemd-analyze time
            result = subprocess.run(['systemd-analyze'], capture_output=True, text=True)
            print(f"\n{result.stdout}")

            # Get systemd-analyze blame (top 10 slowest services)
            print(self.colorize("\n🐌 TOP 10 SLOWEST SERVICES:", "1;91"))
            print("-" * 80)
            result = subprocess.run(['systemd-analyze', 'blame'], capture_output=True, text=True)
            lines = result.stdout.split('\n')[:10]

            for i, line in enumerate(lines, 1):
                if line.strip():
                    print(f"  {i}. {line}")

        except FileNotFoundError:
            print("  systemd-analyze not found. This system may not use systemd.")
        except Exception as e:
            print(f"  Error analyzing systemd: {e}")

    def get_boot_loader_info(self):
        """Get bootloader information"""
        print(self.colorize("\n🔧 BOOTLOADER INFORMATION", "1;93"))
        print("-" * 80)

        # Check for GRUB
        grub_cfg_paths = [
            '/boot/grub/grub.cfg',
            '/boot/grub2/grub.cfg',
            '/boot/efi/EFI/ubuntu/grub.cfg'
        ]

        grub_found = False
        for path in grub_cfg_paths:
            if os.path.exists(path):
                print(f"  Bootloader: GRUB2")
                print(f"  Config File: {path}")
                grub_found = True
                break

        if not grub_found:
            print("  Bootloader: Unknown or not GRUB")

        # Check for EFI
        if os.path.exists('/sys/firmware/efi'):
            print(f"  Boot Mode: UEFI")
        else:
            print(f"  Boot Mode: Legacy BIOS")

    def get_kernel_info(self):
        """Get kernel information"""
        print(self.colorize("\n🐧 KERNEL INFORMATION", "1;93"))
        print("-" * 80)

        try:
            # Kernel version
            with open('/proc/version', 'r') as f:
                print(f"  {f.read().strip()}")

            # Kernel command line
            print(f"\n  Kernel Parameters:")
            with open('/proc/cmdline', 'r') as f:
                cmdline = f.read().strip()
                params = cmdline.split()
                for param in params[:5]:  # Show first 5 params
                    print(f"    • {param}")
                if len(params) > 5:
                    print(f"    ... and {len(params) - 5} more parameters")

        except Exception as e:
            print(f"  Error reading kernel info: {e}")

    def visualize_boot_stages(self):
        """Visualize boot stages"""
        print(self.colorize("\n🚀 BOOT SEQUENCE VISUALIZATION", "1;93"))
        print("-" * 80)
        print()

        stages_info = [
            ("BIOS/UEFI", "Hardware POST & Initialization", "0-2s"),
            ("Bootloader", "GRUB loads kernel", "2-4s"),
            ("Kernel", "Linux kernel initialization", "4-8s"),
            ("Init System", "systemd starts (PID 1)", "8-15s"),
            ("Services", "System services startup", "15-25s"),
            ("Login Ready", "Display manager / TTY ready", "25-30s")
        ]

        for i, (stage, desc, timing) in enumerate(stages_info, 1):
            icon = self.boot_stages[i]["icon"]
            color = self.boot_stages[i]["color"]

            print(f"  {icon}  {self.colorize(f'Stage {i}: {stage}', color)}")
            print(f"      Description: {desc}")
            print(f"      Typical Time: {timing}")
            print()

    def show_boot_log_locations(self):
        """Show where boot logs are located"""
        print(self.colorize("\n📁 BOOT LOG LOCATIONS", "1;93"))
        print("-" * 80)

        log_locations = {
            "Kernel Messages": "/var/log/kern.log or dmesg",
            "System Log": "/var/log/syslog",
            "Boot Log": "/var/log/boot.log",
            "systemd Journal": "journalctl -b (current boot)",
            "Previous Boots": "journalctl --list-boots",
            "GRUB Logs": "/var/log/grub.log (if available)"
        }

        for log_type, location in log_locations.items():
            print(f"  • {log_type:20} → {location}")

    def analyze_critical_files(self):
        """Check critical boot files"""
        print(self.colorize("\n📄 CRITICAL BOOT FILES", "1;93"))
        print("-" * 80)

        critical_files = [
            ("/boot/vmlinuz", "Kernel image"),
            ("/boot/initrd.img", "Initial RAM disk"),
            ("/etc/fstab", "Filesystem table"),
            ("/etc/systemd/system", "systemd configuration"),
            ("/proc/cmdline", "Kernel parameters")
        ]

        for filepath, description in critical_files:
            if os.path.exists(filepath):
                status = self.colorize("✓ EXISTS", "92")
            else:
                status = self.colorize("✗ MISSING", "91")

            print(f"  {status}  {filepath:30} ({description})")

    def get_system_info(self):
        """Get basic system information"""
        print(self.colorize("\n💻 SYSTEM INFORMATION", "1;93"))
        print("-" * 80)

        boot_time = self.get_boot_time()
        if boot_time:
            uptime = datetime.now() - boot_time
            print(f"  Last Boot: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  Uptime: {uptime.days} days, {uptime.seconds // 3600} hours")

        kernel_uptime = self.get_kernel_boot_time()
        if kernel_uptime:
            print(f"  Kernel Uptime: {kernel_uptime:.2f} seconds")

    def show_useful_commands(self):
        """Show useful commands for boot analysis"""
        print(self.colorize("\n🔍 USEFUL COMMANDS FOR BOOT ANALYSIS", "1;93"))
        print("-" * 80)

        commands = [
            ("systemd-analyze", "Show boot time breakdown"),
            ("systemd-analyze blame", "Show service startup times"),
            ("systemd-analyze critical-chain", "Show critical startup path"),
            ("journalctl -b", "Show current boot logs"),
            ("journalctl -b -1", "Show previous boot logs"),
            ("dmesg", "Show kernel ring buffer"),
            ("dmesg -T", "Show kernel messages with timestamps"),
            ("last reboot", "Show reboot history")
        ]

        for cmd, desc in commands:
            print(f"  • {cmd:35} - {desc}")

    def run_analysis(self):
        """Run complete boot analysis"""
        self.print_header()
        self.get_system_info()
        self.visualize_boot_stages()
        self.get_boot_loader_info()
        self.get_kernel_info()
        self.analyze_critical_files()
        self.analyze_systemd_boot()
        self.analyze_dmesg()
        self.show_boot_log_locations()
        self.show_useful_commands()

        print("\n" + "=" * 80)
        print(self.colorize("Analysis Complete!", "1;92"))
        print("=" * 80)
        print()


def main():
    """Main entry point"""
    analyzer = LinuxBootAnalyzer()

    print("\n" + "=" * 80)
    print("Starting Linux Boot Process Analysis...")
    print("=" * 80)

    # Check if running on Linux
    if os.name != 'posix':
        print("\n⚠️  Warning: This tool is designed for Linux systems.")
        print("   Some features may not work on other operating systems.\n")

    # Check for root privileges
    if os.geteuid() != 0:
        print("\n⚠️  Note: Some features require root privileges.")
        print("   Run with 'sudo' for complete analysis.\n")
        input("Press Enter to continue...")

    analyzer.run_analysis()


if __name__ == "__main__":
    main()

    """
Linux boot analyzer  
Developed by SSoft.in

"""
