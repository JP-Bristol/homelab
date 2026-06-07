#!/bin/bash

DATE=$(date +%Y-%m-%d)
BACKUP_DIR="/mnt/backup/$DATE"

echo "Backup startet: $DATE"

mkdir -p $BACKUP_DIR

# Homelab Configs
rsync -av ~/homelab/ $BACKUP_DIR/homelab/

# Service Daten
rsync -av ~/homelab/services/pihole/data/ $BACKUP_DIR/pihole-data/
rsync -av ~/homelab/services/uptime-kuma/data/ $BACKUP_DIR/uptime-kuma-data/
rsync -av ~/homelab/services/nginx-proxy-manager/data/ $BACKUP_DIR/npm-data/

echo "Backup fertig: $BACKUP_DIR"

find /mnt/backup -maxdepth 1 -type d -mtime +7 -exec rm -rf {} \;
