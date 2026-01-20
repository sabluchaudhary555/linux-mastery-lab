#!/usr/bin/env python3
"""
Linux Permission Visualizer
Displays file/directory permissions in multiple formats with detailed explanations
"""

import os
import sys
import stat
from datetime import datetime


class PermissionVisualizer:
    def __init__(self):
        self.risky_perms = ['777', '666', '776', '767']

    def colorize(self, text, color_code):
        """Add color to terminal output"""
        return f"\033[{color_code}m{text}\033[0m"

    def get_file_type_symbol(self, mode):
        """Get file type symbol from mode"""
        if stat.S_ISDIR(mode):
            return 'd', 'Directory'
        elif stat.S_ISLNK(mode):
            return 'l', 'Symbolic Link'
        elif stat.S_ISBLK(mode):
            return 'b', 'Block Device'
        elif stat.S_ISCHR(mode):
            return 'c', 'Character Device'
        elif stat.S_ISFIFO(mode):
            return 'p', 'Named Pipe'
        elif stat.S_ISSOCK(mode):
            return 's', 'Socket'
        else:
            return '-', 'Regular File'

    def mode_to_symbolic(self, mode):
        """Convert mode to symbolic notation (rwxrwxrwx)"""
        perms = []

        # Owner permissions
        perms.append('r' if mode & stat.S_IRUSR else '-')
        perms.append('w' if mode & stat.S_IWUSR else '-')
        perms.append('x' if mode & stat.S_IXUSR else '-')

        # Group permissions
        perms.append('r' if mode & stat.S_IRGRP else '-')
        perms.append('w' if mode & stat.S_IWGRP else '-')
        perms.append('x' if mode & stat.S_IXGRP else '-')

        # Other permissions
        perms.append('r' if mode & stat.S_IROTH else '-')
        perms.append('w' if mode & stat.S_IWOTH else '-')
        perms.append('x' if mode & stat.S_IXOTH else '-')

        return ''.join(perms)

    def mode_to_numeric(self, mode):
        """Convert mode to numeric notation (755)"""
        # Extract permission bits
        owner = (mode & 0o700) >> 6
        group = (mode & 0o070) >> 3
        other = mode & 0o007

        return f"{owner}{group}{other}"

    def symbolic_to_numeric_single(self, symbolic):
        """Convert single rwx to numeric (e.g., rwx -> 7)"""
        value = 0
        if symbolic[0] == 'r':
            value += 4
        if symbolic[1] == 'w':
            value += 2
        if symbolic[2] == 'x':
            value += 1
        return value

    def get_permission_explanation(self, perm_char, perm_type, file_type):
        """Get explanation for a permission"""
        if perm_char == '-':
            return f"Cannot {perm_type.lower()}"

        if file_type == 'Directory':
            explanations = {
                'Read': 'Can list directory contents',
                'Write': 'Can create/delete files in directory',
                'Execute': 'Can access/enter directory'
            }
        else:
            explanations = {
                'Read': 'Can view file contents',
                'Write': 'Can modify file contents',
                'Execute': 'Can run file as program'
            }

        return explanations.get(perm_type, '')

    def analyze_security(self, numeric, symbolic, file_type):
        """Analyze security implications of permissions"""
        risks = []
        warnings = []

        # Check for 777 or 666
        if numeric in self.risky_perms:
            risks.append(f"⚠️  Dangerous permissions ({numeric})!")
            if numeric == '777':
                risks.append("   EVERYONE has FULL ACCESS to this file!")
            elif numeric == '666':
                risks.append("   EVERYONE can read and write this file!")

        # Check for world-writable
        if symbolic[7] == 'w':
            risks.append("⚠️  File is world-writable! ANYONE can modify it!")
            warnings.append("   Malicious users can modify or delete the file")
            warnings.append("   File could be replaced with malicious code")

        # Check for world-executable
        if symbolic[8] == 'x' and file_type == 'Regular File':
            if symbolic[7] == 'w':
                risks.append("⚠️  File is world-executable AND writable!")
                warnings.append("   This is extremely dangerous!")

        return risks, warnings

    def suggest_permissions(self, file_type, filename, numeric):
        """Suggest appropriate permissions"""
        suggestions = []

        if numeric in self.risky_perms:
            if file_type == 'Directory':
                suggestions.append("• chmod 755 " + filename + "  (standard directory)")
                suggestions.append("• chmod 700 " + filename + "  (private directory)")
            else:
                if filename.endswith(('.sh', '.py', '.pl', '.rb')):
                    suggestions.append("• chmod 755 " + filename + "  (executable script)")
                    suggestions.append("• chmod 700 " + filename + "  (private script)")
                elif 'config' in filename.lower() or 'secret' in filename.lower():
                    suggestions.append("• chmod 600 " + filename + "  (private config)")
                    suggestions.append("• chmod 400 " + filename + "  (read-only secret)")
                else:
                    suggestions.append("• chmod 644 " + filename + "  (standard file)")
                    suggestions.append("• chmod 600 " + filename + "  (private file)")

        return suggestions

    def visualize_file(self, filepath):
        """Visualize permissions for a single file"""
        try:
            # Get file stats
            file_stat = os.stat(filepath)
            mode = file_stat.st_mode

            # Get file information
            file_type_symbol, file_type = self.get_file_type_symbol(mode)
            symbolic = self.mode_to_symbolic(mode)
            numeric = self.mode_to_numeric(mode)

            # Get owner and group info
            try:
                import pwd
                import grp
                owner = pwd.getpwuid(file_stat.st_uid).pw_name
                group = grp.getgrgid(file_stat.st_gid).gr_name
            except:
                owner = str(file_stat.st_uid)
                group = str(file_stat.st_gid)

            # Extract individual permissions
            owner_perms = symbolic[0:3]
            group_perms = symbolic[3:6]
            other_perms = symbolic[6:9]

            # Print header
            print("\n" + "┌" + "─" * 63 + "┐")
            print("│" + self.colorize("              PERMISSION VISUALIZER", "1;96").center(73) + "│")
            print("├" + "─" * 63 + "┤")
            print(f"│ File: {self.colorize(os.path.basename(filepath), '1;97'):<63}│")
            print(f"│ Type: {file_type:<55}│")
            if file_type == 'Regular File' and mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH):
                print(f"│       {self.colorize('(Executable)', '92'):<63}│")
            print("└" + "─" * 63 + "┘")

            # Symbolic notation
            print(f"\n{self.colorize('📊 SYMBOLIC NOTATION:', '1;93')} {file_type_symbol}{symbolic}")
            print(f"    │ │  │  │")
            print(f"    │ │  │  └──── Other (Everyone): {other_perms}")
            print(f"    │ │  └─────── Group ({group}): {group_perms}")
            print(f"    │ └────────── Owner ({owner}): {owner_perms}")
            print(f"    └─────────── Type: {file_type_symbol} ({file_type})")

            # Numeric notation
            print(f"\n{self.colorize('🔢 NUMERIC NOTATION:', '1;93')} {numeric}")
            print(f"    {numeric[0]}     {numeric[1]}     {numeric[2]}")
            print(f"    │     │     │")
            print(f"    │     │     └──── Other: {numeric[2]} = {other_perms}")
            print(f"    │     └────────── Group: {numeric[1]} = {group_perms}")
            print(f"    └──────────────── Owner: {numeric[0]} = {owner_perms}")

            # Calculation breakdown
            print(f"\n{self.colorize('📐 CALCULATION BREAKDOWN:', '1;93')}")
            print(f"  Owner: {numeric[0]} = ", end="")
            calc_parts = []
            if owner_perms[0] == 'r': calc_parts.append("Read(4)")
            if owner_perms[1] == 'w': calc_parts.append("Write(2)")
            if owner_perms[2] == 'x': calc_parts.append("Execute(1)")
            if calc_parts:
                print(" + ".join(calc_parts) + f" = {owner_perms}")
            else:
                print("No permissions = ---")

            print(f"  Group: {numeric[1]} = ", end="")
            calc_parts = []
            if group_perms[0] == 'r': calc_parts.append("Read(4)")
            if group_perms[1] == 'w': calc_parts.append("Write(2)")
            if group_perms[2] == 'x': calc_parts.append("Execute(1)")
            if calc_parts:
                print(" + ".join(calc_parts) + f" = {group_perms}")
            else:
                print("No permissions = ---")

            print(f"  Other: {numeric[2]} = ", end="")
            calc_parts = []
            if other_perms[0] == 'r': calc_parts.append("Read(4)")
            if other_perms[1] == 'w': calc_parts.append("Write(2)")
            if other_perms[2] == 'x': calc_parts.append("Execute(1)")
            if calc_parts:
                print(" + ".join(calc_parts) + f" = {other_perms}")
            else:
                print("No permissions = ---")

            # Detailed breakdown
            print(f"\n{self.colorize('📋 DETAILED BREAKDOWN:', '1;93')}")

            # Owner permissions
            print(f"\n  Owner ({self.colorize(owner, '96')}):")
            for i, perm_type in enumerate(['Read', 'Write', 'Execute']):
                perm_char = owner_perms[i]
                symbol = '✓' if perm_char != '-' else '✗'
                color = '92' if perm_char != '-' else '91'
                explanation = self.get_permission_explanation(perm_char, perm_type, file_type)
                print(f"    {self.colorize(symbol, color)} {perm_type:<8} ({perm_char}) - {explanation}")

            # Group permissions
            print(f"\n  Group ({self.colorize(group, '96')}):")
            for i, perm_type in enumerate(['Read', 'Write', 'Execute']):
                perm_char = group_perms[i]
                symbol = '✓' if perm_char != '-' else '✗'
                color = '92' if perm_char != '-' else '91'
                explanation = self.get_permission_explanation(perm_char, perm_type, file_type)
                print(f"    {self.colorize(symbol, color)} {perm_type:<8} ({perm_char}) - {explanation}")

            # Other permissions
            print(f"\n  Other ({self.colorize('Everyone else', '96')}):")
            for i, perm_type in enumerate(['Read', 'Write', 'Execute']):
                perm_char = other_perms[i]
                symbol = '✓' if perm_char != '-' else '✗'
                color = '92' if perm_char != '-' else '91'
                explanation = self.get_permission_explanation(perm_char, perm_type, file_type)
                print(f"    {self.colorize(symbol, color)} {perm_type:<8} ({perm_char}) - {explanation}")

            # Security assessment
            risks, warnings = self.analyze_security(numeric, symbolic, file_type)

            if risks:
                print(f"\n{self.colorize('🔐 SECURITY ASSESSMENT:', '1;93')} {self.colorize('⚠️ HIGH RISK!', '1;91')}")
                for risk in risks:
                    print(f"   {risk}")
                if warnings:
                    print(f"\n   RISKS:")
                    for warning in warnings:
                        print(f"   {warning}")
            else:
                print(f"\n{self.colorize('🔐 SECURITY ASSESSMENT:', '1;93')} {self.colorize('✓ SAFE', '1;92')}")
                if numeric == '644':
                    print("   Standard file permissions. Readable by everyone,")
                    print("   but only owner can modify.")
                elif numeric == '755':
                    if file_type == 'Directory':
                        print("   Standard directory permissions. Everyone can access,")
                        print("   but only owner can modify contents.")
                    else:
                        print("   Standard executable permissions. Everyone can run,")
                        print("   but only owner can modify.")
                elif numeric == '600':
                    print("   Private file. Only owner can read and write.")
                elif numeric == '700':
                    if file_type == 'Directory':
                        print("   Private directory. Only owner has access.")
                    else:
                        print("   Private executable. Only owner can use.")
                elif numeric == '400':
                    print("   Read-only for owner. Maximum security for secrets.")

            # Suggestions
            suggestions = self.suggest_permissions(file_type, os.path.basename(filepath), numeric)
            if suggestions:
                print(f"\n{self.colorize('💡 RECOMMENDATIONS:', '1;93')}")
                for suggestion in suggestions:
                    print(f"   {suggestion}")

            # Use case
            print(f"\n{self.colorize('💡 COMMON USE CASES:', '1;93')}")
            if numeric == '644':
                print("   • Text files, documents, README files")
                print("   • HTML, CSS, configuration files")
            elif numeric == '755':
                if file_type == 'Directory':
                    print("   • Public directories, project folders")
                else:
                    print("   • Shell scripts, Python scripts")
                    print("   • Any executable programs")
            elif numeric == '600':
                print("   • Private notes, personal data")
                print("   • SSH keys, API tokens")
            elif numeric == '700':
                print("   • Private scripts and executables")
                print("   • Personal bin directory")
            elif numeric == '400':
                print("   • SSH private keys")
                print("   • API secrets, passwords")
                print("   • Read-only configuration")

            print()

        except FileNotFoundError:
            print(f"\n{self.colorize('Error:', '91')} File not found: {filepath}")
        except PermissionError:
            print(f"\n{self.colorize('Error:', '91')} Permission denied: {filepath}")
        except Exception as e:
            print(f"\n{self.colorize('Error:', '91')} {str(e)}")

    def run(self, files):
        """Run visualizer on multiple files"""
        print("\n" + "=" * 65)
        print(self.colorize("       LINUX FILE PERMISSION VISUALIZER", "1;96"))
        print("=" * 65)

        if not files:
            print("\nUsage: python3 permission_visualizer.py <file1> [file2] [...]")
            print("\nExamples:")
            print("  python3 permission_visualizer.py myfile.txt")
            print("  python3 permission_visualizer.py script.sh config.json")
            print("  python3 permission_visualizer.py /path/to/directory/*")
            return

        for filepath in files:
            self.visualize_file(filepath)

        print("=" * 65)
        print(self.colorize("Visualization Complete!", "1;92"))
        print("=" * 65)
        print()


def main():
    """Main entry point"""
    visualizer = PermissionVisualizer()

    # Get files from command line arguments
    files = sys.argv[1:]

    visualizer.run(files)


if __name__ == "__main__":
    main()

    """
        Linux Permission Visualizer
        Developed By SSoft.in

        """