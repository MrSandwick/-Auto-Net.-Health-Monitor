import json
import csv
import os
from datetime import datetime

class FileHandler:
    def __init__(self, file_type="json"):
        self.file_type = file_type
        self.log_file = f"network_log.{file_type}"
        
    def save(self, data):
        if self.file_type == "json":
            self._save_json(data)
        else:
            self._save_csv(data)
    
    def _save_json(self, data):
        try:
            existing_data = []
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    existing_data = json.load(f)
            
            existing_data.append(data)
            
            with open(self.log_file, 'w') as f:
                json.dump(existing_data, f, indent=2)
        except Exception as e:
            raise Exception(f"JSON save error: {e}")
    
    def _save_csv(self, data):
        try:
            file_exists = os.path.exists(self.log_file)
            with open(self.log_file, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=data.keys())
                if not file_exists:
                    writer.writeheader()
                writer.writerow(data)
        except Exception as e:
            raise Exception(f"CSV save error: {e}")
    
    def load_data(self):
        if not os.path.exists(self.log_file):
            return None
            
        try:
            if self.file_type == "json":
                with open(self.log_file, 'r') as f:
                    return json.load(f)
            else:
                import pandas as pd
                return pd.read_csv(self.log_file)
        except Exception as e:
            raise Exception(f"Data load error: {e}")