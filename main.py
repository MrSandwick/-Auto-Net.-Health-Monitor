import speedtest
import ping3
import pandas as pd
import time
import os
import smtplib
import json
import csv
from datetime import datetime

class NetworkMonitor:
    def __init__(self):
        self.servers = ["google.com", "8.8.8.8", "192.168.1.1"]
        self.email_config = {
            "sender": "your_email@gmail.com",
            "password": "your_app_password",
            "receiver": "admin@example.com"
        }
        self.log_file = None
        self.save_data = None
        self.set_output_format()

    def set_output_format(self):
        """Let user choose between JSON or CSV output format"""
        print("\n" + "="*40)
        print("NETWORK MONITOR CONFIGURATION".center(40))
        print("="*40)
        
        while True:
            choice = input("\nChoose output format:\n1. JSON (recommended)\n2. CSV\n\nEnter choice (1/2): ").strip()
            
            if choice == "1":
                self.log_file = "network_log.json"
                self.save_data = self.save_to_json
                print(f"\n✓ Selected JSON format. New log will be created at {self.log_file}")
                break
            elif choice == "2":
                self.log_file = "network_log.csv"
                self.save_data = self.save_to_csv
                print(f"\n✓ Selected CSV format. New log will be created at {self.log_file}")
                break
            else:
                print("\n⚠ Invalid input. Please enter 1 or 2")

    def save_to_json(self, data):
        """Save data to JSON file with proper formatting"""
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    existing_data = json.load(f)
            else:
                existing_data = []
            
            existing_data.append(data)
            
            with open(self.log_file, 'w') as f:
                json.dump(existing_data, f, indent=2)
                
        except Exception as e:
            print(f"\n⚠ Error saving JSON: {e}")

    def save_to_csv(self, data):
        """Save data to CSV file with headers"""
        try:
            file_exists = os.path.exists(self.log_file)
            with open(self.log_file, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=data.keys())
                if not file_exists:
                    writer.writeheader()
                writer.writerow(data)
        except Exception as e:
            print(f"\n⚠ Error saving CSV: {e}")

    def ping_test(self, server):
        """Test server connectivity with timeout"""
        try:
            latency = ping3.ping(server, timeout=2)
            return "Success" if latency else "Failed"
        except Exception as e:
            print(f"\n⚠ Ping error ({server}): {e}")
            return "Error"

    def speed_test(self):
        """Run speedtest and return results"""
        try:
            print("\nRunning speed test...")
            st = speedtest.Speedtest()
            st.download()
            st.upload()
            return st.results.dict()
        except Exception as e:
            print(f"\n⚠ Speedtest error: {e}")
            return None

    def send_alert(self, message):
        """Send email notification on failures"""
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.email_config["sender"], self.email_config["password"])
            server.sendmail(
                self.email_config["sender"],
                self.email_config["receiver"],
                f"Subject: Network Alert\n\n{message}"
            )
            server.quit()
            print("\n✓ Alert email sent!")
        except Exception as e:
            print(f"\n⚠ Email error: {e}")

    def analyze_logs(self):
        """Analyze and display log data"""
        if not os.path.exists(self.log_file):
            print("\n⚠ No log file found - no data collected yet")
            return

        try:
            if self.log_file.endswith('.json'):
                with open(self.log_file, 'r') as f:
                    data = json.load(f)
                    df = pd.DataFrame(data)
            else:
                df = pd.read_csv(self.log_file)

            print("\n" + "="*40)
            print("NETWORK REPORT".center(40))
            print("="*40)
            
            print(f"\nTotal entries: {len(df)}")
            
            if 'Download_Mbps' in df.columns:
                print(f"Average download speed: {df['Download_Mbps'].mean():.2f} Mbps")
            
            if 'Ping_google.com' in df.columns:
                failed_pings = df[df['Ping_google.com'] == 'Failed']
                print(f"Google ping failures: {len(failed_pings)}")
                
        except Exception as e:
            print(f"\n⚠ Error analyzing logs: {e}")

    def run_monitor(self, interval_minutes=1):
        """Main monitoring loop"""
        print("\n" + "="*40)
        print("NETWORK MONITOR ACTIVE".center(40))
        print("="*40)
        print(f"\nLogging to: {self.log_file}")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                # Run ping tests
                results = {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    **{f"Ping_{server}": self.ping_test(server) for server in self.servers}
                }
                
                # Run speed test every 10 minutes
                if int(datetime.now().strftime("%M")) % 10 == 0:
                    speed_data = self.speed_test()
                    if speed_data:
                        results.update({
                            "Download_Mbps": round(speed_data["download"] / 1_000_000, 2),
                            "Upload_Mbps": round(speed_data["upload"] / 1_000_000, 2)
                        })
                
                # Save results
                self.save_data(results)
                print(f"\nLogged: {results}")

                # Send alert if any ping failed
                if "Failed" in results.values():
                    self.send_alert(f"Network failure detected at {results['Timestamp']}")

                # Wait for next interval
                time.sleep(interval_minutes * 60)

        except KeyboardInterrupt:
            if os.path.exists(self.log_file) and os.path.getsize(self.log_file) > 0:
                self.analyze_logs()
            print("\n" + "="*40)
            print("MONITOR STOPPED".center(40))
            print("="*40)

if __name__ == "__main__":
    monitor = NetworkMonitor()
    monitor.run_monitor()