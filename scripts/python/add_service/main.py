import os
from dotenv import load_dotenv

from parser import parse_arguments
from output import print_status
from validation import is_valid_input, validate_env, validate_uptime_monitor, validate_pihole_dns_records
from uptime_kuma import (
    connect_to_uptime_kuma,
    get_uptime_monitors,
    build_monitor_url,
    add_uptime_monitor,
    disconnect_uptime_kuma
)

from pihole import (
    connect_to_pihole,
    disconnect_from_pihole,
    fetch_dns_records,
    build_dns_records,
    build_dns_hostname,
    add_local_dns_record
)


load_dotenv()

def main():

    """
    Steuert den Programmablauf: validiert Eingaben und Umgebungsvariablen,
    stellt die benötigten API-Verbindungen her, prüft bestehende Ressourcen
    und erstellt neue Einträge in Uptime Kuma und Pi-hole.
    """
    args = parse_arguments()

    if args is None:
        print("Keine Eingabe")
        return 

    if is_valid_input(args) is None:
        print("Fehler: Keine Gültige Eingabe")
        return

    if not validate_env():
        return   

    print_status(args)


    # TODO: os.getenv() Aufrufe in load_env_config() auslagern,
    # um Duplikation mit validate_env() zu vermeiden (Single Responsibility)

    url_kuma = os.getenv("KUMA_URL")
    target_ip = os.getenv("TARGET_IP")
    username_kuma = os.getenv("KUMA_USERNAME")
    password_kuma = os.getenv("KUMA_PASSWORD")

    pihole_api_url = os.getenv("PIHOLE_API_URL")
    pihole_password = os.getenv("PIHOLE_PASSWORD")


    # TODO (v0.4.0):
    # Ressourcenverwaltung auf try/finally umstellen, damit alle API-Verbindungen
    # zentral und unabhängig vom Programmablauf sauber beendet werden.


    api = None
    session = None
    
    try:
        # 1. Verbindung
        api = connect_to_uptime_kuma(url_kuma, username_kuma, password_kuma)
        session = connect_to_pihole(pihole_api_url, pihole_password)

        # 2. Prüfen 

        if api is None:
            print("Fehler: Verbindung zu Uptime Kuma fehlgeschlagen")
            return
        
        if session is None:
            print("Fehler: Verbindung zu Pi-Hole Fehlgeschlagen")
            return

        
        # 3. Daten holen 
        monitor_url = build_monitor_url(target_ip, args.port)
        monitors = get_uptime_monitors(api)

        pihole_hostname = build_dns_hostname(args.service)
        raw_dns_records = fetch_dns_records(pihole_api_url,session)

        if raw_dns_records is None:
            print("Fehler DNS Records")
            return        
    
        parsed_records = build_dns_records(raw_dns_records)
        print(f"[DEBUG] {len(parsed_records)} DNS-Einträge geladen")

        # 4. Duplikate prüfen
        if not validate_uptime_monitor(monitors, monitor_url, args.service):
            print("Fehler: Monitor oder URL bereits vorhanden")
            return
        
        if not validate_pihole_dns_records(parsed_records, pihole_hostname):
             print("Fehler: DNS-Eintrag in Pihole bereits vorhanden")
             return
        
        # 5. Erstellen

        if args.dry_run:
            print(f"[DRY-RUN] Würde Uptime-Kuma Monitor '{args.service}' auf {monitor_url} erstellen")
            print(f"[DRY-RUN] Würde local dns record in pi-hole '{pihole_hostname}' auf {target_ip} erstellen")

        else:
            success_add_uptime_monitor = add_uptime_monitor(api, args.service, monitor_url)

            if not success_add_uptime_monitor:
                return
            
            success_add_pihole_local_dns = add_local_dns_record(session,pihole_api_url,target_ip,pihole_hostname)
            if not success_add_pihole_local_dns:
                return
            
            print("Uptime Kuma Monitor erfolgreich erstellt")
            print("Pi-hole local dns record erfolgreich angelegt")


    
    finally:

        #6 Verbindung trennen

        disconnect_uptime_kuma(api)
        disconnect_from_pihole(pihole_api_url, session)


if __name__ == "__main__":
    main()