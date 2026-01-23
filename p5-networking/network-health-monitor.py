#!/usr/bin/env python3
"""
Network Health Monitor - Simple and Clean Implementation
Monitor network connectivity and performance in real-time
"""

import subprocess
import time
import json
import csv
import re
from datetime import datetime
from collections import deque


class NetworkMonitor:
    def __init__(self):
        self.hosts = {
            'Google DNS': '8.8.8.8',
            'Cloudflare DNS': '1.1.1.1',
            'Local Gateway': '192.168.1.1'
        }
        self.results = []
        self.latency_history = {host: deque(maxlen=100) for host in self.hosts}

    def ping_host(self, host, ip):
        """Ping a host and return metrics"""
        try:
            result = subprocess.run(
                ['ping', '-c', '5', '-W', '2', ip],
                capture_output=True,
                text=True,
                timeout=15
            )

            output = result.stdout

            # Parse packet loss
            loss_match = re.search(r'(\d+)% packet loss', output)
            packet_loss = float(loss_match.group(1)) if loss_match else 100

            # Parse latency
            latency_match = re.search(r'min/avg/max/[^=]* = ([\d.]+)/([\d.]+)/([\d.]+)', output)

            if latency_match:
                min_lat = float(latency_match.group(1))
                avg_lat = float(latency_match.group(2))
                max_lat = float(latency_match.group(3))

                return {
                    'host': host,
                    'ip': ip,
                    'status': 'UP' if packet_loss < 100 else 'DOWN',
                    'latency_avg': round(avg_lat, 2),
                    'latency_min': round(min_lat, 2),
                    'latency_max': round(max_lat, 2),
                    'packet_loss': packet_loss,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            else:
                return {
                    'host': host,
                    'ip': ip,
                    'status': 'DOWN',
                    'latency_avg': 0,
                    'packet_loss': 100,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }

        except Exception as e:
            return {
                'host': host,
                'ip': ip,
                'status': 'ERROR',
                'error': str(e),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

    def calculate_jitter(self, host):
        """Calculate jitter from latency history"""
        history = list(self.latency_history[host])
        if len(history) < 2:
            return 0

        differences = [abs(history[i] - history[i - 1]) for i in range(1, len(history))]
        return round(sum(differences) / len(differences), 2)

    def check_alerts(self, result):
        """Check if metrics exceed thresholds"""
        alerts = []

        if result['status'] == 'DOWN':
            alerts.append(f"🔴 {result['host']} is DOWN!")
        elif result['packet_loss'] > 10:
            alerts.append(f"⚠️  {result['host']} has {result['packet_loss']}% packet loss")
        elif result['latency_avg'] > 100:
            alerts.append(f"⚠️  {result['host']} has high latency: {result['latency_avg']}ms")

        return alerts

    def display_status(self, results):
        """Display current network status"""
        print(f"\n{'=' * 70}")
        print(f"Network Health Status - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'=' * 70}\n")

        for result in results:
            status_icon = '✅' if result['status'] == 'UP' else '❌'

            print(f"{status_icon} {result['host']} ({result['ip']})")
            print(f"   Status: {result['status']}")

            if result['status'] == 'UP':
                print(f"   Latency: {result['latency_avg']}ms "
                      f"(min: {result['latency_min']}ms, max: {result['latency_max']}ms)")
                print(f"   Packet Loss: {result['packet_loss']}%")

                jitter = self.calculate_jitter(result['host'])
                print(f"   Jitter: {jitter}ms")

            print()

    def save_to_json(self, filename='network_log.json'):
        """Save results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"✓ Saved to {filename}")

    def save_to_csv(self, filename='network_log.csv'):
        """Save results to CSV file"""
        if not self.results:
            return

        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.results[0].keys())
            writer.writeheader()
            writer.writerows(self.results)
        print(f"✓ Saved to {filename}")

    def generate_uptime_report(self):
        """Generate uptime report for all hosts"""
        print(f"\n{'=' * 70}")
        print("UPTIME REPORT")
        print(f"{'=' * 70}\n")

        for host in self.hosts:
            host_results = [r for r in self.results if r['host'] == host]

            if not host_results:
                continue

            total_checks = len(host_results)
            up_checks = sum(1 for r in host_results if r['status'] == 'UP')
            uptime_percent = (up_checks / total_checks) * 100

            avg_latencies = [r['latency_avg'] for r in host_results if r['status'] == 'UP']
            avg_latency = round(sum(avg_latencies) / len(avg_latencies), 2) if avg_latencies else 0

            print(f"{host}:")
            print(f"  Total Checks: {total_checks}")
            print(f"  Uptime: {uptime_percent:.2f}% ({up_checks}/{total_checks})")
            print(f"  Average Latency: {avg_latency}ms")
            print()

    def run_continuous(self, interval=10, duration=300):
        """Run continuous monitoring"""
        print("Starting Network Health Monitor...")
        print(f"Monitoring interval: {interval} seconds")
        print(f"Duration: {duration} seconds")
        print("Press Ctrl+C to stop\n")

        start_time = time.time()

        try:
            while time.time() - start_time < duration:
                current_results = []

                for host, ip in self.hosts.items():
                    result = self.ping_host(host, ip)
                    current_results.append(result)
                    self.results.append(result)

                    # Store latency for jitter calculation
                    if result['status'] == 'UP':
                        self.latency_history[host].append(result['latency_avg'])

                    # Check for alerts
                    alerts = self.check_alerts(result)
                    for alert in alerts:
                        print(alert)

                self.display_status(current_results)

                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n\nMonitoring stopped by user")

        # Generate final reports
        print("\nGenerating reports...")
        self.generate_uptime_report()
        self.save_to_json()
        self.save_to_csv()

    def run_single_check(self):
        """Run a single check on all hosts"""
        print("Running single network check...\n")

        results = []
        for host, ip in self.hosts.items():
            result = self.ping_host(host, ip)
            results.append(result)
            self.results.append(result)

            if result['status'] == 'UP':
                self.latency_history[host].append(result['latency_avg'])

        self.display_status(results)


def main():
    monitor = NetworkMonitor()

    print("\n" + "=" * 70)
    print("NETWORK HEALTH MONITOR")
    print("=" * 70)
    print("\n1. Single Check")
    print("2. Continuous Monitoring (5 minutes)")
    print("3. Custom Monitoring")
    print("4. Exit\n")

    choice = input("Select option: ").strip()

    if choice == '1':
        monitor.run_single_check()

    elif choice == '2':
        monitor.run_continuous(interval=10, duration=300)

    elif choice == '3':
        try:
            interval = int(input("Enter check interval (seconds): "))
            duration = int(input("Enter total duration (seconds): "))
            monitor.run_continuous(interval=interval, duration=duration)
        except ValueError:
            print("Invalid input!")

    elif choice == '4':
        print("Goodbye!")

    else:
        print("Invalid option!")


if __name__ == '__main__':
    main()