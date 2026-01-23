# Network Health Monitor 🌐

A lightweight Python tool to monitor network connectivity and performance metrics in real-time.

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS-lightgrey.svg)

## 🎯 Features

- ✅ **Real-time Monitoring** - Continuous ping monitoring to multiple hosts
- 📊 **Performance Metrics** - Track latency, packet loss, and jitter
- 🚨 **Smart Alerts** - Automatic alerts on network degradation
- 📈 **Uptime Reports** - Generate detailed uptime statistics
- 💾 **Data Export** - Save logs to JSON and CSV formats
- 🎨 **Clean Output** - Easy-to-read terminal interface

## 🚀 Quick Start

### Prerequisites

- Python 3.6+
- Linux or macOS (uses `ping` command)
- No external packages required (uses only standard library)

### Installation

```bash
# Clone or download the script
wget https://raw.githubusercontent.com/yourusername/network-monitor/main/network_monitor.py

# Make executable
chmod +x network_monitor.py

# Run
python3 network_monitor.py
```

## 📖 Usage

### Interactive Menu

```bash
python3 network_monitor.py
```

**Options:**
1. **Single Check** - Run one-time network check
2. **Continuous Monitoring** - Monitor for 5 minutes
3. **Custom Monitoring** - Set custom interval and duration
4. **Exit**

### Single Network Check

```bash
python3 network_monitor.py
# Select option 1
```

**Output:**
```
======================================================================
Network Health Status - 2025-01-23 14:30:45
======================================================================

✅ Google DNS (8.8.8.8)
   Status: UP
   Latency: 12.5ms (min: 11.2ms, max: 14.8ms)
   Packet Loss: 0.0%
   Jitter: 1.2ms

✅ Cloudflare DNS (1.1.1.1)
   Status: UP
   Latency: 8.3ms (min: 7.5ms, max: 9.1ms)
   Packet Loss: 0.0%
   Jitter: 0.8ms

❌ Local Gateway (192.168.1.1)
   Status: DOWN
```

### Continuous Monitoring

```bash
python3 network_monitor.py
# Select option 2
```

Monitors network every 10 seconds for 5 minutes and generates:
- Real-time status updates
- Alert notifications
- Uptime report
- JSON log file
- CSV log file

### Custom Monitoring

```bash
python3 network_monitor.py
# Select option 3
# Enter check interval: 30
# Enter total duration: 600
```

Monitors every 30 seconds for 10 minutes.

## 📊 Output Files

### JSON Log (`network_log.json`)

```json
[
  {
    "host": "Google DNS",
    "ip": "8.8.8.8",
    "status": "UP",
    "latency_avg": 12.5,
    "latency_min": 11.2,
    "latency_max": 14.8,
    "packet_loss": 0.0,
    "timestamp": "2025-01-23 14:30:45"
  }
]
```

### CSV Log (`network_log.csv`)

```csv
host,ip,status,latency_avg,latency_min,latency_max,packet_loss,timestamp
Google DNS,8.8.8.8,UP,12.5,11.2,14.8,0.0,2025-01-23 14:30:45
Cloudflare DNS,1.1.1.1,UP,8.3,7.5,9.1,0.0,2025-01-23 14:30:45
```

## 🔧 Configuration

Edit the `hosts` dictionary in the script to monitor different hosts:

```python
self.hosts = {
    'Google DNS': '8.8.8.8',
    'Cloudflare DNS': '1.1.1.1',
    'Local Gateway': '192.168.1.1',
    'Custom Server': '192.168.1.100'
}
```

## 📈 Metrics Explained

### Latency
- **Average** - Mean round-trip time
- **Min/Max** - Fastest and slowest response times
- **Measured in:** milliseconds (ms)

### Packet Loss
- Percentage of packets that didn't receive a response
- **0%** = Perfect connection
- **>5%** = Poor connection
- **100%** = Host unreachable

### Jitter
- Variation in latency over time
- Calculated from last 100 measurements
- **Low (<10ms)** = Stable connection
- **High (>30ms)** = Unstable connection

### Uptime
- Percentage of successful checks
- **99%+** = Excellent
- **95-99%** = Good
- **<95%** = Poor reliability

## 🚨 Alert Thresholds

The monitor automatically alerts on:

| Condition | Threshold | Alert |
|-----------|-----------|-------|
| Host Down | Status = DOWN | 🔴 Critical |
| High Packet Loss | >10% | ⚠️ Warning |
| High Latency | >100ms | ⚠️ Warning |

**Example Alerts:**
```
🔴 Local Gateway is DOWN!
⚠️  Google DNS has 15% packet loss
⚠️  Cloudflare DNS has high latency: 150ms
```

## 📋 Sample Uptime Report

```
======================================================================
UPTIME REPORT
======================================================================

Google DNS:
  Total Checks: 30
  Uptime: 100.00% (30/30)
  Average Latency: 12.34ms

Cloudflare DNS:
  Total Checks: 30
  Uptime: 96.67% (29/30)
  Average Latency: 8.52ms

Local Gateway:
  Total Checks: 30
  Uptime: 80.00% (24/30)
  Average Latency: 2.15ms
```

## 🔄 Automation with Cron

### Monitor Every Hour

```bash
# Edit crontab
crontab -e

# Add this line
0 * * * * cd /path/to/script && python3 network_monitor.py --single >> monitor.log 2>&1
```

### Daily Report at 6 AM

```bash
0 6 * * * cd /path/to/script && python3 network_monitor.py --report
```

## 🛠️ Troubleshooting

### Permission Denied

```bash
# Run with sudo if needed
sudo python3 network_monitor.py
```

### Ping Command Not Found

```bash
# Install iputils (Ubuntu/Debian)
sudo apt-get install iputils-ping

# Install iputils (RHEL/CentOS)
sudo yum install iputils
```

### No Response from Host

Check if host is reachable:
```bash
ping -c 3 8.8.8.8
```

### Firewall Blocking ICMP

```bash
# Allow ICMP in firewall
sudo ufw allow proto icmp
```

## 💡 Use Cases

### 1. ISP Monitoring
Monitor your internet connection stability over time.

### 2. Server Health
Track connectivity to critical servers.

### 3. Network Troubleshooting
Identify when and where network issues occur.

### 4. VPN Performance
Monitor VPN connection quality.

### 5. Remote Site Monitoring
Check connectivity to remote office locations.

## 🎯 Best Practices

1. **Don't Over-Monitor** - 10-30 second intervals are sufficient
2. **Monitor Multiple Targets** - Use 3-5 diverse hosts
3. **Check Logs Regularly** - Review JSON/CSV files weekly
4. **Set Up Alerts** - Integrate with email or Slack for critical alerts
5. **Archive Old Logs** - Keep logs organized by date

## 📊 Advanced Usage

### Export to Excel

```python
import pandas as pd

# Read CSV
df = pd.read_csv('network_log.csv')

# Create Excel with charts
with pd.ExcelWriter('network_report.xlsx') as writer:
    df.to_excel(writer, sheet_name='Raw Data', index=False)
```

### Visualize with Matplotlib

```python
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('network_log.csv')
df_google = df[df['host'] == 'Google DNS']

plt.plot(df_google['timestamp'], df_google['latency_avg'])
plt.title('Google DNS Latency Over Time')
plt.xlabel('Time')
plt.ylabel('Latency (ms)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('latency_graph.png')
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

**Happy Learning! 🚀**

*Contributions and suggestions are welcome!*

---

**Maintained by: [Sablu Chaudhary](https://github.com/sabluchaudhary555)** 🔗 **Connect with me:** [LinkedIn](https://www.linkedin.com/in/sablu-chaudhary555/) | [GitHub](https://github.com/sabluchaudhary555)

---
**Made with ❤️ for the Open Source Community**