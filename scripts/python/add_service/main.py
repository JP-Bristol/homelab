import logging 

from parser import parse_arguments
from output import (
    print_status,
    print_ok,
    print_info,
    print_warning,
    print_error,
    print_debug
)

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
from logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)





def main():

    """
    Steuert den Programmablauf: validiert Eingaben und Umgebungsvariablen,
    stellt die benötigten api Verbindungen her, prüft bestehende Ressourcen
    und erstellt neue Einträge in Uptime Kuma und Pi-hole.
    """
    args = parse_arguments()

    if args is None:
        print_error(logger,"Argumente fehlen oder sind ungültig")
        return 

    if is_valid_input(args) is None:
        print_error(logger,"Keine gültige Eingabe")
        return
    
    config = load_env_config()

    if not validate_env(config):
        return   

    print_status(args)

    session_uptime_kuma = None
    session_pihole = None
    
    try:
        # 1. Verbindungen herstellen

        session_uptime_kuma = connect_to_uptime_kuma(
            config["kuma"]["url"],
            config["kuma"]["username"],
            config["kuma"]["password"]
           )
        session_pihole = connect_to_pihole(
            config["pihole"]["api_url"],
            config["pihole"]["password"]
            )

        # 2. Verbindungen prüfen 

        if session_uptime_kuma is None:
            print_error(logger,"Verbindung zu Uptime-Kuma konnte nicht hergestellt werden")
            return
        
        if session_pihole is None:
            print_error(logger,"Verbindung zu Pi-Hole konnte nicht hergestellt werden")
            return

        
        # 3. Daten abrufen

        monitor_url = build_monitor_url(
            config["network"]["target_ip"],
            args.port)
         
        raw_monitors = get_uptime_monitors(session_uptime_kuma)

        if raw_monitors is None:
            print_error(logger,"Uptime-Kuma-Monitore konnten nicht abgerufen werden")
            return

        monitors = build_monitor_records(raw_monitors)


        pihole_hostname = build_dns_hostname(args.service)
        raw_dns_records = fetch_dns_records(config["pihole"]["api_url"],
                                            session_pihole)

        if raw_dns_records is None:
            print_error(logger,"Pi-hole DNS-Einträge konnten nicht abgerufen werden")
            return        
    
        dns_records = build_dns_records(raw_dns_records)
        print_debug(logger,f"{len(dns_records)} Pi-hole DNS-Einträge geladen")

        # 4. Duplikate prüfen

        if not validate_uptime_monitor(monitors, monitor_url, args.service):
            print_error(logger,"Uptime-Kuma-Monitor oder URL bereits vorhanden")
            return
        
        if not validate_pihole_dns_records(dns_records, pihole_hostname):
             print_error(logger,"Pi-hole DNS-Eintrag bereits vorhanden")
             return
        
        # 5. Ressourcen erstellen

        target_ip = config["network"]["target_ip"]

        if args.dry_run:
            print_info(logger,f"Würde Uptime-Kuma-Monitor '{args.service}' auf {monitor_url} erstellen")
            print_info(logger,f"Würde Pi-hole DNS-Eintrag '{pihole_hostname}' auf {target_ip} erstellen")

        else:
            success_add_uptime_monitor = add_uptime_monitor(session_uptime_kuma, args.service, monitor_url)

            if not success_add_uptime_monitor:
                return
            
            success_add_pihole_local_dns = add_local_dns_record(session_pihole,
                                                                config["pihole"]["api_url"],
                                                                config["network"]["target_ip"],
                                                                pihole_hostname)
            if not success_add_pihole_local_dns:
                return
            
            print_ok(logger,"Uptime-Kuma-Monitor erfolgreich erstellt")
            print_ok(logger,"Pi-hole DNS-Eintrag erfolgreich erstellt")


    
    finally:

        #6 Verbindungen trennen

        if session_uptime_kuma is not None:
            success_uptime_kuma = disconnect_uptime_kuma(session_uptime_kuma)
            if not success_uptime_kuma:
                print_warning(logger,"Uptime-Kuma-Session nicht beendet")


        if session_pihole is not None:
            success_pihole = disconnect_from_pihole(config["pihole"]["api_url"], session_pihole)
            if not success_pihole:
                print_warning(logger,"Pi-hole Session nicht beendet")

if __name__ == "__main__":
    main()