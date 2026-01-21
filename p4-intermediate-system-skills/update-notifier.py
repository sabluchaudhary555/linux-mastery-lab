#!/usr/bin/env python3
"""
System Update Notifier & Scheduler
Checks for available updates, sends notifications, and schedules automatic updates
"""

import subprocess
import platform
import os
import json
import time
from datetime import datetime
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class UpdateNotifier:
    def __init__(self):
        self.distro = self.detect_distro()
        self.config_file = Path.home() / '.update_notifier_config.json'
        self.log_file = Path.home() / '.update_notifier.log'
        self.config = self.load_config()

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

    def load_config(self):
        """Load configuration from file"""
        default_config = {
            'email_enabled': False,
            'email_to': '',
            'email_from': '',
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'smtp_password': '',
            'check_interval': 3600,  # seconds
            'auto_update_enabled': False,
            'auto_update_time': '03:00'
        }

        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return {**default_config, **json.load(f)}
        return default_config

    def save_config(self, config):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)

    def log(self, message):
        """Log messages to file"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}\n"

        with open(self.log_file, 'a') as f:
            f.write(log_entry)
        print(log_entry.strip())

    def check_updates(self):
        """Check for available updates based on distro"""
        self.log(f"Checking for updates on {self.distro} system...")

        try:
            if self.distro == 'debian':
                return self._check_debian_updates()
            elif self.distro == 'redhat':
                return self._check_redhat_updates()
            elif self.distro == 'arch':
                return self._check_arch_updates()
            elif self.distro == 'suse':
                return self._check_suse_updates()
            else:
                return {'error': 'Unsupported distribution'}
        except Exception as e:
            self.log(f"Error checking updates: {str(e)}")
            return {'error': str(e)}

    def _check_debian_updates(self):
        """Check updates for Debian/Ubuntu"""
        # Update package database
        subprocess.run(['sudo', 'apt', 'update'],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)

        # Get upgradable packages
        result = subprocess.run(['apt', 'list', '--upgradable'],
                                capture_output=True, text=True)

        packages = [line.split('/')[0] for line in result.stdout.split('\n')[1:]
                    if line and not line.startswith('Listing')]

        return {
            'count': len(packages),
            'packages': packages,
            'distro': 'Debian/Ubuntu'
        }

    def _check_redhat_updates(self):
        """Check updates for RHEL/Fedora"""
        result = subprocess.run(['dnf', 'check-update'],
                                capture_output=True, text=True)

        lines = result.stdout.split('\n')
        packages = [line.split()[0] for line in lines
                    if line and not line.startswith(('Last', 'Loaded'))]

        return {
            'count': len(packages),
            'packages': packages,
            'distro': 'RHEL/Fedora'
        }

    def _check_arch_updates(self):
        """Check updates for Arch Linux"""
        subprocess.run(['sudo', 'pacman', '-Sy'],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)

        result = subprocess.run(['pacman', '-Qu'],
                                capture_output=True, text=True)

        packages = [line.split()[0] for line in result.stdout.split('\n') if line]

        return {
            'count': len(packages),
            'packages': packages,
            'distro': 'Arch Linux'
        }

    def _check_suse_updates(self):
        """Check updates for openSUSE"""
        subprocess.run(['sudo', 'zypper', 'refresh'],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)

        result = subprocess.run(['zypper', 'list-updates'],
                                capture_output=True, text=True)

        lines = result.stdout.split('\n')
        packages = [line.split('|')[2].strip() for line in lines
                    if '|' in line and not line.startswith(('S', '-'))]

        return {
            'count': len(packages),
            'packages': packages,
            'distro': 'openSUSE'
        }

    def send_notification(self, update_info):
        """Send desktop notification"""
        if update_info.get('error'):
            return

        count = update_info['count']
        if count == 0:
            message = "System is up to date!"
        else:
            message = f"{count} update(s) available"

        try:
            subprocess.run([
                'notify-send',
                'System Updates',
                message,
                '-i', 'system-software-update',
                '-u', 'normal'
            ])
            self.log(f"Desktop notification sent: {message}")
        except Exception as e:
            self.log(f"Failed to send desktop notification: {str(e)}")

    def send_email(self, update_info):
        """Send email notification"""
        if not self.config['email_enabled'] or update_info.get('error'):
            return

        count = update_info['count']
        if count == 0:
            return  # Don't send email if no updates

        try:
            msg = MIMEMultipart()
            msg['From'] = self.config['email_from']
            msg['To'] = self.config['email_to']
            msg['Subject'] = f"System Updates Available: {count} package(s)"

            body = f"""
System Update Notification
{'-' * 50}

Distribution: {update_info['distro']}
Available Updates: {count}

Packages:
{chr(10).join(f"  - {pkg}" for pkg in update_info['packages'][:20])}

{'...' if len(update_info['packages']) > 20 else ''}

Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """

            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port']) as server:
                server.starttls()
                server.login(self.config['email_from'], self.config['smtp_password'])
                server.send_message(msg)

            self.log(f"Email notification sent to {self.config['email_to']}")
        except Exception as e:
            self.log(f"Failed to send email: {str(e)}")

    def perform_update(self):
        """Perform system update"""
        self.log("Starting automatic system update...")

        try:
            if self.distro == 'debian':
                subprocess.run(['sudo', 'apt', 'update', '-y'], check=True)
                subprocess.run(['sudo', 'apt', 'upgrade', '-y'], check=True)
            elif self.distro == 'redhat':
                subprocess.run(['sudo', 'dnf', 'upgrade', '-y'], check=True)
            elif self.distro == 'arch':
                subprocess.run(['sudo', 'pacman', '-Syu', '--noconfirm'], check=True)
            elif self.distro == 'suse':
                subprocess.run(['sudo', 'zypper', 'update', '-y'], check=True)

            self.log("System update completed successfully")
            return True
        except Exception as e:
            self.log(f"System update failed: {str(e)}")
            return False

    def run_daemon(self):
        """Run as daemon to check for updates periodically"""
        self.log("Update notifier daemon started")

        while True:
            update_info = self.check_updates()

            if not update_info.get('error'):
                self.send_notification(update_info)
                self.send_email(update_info)

                # Check if auto-update is enabled and it's time to update
                if self.config['auto_update_enabled']:
                    current_time = datetime.now().strftime('%H:%M')
                    if current_time == self.config['auto_update_time']:
                        if update_info['count'] > 0:
                            self.perform_update()

            time.sleep(self.config['check_interval'])

    def configure(self):
        """Interactive configuration"""
        print("\n=== Update Notifier Configuration ===\n")

        print(f"Current Distribution: {self.distro}")

        # Email configuration
        enable_email = input("\nEnable email notifications? (y/n): ").lower() == 'y'

        if enable_email:
            email_to = input("Recipient email: ")
            email_from = input("Sender email: ")
            smtp_password = input("SMTP password: ")

            self.config.update({
                'email_enabled': True,
                'email_to': email_to,
                'email_from': email_from,
                'smtp_password': smtp_password
            })

        # Auto-update configuration
        auto_update = input("\nEnable automatic updates? (y/n): ").lower() == 'y'

        if auto_update:
            update_time = input("Update time (HH:MM, 24-hour format, e.g., 03:00): ")
            self.config.update({
                'auto_update_enabled': True,
                'auto_update_time': update_time
            })

        # Check interval
        interval = input("\nCheck interval in minutes (default: 60): ") or "60"
        self.config['check_interval'] = int(interval) * 60

        self.save_config(self.config)
        print("\nConfiguration saved!")


def main():
    import sys

    notifier = UpdateNotifier()

    if len(sys.argv) < 2:
        print("Usage: python update_notifier.py [check|daemon|configure|update]")
        print("\nCommands:")
        print("  check      - Check for updates once")
        print("  daemon     - Run as background daemon")
        print("  configure  - Configure settings")
        print("  update     - Perform system update now")
        return

    command = sys.argv[1]

    if command == 'check':
        update_info = notifier.check_updates()
        if not update_info.get('error'):
            print(f"\nDistribution: {update_info['distro']}")
            print(f"Available updates: {update_info['count']}")
            if update_info['count'] > 0:
                print("\nPackages:")
                for pkg in update_info['packages']:
                    print(f"  - {pkg}")
            notifier.send_notification(update_info)

    elif command == 'daemon':
        print("Starting daemon mode (press Ctrl+C to stop)...")
        try:
            notifier.run_daemon()
        except KeyboardInterrupt:
            print("\nDaemon stopped")

    elif command == 'configure':
        notifier.configure()

    elif command == 'update':
        notifier.perform_update()

    else:
        print(f"Unknown command: {command}")


if __name__ == '__main__':
    main()