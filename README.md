# Harvester : Logiciel / Nester : Application WEB

# Prérequis : 

# Installer : Python / PostgreSQL

- Création de la BDD dans PostGreSQL :

BDD PostGreSQL : 
CREATE TABLE harvesters (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    ip_address VARCHAR(50) NOT NULL,
    status VARCHAR(10) NOT NULL,
    last_scan JSON
);


# Ligne de commande dans la console :
 
Installer flask (dossier nester) : pip install flask

Drivers pour PostgreSQL : pip install flask_sqlalchemy psycopg2

Drivers pour que le navigateur accède aux infos : pip install flask-cors



# ! Avant de lancer le serveur ! (nester.py)
Configuration de la base PostgreSQL :

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:motdepasse@localhost/seahawks_db'
--> Changer le motdepasse par le mot de passe défini pendant l'installation de PostgreSQL (Ligne 11 de nester.py)


Lancer serveur : python nester.py
Lancer harvester : python harvester.py


Accès à la page web : http://127.0.0.1:5000/
Accès au Json : http://127.0.0.1:5000/get_results

