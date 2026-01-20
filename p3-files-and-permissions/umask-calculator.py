#!/usr/bin/env python3
"""
umask Calculator & Simulator
Shows how umask values affect default file/directory permissions
"""

import os
import sys


class UmaskCalculator:
    def __init__(self):
        self.presets = {
            '0000': {
                'name': 'Unrestricted',
                'desc': 'No restrictions (DANGEROUS - not recommended)',
                'use_case': 'Testing only, never for production'
            },
            '0002': {
                'name': 'Group Writable',
                'desc': 'Group members can write, others read only',
                'use_case': 'Team collaboration, shared projects'
            },
            '0022': {
                'name': 'Standard (Default)',
                'desc': 'Owner writes, everyone reads',
                'use_case': 'Most common, general purpose usage'
            },
            '0027': {
                'name': 'Restricted Group',
                'desc': 'Group can read, no access for others',
                'use_case': 'Departmental files, limited sharing'
            },
            '0077': {
                'name': 'Private (Secure)',
                'desc': 'Only owner has access',
                'use_case': 'Personal files, sensitive data'
            }
        }

    def colorize(self, text, color_code):
        """Add color to terminal output"""
        return f"\033[{color_code}m{text}\033[0m"

    def octal_to_symbolic(self, octal):
        """Convert octal to symbolic notation"""
        perms = ['r', 'w', 'x']
        result = []

        for digit in octal:
            value = int(digit)
            symbolic = ''
            for i, perm in enumerate(perms):
                if value & (4 >> i):
                    symbolic += perm
                else:
                    symbolic += '-'
            result.append(symbolic)

        return ''.join(result)

    def calculate_permissions(self, umask_value):
        """Calculate resulting file and directory permissions"""
        # Remove leading zeros and convert to int
        umask_int = int(umask_value, 8)

        # Maximum permissions
        max_file = 0o666  # rw-rw-rw-
        max_dir = 0o777  # rwxrwxrwx

        # Calculate resulting permissions
        file_perms = max_file & ~umask_int
        dir_perms = max_dir & ~umask_int

        # Convert to octal strings (without 0o prefix)
        file_octal = oct(file_perms)[2:].zfill(3)
        dir_octal = oct(dir_perms)[2:].zfill(3)

        # Convert to symbolic
        file_symbolic = self.octal_to_symbolic(file_octal)
        dir_symbolic = self.octal_to_symbolic(dir_octal)

        return {
            'file_octal': file_octal,
            'file_symbolic': file_symbolic,
            'dir_octal': dir_octal,
            'dir_symbolic': dir_symbolic
        }

    def print_header(self):
        """Print calculator header"""
        print("\n" + "=" * 80)
        print(self.colorize("                 umask CALCULATOR & SIMULATOR", "1;96"))
        print("=" * 80)
        print()

    def print_umask_explanation(self):
        """Print explanation of umask"""
        print(self.colorize("📚 WHAT IS umask?", "1;93"))
        print("-" * 80)
        print("umask (User Mask) sets the DEFAULT permissions for newly created files")
        print("and directories by subtracting from maximum permissions.")
        print()
        print("Formula:")
        print("  • File permissions       = 666 (rw-rw-rw-) - umask")
        print("  • Directory permissions  = 777 (rwxrwxrwx) - umask")
        print()
        print("The umask value specifies which permissions to REMOVE.")
        print()

    def display_calculation_steps(self, umask_value):
        """Display step-by-step calculation"""
        print(self.colorize(f"🔢 CALCULATING FOR umask: {umask_value}", "1;93"))
        print("-" * 80)
        print()

        # Show for files
        print(self.colorize("📄 FILES:", "1;94"))
        print(f"  Maximum permissions:  666 (rw-rw-rw-)")
        print(f"  Minus umask:         -{umask_value[1:]}")
        print(f"  {'─' * 25}")

        result = self.calculate_permissions(umask_value)
        file_color = '92' if result['file_octal'] in ['644', '640', '600'] else '93'

        print(f"  Result:               {self.colorize(result['file_octal'], file_color)} ({result['file_symbolic']})")
        print()

        # Show for directories
        print(self.colorize("📁 DIRECTORIES:", "1;94"))
        print(f"  Maximum permissions:  777 (rwxrwxrwx)")
        print(f"  Minus umask:         -{umask_value[1:]}")
        print(f"  {'─' * 25}")

        dir_color = '92' if result['dir_octal'] in ['755', '750', '700'] else '93'
        print(f"  Result:               {self.colorize(result['dir_octal'], dir_color)} ({result['dir_symbolic']})")
        print()

    def display_detailed_breakdown(self, umask_value):
        """Display detailed permission breakdown"""
        result = self.calculate_permissions(umask_value)

        print(self.colorize("📊 DETAILED BREAKDOWN:", "1;93"))
        print("-" * 80)
        print()

        # Files
        print(self.colorize("Files created with this umask:", "1;97"))
        print(f"  Octal:    {result['file_octal']}")
        print(f"  Symbolic: {result['file_symbolic']}")
        print(f"  Meaning:")

        file_parts = [result['file_symbolic'][i:i + 3] for i in range(0, 9, 3)]
        categories = ['Owner', 'Group', 'Other']

        for i, (cat, perms) in enumerate(zip(categories, file_parts)):
            can_do = []
            if perms[0] == 'r': can_do.append('read')
            if perms[1] == 'w': can_do.append('write')
            if perms[2] == 'x': can_do.append('execute')

            if can_do:
                print(f"    • {cat:6} ({perms}): Can {', '.join(can_do)}")
            else:
                print(f"    • {cat:6} ({perms}): No permissions")

        print()

        # Directories
        print(self.colorize("Directories created with this umask:", "1;97"))
        print(f"  Octal:    {result['dir_octal']}")
        print(f"  Symbolic: {result['dir_symbolic']}")
        print(f"  Meaning:")

        dir_parts = [result['dir_symbolic'][i:i + 3] for i in range(0, 9, 3)]

        for i, (cat, perms) in enumerate(zip(categories, dir_parts)):
            can_do = []
            if perms[0] == 'r': can_do.append('list contents')
            if perms[1] == 'w': can_do.append('create/delete files')
            if perms[2] == 'x': can_do.append('enter directory')

            if can_do:
                print(f"    • {cat:6} ({perms}): Can {', '.join(can_do)}")
            else:
                print(f"    • {cat:6} ({perms}): No access")

        print()

    def display_security_analysis(self, umask_value):
        """Display security analysis"""
        result = self.calculate_permissions(umask_value)

        print(self.colorize("🔐 SECURITY ANALYSIS:", "1;93"))
        print("-" * 80)

        warnings = []
        recommendations = []

        # Check file permissions
        file_octal = result['file_octal']
        if file_octal[2] in ['2', '3', '6', '7']:
            warnings.append("⚠️  Files are world-writable! Anyone can modify your files.")
        if file_octal == '666':
            warnings.append("⚠️  Files are fully readable and writable by everyone!")

        # Check directory permissions
        dir_octal = result['dir_octal']
        if dir_octal[2] in ['2', '3', '6', '7']:
            warnings.append("⚠️  Directories are world-writable! Anyone can create/delete files.")
        if dir_octal == '777':
            warnings.append("⚠️  Directories have full permissions for everyone!")

        # Security level
        if umask_value == '0077':
            level = self.colorize("🟢 MAXIMUM SECURITY", "1;92")
            print(f"  Security Level: {level}")
            print("  • Files and directories are completely private")
            print("  • Only the owner has any access")
            print("  • Ideal for sensitive personal data")
        elif umask_value == '0027':
            level = self.colorize("🟢 HIGH SECURITY", "1;92")
            print(f"  Security Level: {level}")
            print("  • Files are protected from non-group members")
            print("  • Group has restricted access")
            print("  • Good for departmental data")
        elif umask_value == '0022':
            level = self.colorize("🟡 MODERATE SECURITY", "1;93")
            print(f"  Security Level: {level}")
            print("  • Standard Unix/Linux default")
            print("  • Files readable by everyone")
            print("  • Only owner can modify")
        elif umask_value == '0002':
            level = self.colorize("🟡 LOW SECURITY", "1;93")
            print(f"  Security Level: {level}")
            print("  • Group members can modify files")
            print("  • Good for collaborative environments")
            print("  • Requires trust within group")
        else:
            level = self.colorize("🔴 VERY LOW SECURITY", "1;91")
            print(f"  Security Level: {level}")

        if warnings:
            print()
            print(self.colorize("  WARNINGS:", "1;91"))
            for warning in warnings:
                print(f"    {warning}")

        print()

    def display_use_cases(self, umask_value):
        """Display practical use cases"""
        print(self.colorize("💡 PRACTICAL USE CASES:", "1;93"))
        print("-" * 80)

        if umask_value == '0022':
            print("  ✓ Personal workstations")
            print("  ✓ General purpose servers")
            print("  ✓ Web servers (public content)")
            print("  ✓ Documentation and README files")
        elif umask_value == '0002':
            print("  ✓ Development teams")
            print("  ✓ Shared project directories")
            print("  ✓ Collaborative workspaces")
            print("  ✓ Group-managed servers")
        elif umask_value == '0027':
            print("  ✓ Department servers")
            print("  ✓ Restricted project files")
            print("  ✓ Internal documentation")
            print("  ✓ Confidential group data")
        elif umask_value == '0077':
            print("  ✓ Personal home directories")
            print("  ✓ SSH keys and credentials")
            print("  ✓ Private configuration files")
            print("  ✓ Sensitive personal data")
        elif umask_value == '0000':
            print("  ⚠️  NOT RECOMMENDED for any production use")
            print("  ⚠️  Testing/debugging only")
            print("  ⚠️  Creates major security vulnerabilities")

        print()

    def display_commands(self, umask_value):
        """Display commands to set this umask"""
        print(self.colorize("⚙️  HOW TO SET THIS umask:", "1;93"))
        print("-" * 80)

        print(self.colorize("Temporary (current session only):", "97"))
        print(f"  umask {umask_value}")
        print()

        print(self.colorize("Permanent (for your user):", "97"))
        print(f"  echo 'umask {umask_value}' >> ~/.bashrc")
        print(f"  source ~/.bashrc")
        print()

        print(self.colorize("System-wide (requires root):", "97"))
        print(f"  echo 'umask {umask_value}' >> /etc/profile")
        print()

        print(self.colorize("Verify current umask:", "97"))
        print("  umask")
        print()

        print(self.colorize("Test by creating files:", "97"))
        print("  touch testfile.txt")
        print("  mkdir testdir")
        print("  ls -l testfile.txt")
        print("  ls -ld testdir")
        print()

    def compare_umasks(self):
        """Compare all preset umasks side by side"""
        print(self.colorize("📊 PRESET COMPARISON TABLE:", "1;93"))
        print("=" * 80)
        print()

        print(f"{'umask':<8} {'Files':<15} {'Dirs':<15} {'Security':<15} {'Use Case'}")
        print("-" * 80)

        for umask_val in ['0000', '0002', '0022', '0027', '0077']:
            result = self.calculate_permissions(umask_val)
            preset = self.presets[umask_val]

            files = f"{result['file_octal']} ({result['file_symbolic']})"
            dirs = f"{result['dir_octal']} ({result['dir_symbolic']})"

            # Color code security
            if umask_val in ['0077', '0027']:
                security_color = '92'  # Green
            elif umask_val in ['0022', '0002']:
                security_color = '93'  # Yellow
            else:
                security_color = '91'  # Red

            security = self.colorize(preset['name'], security_color)

            print(f"{umask_val:<8} {files:<15} {dirs:<15} {security:<24} {preset['use_case'][:30]}")

        print()

    def interactive_mode(self):
        """Interactive umask calculator"""
        self.print_header()

        print(self.colorize("Welcome to the umask Calculator & Simulator!", "1;96"))
        print()

        while True:
            print("\n" + "=" * 80)
            print(self.colorize("MENU:", "1;93"))
            print("  1. Calculate custom umask value")
            print("  2. View preset umask values")
            print("  3. Compare all presets")
            print("  4. Learn about umask")
            print("  5. Exit")
            print("=" * 80)

            choice = input("\nEnter your choice (1-5): ").strip()

            if choice == '1':
                umask_input = input("\nEnter umask value (e.g., 0022): ").strip()

                # Validate input
                if not umask_input.startswith('0'):
                    umask_input = '0' + umask_input

                if len(umask_input) != 4 or not all(c in '01234567' for c in umask_input):
                    print(self.colorize("\n❌ Invalid umask value! Use 4 octal digits (0-7).", "91"))
                    continue

                print()
                self.display_calculation_steps(umask_input)
                self.display_detailed_breakdown(umask_input)
                self.display_security_analysis(umask_input)
                self.display_use_cases(umask_input)
                self.display_commands(umask_input)

            elif choice == '2':
                print("\n" + "=" * 80)
                print(self.colorize("PRESET umask VALUES:", "1;93"))
                print("=" * 80)
                print()

                for i, (umask_val, preset) in enumerate(self.presets.items(), 1):
                    print(f"{i}. {self.colorize(preset['name'], '1;96')} - umask {umask_val}")
                    print(f"   {preset['desc']}")
                    print(f"   Use case: {preset['use_case']}")
                    print()

                preset_choice = input("Enter preset number (1-5) or 0 to go back: ").strip()

                if preset_choice in ['1', '2', '3', '4', '5']:
                    umask_val = list(self.presets.keys())[int(preset_choice) - 1]
                    print()
                    self.display_calculation_steps(umask_val)
                    self.display_detailed_breakdown(umask_val)
                    self.display_security_analysis(umask_val)
                    self.display_use_cases(umask_val)
                    self.display_commands(umask_val)

            elif choice == '3':
                print()
                self.compare_umasks()

            elif choice == '4':
                print()
                self.print_umask_explanation()

            elif choice == '5':
                print("\n" + self.colorize("Thank you for using umask Calculator!", "1;92"))
                print()
                break

            else:
                print(self.colorize("\n❌ Invalid choice! Please enter 1-5.", "91"))


def main():
    """Main entry point"""
    calculator = UmaskCalculator()

    if len(sys.argv) > 1:
        # Command line mode
        umask_value = sys.argv[1]

        if not umask_value.startswith('0'):
            umask_value = '0' + umask_value

        if len(umask_value) != 4 or not all(c in '01234567' for c in umask_value):
            print("Error: Invalid umask value! Use 4 octal digits (0-7).")
            print("Example: python3 umask_calculator.py 0022")
            sys.exit(1)

        calculator.print_header()
        calculator.display_calculation_steps(umask_value)
        calculator.display_detailed_breakdown(umask_value)
        calculator.display_security_analysis(umask_value)
        calculator.display_use_cases(umask_value)
        calculator.display_commands(umask_value)
    else:
        # Interactive mode
        calculator.interactive_mode()


if __name__ == "__main__":
    main()