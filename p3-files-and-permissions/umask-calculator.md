# umask Calculator & Simulator

A comprehensive Python tool that explains, calculates, and simulates how umask values affect default file and directory permissions in Linux/Unix systems.

## Overview

Understanding umask can be confusing. This interactive calculator shows exactly how umask values translate to actual file permissions, with security analysis, practical use cases, and step-by-step explanations.

## Features

- **Interactive Calculator** - Menu-driven interface for exploring umask values
- **Custom Calculations** - Calculate permissions for any umask value
- **Preset Values** - 5 common umask configurations with explanations
- **Comparison Table** - Side-by-side comparison of all presets
- **Step-by-Step Math** - Shows how permissions are calculated
- **Security Analysis** - Identifies risks and security levels
- **Use Case Suggestions** - Practical scenarios for each umask
- **Command Examples** - How to set umask temporarily or permanently
- **Educational Mode** - Learn what umask is and how it works

## Installation

1. Save the script as `umask-calculator.py`
2. Make it executable:
```bash
chmod +x umask-calculator.py
```

## Usage

### Interactive Mode
```bash
python3 umask-calculator.py
```

Launches the interactive menu with options to:
1. Calculate custom umask values
2. View preset configurations
3. Compare all presets
4. Learn about umask
5. Exit

### Command Line Mode
```bash
python3 umask-calculator.py 0022
```

Displays detailed analysis for the specified umask value.

### Direct Execution
```bash
./umask-calculator.py 0077
```

## Understanding umask

### What is umask?

umask (User Mask) sets **default permissions** for newly created files and directories by **subtracting** from maximum permissions.

**Formula:**
- Files: `666 (rw-rw-rw-) - umask = actual permissions`
- Directories: `777 (rwxrwxrwx) - umask = actual permissions`

### Example Calculation

For umask `0022`:
```
FILES:
  Maximum: 666 (rw-rw-rw-)
  Minus:  -022
  Result:  644 (rw-r--r--)

DIRECTORIES:
  Maximum: 777 (rwxrwxrwx)
  Minus:  -022
  Result:  755 (rwxr-xr-x)
```

## Preset umask Values

### 0022 - Standard (Default)
- **Files:** 644 (rw-r--r--)
- **Dirs:** 755 (rwxr-xr-x)
- **Security:** Moderate
- **Use Case:** Most common, general purpose
- Owner can modify, everyone can read

### 0077 - Private (Secure)
- **Files:** 600 (rw-------)
- **Dirs:** 700 (rwx------)
- **Security:** Maximum
- **Use Case:** Personal files, SSH keys, sensitive data
- Only owner has any access

### 0002 - Group Writable
- **Files:** 664 (rw-rw-r--)
- **Dirs:** 775 (rwxrwxr-x)
- **Security:** Low
- **Use Case:** Team collaboration, shared projects
- Group members can modify

### 0027 - Restricted Group
- **Files:** 640 (rw-r-----)
- **Dirs:** 750 (rwxr-x---)
- **Security:** High
- **Use Case:** Departmental files, limited sharing
- Group can read, no access for others

### 0000 - Unrestricted
- **Files:** 666 (rw-rw-rw-)
- **Dirs:** 777 (rwxrwxrwx)
- **Security:** None (DANGEROUS!)
- **Use Case:** Testing only, NEVER production
- Everyone has full access

## Output Sections

### 1. Calculation Steps
Shows the mathematical subtraction:
```
FILES:
  Maximum permissions:  666 (rw-rw-rw-)
  Minus umask:         -022
  ─────────────────────────
  Result:               644 (rw-r--r--)
```

### 2. Detailed Breakdown
Explains what each permission group can do:
```
Owner (rw-): Can read, write
Group (r--): Can read
Other (r--): Can read
```

### 3. Security Analysis
Identifies risks and security level:
- 🟢 Maximum/High Security
- 🟡 Moderate/Low Security
- 🔴 Very Low Security
- ⚠️ Warnings for dangerous permissions

### 4. Use Cases
Suggests practical scenarios for the umask value

### 5. Commands
Shows how to set the umask:
- Temporary (current session)
- Permanent (user profile)
- System-wide (all users)

## Requirements

- **OS:** Linux, macOS, or any Unix-like system
- **Python:** 3.6 or higher
- **Dependencies:** Standard library only (os, sys modules)

## Examples

### Check Your Current umask
```bash
umask
```

### Set umask Temporarily
```bash
umask 0022
```

### Set umask Permanently
Add to `~/.bashrc`:
```bash
echo 'umask 0022' >> ~/.bashrc
source ~/.bashrc
```

### Test Your umask
```bash
# Create test files
touch testfile.txt
mkdir testdir

# Check their permissions
ls -l testfile.txt
ls -ld testdir

# Clean up
rm testfile.txt
rmdir testdir
```

## Common Use Cases

### Secure Personal Files
```bash
umask 0077  # Private files only you can access
```

### Web Server Content
```bash
umask 0022  # Readable by web server, writable by owner
```

### Team Development
```bash
umask 0002  # Group can collaborate on files
```

### Confidential Documents
```bash
umask 0027  # Group can view, others have no access
```

## Security Best Practices

### Good umask Values
- **0022** - General purpose, standard default
- **0027** - More secure for shared systems
- **0077** - Maximum security for personal data

### Dangerous umask Values
- **0000** - Everyone can read/write everything (NEVER use!)
- **0002** - Requires trust in all group members
- Values with world-write (e.g., 0020, 0002, 0000)

### Recommendations
1. Use **0022** for most situations
2. Use **0077** for home directories and SSH keys
3. Use **0027** for department servers
4. Avoid world-writable permissions
5. Test new umask values before applying system-wide

## Comparison Table

| umask | Files       | Directories | Security Level | Best For |
|-------|-------------|-------------|----------------|----------|
| 0000  | 666 (rw-rw-rw-) | 777 (rwxrwxrwx) | None | Testing only |
| 0002  | 664 (rw-rw-r--) | 775 (rwxrwxr-x) | Low | Team projects |
| 0022  | 644 (rw-r--r--) | 755 (rwxr-xr-x) | Moderate | General use |
| 0027  | 640 (rw-r-----) | 750 (rwxr-x---) | High | Department files |
| 0077  | 600 (rw-------) | 700 (rwx------) | Maximum | Private data |

## Interactive Menu

```
MENU:
  1. Calculate custom umask value
  2. View preset umask values
  3. Compare all presets
  4. Learn about umask
  5. Exit
```

### Option 1: Custom Calculator
Enter any umask value for complete analysis

### Option 2: Presets
Choose from 5 common configurations

### Option 3: Comparison
See all presets side-by-side

### Option 4: Tutorial
Learn how umask works

## Troubleshooting

**"Invalid umask value"** - Use 4 octal digits (0-7), e.g., 0022

**Permissions don't match** - Check if other factors (ACLs, SELinux) are affecting permissions

**Changes not persisting** - Add umask to shell config file (~/.bashrc)

**System-wide changes not working** - Check /etc/profile and /etc/bashrc

## Technical Details

### Octal Notation
Each digit represents permissions for:
- First digit: Owner
- Second digit: Group
- Third digit: Other

### Permission Values
- **r (read)** = 4
- **w (write)** = 2
- **x (execute)** = 1

### Maximum Permissions
- **Files:** 666 (no execute by default for security)
- **Directories:** 777 (execute = access/enter)

## Related Commands

- `umask` - Display or set umask value
- `chmod` - Change file permissions
- `ls -l` - View file permissions
- `stat` - Detailed file information

## License

Developed by SSoft.in

---

*Master umask and control your default permissions!*