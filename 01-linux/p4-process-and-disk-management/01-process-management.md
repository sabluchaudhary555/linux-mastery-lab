# Linux Process Management

A quick reference guide for managing processes in Linux using `ps`, `top`, `htop`, `kill`, and `nice`.

---

## 📋 Table of Contents
- [ps - Process Status](#ps---process-status)
- [top - Real-Time Process Monitor](#top---real-time-process-monitor)
- [htop - Interactive Process Viewer](#htop---interactive-process-viewer)
- [kill - Terminate Processes](#kill---terminate-processes)
- [nice - Process Priority](#nice---process-priority)

---

## `ps` - Process Status

Display information about active processes.

### Basic Usage
```bash
ps              # Show processes for current shell
ps -e           # Show all processes
ps -ef          # Full format listing
ps -aux         # BSD style - detailed info
```

### Common Options
| Option | Description |
|--------|-------------|
| `-e` or `-A` | Show all processes |
| `-f` | Full format listing |
| `-u username` | Processes for specific user |
| `-p PID` | Info for specific process ID |
| `aux` | Detailed BSD format |
| `--sort` | Sort by column (e.g., `--sort=-%mem`) |

### Useful Examples
```bash
# Find specific process
ps aux | grep firefox

# Show processes by memory usage
ps aux --sort=-%mem | head

# Show processes by CPU usage
ps aux --sort=-%cpu | head

# Process tree (hierarchy)
ps -ejH
ps axjf

# Custom output format
ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%mem
```

---

## `top` - Real-Time Process Monitor

Interactive real-time view of running processes.

### Basic Usage
```bash
top             # Start top
top -u username # Show processes for specific user
top -p PID      # Monitor specific process
```

### Interactive Commands (While Running)

| Key | Action |
|-----|--------|
| `h` or `?` | Help |
| `q` | Quit |
| `k` | Kill a process |
| `r` | Renice (change priority) |
| `M` | Sort by memory usage |
| `P` | Sort by CPU usage |
| `T` | Sort by time |
| `u` | Filter by user |
| `c` | Toggle command/program name |
| `V` | Forest view (tree) |
| `1` | Show individual CPU cores |
| `d` or `s` | Change refresh interval |
| `Space` | Refresh immediately |

### Understanding the Display
```
top - 14:30:45 up 2 days,  3:21,  2 users,  load average: 0.52, 0.58, 0.59
Tasks: 245 total,   1 running, 244 sleeping,   0 stopped,   0 zombie
%Cpu(s):  3.2 us,  1.1 sy,  0.0 ni, 95.5 id,  0.2 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem :   7842.5 total,    892.3 free,   4234.2 used,   2716.0 buff/cache
MiB Swap:   2048.0 total,   1024.0 free,   1024.0 used.   3156.4 avail Mem

  PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
 1234 user      20   0 1234567 123456  12345 S   5.3   1.6   12:34.56 firefox
```

**Key Columns:**
- `PID` - Process ID
- `USER` - Process owner
- `PR` - Priority
- `NI` - Nice value
- `VIRT` - Virtual memory
- `RES` - Physical memory
- `%CPU` - CPU usage
- `%MEM` - Memory usage
- `TIME+` - Total CPU time
- `COMMAND` - Process name

### Useful Options
```bash
# Batch mode (for scripts)
top -b -n 1

# Show specific number of processes
top -n 1 -b | head -20

# Set refresh interval (2 seconds)
top -d 2
```

---

## `htop` - Interactive Process Viewer

Enhanced version of `top` with better interface and features.

### Installation
```bash
# Ubuntu/Debian
sudo apt install htop

# Fedora/RHEL
sudo dnf install htop

# Arch Linux
sudo pacman -S htop
```

### Basic Usage
```bash
htop            # Start htop
htop -u username # Show processes for specific user
htop -p PID     # Monitor specific processes
```

### Interactive Keys

| Key | Action |
|-----|--------|
| `F1` or `h` | Help |
| `F2` | Setup menu |
| `F3` or `/` | Search process |
| `F4` or `\` | Filter processes |
| `F5` | Tree view |
| `F6` | Sort by column |
| `F9` | Kill process |
| `F10` or `q` | Quit |
| `Space` | Tag/untag process |
| `U` | Untag all |
| `k` | Kill tagged processes |
| `t` | Tree/list view toggle |
| `H` | Hide/show user threads |
| `K` | Hide/show kernel threads |
| `I` | Invert sort order |
| `l` | Show open files (lsof) |
| `s` | System call trace (strace) |

### Advantages Over `top`
- Mouse support
- Colored interface
- Easier navigation
- Tree view by default
- Easier process killing
- Better visual representation
- Horizontal/vertical scrolling

---

## `kill` - Terminate Processes

Send signals to processes (not just for killing).

### Basic Usage
```bash
kill PID           # Send TERM signal (graceful)
kill -9 PID        # Send KILL signal (force)
kill -15 PID       # Send TERM signal (same as default)
killall name       # Kill by process name
pkill pattern      # Kill by pattern match
```

### Common Signals

| Signal | Number | Description | Usage |
|--------|--------|-------------|-------|
| `SIGHUP` | 1 | Hangup | Reload config |
| `SIGINT` | 2 | Interrupt | Ctrl+C |
| `SIGQUIT` | 3 | Quit | Ctrl+\ |
| `SIGKILL` | 9 | Kill (forced) | Cannot be caught |
| `SIGTERM` | 15 | Terminate (default) | Graceful shutdown |
| `SIGSTOP` | 19 | Stop | Pause process |
| `SIGCONT` | 18 | Continue | Resume process |

### Examples
```bash
# List all signals
kill -l

# Graceful termination (allows cleanup)
kill 1234
kill -TERM 1234
kill -15 1234

# Force kill (immediate termination)
kill -9 1234
kill -KILL 1234

# Reload configuration (e.g., nginx)
kill -HUP 1234
kill -1 1234

# Kill by process name
killall firefox
killall -9 firefox

# Kill by pattern
pkill fire
pkill -9 -f "python.*script.py"

# Kill all processes for a user
pkill -u username
killall -u username

# Interactive kill
kill -9 $(pgrep firefox)
```

### Safe Kill Sequence
```bash
# 1. Try graceful termination
kill PID

# 2. Wait a few seconds
sleep 5

# 3. Check if still running
ps -p PID

# 4. Force kill if necessary
kill -9 PID
```

---

## `nice` - Process Priority

Control process scheduling priority (-20 to 19, lower = higher priority).

### Understanding Priority
- **Nice values:** `-20` (highest priority) to `19` (lowest priority)
- **Default:** `0` (normal priority)
- **Only root** can set negative nice values (higher priority)
- Regular users can only lower priority (positive values)

### Basic Usage
```bash
# Start process with specific nice value
nice -n 10 command

# Start with low priority
nice -n 19 ./long-running-script.sh

# Start with high priority (requires root)
sudo nice -n -10 important-process

# Default nice (if -n not specified, uses 10)
nice command
```

### `renice` - Change Priority of Running Process
```bash
# Change priority of running process
renice -n 5 -p PID

# Change priority by user
renice -n 10 -u username

# Change priority by group
renice -n 5 -g groupname

# Lower priority of specific process
renice +10 1234

# Increase priority (requires root)
sudo renice -10 1234
```

### Practical Examples
```bash
# Run backup with lowest priority
nice -n 19 tar -czf backup.tar.gz /data/

# Run critical database with high priority
sudo nice -n -5 ./database-server

# Lower priority of running process
renice -n 15 -p $(pgrep firefox)

# Background process with low priority
nice -n 15 ./heavy-computation.sh &

# Monitor nice values
ps -eo pid,ni,comm
```

### `ionice` - I/O Priority (Bonus)
```bash
# Set I/O priority (requires ionice package)
ionice -c 3 -p PID        # Idle class
ionice -c 2 -n 7 command  # Best effort, priority 7
ionice -c 1 -n 4 command  # Real-time, priority 4

# Classes:
# 1 = Real-time (highest)
# 2 = Best-effort (normal)
# 3 = Idle (lowest)
```

---

## 🔗 Quick Reference Card

### Process Discovery
```bash
ps aux                    # All processes, detailed
ps -ef                    # All processes, full format
ps aux | grep process     # Find specific process
pgrep process_name        # Get PID by name
pidof process_name        # Get PID(s) by exact name
```

### Process Monitoring
```bash
top                       # Real-time monitor
htop                      # Enhanced monitor
top -u username           # Monitor user's processes
watch -n 1 'ps aux'       # Refresh every second
```

### Process Termination
```bash
kill PID                  # Graceful stop
kill -9 PID               # Force kill
killall name              # Kill by name
pkill pattern             # Kill by pattern
kill -STOP PID            # Pause process
kill -CONT PID            # Resume process
```

### Process Priority
```bash
nice -n 10 command        # Start with low priority
nice -n -5 command        # Start with high priority (root)
renice -n 5 -p PID        # Change priority
ps -eo pid,ni,comm        # View nice values
```

---

## 💡 Pro Tips

1. **Always try graceful kill first** (`kill PID`) before force kill (`kill -9 PID`)
2. **Use `htop` instead of `top`** for better user experience
3. **Combine with grep** for finding processes: `ps aux | grep nginx`
4. **Background tasks** should use nice: `nice -n 19 ./script.sh &`
5. **Watch CPU hogs**: `ps aux --sort=-%cpu | head`
6. **Watch memory hogs**: `ps aux --sort=-%mem | head`
7. **Process hierarchy**: `pstree -p` or `ps axjf`
8. **Check before killing**: Always verify PID with `ps -p PID`

---

## 🚨 Common Mistakes to Avoid

```bash
# ❌ DON'T: Kill PID 1 (init/systemd)
kill -9 1

# ❌ DON'T: Kill all processes blindly
killall -9 *

# ❌ DON'T: Use kill -9 as first option
kill -9 PID  # Try kill PID first

# ✅ DO: Verify before killing
ps -p PID
kill PID
sleep 2
ps -p PID && kill -9 PID
```

---

## 📚 Additional Resources

- `man ps` - Process status manual
- `man top` - Top manual
- `man kill` - Kill command manual
- `man nice` - Nice manual
- `man renice` - Renice manual
- `man signal` - Signal descriptions
- [Linux Process Management Tutorial](https://www.kernel.org/doc/html/latest/)

---

## 📝 Practice Exercises

```bash
# 1. Find all Firefox processes
ps aux | grep firefox

# 2. Monitor system in real-time
htop

# 3. Start a low-priority background job
nice -n 19 sleep 1000 &

# 4. Find and kill a process
pgrep sleep
kill $(pgrep sleep)

# 5. View process tree
pstree -p $$

# 6. Monitor specific user
top -u $USER

# 7. Change priority of running process
renice -n 10 -p $(pgrep sleep)
```

---

## ⚙️ Quick Aliases (Add to ~/.bashrc)

```bash
# Process management aliases
alias psg='ps aux | grep -v grep | grep -i -e VSZ -e'
alias psme='ps aux | grep $USER'
alias topcpu='ps aux --sort=-%cpu | head -10'
alias topmem='ps aux --sort=-%mem | head -10'
alias pstree='pstree -p'

# Safe kill function
killp() {
    ps aux | grep "$1" | grep -v grep
    read -p "Kill these processes? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pkill "$1"
    fi
}
```

---

**Happy Learning! 🚀**

*Contributions and suggestions are welcome!*

---

**Maintained by: [Sablu Chaudhary](https://github.com/sabluchaudhary555)** 🔗 **Connect with me:** [LinkedIn](https://www.linkedin.com/in/sablu-chaudhary555/) | [GitHub](https://github.com/sabluchaudhary555)

---
**Made with ❤️ for the Open Source Community**