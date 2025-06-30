# Harvester : Logiciel / Nester : Application WEB

# Prérequis : 

# Installer : Python / PostgreSQL

- PgAdmin
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

# ! Avant de lancer le Harvester ! (harvester.py)
Changer les URL  :
        ip_range = "192.168.1.144/24"  --> Voir son IP

Changer le token :
    MY_TOKEN = "token_harvester1"


Lancer serveur : python nester.py
Lancer harvester : python harvester.py

Exemple : 
Accès à la page web : http://127.0.0.1:5000/
Accès au Json : http://127.0.0.1:5000/get_results

# ! Test de connexion du Harvester vers Nester : 
harvester/ping/send_to_nester


# ! MSPR 3
Commandes essentielles :
 
Démarrer PostGre : 
sudo systemctl start postgresql
Vérifier statut : 	
sudo systemctl status postgresql
Arrêter : 
	sudo systemctl stop postgresql
Redémarrer : 
sudo systemctl restart postgresql

Démarrer PostGre au démarrage : 
	sudo systemctl enable postgresql

Connexion user postgres (superAdmin): 
sudo -i -u postgres


Commande PostGreSQL : 

Se connecter à PostgreSQL en tant qu’utilisateur 'postgres'
sudo -i -u postgres

Se connecter à une base précise 
psql -U postgres -d mspr3

Entrer dans le shell : 
		psql -d mspr3

Lister les bases de données
\l

Lister les tables
\dt

Afficher la structure d’une table
\d nom_table

Voir les index
\di

Voir les utilisateurs
\du

Voir les vues
\dv

Voir les droits sur une table/vue
\z nom_table_ou_vue

Quitter psql
\q

Commandes supplémentaires : 

Sauvegarde : 
crontab -l

	Restaurer depuis une sauvegarde : 
pg_restore -U postgres -d mspr3 /home/backup/mspr3_2024-06-05_1400.dump

