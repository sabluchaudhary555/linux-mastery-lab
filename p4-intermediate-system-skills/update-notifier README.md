# System Update Notifier & Scheduler

A powerful Python utility that monitors system updates, sends notifications, and can automatically schedule updates across multiple Linux distributions. Keep your system secure and up-to-date with minimal manual intervention.

## 🚀 Features

- **Multi-Distribution Support**: Debian/Ubuntu (APT), RHEL/Fedora (DNF), Arch Linux (Pacman), openSUSE (Zypper)
- **Desktop Notifications**: Get notified about available updates via system notifications
- **Email Alerts**: Receive detailed email reports about pending updates
- **Automatic Updates**: Schedule unattended updates at your preferred time
- **Daemon Mode**: Run continuously in the background to monitor for updates
- **Configurable**: Easy-to-use interactive configuration
- **Detailed Logging**: All activities logged for audit and troubleshooting

## 📋 Requirements

- Python 3.6+
- Linux-based operating system
- `notify-send` for desktop notifications (usually pre-installed)
- SMTP access for email notifications (optional)
- Root/sudo access for automatic updates

## 🔧 Installation

1. Download the script:
```bash
wget https://raw.githubusercontent.com/yourusername/update-notifier/main/update_notifier.py
chmod +x update_notifier.py
```

2. Install system dependencies (if needed):
```bash
# For desktop notifications (usually already installed)
sudo apt install libnotify-bin  # Debian/Ubuntu
sudo dnf install libnotify       # Fedora
sudo pacman -S libnotify         # Arch
```

## 📖 Usage

### Basic Commands

```bash
# Check for updates once
python3 update_notifier.py check

# Run in daemon mode (continuous monitoring)
python3 update_notifier.py daemon

# Configure settings interactively
python3 update_notifier.py configure

# Perform system update now
sudo python3 update_notifier.py update
```

### Command Reference

| Command | Description | Requires Sudo |
|---------|-------------|---------------|
| `check` | Check for available updates once | No |
| `daemon` | Run as background daemon | No* |
| `configure` | Interactive configuration setup | No |
| `update` | Perform system update immediately | Yes |

*Daemon mode doesn't require sudo for checking, but auto-updates do

## ⚙️ Configuration

### Interactive Setup

Run the configuration wizard:
```bash
python3 update_notifier.py configure
```

You'll be prompted for:
1. **Email Notifications**
   - Enable/disable email alerts
   - Recipient email address
   - Sender email address
   - SMTP password

2. **Automatic Updates**
   - Enable/disable auto-updates
   - Preferred update time (24-hour format)

3. **Check Interval**
   - How often to check for updates (in minutes)

### Configuration File

Settings are stored in:
```
~/.update_notifier_config.json
```

Example configuration:
```json
{
  "email_enabled": true,
  "email_to": "admin@example.com",
  "email_from": "updates@example.com",
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "smtp_password": "your_app_password",
  "check_interval": 3600,
  "auto_update_enabled": true,
  "auto_update_time": "03:00"
}
```

## 📧 Email Setup

### Gmail Configuration

1. Enable 2-factor authentication on your Google account
2. Generate an App Password:
   - Go to Google Account Settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. Use the generated password in the configuration

### Other Email Providers

Update SMTP settings in the config file:
```json
{
  "smtp_server": "smtp.yourprovider.com",
  "smtp_port": 587
}
```

## 📊 Example Output

### Check Command
```
Checking for updates on debian system...

Distribution: Debian/Ubuntu
Available updates: 23

Packages:
  - linux-image-generic
  - firefox
  - python3-pip
  - nginx
  - docker-ce
  ...
```

### Email Notification
```
Subject: System Updates Available: 23 package(s)

System Update Notification
--------------------------------------------------

Distribution: Debian/Ubuntu
Available Updates: 23

Packages:
  - linux-image-generic
  - firefox
  - python3-pip
  ...

Time: 2024-01-20 14:30:00
```

## 🔄 Daemon Mode

Run the notifier as a background service:

### Manual Start
```bash
# Start in background
nohup python3 update_notifier.py daemon > /dev/null 2>&1 &

# Stop
pkill -f update_notifier.py
```

### Systemd Service (Recommended)

Create `/etc/systemd/system/update-notifier.service`:
```ini
[Unit]
Description=System Update Notifier
After=network.target

[Service]
Type=simple
User=your_username
ExecStart=/usr/bin/python3 /path/to/update_notifier.py daemon
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable update-notifier
sudo systemctl start update-notifier
```

Check status:
```bash
sudo systemctl status update-notifier
```

## 📝 Logging

All activities are logged to:
```
~/.update_notifier.log
```

Example log entries:
```
[2024-01-20 14:30:15] Checking for updates on debian system...
[2024-01-20 14:30:18] Desktop notification sent: 23 update(s) available
[2024-01-20 14:30:20] Email notification sent to admin@example.com
[2024-01-21 03:00:00] Starting automatic system update...
[2024-01-21 03:05:32] System update completed successfully
```

## 💡 Use Cases

1. **Security Compliance**: Ensure systems are always updated
2. **Minimal Downtime**: Schedule updates during off-hours
3. **Team Awareness**: Email notifications keep teams informed
4. **Audit Trail**: Detailed logs for compliance and troubleshooting
5. **Multi-Server Management**: Monitor multiple systems via email
6. **Desktop Users**: Get timely notifications without manual checks

## 🛠️ Advanced Usage

### Custom Update Schedule

For multiple daily checks, modify `check_interval`:
```python
# Check every 4 hours
"check_interval": 14400  # seconds
```

### Conditional Auto-Updates

Only update if less than N packages:
```python
# In perform_update method, add:
if update_info['count'] > 50:
    self.log("Too many updates, skipping auto-update")
    return False
```

### Whitelist/Blacklist Packages

Modify the check methods to filter packages:
```python
blacklist = ['linux-kernel', 'nvidia-driver']
packages = [p for p in packages if p not in blacklist]
```

## 🔒 Security Considerations

- **SMTP Password**: Store securely, use app-specific passwords
- **Automatic Updates**: Test in non-production environments first
- **Log File**: Contains system information, protect appropriately
- **Sudo Access**: Required for auto-updates, configure sudo timeout appropriately

## 🐛 Troubleshooting

### Notifications Not Appearing
```bash
# Test notify-send manually
notify-send "Test" "This is a test"

# Install if missing
sudo apt install libnotify-bin
```

### Email Failures
- Verify SMTP credentials
- Check firewall/network connectivity
- Use app-specific passwords for Gmail
- Enable "Less secure app access" if needed (not recommended)

### Permission Errors During Auto-Update
```bash
# Configure passwordless sudo for update commands
sudo visudo
# Add: username ALL=(ALL) NOPASSWD: /usr/bin/apt upgrade
```

### Daemon Not Starting
```bash
# Check logs
tail -f ~/.update_notifier.log

# Run in foreground for debugging
python3 update_notifier.py daemon
```

## 📋 Supported Update Commands

| Distribution | Check Command | Update Command |
|--------------|---------------|----------------|
| Debian/Ubuntu | `apt list --upgradable` | `apt upgrade -y` |
| RHEL/Fedora | `dnf check-update` | `dnf upgrade -y` |
| Arch Linux | `pacman -Qu` | `pacman -Syu --noconfirm` |
| openSUSE | `zypper list-updates` | `zypper update -y` |

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Add support for more distributions
- Implement package filtering
- Add webhook notifications
- Create web dashboard
- Add rollback functionality

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

Built for system administrators who value automation and reliability

## 🔗 Related Tools

- Package Installation History Tracker (companion tool)
- System monitoring solutions
- Configuration management tools

## ⚠️ Disclaimer

Automatic updates can occasionally cause system issues. Always:
- Test in non-production environments first
- Maintain regular backups
- Review update logs periodically
- Keep a recovery plan ready

---

**Happy Learning! 🚀**

*Contributions and suggestions are welcome!*

---

**Maintained by: [Sablu Chaudhary](https://github.com/sabluchaudhary555)** 🔗 **Connect with me:** [LinkedIn](https://www.linkedin.com/in/sablu-chaudhary555/) | [GitHub](https://github.com/sabluchaudhary555)

---
**Made with ❤️ for the Open Source Community**