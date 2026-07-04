from uptime_kuma_api import UptimeKumaApi
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

def get_kuma_api():
    """Verbindung zu Uptime Kuma aufbauen und einloggen."""
    ip = os.getenv("HOMELAB_IP")
    user_kuma = os.getenv("USER_KUMA")
    password_kuma = os.getenv("PASSWORD_KUMA")
    try:
        api = UptimeKumaApi(f"http://{ip}:3001")
        api.login(str(user_kuma), str(password_kuma))
        return api
    except Exception as e:
        print(f"❌ Verbindung fehlgeschlagen: {e}")
        return None

def fetch_monitors(api):
    """Alle konfigurierten Monitore laden."""
    return api.get_monitors()

def fetch_uptime_stats(api):
    """Uptime-Statistiken laden."""
    return api.uptime()

def fetch_monitors_heartbeats(api):
    """Letzte Heartbeats aller Monitore laden."""
    return api.get_heartbeats()

def get_monitor_summary(monitor, uptime_stats, heartbeats):
    """Relevante Daten eines Monitors zusammenfassen."""
    m_id = monitor.get('id')
    stats = uptime_stats.get(m_id, {})
    status_code = monitor.get('active', False)
    
    # Letzten Heartbeat holen, Fallback wenn leer
    monitor_beats = heartbeats.get(m_id, [])
    latest_beat = monitor_beats[-1] if monitor_beats else {}

    # Status aus dem Heartbeat holen — nicht aus monitor.active!
    beat_status = latest_beat.get('status')
    is_up = beat_status.value == 1

    return {
        "name": monitor.get('name', 'Unbekannt'),
        "uptime_24h": stats.get(24, 0) * 100,
        "status": "✅ UP" if is_up else "❌ DOWN",
        "time": latest_beat.get('time', 'unbekannt')
    }

def print_status(monitors, uptime, heartbeat):
    """Status aller Monitore formatiert ausgeben."""
    count_up = sum(1 for m in monitors if m.get('active') == True)
    count_down = len(monitors) - count_up
    
    print("=" * 135)
    print(f"  🏠 Homelab Status Check")
    print(f"  📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 135)
    
    for m in monitors:
        data = get_monitor_summary(m, uptime, heartbeat)
        print(f"Service: {data['name']:<20} Uptime_24h: {data['uptime_24h']:<20} | Status: {data['status']:<20} | Letzter Check: {data['time']:<20}")
    
    print("=" * 135)
    print(f"  📊 Zusammenfassung: {count_up} UP | {count_down} DOWN")
    print(f"  ✅ Alle {len(monitors)} Services geprüft")
    print("=" * 135)

def main():
    """Hauptfunktion."""
    api = get_kuma_api()
    if api is None:
        exit()
    
    monitors = fetch_monitors(api)
    uptime = fetch_uptime_stats(api)
    heartbeats = fetch_monitors_heartbeats(api)
    
    print_status(monitors, uptime, heartbeats)
    api.disconnect()

if __name__ == "__main__":
    main()