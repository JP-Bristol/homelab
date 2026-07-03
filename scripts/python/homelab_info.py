# Homelab Info 
hostname = "arasaka"
services = ["pihole", "uptime-kuma", "nginx", "vaultwarden", "wikijs", "syncthing"]

print(f"Hostname: {hostname}")
print(f"Anzahl der Services: {len(services)}")

for service in services:
    print(f" - {service}")

