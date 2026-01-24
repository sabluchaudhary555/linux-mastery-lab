#!/usr/bin/env python3
"""
Dynamic IP Blocker - Fail2Ban Alternative
Automatically block IPs based on suspicious activity
"""

import subprocess
import re
import time
import json
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
import threading


class DynamicIPBlocker:
    def __init__(self):
        self.config_file = Path.home() / '.ip_blocker_config.json'
        self.banned_ips_file = Path.home() / '.ip_blocker_banned.json'
        self.log_file = Path('/var/log/ip_blocker.log')

        self.config = self.load_config()
        self.banned_ips = self.load_banned_ips()
        self.failed_attempts = defaultdict(list)
        self.monitoring = False

    def load_config(self):
        """Load configuration"""
        default_config = {
            'ssh': {
                'enabled': True,
                'log_file': '/var/log/auth.log',
                'max_attempts': 5,
                'time_window': 600,  # seconds
                'ban_duration': 3600,  # seconds
                'regex': r'Failed password for .* from (\d+\.\d+\.\d+\.\d+)'
            },
            'http': {
                'enabled': False,
                'log_file': '/var/log/apache2/error.log',
                'max_attempts': 10,
                'time_window': 300,
                'ban_duration': 1800,
                'regex': r'client (\d+\.\d+\.\d+\.\d+)'
            },
            'ftp': {
                'enabled': False,
                'log_file': '/var/log/vsftpd.log',
                'max_attempts': 5,
                'time_window': 600,
                'ban_duration': 3600,
                'regex': r'FAIL LOGIN.*from (\d+\.\d+\.\d+\.\d+)'
            },
            'whitelist': ['127.0.0.1', '::1'],
            'auto_unblock': True,
            'notification_email': ''
        }

        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                loaded = json.load(f)
                return {**default_config, **loaded}

        self.save_config(default_config)
        return default_config

    def save_config(self, config=None):
        """Save configuration"""
        if config:
            self.config = config
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    def load_banned_ips(self):
        """Load banned IPs from file"""
        if self.banned_ips_file.exists():
            with open(self.banned_ips_file, 'r') as f:
                return json.load(f)
        return {}

    def save_banned_ips(self):
        """Save banned IPs to file"""
        with open(self.banned_ips_file, 'w') as f:
            json.dump(self.banned_ips, f, indent=4)

    def log(self, message):
        """Log messages"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}\n"

        try:
            with open(self.log_file, 'a') as f:
                f.write(log_entry)
        except PermissionError:
            pass

        print(log_entry.strip())

    def is_whitelisted(self, ip):
        """Check if IP is whitelisted"""
        return ip in self.config['whitelist']

    def block_ip(self, ip, service='manual', duration=3600):
        """Block IP using iptables"""
        if self.is_whitelisted(ip):
            self.log(f"⚠️  IP {ip} is whitelisted, skipping block")
            return False

        if ip in self.banned_ips:
            self.log(f"IP {ip} is already blocked")
            return False

        try:
            # Add iptables DROP rule
            subprocess.run(['sudo', 'iptables', '-I', 'INPUT', '-s', ip, '-j', 'DROP'],
                           check=True, capture_output=True)

            # Record ban
            ban_time = datetime.now()
            unblock_time = ban_time + timedelta(seconds=duration)

            self.banned_ips[ip] = {
                'service': service,
                'banned_at': ban_time.strftime('%Y-%m-%d %H:%M:%S'),
                'unblock_at': unblock_time.strftime('%Y-%m-%d %H:%M:%S'),
                'duration': duration
            }

            self.save_banned_ips()

            self.log(f"🚫 BLOCKED: {ip} ({service}) - Duration: {duration}s")
            return True

        except subprocess.CalledProcessError as e:
            self.log(f"✗ Failed to block {ip}: {e}")
            return False

    def unblock_ip(self, ip):
        """Unblock IP by removing iptables rule"""
        if ip not in self.banned_ips:
            self.log(f"IP {ip} is not blocked")
            return False

        try:
            # Remove iptables DROP rule
            subprocess.run(['sudo', 'iptables', '-D', 'INPUT', '-s', ip, '-j', 'DROP'],
                           check=True, capture_output=True)

            service = self.banned_ips[ip]['service']
            del self.banned_ips[ip]
            self.save_banned_ips()

            self.log(f"✓ UNBLOCKED: {ip} ({service})")
            return True

        except subprocess.CalledProcessError as e:
            self.log(f"✗ Failed to unblock {ip}: {e}")
            return False

    def check_failed_attempts(self, ip, service):
        """Check if IP has exceeded failed attempt threshold"""
        service_config = self.config[service]
        max_attempts = service_config['max_attempts']
        time_window = service_config['time_window']

        # Get recent attempts
        now = datetime.now()
        cutoff_time = now - timedelta(seconds=time_window)

        # Filter attempts within time window
        recent_attempts = [
            attempt for attempt in self.failed_attempts[ip]
            if attempt > cutoff_time
        ]

        self.failed_attempts[ip] = recent_attempts

        # Check if threshold exceeded
        if len(recent_attempts) >= max_attempts:
            return True

        return False

    def monitor_log_file(self, service):
        """Monitor log file for failed attempts"""
        service_config = self.config[service]
        log_file = service_config['log_file']
        pattern = re.compile(service_config['regex'])

        self.log(f"📊 Monitoring {service} log: {log_file}")

        try:
            with open(log_file, 'r') as f:
                # Move to end of file
                f.seek(0, 2)

                while self.monitoring:
                    line = f.readline()

                    if not line:
                        time.sleep(0.1)
                        continue

                    # Search for IP in line
                    match = pattern.search(line)
                    if match:
                        ip = match.group(1)

                        if self.is_whitelisted(ip):
                            continue

                        if ip in self.banned_ips:
                            continue

                        # Record failed attempt
                        self.failed_attempts[ip].append(datetime.now())

                        self.log(f"⚠️  Failed {service} attempt from {ip}")

                        # Check if should block
                        if self.check_failed_attempts(ip, service):
                            ban_duration = service_config['ban_duration']
                            self.block_ip(ip, service, ban_duration)

                            # Clear attempts for this IP
                            del self.failed_attempts[ip]

        except FileNotFoundError:
            self.log(f"✗ Log file not found: {log_file}")
        except PermissionError:
            self.log(f"✗ Permission denied: {log_file}")

    def auto_unblock_daemon(self):
        """Daemon to automatically unblock expired bans"""
        self.log("🔄 Auto-unblock daemon started")

        while self.monitoring:
            now = datetime.now()

            ips_to_unblock = []
            for ip, info in self.banned_ips.items():
                unblock_time = datetime.strptime(info['unblock_at'], '%Y-%m-%d %H:%M:%S')

                if now >= unblock_time:
                    ips_to_unblock.append(ip)

            for ip in ips_to_unblock:
                self.unblock_ip(ip)

            time.sleep(60)  # Check every minute

    def start_monitoring(self):
        """Start monitoring all enabled services"""
        self.monitoring = True

        threads = []

        # Start log monitoring threads
        for service in ['ssh', 'http', 'ftp']:
            if self.config[service]['enabled']:
                thread = threading.Thread(
                    target=self.monitor_log_file,
                    args=(service,),
                    daemon=True
                )
                thread.start()
                threads.append(thread)

        # Start auto-unblock daemon
        if self.config['auto_unblock']:
            unblock_thread = threading.Thread(
                target=self.auto_unblock_daemon,
                daemon=True
            )
            unblock_thread.start()
            threads.append(unblock_thread)

        self.log("🚀 Dynamic IP Blocker started")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.log("⏹️  Stopping Dynamic IP Blocker...")
            self.monitoring = False
            time.sleep(2)

    def list_blocked_ips(self):
        """List all currently blocked IPs"""
        if not self.banned_ips:
            print("No IPs currently blocked")
            return

        print("\n" + "=" * 80)
        print("BLOCKED IP ADDRESSES")
        print("=" * 80 + "\n")

        print(f"{'IP Address':<20} {'Service':<10} {'Banned At':<20} {'Unblock At':<20}")
        print("-" * 80)

        for ip, info in self.banned_ips.items():
            print(f"{ip:<20} {info['service']:<10} {info['banned_at']:<20} {info['unblock_at']:<20}")

    def add_to_whitelist(self, ip):
        """Add IP to whitelist"""
        if ip not in self.config['whitelist']:
            self.config['whitelist'].append(ip)
            self.save_config()
            self.log(f"✓ Added {ip} to whitelist")

            # Unblock if currently blocked
            if ip in self.banned_ips:
                self.unblock_ip(ip)
        else:
            print(f"{ip} is already whitelisted")

    def remove_from_whitelist(self, ip):
        """Remove IP from whitelist"""
        if ip in self.config['whitelist']:
            self.config['whitelist'].remove(ip)
            self.save_config()
            self.log(f"✓ Removed {ip} from whitelist")
        else:
            print(f"{ip} is not in whitelist")

    def show_whitelist(self):
        """Display whitelisted IPs"""
        print("\n" + "=" * 50)
        print("WHITELISTED IP ADDRESSES")
        print("=" * 50 + "\n")

        for ip in self.config['whitelist']:
            print(f"  {ip}")

    def show_stats(self):
        """Display statistics"""
        print("\n" + "=" * 60)
        print("DYNAMIC IP BLOCKER STATISTICS")
        print("=" * 60 + "\n")

        print(f"Currently Blocked IPs: {len(self.banned_ips)}")
        print(f"Whitelisted IPs: {len(self.config['whitelist'])}")

        print("\nService Status:")
        for service in ['ssh', 'http', 'ftp']:
            status = "✓ Enabled" if self.config[service]['enabled'] else "✗ Disabled"
            print(f"  {service.upper()}: {status}")

        print(f"\nAuto-unblock: {'✓ Enabled' if self.config['auto_unblock'] else '✗ Disabled'}")


def main():
    import sys

    blocker = DynamicIPBlocker()

    if len(sys.argv) < 2:
        print("Usage: python dynamic_ip_blocker.py [command]")
        print("\nCommands:")
        print("  start                  - Start monitoring (daemon mode)")
        print("  block <ip> [duration]  - Manually block IP (default: 3600s)")
        print("  unblock <ip>           - Manually unblock IP")
        print("  list                   - List blocked IPs")
        print("  whitelist-add <ip>     - Add IP to whitelist")
        print("  whitelist-remove <ip>  - Remove IP from whitelist")
        print("  whitelist-show         - Show whitelisted IPs")
        print("  stats                  - Show statistics")
        print("\nExamples:")
        print("  sudo python3 dynamic_ip_blocker.py start")
        print("  sudo python3 dynamic_ip_blocker.py block 192.168.1.100 7200")
        print("  sudo python3 dynamic_ip_blocker.py unblock 192.168.1.100")
        return

    command = sys.argv[1]

    if command == 'start':
        blocker.start_monitoring()

    elif command == 'block':
        if len(sys.argv) < 3:
            print("Usage: block <ip> [duration_seconds]")
            return

        ip = sys.argv[2]
        duration = int(sys.argv[3]) if len(sys.argv) > 3 else 3600
        blocker.block_ip(ip, 'manual', duration)

    elif command == 'unblock':
        if len(sys.argv) < 3:
            print("Usage: unblock <ip>")
            return

        blocker.unblock_ip(sys.argv[2])

    elif command == 'list':
        blocker.list_blocked_ips()

    elif command == 'whitelist-add':
        if len(sys.argv) < 3:
            print("Usage: whitelist-add <ip>")
            return

        blocker.add_to_whitelist(sys.argv[2])

    elif command == 'whitelist-remove':
        if len(sys.argv) < 3:
            print("Usage: whitelist-remove <ip>")
            return

        blocker.remove_from_whitelist(sys.argv[2])

    elif command == 'whitelist-show':
        blocker.show_whitelist()

    elif command == 'stats':
        blocker.show_stats()

    else:
        print(f"Unknown command: {command}")


if __name__ == '__main__':
    main()