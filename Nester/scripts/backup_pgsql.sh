#!/bin/bash

# Save Database and logs

DB_NAME="mspr3"
BACKUP_DIR="$HOME/EPSI_MSPR1-main/Nester/pg_backups"
DATE=$(date +'%Y-%m-%d_%H-%M-%S')
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_${DATE}.sql"

mkdir -p "$BACKUP_DIR"

pg_dump -U postgres "$DB_NAME" > "$BACKUP_FILE"

# Garde les 20 dernières sauvegardes
ls -1tr "$BACKUP_DIR"/*.sql | head -n -20 | xargs -d '\n' rm -f 2>/dev/null

echo "Backup lancé à $(date)" >> "$BACKUP_DIR/backup.log"
