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


def validate_env(config):
    """Prüft, ob alle benötigten Umgebungsvariablen gesetzt sind."""
    if not config["kuma"]["url"]:
        print("Fehler: KUMA_URL ist nicht gesetzt")
        return False

    if not config["network"]["target_ip"]:
        print("Fehler: TARGET_IP ist nicht gesetzt")
        return False

    if not config["kuma"]["username"]:
        print("Fehler: KUMA_USERNAME ist nicht gesetzt")
        return False

    if not config["kuma"]["password"]:
        print("Fehler: KUMA_PASSWORD ist nicht gesetzt")
        return False
    
    if not config["pihole"]["api_url"]:
        print("Fehler: PIHOLE_API_URL ist nicht gesetzt")
        return False

    if not config["pihole"]["password"]:
        print("Fehler: PIHOLE_PASSWORD ist nicht gesetzt")
        return False
    
    return True

def validate_uptime_monitor(monitors, monitor_url, monitor_name):
    """Prüft, ob URL oder Name bereits als Monitor existieren."""
    if any(monitor_url == m['url'] for m in monitors):
        return False

    if any(monitor_name.lower() == m['name'].lower() for m in monitors):
        return False
    
    return True


def validate_pihole_dns_records(records,service_name):

    """Prüft, ob der Hostname bereits in den Pi-hole DNS-Einträgen vorhanden ist."""

    if any(service_name.lower() == r['hostname'].lower() for r in records):
        return False
    return True