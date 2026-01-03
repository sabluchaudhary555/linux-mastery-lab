# Basic Linux Commands

## Table of Contents
- [Overview](#overview)
- [ls - List Directory Contents](#ls---list-directory-contents)
- [cd - Change Directory](#cd---change-directory)
- [pwd - Print Working Directory](#pwd---print-working-directory)
- [mkdir - Make Directory](#mkdir---make-directory)
- [rmdir - Remove Directory](#rmdir---remove-directory)
- [Practical Examples](#practical-examples)
- [Summary](#summary)

---

## Overview

This guide covers the five fundamental Linux commands that every user must master to navigate and manage the filesystem effectively. These commands form the foundation of command-line interaction in Linux/Unix systems.

---

## ls - List Directory Contents

The `ls` command displays files and directories in the current or specified location.

### Syntax
```bash
ls [OPTIONS] [PATH]
```

### Common Options

| Option | Description |
|--------|-------------|
| `ls` | List files in current directory |
| `ls -l` | Long format with detailed information |
| `ls -a` | Show all files including hidden files (starting with .) |
| `ls -lh` | Human-readable file sizes (KB, MB, GB) |
| `ls -R` | Recursive listing of subdirectories |
| `ls -t` | Sort by modification time (newest first) |
| `ls -S` | Sort by file size |

### Examples

```bash
# Basic listing
ls

# Detailed listing with permissions and sizes
ls -l

# Show all files including hidden ones
ls -la

# List specific directory
ls /home/user/Documents

# List with human-readable sizes
ls -lh

# Recursive listing
ls -R

# Sort by modification time
ls -lt
```

### Output Explanation

When using `ls -l`, the output format is:
```
-rw-r--r-- 1 user group 1234 Jan 01 12:00 filename
```
- **-rw-r--r--**: File permissions
- **1**: Number of links
- **user**: Owner name
- **group**: Group name
- **1234**: File size in bytes
- **Jan 01 12:00**: Last modification date and time
- **filename**: Name of the file

---

## cd - Change Directory

The `cd` command navigates between directories in the filesystem hierarchy.

### Syntax
```bash
cd [DIRECTORY]
```

### Common Usage

| Command | Description |
|---------|-------------|
| `cd /path/to/directory` | Navigate to absolute path |
| `cd directory` | Navigate to relative path |
| `cd ..` | Move up one directory level |
| `cd ~` or `cd` | Go to home directory |
| `cd -` | Go to previous directory |
| `cd ../..` | Move up two levels |

### Examples

```bash
# Go to home directory
cd ~
cd

# Navigate to specific path
cd /usr/local/bin

# Relative path navigation
cd Documents/Projects

# Go back one level
cd ..

# Go back two levels
cd ../..

# Return to previous directory
cd -

# Navigate to root directory
cd /
```

### Pro Tips
- Use **Tab** key for auto-completion of directory names
- Use `cd -` to toggle between two directories quickly
- Paths starting with `/` are absolute, others are relative

---

## pwd - Print Working Directory

The `pwd` command displays the full path of the current working directory.

### Syntax
```bash
pwd [OPTIONS]
```

### Common Options

| Option | Description |
|--------|-------------|
| `pwd` | Display current directory path |
| `pwd -P` | Display physical path (resolves symbolic links) |
| `pwd -L` | Display logical path (default, keeps symbolic links) |

### Examples

```bash
# Show current directory
pwd
# Output: /home/user/Documents

# Show physical path (resolve symlinks)
pwd -P

# Show logical path
pwd -L
```

### Use Cases
- Verify your current location before executing commands
- Get the full path for use in scripts or other commands
- Confirm successful navigation after using `cd`

---

## mkdir - Make Directory

The `mkdir` command creates new directories (folders).

### Syntax
```bash
mkdir [OPTIONS] DIRECTORY_NAME
```

### Common Options

| Option | Description |
|--------|-------------|
| `mkdir dirname` | Create a single directory |
| `mkdir -p path/to/dir` | Create parent directories as needed |
| `mkdir -m MODE dirname` | Set permissions during creation |
| `mkdir -v dirname` | Verbose output (show what's being created) |

### Examples

```bash
# Create a single directory
mkdir projects

# Create multiple directories
mkdir docs images videos

# Create nested directories (parent directories created automatically)
mkdir -p projects/2024/january/week1

# Create with specific permissions (755)
mkdir -m 755 public_html

# Create with verbose output
mkdir -v new_folder
# Output: mkdir: created directory 'new_folder'

# Create multiple nested structures
mkdir -p project/{src,bin,docs,tests}
```

### Permission Modes

Common permission values:
- **755**: Owner can read/write/execute, others can read/execute
- **700**: Owner has full access, no access for others
- **644**: Owner can read/write, others can read only

---

## rmdir - Remove Directory

The `rmdir` command removes empty directories only.

### Syntax
```bash
rmdir [OPTIONS] DIRECTORY_NAME
```

### Common Options

| Option | Description |
|--------|-------------|
| `rmdir dirname` | Remove empty directory |
| `rmdir -p path/to/dir` | Remove directory and empty parent directories |
| `rmdir -v dirname` | Verbose output |

### Examples

```bash
# Remove single empty directory
rmdir old_project

# Remove nested empty directories
rmdir -p temp/old/unused

# Remove with verbose output
rmdir -v test_folder
# Output: rmdir: removing directory, 'test_folder'

# Remove multiple empty directories
rmdir dir1 dir2 dir3
```

### Important Notes

- `rmdir` **only works on empty directories**
- To remove non-empty directories, use: `rm -r dirname` (use with caution!)
- To remove non-empty directories with confirmation: `rm -ri dirname`
- Always verify directory contents before deletion

---

## Practical Examples

### Example 1: Creating a Project Structure

```bash
# Check current location
pwd
# Output: /home/user

# Create project structure
mkdir -p myproject/{src,docs,tests,config}

# Navigate into project
cd myproject

# Verify location
pwd
# Output: /home/user/myproject

# List the structure
ls -l
# Output:
# drwxr-xr-x 2 user user 4096 Jan 01 12:00 config
# drwxr-xr-x 2 user user 4096 Jan 01 12:00 docs
# drwxr-xr-x 2 user user 4096 Jan 01 12:00 src
# drwxr-xr-x 2 user user 4096 Jan 01 12:00 tests
```

### Example 2: Navigating the Filesystem

```bash
# Start from home
cd ~

# Go to Documents
cd Documents

# Check location
pwd
# Output: /home/user/Documents

# List files
ls -lh

# Go up one level
cd ..

# Verify
pwd
# Output: /home/user

# Go to previous directory
cd -
# Output: /home/user/Documents
```

### Example 3: Cleaning Up

```bash
# List current directory
ls

# Remove empty directory
rmdir old_temp

# Try to remove non-empty directory
rmdir projects
# Output: rmdir: failed to remove 'projects': Directory not empty

# Remove non-empty directory (use carefully!)
rm -r old_projects

# Verify removal
ls
```

---

## Summary

### Quick Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `ls` | List directory contents | `ls -la` |
| `cd` | Change directory | `cd /home/user` |
| `pwd` | Show current directory | `pwd` |
| `mkdir` | Create directory | `mkdir -p dir/subdir` |
| `rmdir` | Remove empty directory | `rmdir temp` |

### Key Takeaways

1. **`ls`** - Your eyes in the command line, shows what's in directories
2. **`cd`** - Your legs, moves you around the filesystem
3. **`pwd`** - Your GPS, tells you where you are
4. **`mkdir`** - Your builder, creates new directories
5. **`rmdir`** - Your cleanup tool, removes empty directories


<br>



**Happy Learning! 🚀**

*Contributions and suggestions are welcome!*

---

**Maintained by: [Sablu Chaudhary](https://github.com/sabluchaudhary555)** 🔗 **Connect with me:** [LinkedIn](https://www.linkedin.com/in/sablu-chaudhary555/) | [GitHub](https://github.com/sabluchaudhary555)

---
**Made with ❤️ for the Open Source Community**