import speedtest
import ping3
import pandas as pd
import time
import os
import smtplib
import json
from datetime import datetime
from threading import Thread

class NetworkMonitor:
    def __init__(self):
        self.log_file = "network_log.json"  # Changed to JSON
        self.servers = ["google.com", "8.8.8.8", "192.168.1.1"]
        self.email_config = {
            "sender": "your_email@gmail.com",
            "password": "your_app_password",
            "receiver": "admin@example.com"
        }

    def ping_test(self, server):
        try:
            latency = ping3.ping(server, timeout=2)
            return "Success" if latency else "Failed"
        except Exception as e:
            print(f"Ping error ({server}): {e}")
            return "Error"

    def speed_test(self):
        try:
            st = speedtest.Speedtest()
            st.download()
            st.upload()
            return st.results.dict()
        except Exception as e:
            print(f"Speedtest error: {e}")
            return None

    def log_data(self, data):
        """Save data to JSON file, appending to existing array"""
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
            print(f"Error saving JSON: {e}")

    def send_alert(self, message):
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
            print("Alert email sent!")
        except Exception as e:
            print(f"Email error: {e}")

    def analyze_logs(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                data = json.load(f)
                df = pd.DataFrame(data)
                print("\n--- Network Report ---")
                print(f"Total entries: {len(df)}")
                print(f"Average download: {df['Download_Mbps'].mean():.2f} Mbps" if 'Download_Mbps' in df.columns else "No speed tests recorded")
                if 'Ping_google.com' in df.columns:
                    failed_pings = df[df['Ping_google.com'] == 'Failed']
                    print(f"Google ping failed {len(failed_pings)} times")
        else:
            print("No log file found.")

    def run_monitor(self, interval_minutes=1):
        print("Starting Network Monitor (Ctrl+C to stop)...")
        try:
            while True:
                results = {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    **{f"Ping_{server}": self.ping_test(server) for server in self.servers}
                }
                
                if int(datetime.now().strftime("%M")) % 10 == 0:
                    speed_data = self.speed_test()
                    if speed_data:
                        results.update({
                            "Download_Mbps": round(speed_data["download"] / 1_000_000, 2),
                            "Upload_Mbps": round(speed_data["upload"] / 1_000_000, 2)
                        })
                
                self.log_data(results)
                print(f"Logged: {results}")

                if "Failed" in results.values():
                    self.send_alert(f"Network failure at {results['Timestamp']}")

                time.sleep(interval_minutes * 60)

        except KeyboardInterrupt:
            self.analyze_logs()
            print("Monitor stopped.")

if __name__ == "__main__":
    monitor = NetworkMonitor()
    monitor.run_monitor()