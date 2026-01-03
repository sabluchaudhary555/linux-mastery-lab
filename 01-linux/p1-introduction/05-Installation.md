# 💿 Linux Installation Guide

## Table of Contents
- [Introduction](#introduction)
- [Installation Methods Overview](#installation-methods-overview)
- [Method 1: Virtual Machine (VM)](#method-1-virtual-machine-vm)
- [Method 2: Dual Boot](#method-2-dual-boot)
- [Method 3: WSL (Windows Subsystem for Linux)](#method-3-wsl-windows-subsystem-for-linux)
- [Method 4: Live USB](#method-4-live-usb)
- [Post-Installation Setup](#post-installation-setup)
- [Troubleshooting](#troubleshooting)

---

## Introduction

There are multiple ways to install and run Linux. Each method has its own advantages and use cases. This guide covers the **three most popular methods** plus a bonus method.

### Which Method Should You Choose?

```
┌─────────────────────────────────────────────┐
│    Are you a complete beginner?             │
│         Yes → Start with VM                 │
│         No  → Continue                      │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│    Do you want full Linux experience?       │
│         Yes → Dual Boot or Dedicated        │
│         No  → VM or WSL                     │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│    Need Windows + Linux simultaneously?     │
│         Yes → VM or WSL                     │
│         No  → Dual Boot                     │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│    Need GUI applications?                   │
│         Yes → VM or Dual Boot               │
│         No  → WSL is sufficient             │
└─────────────────────────────────────────────┘
```

---

## Installation Methods Overview

| Method | Best For | Pros | Cons |
|--------|----------|------|------|
| **Virtual Machine** | Beginners, Testing | Safe, Easy, Multiple OSes | Slower, Resource-heavy |
| **Dual Boot** | Full experience | Native speed, Full access | Reboot needed, Risk to data |
| **WSL** | Developers on Windows | Convenient, Fast, Windows integration | Limited GUI, Not full Linux |
| **Live USB** | Trying Linux | No installation, Portable | Temporary, Slow from USB |

---

## Method 1: Virtual Machine (VM)

### 📌 What is a Virtual Machine?

A VM runs an entire operating system **inside** your current OS as an application. Think of it as a "computer within a computer."

### ✅ Advantages

- ✔️ **Safe**: No risk to your main system
- ✔️ **Easy**: Simple to set up and remove
- ✔️ **Flexible**: Run multiple OSes simultaneously
- ✔️ **Snapshots**: Save and restore system states
- ✔️ **Perfect for learning**: Make mistakes without consequences

### ❌ Disadvantages

- ✖️ **Performance**: Slower than native (10-30% overhead)
- ✖️ **Resources**: Requires RAM and CPU from host
- ✖️ **Hardware**: Limited direct hardware access
- ✖️ **Graphics**: Not ideal for gaming or heavy graphics

---

## VM Installation: VirtualBox

### Step 1: Download and Install VirtualBox

**VirtualBox** is free, open-source, and cross-platform.

```bash
# Download from: https://www.virtualbox.org/

# Linux installation (Ubuntu/Debian)
sudo apt update
sudo apt install virtualbox

# For Extension Pack (USB 3.0, etc.)
# Download from VirtualBox website and install via:
# File → Preferences → Extensions → Add
```

### Step 2: Download Linux ISO

Choose a distribution (Ubuntu recommended for beginners):

- **Ubuntu**: https://ubuntu.com/download/desktop
- **Linux Mint**: https://linuxmint.com/download.php
- **Fedora**: https://getfedora.org/

**File size**: Usually 2-4 GB

### Step 3: Create Virtual Machine

#### 3.1 Create New VM

1. Open VirtualBox
2. Click **"New"**
3. Enter details:
   - **Name**: Ubuntu (or your distro name)
   - **Type**: Linux
   - **Version**: Ubuntu (64-bit) or appropriate
   - Click **Next**

#### 3.2 Allocate Memory (RAM)

```
Recommended RAM allocation:
┌────────────────────────────────────┐
│ Host RAM  │ Allocate to VM         │
├────────────────────────────────────┤
│ 4 GB      │ 1-2 GB                 │
│ 8 GB      │ 2-4 GB                 │
│ 16 GB     │ 4-8 GB                 │
│ 32 GB     │ 8-16 GB                │
└────────────────────────────────────┘

Rule: Leave at least 4 GB for host OS
```

- Select memory (e.g., 4096 MB = 4 GB)
- Click **Next**

#### 3.3 Create Virtual Hard Disk

1. Select **"Create a virtual hard disk now"**
2. Click **Create**
3. Choose **VDI (VirtualBox Disk Image)**
4. Click **Next**
5. Choose **Dynamically allocated** (saves space)
6. Set disk size:
   - **Minimum**: 25 GB
   - **Recommended**: 50 GB
7. Click **Create**

### Step 4: Configure VM Settings

Right-click on VM → **Settings**:

#### 4.1 System Settings

**Processor Tab:**
- CPUs: 2-4 cores (50% of your total cores)
- Enable PAE/NX

**Acceleration Tab:**
- Enable VT-x/AMD-V (if available)
- Enable Nested Paging

#### 4.2 Display Settings

- Video Memory: 128 MB (maximum)
- Graphics Controller: VMSVGA or VBoxVGA
- Enable 3D Acceleration (optional)

#### 4.3 Storage Settings

1. Click on **"Empty"** under Controller: IDE
2. Click disk icon → **Choose a disk file**
3. Select your downloaded Ubuntu ISO
4. Click **OK**

#### 4.4 Network Settings

- Attached to: **NAT** (default - internet access)
- Or **Bridged Adapter** (acts like separate computer on network)

### Step 5: Install Linux

1. **Start the VM** (click "Start")
2. VM boots from ISO
3. Select **"Try Ubuntu"** or **"Install Ubuntu"**
4. Choose language
5. Select keyboard layout
6. **Updates and Software**:
   - ☑ Download updates while installing
   - ☑ Install third-party software
7. **Installation Type**: 
   - Select **"Erase disk and install Ubuntu"**
   - (Don't worry - this only affects the virtual disk!)
8. Select timezone
9. Create user:
   - Your name
   - Computer name
   - Username
   - Password
10. Click **Install Now**
11. Wait 10-20 minutes
12. Click **Restart Now**

### Step 6: Post-Installation

#### Install Guest Additions (Important!)

Guest Additions provide:
- Better graphics performance
- Shared folders
- Clipboard sharing
- Auto-resize display

**Installation:**

1. In VM menu: **Devices → Insert Guest Additions CD image**
2. In Ubuntu terminal:

```bash
# Navigate to CD
cd /media/$USER/VBox_GAs*

# Install
sudo ./VBoxLinuxAdditions.run

# Reboot
sudo reboot
```

#### Enable Shared Folders

1. VM → **Settings → Shared Folders**
2. Click **+** icon
3. Select folder on host
4. Check **Auto-mount** and **Make Permanent**
5. In Linux:

```bash
# Add user to vboxsf group
sudo usermod -aG vboxsf $USER

# Logout and login

# Access at:
cd /media/sf_FolderName
```

#### Enable Clipboard Sharing

VM → **Devices → Shared Clipboard → Bidirectional**

---

## Method 2: Dual Boot

### 📌 What is Dual Boot?

Dual booting means installing Linux **alongside** Windows on the same computer. At startup, you choose which OS to boot.

### ✅ Advantages

- ✔️ **Full performance**: Native speed
- ✔️ **Full hardware access**: Use all devices
- ✔️ **Best experience**: Complete Linux environment
- ✔️ **No resource sharing**: Each OS gets full resources

### ❌ Disadvantages

- ✖️ **Risk**: Can affect Windows boot if done incorrectly
- ✖️ **Complexity**: More complex than VM
- ✖️ **Reboot required**: Can't use both OSes simultaneously
- ✖️ **Disk space**: Needs dedicated partition

---

## Dual Boot Installation: Windows + Ubuntu

### ⚠️ Before You Start

**CRITICAL STEPS - DO NOT SKIP:**

1. **Backup all important data** to external drive
2. **Create Windows Recovery Drive**:
   - Search "Recovery Drive" in Windows
   - Follow wizard
3. **Disable Fast Startup** (Windows):
   - Control Panel → Power Options → Choose what power buttons do
   - Uncheck "Turn on fast startup"
4. **Disable Secure Boot** (optional, if issues):
   - Enter BIOS/UEFI
   - Disable Secure Boot
5. **Have Windows installation media** ready (just in case)

### Step 1: Create Free Space

#### Method 1: Windows Disk Management (Recommended)

1. Press `Win + X` → **Disk Management**
2. Right-click on C: drive (or largest partition)
3. Select **"Shrink Volume"**
4. Enter shrink amount:
   - **Minimum**: 25,000 MB (25 GB)
   - **Recommended**: 50,000 MB (50 GB) or more
5. Click **Shrink**
6. You'll see "Unallocated Space" - leave it as is

#### Method 2: During Ubuntu Installation

Ubuntu installer can resize partitions (but method 1 is safer)

### Step 2: Create Bootable USB

#### Using Rufus (Windows)

1. Download Rufus: https://rufus.ie/
2. Insert USB drive (8 GB minimum)
3. **⚠️ WARNING: USB will be erased!**
4. Open Rufus
5. Settings:
   - Device: Your USB
   - Boot selection: Ubuntu ISO
   - Partition scheme: GPT (for UEFI) or MBR (for BIOS)
   - File system: FAT32
6. Click **START**
7. Wait 5-10 minutes

#### Using Etcher (Cross-platform)

1. Download Etcher: https://www.balena.io/etcher/
2. Insert USB drive
3. Select ISO
4. Select USB drive
5. Click **Flash**

### Step 3: Boot from USB

1. **Restart computer**
2. Enter **Boot Menu** (press during startup):
   - Dell: F12
   - HP: F9 or ESC
   - Lenovo: F12
   - ASUS: ESC or F8
   - Acer: F12
   - Common: F12, F2, ESC, DEL
3. Select USB drive from boot menu
4. If Boot Menu doesn't work:
   - Enter **BIOS/UEFI Setup** (F2, DEL, F10)
   - Change boot order: USB first
   - Save and exit

### Step 4: Install Ubuntu (Dual Boot)

1. Boot from USB
2. Select **"Try Ubuntu"** (test first, optional)
3. Click **"Install Ubuntu"**
4. Choose language
5. Keyboard layout
6. **Updates and Software**:
   - ☑ Download updates
   - ☑ Install third-party software (for WiFi, graphics)
7. **Installation Type** - ⚠️ IMPORTANT:
   
   **Option 1: Automatic (Easier)**
   - Select **"Install Ubuntu alongside Windows"**
   - Ubuntu automatically handles partitioning
   - Drag slider to choose space for each OS
   
   **Option 2: Manual (Advanced)**
   - Select **"Something else"**
   - Create partitions manually:

```
Partition Scheme:
┌────────────────────────────────────────┐
│ Partition  │ Size     │ Type  │ Mount  │
├────────────────────────────────────────┤
│ EFI        │ 512 MB   │ FAT32 │ /boot/ │
│            │          │       │ efi    │
├────────────────────────────────────────┤
│ Root       │ 30+ GB   │ ext4  │ /      │
├────────────────────────────────────────┤
│ Swap       │ = RAM    │ swap  │ -      │
│            │ (or 2GB) │       │        │
├────────────────────────────────────────┤
│ Home       │ Rest     │ ext4  │ /home  │
└────────────────────────────────────────┘

Simple Scheme (Easier):
┌────────────────────────────────────────┐
│ Root       │ All      │ ext4  │ /      │
│            │ space    │       │        │
└────────────────────────────────────────┘
```

8. **Bootloader**: Install GRUB on same disk as Ubuntu
9. Choose timezone
10. Create user account
11. Click **Install Now**
12. Confirm partition changes
13. Wait 15-30 minutes
14. Click **Restart Now**
15. Remove USB when prompted

### Step 5: First Boot

1. Computer restarts
2. **GRUB Bootloader** appears (menu)
3. Select:
   - **Ubuntu** (default)
   - **Windows Boot Manager** (for Windows)
   - Use arrow keys, press Enter
4. Default: Ubuntu boots in 10 seconds
5. Login to Ubuntu

### Step 6: Configure GRUB (Optional)

Change default OS or timeout:

```bash
# Edit GRUB configuration
sudo nano /etc/default/grub

# Change these values:
GRUB_DEFAULT=0              # 0=Ubuntu, 2=Windows (usually)
GRUB_TIMEOUT=10             # Seconds to wait

# To set Windows as default:
GRUB_DEFAULT=saved
# Then run: sudo grub-set-default 2

# Save and exit (Ctrl+X, Y, Enter)

# Update GRUB
sudo update-grub

# Reboot
sudo reboot
```

---

## Method 3: WSL (Windows Subsystem for Linux)

### 📌 What is WSL?

WSL lets you run **Linux inside Windows** without VM or dual boot. It's integrated into Windows 10/11.

### ✅ Advantages

- ✔️ **Convenient**: No reboot needed
- ✔️ **Fast**: Near-native performance
- ✔️ **Integration**: Access Windows files from Linux
- ✔️ **Easy**: One command installation
- ✔️ **Multiple distros**: Run several at once

### ❌ Disadvantages

- ✖️ **Limited GUI**: Primarily command-line (WSL2 has GUI support)
- ✖️ **Not full Linux**: Some features missing
- ✖️ **Windows-dependent**: Requires Windows 10/11
- ✖️ **Performance**: Some operations slower than native

---

## WSL Installation

### Prerequisites

- Windows 10 version 2004+ (Build 19041+) or Windows 11
- Administrator access

### Method 1: Automatic Installation (Easiest)

#### Step 1: Open PowerShell as Administrator

1. Press `Win + X`
2. Select **"Windows PowerShell (Admin)"** or **"Terminal (Admin)"**

#### Step 2: Install WSL

```powershell
# Install WSL with default Ubuntu
wsl --install

# This command:
# - Enables WSL feature
# - Installs WSL 2
# - Downloads Ubuntu
# - Sets up everything
```

#### Step 3: Restart Computer

Restart is required to complete installation.

#### Step 4: First Launch

1. Search "Ubuntu" in Start Menu
2. Open Ubuntu
3. Wait for installation to complete (first time only)
4. Create Linux username (can be different from Windows)
5. Create Linux password
6. Done! You're in Linux terminal

### Method 2: Manual Installation

If automatic method doesn't work:

#### Step 1: Enable WSL Feature

```powershell
# Enable WSL
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

# Enable Virtual Machine Platform
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Restart computer
```

#### Step 2: Set WSL 2 as Default

Download and install WSL2 Linux kernel update:
https://aka.ms/wsl2kernel

```powershell
# Set WSL 2 as default
wsl --set-default-version 2
```

#### Step 3: Install Linux Distribution

```powershell
# List available distributions
wsl --list --online

# Output example:
# NAME            FRIENDLY NAME
# Ubuntu          Ubuntu
# Debian          Debian GNU/Linux
# kali-linux      Kali Linux Rolling
# openSUSE-42     openSUSE Leap 42
# SLES-12         SUSE Linux Enterprise Server v12
# Ubuntu-18.04    Ubuntu 18.04 LTS
# Ubuntu-20.04    Ubuntu 20.04 LTS

# Install a distribution
wsl --install -d Ubuntu

# Or install from Microsoft Store:
# Open Microsoft Store → Search "Ubuntu" → Install
```

### WSL Commands

```powershell
# List installed distributions
wsl --list --verbose
# or
wsl -l -v

# Set default distribution
wsl --set-default Ubuntu

# Run specific distribution
wsl -d Ubuntu

# Run as specific user
wsl -u root

# Shutdown WSL
wsl --shutdown

# Terminate specific distro
wsl --terminate Ubuntu

# Unregister (delete) distribution
wsl --unregister Ubuntu

# Export distribution (backup)
wsl --export Ubuntu C:\backup\ubuntu.tar

# Import distribution (restore)
wsl --import Ubuntu C:\Ubuntu C:\backup\ubuntu.tar

# Update WSL
wsl --update
```

### Accessing Files

#### From Linux to Windows:

```bash
# Windows drives mounted at /mnt/
cd /mnt/c/Users/YourName/Documents

# List Windows C: drive
ls /mnt/c/
```

#### From Windows to Linux:

```
# In File Explorer address bar:
\\wsl$\Ubuntu\home\username

# Or browse:
\\wsl$\
```

### WSL Configuration

Create/edit `~/.wslconfig` (Windows user directory):

```ini
[wsl2]
memory=4GB              # Limit RAM
processors=2            # Limit CPU cores
swap=8GB               # Swap file size
localhostForwarding=true
```

### Installing GUI Applications (WSL2)

WSL2 supports GUI applications (WSLg):

```bash
# Update packages
sudo apt update && sudo apt upgrade

# Install GUI apps
sudo apt install gedit    # Text editor
sudo apt install firefox  # Browser
sudo apt install gimp     # Image editor

# Run GUI app
gedit &
```

### Using Windows Terminal (Recommended)

**Windows Terminal** provides better WSL experience:

1. Install from Microsoft Store: "Windows Terminal"
2. Features:
   - Multiple tabs
   - Split panes
   - Custom themes
   - Better fonts

---

## Method 4: Live USB (Bonus)

### 📌 What is Live USB?

Run Linux directly from USB without installing. Great for:
- Testing Linux before installing
- Portable Linux system
- System rescue/recovery
- Privacy (no trace on computer)

### Creating Live USB

1. Download Linux ISO
2. Use Rufus/Etcher to create bootable USB
3. Boot from USB
4. Select **"Try Ubuntu without installing"**
5. Use Linux normally (slower than installed)
6. Changes lost after restart (unless using persistence)

### Live USB with Persistence

Persistence saves your changes:

**Using Rufus:**
1. Create bootable USB
2. Enable "Persistent partition" (if available)
3. Allocate space for persistence
4. Your changes will be saved

**Manual Method (Linux):**

```bash
# Create persistence partition
# Advanced - requires manual partitioning
```

---

## Post-Installation Setup

### Essential First Steps

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install essential tools
sudo apt install build-essential curl wget git vim

# 3. Install restricted extras (codecs, fonts)
sudo apt install ubuntu-restricted-extras

# 4. Enable firewall
sudo ufw enable

# 5. Install graphics drivers (if needed)
ubuntu-drivers devices
sudo ubuntu-drivers autoinstall

# 6. Install favorite applications
sudo apt install vlc gimp firefox

# 7. Set up GNOME Tweaks (for customization)
sudo apt install gnome-tweaks

# 8. Install synaptic (graphical package manager)
sudo apt install synaptic
```

### Recommended Software

```bash
# Development
sudo apt install code            # VS Code
sudo apt install git
sudo apt install docker.io

# Internet
sudo apt install firefox
sudo apt install thunderbird     # Email

# Multimedia
sudo apt install vlc
sudo apt install audacity
sudo apt install gimp

# Office
sudo apt install libreoffice

# Utilities
sudo apt install htop           # System monitor
sudo apt install neofetch       # System info
sudo apt install timeshift      # Backup tool
```

---

## Troubleshooting

### Common Issues

#### 1. "No Bootable Device" After Dual Boot

**Cause**: GRUB not installed or BIOS boot order wrong

**Solution:**
```bash
# Boot from Ubuntu USB
# Open terminal

# Reinstall GRUB
sudo mount /dev/sdXY /mnt  # Replace X with drive, Y with partition
sudo grub-install --root-directory=/mnt /dev/sdX
sudo update-grub
```

#### 2. Windows Not Showing in GRUB

**Solution:**
```bash
sudo update-grub
# or
sudo grub-mkconfig -o /boot/grub/grub.cfg
```

#### 3. WiFi Not Working

**Solution:**
```bash
# Install additional drivers
sudo ubuntu-drivers autoinstall
# Reboot
```

#### 4. Screen Resolution Issues (VM)

**Solution:**
- Install Guest Additions (VirtualBox)
- Install VMware Tools (VMware)
- Update graphics drivers

#### 5. Slow Performance (VM)

**Solutions:**
- Allocate more RAM
- Enable 3D acceleration
- Use SSD instead of HDD
- Close unnecessary host applications

#### 6. WSL Can't Access Network

**Solution:**
```powershell
# Reset WSL network
wsl --shutdown
# Restart WSL
```

#### 7. Dual Boot Time Wrong

Windows and Linux handle time differently.

**Solution (Make Linux use Local Time):**
```bash
timedatectl set-local-rtc 1 --adjust-system-clock
```

---

## Comparison Summary

| Feature | VM | Dual Boot | WSL |
|---------|-----|-----------|-----|
| **Ease of Setup** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Performance** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Safety** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **GUI Support** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Hardware Access** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Convenience** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## Final Recommendations

### For Beginners:
🥇 **Start with VM** (VirtualBox) - safest way to learn

### For Developers:
🥇 **Use WSL** - convenient for development work

### For Full Linux Experience:
🥇 **Dual Boot** - best performance and complete access

### For Testing Multiple Distros:
🥇 **VM or Live USB** - easy to switch

---

## Resources

### Official Documentation
- [Ubuntu Installation Guide](https://ubuntu.com/tutorials/install-ubuntu-desktop)
- [VirtualBox Manual](https://www.virtualbox.org/manual/)
- [WSL Documentation](https://docs.microsoft.com/en-us/windows/wsl/)

### Video Tutorials
- Search YouTube: "How to install Ubuntu"
- Linux installation walkthroughs
- Dual boot tutorials

### Communities
- r/linux4noobs
- r/linuxquestions
- Ubuntu Forums
- Ask Ubuntu (StackExchange)

---

**Remember**: You can always try VM first, then move to dual boot later!

<br>



**Happy Learning! 🚀**

*Contributions and suggestions are welcome!*

---

**Maintained by: [Sablu Chaudhary](https://github.com/sabluchaudhary555)** 🔗 **Connect with me:** [LinkedIn](https://www.linkedin.com/in/sablu-chaudhary555/) | [GitHub](https://github.com/sabluchaudhary555)

---
**Made with ❤️ for the Open Source Community**