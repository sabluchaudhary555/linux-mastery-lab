#!/usr/bin/env python3
"""
Password Expiration Notification System
Monitors user password expiration dates and sends notifications
"""

import subprocess
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Tuple


class PasswordExpirationMonitor:
    def __init__(self, config_file='config.json'):
        """Initialize the monitor with configuration"""
        self.config = self.load_config(config_file)
        self.users_data = []

    def load_config(self, config_file: str) -> dict:
        """Load configuration from JSON file"""
        default_config = {
            "warning_days": [30, 14, 7, 3, 1],
            "email": {
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "sender_email": "admin@company.com",
                "sender_password": "your_app_password",
                "admin_email": "admin@company.com"
            },
            "exclude_users": ["root", "daemon", "bin", "sys", "sync"],
            "log_file": "/var/log/password_expiry.log"
        }

        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        else:
            # Create default config file
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=4)
            print(f"Created default config file: {config_file}")
            return default_config

    def get_all_users(self) -> List[str]:
        """Get list of all regular users (UID >= 1000)"""
        try:
            result = subprocess.run(
                ['awk', '-F:', '$3 >= 1000 {print $1}', '/etc/passwd'],
                capture_output=True,
                text=True,
                check=True
            )
            users = result.stdout.strip().split('\n')
            # Filter out excluded users
            exclude = self.config.get('exclude_users', [])
            return [u for u in users if u and u not in exclude]
        except subprocess.CalledProcessError as e:
            print(f"Error getting users: {e}")
            return []

    def get_password_info(self, username: str) -> Dict:
        """Get password expiration information for a user"""
        try:
            # Run chage -l command
            result = subprocess.run(
                ['sudo', 'chage', '-l', username],
                capture_output=True,
                text=True,
                check=True
            )

            output = result.stdout
            info = {
                'username': username,
                'last_change': None,
                'expires': None,
                'inactive': None,
                'account_expires': None,
                'min_days': None,
                'max_days': None,
                'warn_days': None,
                'days_until_expiry': None,
                'status': 'active'
            }

            # Parse output
            for line in output.split('\n'):
                if 'Last password change' in line:
                    date_match = re.search(r':\s*(.+)$', line)
                    if date_match and 'never' not in date_match.group(1).lower():
                        info['last_change'] = date_match.group(1).strip()

                elif 'Password expires' in line:
                    date_match = re.search(r':\s*(.+)$', line)
                    if date_match:
                        expires_str = date_match.group(1).strip()
                        if 'never' in expires_str.lower():
                            info['expires'] = 'never'
                        else:
                            info['expires'] = expires_str

                elif 'Password inactive' in line:
                    date_match = re.search(r':\s*(.+)$', line)
                    if date_match:
                        info['inactive'] = date_match.group(1).strip()

                elif 'Account expires' in line:
                    date_match = re.search(r':\s*(.+)$', line)
                    if date_match:
                        info['account_expires'] = date_match.group(1).strip()

                elif 'Minimum number of days' in line:
                    num_match = re.search(r':\s*(\d+)', line)
                    if num_match:
                        info['min_days'] = int(num_match.group(1))

                elif 'Maximum number of days' in line:
                    num_match = re.search(r':\s*(\d+)', line)
                    if num_match:
                        info['max_days'] = int(num_match.group(1))

                elif 'Number of days of warning' in line:
                    num_match = re.search(r':\s*(\d+)', line)
                    if num_match:
                        info['warn_days'] = int(num_match.group(1))

            # Calculate days until expiry
            if info['expires'] and info['expires'] != 'never':
                info['days_until_expiry'] = self.calculate_days_until_expiry(info['expires'])

            # Check password status
            status_result = subprocess.run(
                ['sudo', 'passwd', '-S', username],
                capture_output=True,
                text=True,
                check=True
            )

            status_line = status_result.stdout.strip()
            if ' L ' in status_line:
                info['status'] = 'locked'
            elif ' NP ' in status_line:
                info['status'] = 'no_password'
            elif ' PS ' in status_line:
                info['status'] = 'active'

            return info

        except subprocess.CalledProcessError as e:
            print(f"Error getting password info for {username}: {e}")
            return None

    def calculate_days_until_expiry(self, expiry_date_str: str) -> int:
        """Calculate days until password expires"""
        try:
            # Parse date string (format: "Jan 15, 2025" or similar)
            expiry_date = datetime.strptime(expiry_date_str, "%b %d, %Y")
            today = datetime.now()
            delta = expiry_date - today
            return delta.days
        except Exception as e:
            print(f"Error parsing date {expiry_date_str}: {e}")
            return None

    def scan_all_users(self) -> List[Dict]:
        """Scan all users and get their password information"""
        users = self.get_all_users()
        self.users_data = []

        print(f"Scanning {len(users)} users...")
        for username in users:
            print(f"Checking {username}...", end=' ')
            info = self.get_password_info(username)
            if info:
                self.users_data.append(info)
                print("✓")
            else:
                print("✗")

        return self.users_data

    def get_users_needing_notification(self) -> List[Dict]:
        """Get users who need password expiration notifications"""
        warning_days = self.config.get('warning_days', [30, 14, 7, 3, 1])
        users_to_notify = []

        for user in self.users_data:
            if user['days_until_expiry'] is not None:
                days = user['days_until_expiry']

                # Check if user needs notification
                if days in warning_days or days <= 0:
                    user['urgency'] = self.get_urgency_level(days)
                    users_to_notify.append(user)

        return users_to_notify

    def get_urgency_level(self, days: int) -> str:
        """Determine urgency level based on days until expiry"""
        if days <= 0:
            return "EXPIRED"
        elif days <= 3:
            return "CRITICAL"
        elif days <= 7:
            return "HIGH"
        elif days <= 14:
            return "MEDIUM"
        else:
            return "LOW"

    def send_email_notification(self, user_info: Dict) -> bool:
        """Send email notification to user"""
        try:
            email_config = self.config['email']

            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = email_config['sender_email']
            msg['To'] = f"{user_info['username']}@company.com"
            msg['Subject'] = f"Password Expiration Warning - {user_info['urgency']}"

            # Create email body
            if user_info['days_until_expiry'] <= 0:
                body = f"""
Dear {user_info['username']},

YOUR PASSWORD HAS EXPIRED!

Your password expired on {user_info['expires']}.
You must change your password immediately to continue accessing the system.

To change your password:
1. Login to the system
2. Run: passwd
3. Follow the prompts to set a new password

If you have any issues, please contact IT support.

Best regards,
IT Security Team
                """
            else:
                body = f"""
Dear {user_info['username']},

This is a reminder that your password will expire in {user_info['days_until_expiry']} day(s).

Password Details:
- Last Changed: {user_info['last_change']}
- Expires On: {user_info['expires']}
- Days Remaining: {user_info['days_until_expiry']}

To change your password before it expires:
1. Login to the system
2. Run: passwd
3. Follow the prompts to set a new password

Password Requirements:
- Minimum 8 characters
- Mix of uppercase, lowercase, numbers, and special characters
- Cannot reuse recent passwords

If you have any questions, please contact IT support.

Best regards,
IT Security Team
                """

            msg.attach(MIMEText(body, 'plain'))

            # Send email
            with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
                server.starttls()
                server.login(email_config['sender_email'], email_config['sender_password'])
                server.send_message(msg)

            print(f"✓ Email sent to {user_info['username']}")
            return True

        except Exception as e:
            print(f"✗ Error sending email to {user_info['username']}: {e}")
            return False

    def send_admin_summary(self, users_to_notify: List[Dict]) -> bool:
        """Send summary report to admin"""
        try:
            email_config = self.config['email']

            msg = MIMEMultipart('alternative')
            msg['From'] = email_config['sender_email']
            msg['To'] = email_config['admin_email']
            msg['Subject'] = f"Password Expiration Report - {datetime.now().strftime('%Y-%m-%d')}"

            # Create summary
            expired = [u for u in users_to_notify if u['days_until_expiry'] <= 0]
            critical = [u for u in users_to_notify if 0 < u['days_until_expiry'] <= 3]
            high = [u for u in users_to_notify if 3 < u['days_until_expiry'] <= 7]
            medium = [u for u in users_to_notify if 7 < u['days_until_expiry'] <= 14]
            low = [u for u in users_to_notify if u['days_until_expiry'] > 14]

            body = f"""
Password Expiration Summary Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SUMMARY:
========
Total Users Scanned: {len(self.users_data)}
Users Needing Action: {len(users_to_notify)}

- EXPIRED: {len(expired)}
- CRITICAL (1-3 days): {len(critical)}
- HIGH (4-7 days): {len(high)}
- MEDIUM (8-14 days): {len(medium)}
- LOW (15+ days): {len(low)}

EXPIRED PASSWORDS:
==================
"""

            if expired:
                for user in expired:
                    body += f"- {user['username']}: Expired on {user['expires']}\n"
            else:
                body += "None\n"

            body += "\nCRITICAL (1-3 days):\n====================\n"
            if critical:
                for user in critical:
                    body += f"- {user['username']}: {user['days_until_expiry']} days remaining\n"
            else:
                body += "None\n"

            body += "\nHIGH PRIORITY (4-7 days):\n=========================\n"
            if high:
                for user in high:
                    body += f"- {user['username']}: {user['days_until_expiry']} days remaining\n"
            else:
                body += "None\n"

            body += f"""

ACTIONS TAKEN:
==============
- Sent {len(users_to_notify)} notification emails
- Updated log file

Next scheduled scan: {(datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')}
            """

            msg.attach(MIMEText(body, 'plain'))

            # Send email
            with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
                server.starttls()
                server.login(email_config['sender_email'], email_config['sender_password'])
                server.send_message(msg)

            print("✓ Admin summary sent")
            return True

        except Exception as e:
            print(f"✗ Error sending admin summary: {e}")
            return False

    def generate_report(self) -> str:
        """Generate detailed report"""
        report = f"""
{'=' * 70}
PASSWORD EXPIRATION REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'=' * 70}

"""

        # Group users by urgency
        expired = [u for u in self.users_data if u['days_until_expiry'] is not None and u['days_until_expiry'] <= 0]
        critical = [u for u in self.users_data if
                    u['days_until_expiry'] is not None and 0 < u['days_until_expiry'] <= 3]
        high = [u for u in self.users_data if u['days_until_expiry'] is not None and 3 < u['days_until_expiry'] <= 7]
        medium = [u for u in self.users_data if u['days_until_expiry'] is not None and 7 < u['days_until_expiry'] <= 14]
        never_expire = [u for u in self.users_data if u['expires'] == 'never']
        locked = [u for u in self.users_data if u['status'] == 'locked']

        report += f"Total Users: {len(self.users_data)}\n"
        report += f"Expired: {len(expired)}\n"
        report += f"Critical (1-3 days): {len(critical)}\n"
        report += f"High (4-7 days): {len(high)}\n"
        report += f"Medium (8-14 days): {len(medium)}\n"
        report += f"Never Expire: {len(never_expire)}\n"
        report += f"Locked Accounts: {len(locked)}\n\n"

        # Detailed listings
        if expired:
            report += "EXPIRED PASSWORDS:\n" + "-" * 70 + "\n"
            for user in expired:
                report += f"  {user['username']:<20} Expired: {user['expires']}\n"
            report += "\n"

        if critical:
            report += "CRITICAL (1-3 days):\n" + "-" * 70 + "\n"
            for user in critical:
                report += f"  {user['username']:<20} Days left: {user['days_until_expiry']:<5} Expires: {user['expires']}\n"
            report += "\n"

        if high:
            report += "HIGH PRIORITY (4-7 days):\n" + "-" * 70 + "\n"
            for user in high:
                report += f"  {user['username']:<20} Days left: {user['days_until_expiry']:<5} Expires: {user['expires']}\n"
            report += "\n"

        if medium:
            report += "MEDIUM PRIORITY (8-14 days):\n" + "-" * 70 + "\n"
            for user in medium:
                report += f"  {user['username']:<20} Days left: {user['days_until_expiry']:<5} Expires: {user['expires']}\n"
            report += "\n"

        report += "=" * 70 + "\n"

        return report

    def log_activity(self, message: str):
        """Log activity to log file"""
        log_file = self.config.get('log_file', '/var/log/password_expiry.log')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            with open(log_file, 'a') as f:
                f.write(f"[{timestamp}] {message}\n")
        except Exception as e:
            print(f"Error writing to log: {e}")

    def run(self, send_notifications=True):
        """Main execution method"""
        print("=" * 70)
        print("PASSWORD EXPIRATION NOTIFICATION SYSTEM")
        print("=" * 70)
        print()

        # Scan all users
        self.log_activity("Starting password expiration scan")
        self.scan_all_users()

        # Generate and display report
        report = self.generate_report()
        print(report)

        # Get users needing notification
        users_to_notify = self.get_users_needing_notification()

        if send_notifications and users_to_notify:
            print(f"\nSending notifications to {len(users_to_notify)} users...")
            for user in users_to_notify:
                self.send_email_notification(user)
                self.log_activity(f"Sent notification to {user['username']} ({user['urgency']})")

            # Send admin summary
            self.send_admin_summary(users_to_notify)
            self.log_activity("Sent admin summary report")

        print("\n✓ Scan complete!")
        self.log_activity("Password expiration scan completed")


def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(description='Password Expiration Notification System')
    parser.add_argument('--config', default='config.json', help='Configuration file path')
    parser.add_argument('--no-email', action='store_true', help='Skip sending email notifications')
    parser.add_argument('--report-only', action='store_true', help='Generate report only, no notifications')

    args = parser.parse_args()

    # Create monitor instance
    monitor = PasswordExpirationMonitor(config_file=args.config)

    # Run the monitor
    send_emails = not (args.no_email or args.report_only)
    monitor.run(send_notifications=send_emails)


if __name__ == '__main__':
    main()