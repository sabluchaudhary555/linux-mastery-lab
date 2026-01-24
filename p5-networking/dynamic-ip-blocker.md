# Dynamic IP Blocker (Fail2Ban Alternative)

A lightweight Python-based intrusion prevention system that automatically blocks malicious IPs based on failed login attempts. Monitor SSH, HTTP, FTP, and other services with configurable thresholds and automatic unblocking.

## 🚀 Features

- 🔍 **Real-time Log Monitoring** - Continuously watch log files for suspicious activity
- 🚫 **Automatic IP Blocking** - Add iptables DROP rules for offending IPs
- ⏰ **Auto-Unblock** - Automatically remove blocks after timeout
- ✅ **IP Whitelist** - Protect trusted IPs from being blocked
- 🎯 **Multi-Service Support** - Monitor SSH, HTTP, FTP simultaneously
- ⚙️ **Configurable Thresholds** - Customize attempts/time window per service
- 📊 **Statistics & Reports** - Track blocked IPs and service status
- 🔄 **Persistent Storage** - Banned IPs survive reboots

## 📋 Requirements

- Python 3.6+
- Linux system with iptables
- Root/sudo access (for iptables management)
- Read access to log files

```bash
# Verify iptables is installed
which iptables

# Verify log files exist
ls -la /var/log/auth.log     # SSH logs (Debian/Ubuntu)
ls -la /var/log/secure       # SSH logs (RHEL/CentOS)
```

## 🔧 Installation

```bash
# Download the script
wget https://raw.githubusercontent.com/yourusername/dynamic-ip-blocker/main/dynamic_ip_blocker.py
chmod +x dynamic_ip_blocker.py

# Create required directories
sudo mkdir -p /var/log
sudo touch /var/log/ip_blocker.log

# Optional: Install as systemd service (see below)
```

## 📖 Usage

### Start Monitoring (Daemon Mode)

```bash
# Start the blocker (runs continuously)
sudo python3 dynamic_ip_blocker.py start

# Output:
# [2024-01-24 10:30:00] 📊 Monitoring ssh log: /var/log/auth.log
# [2024-01-24 10:30:00] 🔄 Auto-unblock daemon started
# [2024-01-24 10:30:00] 🚀 Dynamic IP Blocker started
```

### Manual IP Management

```bash
# Block an IP manually for 1 hour (3600 seconds)
sudo python3 dynamic_ip_blocker.py block 192.168.1.100 3600

# Block an IP for 2 hours
sudo python3 dynamic_ip_blocker.py block 203.0.113.50 7200

# Unblock an IP
sudo python3 dynamic_ip_blocker.py unblock 192.168.1.100
```

### Whitelist Management

```bash
# Add IP to whitelist (never gets blocked)
sudo python3 dynamic_ip_blocker.py whitelist-add 10.0.0.5

# Remove from whitelist
sudo python3 dynamic_ip_blocker.py whitelist-remove 10.0.0.5

# Show all whitelisted IPs
python3 dynamic_ip_blocker.py whitelist-show
```

### Monitoring & Statistics

```bash
# List all currently blocked IPs
python3 dynamic_ip_blocker.py list

# Show statistics and service status
python3 dynamic_ip_blocker.py stats
```

## 📊 Example Output

### Blocking in Action
```
[2024-01-24 10:35:22] ⚠️  Failed ssh attempt from 203.0.113.50
[2024-01-24 10:35:45] ⚠️  Failed ssh attempt from 203.0.113.50
[2024-01-24 10:36:12] ⚠️  Failed ssh attempt from 203.0.113.50
[2024-01-24 10:36:30] ⚠️  Failed ssh attempt from 203.0.113.50
[2024-01-24 10:36:55] ⚠️  Failed ssh attempt from 203.0.113.50
[2024-01-24 10:36:55] 🚫 BLOCKED: 203.0.113.50 (ssh) - Duration: 3600s
```

### List Blocked IPs
```
================================================================================
BLOCKED IP ADDRESSES
================================================================================

IP Address           Service    Banned At            Unblock At          
--------------------------------------------------------------------------------
203.0.113.50         ssh        2024-01-24 10:36:55  2024-01-24 11:36:55
198.51.100.25        http       2024-01-24 09:15:30  2024-01-24 09:45:30
```

### Statistics
```
============================================================
DYNAMIC IP BLOCKER STATISTICS
============================================================

Currently Blocked IPs: 3
Whitelisted IPs: 2

Service Status:
  SSH: ✓ Enabled
  HTTP: ✗ Disabled
  FTP: ✗ Disabled

Auto-unblock: ✓ Enabled
```

## ⚙️ Configuration

Configuration is stored in `~/.ip_blocker_config.json`. Default settings:

```json
{
  "ssh": {
    "enabled": true,
    "log_file": "/var/log/auth.log",
    "max_attempts": 5,
    "time_window": 600,
    "ban_duration": 3600,
    "regex": "Failed password for .* from (\\d+\\.\\d+\\.\\d+\\.\\d+)"
  },
  "http": {
    "enabled": false,
    "log_file": "/var/log/apache2/error.log",
    "max_attempts": 10,
    "time_window": 300,
    "ban_duration": 1800
  },
  "ftp": {
    "enabled": false,
    "log_file": "/var/log/vsftpd.log",
    "max_attempts": 5,
    "time_window": 600,
    "ban_duration": 3600
  },
  "whitelist": ["127.0.0.1", "::1"],
  "auto_unblock": true
}
```

### Configuration Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `enabled` | Enable monitoring for this service | `true` (SSH) |
| `log_file` | Path to service log file | `/var/log/auth.log` |
| `max_attempts` | Failed attempts before blocking | `5` |
| `time_window` | Time window in seconds | `600` (10 min) |
| `ban_duration` | Block duration in seconds | `3600` (1 hour) |
| `regex` | Regex pattern to extract IP | Service-specific |
| `whitelist` | IPs that never get blocked | `["127.0.0.1"]` |
| `auto_unblock` | Automatically unblock after timeout | `true` |

### Enable Additional Services

Edit `~/.ip_blocker_config.json`:

```json
{
  "http": {
    "enabled": true,
    "log_file": "/var/log/nginx/error.log",
    "max_attempts": 10,
    "time_window": 300,
    "ban_duration": 1800,
    "regex": "client (\\d+\\.\\d+\\.\\d+\\.\\d+)"
  }
}
```

## 🔧 Systemd Service Setup

Create `/etc/systemd/system/ip-blocker.service`:

```ini
[Unit]
Description=Dynamic IP Blocker Service
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/bin/python3 /opt/ip-blocker/dynamic_ip_blocker.py start
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable ip-blocker
sudo systemctl start ip-blocker

# Check status
sudo systemctl status ip-blocker

# View logs
sudo journalctl -u ip-blocker -f
```

## 📁 File Locations

- **Configuration**: `~/.ip_blocker_config.json`
- **Banned IPs**: `~/.ip_blocker_banned.json`
- **Log File**: `/var/log/ip_blocker.log`

## 🎯 Use Cases

1. **SSH Brute-Force Protection** - Block IPs attempting password guessing
2. **Web Server Protection** - Prevent HTTP-based attacks
3. **FTP Security** - Stop unauthorized FTP access attempts
4. **Multi-Service Defense** - Protect all services simultaneously
5. **Compliance** - Meet security audit requirements
6. **Automated Response** - No manual intervention needed

## 🔍 How It Works

1. **Log Monitoring**: Continuously reads log files in real-time
2. **Pattern Matching**: Uses regex to extract IPs from failed attempts
3. **Threshold Checking**: Counts attempts within time window
4. **Automatic Blocking**: Adds iptables DROP rule when threshold exceeded
5. **Scheduled Unblocking**: Removes rules after configured duration

### Flow Diagram
```
Failed Login → Log Entry → Pattern Match → IP Extracted
                                              ↓
                                        Count Attempts
                                              ↓
                                   Threshold Exceeded?
                                              ↓
                                        Add iptables Rule
                                              ↓
                                        Schedule Unblock
                                              ↓
                                    Auto-Remove After Timeout
```

## 🔒 Security Features

- ✅ **Whitelist Protection** - Trusted IPs never blocked
- ✅ **Persistent Bans** - Survive script restarts
- ✅ **Configurable Thresholds** - Adjust sensitivity per service
- ✅ **Automatic Recovery** - Auto-unblock prevents permanent locks
- ✅ **Audit Logging** - Complete activity logs
- ✅ **Manual Override** - Admin can block/unblock anytime

## 🐛 Troubleshooting

### IPs Not Being Blocked

```bash
# Check if script is running
ps aux | grep dynamic_ip_blocker

# Verify log file path is correct
tail -f /var/log/auth.log

# Check regex pattern is matching
# Test manually with sample log line

# Ensure sudo/root access
sudo python3 dynamic_ip_blocker.py start
```

### Locked Out of Server

```bash
# Access via console/IPMI
# Add your IP to whitelist FIRST
python3 dynamic_ip_blocker.py whitelist-add YOUR.IP.ADDRESS

# Or manually remove iptables rule
sudo iptables -D INPUT -s YOUR.IP.ADDRESS -j DROP
```

### Service Not Starting

```bash
# Check log file permissions
sudo touch /var/log/ip_blocker.log
sudo chmod 644 /var/log/ip_blocker.log

# Verify iptables is available
which iptables

# Test manually first
sudo python3 dynamic_ip_blocker.py start
```

### Different Log Locations

For **CentOS/RHEL** (SSH logs in `/var/log/secure`):

```json
{
  "ssh": {
    "log_file": "/var/log/secure"
  }
}
```

For **Nginx**:

```json
{
  "http": {
    "log_file": "/var/log/nginx/error.log"
  }
}
```

## 📝 Log File Regex Patterns

### SSH (auth.log)
```regex
Failed password for .* from (\d+\.\d+\.\d+\.\d+)
```

### Apache/Nginx
```regex
client (\d+\.\d+\.\d+\.\d+)
```

### vsftpd
```regex
FAIL LOGIN.*from (\d+\.\d+\.\d+\.\d+)
```

### Custom Pattern
Edit config and use your own regex to extract IP addresses.

## ⚠️ Important Notes

- **Always whitelist your own IP** before enabling
- **Test in non-production** environment first
- **Keep console access** ready (in case of lockout)
- **Monitor logs regularly** for false positives
- **Backup iptables rules** before running
- **Use strong passwords** as primary defense (this is secondary)

## 🆚 Comparison with Fail2Ban

| Feature | Dynamic IP Blocker | Fail2Ban |
|---------|-------------------|----------|
| Language | Python (single file) | Python (complex) |
| Configuration | JSON (simple) | INI files (many) |
| Dependencies | None (stdlib only) | Multiple packages |
| Size | ~300 lines | 10,000+ lines |
| Learning Curve | Easy | Moderate |
| Flexibility | Good | Excellent |
| Community | New | Mature |

## 🔄 Backup & Restore

### Backup Current iptables Rules
```bash
sudo iptables-save > iptables-backup.rules
```

### Restore if Needed
```bash
sudo iptables-restore < iptables-backup.rules
```

