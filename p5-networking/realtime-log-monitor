#!/usr/bin/env python3
"""
Real-Time Log Monitor Dashboard
Live dashboard showing system events as they happen
"""

import curses
import time
import re
import threading
from pathlib import Path
from collections import deque
from datetime import datetime
import subprocess

class LogMonitor:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.logs = {}
        self.active_logs = []
        self.paused = False
        self.filter_pattern = ""
        self.alert_patterns = []
        self.max_lines = 1000
        self.current_view = 0
        self.monitoring = True

        # Color pairs
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)      # ERROR/CRITICAL
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)   # WARNING
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)    # INFO/SUCCESS
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)     # DEBUG
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  # ALERT
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLUE)     # HEADER

        # Default log files
        self.default_logs = [
            '/var/log/syslog',
            '/var/log/auth.log',
            '/var/log/apache2/error.log',
            '/var/log/nginx/error.log'
        ]

        self.init_logs()

    def init_logs(self):
        """Initialize log file monitoring"""
        for log_file in self.default_logs:
            if Path(log_file).exists():
                self.logs[log_file] = {
                    'lines': deque(maxlen=self.max_lines),
                    'file_handle': None,
                    'position': 0,
                    'enabled': True
                }
                self.active_logs.append(log_file)

    def get_severity_color(self, line):
        """Determine color based on log severity"""
        line_upper = line.upper()

        if any(word in line_upper for word in ['ERROR', 'FATAL', 'CRITICAL', 'FAILED']):
            return curses.color_pair(1)  # Red
        elif any(word in line_upper for word in ['WARN', 'WARNING']):
            return curses.color_pair(2)  # Yellow
        elif any(word in line_upper for word in ['INFO', 'SUCCESS', 'OK']):
            return curses.color_pair(3)  # Green
        elif 'DEBUG' in line_upper:
            return curses.color_pair(4)  # Cyan

        return curses.A_NORMAL

    def check_alert(self, line):
        """Check if line matches alert patterns"""
        for pattern in self.alert_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                return True
        return False

    def tail_log(self, log_file):
        """Tail a log file continuously"""
        try:
            # Use tail -f for efficient monitoring
            process = subprocess.Popen(
                ['tail', '-f', '-n', '50', log_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            for line in iter(process.stdout.readline, ''):
                if not self.monitoring:
                    process.kill()
                    break

                if self.paused:
                    time.sleep(0.1)
                    continue

                line = line.strip()
                if not line:
                    continue

                # Apply filter
                if self.filter_pattern and self.filter_pattern not in line:
                    continue

                # Add timestamp if not present
                timestamp = datetime.now().strftime('%H:%M:%S')

                # Check for alerts
                is_alert = self.check_alert(line)

                self.logs[log_file]['lines'].append({
                    'text': line,
                    'time': timestamp,
                    'alert': is_alert
                })

        except FileNotFoundError:
            pass
        except PermissionError:
            pass

    def draw_header(self):
        """Draw the header section"""
        height, width = self.stdscr.getmaxyx()

        # Title
        title = " Real-Time Log Monitor Dashboard "
        self.stdscr.attron(curses.color_pair(6) | curses.A_BOLD)
        self.stdscr.addstr(0, (width - len(title)) // 2, title)
        self.stdscr.attroff(curses.color_pair(6) | curses.A_BOLD)

        # Status line
        status = f" {'PAUSED' if self.paused else 'MONITORING'} | Filter: {self.filter_pattern or 'None'} | Logs: {len(self.active_logs)} "
        self.stdscr.addstr(1, 0, status[:width-1])

        # Active log files
        log_info = f" Viewing: {Path(self.active_logs[self.current_view]).name if self.active_logs else 'None'} "
        self.stdscr.addstr(2, 0, log_info[:width-1], curses.A_BOLD)

        # Separator
        self.stdscr.addstr(3, 0, "─" * (width - 1))

    def draw_footer(self):
        """Draw the footer with commands"""
        height, width = self.stdscr.getmaxyx()

        commands = [
            "q:Quit", "p:Pause/Resume", "f:Filter", "n:Next Log",
            "a:Add Alert", "c:Clear", "h:Help"
        ]

        footer = " | ".join(commands)
        self.stdscr.attron(curses.color_pair(6))
        self.stdscr.addstr(height - 1, 0, footer[:width-1].ljust(width-1))
        self.stdscr.attroff(curses.color_pair(6))

    def draw_logs(self):
        """Draw log lines"""
        height, width = self.stdscr.getmaxyx()

        if not self.active_logs:
            self.stdscr.addstr(5, 2, "No log files available")
            return

        current_log = self.active_logs[self.current_view]
        lines = list(self.logs[current_log]['lines'])

        # Calculate available space
        start_row = 4
        end_row = height - 2
        visible_lines = end_row - start_row

        # Show recent lines
        display_lines = lines[-visible_lines:] if len(lines) > visible_lines else lines

        row = start_row
        for line_data in display_lines:
            if row >= end_row:
                break

            text = line_data['text']
            time_str = line_data['time']
            is_alert = line_data['alert']

            # Format: [TIME] message
            display_text = f"[{time_str}] {text}"

            # Truncate if too long
            if len(display_text) > width - 2:
                display_text = display_text[:width-5] + "..."

            # Apply color
            if is_alert:
                color = curses.color_pair(5) | curses.A_BOLD  # Magenta for alerts
            else:
                color = self.get_severity_color(text)

            try:
                self.stdscr.addstr(row, 1, display_text, color)
            except curses.error:
                pass

            row += 1

    def draw_split_view(self):
        """Draw multiple logs in split view"""
        height, width = self.stdscr.getmaxyx()

        if len(self.active_logs) < 2:
            self.draw_logs()
            return

        # Split horizontally for 2 logs
        mid_col = width // 2

        for idx, log_file in enumerate(self.active_logs[:2]):
            lines = list(self.logs[log_file]['lines'])

            # Column boundaries
            start_col = 1 if idx == 0 else mid_col + 1
            end_col = mid_col - 1 if idx == 0 else width - 2
            col_width = end_col - start_col

            # Draw log name
            log_name = Path(log_file).name
            try:
                self.stdscr.addstr(4, start_col, log_name[:col_width], curses.A_BOLD)
            except curses.error:
                pass

            # Draw separator
            if idx == 0:
                for r in range(4, height - 2):
                    try:
                        self.stdscr.addstr(r, mid_col, "│")
                    except curses.error:
                        pass

            # Draw lines
            start_row = 5
            end_row = height - 2
            visible_lines = end_row - start_row
            display_lines = lines[-visible_lines:] if len(lines) > visible_lines else lines

            row = start_row
            for line_data in display_lines:
                if row >= end_row:
                    break

                text = line_data['text']
                is_alert = line_data['alert']

                # Truncate
                if len(text) > col_width:
                    text = text[:col_width-3] + "..."

                # Apply color
                color = curses.color_pair(5) if is_alert else self.get_severity_color(text)

                try:
                    self.stdscr.addstr(row, start_col, text, color)
                except curses.error:
                    pass

                row += 1

    def show_help(self):
        """Show help screen"""
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()

        help_text = [
            "Real-Time Log Monitor - Help",
            "",
            "Commands:",
            "  q - Quit the application",
            "  p - Pause/Resume monitoring",
            "  f - Set filter pattern",
            "  n - Switch to next log file",
            "  a - Add alert pattern",
            "  c - Clear current log view",
            "  s - Toggle split view (2 logs)",
            "  h - Show this help",
            "",
            "Colors:",
            "  RED - Errors, Critical, Failed",
            "  YELLOW - Warnings",
            "  GREEN - Info, Success",
            "  CYAN - Debug",
            "  MAGENTA - Alert matches",
            "",
            "Press any key to continue..."
        ]

        row = 2
        for line in help_text:
            if row >= height - 2:
                break
            self.stdscr.addstr(row, 2, line[:width-4])
            row += 1

        self.stdscr.refresh()
        self.stdscr.getch()

    def set_filter(self):
        """Set filter pattern"""
        height, width = self.stdscr.getmaxyx()

        curses.echo()
        self.stdscr.addstr(height - 2, 0, "Enter filter pattern: ".ljust(width-1))
        self.stdscr.refresh()

        try:
            pattern = self.stdscr.getstr(height - 2, 22, 50).decode('utf-8')
            self.filter_pattern = pattern
        except:
            pass

        curses.noecho()

    def add_alert_pattern(self):
        """Add alert pattern"""
        height, width = self.stdscr.getmaxyx()

        curses.echo()
        self.stdscr.addstr(height - 2, 0, "Enter alert pattern: ".ljust(width-1))
        self.stdscr.refresh()

        try:
            pattern = self.stdscr.getstr(height - 2, 21, 50).decode('utf-8')
            if pattern:
                self.alert_patterns.append(pattern)
        except:
            pass

        curses.noecho()

    def next_log(self):
        """Switch to next log file"""
        if self.active_logs:
            self.current_view = (self.current_view + 1) % len(self.active_logs)

    def clear_current_log(self):
        """Clear current log view"""
        if self.active_logs:
            current_log = self.active_logs[self.current_view]
            self.logs[current_log]['lines'].clear()

    def run(self):
        """Main run loop"""
        # Start monitoring threads
        threads = []
        for log_file in self.active_logs:
            thread = threading.Thread(target=self.tail_log, args=(log_file,), daemon=True)
            thread.start()
            threads.append(thread)

        # Set up curses
        self.stdscr.nodelay(True)
        curses.curs_set(0)

        split_view = False

        try:
            while True:
                self.stdscr.clear()

                # Draw interface
                self.draw_header()

                if split_view and len(self.active_logs) >= 2:
                    self.draw_split_view()
                else:
                    self.draw_logs()

                self.draw_footer()

                self.stdscr.refresh()

                # Handle input
                try:
                    key = self.stdscr.getch()

                    if key == ord('q'):
                        break
                    elif key == ord('p'):
                        self.paused = not self.paused
                    elif key == ord('f'):
                        self.set_filter()
                    elif key == ord('n'):
                        self.next_log()
                    elif key == ord('a'):
                        self.add_alert_pattern()
                    elif key == ord('c'):
                        self.clear_current_log()
                    elif key == ord('s'):
                        split_view = not split_view
                    elif key == ord('h'):
                        self.show_help()

                except curses.error:
                    pass

                time.sleep(0.1)

        finally:
            self.monitoring = False


def main(stdscr):
    monitor = LogMonitor(stdscr)
    monitor.run()


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("\nMonitoring stopped")
    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: This tool requires read access to log files.")
        print("Try running with sudo: sudo python3 realtime_log_monitor.py")