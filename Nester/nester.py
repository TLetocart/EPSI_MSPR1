from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os
import csv

# ========== CONFIGURATION ARCHIVES ==========

ARCHIVES_DIR = os.path.join(os.path.dirname(__file__), "archives")
os.makedirs(ARCHIVES_DIR, exist_ok=True)

# Pour les POST sur /api/data (santé système)
CSV_FILE = os.path.join(ARCHIVES_DIR, "data_received.csv")
# Pour les POST sur /upload_results (scans, tout Harvester)
CSV_ARCHIVE = os.path.join(ARCHIVES_DIR, "harvesters_history.csv")

API_SECRET = "MonSecretToken123"

# ========== FLASK & BDD ==========
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:poketom@localhost/seahawks_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ScanResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(50), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(10), nullable=False)

with app.app_context():
    db.create_all()

# ========== ROUTES ==========

@app.route('/')
def home():
    try:
        return render_template('index.html')
    except:
        return "API Seahawks Nester prête !"

# API santé/infos système
@app.route('/api/data', methods=['POST'])
def api_receive_data():
    data = request.json
    print(f"Data received: {data}")

    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, "a", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["date", "hostname", "cpu_percent", "ram_percent", "disk_percent"])
        row = [
            datetime.now().isoformat(),
            data.get("hostname", ""),
            data.get("cpu_percent", ""),
            data.get("ram_percent", ""),
            data.get("disk_percent", "")
        ]
        writer.writerow(row)
    return jsonify({"status": "success", "received_data": data}), 200

# API upload_results : stocke en base ET archive tout
@app.route('/upload_results', methods=['POST'])
def receive_results():
    data = request.json
    print("Data received (upload_results):", data)
    if not data or "results" not in data:
        return jsonify({"error": "Données invalides"}), 400

    # 1. Sauvegarde d'archive (CSV)
    file_exists = os.path.isfile(CSV_ARCHIVE)
    with open(CSV_ARCHIVE, "a", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["datetime", "source", "ip", "port", "status"])
        source = request.remote_addr  # Adresse IP du Harvester
        now = datetime.now().isoformat()
        for entry in data["results"]:
            writer.writerow([
                now,
                source,
                entry.get("ip", ""),
                entry.get("port", ""),
                entry.get("status", "")
            ])

    # 2. Stockage en base de données (ScanResult)
    for entry in data["results"]:
        status = str(entry.get('status', ''))[:10]
        ip = entry.get("ip", "")
        port = int(entry.get("port", 0))
        existing_scan = ScanResult.query.filter_by(ip_address=ip, port=port).first()
        if existing_scan:
            existing_scan.status = status
        else:
            new_scan = ScanResult(ip_address=ip, port=port, status=status)
            db.session.add(new_scan)
    db.session.commit()
    return jsonify({"message": "Données reçues et stockées avec succès"}), 200

@app.route('/get_results', methods=['GET'])
def get_results():
    scans = ScanResult.query.all()
    return jsonify([{
        "ip": scan.ip_address,
        "port": scan.port,
        "status": scan.status
    } for scan in scans])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
