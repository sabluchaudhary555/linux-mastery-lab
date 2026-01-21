# Linux Boot Process Analyzer

A Python tool that traces and visualizes the Linux boot sequence with detailed performance metrics.

## Overview

This tool analyzes the complete Linux boot process from BIOS/UEFI to the login prompt, providing insights into boot performance, service startup times, and system configuration.

## Features

- **Boot Time Analysis** - Shows total boot time and breakdown by component
- **systemd Performance** - Identifies slowest services and critical startup paths
- **Kernel Messages** - Displays dmesg output with timestamps
- **Boot Stage Visualization** - Visual representation of the 6 boot stages
- **Bootloader Detection** - Identifies GRUB configuration and boot mode (UEFI/BIOS)
- **Critical File Verification** - Checks existence of essential boot files
- **Log Location Guide** - Shows where to find various boot logs

## Installation

1. Save the script as `linux_boot_analyzer.py`
2. Make it executable:
```bash
chmod +x linux_boot_analyzer.py
```

## Usage

### Basic usage (limited information):
```bash
./linux_boot_analyzer.py
```

### Full analysis (recommended):
```bash
sudo ./linux_boot_analyzer.py
```

> **Note:** Root privileges are required for complete dmesg access and full systemd analysis.

## Boot Stages Analyzed

1. **BIOS/UEFI** - Hardware initialization (0-2s)
2. **Bootloader (GRUB)** - Kernel loading (2-4s)
3. **Kernel** - Linux kernel initialization (4-8s)
4. **Init System (systemd)** - PID 1 startup (8-15s)
5. **Services** - System services (15-25s)
6. **Login Ready** - Display manager ready (25-30s)

## Output Information

The tool provides:

- System uptime and last boot time
- Kernel version and parameters
- Bootloader type and configuration location
- Boot mode (UEFI or Legacy BIOS)
- Top 10 slowest services
- Critical boot file status
- Kernel boot messages (first 20 lines)
- Useful commands for further analysis

## Requirements

- **OS:** Linux (any distribution)
- **Python:** 3.6 or higher
- **Dependencies:** Standard library only (no pip packages needed)
- **Tools Used:**
  - `systemd-analyze` (for systemd-based systems)
  - `dmesg` (kernel messages)
  - `uptime` (boot time)

## Useful Commands Reference

The tool provides a list of helpful commands including:

- `systemd-analyze` - Boot time breakdown
- `systemd-analyze blame` - Service startup times
- `journalctl -b` - Current boot logs
- `dmesg -T` - Kernel messages with timestamps

## Troubleshooting

**"systemd-analyze not found"** - Your system may use a different init system (SysVinit, OpenRC)

**"Unable to read dmesg"** - Run with `sudo` for full kernel message access

**Missing boot files** - Check your bootloader configuration

## License

Developed by SSoft.in

---

*For detailed boot analysis, always run with sudo privileges.*