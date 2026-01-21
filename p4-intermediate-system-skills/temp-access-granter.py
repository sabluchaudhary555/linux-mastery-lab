#!/usr/bin/env python3
"""
Temporary Access Granter
System for granting temporary elevated permissions with automatic revocation
"""

import subprocess
import sqlite3
import os
import json
import smtplib
import requests
from datetime import datetime, timedelta
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass
import pwd
import grp


class TemporaryAccessGranter:
    def __init__(self):
        self.db_path = Path.home() / '.temp_access.db'
        self.config_file = Path.home() / '.temp_access_config.json'
        self.log_file = Path('/var/log/temp_access.log')
        self.config = self.load_config()
        self.init_database()

    def load_config(self):
        """Load configuration"""
        default_config = {
            'email_enabled': False,
            'email_to': '',
            'email_from': '',
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'smtp_password': '',
            'slack_enabled': False,
            'slack_webhook': '',
            'approval_required': True,
            'max_duration_hours': 24,
            'allowed_groups': ['sudo', 'wheel', 'admin'],
            'log_sudo_commands': True
        }

        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return {**default_config, **json.load(f)}
        return default_config

    def save_config(self, config):
        """Save configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)

    def init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS access_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                requested_group TEXT NOT NULL,
                duration_hours INTEGER NOT NULL,
                reason TEXT,
                status TEXT DEFAULT 'pending',
                requested_by TEXT,
                requested_at TEXT,
                approved_by TEXT,
                approved_at TEXT,
                expires_at TEXT,
                revoked_at TEXT,
                emergency BOOLEAN DEFAULT 0
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS access_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_id INTEGER,
                username TEXT,
                action TEXT,
                timestamp TEXT,
                details TEXT,
                FOREIGN KEY (request_id) REFERENCES access_requests(id)
            )
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_username 
            ON access_requests(username)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_status 
            ON access_requests(status)
        ''')

        conn.commit()
        conn.close()

    def log(self, message, request_id=None, username=None, action=None):
        """Log to file and database"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}\n"

        # Log to file
        try:
            with open(self.log_file, 'a') as f:
                f.write(log_entry)
        except PermissionError:
            print(f"Warning: Cannot write to {self.log_file}")

        print(log_entry.strip())

        # Log to database
        if action:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO access_log (request_id, username, action, timestamp, details)
                VALUES (?, ?, ?, ?, ?)
            ''', (request_id, username, action, timestamp, message))
            conn.commit()
            conn.close()

    def request_access(self, username, group, duration_hours, reason, emergency=False):
        """Request temporary access to a group"""
        # Validate inputs
        if group not in self.config['allowed_groups']:
            print(f"Error: Group '{group}' is not in allowed groups list")
            return None

        if duration_hours > self.config['max_duration_hours']:
            print(f"Error: Duration exceeds maximum of {self.config['max_duration_hours']} hours")
            return None

        # Check if user exists
        try:
            pwd.getpwnam(username)
        except KeyError:
            print(f"Error: User '{username}' does not exist")
            return None

        # Check if group exists
        try:
            grp.getgrnam(group)
        except KeyError:
            print(f"Error: Group '{group}' does not exist")
            return None

        requested_by = getpass.getuser()
        requested_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO access_requests 
            (username, requested_group, duration_hours, reason, requested_by, 
             requested_at, status, emergency)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (username, group, duration_hours, reason, requested_by,
              requested_at, 'pending', emergency))

        request_id = cursor.lastrowid
        conn.commit()
        conn.close()

        self.log(f"Access request created: {username} → {group} for {duration_hours}h",
                 request_id=request_id, username=username, action='request')

        # Send notifications
        self.send_notification(request_id, 'request')

        # Auto-approve if emergency and configured
        if emergency and not self.config['approval_required']:
            print("\n⚠️  EMERGENCY ACCESS - Auto-approving...")
            self.approve_request(request_id, auto_approved=True)

        return request_id

    def approve_request(self, request_id, auto_approved=False):
        """Approve an access request and grant permissions"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT username, requested_group, duration_hours, emergency, status
            FROM access_requests WHERE id = ?
        ''', (request_id,))

        result = cursor.fetchone()

        if not result:
            print(f"Error: Request ID {request_id} not found")
            conn.close()
            return False

        username, group, duration_hours, emergency, status = result

        if status != 'pending':
            print(f"Error: Request is already {status}")
            conn.close()
            return False

        approved_by = 'SYSTEM' if auto_approved else getpass.getuser()
        approved_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        expires_at = (datetime.now() + timedelta(hours=duration_hours)).strftime('%Y-%m-%d %H:%M:%S')

        # Add user to group
        try:
            subprocess.run(['sudo', 'usermod', '-aG', group, username], check=True)
            self.log(f"✓ User {username} added to group {group}",
                     request_id=request_id, username=username, action='approve')
        except subprocess.CalledProcessError as e:
            self.log(f"✗ Failed to add user to group: {str(e)}",
                     request_id=request_id, username=username, action='error')
            conn.close()
            return False

        # Update database
        cursor.execute('''
            UPDATE access_requests
            SET status = 'approved', approved_by = ?, approved_at = ?, expires_at = ?
            WHERE id = ?
        ''', (approved_by, approved_at, expires_at, request_id))

        conn.commit()
        conn.close()

        # Schedule automatic revocation
        self.schedule_revocation(request_id, username, group, duration_hours)

        # Send notifications
        self.send_notification(request_id, 'approval')

        print(f"\n✓ Access approved for {username}")
        print(f"  Group: {group}")
        print(f"  Duration: {duration_hours} hours")
        print(f"  Expires: {expires_at}")

        return True

    def deny_request(self, request_id, reason=None):
        """Deny an access request"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT username, requested_group, status
            FROM access_requests WHERE id = ?
        ''', (request_id,))

        result = cursor.fetchone()

        if not result:
            print(f"Error: Request ID {request_id} not found")
            conn.close()
            return False

        username, group, status = result

        if status != 'pending':
            print(f"Error: Request is already {status}")
            conn.close()
            return False

        denied_by = getpass.getuser()

        cursor.execute('''
            UPDATE access_requests
            SET status = 'denied', approved_by = ?
            WHERE id = ?
        ''', (denied_by, request_id))

        conn.commit()
        conn.close()

        self.log(f"✗ Request denied by {denied_by}" + (f": {reason}" if reason else ""),
                 request_id=request_id, username=username, action='deny')

        self.send_notification(request_id, 'denial')

        return True

    def revoke_access(self, request_id, manual=True):
        """Revoke access and remove user from group"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT username, requested_group, status
            FROM access_requests WHERE id = ?
        ''', (request_id,))

        result = cursor.fetchone()

        if not result:
            print(f"Error: Request ID {request_id} not found")
            conn.close()
            return False

        username, group, status = result

        if status != 'approved':
            print(f"Error: Cannot revoke - request status is {status}")
            conn.close()
            return False

        # Remove user from group
        try:
            subprocess.run(['sudo', 'gpasswd', '-d', username, group], check=True)
            revoked_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            cursor.execute('''
                UPDATE access_requests
                SET status = 'revoked', revoked_at = ?
                WHERE id = ?
            ''', (revoked_at, request_id))

            conn.commit()

            action_type = 'manual_revoke' if manual else 'auto_revoke'
            self.log(f"✓ Access revoked: {username} removed from {group}",
                     request_id=request_id, username=username, action=action_type)

            # Send notification
            self.send_notification(request_id, 'revocation')

            print(f"✓ Access revoked for {username}")

        except subprocess.CalledProcessError as e:
            self.log(f"✗ Failed to revoke access: {str(e)}",
                     request_id=request_id, username=username, action='error')
            conn.close()
            return False

        conn.close()
        return True

    def schedule_revocation(self, request_id, username, group, duration_hours):
        """Schedule automatic revocation using 'at' command"""
        revoke_time = datetime.now() + timedelta(hours=duration_hours)

        # Create a script to revoke access
        script = f"""#!/bin/bash
python3 {os.path.abspath(__file__)} auto-revoke {request_id}
"""

        script_path = f"/tmp/revoke_{request_id}.sh"
        with open(script_path, 'w') as f:
            f.write(script)
        os.chmod(script_path, 0o755)

        # Schedule using 'at'
        try:
            at_time = revoke_time.strftime('%H:%M %Y-%m-%d')
            process = subprocess.Popen(['at', at_time],
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       text=True)
            stdout, stderr = process.communicate(input=script)

            self.log(f"⏰ Auto-revocation scheduled for {at_time}",
                     request_id=request_id, username=username, action='schedule')

        except Exception as e:
            self.log(f"Warning: Could not schedule auto-revocation: {str(e)}",
                     request_id=request_id, username=username, action='error')

    def list_requests(self, status=None, username=None):
        """List access requests"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        query = 'SELECT * FROM access_requests WHERE 1=1'
        params = []

        if status:
            query += ' AND status = ?'
            params.append(status)

        if username:
            query += ' AND username = ?'
            params.append(username)

        query += ' ORDER BY requested_at DESC'

        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()

        return results

    def display_requests(self, status=None, username=None):
        """Display formatted list of requests"""
        requests = self.list_requests(status, username)

        if not requests:
            print("No requests found")
            return

        print("\n" + "=" * 100)
        print(f"{'ID':<5} {'User':<15} {'Group':<10} {'Duration':<10} {'Status':<10} {'Requested':<20} {'Expires':<20}")
        print("=" * 100)

        for req in requests:
            req_id, username, group, duration, reason, status, requested_by, requested_at, \
                approved_by, approved_at, expires_at, revoked_at, emergency = req

            emergency_flag = "🚨 " if emergency else ""

            print(f"{emergency_flag}{req_id:<5} {username:<15} {group:<10} {duration}h{'':<7} "
                  f"{status:<10} {requested_at:<20} {expires_at or 'N/A':<20}")

    def check_expired(self):
        """Check for expired access and revoke automatically"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute('''
            SELECT id FROM access_requests
            WHERE status = 'approved' AND expires_at < ?
        ''', (now,))

        expired = cursor.fetchall()
        conn.close()

        for (request_id,) in expired:
            print(f"⏰ Revoking expired access: Request #{request_id}")
            self.revoke_access(request_id, manual=False)

    def send_notification(self, request_id, event_type):
        """Send email and Slack notifications"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM access_requests WHERE id = ?', (request_id,))
        req = cursor.fetchone()
        conn.close()

        if not req:
            return

        req_id, username, group, duration, reason, status, requested_by, requested_at, \
            approved_by, approved_at, expires_at, revoked_at, emergency = req

        # Prepare message
        if event_type == 'request':
            subject = f"🔐 Access Request: {username} → {group}"
            message = f"""
New Access Request {'(EMERGENCY)' if emergency else ''}

User: {username}
Group: {group}
Duration: {duration} hours
Reason: {reason}
Requested by: {requested_by}
Time: {requested_at}

Request ID: {req_id}
"""

        elif event_type == 'approval':
            subject = f"✅ Access Approved: {username} → {group}"
            message = f"""
Access Request Approved

User: {username}
Group: {group}
Duration: {duration} hours
Approved by: {approved_by}
Expires: {expires_at}

Request ID: {req_id}
"""

        elif event_type == 'denial':
            subject = f"❌ Access Denied: {username} → {group}"
            message = f"""
Access Request Denied

User: {username}
Group: {group}
Denied by: {approved_by}

Request ID: {req_id}
"""

        elif event_type == 'revocation':
            subject = f"🔒 Access Revoked: {username} → {group}"
            message = f"""
Access Revoked

User: {username}
Group: {group}
Revoked at: {revoked_at}

Request ID: {req_id}
"""

        # Send email
        if self.config['email_enabled']:
            self.send_email(subject, message)

        # Send Slack notification
        if self.config['slack_enabled']:
            self.send_slack(message)

    def send_email(self, subject, body):
        """Send email notification"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config['email_from']
            msg['To'] = self.config['email_to']
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port']) as server:
                server.starttls()
                server.login(self.config['email_from'], self.config['smtp_password'])
                server.send_message(msg)

            print(f"📧 Email sent: {subject}")
        except Exception as e:
            print(f"Failed to send email: {str(e)}")

    def send_slack(self, message):
        """Send Slack notification"""
        try:
            payload = {'text': message}
            response = requests.post(self.config['slack_webhook'], json=payload)

            if response.status_code == 200:
                print(f"💬 Slack notification sent")
            else:
                print(f"Failed to send Slack notification: {response.status_code}")
        except Exception as e:
            print(f"Failed to send Slack notification: {str(e)}")

    def configure(self):
        """Interactive configuration"""
        print("\n=== Temporary Access Granter Configuration ===\n")

        # Email settings
        enable_email = input("Enable email notifications? (y/n): ").lower() == 'y'
        if enable_email:
            self.config['email_enabled'] = True
            self.config['email_to'] = input("Recipient email: ")
            self.config['email_from'] = input("Sender email: ")
            self.config['smtp_password'] = input("SMTP password: ")

        # Slack settings
        enable_slack = input("\nEnable Slack notifications? (y/n): ").lower() == 'y'
        if enable_slack:
            self.config['slack_enabled'] = True
            self.config['slack_webhook'] = input("Slack webhook URL: ")

        # Access settings
        self.config['approval_required'] = input("\nRequire approval for requests? (y/n): ").lower() == 'y'

        max_hours = input("Maximum duration in hours (default 24): ") or "24"
        self.config['max_duration_hours'] = int(max_hours)

        # Allowed groups
        print("\nCurrent allowed groups:", ', '.join(self.config['allowed_groups']))
        update_groups = input("Update allowed groups? (y/n): ").lower() == 'y'
        if update_groups:
            groups = input("Enter groups (comma-separated): ")
            self.config['allowed_groups'] = [g.strip() for g in groups.split(',')]

        self.save_config(self.config)
        print("\n✓ Configuration saved!")


def main():
    import sys

    granter = TemporaryAccessGranter()

    if len(sys.argv) < 2:
        print("Usage: python temp_access_granter.py [command]")
        print("\nCommands:")
        print("  request <user> <group> <hours> <reason>  - Request temporary access")
        print("  request-emergency <user> <group> <hours> - Emergency access request")
        print("  approve <request_id>                      - Approve a request")
        print("  deny <request_id> [reason]                - Deny a request")
        print("  revoke <request_id>                       - Manually revoke access")
        print("  list [status] [username]                  - List requests")
        print("  check-expired                             - Check and revoke expired access")
        print("  configure                                 - Configure settings")
        print("  auto-revoke <request_id>                  - Auto-revoke (internal use)")
        return

    command = sys.argv[1]

    if command == 'request':
        if len(sys.argv) < 6:
            print("Usage: request <user> <group> <hours> <reason>")
            return

        username = sys.argv[2]
        group = sys.argv[3]
        hours = int(sys.argv[4])
        reason = ' '.join(sys.argv[5:])

        request_id = granter.request_access(username, group, hours, reason)
        if request_id:
            print(f"\n✓ Request created with ID: {request_id}")

    elif command == 'request-emergency':
        if len(sys.argv) < 5:
            print("Usage: request-emergency <user> <group> <hours>")
            return

        username = sys.argv[2]
        group = sys.argv[3]
        hours = int(sys.argv[4])
        reason = "EMERGENCY ACCESS"

        request_id = granter.request_access(username, group, hours, reason, emergency=True)
        if request_id:
            print(f"\n✓ Emergency request created with ID: {request_id}")

    elif command == 'approve':
        if len(sys.argv) < 3:
            print("Usage: approve <request_id>")
            return

        request_id = int(sys.argv[2])
        granter.approve_request(request_id)

    elif command == 'deny':
        if len(sys.argv) < 3:
            print("Usage: deny <request_id> [reason]")
            return

        request_id = int(sys.argv[2])
        reason = ' '.join(sys.argv[3:]) if len(sys.argv) > 3 else None
        granter.deny_request(request_id, reason)

    elif command == 'revoke':
        if len(sys.argv) < 3:
            print("Usage: revoke <request_id>")
            return

        request_id = int(sys.argv[2])
        granter.revoke_access(request_id, manual=True)

    elif command == 'auto-revoke':
        if len(sys.argv) < 3:
            return

        request_id = int(sys.argv[2])
        granter.revoke_access(request_id, manual=False)

    elif command == 'list':
        status = sys.argv[2] if len(sys.argv) > 2 else None
        username = sys.argv[3] if len(sys.argv) > 3 else None
        granter.display_requests(status, username)

    elif command == 'check-expired':
        granter.check_expired()

    elif command == 'configure':
        granter.configure()

    else:
        print(f"Unknown command: {command}")


if __name__ == '__main__':
    main()