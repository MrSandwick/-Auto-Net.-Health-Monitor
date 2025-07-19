from datetime import datetime

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def format_speedtest_results(results):
    if not results:
        return None
    return {
        "Download_Mbps": round(results["download"] / 1_000_000, 2),
        "Upload_Mbps": round(results["upload"] / 1_000_000, 2)
    }