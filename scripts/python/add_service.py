from uptime_kuma_api import UptimeKumaApi, MonitorType
from dotenv import load_dotenv
from datetime import datetime
import argparse
import sys
import string
import os


load_dotenv()


def connect_to_uptime_kuma(url, username, password):
    try:
        api = UptimeKumaApi(str(url))
        api.login(str(username), str(password))
        print("Verbindung erfolgreich")
        return api
    except Exception as e:
        print(f" Verbindung fehlgeschlagen: {e}")
        return None

def add_uptime_monitor(api, args, ip):
    try:
        api.add_monitor(
            type=MonitorType.HTTP,
            name=f"{args.service}",
            url=f"{ip}:{args.port}",
        )
        return True

    except Exception as e:
        print(f"Monitor konnte nicht erstellt werden: {e}")
        return False

def disconnect_uptime_kuma(api):
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

def is_valid_input(args):

    """Prüft Service-Name und Port auf gültige Eingaben."""

    allowed = set(string.ascii_letters + string.digits + "_-")
    if all(char in allowed for char in args.service) == False:
        return None

    if args.port not in range(1,65536):
        return None
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

    """Steuert den Programmablauf."""
    
    args = parse_arguments()
    
    if args is None:
        print("Keine Eingabe")
        exit()
    
    input_test = is_valid_input(args)
        
    if input_test is None:
        print("Fehler")
        exit()

    print_status(args)

    url_kuma = os.getenv("KUMA_URL")
    target_ip = os.getenv("TARGET_IP")
    username_kuma = os.getenv("KUMA_USERNAME")
    password_kuma = os.getenv("KUMA_PASSWORD")

    api = connect_to_uptime_kuma(url_kuma, username_kuma, password_kuma)

    if api is None:
        print("Fehler: Verbindung zu Uptime Kuma fehlgeschlagen")
        exit()

    success = add_uptime_monitor(api, args, target_ip)

    if not success:
        disconnect_uptime_kuma(api)
        return

    print("Monitor erfolgreich erstellt")

    disconnect_uptime_kuma(api)


if __name__ == "__main__":
    main()
