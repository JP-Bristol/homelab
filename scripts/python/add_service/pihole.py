import requests

def connect_to_pihole(pihole_api_url, pihole_password):

    """Stellt eine Verbindung zur Pi-hole-API her, authentifiziert den Benutzer und gibt eine vorbereitete HTTP-Session zurück"""

    session = requests.Session()
    session.headers.update({"Accept": "application/json"})

    try:
        password_json = {"password": pihole_password}
        response = session.post(f"{pihole_api_url}/auth", json=password_json)

        

        if response.status_code != 200:
            session.close() 
            print(f"Fehler: Status {response.status_code}")
            return None

        data = response.json()
        sid = data.get('session', {}).get('sid')

        if sid is None:
            session.close() 
            print("Fehler: SID")
            return None

        session.headers.update({"X-FTL-SID": sid})  

        return session

    
    except Exception as e:
        session.close() 
        print(f"Verbindungfehler: {e}")
        return None


def disconnect_from_pihole(pihole_api_url, session):
    
    """ Beendet die Pi-hole-Session über die API und schließt die lokale HTTP-Session. """

    if session is None:
        return False
    try:
        response = session.delete(f"{pihole_api_url}/auth")

        

        if response.status_code != 204:
            print(f"Fehler: Status {response.status_code}")
            return False

        print("Verbindung zu Pihole getrennt")
        return True

    except Exception as e:
        print(f"Fehler: {e}")
        return False

    finally:
        session.close()

def fetch_dns_records(pihole_api_url,session):

    """ Ruft alle Local-DNS-Einträge von der Pi-hole-API ab und gibt sie als Liste zurück. """

    try:   
        response = session.get(f"{pihole_api_url}/config/dns/hosts")
        if response.status_code != 200:
            print(f"Fehler: Status {response.status_code}")
            return None
        return response.json()['config']['dns']['hosts']

    except Exception as e:
        print(f"Fehler Fetch DNS: {e}")
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
    
    return f"{service_name}.home"