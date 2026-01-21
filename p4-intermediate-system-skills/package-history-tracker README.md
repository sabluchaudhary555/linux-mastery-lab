# Package Installation History Tracker

A comprehensive Python tool for tracking, analyzing, and reporting package installation history across multiple Linux distributions. This utility helps system administrators and users maintain detailed records of package management operations.

## 🚀 Features

- **Multi-Distribution Support**: Works with Debian/Ubuntu (APT), RHEL/Fedora (DNF/YUM), Arch Linux (Pacman), and openSUSE (Zypper)
- **SQLite Database**: Stores all package history in a local database for fast querying
- **Comprehensive Tracking**: Records installations, upgrades, and removals with timestamps
- **Search Functionality**: Quickly find history for specific packages
- **Detailed Reports**: Generate comprehensive statistics and insights
- **JSON Export**: Export your package history for backup or analysis
- **Automatic Detection**: Automatically detects your Linux distribution

## 📋 Requirements

- Python 3.6+
- Linux-based operating system
- Root/sudo access (for reading system logs)
- SQLite3 (usually pre-installed)

## 🔧 Installation

1. Clone or download the script:
```bash
wget https://raw.githubusercontent.com/yourusername/package-history-tracker/main/package_history_tracker.py
chmod +x package_history_tracker.py
```

2. No additional dependencies required - uses Python standard library only!

## 📖 Usage

### Basic Commands

```bash
# Import package history from system logs
sudo python3 package_history_tracker.py import

# Search for a specific package
python3 package_history_tracker.py search firefox

# Show recently installed packages (last 7 days)
python3 package_history_tracker.py recent

# Show packages from last 30 days
python3 package_history_tracker.py recent 30

# Generate comprehensive report
python3 package_history_tracker.py report

# Export history to JSON
python3 package_history_tracker.py export
python3 package_history_tracker.py export my_history.json
```

### Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `import` | Import history from system logs | `sudo python3 package_history_tracker.py import` |
| `search <name>` | Search for package history | `python3 package_history_tracker.py search nginx` |
| `recent [days]` | Show recently installed packages | `python3 package_history_tracker.py recent 14` |
| `report` | Generate comprehensive report | `python3 package_history_tracker.py report` |
| `export [file]` | Export to JSON file | `python3 package_history_tracker.py export backup.json` |

## 📊 Example Output

### Search Results
```
History for 'firefox':
------------------------------------------------------------
[2024-01-15 10:30:45] INSTALL: v120.0-1 by john
[2024-01-10 14:22:30] UPGRADE: v119.0-1 by john
[2023-12-20 09:15:12] INSTALL: v118.0-1 by john
```

### Report Output
```
============================================================
PACKAGE INSTALLATION HISTORY REPORT
============================================================

Total Operations: 1,247

Operations by Type:
  Install: 856
  Upgrade: 324
  Remove: 67

Top 10 Most Installed/Updated Packages:
  python3: 45 times
  firefox: 32 times
  nginx: 28 times
  ...

Recent Activity (Last 10 Operations):
  [2024-01-20 08:30:15] INSTALL: docker-ce 24.0.7
  [2024-01-19 16:45:22] UPGRADE: linux-kernel 6.5.0
  ...
```

## 🗂️ Database Location

The package history is stored in:
```
~/.package_history.db
```

This SQLite database contains indexed tables for fast querying.

## 🔍 Supported Distributions

### Debian/Ubuntu (APT)
- Parses `/var/log/apt/history.log`
- Tracks install, upgrade, and remove operations
- Records package versions and architectures

### RHEL/Fedora/CentOS (DNF/YUM)
- Uses `dnf history` command
- Provides detailed transaction information
- Includes command-line history

### Arch Linux (Pacman)
- Parses `/var/log/pacman.log`
- Comprehensive ALPM operation tracking
- Real-time package state changes

### openSUSE (Zypper)
- Reads `/var/log/zypp/history`
- Detailed user and timestamp information
- Architecture-specific data

## 💡 Use Cases

1. **System Auditing**: Track what packages were installed and when
2. **Troubleshooting**: Identify when problematic packages were installed
3. **Compliance**: Maintain records for security audits
4. **Documentation**: Generate reports for system documentation
5. **Rollback Planning**: Understand package history before system changes
6. **Team Coordination**: Track who installed what in shared systems

## 🛠️ Advanced Usage

### Automated Imports
Set up a cron job to regularly import history:
```bash
# Add to crontab (crontab -e)
0 */6 * * * /usr/bin/python3 /path/to/package_history_tracker.py import
```

### Querying the Database Directly
```python
import sqlite3
conn = sqlite3.connect('~/.package_history.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM package_history WHERE action='install' LIMIT 10")
print(cursor.fetchall())
```

### Integration with Monitoring Tools
Export to JSON and integrate with monitoring systems:
```bash
python3 package_history_tracker.py export | curl -X POST -d @- https://monitoring.example.com/api/packages
```

## 🔒 Permissions

- **Import**: Requires sudo/root access to read system log files
- **Search/Report/Export**: Regular user permissions (reads from local database)

## 🐛 Troubleshooting

**Permission Denied Error**
```bash
# Use sudo for import command
sudo python3 package_history_tracker.py import
```

**No Log Files Found**
- Ensure you're running on a supported distribution
- Check if log rotation has cleared old logs
- Verify log file paths exist

**Empty Results**
- First run `import` to populate the database
- Check if you have package management history on your system

## 📝 Data Schema

```sql
CREATE TABLE package_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    action TEXT,
    package_name TEXT,
    version TEXT,
    dependencies TEXT,
    user TEXT,
    distro TEXT,
    size_kb INTEGER
)
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add support for more distributions
- Improve parsing accuracy
- Add new report formats
- Enhance search capabilities


**Happy Learning! 🚀**

*Contributions and suggestions are welcome!*

---

**Maintained by: [Sablu Chaudhary](https://github.com/sabluchaudhary555)** 🔗 **Connect with me:** [LinkedIn](https://www.linkedin.com/in/sablu-chaudhary555/) | [GitHub](https://github.com/sabluchaudhary555)

---
**Made with ❤️ for the Open Source Community**