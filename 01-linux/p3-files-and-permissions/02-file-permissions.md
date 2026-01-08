# File Permissions Guide

## The Basics

Every file and directory in Linux has permissions for three groups:
- **Owner** - the user who owns the file
- **Group** - users in the file's group  
- **Others** - everyone else

## Permission Types (rwx)

| Symbol | Permission | What it does |
|--------|------------|--------------|
| `r` | Read | View contents |
| `w` | Write | Modify/delete |
| `x` | Execute | Run file or access directory |
| `-` | None | No permission |

## Reading Permissions
```bash
ls -l myfile.txt
-rw-r--r-- 1 user group 1234 Jan 1 12:00 myfile.txt
 │││ │││ │││
 │││ │││ └── Others: read only
 │││ └────── Group: read only
 └────────── Owner: read & write
```

## Octal Notation

Each permission has a numeric value:
- **r** = 4
- **w** = 2  
- **x** = 1

Add them up for each group:
```
rwx = 4+2+1 = 7
rw- = 4+2+0 = 6
r-x = 4+0+1 = 5
r-- = 4+0+0 = 4
--- = 0+0+0 = 0
```

## Common Examples

**755** → `rwxr-xr-x`
```
Owner: 7 (rwx) - full control
Group: 5 (r-x) - read and execute
Others: 5 (r-x) - read and execute
```
Use for: Scripts, executables, directories

**644** → `rw-r--r--`
```
Owner: 6 (rw-) - read and write
Group: 4 (r--) - read only
Others: 4 (r--) - read only
```
Use for: Text files, documents, configs

## Changing Permissions
```bash
chmod 755 script.sh    # Using octal
chmod u+x script.sh    # Add execute for owner
chmod go-w file.txt    # Remove write for group and others
```

---


**Happy Learning! 🚀**

*Contributions and suggestions are welcome!*

---

**Maintained by: [Sablu Chaudhary](https://github.com/sabluchaudhary555)** 🔗 **Connect with me:** [LinkedIn](https://www.linkedin.com/in/sablu-chaudhary555/) | [GitHub](https://github.com/sabluchaudhary555)

---
**Made with ❤️ for the Open Source Community**
