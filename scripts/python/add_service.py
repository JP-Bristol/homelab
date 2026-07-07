import argparse
import sys
import string


def parse_arguments():
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
    allowed = set(string.ascii_letters + string.digits + "_-")
    if all(char in allowed for char in args.service) == False:
        return None

    if args.port not in range(1,65536):
        return None
    return True


def print_status(args):
    print("=" * 50)
    print(f"  🏠 Homelab Add Service")
    print("=" * 50)

    print(f"-Service-Name: {args.service}")
    print(f"-Service-Port: {args.port}""\n")

    print(f"✓ Eingaben validiert""\n")

    print(f"Geplante Schritte:")
    print(f" - Uptime Kuma Monitor würde erstellt")
    print(f" - DNS-Eintrag würde erstellt")
    print(f" - Proxy Host würde erstellt")
    print(f" - UFW-Port würde freigegeben")
    print(f" - Service-Log würde geschriebe""\n")

    print(f"v0.1: Simulation beendet.""\n")
    print("=" * 50)


 

def main():
    args = parse_arguments()
    
    if args is None:
        print("Keine Eingabe")
        exit()
    
    input_test = is_valid_input(args)
        
    if input_test is None:
        print("Fehler")
        exit()

    print_status(args)


if __name__ == "__main__":
    main()
