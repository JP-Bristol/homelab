import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()


def read_log(pfad):
    """Log-Datei einlesen und als String zurückgeben."""
    try:
        with open(pfad, "r") as f:
            inhalt = f.read()
        return inhalt
    except Exception as e:
        print(f"Datei nicht geöffnet: {e}")
        return None

def get_last_backup(inhalt):
    """Letzten Backup-Eintrag aus dem Log extrahieren."""
    eintraege = inhalt.split("Backup startet:")

    if len(eintraege) < 2:
        print("Keine Backup-Einträge gefunden")
        return None
    return eintraege[-1]

def get_backup_date(letzter):
    """Datum des letzten Backups extrahieren."""
    
    return letzter.split("\n")[0].strip()

def get_backup_status(letzter):
    """Prüfen ob das Backup erfolgreich abgeschlossen wurde."""
    if "Backup fertig" in letzter:
        return True
    else:
        return False


def get_backup_errors(letzter):
    """Bekannte und unbekannte Permission-Fehler aus dem Log zählen."""
    bekannte_fehler = ["logrotate", "letsencrypt"]
    unbekannte_fehler_count = 0
    unbekannte_fehler = []
    
    
    for zeile in letzter.split("\n"):
        if "Permission denied" in zeile:
            if not any(b in zeile for b in bekannte_fehler):
                unbekannte_fehler_count += 1
                unbekannte_fehler.append(zeile)

    bekannte_fehler_count = letzter.count("Permission denied") - unbekannte_fehler_count
    return bekannte_fehler_count, unbekannte_fehler_count, unbekannte_fehler

            

def get_backed_up_services(letzter):
    """Liste der gesicherten Services aus dem Log extrahieren."""
    gesicherte_service = []
    for zeile in letzter.split("\n"):
        if "created directory" in zeile:
            gesicherte_service.append(zeile.split('/')[-1])
    return gesicherte_service


def get_backup_dirs(backup_pfad):
    """Anzahl vorhandener Backup-Verzeichnisse zählen."""
    dirs = []
    for d in os.listdir(backup_pfad):
        try:
            datetime.strptime(d, "%Y-%m-%d")
            dirs.append(d)
        except ValueError:
            pass  # Kein Datum-Format — überspringen
    return len(dirs)


def print_backup_status(datum, status, services, bekannte_fehler_count, unbekannte_fehler_count,unbekannte_fehler, count_dir):
    """Backup-Status formatiert ausgeben."""
    print("=" * 50)
    print(f"  🏠 Backup Status Check")
    print(f"  📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    print(f"Letztes Backup: {datum}")
    print(f"Status: {'Erfolgreich' if status else 'Fehlgeschlagen'}""\n")
    print("Gesicherte Services:")
    print("\n".join(f"- {s}" for s in services))
    
    print("\n"f"Bekannte Fehler: {bekannte_fehler_count}")
    print(f"Unbekannte Fehler: {unbekannte_fehler_count}""\n")
    if unbekannte_fehler_count > 0: 
        for zeile in unbekannte_fehler:
            print(f" -> {zeile}")

    print(f"Backup-Verzeichnisse: {count_dir} (max. 7 erwartet)")
    print("=" * 50)


   
def main():
    """Hauptfunktion — Backup-Log auswerten und Status ausgeben."""

    pfad = os.getenv("PFAD")
    backup_pfad = os.getenv("BACKUP_PFAD")

    inhalt = read_log(pfad)
    if inhalt is None:
        exit()

    letzter = get_last_backup(inhalt)
    if letzter is None:
        exit()

    datum = get_backup_date(letzter)
    status = get_backup_status(letzter)
    services = get_backed_up_services(letzter)
    count_dir = get_backup_dirs(backup_pfad)
    bekannte_fehler_count, unbekannte_fehler_count, unbekannte_fehler = get_backup_errors(letzter)

    print_backup_status(datum, status, services, bekannte_fehler_count, unbekannte_fehler_count,unbekannte_fehler, count_dir)

if __name__ == "__main__":
    main()


