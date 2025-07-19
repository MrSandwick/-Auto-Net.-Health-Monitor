import time
import os
from config import settings
from modules.file_handler import FileHandler
from modules.network_tests import NetworkTester
from modules.alert_system import AlertSystem
from modules.analysis import LogAnalyzer
from utils.helpers import get_timestamp, format_speedtest_results

class NetworkMonitor:
    def __init__(self):
        self.file_type = self._select_file_type()
        self.file_handler = FileHandler(self.file_type)
        self.network_tester = NetworkTester()
        self.alert_system = AlertSystem(settings.EMAIL_CONFIG)
    
    def _select_file_type(self):
        while True:
            print("\nChoose output format:")
            print("1. JSON (recommended)")
            print("2. CSV")
            choice = input("Enter choice (1/2): ").strip()
            
            if choice == "1":
                return "json"
            elif choice == "2":
                return "csv"
            print("Invalid input. Please try again.")
    
    def run(self):
        print(f"\nStarting Network Monitor (Logging to {self.file_handler.log_file})")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                results = self._run_tests()
                self._process_results(results)
                time.sleep(settings.LOG_INTERVAL_MINUTES * 60)
                
        except KeyboardInterrupt:
            self._shutdown()
    
    def _run_tests(self):
        results = {
            "Timestamp": get_timestamp(),
            **{f"Ping_{server}": self.network_tester.ping_test(server) 
               for server in settings.SERVERS}
        }
        
        if int(time.strftime("%M")) % settings.SPEEDTEST_INTERVAL_MINUTES == 0:
            speed_data = format_speedtest_results(self.network_tester.speed_test())
            if speed_data:
                results.update(speed_data)
        
        return results
    
    def _process_results(self, results):
        try:
            self.file_handler.save(results)
            print(f"Logged: {results}")
            
            if "Failed" in results.values():
                self.alert_system.send_alert(
                    f"Network failure at {results['Timestamp']}"
                )
        except Exception as e:
            print(f"Error processing results: {e}")
    
    def _shutdown(self):
        data = self.file_handler.load_data()
        report = LogAnalyzer.analyze(data, self.file_type)
        
        print("\n=== Shutdown Report ===")
        for key, value in report.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        print("\nMonitor stopped.")

if __name__ == "__main__":
    monitor = NetworkMonitor()
    monitor.run()