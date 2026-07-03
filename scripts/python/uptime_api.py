from dotenv import load_dotenv
from datetime import datetime
import os
import requests

load_dotenv()
ip = os.getenv("HOMELAB_IP")

# Monitore mit Namen laden
#url_status = f"http://{ip}:3001/api/status-page/homelab"
#monitors_data = requests.get(url_status).json()
#monitors = {m['id']: m['name'] for m in monitors_data['publicGroupList'][0]['monitorList']}

try:
    url_status = f"http://{ip}:3001/api/status-page/homelab"
    response = requests.get(url_status, timeout=5)
    response.raise_for_status()
    monitors_data = response.json()
except requests.exceptions.ConnectionError:
    print("❌ Uptime Kuma nicht erreichbar!")
    exit(1)
except requests.exceptions.Timeout:
    print("❌ Timeout — Uptime Kuma antwortet nicht!")
    exit(1)

monitors = {m['id']: m['name'] for m in monitors_data['publicGroupList'][0]['monitorList']}

# Heartbeats laden
url_heartbeat = f"http://{ip}:3001/api/status-page/heartbeat/homelab"
heartbeat_data = requests.get(url_heartbeat).json()

for monitor_id, beats in heartbeat_data['heartbeatList'].items():
    if beats:
        latest = beats[-1]
        status = "✅ UP" if latest['status'] == 1 else "❌ DOWN"
        name = monitors.get(int(monitor_id), f"Monitor {monitor_id}")
        
        # Timestamp
        time = latest.get('time', 'unbekannt')
        
        # Uptime
        uptime = heartbeat_data['uptimeList'].get(f"{monitor_id}_24", 0)
        uptime_pct = round(uptime * 100, 2)
        
        print(f"  {status} {name} | Uptime: {uptime_pct}% | Letzter Check: {time}")
        
        
