from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os
import csv

# ---------- CONFIGURATION ARCHIVES ----------------

ARCHIVES_DIR = os.path.join(os.path.dirname(__file__), "archives")
os.makedirs(ARCHIVES_DIR, exist_ok=True)

# /api/data 
CSV_FILE = os.path.join(ARCHIVES_DIR, "data_received.csv")
# /upload_results
CSV_ARCHIVE = os.path.join(ARCHIVES_DIR, "harvesters_history.csv")


# ------------- TOKEN ----------------------------

def load_tokens(filename="tokens.txt"):
    if not os.path.isfile(filename):
        return set()
    with open(filename, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())


# -------------- FLASK & BDD --------------------

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:psql@localhost/seahawks_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ScanResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(50), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(10), nullable=False)

with app.app_context():
    db.create_all()


# --------------- ROUTES ------------------

@app.route('/')
def home():
    try:
        return render_template('index.html')
    except:
        return "API Seahawks Nester prête !"

@app.route('/api/data', methods=['POST'])
def api_receive_data():
    auth_header = request.headers.get("Authorization")
    authorized_tokens = load_tokens() 
    if not auth_header or auth_header not in authorized_tokens:
        return jsonify({"error": "Unauthorized"}), 401

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

# ------- API upload_results : SAVE DATABASE AND ARCHIVES -----------

@app.route('/upload_results', methods=['POST'])
def receive_results():
    auth_header = request.headers.get("Authorization")
    authorized_tokens = load_tokens()  
    if not auth_header or auth_header not in authorized_tokens:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    print("Data received (upload_results):", data)
    if not data or "results" not in data:
        return jsonify({"error": "Données invalides"}), 400

    # Save Archives (CSV)
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

    # Save database (ScanResult)
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
    auth_header = request.headers.get("Authorization")
    authorized_tokens = load_tokens() 
    if not auth_header or auth_header not in authorized_tokens:
        return jsonify({"error": "Unauthorized"}), 401

    scans = ScanResult.query.all()
    return jsonify([{
        "ip": scan.ip_address,
        "port": scan.port,
        "status": scan.status
    } for scan in scans])




# ---------- Supervision ----------------
# Génère le bouton actualiser de la page de supervision

from flask import send_file, redirect, url_for, request
import subprocess

SUPERVISION_SCRIPT = "/home/thomas/EPSI_MSPR1-main/Nester/scripts/supervision/rapport_supervision.sh"
SUPERVISION_HTML = "/home/thomas/EPSI_MSPR1-main/Nester/scripts/supervision/supervision_report.html"

@app.route('/supervision', methods=['GET', 'POST'])
def show_supervision():
    if request.method == 'POST':
        subprocess.run([SUPERVISION_SCRIPT])
        return redirect(url_for('show_supervision'))
    with open(SUPERVISION_HTML, 'r', encoding='utf-8') as f:
        page = f.read()
    bouton = """
    <div style="text-align:center;margin:18px;">
      <form method="post" action="/supervision">
        <button type="submit" style="font-size:1.1em;padding:8px 24px;border-radius:8px;background:#1761a0;color:white;border:none;cursor:pointer;">
          Générer une supervision à jour
        </button>
      </form>
    </div>
    """
    page = page.replace("</h1>", "</h1>" + bouton, 1)
    return page







if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)