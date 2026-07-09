from uptime_kuma_api import UptimeKumaApi, MonitorType
from dotenv import load_dotenv
from datetime import datetime
import argparse
import sys
import string
import os


load_dotenv()


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

def get_uptime_monitor(api):
    """Gibt alle aktuell vorhandenen Uptime Kuma Monitore zurück."""
    return api.get_monitors()

def disconnect_uptime_kuma(api):
    """Trennt die Verbindung zur Uptime Kuma API."""
    try:
        api.disconnect()
        print("Verbindung zu Uptime Kuma getrennt")
        return True
    except Exception as e:
        print(f"Verbindung konnte nicht getrennt werden: {e}")
        return False

def parse_arguments():

    """Liest und verarbeitet die Kommandozeilenargumente."""

    try:
        parser = argparse.ArgumentParser(description="Automatisiert das Einrichten neuer Homelab-Services.")
        # Argument für Servicename
        parser.add_argument(
            '--service', 
            type=str, 
            required=True, 
            help='Service-Name'
        )
    
        # Argument für Port
        parser.add_argument(
            '--port', 
            type=int, 
            required=True, 
            help='Service-Port'
        )
        return parser.parse_args()

    except SystemExit:
        if "--help" not in sys.argv and "-h" not in sys.argv:
            print("Fehler: Das Argument --service und --port wird benötigt")
        return None

def build_monitor_url(target_ip, port):
    """Baut aus Ziel-IP und Port die vollständige Monitor-URL."""
    monitor_url = f"{target_ip}:{port}"
    return monitor_url

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

def print_status(args):

    """Gibt eine Zusammenfassung der geplanten Einrichtungsschritte aus."""

    print("=" * 50)
    print(f"  🏠 Homelab Add Service")
    print(f"  📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    print(f"-Service-Name: {args.service}")
    print(f"-Service-Port: {args.port}""\n")

    print(f"✓ Eingaben validiert""\n")

    print(f"Geplante Schritte:")
    print(f" - Uptime Kuma Monitor hinzufügen")
    print(f" - Pihole lokalen DNS-Eintrag anlegen")
    print(f" - Nginx Proxy Manager Proxy Host erstellen")
    print(f" - ufw Port freigeben")
    print(f" - Service-Log schreiben""\n")

    print(f"v0.1: Simulation beendet.""\n")
    print("=" * 50)


 

def main():

    """
    Steuert den Programmablauf: validiert Eingaben und .env,
    verbindet sich mit Uptime Kuma, prüft auf Duplikate
    und erstellt den Monitor.
    """
    
    args = parse_arguments()
    
    if args is None:
        print("Keine Eingabe")
        return
    
    input_test = is_valid_input(args)
        
    if input_test is None:
        print("Fehler")
        return

    if not validate_env():
        print("Fehler")
        return

    print_status(args)

    url_kuma = os.getenv("KUMA_URL")
    target_ip = os.getenv("TARGET_IP")
    username_kuma = os.getenv("KUMA_USERNAME")
    password_kuma = os.getenv("KUMA_PASSWORD")


    api = connect_to_uptime_kuma(url_kuma, username_kuma, password_kuma)

    if api is None:
        print("Fehler: Verbindung zu Uptime Kuma fehlgeschlagen")
        return

    monitor_url = build_monitor_url(target_ip, args.port)
    monitors = get_uptime_monitor(api)

    if not validate_uptime_monitor(monitors, monitor_url, args.service):
        print("Fehler: Monitor oder Port bereits vorhanden/belegt")
        disconnect_uptime_kuma(api)
        return

    success = add_uptime_monitor(api, args.service, monitor_url)

    if not success:
        disconnect_uptime_kuma(api)
        return

    print("Monitor erfolgreich erstellt")

    disconnect_uptime_kuma(api)


if __name__ == "__main__":
    main()
