import os
from dotenv import load_dotenv

load_dotenv()

def load_env_config():
    """Lädt alle benötigten Umgebungsvariablen als strukturiertes Dict."""
    return {
        "kuma": {
            "url": os.getenv("KUMA_URL"),
            "username": os.getenv("KUMA_USERNAME"),
            "password": os.getenv("KUMA_PASSWORD")
        },
        "pihole": {
            "api_url": os.getenv("PIHOLE_API_URL"),
            "password": os.getenv("PIHOLE_PASSWORD")
        },
        "npm":{
            "identity": os.getenv("NPM_IDENTITY"),
            "secret": os.getenv("NPM_SECRET"),
            "api_url": os.getenv("NPM_API_URL")
        },
        "network": {
            "target_ip": os.getenv("TARGET_IP")
        }
    }

def build_hostname(service_name):

    """ Erstellt aus dem Servicenamen den vollständigen Hostnamen. """

    return f"{service_name}.home"

