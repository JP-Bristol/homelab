import string
import logging

from output import print_error

logger = logging.getLogger(__name__)


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
    
    for service, fields in config.items():
        for field_name in fields:
            if not fields[field_name]:
                print_error(logger, f"{service}.{field_name} ist nicht gesetzt")
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