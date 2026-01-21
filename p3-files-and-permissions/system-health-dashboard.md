# System Health Dashboard - Linux FHS Monitor

A real-time Python dashboard that monitors system resources and Linux Filesystem Hierarchy Standard (FHS) directories with continuous updates.

## Overview

This tool provides a comprehensive view of your Linux system's health by monitoring CPU, memory, disk usage, and key FHS directories. It displays everything in a clean, auto-refreshing terminal dashboard.

## Features

- **Real-Time System Monitoring** - CPU, memory, and disk usage with progress bars
- **FHS Directory Tracking** - Monitors critical Linux directories
- **Log Activity** - Shows recently modified files in `/var/log`
- **Auto-Refresh** - Continuous updates every 5 seconds
- **Visual Progress Bars** - Easy-to-read resource utilization
- **Human-Readable Sizes** - Automatic conversion to KB, MB, GB, TB
- **Timestamp Display** - Know exactly when data was collected

## Installation

1. Save the script as `system-health-dashboard.py`
2. Install required dependency:
```bash
pip3 install psutil
```
3. Make it executable:
```bash
chmod +x system-health-dashboard.py
```

## Usage

### Standard Mode (Limited Access)
```bash
python3 system-health-dashboard.py
```

### Full Access Mode (Recommended)
```bash
sudo python3 system-health-dashboard.py
```

### Direct Execution
```bash
sudo ./system-health-dashboard.py
```

> **Note:** Root privileges are recommended for full access to all monitored directories.

## Dashboard Sections

### 1. System Resources
Displays real-time metrics:
```
CPU Usage:    [████████░░░░░░░░░░░░] 35.2%
Memory:       [████████████░░░░░░░░] 62.8%
              4.12 GB / 8.00 GB
Disk Usage:   [██████████████░░░░░░] 68.5%
              142.45 GB / 256.00 GB
```

### 2. Monitored Directories (FHS)
Tracks key Linux filesystem locations:

| Directory | Description | Purpose |
|-----------|-------------|---------|
| `/var/log` | System Logs | Application and system log files |
| `/tmp` | Temporary Files | Temporary data storage |
| `/home` | User Home Directories | User personal files |
| `/var/cache` | Cache Files | Application cache data |
| `/var/spool` | Spool Files | Print jobs, mail queues |
| `/etc` | Configuration Files | System configuration |

### 3. Recent Log Activity
Shows the 5 most recently modified log files:
```
• syslog                        (Modified: 2026-01-17 14:23:45)
• auth.log                      (Modified: 2026-01-17 14:20:12)
• kern.log                      (Modified: 2026-01-17 14:15:03)
```

## What Gets Monitored

### System Metrics
- **CPU Usage** - Current processor utilization percentage
- **Memory Usage** - RAM consumption (used/total)
- **Disk Usage** - Root filesystem space (used/free/total)

### Directory Statistics
For each monitored directory:
- Total size in human-readable format
- Number of files contained
- Number of subdirectories
- Accessibility status

## Requirements

- **OS:** Linux (designed for Linux FHS)
- **Python:** 3.6 or higher
- **Dependencies:** 
  - `psutil` - System and process utilities
  - Standard library: `os`, `shutil`, `time`, `datetime`, `collections`

## Installation of Dependencies

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install python3-psutil
```

### Fedora/RHEL
```bash
sudo dnf install python3-psutil
```

### Using pip
```bash
pip3 install psutil
```

## Understanding the Output

### Progress Bars
- `█` - Filled portion (used resources)
- `░` - Empty portion (available resources)
- Percentage shown on the right

### Directory Sizes
- Automatically converts to appropriate units
- Shows total size of all files recursively
- Counts files and directories

### Colors
Progress bars fill based on resource usage intensity.

## Use Cases

- **System Administration** - Monitor server health
- **Performance Tuning** - Identify resource bottlenecks
- **Disk Management** - Track directory growth
- **Log Monitoring** - Stay aware of recent system activity
- **Server Dashboards** - Quick visual system overview

## Customization

### Change Refresh Interval
Edit the refresh interval in the code (default: 5 seconds):
```python
dashboard.run(refresh_interval=10)  # 10 seconds
```

### Add/Remove Directories
Modify the `monitored_dirs` dictionary:
```python
self.monitored_dirs = {
    '/your/custom/path': 'Custom Description',
    # Add more directories here
}
```

### Adjust Log File Limit
Change the number of recent logs shown:
```python
recent_logs = self.get_recent_logs(limit=10)  # Show 10 logs
```

## Keyboard Controls

- **Ctrl+C** - Stop dashboard and exit cleanly

## Troubleshooting

**"Permission denied" errors** - Run with `sudo` for full access

**"Module not found: psutil"** - Install psutil: `pip3 install psutil`

**Directories show "N/A"** - No permission to access; use sudo

**High CPU usage** - Increase refresh interval for slower updates

**Screen flickering** - Terminal may not support rapid screen clearing

## Performance Notes

- Scanning large directories (like `/home`) can be slow
- Root privileges improve access but increase security risk
- Dashboard refreshes consume some CPU resources
- Use longer refresh intervals on resource-constrained systems

## Security Considerations

- Running with sudo provides full system access
- Dashboard only reads data, doesn't modify files
- Be cautious when monitoring sensitive directories
- Log files may contain sensitive information

## Example Session

```bash
$ sudo python3 system-health-dashboard.py
Starting System Health Dashboard...
Gathering system information...

[Dashboard displays with auto-refresh]

Press Ctrl+C when done

^C
✓ Dashboard stopped. Goodbye!
```

## Linux FHS Reference

The tool monitors standard Linux Filesystem Hierarchy directories:
- **/var/log** - Logs from system and applications
- **/tmp** - Temporary files (cleared on reboot)
- **/home** - User personal directories
- **/var/cache** - Application cache data
- **/var/spool** - Queued data for processing
- **/etc** - System-wide configuration files

## License

Developed by SSoft.in

---

*Keep your Linux system healthy with real-time monitoring!*