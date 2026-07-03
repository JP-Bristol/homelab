from dotenv import load_dotenv
import os
import requests

load_dotenv()
ip = os.getenv("HOMELAB_IP")

# Monitore mit Namen laden
url_status = f"http://{ip}:3001/api/status-page/homelab"
monitors_data = requests.get(url_status).json()
monitors = {m['id']: m['name'] for m in monitors_data['publicGroupList'][0]['monitorList']}

# Heartbeats laden
url_heartbeat = f"http://{ip}:3001/api/status-page/heartbeat/homelab"
heartbeat_data = requests.get(url_heartbeat).json()

print(f"\n=== Homelab Status ===")
for monitor_id, beats in heartbeat_data['heartbeatList'].items():
    if beats:
        latest = beats[-1]
        status = "✅ UP" if latest['status'] == 1 else "❌ DOWN"
        name = monitors.get(int(monitor_id), f"Monitor {monitor_id}")
        print(f"{name} {status}")

        
        
