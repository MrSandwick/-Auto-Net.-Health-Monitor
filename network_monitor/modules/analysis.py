import pandas as pd

class LogAnalyzer:
    @staticmethod
    def analyze(data, file_type):
        if not data:
            return "No data available for analysis"
        
        if file_type == "json":
            df = pd.DataFrame(data)
        else:
            df = data
            
        report = {
            "total_entries": len(df),
            "avg_download": None,
            "failure_count": None
        }
        
        if 'Download_Mbps' in df.columns:
            report["avg_download"] = f"{df['Download_Mbps'].mean():.2f} Mbps"
            
        if 'Ping_google.com' in df.columns:
            report["failure_count"] = len(df[df['Ping_google.com'] == 'Failed'])
            
        return report