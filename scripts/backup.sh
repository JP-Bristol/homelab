sudo /home/jp/homelab/scripts/cleanup_backup.sh#!/bin/bash

DATE=$(date +%Y-%m-%d)
BACKUP_DIR="/mnt/backup/$DATE"

echo "Backup startet: $DATE"

mkdir -p $BACKUP_DIR

# Homelab Configs
rsync -av --ignore-errors  --exclude='logs/' --exclude='.git/' ~/homelab/ $BACKUP_DIR/homelab/

# Service Daten
rsync -av --ignore-errors ~/homelab/services/pihole/data/ $BACKUP_DIR/pihole-data/
rsync -av --ignore-errors ~/homelab/services/uptime-kuma/data/ $BACKUP_DIR/uptime-kuma-data/
rsync -av --ignore-errors ~/homelab/services/nginx-proxy-manager/data/ $BACKUP_DIR/npm-data/
rsync -av --ignore-errors ~/homelab/services/wikijs/data/ $BACKUP_DIR/wikijs-data/
rsync -av --ignore-errors ~/homelab/services/vaultwarden/data/ $BACKUP_DIR/vaultwarden-data/
rsync -av --ignore-errors ~/homelab/services/syncthing/data/ $BACKUP_DIR/syncthing-data/
sudo rsync -av --ignore-errors ~/homelab/services/gitea/gitea/ $BACKUP_DIR/gitea-data/

echo "Backup fertig: $BACKUP_DIR"

sudo /home/jp/homelab/scripts/cleanup_backup.sh
