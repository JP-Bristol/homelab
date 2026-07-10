import requests

def connect_to_pihole(pihole_api_url, pihole_password):

    """Stellt eine Verbindung zur Pi-hole-API her, authentifiziert den Benutzer und gibt eine vorbereitete HTTP-Session zurück"""

    session = requests.Session()
    session.headers.update({"Accept": "application/json"})

    try:
        password_json = {"password": pihole_password}
        response = session.post(pihole_api_url, json=password_json)
        

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


def disconnect_from_pihole(url, session):
    if session is None:
        return False
    try:
        response = session.delete(url)

        

        if response.status_code != 204:
            print(f"Fehler: Status {response.status_code}")
            return False

        print("Verbindung getrennt")
        return True

    except Exception as e:
        print(f"Fehler: {e}")
        return False

    finally:
        session.close()