from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialisation de l'application Flask
app = Flask(__name__)
CORS(app)  # Permet d'accepter les requêtes du Harvester

# Configuration de la base PostgreSQL
###### Pensez à indiquer le mdp !
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:poketom@localhost/seahawks_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de SQLAlchemy
db = SQLAlchemy(app)

# Modèle pour stocker les résultats du Harvester
class ScanResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(50), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(10), nullable=False)

# Créer les tables dans la base de données (exécuté lors du démarrage de l'application)
with app.app_context():
    db.create_all()

# Route pour la page d'accueil (HTML)
@app.route('/')
def home():
    return render_template('index.html')  # Cette fonction rend la page HTML

# Endpoint pour recevoir les résultats du Harvester
@app.route('/upload_results', methods=['POST'])
def receive_results():
    data = request.json
    print("Data received:", data)  # Debug pour afficher les données reçues

    if not data or "results" not in data:
        return jsonify({"error": "Données invalides"}), 400

    # Sauvegarde des résultats en base de données
    for entry in data["results"]:
        status = entry['status'][:10]
        existing_scan = ScanResult.query.filter_by(ip_address=entry["ip"]).first()  # Chercher si l'IP existe déjà
        if existing_scan:
            # Si l'entrée existe, on met à jour les données
            existing_scan.port = entry["port"]
            existing_scan.status = entry["status"]
        else:
            # Si l'entrée n'existe pas, on en crée une nouvelle
            new_scan_result = ScanResult(ip_address=entry['ip'], port=entry['port'], status=status)
            db.session.add(new_scan_result)

    db.session.commit()
    return jsonify({"message": "Données reçues et stockées avec succès"}), 200


# Endpoint pour récupérer tous les résultats (pour l'interface web)
@app.route('/get_results', methods=['GET'])
def get_results():
    scans = ScanResult.query.all()
    return jsonify([{"ip": scan.ip_address, "port": scan.port, "status": scan.status} for scan in scans])

# Lancer le serveur
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

