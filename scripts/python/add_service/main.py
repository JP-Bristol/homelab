from parser import parse_arguments
from output import print_status
from validation import is_valid_input, validate_env, validate_uptime_monitor, validate_pihole_dns_records
from uptime_kuma import (
    connect_to_uptime_kuma,
    get_uptime_monitors,
    build_monitor_url,
    add_uptime_monitor,
    disconnect_uptime_kuma,
    build_monitor_records
)

from pihole import (
    connect_to_pihole,
    disconnect_from_pihole,
    fetch_dns_records,
    build_dns_records,
    build_dns_hostname,
    add_local_dns_record
)

from config import load_env_config



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
    
    config = load_env_config()

    if not validate_env(config):
        return   

    print_status(args)

    api = None
    session = None
    
    try:
        # 1. Verbindung
        api = connect_to_uptime_kuma(
            config["kuma"]["url"],
            config["kuma"]["username"],
            config["kuma"]["password"]
           )
        session = connect_to_pihole(
            config["pihole"]["api_url"],
            config["pihole"]["password"]
            )

        # 2. Prüfen 

        if api is None:
            print("Fehler: Verbindung zu Uptime Kuma fehlgeschlagen")
            return
        
        if session is None:
            print("Fehler: Verbindung zu Pi-Hole Fehlgeschlagen")
            return

        
        # 3. Daten holen 
        monitor_url = build_monitor_url(
            config["network"]["target_ip"],
            args.port)
         
        raw_monitors = get_uptime_monitors(api)

        if raw_monitors is None:
            print("Fehler Uptime Kuma Monitors")
            return

        monitors = build_monitor_records(raw_monitors)


        pihole_hostname = build_dns_hostname(args.service)
        raw_dns_records = fetch_dns_records(config["pihole"]["api_url"],
                                            session)

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
        target_ip = config["network"]["target_ip"]

        if args.dry_run:
            print(f"[DRY-RUN] Würde Uptime-Kuma Monitor '{args.service}' auf {monitor_url} erstellen")
            print(f"[DRY-RUN] Würde local dns record in pi-hole '{pihole_hostname}' auf {target_ip} erstellen")

        else:
            success_add_uptime_monitor = add_uptime_monitor(api, args.service, monitor_url)

            if not success_add_uptime_monitor:
                return
            
            success_add_pihole_local_dns = add_local_dns_record(session,
                                                                config["pihole"]["api_url"],
                                                                config["network"]["target_ip"],
                                                                pihole_hostname)
            if not success_add_pihole_local_dns:
                return
            
            print("Uptime Kuma Monitor erfolgreich erstellt")
            print("Pi-hole local dns record erfolgreich angelegt")


    
    finally:

        #6 Verbindungen trennen

        disconnect_uptime_kuma(api)
        disconnect_from_pihole(config["pihole"]["api_url"],
                               session)


if __name__ == "__main__":
    main()