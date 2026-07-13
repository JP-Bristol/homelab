from uptime_kuma_api import UptimeKumaApi, MonitorType

def connect_to_uptime_kuma(url, username, password):
    """Baut die Verbindung zur Uptime Kuma API auf und meldet sich an."""
    try:
        api = UptimeKumaApi(str(url))
        api.login(str(username), str(password))
        print("Verbindung erfolgreich")
        return api
    except Exception as e:
        print(f" Verbindung fehlgeschlagen: {e}")
        return None

def get_uptime_monitors(api):
    """Gibt alle aktuell vorhandenen Uptime Kuma Monitore zurück."""
    return api.get_monitors()


def build_monitor_url(target_ip, port):
    """Baut aus Ziel-IP und Port die vollständige Monitor-URL."""
    monitor_url = f"http://{target_ip}:{port}"
    return monitor_url


def add_uptime_monitor(api, monitor_name, monitor_url):
    """Erstellt einen neuen HTTP-Monitor in Uptime Kuma."""
    try:
        api.add_monitor(
            type=MonitorType.HTTP,
            name=monitor_name,
            url=monitor_url,
        )
        return True

    except Exception as e:
        print(f"Monitor konnte nicht erstellt werden: {e}")
        return False

def disconnect_uptime_kuma(api):
    """Trennt die Verbindung zur Uptime Kuma API."""
    if api is None:
        return False
    try:
        api.disconnect()
        print("Verbindung zu Uptime Kuma getrennt")
        return True
    except Exception as e:
        print(f"Verbindung konnte nicht getrennt werden: {e}")
        return False