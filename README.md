# Network Monitor

A Python tool to monitor network health, test speeds, and alert on failures. Perfect for 5G/ISP troubleshooting.

## Features
- ✅ Ping multiple servers (Google, Cloudflare, local router)
- 📊 Speed tests (download/upload) with CSV logging
- 🔔 Email alerts when connections fail
- 📈 Automatic log analysis with Pandas

## Quick Start
1. Install dependencies:
```bash
pip install speedtest-cli ping3 pandas
```

## Configure email (optional):
Edit email_config in network_monitor.py with your Gmail credentials.

## Run:
```bash
python network_monitor.py
```

## Customize
Test Frequency: Change interval_minutes in run_monitor()
Servers: Modify self.servers list
Alerts: Disable by commenting out send_alert() call

## Sample Output
```bash
{
  "Timestamp": "2025-07-18 19:30:00",
  "Ping_google.com": "Success",
  "Download_Mbps": 164.07,
  "Upload_Mbps": 8.47
}
```