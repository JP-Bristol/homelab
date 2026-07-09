import string
import os

def is_valid_input(args):

    """Prüft Service-Name und Port auf gültige Eingaben."""

    allowed = set(string.ascii_letters + string.digits + "_-")
    if not all(char in allowed for char in args.service):
        return None

    if args.port not in range(1,65536):
        return None
    return True


def validate_env():
    """Prüft, ob alle benötigten Umgebungsvariablen gesetzt sind."""
    if not os.getenv("KUMA_URL"):
        print("Fehler: KUMA_URL ist nich gesetzt")
        return False

    if not os.getenv("TARGET_IP"):
        print("Fehler: TARGET_IP ist nicht gesetzt")
        return False

    if not os.getenv("KUMA_USERNAME"):
        print("Fehler: KUMA_USERNAME ist nicht gesetzt")
        return False

    if not os.getenv("KUMA_PASSWORD"):
        print("Fehler: KUMA_PASSWORD ist nicht gesetzt")
        return False
    
    return True

def validate_uptime_monitor(monitors, monitor_url, monitor_name):
    """Prüft, ob URL oder Name bereits als Monitor existieren."""
    if any(monitor_url == m['url'] for m in monitors):
        return False

    if any(monitor_name.lower() == m['name'].lower() for m in monitors):
        return False
    
    return True
