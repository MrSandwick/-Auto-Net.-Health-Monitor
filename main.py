import speedtest
import ping3
import pandas as pd
import time
from threading import Thread
import smtplib
from datetime import datetime

class NetworkMonitor:
    def __init__(self):
        self.log_file = "network_log.csv"
        self.servers = ["google.com", "8.8.8.8", "192.168.1.1"]

    def ping_test(self, server):
        latency = ping3.ping(server, timeout=2)
        return "Success" if latency else "Failed"

    def speed_test(self):
        st = speedtest.Speedtest()
        st.download()
        st.upload()
        return st.results.dict()

    def log_data(self, data):
        df = pd.DataFrame([data])
        df.to_csv(self.log_file, mode='a', header=False, index=False)

    def send_alert(self, message):
        # Configure your email (Gmail example)
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("your_email@gmail.com", "your_password")
        server.sendmail("your_email@gmail.com", "admin@example.com", message)
        server.quit()

    def run_monitor(self):
        while True:
            results = {"Timestamp": datetime.now()}
            
            # Ping all servers
            for server in self.servers:
                results[f"Ping_{server}"] = self.ping_test(server)
            
            # Speed test (every 10 mins to avoid API limits)
            if time.localtime().tm_min % 10 == 0:
                speed_data = self.speed_test()
                results["Download_Mbps"] = speed_data["download"] / 1_000_000
                results["Upload_Mbps"] = speed_data["upload"] / 1_000_000
            
            self.log_data(results)
            print(f"Logged: {results}")
            time.sleep(60)  # Check every minute

monitor = NetworkMonitor()
monitor.run_monitor()