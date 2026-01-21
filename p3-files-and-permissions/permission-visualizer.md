# Linux Permission Visualizer

A Python tool that displays file and directory permissions in multiple formats with detailed explanations, security assessments, and recommendations.

## Overview

Understanding Linux permissions can be confusing. This tool transforms cryptic permission codes into clear, visual explanations that help you understand exactly who can do what with your files.

## Features

- **Multiple Formats** - Shows permissions in symbolic (rwxrwxrwx) and numeric (755) notation
- **Visual Breakdown** - Color-coded permission analysis for owner, group, and others
- **Calculation Explanation** - Shows how numeric permissions are calculated (4+2+1)
- **Security Assessment** - Identifies dangerous permissions and security risks
- **Smart Recommendations** - Suggests appropriate permissions based on file type
- **Common Use Cases** - Shows typical scenarios for each permission set
- **File Type Detection** - Identifies directories, symlinks, executables, and more

## Installation

1. Save the script as `permission-visualizer.py`
2. Make it executable:
```bash
chmod +x permission-visualizer.py
```

## Usage

### Single File
```bash
python3 permission-visualizer.py myfile.txt
```

### Multiple Files
```bash
python3 permission-visualizer.py file1.txt file2.sh config.json
```

### Using Wildcards
```bash
python3 permission-visualizer.py /path/to/files/*
```

### Direct Execution
```bash
./permission-visualizer.py script.sh
```

## Output Sections

### 1. Symbolic Notation
Shows traditional Unix permission format:
```
drwxr-xr-x
│ │  │  │
│ │  │  └──── Other (Everyone)
│ │  └─────── Group
│ └────────── Owner
└─────────── File Type
```

### 2. Numeric Notation
Shows octal permission format:
```
755
│││
││└──── Other: 5 = r-x
│└───── Group: 5 = r-x
└────── Owner: 7 = rwx
```

### 3. Calculation Breakdown
Explains how numbers are calculated:
```
Owner: 7 = Read(4) + Write(2) + Execute(1) = rwx
Group: 5 = Read(4) + Execute(1) = r-x
Other: 5 = Read(4) + Execute(1) = r-x
```

### 4. Detailed Breakdown
Shows what each permission means:
- ✓ Read (r) - Can view file contents
- ✓ Write (w) - Can modify file contents
- ✗ Execute (x) - Cannot run file as program

### 5. Security Assessment
Identifies dangerous permissions:
- ⚠️ World-writable files (anyone can modify)
- ⚠️ Dangerous 777 or 666 permissions
- ✓ Safe permission configurations

### 6. Recommendations
Suggests better permissions:
```
• chmod 644 myfile.txt  (standard file)
• chmod 755 script.sh   (executable)
• chmod 600 secret.key  (private file)
```

### 7. Common Use Cases
Shows typical scenarios for the permission set

## Understanding Permissions

### Permission Values
- **Read (r)** = 4
- **Write (w)** = 2
- **Execute (x)** = 1

### Common Permission Sets

**Files:**
- `644` - Standard file (owner can write, everyone can read)
- `600` - Private file (only owner can read/write)
- `755` - Executable script (owner can modify, everyone can run)
- `400` - Read-only secret (maximum security)

**Directories:**
- `755` - Standard directory (owner can modify, everyone can access)
- `700` - Private directory (only owner has access)
- `775` - Shared directory (group can modify)

### Security Risks

**Dangerous Permissions:**
- `777` - Everyone has full access (NEVER use this!)
- `666` - Everyone can read and write
- `---w-` - World-writable (anyone can modify)

## Requirements

- **OS:** Linux, macOS, or any Unix-like system
- **Python:** 3.6 or higher
- **Dependencies:** Standard library only (os, sys, stat modules)

## Examples

### Analyzing a Script
```bash
python3 permission-visualizer.py myscript.sh
```
Shows if script is executable and recommends appropriate permissions.

### Checking Configuration Files
```bash
python3 permission-visualizer.py ~/.ssh/config
```
Verifies SSH config has secure permissions (should be 600).

### Directory Analysis
```bash
python3 permission-visualizer.py /var/www/html
```
Checks web directory permissions for security.

### Batch Analysis
```bash
python3 permission-visualizer.py ~/.ssh/*
```
Analyzes all files in SSH directory at once.

## Color Coding

- **Green (✓)** - Permission granted
- **Red (✗)** - Permission denied
- **Yellow** - Section headers
- **Cyan** - Important information
- **Red warnings** - Security risks

## File Types Detected

- 📄 Regular File
- 📁 Directory
- 🔗 Symbolic Link
- 🔵 Block Device
- ⚙️ Character Device
- 📡 Named Pipe (FIFO)
- 🔌 Socket

## Use Cases

- **Security Auditing** - Find insecure file permissions
- **Learning** - Understand how Linux permissions work
- **Troubleshooting** - Diagnose permission-related issues
- **Documentation** - Generate permission reports
- **Best Practices** - Ensure files have appropriate permissions

## Tips

1. **Check critical files regularly:**
```bash
python3 permission-visualizer.py ~/.ssh/id_rsa
```

2. **Audit web directories:**
```bash
python3 permission-visualizer.py /var/www/*
```

3. **Verify script permissions:**
```bash
python3 permission-visualizer.py ~/bin/*
```

## Troubleshooting

**"Permission denied"** - You don't have rights to view file stats; try with sudo

**"File not found"** - Check the path is correct and file exists

**No color output** - Your terminal may not support ANSI colors

## License

Developed by SSoft.in

---

*Make Linux permissions crystal clear!*