# Real-Time Log Monitor Dashboard

A powerful terminal-based dashboard for monitoring system logs in real-time with color-coded severity levels, filtering, and multi-log split view capabilities.

## 🚀 Features

- 📊 **Real-Time Monitoring** - Live log tailing like `tail -f` but better
- 🎨 **Color-Coded Severity** - Errors in red, warnings in yellow, info in green
- 🔍 **Pattern Filtering** - Filter logs by keywords or regex patterns
- 🚨 **Alert System** - Highlight lines matching alert patterns
- ⏸️ **Pause/Resume** - Freeze display to read without stopping collection
- 📂 **Multi-Log Support** - Monitor multiple log files simultaneously
- 🪟 **Split View** - View two logs side-by-side
- 💻 **Terminal UI** - Beautiful ncurses-based interface
- 🔄 **Auto-Scroll** - Always shows latest entries

## 📋 Requirements

- Python 3.6+
- Linux/Unix system with `/var/log` directory
- Read access to log files (usually requires sudo)
- Terminal with color support

```bash
# Verify Python version
python3 --version

# Check if ncurses is available (usually pre-installed)
python3 -c "import curses; print('curses available')"
```

## 🔧 Installation

```bash
# Download the script
wget https://raw.githubusercontent.com/yourusername/realtime-log-monitor/main/realtime_log_monitor.py
chmod +x realtime_log_monitor.py

# Run with sudo (required for log file access)
sudo python3 realtime_log_monitor.py
```

## 📖 Usage

### Basic Monitoring

```bash
# Start the monitor
sudo python3 realtime_log_monitor.py
```

### Keyboard Commands

| Key | Action | Description |
|-----|--------|-------------|
| `q` | Quit | Exit the application |
| `p` | Pause/Resume | Freeze/unfreeze the display |
| `f` | Filter | Enter a filter pattern |
| `n` | Next Log | Switch to next log file |
| `a` | Add Alert | Add an alert pattern |
| `c` | Clear | Clear current log view |
| `s` | Split View | Toggle split view mode |
| `h` | Help | Show help screen |

## 🎨 Color Coding

The monitor automatically color-codes log entries based on severity:

| Color | Severity | Keywords |
|-------|----------|----------|
| 🔴 **Red** | ERROR/CRITICAL | ERROR, FATAL, CRITICAL, FAILED |
| 🟡 **Yellow** | WARNING | WARN, WARNING |
| 🟢 **Green** | INFO/SUCCESS | INFO, SUCCESS, OK |
| 🔵 **Cyan** | DEBUG | DEBUG |
| 🟣 **Magenta** | ALERT | Matches alert patterns |

## 📊 Interface Layout

```
┌─────────────────────────────────────────────────────────┐
│        Real-Time Log Monitor Dashboard                  │
│ MONITORING | Filter: ssh | Logs: 4                      │
│ Viewing: syslog                                         │
├─────────────────────────────────────────────────────────┤
│ [10:30:15] Jan 24 10:30:15 server sshd[1234]: ...      │
│ [10:30:16] Jan 24 10:30:16 server kernel: ...          │
│ [10:30:17] ERROR: Connection failed to database        │
│ [10:30:18] WARNING: Disk usage above 80%               │
│ [10:30:19] INFO: Service started successfully          │
│ ...                                                      │
├─────────────────────────────────────────────────────────┤
│ q:Quit | p:Pause | f:Filter | n:Next | a:Alert | h:Help│
└─────────────────────────────────────────────────────────┘
```

## 🔍 Filtering Logs

### Set a Filter

1. Press `f` to enter filter mode
2. Type your search pattern (e.g., "ssh", "error", "192.168")
3. Press Enter
4. Only matching lines will be displayed

### Example Filters
- `ssh` - Show only SSH-related entries
- `error` - Show only lines containing "error"
- `192.168.1.100` - Show entries from specific IP
- `Failed password` - Show failed login attempts

### Clear Filter
- Press `f` and leave empty, then Enter

## 🚨 Alert Patterns

Alerts highlight important patterns in **magenta/purple** color.

### Add Alert Pattern

1. Press `a` to add alert
2. Enter pattern (e.g., "unauthorized", "attack", "denied")
3. Press Enter
4. Matching lines will be highlighted

### Example Alert Patterns
- `Failed password` - Highlight failed logins
- `error|critical` - Regex for multiple terms
- `denied` - Show denied access attempts
- `out of memory` - Memory issues

## 🪟 Split View Mode

View two logs simultaneously in split-screen mode.

```bash
# Press 's' to toggle split view
```

```
┌──────────────────────────┬──────────────────────────┐
│ syslog                   │ auth.log                 │
├──────────────────────────┼──────────────────────────┤
│ [10:30] System started   │ [10:30] SSH login: user  │
│ [10:31] Service ready    │ [10:31] Session opened   │
│ [10:32] All systems go   │ [10:32] Command executed │
│ ...                      │ ...                      │
└──────────────────────────┴──────────────────────────┘
```

## 📁 Monitored Log Files

By default, the monitor watches these files (if they exist):

| Log File | Description |
|----------|-------------|
| `/var/log/syslog` | General system messages |
| `/var/log/auth.log` | Authentication/authorization |
| `/var/log/apache2/error.log` | Apache web server errors |
| `/var/log/nginx/error.log` | Nginx web server errors |

### Switch Between Logs

Press `n` to cycle through available log files.

## 🎯 Use Cases

### 1. Security Monitoring
```bash
# Monitor authentication attempts
# Press 'a' and add: "Failed password"
# Watch for brute-force attacks in real-time
```

### 2. Web Server Debugging
```bash
# Switch to apache2/error.log (press 'n')
# Filter for specific error codes
# Press 'f' and enter: "500" or "404"
```

### 3. System Troubleshooting
```bash
# Monitor syslog for system errors
# Add alert for: "error|critical|fatal"
# Pause when you see relevant entries
```

### 4. Live Log Analysis
```bash
# Use split view to watch syslog and auth.log
# Press 's' for split view
# Monitor system and security simultaneously
```

## 🔒 Permissions

Most log files require root access to read.

```bash
# Run with sudo
sudo python3 realtime_log_monitor.py

# Or add user to appropriate groups
sudo usermod -aG adm username
sudo usermod -aG syslog username

# Then logout and login for changes to take effect
```

## ⚙️ Configuration

### Customize Monitored Logs

Edit the script to add/remove log files:

```python
self.default_logs = [
    '/var/log/syslog',
    '/var/log/auth.log',
    '/var/log/your-custom-app.log',  # Add your logs here
]
```

### Adjust Buffer Size

Change how many lines are kept in memory:

```python
self.max_lines = 1000  # Default: 1000 lines per log
```

## 📊 Example Workflows

### Monitor Failed SSH Logins
1. Start monitor: `sudo python3 realtime_log_monitor.py`
2. Press `n` until you see "auth.log"
3. Press `a` and add alert: `Failed password`
4. Watch for authentication failures in magenta

### Debug Apache Errors
1. Start monitor
2. Press `n` to switch to apache2/error.log
3. Press `f` and filter: `PHP`
4. See only PHP-related errors

### System Health Check
1. Start monitor on syslog
2. Press `a` and add: `error|warning|critical`
3. Watch for any system issues
4. Press `p` to pause when investigating

## 🐛 Troubleshooting

### "Permission Denied" Errors

```bash
# Solution 1: Use sudo
sudo python3 realtime_log_monitor.py

# Solution 2: Add to groups
sudo usermod -aG adm $USER
# Logout and login again
```

### "No log files available"

```bash
# Check if log files exist
ls -la /var/log/syslog
ls -la /var/log/auth.log

# Different distributions use different paths:
# RHEL/CentOS: /var/log/secure (instead of auth.log)
# Check your system's log locations
```

### Terminal Display Issues

```bash
# Ensure terminal supports colors
echo $TERM  # Should show xterm-256color or similar

# Resize terminal if layout looks wrong
# Minimum recommended: 80x24 characters
```

### Script Crashes

```bash
# Check Python version (needs 3.6+)
python3 --version

# Verify curses module
python3 -c "import curses"

# Run with error output
python3 realtime_log_monitor.py 2> errors.log
```

## 💡 Tips & Tricks

### Tip 1: Multiple Patterns
Use regex for complex filters:
```
Press 'f': error|warning|critical
```

### Tip 2: IP Tracking
Filter by specific IP address:
```
Press 'f': 192.168.1.100
```

### Tip 3: Service Monitoring
Watch specific service:
```
Press 'f': sshd|ssh
```

### Tip 4: Time-based Filtering
While the tool shows timestamps, you can filter by time:
```
Press 'f': 10:3[0-9]  # Shows entries from 10:30-10:39
```

### Tip 5: Case-Insensitive Search
All filters are case-insensitive by default.

## 🔄 Alternative Log Locations

Different Linux distributions use different log paths:

| Distribution | Auth Logs | System Logs |
|--------------|-----------|-------------|
| **Debian/Ubuntu** | `/var/log/auth.log` | `/var/log/syslog` |
| **RHEL/CentOS** | `/var/log/secure` | `/var/log/messages` |
| **Arch Linux** | `/var/log/auth.log` | `/var/log/syslog` |

Update the script's `default_logs` for your system.

## 🚀 Advanced Usage

### Custom Log Integration

Add your application logs:

```python
self.default_logs = [
    '/var/log/syslog',
    '/var/log/auth.log',
    '/var/log/myapp/application.log',
    '/var/log/myapp/access.log'
]
```

### Automation with Screen/Tmux

Run in background session:

```bash
# Using screen
screen -S logmonitor
sudo python3 realtime_log_monitor.py
# Detach: Ctrl+A, D
# Reattach: screen -r logmonitor

# Using tmux
tmux new -s logmonitor
sudo python3 realtime_log_monitor.py
# Detach: Ctrl+B, D
# Reattach: tmux attach -t logmonitor
```

## 📝 Keyboard Shortcuts Summary

```
┌─────────────────────────────────────┐
│     Quick Reference Card            │
├─────────────────────────────────────┤
│ q          Quit application         │
│ p          Pause/Resume monitoring  │
│ f          Set filter pattern       │
│ n          Next log file            │
│ a          Add alert pattern        │
│ c          Clear current view       │
│ s          Toggle split view        │
│ h          Show help screen         │
└─────────────────────────────────────┘
```

