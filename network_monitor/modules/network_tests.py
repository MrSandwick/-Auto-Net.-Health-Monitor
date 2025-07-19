import ping3
import speedtest
from datetime import datetime

class NetworkTester:
    @staticmethod
    def ping_test(server):
        try:
            latency = ping3.ping(server, timeout=2)
            return "Success" if latency else "Failed"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @staticmethod
    def speed_test():
        try:
            st = speedtest.Speedtest()
            st.download()
            st.upload()
            return {
                "download": st.results.download,
                "upload": st.results.upload,
                "ping": st.results.ping
            }
        except Exception as e:
            return None