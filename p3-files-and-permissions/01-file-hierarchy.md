# Linux File Hierarchy Standard (FHS)

## Quick Reference Table

| Directory | Purpose | Typical Contents |
|-----------|---------|------------------|
| `/` | Root directory | Top-level of filesystem hierarchy |
| `/bin` | Essential binaries | Basic commands (ls, cp, cat, bash) |
| `/boot` | Boot loader files | Kernel, initrd, bootloader config |
| `/dev` | Device files | Hardware device nodes (sda, tty) |
| `/etc` | Configuration files | System-wide config files |
| `/home` | User directories | Personal files and settings |
| `/lib` | Essential libraries | Shared libraries for /bin and /sbin |
| `/media` | Removable media | USB drives, CDs mount points |
| `/mnt` | Temporary mounts | Temporary filesystem mounts |
| `/opt` | Optional software | Third-party applications |
| `/proc` | Process information | Virtual filesystem for processes |
| `/root` | Root user home | Home directory for root |
| `/sbin` | System binaries | Administrative commands (fsck, reboot) |
| `/srv` | Service data | Data for services (web, FTP) |
| `/tmp` | Temporary files | Temporary storage (cleared on reboot) |
| `/usr` | User programs | Secondary hierarchy for user data |
| `/var` | Variable data | Logs, caches, spool files |

---

## Detailed Overview

### Essential Directories

**`/` (Root)**
The top-level directory from which all other directories branch. Everything in Linux exists under this directory.

**`/bin` (Binaries)**
Contains essential command binaries needed in single-user mode and for all users. Examples include `ls`, `cp`, `mv`, `cat`, `bash`, and `mkdir`. These commands are required for basic system operation.

**`/boot` (Boot)**
Holds static files needed for the boot process, including the Linux kernel (`vmlinuz`), initial RAM disk (`initrd`), and bootloader configuration files (GRUB).

**`/dev` (Devices)**
Contains device files representing hardware components. Examples: `/dev/sda` (hard disk), `/dev/tty` (terminals), `/dev/null` (null device). These are special files that provide interface to device drivers.

**`/etc` (Et Cetera)**
Stores system-wide configuration files and shell scripts used during boot. Examples include `/etc/passwd` (user accounts), `/etc/fstab` (filesystem mounts), and `/etc/hosts` (hostname resolution). No binaries are stored here.

**`/home` (Home)**
Contains personal directories for regular users. Each user has a subdirectory (e.g., `/home/john`) where they store personal files, documents, and user-specific configurations.

### Library and Runtime Directories

**`/lib` (Libraries)**
Contains essential shared libraries needed by binaries in `/bin` and `/sbin`. Also includes kernel modules in `/lib/modules`.

**`/proc` (Process)**
A virtual filesystem providing process and system information. Files like `/proc/cpuinfo`, `/proc/meminfo`, and `/proc/<PID>/` provide runtime system data. Not stored on disk.

**`/sys` (System)**
Another virtual filesystem exposing kernel data structures, device information, and hardware configuration to userspace.

### Mount Points

**`/media` (Media)**
Standard mount point for removable media devices. Modern systems auto-mount USB drives, CDs, and DVDs here (e.g., `/media/usb`).

**`/mnt` (Mount)**
Temporary mount point for system administrators to manually mount filesystems (e.g., mounting a network share or additional disk).

### Optional and Service Directories

**`/opt` (Optional)**
Reserved for installation of add-on application software packages. Third-party applications are often installed here to keep them separate from system files.

**`/srv` (Service)**
Contains site-specific data served by the system, such as web server data (`/srv/www`) or FTP files (`/srv/ftp`).

### Administrative Directories

**`/root` (Root Home)**
The home directory for the root (superuser) account. Separate from `/home` for security and accessibility during system recovery.

**`/sbin` (System Binaries)**
Contains essential system administration binaries typically requiring root privileges. Examples: `fsck`, `ifconfig`, `reboot`, `shutdown`.

### Variable Data

**`/tmp` (Temporary)**
Stores temporary files created by applications and users. Typically cleared on reboot. All users have read/write access with sticky bit set for security.

**`/var` (Variable)**
Contains variable data files that change during system operation:
- `/var/log` - System and application log files
- `/var/cache` - Application cache data
- `/var/spool` - Print queues, mail queues
- `/var/tmp` - Temporary files preserved between reboots
- `/var/www` - Web server content (common convention)

### User Hierarchy

**`/usr` (User)**
A secondary hierarchy containing user programs and data:
- `/usr/bin` - User command binaries
- `/usr/sbin` - Non-essential system binaries
- `/usr/lib` - Libraries for /usr/bin and /usr/sbin
- `/usr/local` - Local system administrator software installations
- `/usr/share` - Architecture-independent shared data (documentation, icons)

---

## Key Principles

1. **Separation of concerns:** System files are separate from user files, and essential utilities are separate from optional ones.

2. **Shareable vs unshareable:** Some directories can be shared across systems (like `/usr`), while others are system-specific (like `/etc`).

3. **Static vs variable:** Static files don't change without system administrator intervention, while variable files change during normal operation.

4. **Security:** The hierarchy design supports permission management and system security through logical separation.

---

## Sources

- [Filesystem Hierarchy Standard (FHS) 3.0 - Official Documentation](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html)
- [Linux Foundation - FHS Specification](https://www.linuxfoundation.org/)
- [The Linux Documentation Project - Filesystem Hierarchy](https://tldp.org/LDP/Linux-Filesystem-Hierarchy/html/)
- [Debian Wiki - Filesystem Hierarchy Standard](https://wiki.debian.org/FilesystemHierarchyStandard)



<br>



**Happy Learning! 🚀**

*Contributions and suggestions are welcome!*

---

**Maintained by: [Sablu Chaudhary](https://github.com/sabluchaudhary555)** 🔗 **Connect with me:** [LinkedIn](https://www.linkedin.com/in/sablu-chaudhary555/) | [GitHub](https://github.com/sabluchaudhary555)

---
**Made with ❤️ for the Open Source Community**