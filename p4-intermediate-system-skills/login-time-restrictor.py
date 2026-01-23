#!/usr/bin/env python3
"""
Login Time Restrictor
Restrict user login times based on schedules
"""

import subprocess
import json
from datetime import datetime
from pathlib import Path
import pwd


class LoginTimeRestrictor:
    def __init__(self):
        self.config_file = Path.home() / '.login_time_config.json'
        self.config = self.load_config()

    def load_config(self):
        """Load time restrictions configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {}

    def save_config(self):
        """Save configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    def set_restriction(self, username, allowed_hours, allowed_days):
        """Set login time restriction for user

        Args:
            username: User to restrict
            allowed_hours: e.g., "09:00-17:00"
            allowed_days: e.g., "Mon-Fri" or "Mon,Wed,Fri"
        """
        # Verify user exists
        try:
            pwd.getpwnam(username)
        except KeyError:
            print(f"Error: User '{username}' does not exist")
            return False

        self.config[username] = {
            'allowed_hours': allowed_hours,
            'allowed_days': allowed_days,
            'enabled': True
        }
        self.save_config()

        # Update PAM time configuration
        self.update_pam_time(username, allowed_hours, allowed_days)

        print(f"✓ Restriction set for {username}")
        print(f"  Hours: {allowed_hours}")
        print(f"  Days: {allowed_days}")
        return True

    def update_pam_time(self, username, hours, days):
        """Update /etc/security/time.conf"""
        time_conf = "/etc/security/time.conf"

        # Convert format: login;*;username;hours;days
        entry = f"login;*;{username};{self.convert_time_format(hours)};{self.convert_day_format(days)}\n"

        try:
            # Read existing
            with open(time_conf, 'r') as f:
                lines = f.readlines()

            # Remove old entry for this user
            lines = [l for l in lines if not l.startswith(f"login;*;{username};")]

            # Add new entry
            lines.append(entry)

            # Write back
            with open(time_conf, 'w') as f:
                f.writelines(lines)

            print(f"✓ Updated {time_conf}")
        except PermissionError:
            print(f"Warning: Need sudo to update {time_conf}")

    def convert_time_format(self, time_range):
        """Convert 09:00-17:00 to 0900-1700"""
        return time_range.replace(':', '')

    def convert_day_format(self, days):
        """Convert Mon-Fri to Wk (weekday) or expand Mon,Wed,Fri"""
        if days == "Mon-Fri":
            return "Wk"
        elif days == "Mon-Sun":
            return "Al"
        else:
            # Return as-is for custom days
            return days

    def remove_restriction(self, username):
        """Remove login time restriction"""
        if username in self.config:
            del self.config[username]
            self.save_config()

            # Remove from PAM time.conf
            time_conf = "/etc/security/time.conf"
            try:
                with open(time_conf, 'r') as f:
                    lines = f.readlines()

                lines = [l for l in lines if not l.startswith(f"login;*;{username};")]

                with open(time_conf, 'w') as f:
                    f.writelines(lines)

                print(f"✓ Restriction removed for {username}")
            except PermissionError:
                print(f"Warning: Need sudo to update {time_conf}")
        else:
            print(f"No restriction found for {username}")

    def check_current_access(self, username):
        """Check if user can login at current time"""
        if username not in self.config or not self.config[username]['enabled']:
            return True, "No restrictions"

        restriction = self.config[username]
        now = datetime.now()
        current_time = now.strftime('%H:%M')
        current_day = now.strftime('%a')

        # Check time
        allowed_hours = restriction['allowed_hours']
        start_time, end_time = allowed_hours.split('-')

        if not (start_time <= current_time <= end_time):
            return False, f"Outside allowed hours ({allowed_hours})"

        # Check day
        allowed_days = restriction['allowed_days']
        if allowed_days == "Mon-Fri":
            if current_day in ['Sat', 'Sun']:
                return False, "Weekends not allowed"
        elif allowed_days == "Mon-Sun":
            pass  # All days allowed
        else:
            # Check specific days
            if current_day not in allowed_days:
                return False, f"Day {current_day} not allowed"

        return True, "Access allowed"

    def enable_account(self, username):
        """Enable user account"""
        try:
            subprocess.run(['sudo', 'usermod', '-U', username], check=True)
            print(f"✓ Account {username} enabled")
        except subprocess.CalledProcessError:
            print(f"✗ Failed to enable {username}")

    def disable_account(self, username):
        """Disable user account"""
        try:
            subprocess.run(['sudo', 'usermod', '-L', username], check=True)
            print(f"✓ Account {username} disabled")
        except subprocess.CalledProcessError:
            print(f"✗ Failed to disable {username}")

    def enforce_restrictions(self):
        """Check and enforce all restrictions"""
        print("\n" + "=" * 60)
        print("ENFORCING LOGIN TIME RESTRICTIONS")
        print("=" * 60 + "\n")

        for username, restriction in self.config.items():
            if not restriction['enabled']:
                continue

            allowed, reason = self.check_current_access(username)

            if allowed:
                self.enable_account(username)
                print(f"✓ {username}: {reason}")
            else:
                self.disable_account(username)
                print(f"✗ {username}: {reason}")

    def list_restrictions(self):
        """List all configured restrictions"""
        if not self.config:
            print("No restrictions configured")
            return

        print("\n" + "=" * 60)
        print("LOGIN TIME RESTRICTIONS")
        print("=" * 60 + "\n")

        for username, restriction in self.config.items():
            status = "✓ Enabled" if restriction['enabled'] else "✗ Disabled"
            print(f"{username}:")
            print(f"  Hours: {restriction['allowed_hours']}")
            print(f"  Days: {restriction['allowed_days']}")
            print(f"  Status: {status}")

            # Check current access
            allowed, reason = self.check_current_access(username)
            print(f"  Current: {reason}\n")

    def toggle_restriction(self, username):
        """Enable/disable restriction without removing it"""
        if username in self.config:
            self.config[username]['enabled'] = not self.config[username]['enabled']
            self.save_config()
            status = "enabled" if self.config[username]['enabled'] else "disabled"
            print(f"✓ Restriction {status} for {username}")
        else:
            print(f"No restriction found for {username}")


def main():
    import sys

    restrictor = LoginTimeRestrictor()

    if len(sys.argv) < 2:
        print("Usage: python login_time_restrictor.py [command]")
        print("\nCommands:")
        print("  set <user> <hours> <days>  - Set restriction (e.g., set john 09:00-17:00 Mon-Fri)")
        print("  remove <user>              - Remove restriction")
        print("  check <user>               - Check if user can login now")
        print("  enable <user>              - Enable user account")
        print("  disable <user>             - Disable user account")
        print("  enforce                    - Enforce all restrictions now")
        print("  list                       - List all restrictions")
        print("  toggle <user>              - Enable/disable restriction")
        print("\nExamples:")
        print("  python login_time_restrictor.py set bob 08:00-18:00 Mon-Fri")
        print("  python login_time_restrictor.py set alice 09:00-22:00 Mon-Sun")
        return

    command = sys.argv[1]

    if command == 'set':
        if len(sys.argv) < 5:
            print("Usage: set <user> <hours> <days>")
            print("Example: set bob 09:00-17:00 Mon-Fri")
            return

        username = sys.argv[2]
        hours = sys.argv[3]
        days = sys.argv[4]
        restrictor.set_restriction(username, hours, days)

    elif command == 'remove':
        if len(sys.argv) < 3:
            print("Usage: remove <user>")
            return

        restrictor.remove_restriction(sys.argv[2])

    elif command == 'check':
        if len(sys.argv) < 3:
            print("Usage: check <user>")
            return

        username = sys.argv[2]
        allowed, reason = restrictor.check_current_access(username)

        if allowed:
            print(f"✓ {username} CAN login: {reason}")
        else:
            print(f"✗ {username} CANNOT login: {reason}")

    elif command == 'enable':
        if len(sys.argv) < 3:
            print("Usage: enable <user>")
            return

        restrictor.enable_account(sys.argv[2])

    elif command == 'disable':
        if len(sys.argv) < 3:
            print("Usage: disable <user>")
            return

        restrictor.disable_account(sys.argv[2])

    elif command == 'enforce':
        restrictor.enforce_restrictions()

    elif command == 'list':
        restrictor.list_restrictions()

    elif command == 'toggle':
        if len(sys.argv) < 3:
            print("Usage: toggle <user>")
            return

        restrictor.toggle_restriction(sys.argv[2])

    else:
        print(f"Unknown command: {command}")


if __name__ == '__main__':
    main()