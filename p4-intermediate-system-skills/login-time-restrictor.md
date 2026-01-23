# Login Time Restrictor

Restrict user login times based on customizable schedules. Perfect for managing contractor access, enforcing work hours, or implementing security policies.

## 🚀 Features

- ⏰ Set allowed login hours (e.g., 09:00-17:00)
- 📅 Restrict login days (weekdays, weekends, specific days)
- 🔒 Automatic account enable/disable based on schedule
- ✅ Real-time access checking
- 📊 List all configured restrictions
- 🔄 Toggle restrictions without removing them

## 📋 Requirements

- Python 3.6+
- Linux system with PAM support
- Sudo access for user account modifications
- `pam_time` module (usually pre-installed)

## 🔧 Installation

```bash
# Download the script
wget https://raw.githubusercontent.com/yourusername/login-time-restrictor/main/login_time_restrictor.py
chmod +x login_time_restrictor.py

# Ensure PAM time module is enabled
sudo nano /etc/pam.d/common-account
# Add this line if not present:
# account required pam_time.so
```

## 📖 Usage

### Set Time Restriction

```bash
# Restrict to business hours, Monday-Friday
python3 login_time_restrictor.py set john 09:00-17:00 Mon-Fri

# Allow extended hours, all week
python3 login_time_restrictor.py set alice 08:00-20:00 Mon-Sun

# Weekend access only
python3 login_time_restrictor.py set bob 00:00-23:59 Sat,Sun
```

### Check Current Access

```bash
# Check if user can login right now
python3 login_time_restrictor.py check john

# Output examples:
# ✓ john CAN login: Access allowed
# ✗ john CANNOT login: Outside allowed hours (09:00-17:00)
```

### Manage Restrictions

```bash
# List all restrictions
python3 login_time_restrictor.py list

# Remove restriction
python3 login_time_restrictor.py remove john

# Temporarily disable (without removing)
python3 login_time_restrictor.py toggle john
```

### Manual Account Control

```bash
# Manually enable account
python3 login_time_restrictor.py enable john

# Manually disable account
python3 login_time_restrictor.py disable john
```

### Enforce All Restrictions

```bash
# Check all users and enforce restrictions now
python3 login_time_restrictor.py enforce
```

## 📊 Example Output

### List Restrictions
```
============================================================
LOGIN TIME RESTRICTIONS
============================================================

john:
  Hours: 09:00-17:00
  Days: Mon-Fri
  Status: ✓ Enabled
  Current: Access allowed

alice:
  Hours: 08:00-20:00
  Days: Mon-Sun
  Status: ✓ Enabled
  Current: Access allowed

bob:
  Hours: 00:00-23:59
  Days: Sat,Sun
  Status: ✗ Disabled
  Current: Day Mon not allowed
```

### Enforce Restrictions
```
============================================================
ENFORCING LOGIN TIME RESTRICTIONS
============================================================

✓ john: Access allowed
✗ alice: Outside allowed hours (08:00-20:00)
✓ bob: Access allowed
```

## ⏰ Automated Enforcement

Set up cron job to automatically enforce restrictions:

```bash
# Edit crontab
crontab -e

# Add entry to check every 15 minutes
*/15 * * * * /usr/bin/python3 /path/to/login_time_restrictor.py enforce

# Or check at specific times (e.g., 9 AM and 5 PM)
0 9,17 * * * /usr/bin/python3 /path/to/login_time_restrictor.py enforce
```

## 📁 File Locations

- **Configuration**: `~/.login_time_config.json`
- **PAM Config**: `/etc/security/time.conf`
- **PAM Module**: `/etc/pam.d/common-account`

## 🎯 Use Cases

1. **Contractor Management** - Restrict access to contract hours only
2. **Security Compliance** - Enforce work-hour only access policies
3. **Cost Control** - Limit system usage to business hours
4. **Temporary Access** - Grant weekend-only access for maintenance
5. **Student Labs** - Control lab access hours in educational settings

## 📝 Time Format Examples

### Hours Format
- `09:00-17:00` - 9 AM to 5 PM
- `08:00-20:00` - 8 AM to 8 PM
- `00:00-23:59` - All day
- `06:00-14:00` - Morning shift
- `14:00-22:00` - Evening shift

### Days Format
- `Mon-Fri` - Weekdays only
- `Mon-Sun` - All days
- `Sat,Sun` - Weekends only
- `Mon,Wed,Fri` - Specific days
- `Tue,Thu` - Alternate days

## 🔒 Security Features

- Uses PAM (Pluggable Authentication Module) for enforcement
- Account locking via `usermod -L` (preserves data, only locks login)
- Audit trail in configuration file
- Real-time access verification
- No password storage or modification

## 🐛 Troubleshooting

**Restrictions not enforcing**
```bash
# Check if PAM time module is enabled
grep pam_time /etc/pam.d/common-account

# If missing, add:
sudo sh -c 'echo "account required pam_time.so" >> /etc/pam.d/common-account'
```

**User can still login**
```bash
# Verify restriction is active
python3 login_time_restrictor.py list

# Manually enforce
python3 login_time_restrictor.py enforce

# Check PAM time.conf
sudo cat /etc/security/time.conf
```

**Permission errors**
```bash
# Need sudo for account modifications
sudo python3 login_time_restrictor.py enforce
```

## ⚙️ Advanced Configuration

### Custom PAM Time Format

The script automatically converts to PAM time.conf format:
```
# Format: service;tty;user;times;days
login;*;john;0900-1700;Wk
```

Where:
- `Wk` = Weekdays (Mon-Fri)
- `Wd` = Weekend (Sat-Sun)
- `Al` = All days

### Integration with Other Tools

```python
# Import as module
from login_time_restrictor import LoginTimeRestrictor

restrictor = LoginTimeRestrictor()
restrictor.set_restriction('bob', '09:00-17:00', 'Mon-Fri')
allowed, reason = restrictor.check_current_access('bob')
```

## 📋 Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `set` | Create/update restriction | `set john 09:00-17:00 Mon-Fri` |
| `remove` | Delete restriction | `remove john` |
| `check` | Check current access | `check john` |
| `enable` | Enable user account | `enable john` |
| `disable` | Disable user account | `disable john` |
| `enforce` | Apply all restrictions | `enforce` |
| `list` | Show all restrictions | `list` |
| `toggle` | Enable/disable restriction | `toggle john` |

## ⚠️ Important Notes

- Changes require sudo for user account modifications
- Existing logged-in sessions are not affected (only new logins)
- Use `who` command to check currently logged-in users
- Test thoroughly before deploying in production
- Keep emergency admin account unrestricted

## 🤝 Contributing

Contributions welcome! Ideas:
- Web interface for management
- Email notifications on access violations
- Integration with LDAP/Active Directory
- Mobile app for emergency overrides
- Detailed access logs and reports


**Security Tip**: Always maintain at least one unrestricted admin account for emergency access!




**Happy Learning! 🚀**

*Contributions and suggestions are welcome!*

---

**Maintained by: [Sablu Chaudhary](https://github.com/sabluchaudhary555)** 🔗 **Connect with me:** [LinkedIn](https://www.linkedin.com/in/sablu-chaudhary555/) | [GitHub](https://github.com/sabluchaudhary555)

---
**Made with ❤️ for the Open Source Community**