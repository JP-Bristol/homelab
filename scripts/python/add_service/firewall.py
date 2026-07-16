import logging
import subprocess

from output import print_ok, print_error

logger = logging.getLogger(__name__)

def open_service_port(port):

    """ Öffnet einen Port über ufw (Uncomplicated Firewall). """

    try:
        result = subprocess.run(["sudo", "ufw", "allow", f"{port}/tcp"], capture_output=True, text=True)
        if result.returncode == 0:
            print_ok(logger, f"UFW-Regel für Port {port}/tcp erfolgreich hinzugefügt.")
            return True
        else:
            print_error(logger, f"UFW-Regel für Port {port}/tcp konnte nicht hinzugefügt werden: {result.stderr}")
            return False

    except FileNotFoundError as err:
        print_error(logger, f"Der UFW-Befehl wurde nicht gefunden: {err}.")
        return False

    except Exception as err:
        print_error(logger,f"Unbekannter Fehler: {err}")
        return False        
