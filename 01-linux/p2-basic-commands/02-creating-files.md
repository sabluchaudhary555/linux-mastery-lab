# File Operations

## Table of Contents
- [Overview](#overview)
- [cp - Copy Files and Directories](#cp---copy-files-and-directories)
- [mv - Move and Rename Files](#mv---move-and-rename-files)
- [rm - Remove Files and Directories](#rm---remove-files-and-directories)
- [touch - Create and Update Files](#touch---create-and-update-files)
- [Practical Examples](#practical-examples)
- [Summary](#summary)

---

## Overview

This guide covers the essential file operation commands in Linux. These commands allow you to copy, move, rename, delete, and create files, forming the core of file management in the command-line environment.

**Important**: Always double-check file paths and use these commands carefully, especially `rm`, as deleted files cannot be easily recovered.

---

## cp - Copy Files and Directories

The `cp` command copies files and directories from one location to another.

### Syntax
```bash
cp [OPTIONS] SOURCE DESTINATION
```

### Common Options

| Option | Description |
|--------|-------------|
| `cp file1 file2` | Copy file1 to file2 |
| `cp -r dir1 dir2` | Copy directory recursively |
| `cp -i file1 file2` | Interactive mode (prompt before overwrite) |
| `cp -v file1 file2` | Verbose mode (show files being copied) |
| `cp -u file1 file2` | Update mode (copy only if source is newer) |
| `cp -p file1 file2` | Preserve file attributes (permissions, timestamps) |
| `cp -a dir1 dir2` | Archive mode (recursive + preserve attributes) |

### Examples

#### Copying Files

```bash
# Copy a single file
cp document.txt backup.txt

# Copy file to another directory
cp report.pdf /home/user/Documents/

# Copy with interactive mode (asks before overwriting)
cp -i data.txt backup/data.txt

# Copy with verbose output
cp -v file1.txt file2.txt
# Output: 'file1.txt' -> 'file2.txt'

# Copy and preserve attributes
cp -p original.txt copy.txt
```

#### Copying Directories

```bash
# Copy directory recursively
cp -r projects/ backup_projects/

# Copy directory with all attributes preserved
cp -a website/ website_backup/

# Copy multiple files to a directory
cp file1.txt file2.txt file3.txt /destination/folder/

# Copy with wildcards
cp *.txt backup/
cp *.jpg images/backup/
```

#### Advanced Copying

```bash
# Copy only if source is newer
cp -u newfile.txt backup/

# Copy with structure preservation
cp -r --parents src/code/file.py /backup/
# Creates /backup/src/code/file.py

# Copy with verbose and interactive
cp -vi important.doc backup/

# Copy specific file types
cp *.{jpg,png,gif} images_backup/
```

### Important Notes

- **Without `-r`**: Cannot copy directories
- **Overwriting**: By default, `cp` overwrites existing files without warning
- **Use `-i`**: For safety, use interactive mode to prevent accidental overwrites
- **Use `-a`**: For complete directory backups with all attributes

---

## mv - Move and Rename Files

The `mv` command moves or renames files and directories. Unlike `cp`, it doesn't create a copy - it relocates the original.

### Syntax
```bash
mv [OPTIONS] SOURCE DESTINATION
```

### Common Options

| Option | Description |
|--------|-------------|
| `mv file1 file2` | Rename file1 to file2 |
| `mv file dir/` | Move file to directory |
| `mv -i file1 file2` | Interactive mode (prompt before overwrite) |
| `mv -v file1 file2` | Verbose mode (show files being moved) |
| `mv -u file1 file2` | Update mode (move only if source is newer) |
| `mv -n file1 file2` | No-clobber mode (don't overwrite existing files) |

### Examples

#### Renaming Files and Directories

```bash
# Rename a file
mv oldname.txt newname.txt

# Rename a directory
mv old_folder new_folder

# Rename with verbose output
mv -v report_v1.pdf report_v2.pdf
# Output: renamed 'report_v1.pdf' -> 'report_v2.pdf'

# Rename multiple files (requires additional tools)
# Use rename command or loops for batch renaming
```

#### Moving Files

```bash
# Move file to another directory
mv document.txt /home/user/Documents/

# Move multiple files to a directory
mv file1.txt file2.txt file3.txt /destination/

# Move with interactive confirmation
mv -i important.doc archive/

# Move all text files
mv *.txt text_files/

# Move with verbose output
mv -v data.csv /backup/
```

#### Moving Directories

```bash
# Move directory and its contents
mv projects/ /home/user/archive/

# Move and rename directory
mv old_project/ /home/user/new_project/

# Move multiple directories
mv dir1/ dir2/ dir3/ /destination/
```

#### Advanced Operations

```bash
# Move only if destination doesn't exist
mv -n file.txt backup/

# Move only if source is newer
mv -u data.txt backup/

# Move with backup of existing file
mv -b file.txt destination/
# Creates destination/file.txt~ as backup

# Safe move with interactive and verbose
mv -iv important_file.doc archive/
```

### Important Notes

- **Renaming vs Moving**: Same command, different outcome based on destination
- **No Undo**: Files are moved, not copied - be careful!
- **Cross-filesystem**: Moving between different partitions actually copies then deletes
- **Directories**: Can be moved without `-r` flag (unlike `cp`)

---

## rm - Remove Files and Directories

The `rm` command permanently deletes files and directories. **Use with extreme caution** - deleted files are not sent to a trash bin.

### Syntax
```bash
rm [OPTIONS] FILE/DIRECTORY
```

### Common Options

| Option | Description |
|--------|-------------|
| `rm file` | Remove a file |
| `rm -r dir/` | Remove directory recursively |
| `rm -i file` | Interactive mode (prompt before each deletion) |
| `rm -f file` | Force removal (no prompts, ignore nonexistent files) |
| `rm -v file` | Verbose mode (show files being removed) |
| `rm -rf dir/` | Force remove directory recursively (DANGEROUS!) |
| `rm -I files` | Prompt once before removing more than 3 files |

### Examples

#### Removing Files

```bash
# Remove a single file
rm unwanted.txt

# Remove with confirmation
rm -i important.txt
# Prompt: rm: remove regular file 'important.txt'? y

# Remove multiple files
rm file1.txt file2.txt file3.txt

# Remove with verbose output
rm -v oldfile.txt
# Output: removed 'oldfile.txt'

# Remove all text files
rm *.txt

# Remove specific file types
rm *.log *.tmp
```

#### Removing Directories

```bash
# Remove empty directory (alternative to rmdir)
rm -d empty_folder/

# Remove directory and contents recursively
rm -r old_project/

# Remove with confirmation for each file
rm -ri project/

# Force remove directory (NO CONFIRMATION - DANGEROUS!)
rm -rf temp_folder/

# Remove with verbose output
rm -rv old_directory/
```

#### Safe Deletion Practices

```bash
# Interactive mode for safety
rm -i important_file.txt

# Prompt once for multiple files
rm -I *.txt

# Verbose + interactive
rm -iv file1.txt file2.txt

# List files before removing (using ls first)
ls *.log
rm *.log
```

#### Common Patterns

```bash
# Remove backup files
rm *~ 
rm *.bak

# Remove hidden files
rm .*.swp

# Remove files older than 30 days (using find)
find . -name "*.log" -mtime +30 -exec rm {} \;

# Remove empty files
find . -type f -empty -delete
```

### Critical Warnings

⚠️ **DANGEROUS COMMANDS - NEVER USE WITHOUT THINKING:**

```bash
# These can destroy your entire system!
rm -rf /          # Deletes everything (root directory)
rm -rf /*         # Deletes all top-level directories
rm -rf ~/*        # Deletes all files in home directory
```

### Safety Best Practices

1. **Always use `-i` flag** when removing important files
2. **Never use `rm -rf /`** or variations without absolute certainty
3. **List files first** using `ls` before removing with wildcards
4. **Use backups** before mass deletions
5. **Consider moving to trash** instead of permanent deletion:
   ```bash
   # Create a trash directory
   mkdir -p ~/.trash
   
   # Move instead of delete
   mv unwanted_file.txt ~/.trash/
   ```

---

## touch - Create and Update Files

The `touch` command creates empty files or updates timestamps of existing files.

### Syntax
```bash
touch [OPTIONS] FILE
```

### Common Options

| Option | Description |
|--------|-------------|
| `touch file` | Create empty file or update timestamp |
| `touch -a file` | Update only access time |
| `touch -m file` | Update only modification time |
| `touch -c file` | Don't create file if it doesn't exist |
| `touch -t TIMESTAMP file` | Set specific timestamp |
| `touch -r ref_file file` | Use timestamp from reference file |
| `touch -d "date string" file` | Set timestamp using date string |

### Examples

#### Creating Files

```bash
# Create a single empty file
touch newfile.txt

# Create multiple files
touch file1.txt file2.txt file3.txt

# Create files with specific extension
touch index.html style.css script.js

# Create numbered files
touch file{1..10}.txt
# Creates: file1.txt, file2.txt, ..., file10.txt

# Create nested structure files
touch project/{src,docs,tests}/README.md
```

#### Updating Timestamps

```bash
# Update timestamp of existing file
touch existing_file.txt

# Update only access time
touch -a document.pdf

# Update only modification time
touch -m report.txt

# Don't create if file doesn't exist
touch -c maybe_exists.txt
```

#### Advanced Timestamp Operations

```bash
# Set specific date and time
touch -t 202401011200 file.txt
# Format: YYYYMMDDhhmm

# Use date string
touch -d "2024-01-01 12:00:00" file.txt
touch -d "yesterday" file.txt
touch -d "2 days ago" file.txt

# Copy timestamp from another file
touch -r reference.txt target.txt

# Set both access and modification time
touch -d "2024-01-15" file.txt
```

#### Practical Uses

```bash
# Create placeholder files
touch TODO.md CHANGELOG.md

# Create log file
touch /var/log/myapp.log

# Mark files as recently modified (for build systems)
touch src/*.c

# Create test files
touch test_{1..5}.txt

# Create hidden configuration file
touch .config
```

### Use Cases

1. **Creating empty files** for later editing
2. **Updating timestamps** to trigger build systems
3. **Creating placeholders** in project structures
4. **Testing file operations** with dummy files
5. **Marking files** for backup systems that check modification time

---

## Practical Examples

### Example 1: Project Backup

```bash
# Create backup directory
mkdir -p ~/backups/myproject

# Copy project with archive mode
cp -a ~/projects/myproject ~/backups/myproject_backup

# Verify backup
ls -lh ~/backups/

# Alternative: Move old version
mv ~/projects/old_version ~/archive/
```

### Example 2: File Organization

```bash
# Create directory structure
mkdir -p ~/Documents/{Work,Personal,Archive}

# Move files to appropriate folders
mv *.pdf ~/Documents/Work/
mv *.jpg ~/Documents/Personal/
mv old_*.* ~/Documents/Archive/

# Copy important files to backup
cp -v important_*.doc ~/backup/
```

### Example 3: Safe File Deletion

```bash
# List files to be deleted
ls *.tmp

# Remove with confirmation
rm -i *.tmp

# Or remove all at once with one confirmation
rm -I *.tmp

# Remove old logs verbosely
rm -v old_*.log
```

### Example 4: Batch File Creation

```bash
# Create project structure
mkdir -p webapp/{src,public,config}

# Create empty files
touch webapp/src/{index.js,app.js,utils.js}
touch webapp/public/{index.html,style.css}
touch webapp/config/settings.json

# Verify structure
ls -R webapp/
```

### Example 5: File Renaming Workflow

```bash
# Rename with descriptive name
mv report.pdf project_report_2024.pdf

# Move to organized location
mv project_report_2024.pdf ~/Documents/Reports/

# Create backup copy
cp ~/Documents/Reports/project_report_2024.pdf ~/backup/

# Verify
ls -lh ~/Documents/Reports/
ls -lh ~/backup/
```

---

## Summary

### Quick Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `cp` | Copy files/directories | `cp -r src/ backup/` |
| `mv` | Move/rename files | `mv old.txt new.txt` |
| `rm` | Remove files/directories | `rm -i file.txt` |
| `touch` | Create/update files | `touch newfile.txt` |

### Key Takeaways

1. **`cp`** - Creates duplicates, use `-r` for directories, use `-i` for safety
2. **`mv`** - Relocates or renames, no `-r` needed, irreversible action
3. **`rm`** - Permanently deletes, extremely dangerous with `-rf`, always use `-i` for important files
4. **`touch`** - Creates empty files, updates timestamps, useful for placeholders


<br>



**Happy Learning! 🚀**

*Contributions and suggestions are welcome!*

---

**Maintained by: [Sablu Chaudhary](https://github.com/sabluchaudhary555)** 🔗 **Connect with me:** [LinkedIn](https://www.linkedin.com/in/sablu-chaudhary555/) | [GitHub](https://github.com/sabluchaudhary555)

---
**Made with ❤️ for the Open Source Community**