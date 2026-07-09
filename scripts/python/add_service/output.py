from datetime import datetime

def print_status(args):
    """Gibt eine Zusammenfassung der Eingaben aus."""

    print("=" * 50)
    print(f"  🏠 Homelab Add Service")
    print(f"  📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    print(f"-Service-Name: {args.service}")
    print(f"-Service-Port: {args.port}\n")

    if args.dry_run:
        print("Modus: Dry-Run (keine Änderungen werden vorgenommen)\n")

    print("✓ Eingaben validiert\n")
    print("=" * 50)