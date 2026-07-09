import os
from dotenv import load_dotenv

from parser import parse_arguments
from output import print_status
from validation import is_valid_input, validate_env, validate_uptime_monitor
from uptime_kuma import (
    connect_to_uptime_kuma,
    get_uptime_monitor,
    build_monitor_url,
    add_uptime_monitor,
    disconnect_uptime_kuma
)


load_dotenv()

def main():

    """
    Steuert den Programmablauf: validiert Eingaben und .env,
    verbindet sich mit Uptime Kuma, prüft auf Duplikate
    und erstellt den Monitor.
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

    api = connect_to_uptime_kuma(url_kuma, username_kuma, password_kuma)

    if api is None:
        print("Fehler: Verbindung zu Uptime Kuma fehlgeschlagen")
        return

    monitor_url = build_monitor_url(target_ip, args.port)
    monitors = get_uptime_monitor(api)

    if not validate_uptime_monitor(monitors, monitor_url, args.service):
        print("Fehler: Monitor oder Port bereits vorhanden/belegt")
        disconnect_uptime_kuma(api)
        return

    success = add_uptime_monitor(api, args.service, monitor_url)

    if not success:
        disconnect_uptime_kuma(api)
        return

    print("Monitor erfolgreich erstellt")

    disconnect_uptime_kuma(api)

if __name__ == "__main__":
    main()