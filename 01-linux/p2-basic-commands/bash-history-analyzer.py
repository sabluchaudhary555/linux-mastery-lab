#!/usr/bin/env python3
"""
Bash Command History Analyzer
Analyzes .bash_history to show usage patterns, statistics, and efficiency tips
"""

import os
import re
from collections import Counter, defaultdict
from datetime import datetime
import subprocess


class BashHistoryAnalyzer:
    def __init__(self):
        self.history_file = os.path.expanduser('~/.bash_history')
        self.commands = []
        self.command_stats = Counter()
        self.command_categories = defaultdict(list)

        # Command categories for classification
        self.categories = {
            'navigation': ['cd', 'ls', 'pwd', 'pushd', 'popd', 'dirs'],
            'file_operations': ['cp', 'mv', 'rm', 'touch', 'mkdir', 'rmdir', 'ln'],
            'viewing': ['cat', 'less', 'more', 'head', 'tail', 'nano', 'vi', 'vim'],
            'searching': ['grep', 'find', 'locate', 'which', 'whereis', 'awk', 'sed'],
            'system': ['ps', 'top', 'htop', 'kill', 'systemctl', 'service', 'sudo'],
            'network': ['ping', 'curl', 'wget', 'ssh', 'scp', 'netstat', 'ifconfig'],
            'package': ['apt', 'apt-get', 'yum', 'dnf', 'pip', 'npm', 'brew'],
            'git': ['git', 'github', 'gitlab'],
            'compression': ['tar', 'zip', 'unzip', 'gzip', 'gunzip', 'bzip2'],
            'permissions': ['chmod', 'chown', 'chgrp', 'umask']
        }

    def colorize(self, text, color_code):
        """Add color to terminal output"""
        return f"\033[{color_code}m{text}\033[0m"

    def print_header(self):
        """Print analyzer header"""
        print("\n" + "=" * 80)
        print(self.colorize("       BASH COMMAND HISTORY ANALYZER", "1;96"))
        print("=" * 80)
        print()

    def load_history(self):
        """Load commands from bash history file"""
        if not os.path.exists(self.history_file):
            print(f"Error: History file not found at {self.history_file}")
            return False

        try:
            with open(self.history_file, 'r', encoding='utf-8', errors='ignore') as f:
                self.commands = [line.strip() for line in f if line.strip()]

            if not self.commands:
                print("Warning: History file is empty")
                return False

            return True
        except Exception as e:
            print(f"Error reading history file: {e}")
            return False

    def extract_base_command(self, command):
        """Extract the base command from a full command line"""
        # Remove leading sudo
        command = re.sub(r'^sudo\s+', '', command)

        # Extract first word (the command)
        parts = command.split()
        if parts:
            # Handle pipes - get first command before pipe
            base = parts[0].split('|')[0].strip()
            return base
        return ''

    def analyze_commands(self):
        """Analyze command usage patterns"""
        for cmd in self.commands:
            base_cmd = self.extract_base_command(cmd)
            if base_cmd:
                self.command_stats[base_cmd] += 1

                # Categorize command
                for category, cmds in self.categories.items():
                    if base_cmd in cmds:
                        self.command_categories[category].append(cmd)
                        break

    def show_basic_statistics(self):
        """Show basic statistics about command history"""
        print(self.colorize("📊 BASIC STATISTICS", "1;93"))
        print("-" * 80)
        print(f"  Total Commands in History: {len(self.commands)}")
        print(f"  Unique Commands Used: {len(self.command_stats)}")
        print(f"  History File Location: {self.history_file}")

        # Calculate file size
        file_size = os.path.getsize(self.history_file)
        print(f"  History File Size: {file_size / 1024:.2f} KB")
        print()

    def show_top_commands(self, n=15):
        """Show most frequently used commands"""
        print(self.colorize(f"🏆 TOP {n} MOST USED COMMANDS", "1;93"))
        print("-" * 80)
        print(f"  {'Rank':<6} {'Command':<20} {'Count':<10} {'Percentage':<12} {'Bar'}")
        print("-" * 80)

        total = len(self.commands)
        for i, (cmd, count) in enumerate(self.command_stats.most_common(n), 1):
            percentage = (count / total) * 100
            bar_length = int(percentage / 2)  # Scale down for display
            bar = '█' * bar_length

            print(f"  {i:<6} {cmd:<20} {count:<10} {percentage:>5.2f}%      {bar}")
        print()

    def show_command_categories(self):
        """Show command usage by category"""
        print(self.colorize("📂 COMMAND USAGE BY CATEGORY", "1;93"))
        print("-" * 80)

        category_counts = {cat: len(cmds) for cat, cmds in self.command_categories.items()}
        sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)

        total_categorized = sum(category_counts.values())

        for category, count in sorted_categories:
            if count > 0:
                percentage = (count / len(self.commands)) * 100
                bar_length = int(percentage / 2)
                bar = '▓' * bar_length

                category_display = category.replace('_', ' ').title()
                print(f"  {category_display:<20} {count:>5} ({percentage:>5.1f}%)  {bar}")

        uncategorized = len(self.commands) - total_categorized
        if uncategorized > 0:
            percentage = (uncategorized / len(self.commands)) * 100
            print(f"  {'Other/Uncategorized':<20} {uncategorized:>5} ({percentage:>5.1f}%)")
        print()

    def analyze_pipes_and_redirection(self):
        """Analyze usage of pipes and redirection"""
        print(self.colorize("🔀 PIPES & REDIRECTION USAGE", "1;93"))
        print("-" * 80)

        pipe_commands = [cmd for cmd in self.commands if '|' in cmd]
        redirect_output = [cmd for cmd in self.commands if '>' in cmd or '>>' in cmd]
        redirect_input = [cmd for cmd in self.commands if '<' in cmd]

        print(f"  Commands with Pipes (|):           {len(pipe_commands)}")
        print(f"  Commands with Output Redirect (>): {len(redirect_output)}")
        print(f"  Commands with Input Redirect (<):  {len(redirect_input)}")

        if pipe_commands:
            print(f"\n  Most Complex Pipe Chain:")
            max_pipes = max(pipe_commands, key=lambda x: x.count('|'))
            pipe_count = max_pipes.count('|')
            print(f"    {pipe_count + 1} commands chained:")
            print(f"    {max_pipes[:70]}..." if len(max_pipes) > 70 else f"    {max_pipes}")
        print()

    def show_common_patterns(self):
        """Show common command patterns and combinations"""
        print(self.colorize("🔍 COMMON COMMAND PATTERNS", "1;93"))
        print("-" * 80)

        # Find commands with sudo
        sudo_commands = [cmd for cmd in self.commands if cmd.startswith('sudo')]
        print(f"  Commands run with sudo: {len(sudo_commands)} ({len(sudo_commands) / len(self.commands) * 100:.1f}%)")

        # Find long commands
        long_commands = [cmd for cmd in self.commands if len(cmd) > 50]
        print(f"  Long commands (>50 chars): {len(long_commands)}")

        # Find commands with options/flags
        flag_commands = [cmd for cmd in self.commands if ' -' in cmd]
        print(f"  Commands with flags: {len(flag_commands)} ({len(flag_commands) / len(self.commands) * 100:.1f}%)")

        print()

    def analyze_efficiency(self):
        """Provide efficiency suggestions"""
        print(self.colorize("💡 EFFICIENCY SUGGESTIONS", "1;93"))
        print("-" * 80)

        suggestions = []

        # Check for repetitive cd commands
        cd_count = self.command_stats.get('cd', 0)
        if cd_count > len(self.commands) * 0.15:
            suggestions.append({
                'title': 'Too many cd commands',
                'tip': 'Consider using aliases or CDPATH variable for frequently visited directories',
                'example': 'alias proj="cd ~/projects"'
            })

        # Check for repeated ls after cd
        repeated_cd_ls = 0
        for i in range(len(self.commands) - 1):
            if self.commands[i].startswith('cd ') and self.commands[i + 1].startswith('ls'):
                repeated_cd_ls += 1

        if repeated_cd_ls > 10:
            suggestions.append({
                'title': 'Frequent cd + ls pattern detected',
                'tip': 'Create a function that combines cd and ls',
                'example': 'cdls() { cd "$1" && ls; }'
            })

        # Check if using cat where less would be better
        cat_count = self.command_stats.get('cat', 0)
        less_count = self.command_stats.get('less', 0)
        if cat_count > less_count * 3:
            suggestions.append({
                'title': 'Using cat frequently for file viewing',
                'tip': 'Use less or more for better navigation of large files',
                'example': 'less filename.txt (press q to quit)'
            })

        # Check for grep without pipes
        standalone_grep = len([cmd for cmd in self.commands if cmd.startswith('grep ') and '|' not in cmd])
        if standalone_grep > 5:
            suggestions.append({
                'title': 'Standalone grep usage detected',
                'tip': 'Combine grep with other commands using pipes for powerful filtering',
                'example': 'cat file.txt | grep "pattern" | wc -l'
            })

        # Check for lack of history search
        history_grep = len([cmd for cmd in self.commands if 'history' in cmd and 'grep' in cmd])
        if history_grep < 2:
            suggestions.append({
                'title': 'Not using history search',
                'tip': 'Use Ctrl+R for reverse history search or history | grep',
                'example': 'history | grep "docker"'
            })

        if suggestions:
            for i, sug in enumerate(suggestions, 1):
                print(f"  {i}. {self.colorize(sug['title'], '1;91')}")
                print(f"     💡 {sug['tip']}")
                print(f"     Example: {self.colorize(sug['example'], '92')}")
                print()
        else:
            print("  🎉 Great job! Your command usage looks efficient!")
            print()

    def show_interesting_finds(self):
        """Show interesting patterns in command history"""
        print(self.colorize("🎯 INTERESTING FINDS", "1;93"))
        print("-" * 80)

        # Longest command
        if self.commands:
            longest = max(self.commands, key=len)
            print(f"  Longest Command ({len(longest)} chars):")
            print(f"    {longest[:70]}..." if len(longest) > 70 else f"    {longest}")
            print()

        # Most common command sequence
        sequences = []
        for i in range(len(self.commands) - 1):
            cmd1 = self.extract_base_command(self.commands[i])
            cmd2 = self.extract_base_command(self.commands[i + 1])
            if cmd1 and cmd2:
                sequences.append(f"{cmd1} → {cmd2}")

        if sequences:
            seq_counter = Counter(sequences)
            most_common_seq = seq_counter.most_common(1)[0]
            print(f"  Most Common Command Sequence:")
            print(f"    {most_common_seq[0]} (appeared {most_common_seq[1]} times)")
            print()

    def export_report(self, filename='bash_history_report.txt'):
        """Export analysis report to a file"""
        print(self.colorize("💾 EXPORT REPORT", "1;93"))
        print("-" * 80)

        try:
            with open(filename, 'w') as f:
                f.write("BASH COMMAND HISTORY ANALYSIS REPORT\n")
                f.write("=" * 60 + "\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

                f.write(f"Total Commands: {len(self.commands)}\n")
                f.write(f"Unique Commands: {len(self.command_stats)}\n\n")

                f.write("TOP 20 COMMANDS:\n")
                f.write("-" * 60 + "\n")
                for i, (cmd, count) in enumerate(self.command_stats.most_common(20), 1):
                    percentage = (count / len(self.commands)) * 100
                    f.write(f"{i:3}. {cmd:<20} {count:>6} ({percentage:>5.1f}%)\n")

                f.write("\n" + "=" * 60 + "\n")

            print(f"  ✓ Report exported to: {filename}")
            print()
        except Exception as e:
            print(f"  ✗ Error exporting report: {e}")
            print()

    def run_analysis(self):
        """Run complete analysis"""
        self.print_header()

        if not self.load_history():
            return

        print(self.colorize("Analyzing your bash command history...", "93"))
        print()

        self.analyze_commands()

        self.show_basic_statistics()
        self.show_top_commands(15)
        self.show_command_categories()
        self.analyze_pipes_and_redirection()
        self.show_common_patterns()
        self.show_interesting_finds()
        self.analyze_efficiency()
        self.export_report()

        print("=" * 80)
        print(self.colorize("Analysis Complete!", "1;92"))
        print("=" * 80)
        print()


def main():
    """Main entry point"""
    analyzer = BashHistoryAnalyzer()
    analyzer.run_analysis()


if __name__ == "__main__":
    main()

    """
    Bash History Analyzer
    Developed By SSoft.in

    """
