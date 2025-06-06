#!/bin/bash

# Génère rapport HTML + Page WEB
# API Nester -> Génère bouton dynamique / Relance script

OUTPUT="$HOME/EPSI_MSPR1-main/Nester/scripts/supervision/supervision_report.html"
DB="mspr3"
USER="postgres"

# 1. Mesure initiale
IFS="|" read xact1 blks_read1 blks_hit1 <<< "$(psql -U $USER -d $DB -Atc "SELECT xact_commit + xact_rollback, blks_read, blks_hit FROM pg_stat_database WHERE datname = '$DB';")"
sleep 5
IFS="|" read xact2 blks_read2 blks_hit2 <<< "$(psql -U $USER -d $DB -Atc "SELECT xact_commit + xact_rollback, blks_read, blks_hit FROM pg_stat_database WHERE datname = '$DB';")"
delta_time=5
req_per_sec=$(echo "scale=2; ($xact2-$xact1)/$delta_time" | bc)
read_per_sec=$(echo "scale=2; ($blks_read2-$blks_read1)/$delta_time" | bc)
hit_per_sec=$(echo "scale=2; ($blks_hit2-$blks_hit1)/$delta_time" | bc)

DATE_REPORT=$(date '+%d/%m/%Y à %H:%M:%S')


{
echo "<!DOCTYPE html>"
echo "<html lang='fr'>"
echo "<head><meta charset='UTF-8'><title>Rapport de supervision PostgreSQL</title>"
echo "<style>
body{font-family:Arial,sans-serif;background:#f9f9f9;color:#222;}
h1{color:#1761a0;}
h2{margin-top:30px;}
table{border-collapse:collapse;width:80%;margin:0 auto 2em auto;}
th,td{border:1px solid #aaa;padding:6px 12px;text-align:left;}
th{background:#e5f0fa;}
tr:nth-child(even){background:#f2f2f2;}
.section{margin:40px 0;}
</style></head>"
echo "<h1>Rapport de supervision PostgreSQL</h1>"
echo "<div style='text-align:center;color:#888;margin-bottom:20px;'>Généré le $DATE_REPORT</div>"

echo "<div class='section'><h2>Indicateurs de flux instantanés (calculés sur $delta_time secondes)</h2>"
echo "<table><tr><th>Requêtes/sec</th><th>Lectures disque/sec</th><th>Lectures cache/sec</th></tr>"
echo "<tr><td>$req_per_sec</td><td>$read_per_sec</td><td>$hit_per_sec</td></tr></table>"
echo "</div>"

echo "<div class='section'><h2>Nombre de connexions et transactions</h2>"
psql -U $USER -d $DB -H -P footer=off -c "SELECT datname, numbackends, xact_commit + xact_rollback AS total_transactions FROM pg_stat_database WHERE datname = '$DB';"
echo "</div>"

echo "<div class='section'><h2>Taille des tables</h2>"
psql -U $USER -d $DB -H -P footer=off -c "SELECT relname AS table, pg_size_pretty(pg_total_relation_size(relid)) AS total_size FROM pg_catalog.pg_statio_user_tables ORDER BY pg_total_relation_size(relid) DESC;"
echo "</div>"

echo "<div class='section'><h2>Taille totale de la base</h2>"
psql -U $USER -d $DB -H -P footer=off -c "SELECT pg_size_pretty(pg_database_size('$DB')) AS total_db_size;"
echo "</div>"

echo "<div class='section'><h2>Requêtes longues en cours</h2>"
psql -U $USER -d $DB -H -P footer=off -c "SELECT pid, query, state, now() - query_start AS duree FROM pg_stat_activity WHERE datname = '$DB' AND state = 'active' ORDER BY duree DESC LIMIT 5;"
echo "</div>"

echo "<div class='section'><h2>Utilisation des index</h2>"
psql -U $USER -d $DB -H -P footer=off -c "SELECT relname AS table, idx_scan AS index_scans FROM pg_stat_user_tables ORDER BY idx_scan DESC;"
echo "</div>"

echo "</body></html>"
} > "$OUTPUT"
