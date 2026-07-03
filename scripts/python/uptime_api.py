from dotenv import load_dotenv
from datetime import datetime
import os
import requests

load_dotenv()
ip = os.getenv("HOMELAB_IP")


def get_monitors(ip):
    """Lädt alle Monitore von der Uptime Kuma Status Page."""
    try:
        url_status = f"http://{ip}:3001/api/status-page/homelab"
        response = requests.get(url_status, timeout=5)
        response.raise_for_status()
        monitors_data = response.json()
        return monitors_data
    except requests.exceptions.ConnectionError:
        # Uptime Kuma nicht erreichbar
        print("❌ Uptime Kuma nicht erreichbar!")
        return None
    except requests.exceptions.Timeout:
        # Anfrage hat zu lange gedauert
        print("❌ Timeout!")
        return None

def get_heartbeats(ip):
    """Lädt Heartbeat-Daten für alle Monitore."""
    try:
        url_heartbeat = f"http://{ip}:3001/api/status-page/heartbeat/homelab"
        heartbeat_data = requests.get(url_heartbeat, timeout=5).json()
        return heartbeat_data
    except requests.exceptions.ConnectionError:
        # Uptime Kuma nicht erreichbar
        print("❌ Uptime Kuma nicht erreichbar!")
        return None
    except requests.exceptions.Timeout:
        # Anfrage hat zu lange gedauert
        print("❌ Timeout — Uptime Kuma antwortet nicht!")  # ← eine Einrückung weniger
        return None


def print_status(monitors_data, heartbeat_data):
    """Gibt den Status aller Monitore formatiert aus."""

    # Header
    print("=" * 50)
    print(f"  🏠 Homelab Status Check")
    print(f"  📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Monitor-ID zu Name Mapping erstellen
    monitors = {m['id']: m['name'] for m in monitors_data['publicGroupList'][0]['monitorList']}
    
    for monitor_id, beats in heartbeat_data['heartbeatList'].items():
        if beats:
            # Letzten Heartbeat nehmen
            latest = beats[-1]
            
            # Status bestimmen
            status = "✅ UP" if latest['status'] == 1 else "❌ DOWN"
            name = monitors.get(int(monitor_id), f"Monitor {monitor_id}")
            
            # Zeitstempel und Uptime
            time = latest.get('time', 'unbekannt')
            uptime = heartbeat_data['uptimeList'].get(f"{monitor_id}_24", 0)
            uptime_pct = round(uptime * 100, 2)
            
            print(f"  {status} {name} | Uptime: {uptime_pct}% | Letzter Check: {time}")

    # Footer

    print("=" * 50)
    print(f"  ✅ Alle {len(heartbeat_data['heartbeatList'])} Services geprüft")
    print("=" * 50)


def main():
    """Hauptfunktion — koordiniert alle anderen Funktionen."""
    monitors_data = get_monitors(ip)
    
    if monitors_data is None:
        exit(1)
    
    heartbeat_data = get_heartbeats(ip)
    
    if heartbeat_data is None:
        exit(1)
    
    print_status(monitors_data, heartbeat_data)

if __name__ == "__main__":
    main()
        
        
