# Temporary Access Granter

A Python-based system for granting time-limited elevated permissions with automatic revocation, approval workflows, and comprehensive notifications.

## 🚀 Features

- ⏰ **Time-Limited Access** - Grant temporary group memberships that auto-expire
- ✅ **Approval Workflow** - Request/approve/deny access flow
- 🔔 **Notifications** - Email and Slack alerts for all events
- 📊 **Audit Logging** - Complete tracking of all access requests and changes
- 🚨 **Emergency Access** - Fast-track critical access requests
- 🔄 **Auto-Revocation** - Scheduled automatic permission removal

## 📋 Requirements

- Python 3.6+
- Linux system with sudo access
- `at` command (for scheduled revocation)
- SQLite3 (pre-installed on most systems)

```bash
# Install 'at' if needed
sudo apt install at              # Debian/Ubuntu
sudo dnf install at              # RHEL/Fedora
sudo pacman -S at                # Arch Linux

# Enable and start atd service
sudo systemctl enable atd
sudo systemctl start atd
```

## 🔧 Installation

```bash
# Download the script
wget https://raw.githubusercontent.com/yourusername/temp-access-granter/main/temp_access_granter.py
chmod +x temp_access_granter.py

# Initial configuration
python3 temp_access_granter.py configure
```

## 📖 Usage

### Configuration

```bash
python3 temp_access_granter.py configure
```

Configure:
- Email notifications (SMTP settings)
- Slack webhooks
- Approval requirements
- Maximum access duration
- Allowed groups (sudo, wheel, admin, etc.)

### Request Access

```bash
# Standard request
python3 temp_access_granter.py request <username> <group> <hours> <reason>

# Example: Request sudo access for 4 hours
python3 temp_access_granter.py request john sudo 4 "Need to install development tools"

# Emergency access (auto-approved if configured)
python3 temp_access_granter.py request-emergency alice wheel 2
```

### Manage Requests

```bash
# Approve a request
python3 temp_access_granter.py approve <request_id>

# Deny a request
python3 temp_access_granter.py deny <request_id> "Reason for denial"

# Manually revoke active access
python3 temp_access_granter.py revoke <request_id>
```

### Monitor Access

```bash
# List all requests
python3 temp_access_granter.py list

# List by status
python3 temp_access_granter.py list pending
python3 temp_access_granter.py list approved

# List by username
python3 temp_access_granter.py list "" john

# Check and revoke expired access
python3 temp_access_granter.py check-expired
```

## 📊 Example Workflow

```bash
# 1. User requests sudo access
$ python3 temp_access_granter.py request bob sudo 8 "Database maintenance"
✓ Request created with ID: 1
📧 Email sent: 🔐 Access Request: bob → sudo

# 2. Admin approves request
$ python3 temp_access_granter.py approve 1
✓ User bob added to group sudo
✓ Access approved for bob
  Group: sudo
  Duration: 8 hours
  Expires: 2024-01-21 18:30:00
⏰ Auto-revocation scheduled

# 3. After 8 hours - automatic revocation
[Auto-revoke runs via 'at' command]
✓ Access revoked: bob removed from sudo
📧 Email sent: 🔒 Access Revoked: bob → sudo
```

## 🔔 Notifications

### Email Notifications
Sent for:
- ✉️ New access requests
- ✅ Request approvals
- ❌ Request denials
- 🔒 Access revocations

### Slack Notifications
Real-time updates to configured Slack channel via webhook.

## 📁 File Locations

- **Database**: `~/.temp_access.db`
- **Config**: `~/.temp_access_config.json`
- **Logs**: `/var/log/temp_access.log`

## 🔒 Security Features

- **Approval workflow** prevents unauthorized access
- **Maximum duration limits** prevent indefinite access
- **Audit logging** tracks all activities
- **Automatic revocation** ensures no forgotten permissions
- **Emergency override** with full logging
- **Configurable allowed groups** restricts privilege scope

## 💡 Use Cases

1. **Developer Access** - Temporary sudo for deployments
2. **Contractor Work** - Limited-time access for external staff
3. **Incident Response** - Emergency access with full audit trail
4. **Training/Testing** - Temporary elevated permissions for learning
5. **Compliance** - Meet "just-in-time" access requirements

## 🛠️ Advanced Usage

### Automated Expiry Checks (Cron)

```bash
# Add to crontab (crontab -e)
*/30 * * * * /usr/bin/python3 /path/to/temp_access_granter.py check-expired
```

### Email Setup (Gmail)

1. Enable 2FA on Google account
2. Generate App Password (Security → App passwords)
3. Use app password in configuration

### View Database Directly

```bash
sqlite3 ~/.temp_access.db "SELECT * FROM access_requests;"
```

## 📝 Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `request` | Create access request | `request john sudo 4 "reason"` |
| `request-emergency` | Emergency request | `request-emergency alice wheel 2` |
| `approve` | Approve pending request | `approve 1` |
| `deny` | Deny request | `deny 1 "not authorized"` |
| `revoke` | Manually revoke access | `revoke 1` |
| `list` | List requests | `list pending` |
| `check-expired` | Revoke expired access | `check-expired` |
| `configure` | Interactive setup | `configure` |

## 🐛 Troubleshooting

**"Permission denied" errors**
```bash
# Run with sudo for user/group modifications
sudo python3 temp_access_granter.py approve 1
```

**Auto-revocation not working**
```bash
# Check if atd service is running
sudo systemctl status atd

# View scheduled jobs
atq
```

**Email not sending**
- Verify SMTP credentials
- Check firewall settings
- For Gmail: Use app-specific password

**"Group not allowed" error**
- Add group to allowed list via `configure`
- Or edit `~/.temp_access_config.json` manually




**Happy Learning! 🚀**

*Contributions and suggestions are welcome!*

---

**Maintained by: [Sablu Chaudhary](https://github.com/sabluchaudhary555)** 🔗 **Connect with me:** [LinkedIn](https://www.linkedin.com/in/sablu-chaudhary555/) | [GitHub](https://github.com/sabluchaudhary555)

---
**Made with ❤️ for the Open Source Community**