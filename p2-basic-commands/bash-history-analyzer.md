# Bash Command History Analyzer

A Python tool that analyzes your `.bash_history` file to reveal usage patterns, command statistics, and personalized efficiency tips.

## Overview

This analyzer examines your bash command history to help you understand your command-line habits, identify repetitive patterns, and improve your terminal efficiency with actionable suggestions.

## Features

- **Usage Statistics** - Total commands, unique commands, and file metrics
- **Top Commands** - Visual ranking of your most-used commands with percentages
- **Command Categories** - Breakdown by type (navigation, file ops, git, network, etc.)
- **Pattern Detection** - Identifies pipes, redirections, and command sequences
- **Efficiency Analysis** - Personalized tips based on your usage patterns
- **Interesting Finds** - Longest commands, common sequences, and quirks
- **Export Report** - Save analysis to a text file for reference

## Installation

1. Save the script as `bash-history-analyzer.py`
2. Make it executable:
```bash
chmod +x bash-history-analyzer.py
```

## Usage

Simply run the script:
```bash
./bash-history-analyzer.py
```

Or with Python:
```bash
python3 bash-history-analyzer.py
```

The tool automatically reads from `~/.bash-history` and generates a comprehensive analysis.

## What It Analyzes

### Command Categories
- **Navigation** - cd, ls, pwd
- **File Operations** - cp, mv, rm, mkdir
- **Viewing** - cat, less, vim, nano
- **Searching** - grep, find, awk, sed
- **System** - ps, top, systemctl, sudo
- **Network** - ping, curl, wget, ssh
- **Package Management** - apt, pip, npm
- **Git** - All git commands
- **Compression** - tar, zip, gzip
- **Permissions** - chmod, chown

### Patterns Detected
- Commands with pipes (`|`)
- Output/input redirection (`>`, `<`, `>>`)
- Sudo usage frequency
- Long complex commands
- Common command sequences (e.g., cd → ls)

### Efficiency Suggestions
The tool provides personalized tips such as:
- Creating aliases for frequently used directories
- Using functions for repetitive command sequences
- Better tools for specific tasks (less vs cat)
- Keyboard shortcuts like Ctrl+R for history search

## Output

The analyzer generates:

1. **Terminal Display** - Colorized, formatted analysis with charts
2. **Text Report** - `bash-history-report.txt` with top 20 commands

## Example Output

```
📊 BASIC STATISTICS
  Total Commands in History: 1,523
  Unique Commands Used: 87
  
🏆 TOP 15 MOST USED COMMANDS
  Rank   Command              Count      Percentage   Bar
  1      git                  245        16.09%       ████████
  2      cd                   198        13.00%       ██████
  3      ls                   156        10.24%       █████
```

## Requirements

- **OS:** Linux, macOS, or any Unix-like system with bash
- **Python:** 3.6 or higher
- **Dependencies:** Standard library only (no external packages)
- **History File:** `~/.bash_history` must exist

## Tips for Better Analysis

1. **Increase history size** - Add to `~/.bashrc`:
```bash
HISTSIZE=10000
HISTFILESIZE=20000
```

2. **Enable timestamp in history**:
```bash
export HISTTIMEFORMAT="%F %T "
```

3. **Save history immediately**:
```bash
PROMPT_COMMAND="history -a"
```

## Privacy Note

The tool only reads your local `.bash_history` file. No data is sent anywhere. The exported report is saved locally.

## Troubleshooting

**"History file not found"** - Your shell might use a different file (`.zsh_history`, `.history`)

**"History file is empty"** - Check if `HISTFILE` is set correctly in your shell config

**Limited commands shown** - Increase `HISTSIZE` and `HISTFILESIZE` in `.bashrc`

## License

Developed by SSoft.in

---

*Discover your command-line patterns and work smarter in the terminal!*