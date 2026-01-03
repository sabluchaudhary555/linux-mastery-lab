# Searching & Filtering in Linux

A comprehensive guide to `grep`, `find`, and `locate` commands for efficient file searching and text filtering.

---

## 1. grep - Search Text Patterns

`grep` searches for patterns in files or input streams.

### Basic Syntax
```bash
grep [options] pattern [file...]
```

### Common Options
- `-i` - Ignore case
- `-r` or `-R` - Recursive search
- `-v` - Invert match (show non-matching lines)
- `-n` - Show line numbers
- `-c` - Count matches
- `-l` - List filenames only
- `-w` - Match whole words
- `-A n` - Show n lines after match
- `-B n` - Show n lines before match
- `-C n` - Show n lines around match

### Examples

**Basic search:**
```bash
grep "error" logfile.txt
```

**Case-insensitive search:**
```bash
grep -i "warning" app.log
```

**Recursive search in directory:**
```bash
grep -r "TODO" ./src/
```

**Show line numbers:**
```bash
grep -n "function" script.js
```

**Count occurrences:**
```bash
grep -c "success" results.txt
```

**Invert match (exclude pattern):**
```bash
grep -v "debug" app.log
```

**Multiple patterns (OR):**
```bash
grep -E "error|warning|critical" system.log
```

**Whole word match:**
```bash
grep -w "test" file.txt  # matches "test" but not "testing"
```

**Context lines:**
```bash
grep -C 2 "exception" error.log  # 2 lines before and after
```

### Regular Expressions
```bash
grep "^Error" log.txt        # Lines starting with "Error"
grep "failed$" log.txt       # Lines ending with "failed"
grep "user[0-9]" data.txt    # user followed by a digit
grep "colou?r" text.txt      # Match "color" or "colour"
```

---

## 2. find - Search Files and Directories

`find` searches for files and directories based on various criteria.

### Basic Syntax
```bash
find [path] [options] [expression]
```

### Common Options

#### By Name
```bash
find /path -name "filename"           # Exact name
find /path -iname "filename"          # Case-insensitive
find /path -name "*.txt"              # Pattern matching
```

#### By Type
```bash
find /path -type f                    # Files only
find /path -type d                    # Directories only
find /path -type l                    # Symbolic links
```

#### By Size
```bash
find /path -size +100M                # Larger than 100MB
find /path -size -10k                 # Smaller than 10KB
find /path -size 50M                  # Exactly 50MB
```

#### By Time
```bash
find /path -mtime -7                  # Modified in last 7 days
find /path -mtime +30                 # Modified more than 30 days ago
find /path -atime -1                  # Accessed in last 24 hours
find /path -ctime 0                   # Changed today
```

#### By Permissions
```bash
find /path -perm 644                  # Exact permissions
find /path -perm -644                 # At least these permissions
find /path -perm /u+w                 # User writable
```

### Examples

**Find all JavaScript files:**
```bash
find . -name "*.js"
```

**Find files modified in last 24 hours:**
```bash
find /var/log -type f -mtime -1
```

**Find large files (>500MB):**
```bash
find /home -type f -size +500M
```

**Find and delete temp files:**
```bash
find /tmp -name "*.tmp" -delete
```

**Find empty files:**
```bash
find . -type f -empty
```

**Find with multiple conditions (AND):**
```bash
find . -name "*.log" -size +10M
```

**Find with OR conditions:**
```bash
find . -name "*.txt" -o -name "*.md"
```

**Execute command on results:**
```bash
find . -name "*.txt" -exec grep "error" {} \;
find . -type f -name "*.jpg" -exec cp {} /backup/ \;
```

**Find by user:**
```bash
find /home -user john
```

**Find files with specific permissions:**
```bash
find . -type f -perm 0777
```

**Exclude directories:**
```bash
find . -name "*.py" -not -path "*/venv/*"
```

---

## 3. locate - Fast File Search

`locate` uses a pre-built database for fast file searching.

### Basic Syntax
```bash
locate [options] pattern
```

### Common Options
- `-i` - Ignore case
- `-c` - Count matches
- `-n N` - Limit results to N
- `-b` - Match only basename
- `-r` - Use regex

### Examples

**Basic search:**
```bash
locate nginx.conf
```

**Case-insensitive:**
```bash
locate -i README.md
```

**Count results:**
```bash
locate -c "*.pdf"
```

**Limit results:**
```bash
locate -n 10 python
```

**Basename only:**
```bash
locate -b '\config.json'
```

**Using regex:**
```bash
locate -r "\.log$"
```

### Update Database
```bash
sudo updatedb                         # Update locate database
```

**Note:** `locate` is fast but relies on a database that may be outdated. Use `find` for real-time searches.

---

## Combined Usage Examples

**Find files and search content:**
```bash
find . -name "*.py" -exec grep -l "import flask" {} \;
```

**Search logs excluding archived:**
```bash
find /var/log -name "*.log" -not -name "*old*" -exec grep -i "error" {} \;
```

**List files modified today with specific extension:**
```bash
find . -name "*.txt" -mtime 0 -ls
```

**Locate and verify existence:**
```bash
locate myfile.txt | xargs ls -lh
```

---

## Quick Reference Table

| Task | Command |
|------|---------|
| Search text in file | `grep "pattern" file.txt` |
| Search recursively | `grep -r "pattern" dir/` |
| Find file by name | `find . -name "file.txt"` |
| Find files by extension | `find . -name "*.log"` |
| Find large files | `find . -size +100M` |
| Find recent files | `find . -mtime -7` |
| Quick file search | `locate filename` |
| Update locate database | `sudo updatedb` |

---

## Performance Tips

1. **Use `locate` for quick searches** when exact real-time accuracy isn't critical
2. **Use `find` for precise searches** with specific criteria
3. **Use `grep` with `-l`** when you only need filenames, not content
4. **Combine tools** with pipes for powerful workflows
5. **Limit search scope** to specific directories to improve performance

---

## Common Pitfalls

- `locate` database can be outdated - run `updatedb` regularly
- `grep` without `-r` won't search subdirectories
- `find` without path defaults to current directory
- Forgetting to quote patterns with special characters
- Using `find -delete` without testing the search first (always test with `-print` first!)

---

*Pro Tip: Always test destructive operations (like `-delete` or `-exec rm`) with `-print` first to verify results!*




<br>



**Happy Learning! 🚀**

*Contributions and suggestions are welcome!*

---

**Maintained by: [Sablu Chaudhary](https://github.com/sabluchaudhary555)** 🔗 **Connect with me:** [LinkedIn](https://www.linkedin.com/in/sablu-chaudhary555/) | [GitHub](https://github.com/sabluchaudhary555)

---
**Made with ❤️ for the Open Source Community**