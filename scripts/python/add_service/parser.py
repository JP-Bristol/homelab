import argparse
import sys

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