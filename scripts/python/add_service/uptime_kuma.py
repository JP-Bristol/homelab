import logging 

from uptime_kuma_api import (
    UptimeKumaApi, 
    MonitorType, 
    Timeout, 
    UptimeKumaException
)
from output import print_ok,print_error

logger = logging.getLogger(__name__)



def connect_to_uptime_kuma(url, username, password):
    """Baut die Verbindung zur Uptime-Kuma-API auf und meldet sich an."""
    try:
        api = UptimeKumaApi(str(url))
        api.login(str(username), str(password))
        print_ok(logger,"Verbindung zu Uptime Kuma erfolgreich")
        return api
    
    except Timeout as err:
        print_error(logger,f"Zeitüberschreitung bei der Verbindung zu Uptime Kuma: {err}")
        return None
    
    except UptimeKumaException as err:
        print_error(logger,f"Verbindung zu Uptime Kuma fehlgeschlagen: {err}")
        return None

    except Exception as err:
        print_error(logger,f"Unbekannter Fehler ({type(err).__name__}): {err}")
        return None

def get_uptime_monitors(api):
    """Gibt alle aktuell vorhandenen Uptime-Kuma-Monitore zurück."""
    try:
        return api.get_monitors()
    
    except Timeout as err:
        print_error(logger,f"Zeitüberschreitung beim Abrufen der Uptime-Kuma-Monitor-Einträge: {err}")
        return None
    
    except UptimeKumaException as err:
        print_error(logger,f"Uptime-Kuma-Monitore konnten nicht abgerufen werden: {err}")
        return None

    except Exception as err:
        print_error(logger,f"Unbekannter Fehler: {err}")
        return None


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
    
    except Timeout as err:
        print_error(logger,f"Zeitüberschreitung beim Übertragen der Uptime-Kuma-Monitor-Einträge: {err}")
        return False
    
    except UptimeKumaException as err:
        print_error(logger,f"Uptime-Kuma-Monitor konnte nicht erstellt werden: {err}")
        return False

    except Exception as err:
        print_error(logger,f"Unbekannter Fehler: {err}")
        return False

def disconnect_uptime_kuma(api):
    """Trennt die Verbindung zur Uptime-Kuma-API."""
    if api is None:
        return False
    try:
        api.disconnect()
        print_ok(logger,"Verbindung zu Uptime Kuma getrennt")
        return True
    
    except Timeout as err:
        print_error(logger,f"Zeitüberschreitung bei der Trennung von Uptime Kuma: {err}")
        return False
    
    except UptimeKumaException as err:
        print_error(logger,f"Uptime-Kuma-Verbindung konnte nicht getrennt werden: {err}")
        return False

    except Exception as err:
        print_error(logger,f"Unbekannter Fehler: {err}")
        return False

    
def parse_monitor_record(monitor):
    return {
        "id": monitor["id"],
        "name": monitor["name"],
        "url": monitor["url"]
    }

def build_monitor_records(monitors):
    return [parse_monitor_record(m) for m in monitors if m["type"] == "http"]