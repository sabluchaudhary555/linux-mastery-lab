# Linux Ownership and Links

## Table of Contents
- [File Ownership](#file-ownership)
- [File Links](#file-links)
  - [Soft Links (Symbolic Links)](#soft-links-symbolic-links)
  - [Hard Links](#hard-links)
  - [Key Differences](#key-differences)
- [Sources](#sources)

---

## File Ownership

Every file and directory in Linux has an owner (user) and a group associated with it.

**View Ownership:**
```bash
ls -l file.txt
# Output: -rw-r--r-- 1 user group 1234 Jan 01 12:00 file.txt
```

**Change Owner:**
```bash
chown newuser file.txt
```

**Change Group:**
```bash
chown :newgroup file.txt
```

**Change Both:**
```bash
chown newuser:newgroup file.txt
```

**Recursive Change:**
```bash
chown -R user:group directory/
```

---

## File Links

### Soft Links (Symbolic Links)

A symbolic link is a special file that points to another file or directory by path.

**Create:**
```bash
ln -s target_file link_name
```

**Properties:**
- Points to file path
- Can cross filesystems
- Can link directories
- Breaks if target is deleted
- Shows with `l` in `ls -l`

**Example:**
```bash
ln -s /home/user/docs/report.txt report_link
```

### Hard Links

A hard link is an additional name for an existing file on the same filesystem.

**Create:**
```bash
ln target_file link_name
```

**Properties:**
- Points to same inode
- Cannot cross filesystems
- Cannot link directories
- Data persists until all links deleted
- Indistinguishable from original

**Example:**
```bash
ln original.txt backup.txt
```

### Key Differences

| Feature | Soft Link | Hard Link |
|---------|-----------|-----------|
| **Inode** | Different | Same |
| **Cross filesystem** | ✓ | ✗ |
| **Link directories** | ✓ | ✗ |
| **Target deleted** | Breaks | Still works |
| **Command** | `ln -s` | `ln` |

**Check Links:**
```bash
ls -li          # View inode numbers
readlink link   # Show soft link target
```

---

## Sources

- Linux Manual Pages (`man chown`, `man ln`)
- [GNU Coreutils Documentation](https://www.gnu.org/software/coreutils/manual/)
- [The Linux Documentation Project](https://tldp.org/)
- [Linux File System Documentation](https://www.kernel.org/doc/html/latest/filesystems/)

---

**Happy Learning! 🚀**

*Contributions and suggestions are welcome!*

---

**Maintained by: [Sablu Chaudhary](https://github.com/sabluchaudhary555)** 🔗 **Connect with me:** [LinkedIn](https://www.linkedin.com/in/sablu-chaudhary555/) | [GitHub](https://github.com/sabluchaudhary555)

---
**Made with ❤️ for the Open Source Community**