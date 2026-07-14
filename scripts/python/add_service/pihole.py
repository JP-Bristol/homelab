import requests
from error import get_http_error_message
from output import print_error, print_ok

def connect_to_pihole(pihole_api_url, pihole_password):

    """Stellt eine Verbindung zur Pi-hole-API her, authentifiziert den Benutzer und gibt eine vorbereitete HTTP-Session zurück"""

    session = requests.Session()
    session.headers.update({"Accept": "application/json"})

    try:
        password_json = {"password": pihole_password}
        response = session.post(f"{pihole_api_url}/auth", json=password_json)

        response.raise_for_status()

        data = response.json()
        sid = data.get('session', {}).get('sid')

        if sid is None:
            session.close() 
            print_error("Pi-hole: Keine gültige Session-ID erhalten")
            return None

        session.headers.update({"X-FTL-SID": sid}) 
        print_ok("Verbindung zu Pi-hole erfolgreich") 

        return session
    
    except requests.exceptions.HTTPError as err:
        session.close() 
        message = get_http_error_message(err.response.status_code)
        print_error(f"Pi-hole: {message} (HTTP {err.response.status_code})")
        return None

    except requests.exceptions.ConnectionError as err:
        session.close() 
        print_error(f"Verbindung zu Pi-hole fehlgeschlagen: {err}")
        return None  
    
    except requests.exceptions.Timeout as err:
        session.close() 
        print_error(f"Zeitüberschreitung bei der Verbindung zu Pi-hole: {err}")
        return None      

    except Exception as err:
        session.close()
        print_error(f"Unbekannter Fehler: {err}")
        return None


def disconnect_from_pihole(pihole_api_url, session):
    
    """ Beendet die Pi-hole-Session über die API und schließt die lokale HTTP-Session. """

    if session is None:
        return False
    try:
        response = session.delete(f"{pihole_api_url}/auth")
        response.raise_for_status()


        print_ok("Verbindung zu Pi-hole getrennt")
        return True

    except requests.exceptions.HTTPError as err:
        message = get_http_error_message(err.response.status_code)
        print_error(f"Pi-hole: {message} (HTTP {err.response.status_code})")
        return False

    except requests.exceptions.ConnectionError as err:
        print_error(f"Verbindung vom Pi-hole konnte nicht getrennt werden: {err}")
        return False
        
    except requests.exceptions.Timeout as err:
        print_error(f"Zeitüberschreitung bei der Trennung vom Pi-hole: {err}")
        return False     

    except Exception as err:
        print_error(f"Unbekannter Fehler: {err}")
        return False

    finally:
        session.close()

def fetch_dns_records(pihole_api_url,session):

    """ Ruft alle Local-DNS-Einträge von der Pi-hole-API ab und gibt sie als Liste zurück. """

    try:   
        response = session.get(f"{pihole_api_url}/config/dns/hosts")
        response.raise_for_status()

        return response.json()['config']['dns']['hosts']

    except requests.exceptions.HTTPError as err:
        message = get_http_error_message(err.response.status_code)
        print_error(f"Pi-hole: {message} (HTTP {err.response.status_code})")
        return None

    except requests.exceptions.ConnectionError as err:
        print_error(f"Verbindung zu Pi-hole fehlgeschlagen: {err}")
        return None

    except requests.exceptions.Timeout as err:
        print_error(f"Zeitüberschreitung beim Abrufen der DNS-Einträge: {err}")
        return None

    except KeyError as err:
        print_error(f"Unerwartetes Antwortformat von Pi-hole: {err}")
        return None

    except Exception as err:
        print_error(f"Unbekannter Fehler: {err}")
        return None

def parse_dns_record(record):

    """ Wandelt einen Pi-hole-DNS-Eintrag in ein Dictionary mit IP-Adresse und Hostname um. """

    parts = record.split()
    return {
        "ip": parts[0],
        "hostname": parts[1]
    }

def build_dns_records(records):

    """ Erstellt aus allen Pi-hole-DNS-Einträgen eine strukturierte Liste von Dictionaries. """

    dns_records = [parse_dns_record(record) for record in records ]
    return dns_records

def build_dns_hostname(service_name):

    """ Erstellt aus dem Servicenamen den vollständigen Hostnamen. """
    
    return f"{service_name}.home"

def add_local_dns_record(session, pihole_api_url, ip, hostname):

    """ Erstellt einen Local-DNS-Eintrag über die Pi-hole REST-API."""

    try:
        response = session.put(f"{pihole_api_url}/config/dns/hosts/{ip}%20{hostname}")
        response.raise_for_status()
        return True

    except requests.exceptions.HTTPError as err:
        message = get_http_error_message(err.response.status_code)
        print_error(f"Pi-hole: {message} (HTTP {err.response.status_code})")
        return False

    except requests.exceptions.ConnectionError as err:
        print_error(f"Datenübertragung zu Pi-hole fehlgeschlagen: {err}")
        return False

    except requests.exceptions.Timeout as err:
        print_error(f"Zeitüberschreitung beim Übertragen der DNS-Einträge: {err}")
        return False

    except Exception as err:
        print_error(f"Unbekannter Fehler: {err}")
        return False