from datetime import datetime

def print_status(args):
    """Gibt eine Zusammenfassung der Eingaben aus."""

    print("=" * 50)
    print(f"  🏠 Homelab Add Service")
    print(f"  📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    print(f"-Service-Name: {args.service}")
    print(f"-Service-Port: {args.port}\n")

    print("✓ Eingaben validiert\n")

    print("Geplante Schritte:")
    print(" - Uptime Kuma Monitor hinzufügen")
    print(" - Pihole lokalen DNS-Eintrag anlegen")
    print(" - Nginx Proxy Manager Proxy Host erstellen")
    print(" - ufw Port freigeben")
    print(" - Service-Log schreiben\n")

    print("=" * 50)