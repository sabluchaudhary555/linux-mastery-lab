# 🏗️ Linux Architecture

## Table of Contents
- [Overview](#overview)
- [Linux Architecture Layers](#linux-architecture-layers)
- [1. Hardware Layer](#1-hardware-layer)
- [2. Kernel Layer](#2-kernel-layer)
- [3. Shell Layer](#3-shell-layer)
- [4. User Space (Application Layer)](#4-user-space-application-layer)
- [How They Work Together](#how-they-work-together)
- [Architecture Diagram](#architecture-diagram)
- [Kernel Space vs User Space](#kernel-space-vs-user-space)
- [Boot Process](#boot-process)
- [Conclusion](#conclusion)

---

## Overview

Linux architecture is built on a **layered approach** where each layer has specific responsibilities and communicates with adjacent layers. This modular design makes Linux stable, secure, and efficient.

The four main layers are:
1. **Hardware Layer** (Bottom)
2. **Kernel Layer**
3. **Shell Layer**
4. **User Space / Application Layer** (Top)

---

## Linux Architecture Layers

```
┌─────────────────────────────────────────────┐
│         USER SPACE (Layer 4)                │
│                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Users   │  │   Apps   │  │   GUI    │   │
│  └──────────┘  └──────────┘  └──────────┘   │
│                                             │
└─────────────────────────────────────────────┘
                     ↕
┌─────────────────────────────────────────────┐
│         SHELL LAYER (Layer 3)               │
│                                             │
│     Bash │ Zsh │ Fish │ Sh │ Csh            │
│                                             │
│  (Command Interpreter & Interface)          │
└─────────────────────────────────────────────┘
                     ↕
┌─────────────────────────────────────────────┐
│         KERNEL LAYER (Layer 2)              │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │      System Call Interface          │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────────┐    │
│  │ PM   │ │ MM   │ │ FS   │ │ Network  │    │
│  │      │ │      │ │      │ │ Stack    │    │
│  └──────┘ └──────┘ └──────┘ └──────────┘    │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │      Device Drivers                 │    │ 
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
                     ↕
┌─────────────────────────────────────────────┐
│        HARDWARE LAYER (Layer 1)             │
│                                             │
│  CPU │ RAM │ HDD/SSD │ Network │ Devices    │
└─────────────────────────────────────────────┘
```

**Legend:**
- PM = Process Management
- MM = Memory Management
- FS = File System

---

## 1. Hardware Layer

### 📌 Description
The **Hardware Layer** is the physical foundation of the system - the actual computer components that Linux runs on.

### 🔧 Components

| Component | Description | Role |
|-----------|-------------|------|
| **CPU** | Central Processing Unit | Executes instructions, performs calculations |
| **RAM** | Random Access Memory | Temporary storage for running processes |
| **Storage** | HDD/SSD/NVMe | Permanent data storage |
| **Network Devices** | NIC, WiFi adapters | Network communication |
| **Input Devices** | Keyboard, Mouse, Touchpad | User input |
| **Output Devices** | Monitor, Printer, Speakers | Display/output information |
| **Peripherals** | USB devices, Graphics cards | Extended functionality |

### ⚡ Key Points

- Linux supports **wide range of hardware** architectures:
  - x86 (32-bit)
  - x86_64 (64-bit)
  - ARM (mobile, embedded)
  - PowerPC
  - RISC-V
  - MIPS
  
- **Hardware abstraction**: Kernel provides uniform interface regardless of hardware
- **Plug and Play**: Automatic device detection and configuration
- **Hot-swapping**: Add/remove devices without reboot (USB, etc.)

### 📝 Example Commands

```bash
# View CPU information
lscpu
cat /proc/cpuinfo

# View memory information
free -h
cat /proc/meminfo

# View hardware information
lshw
lspci          # PCI devices
lsusb          # USB devices
lsblk          # Block devices (disks)

# View system information
uname -a
dmidecode      # DMI/SMBIOS information
```

---

## 2. Kernel Layer

### 📌 Description
The **Kernel** is the **core** of the Linux operating system. It acts as a bridge between hardware and software, managing system resources and providing essential services.

### 🎯 Primary Functions

1. **Process Management**
2. **Memory Management**
3. **File System Management**
4. **Device Management**
5. **Network Management**
6. **Security & Access Control**

---

### 2.1 Process Management

**What it does:**
- Creates, schedules, and terminates processes
- Manages CPU time allocation
- Handles process priorities
- Manages inter-process communication (IPC)

**Key Concepts:**

| Concept | Description |
|---------|-------------|
| **Process** | Running instance of a program |
| **Thread** | Lightweight process, shares memory |
| **Scheduler** | Decides which process runs when |
| **PID** | Process ID (unique identifier) |
| **Context Switching** | Switching CPU between processes |

**Example Commands:**

```bash
# View running processes
ps aux
ps -ef

# Real-time process monitoring
top
htop

# Process tree
pstree

# Kill a process
kill PID
killall process_name

# Process priority
nice -n 10 command      # Start with priority
renice -n 5 -p PID      # Change priority

# Background processes
command &               # Run in background
jobs                    # List background jobs
fg                      # Bring to foreground
bg                      # Resume in background
```

---

### 2.2 Memory Management

**What it does:**
- Allocates and deallocates memory
- Manages virtual memory
- Implements memory protection
- Handles paging and swapping

**Key Concepts:**

| Concept | Description |
|---------|-------------|
| **Virtual Memory** | Abstraction that gives each process its own address space |
| **Physical Memory** | Actual RAM installed in system |
| **Swap Space** | Disk space used when RAM is full |
| **Paging** | Moving data between RAM and disk |
| **Memory Mapping** | Mapping files into memory |

**Memory Layout:**

```
High Address
┌────────────────┐
│  Kernel Space  │  ← Kernel code, data, drivers
├────────────────┤
│  User Stack    │  ← Function calls, local       variables 
│       ↓        │
│                │
│       ↑        │
│   Heap         │  ← Dynamic memory allocation
├────────────────┤
│  BSS Segment   │  ← Uninitialized global variables
├────────────────┤
│  Data Segment  │  ← Initialized global variables
├────────────────┤
│  Text Segment  │  ← Program code (read-only)
└────────────────┘
Low Address
```

**Example Commands:**

```bash
# Memory usage
free -h
cat /proc/meminfo

# Swap information
swapon --show
cat /proc/swaps

# Memory map of a process
pmap PID
cat /proc/PID/maps

# Clear cache (requires root)
sync; echo 3 > /proc/sys/vm/drop_caches

# Out of Memory (OOM) killer info
dmesg | grep -i "out of memory"
```

---

### 2.3 File System Management

**What it does:**
- Manages files and directories
- Handles file operations (create, read, write, delete)
- Maintains file permissions
- Supports multiple file systems

**Supported File Systems:**

| File System | Type | Use Case |
|-------------|------|----------|
| **ext4** | Native | Default for most Linux distros |
| **XFS** | Native | High-performance, large files |
| **Btrfs** | Native | Modern, copy-on-write |
| **FAT32** | Foreign | USB drives, compatibility |
| **NTFS** | Foreign | Windows partitions |
| **NFS** | Network | Network file sharing |
| **tmpfs** | RAM-based | Temporary files in memory |

**Virtual File System (VFS):**

```
┌─────────────────────────────────────┐
│     Applications (User Space)       │
└────────────────┬────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│  Virtual File System (VFS) Layer    │
│  (Unified interface for all FS)     │
└─────┬──────┬──────┬──────┬──────────┘
      ↓      ↓      ↓      ↓
   ┌─────┐ ┌────┐ ┌────┐ ┌────┐
   │ext4 │ │XFS │ │FAT │ │NFS │
   └─────┘ └────┘ └────┘ └────┘
```

**Example Commands:**

```bash
# List file systems
df -h
df -T          # Show file system type

# Mount/Unmount
mount /dev/sda1 /mnt
umount /mnt

# File system check
fsck /dev/sda1

# Create file system
mkfs.ext4 /dev/sda1

# View inode information
ls -i
df -i          # Inode usage

# File system statistics
stat filename
```

---

### 2.4 Device Management

**What it does:**
- Controls hardware devices through device drivers
- Provides uniform interface to devices
- Manages device I/O operations

**Device Types:**

| Type | Description | Examples |
|------|-------------|----------|
| **Character Devices** | Sequential access, byte-by-byte | Keyboard, mouse, serial ports |
| **Block Devices** | Random access, block-by-block | Hard drives, SSDs, USB drives |
| **Network Devices** | Network communication | Ethernet, WiFi adapters |
| **Pseudo Devices** | Virtual devices | /dev/null, /dev/zero, /dev/random |

**Device File Location:**

```bash
/dev/              # Device files directory
├── sda            # First SATA disk
├── sda1           # First partition on sda
├── sdb            # Second SATA disk
├── nvme0n1        # NVMe SSD
├── tty            # Terminal devices
├── null           # Null device (discards data)
├── zero           # Zero device (infinite zeros)
├── random         # Random number generator
└── input/         # Input devices (keyboard, mouse)
```

**Example Commands:**

```bash
# List devices
ls -l /dev/

# Block devices
lsblk
blkid          # Block device attributes

# USB devices
lsusb

# PCI devices
lspci

# Input devices
ls /dev/input/

# Device information
udevadm info --query=all --name=/dev/sda

# Kernel modules (drivers)
lsmod          # List loaded modules
modinfo module_name
modprobe module_name    # Load module
rmmod module_name       # Remove module
```

---

### 2.5 Network Management

**What it does:**
- Manages network connections
- Implements network protocols (TCP/IP)
- Handles routing and packet forwarding
- Manages firewalls and security

**Network Stack:**

```
Application Layer (HTTP, FTP, SSH)
           ↓
Transport Layer (TCP, UDP)
           ↓
Network Layer (IP, ICMP)
           ↓
Data Link Layer (Ethernet, WiFi)
           ↓
Physical Layer (Hardware)
```

**Example Commands:**

```bash
# Network interfaces
ip addr show
ifconfig       # Legacy command

# Network configuration
ip link show
ip route show

# Network statistics
netstat -tuln
ss -tuln       # Modern alternative

# Test connectivity
ping google.com
traceroute google.com

# DNS lookup
nslookup domain.com
dig domain.com

# Network monitoring
tcpdump        # Packet capture
iftop          # Bandwidth monitoring
```

---

### 2.6 System Calls

**System Calls** are the interface between user space and kernel space.

**Common System Calls:**

| Category | System Calls | Purpose |
|----------|-------------|---------|
| **Process** | fork(), exec(), wait(), exit() | Process management |
| **File** | open(), read(), write(), close() | File operations |
| **Memory** | brk(), mmap(), munmap() | Memory allocation |
| **Network** | socket(), bind(), connect(), send() | Network operations |
| **I/O** | ioctl(), select(), poll() | I/O control |

**How System Calls Work:**

```
┌─────────────────────────────────┐
│  Application calls function     │  User Space
│  (e.g., printf(), fopen())      │
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│  Library (glibc) wraps          │
│  system call                    │
└────────────┬────────────────────┘
             ↓
        ════════════ System Call Interface ════════════
             ↓
┌─────────────────────────────────┐
│  Kernel executes system call    │  Kernel Space
│  (e.g., sys_write())            │
└─────────────────────────────────┘
```

**Example: Tracing System Calls**

```bash
# Trace system calls
strace ls
strace -c ls   # Count system calls

# Trace specific system call
strace -e open ls

# Trace running process
strace -p PID
```

---

### 2.7 Kernel Types

**Linux uses a Monolithic Kernel with Modular Design**

| Kernel Type | Description | Pros | Cons |
|-------------|-------------|------|------|
| **Monolithic** | All services in kernel space | Fast, efficient | Large, complex |
| **Microkernel** | Minimal kernel, services in user space | Modular, stable | Slower (context switching) |
| **Hybrid** | Mix of both | Balanced | Complexity |

**Linux Kernel Modules:**

```bash
# List loaded modules
lsmod

# Module information
modinfo e1000       # Intel network driver

# Load/unload modules
sudo modprobe module_name
sudo rmmod module_name

# Module dependencies
modprobe --show-depends module_name
```

---

## 3. Shell Layer

### 📌 Description
The **Shell** is a command-line interpreter that provides an interface between the user and the kernel. It accepts commands, interprets them, and passes them to the kernel for execution.

### 🐚 Types of Shells

| Shell | Name | Features |
|-------|------|----------|
| **bash** | Bourne Again Shell | Most popular, default on many systems |
| **sh** | Bourne Shell | Original Unix shell, minimal |
| **zsh** | Z Shell | Advanced features, customizable |
| **fish** | Friendly Interactive Shell | User-friendly, auto-suggestions |
| **csh** | C Shell | C-like syntax |
| **ksh** | Korn Shell | Combines sh and csh features |
| **dash** | Debian Almquist Shell | Lightweight, POSIX-compliant |

### 🎯 Shell Functions

1. **Command Interpretation**
   - Parses and executes commands
   - Expands wildcards and variables
   - Handles redirections and pipes

2. **Scripting**
   - Write automated scripts
   - Conditional statements and loops
   - Functions and variables

3. **Job Control**
   - Manage foreground/background processes
   - Suspend and resume jobs

4. **Command History**
   - Store previous commands
   - Quick recall and editing

5. **Environment Management**
   - Set environment variables
   - Configure shell behavior

### 📝 Shell Features

**Command Line Editing:**
```bash
# Navigate
Ctrl+A         # Beginning of line
Ctrl+E         # End of line
Ctrl+U         # Delete to beginning
Ctrl+K         # Delete to end

# History
↑ / ↓          # Previous/next command
Ctrl+R         # Search history
history        # View command history
!!             # Execute last command
!n             # Execute command #n
!string        # Execute last command starting with string
```

**Variables:**
```bash
# Set variable
name="John"
export PATH="/usr/local/bin:$PATH"

# Use variable
echo $name
echo ${name}

# Special variables
$?             # Exit status of last command
$$             # Current shell PID
$!             # PID of last background command
$0             # Script name
$1, $2, ...    # Script arguments
$#             # Number of arguments
$@             # All arguments
```

**Redirection & Pipes:**
```bash
# Output redirection
command > file          # Overwrite
command >> file         # Append
command 2> error.log    # Redirect stderr
command &> output.log   # Redirect stdout & stderr

# Input redirection
command < input.txt

# Pipes
command1 | command2     # Pass output to next command
ls | grep "txt"
ps aux | grep nginx

# Tee (output to file and stdout)
command | tee output.txt
```

**Wildcards & Globbing:**
```bash
*              # Match any characters
?              # Match single character
[abc]          # Match a, b, or c
[a-z]          # Match range
[!abc]         # Match anything except a, b, c

# Examples
ls *.txt       # All .txt files
ls file?.txt   # file1.txt, file2.txt, etc.
ls [abc]*      # Files starting with a, b, or c
```

**Command Substitution:**
```bash
# Backticks (old style)
result=`command`

# $() syntax (preferred)
result=$(command)
current_date=$(date)
files=$(ls)
```

**Aliases:**
```bash
# Create alias
alias ll='ls -lah'
alias update='sudo apt update && sudo apt upgrade'

# View aliases
alias

# Remove alias
unalias ll
```

**Shell Scripts:**
```bash
#!/bin/bash
# Simple script example

# Variables
name="Linux"
version=5.15

# Conditional
if [ $version -gt 5 ]; then
    echo "Modern kernel"
fi

# Loop
for file in *.txt; do
    echo "Processing: $file"
done

# Function
greet() {
    echo "Hello, $1!"
}

greet "World"
```

### 🔧 Configuration Files

| File | Purpose |
|------|---------|
| **~/.bashrc** | Bash configuration (interactive shells) |
| **~/.bash_profile** | Bash login configuration |
| **~/.profile** | General shell configuration |
| **~/.zshrc** | Zsh configuration |
| **/etc/profile** | System-wide shell configuration |
| **/etc/bash.bashrc** | System-wide Bash configuration |

---

## 4. User Space (Application Layer)

### 📌 Description
**User Space** is where applications and user programs run. This is the top layer where users interact with the system.

### 🎯 Components

#### 4.1 System Libraries

**GNU C Library (glibc):**
- Standard C library
- Provides system call wrappers
- String manipulation, math functions, I/O

```bash
# View library dependencies
ldd /bin/ls

# Library locations
/lib/           # Essential libraries
/usr/lib/       # User libraries
/usr/local/lib/ # Locally compiled libraries
```

#### 4.2 System Utilities

**Core Utilities:**
```bash
# File operations
ls, cp, mv, rm, mkdir, touch

# Text processing
cat, grep, sed, awk, cut, sort

# System information
ps, top, free, df, du

# Networking
ping, curl, wget, ssh, scp

# User management
useradd, usermod, passwd, su, sudo
```

#### 4.3 Applications

**Categories:**

| Category | Examples |
|----------|----------|
| **Text Editors** | vim, nano, emacs, gedit |
| **Web Browsers** | Firefox, Chrome, Chromium |
| **Office Suite** | LibreOffice, ONLYOFFICE |
| **Development** | VS Code, Eclipse, IntelliJ |
| **Media Players** | VLC, MPV, Rhythmbox |
| **Graphics** | GIMP, Inkscape, Blender |
| **Terminal** | GNOME Terminal, Konsole, Alacritty |

#### 4.4 Desktop Environments

**Popular DEs:**

| Desktop | Description | Resource Usage |
|---------|-------------|----------------|
| **GNOME** | Modern, user-friendly | High |
| **KDE Plasma** | Feature-rich, customizable | Medium-High |
| **XFCE** | Lightweight, traditional | Low |
| **LXQt** | Very lightweight | Very Low |
| **Cinnamon** | Traditional desktop | Medium |
| **MATE** | GNOME 2 fork | Low-Medium |

#### 4.5 Services & Daemons

**Background services:**
```bash
# SystemD services
systemctl status service_name
systemctl start service_name
systemctl stop service_name
systemctl enable service_name    # Start on boot
systemctl disable service_name

# View all services
systemctl list-units --type=service

# View logs
journalctl -u service_name
```

**Common Daemons:**
- **sshd**: SSH server
- **httpd/nginx**: Web servers
- **cron**: Task scheduler
- **systemd**: Init system and service manager
- **NetworkManager**: Network management
- **cupsd**: Printing service

---

## How They Work Together

### 🔄 Complete Flow Example: Opening a File

```
1. USER ACTION
   User types: cat file.txt
              ↓

2. SHELL LAYER
   - Shell interprets command
   - Finds 'cat' executable
   - Prepares arguments
              ↓

3. SYSTEM CALL
   - Shell invokes open() system call
   - Switches to kernel mode
              ↓

4. KERNEL LAYER
   - Validates permissions
   - Locates file on disk
   - Allocates memory buffer
   - Reads file data
              ↓

5. HARDWARE LAYER
   - Disk controller accesses storage
   - Data transferred to RAM
              ↓

6. RETURN PATH
   Kernel → Shell → User
   File contents displayed on screen
```

### 🔄 Network Request Example

```
1. Application sends HTTP request
              ↓
2. System call: socket(), connect()
              ↓
3. Kernel TCP/IP stack processes
              ↓
4. Network device driver
              ↓
5. Network hardware (NIC) transmits
              ↓
6. Response follows reverse path
```

---

## Architecture Diagram

### Detailed Architecture

```
╔═══════════════════════════════════════════════════╗
║                  USER SPACE                       ║
║  ┌──────────────────────────────────────────┐     ║
║  │  User Applications & Desktop             │     ║
║  │  (Firefox, LibreOffice, Games, etc.)     │     ║
║  └──────────────────────────────────────────┘     ║
║  ┌──────────────────────────────────────────┐     ║
║  │  System Utilities & Libraries            │     ║
║  │  (GNU Coreutils, glibc, GTK, Qt)         │     ║
║  └──────────────────────────────────────────┘     ║
╚═══════════════════════════════════════════════════╝
                      ↕
╔═══════════════════════════════════════════════════╗
║                  SHELL LAYER                      ║
║  ┌──────────────────────────────────────────┐     ║
║  │  Command Interpreters                    │     ║
║  │  (bash, zsh, fish, sh)                   │     ║
║  └──────────────────────────────────────────┘     ║
╚═══════════════════════════════════════════════════╝
                      ↕
        ═════════ System Call Interface ═════════
                      ↕
╔═══════════════════════════════════════════════════╗
║                  KERNEL SPACE                     ║
║  ┌──────────────────────────────────────────┐     ║
║  │  Process Scheduler                       │     ║
║  └──────────────────────────────────────────┘     ║
║  ┌─────────┐ ┌──────────┐ ┌─────────────┐         ║
║  │ Process │ │  Memory  │ │ File System │         ║
║  │   Mgmt  │ │   Mgmt   │ │    Mgmt     │         ║
║  └─────────┘ └──────────┘ └─────────────┘         ║
║  ┌──────────────────────────────────────────┐     ║
║  │  Network Stack (TCP/IP)                  │     ║
║  └──────────────────────────────────────────┘     ║
║  ┌──────────────────────────────────────────┐     ║
║  │  Device Drivers (Block, Char, Network)   │     ║
║  └──────────────────────────────────────────┘     ║
╚═══════════════════════════════════════════════════╝
                      ↕
╔═══════════════════════════════════════════════════╗
║                  HARDWARE LAYER                   ║
║  ┌────────┐ ┌────────┐ ┌──────────┐ ┌────────┐    ║
║  │  CPU   │ │  RAM   │ │  Storage │ │Network │    ║
║  └────────┘ └────────┘ └──────────┘ └────────┘    ║
║  ┌────────────────────────────────────────────┐   ║
║  │  Peripherals (Keyboard, Mouse, Display)    │   ║
║  └────────────────────────────────────────────┘   ║
╚═══════════════════════════════════════════════════╝
```

---

## Kernel Space vs User Space

### Key Differences

| Aspect | Kernel Space | User Space |
|--------|--------------|------------|
| **Privilege** | Privileged mode | Restricted mode |
| **Memory Access** | Full access to all memory | Limited to own memory |
| **CPU Instructions** | All instructions allowed | Some restricted |
| **Crashes** | System crash (kernel panic) | Only application crashes |
| **Performance** | Direct hardware access | Indirect through system calls |
| **Security** | High risk if compromised | Isolated from system |

### Memory Layout

```
High Address (0xFFFFFFFF)
┌─────────────────────────┐
│    Kernel Space         │ ← Only kernel can access
│    (1 GB typically)     │
├─────────────────────────┤ ← 0xC0000000 (on 32-bit)
│                         │
│    User Space           │ ← Applications run here
│    (3 GB typically)     │
│                         │
└─────────────────────────┘
Low Address (0x00000000)
```

### Protection Rings (x86 Architecture)

```
Ring 0 (Kernel)    - Highest privilege
Ring 1             - Device drivers (rarely used)
Ring 2             - Device drivers (rarely used)
Ring 3 (User)      - User applications
```

---

## Boot Process

Understanding how Linux boots helps understand the architecture:

### Boot Sequence

```
1. BIOS/UEFI
   ↓
2. Bootloader (GRUB)
   - Loads kernel into memory
   ↓
3. Kernel Initialization
   - Decompresses itself
   - Initializes hardware
   - Mounts root filesystem
   ↓
4. Init System (systemd/init)
   - First user space process (PID 1)
   - Starts system services
   ↓
5. Login Manager
   - Display manager (graphical)
   - getty (text console)
   ↓
6. User Session
   - Shell starts
   - Desktop environment loads
   ↓
7. User Applications
   - User can now run programs
```

### Viewing Boot Process

```bash
# View boot messages
dmesg
dmesg | less

# View boot log
journalctl -b

# Check boot time
systemd-analyze
systemd-analyze blame    # What took time

# View init process
ps -p 1
```

---

## Conclusion

### 🎯 Key Takeaways

1. **Linux architecture** is **layered and modular**
2. **Hardware** provides physical resources
3. **Kernel** manages resources and provides services
4. **Shell** provides command-line interface
5. **User Space** is where applications run
6. **System calls** connect user space to kernel
7. **Separation** between kernel and user space provides security and stability

### 💡 Why This Architecture?

✅ **Security**: User space isolated from kernel  
✅ **Stability**: Application crashes don't crash system  
✅ **Portability**: Hardware abstraction  
✅ **Modularity**: Easy to add/remove components  
✅ **Performance**: Efficient resource management  
✅ **Flexibility**: Customizable at every layer  

---

## Quick Reference

### Architecture Summary

| Layer | Function | Examples |
|-------|----------|----------|
| **User Space** | Applications | Firefox, vim, games |
| **Shell** | Command interface | bash, zsh |
| **Kernel** | Resource management | Process, memory, file systems |
| **Hardware** | Physical resources | CPU, RAM, disk |

### Important Directories

```bash
/boot       # Kernel and boot files
/dev        # Device files
/proc       # Process information (virtual)
/sys        # System information (virtual)
/etc        # Configuration files
/lib        # System libraries
/usr        # User programs
/var        # Variable data (logs)
/home       # User home directories
```

---

## Resources

### Documentation
- [Linux Kernel Documentation](https://www.kernel.org/doc/)
- [The Linux Programming Interface](http://man7.org/tlpi/)
- [Linux From Scratch](http://www.linuxfromscratch.org/)

### Books
- "Linux Kernel Development" - Robert Love
- "Understanding the Linux Kernel" - Daniel P. Bovet
- "The Linux Programming Interface" - Michael Kerrisk

### Online Resources
- [kernel.org](https://www.kernel.org/)
- [Linux Journey](https://linuxjourney.com/)
- [Linux Documentation Project](https://www.tldp.org/)



<br>




**Happy Learning! 🚀**

*Contributions and suggestions are welcome!*

---

**Maintained by: [Sablu Chaudhary](https://github.com/sabluchaudhary555)** 🔗 **Connect with me:** [LinkedIn](https://www.linkedin.com/in/sablu-chaudhary555/) | [GitHub](https://github.com/sabluchaudhary555)

---
**Made with ❤️ for the Open Source Community**