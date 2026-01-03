# Standard I/O: Redirection & Pipes

A concise guide to input/output redirection and pipes in Linux.

---

## Understanding Standard Streams

| Stream | Name | Descriptor | Default |
|--------|------|------------|---------|
| stdin | Standard Input | 0 | Keyboard |
| stdout | Standard Output | 1 | Terminal |
| stderr | Standard Error | 2 | Terminal |

---

## 1. Output Redirection

### `>` - Redirect Output (Overwrite)

Writes command output to a file, **overwriting** existing content.

```bash
# Save output to file
echo "Hello World" > output.txt

# Save command result
ls -la > directory_list.txt

# Overwrite file with new content
date > timestamp.txt
```

### `>>` - Redirect Output (Append)

Writes command output to a file, **appending** to existing content.

```bash
# Append to existing file
echo "New line" >> log.txt

# Add multiple entries
date >> activity.log
echo "User logged in" >> activity.log

# Append command output
ls -l *.txt >> file_list.txt
```

### Redirect stderr (`2>`)

Redirect error messages separately from standard output.

```bash
# Redirect errors to file
command 2> errors.txt

# Redirect errors to null (discard)
command 2> /dev/null

# Example: only save errors
ls /nonexistent 2> error.log
```

### Redirect Both stdout and stderr

```bash
# Redirect both to same file
command > output.txt 2>&1

# Modern syntax (Bash 4+)
command &> output.txt

# Append both
command >> output.txt 2>&1

# Separate files for output and errors
command > output.log 2> error.log
```

### Discard Output

```bash
# Discard stdout
command > /dev/null

# Discard stderr
command 2> /dev/null

# Discard everything
command &> /dev/null
```

---

## 2. Input Redirection

### `<` - Redirect Input

Feed file content as input to a command.

```bash
# Send file content to command
wc -l < file.txt

# Sort file content
sort < unsorted.txt > sorted.txt

# Mail content from file
mail -s "Subject" user@example.com < message.txt
```

### `<<` - Here Document

Provide multi-line input directly in script or command.

```bash
# Multi-line input
cat << EOF > config.txt
setting1=value1
setting2=value2
setting3=value3
EOF

# SQL commands
mysql -u user -p database << SQL
SELECT * FROM users;
UPDATE settings SET value='new';
SQL
```

### `<<<` - Here String

Pass a string as input.

```bash
# Single line input
grep "pattern" <<< "text to search"

# With variable
name="John"
cat <<< "Hello, $name"
```

---

## 3. Pipes (`|`)

Connect output of one command to input of another.

### Basic Piping

```bash
# List and count files
ls -l | wc -l

# Search in command output
ps aux | grep python

# Sort and display unique values
cat names.txt | sort | uniq
```

### Multiple Pipes

```bash
# Chain multiple commands
cat access.log | grep "ERROR" | wc -l

# Complex processing
ps aux | grep -v grep | grep python | awk '{print $2}'

# Search, sort, and paginate
cat file.txt | grep "pattern" | sort | less
```

### Common Pipe Patterns

```bash
# Count occurrences
cat file.txt | sort | uniq -c

# Filter and format
ls -l | grep "\.txt" | awk '{print $9}'

# Process logs
tail -f app.log | grep "ERROR"

# Top memory consumers
ps aux | sort -k4 -rn | head -10

# Disk usage sorted
du -h | sort -hr | head -20
```

---

## 4. Combining Redirection and Pipes

```bash
# Pipe and redirect output
ls -la | grep "txt" > text_files.txt

# Process and save errors
cat file.txt | grep "pattern" 2> errors.log > results.txt

# Multiple operations
cat data.txt | sort | uniq > unique_data.txt 2> sort_errors.log

# Pipe, process, and append
ps aux | grep python | awk '{print $2}' >> process_ids.txt
```

---

## 5. Advanced Redirection

### Tee Command

Write output to both file and stdout.

```bash
# Save and display
ls -la | tee output.txt

# Append mode
echo "Log entry" | tee -a log.txt

# Multiple files
echo "Data" | tee file1.txt file2.txt file3.txt

# With pipeline
cat data.txt | grep "pattern" | tee results.txt | wc -l
```

### File Descriptor Manipulation

```bash
# Save stdout to fd 3, redirect to file
exec 3>&1 > output.txt
echo "This goes to file"
exec 1>&3 3>&-  # Restore stdout

# Swap stdout and stderr
command 3>&1 1>&2 2>&3
```

---

## Practical Examples

### Logging

```bash
# Simple logging
echo "[$(date)] Starting process" >> app.log

# Command with timestamp
./script.sh 2>&1 | while read line; do echo "$(date): $line"; done >> app.log

# Separate success and error logs
./deploy.sh > success.log 2> error.log
```

### Data Processing

```bash
# Extract, process, save
cat data.csv | cut -d',' -f2 | sort | uniq > unique_values.txt

# Filter and count
grep "ERROR" app.log | wc -l > error_count.txt

# Complex pipeline
cat access.log | awk '{print $1}' | sort | uniq -c | sort -rn > ip_frequency.txt
```

### System Monitoring

```bash
# Monitor and log
top -b -n 1 | head -20 > system_snapshot.txt

# Continuous monitoring
tail -f /var/log/syslog | grep "error" >> filtered_errors.log

# Process watching
ps aux | grep apache | tee processes.txt
```

### Backup and Archive

```bash
# Backup with timestamp
tar -czf - /data | tee backup_$(date +%Y%m%d).tar.gz > /dev/null

# Database dump
mysqldump database | gzip > backup.sql.gz 2> dump_errors.log
```

---

## Quick Reference

| Operation | Syntax | Description |
|-----------|--------|-------------|
| Overwrite file | `cmd > file` | Redirect stdout, overwrite |
| Append to file | `cmd >> file` | Redirect stdout, append |
| Redirect errors | `cmd 2> file` | Redirect stderr |
| Redirect both | `cmd &> file` | Redirect stdout & stderr |
| Discard output | `cmd > /dev/null` | Discard stdout |
| Input from file | `cmd < file` | Use file as input |
| Pipe commands | `cmd1 | cmd2` | Output of cmd1 → input of cmd2 |
| Tee output | `cmd | tee file` | Write to file and stdout |
| Here document | `cmd << EOF` | Multi-line input |
| Here string | `cmd <<< "text"` | Single string input |

---

## Common Pitfalls

⚠️ **`>` vs `>>`**: Using `>` will **overwrite** the file completely!
```bash
# DANGER: This erases file.txt first!
echo "new content" > file.txt

# SAFE: This adds to existing content
echo "new content" >> file.txt
```

⚠️ **Stderr not captured**: By default, `>` only redirects stdout
```bash
# This won't capture errors
command > output.txt

# This captures errors too
command &> output.txt
```

⚠️ **Pipe failures**: Later commands in pipe can fail silently
```bash
# Use pipefail to catch errors
set -o pipefail
command1 | command2 | command3
```

---

## Best Practices

1. **Always test with `> /tmp/test.txt`** before overwriting important files
2. **Use `>>` for logs** to preserve history
3. **Capture errors separately** for debugging: `2> error.log`
4. **Use `tee` when you need to see output** while saving it
5. **Combine with `set -e` and `set -o pipefail`** in scripts for better error handling

---

*Pro Tip: Use `command 2>&1 | tee output.log` to see and save both output and errors in real-time!*


<br>



**Happy Learning! 🚀**

*Contributions and suggestions are welcome!*

---

**Maintained by: [Sablu Chaudhary](https://github.com/sabluchaudhary555)** 🔗 **Connect with me:** [LinkedIn](https://www.linkedin.com/in/sablu-chaudhary555/) | [GitHub](https://github.com/sabluchaudhary555)

---
**Made with ❤️ for the Open Source Community**