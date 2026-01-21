# LinkManager - Hard & Soft Link Explorer

A Python tool for exploring, analyzing, and managing hard links and symbolic links (symlinks) in your filesystem.

## Overview

LinkManager helps you understand and navigate the complex world of filesystem links. It can identify file types, find all hard links pointing to the same inode, detect broken symlinks, and display detailed file information.

## Features

- **Directory Listing** - Browse directories with visual file type indicators
- **File Details** - Show comprehensive information about files and links
- **Hard Link Discovery** - Find all hard links sharing the same inode
- **Broken Symlink Detection** - Scan directories for broken symbolic links
- **Interactive Menu** - Easy-to-use command-line interface
- **Visual Icons** - Color-coded emojis for different file types

## Installation

1. Save the script as `link-manager.py`
2. Make it executable:
```bash
chmod +x link-manager.py
```

## Usage

Run the interactive menu:
```bash
python3 link-manager.py
```

Or directly execute:
```bash
./link-manager.py
```

### Menu Options

**1. List Directory** - Browse directory contents with file type icons
- Shows first 20 items with type indicators
- Identifies symlinks, hard links, and regular files

**2. Show File Details** - Display comprehensive file information
- File type and inode number
- Hard link count
- File size and permissions
- For symlinks: target path and resolution status

**3. Find Hard Links** - Locate all hard links to a file
- Searches from file's directory (or specify custom root)
- Shows all paths pointing to the same inode
- Displays total link count

**4. Find Broken Symlinks** - Scan for broken symbolic links
- Recursively searches directory tree
- Lists all symlinks with missing targets
- Shows both link path and intended target

**5. Exit** - Close the program

## Understanding Links

### Hard Links
- Multiple directory entries pointing to the same inode
- Share the same data on disk
- Deleting one doesn't affect others
- Cannot span filesystems
- Icon: 🔵

### Symbolic Links (Symlinks)
- Pointer files containing path to target
- Can point to files or directories
- Can span filesystems
- Can become "broken" if target is deleted
- Icon: 🔗 (working) or ❌ (broken)

### Regular Files
- Standard files with single directory entry
- Icon: 📄

### Directories
- Folders containing other files
- Icon: 📁

## Example Usage

### Finding Hard Links
```
Enter file path: /home/user/document.txt
🔍 Searching for hard links (Inode: 12345, Total links: 3)
1. /home/user/document.txt
2. /home/user/backup/doc.txt
3. /var/backup/document.txt
```

### Detecting Broken Symlinks
```
❌ Scanning for broken symlinks in: /home/user
1. /home/user/old-config
   → /etc/old-app/config (missing)
Total broken: 1
```

## Requirements

- **OS:** Linux, macOS, or any Unix-like system
- **Python:** 3.6 or higher
- **Dependencies:** Standard library only (os, stat modules)

## File Information Displayed

For regular files and hard links:
- Inode number
- Number of hard links
- File size in bytes
- Permissions (octal format)
- Owner UID and Group GID

For symbolic links:
- Link target path
- Resolved absolute path (if valid)
- Broken status indicator
- Link size

## Use Cases

- **System Cleanup** - Find and remove broken symlinks
- **Backup Verification** - Ensure hard links are properly maintained
- **Disk Space Analysis** - Identify files with multiple hard links
- **Link Auditing** - Verify symbolic link integrity
- **File System Navigation** - Understand file relationships

## Tips

1. Run with sudo for full system access:
```bash
sudo python3 link-manager.py
```

2. For faster hard link search, specify a smaller search root

3. Regular backups help prevent broken symlinks

## Troubleshooting

**"Permission denied"** - Run with sudo or check file permissions

**"Path not found"** - Verify the path exists and is typed correctly

**Slow hard link search** - Large directory trees take time; consider narrowing search scope

## Technical Notes

- Uses `os.stat()` for file information
- Uses `os.lstat()` for symlink information (doesn't follow link)
- Inode comparison for hard link detection
- Recursive directory walking for broken link scanning

## License

Developed by SSoft.in

---

*Master your filesystem links with confidence!*