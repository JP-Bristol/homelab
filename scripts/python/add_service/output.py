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


def print_ok(logger,message):
    logger.info(f"[OK] {message}")

def print_info(logger,message):
    logger.info(f"[INFO] {message}")

def print_warning(logger,message):
    logger.warning(f"[WARNING] {message}")

def print_error(logger,message):
    logger.error(f"[ERROR] {message}")

def print_debug(logger,message):
    logger.debug(f"[DEBUG] {message}")
