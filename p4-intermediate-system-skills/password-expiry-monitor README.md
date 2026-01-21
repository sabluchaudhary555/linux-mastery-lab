# Password Expiration Notification System 🔐

A Python-based solution for monitoring Linux user password expiration dates and automatically sending notifications to users and administrators.

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)](https://www.linux.org/)

## ✨ Features

- 🔍 Scans all system users for password expiration dates
- 📧 Sends automated email alerts at configurable intervals (30, 14, 7, 3, 1 days)
- 📊 Generates detailed reports with urgency levels (EXPIRED, CRITICAL, HIGH, MEDIUM, LOW)
- 👤 Personalized user notifications with password change instructions
- 📈 Admin summary reports with system-wide statistics
- 📝 Activity logging for audit trails
- ⚙️ JSON-based configuration for easy customization

## 🔧 Prerequisites

- Linux system (Ubuntu, Debian, CentOS, RHEL)
- Python 3.6+
- Root/sudo access
- SMTP server for email notifications

## 📥 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/password-expiration-notifier.git
cd password-expiration-notifier

# Make executable
chmod +x password_expiry_monitor.py

# Create config file
cp config.example.json config.json
nano config.json  # Edit with your settings
```

## ⚙️ Configuration

Create `config.json`:

```json
{
    "warning_days": [30, 14, 7, 3, 1],
    "email": {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "sender_email": "admin@company.com",
        "sender_password": "your_app_password",
        "admin_email": "sysadmin@company.com"
    },
    "exclude_users": ["root", "daemon", "bin", "sys"],
    "log_file": "/var/log/password_expiry.log"
}
```

**For Gmail:** Enable 2FA and generate an [App Password](https://myaccount.google.com/apppasswords)

## 🚀 Usage

```bash
# Full scan with notifications
sudo python3 password_expiry_monitor.py

# Report only (no emails)
sudo python3 password_expiry_monitor.py --report-only

# Custom config file
sudo python3 password_expiry_monitor.py --config /path/to/config.json

# Skip email notifications
sudo python3 password_expiry_monitor.py --no-email
```

## 📊 Sample Output

```
======================================================================
PASSWORD EXPIRATION REPORT
Generated: 2025-01-21 10:30:45
======================================================================

Total Users: 25
Expired: 2
Critical (1-3 days): 3
High (4-7 days): 5
Medium (8-14 days): 8

EXPIRED PASSWORDS:
----------------------------------------------------------------------
  john                 Expired: Jan 15, 2025
  alice                Expired: Jan 18, 2025

CRITICAL (1-3 days):
----------------------------------------------------------------------
  bob                  Days left: 2     Expires: Jan 23, 2025
  charlie              Days left: 3     Expires: Jan 24, 2025
======================================================================
```

## ⏰ Automate with Cron

Run daily at 9:00 AM:

```bash
sudo crontab -e

# Add this line
0 9 * * * /usr/bin/python3 /path/to/password_expiry_monitor.py >> /var/log/password_expiry_cron.log 2>&1
```

## 🔍 How It Works

1. **Scans** `/etc/passwd` for users with UID ≥ 1000
2. **Retrieves** password info using `chage -l` and `passwd -S`
3. **Calculates** days until expiration
4. **Sends** personalized emails to users needing notifications
5. **Generates** admin summary report
6. **Logs** all activities for audit trail

## 📧 Email Examples

### User Notification
```
Subject: Password Expiration Warning - HIGH

Dear john,

Your password will expire in 5 day(s).

Password Details:
- Expires On: Jan 26, 2025
- Days Remaining: 5

To change your password:
1. Login and run: passwd
2. Follow the prompts

Best regards,
IT Security Team
```

### Admin Summary
```
Subject: Password Expiration Report - 2025-01-21

Total Users Scanned: 25
Users Needing Action: 18

- EXPIRED: 2
- CRITICAL (1-3 days): 3
- HIGH (4-7 days): 5
```

## 🛠️ Troubleshooting

**Permission denied error:**
```bash
sudo python3 password_expiry_monitor.py
```

**Email not sending:**
- Check SMTP credentials in config.json
- Verify firewall allows SMTP port (587)
- For Gmail, use App Password

**No users found:**
- Ensure users have UID ≥ 1000
- Check `/etc/passwd` permissions

**Log file errors:**
```bash
sudo touch /var/log/password_expiry.log
sudo chmod 644 /var/log/password_expiry.log
```

## 🔒 Security Notes

- Store `config.json` securely with restricted permissions: `chmod 600 config.json`
- Never commit passwords to version control (use `.gitignore`)
- Use app passwords instead of main email passwords
- Regularly review activity logs
- Run as root only when necessary

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request




**Happy Learning! 🚀**

*Contributions and suggestions are welcome!*

---

**Maintained by: [Sablu Chaudhary](https://github.com/sabluchaudhary555)** 🔗 **Connect with me:** [LinkedIn](https://www.linkedin.com/in/sablu-chaudhary555/) | [GitHub](https://github.com/sabluchaudhary555)

---
**Made with ❤️ for the Open Source Community**