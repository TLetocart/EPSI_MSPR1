import requests

# Remplace l'adresse IP par celle de ta VM Nester
url = "http://192.168.1.159:5000/api/data"
payload = {"message": "Bonjour depuis Harvester !"}

try:
    response = requests.post(url, json=payload)
    print("Réponse reçue :", response.json())
except Exception as e:
    print("Erreur lors de la requête :", e)