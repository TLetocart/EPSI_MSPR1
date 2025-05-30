import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import nmap
from datetime import datetime
import ipaddress
import csv
import requests
import json
#API
import requests
import platform
import psutil

# NESTER ADRESSE
url = "http://192.168.1.159:5000/api/data"
MY_TOKEN = "token_harvester1"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": MY_TOKEN
}


# Prépare les données à envoyer
data = {
    "hostname": platform.node(),
    "cpu_percent": psutil.cpu_percent(interval=1),
    "ram_percent": psutil.virtual_memory().percent,
    "disk_percent": psutil.disk_usage("C:\\" if platform.system() == "Windows" else "/").percent
}


try:
    response = requests.post(url, json=data, headers=HEADERS)
    print("Code HTTP reçu :", response.status_code)
    print("Texte reçu :", response.text)
    try:
        print("Réponse du Nester (JSON):", response.json())
    except Exception as e:
        print("Erreur lors de la lecture du JSON :", e)
except Exception as e:
    print("Erreur lors de la requête :", e)



# Fonction pour envoyer les résultats au serveur Flask
def send_results_to_server(results):
    server_url = "http://192.168.1.159:5000/upload_results"
    payload = {"results": results}

    print("Sending data to server:", json.dumps(payload, indent=4))

    try:
        response = requests.post(server_url, data=json.dumps(payload), headers=HEADERS)
        if response.status_code == 200:
            result_label.config(text="Données envoyées au serveur avec succès!")
        else:
            result_label.config(text=f"Erreur lors de l'envoi des données: {response.status_code}")
            messagebox.showerror("Erreur", f"Erreur serveur : {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'envoi des données : {e}")


def scan_network():
    scanner = nmap.PortScanner()
    ip_range = "192.168.1.159/24"  
    ports = "22,80,443" 

    try:
        result_label.config(text="Scan en cours, veuillez patienter...")

        # Scanner tous les ports ouverts
        result_label.config(text="Scan en cours, veuillez patienter...")
        scanner.scan(hosts=ip_range, ports=ports, arguments="-T4")


        # Générer un nom de fichier avec la date du jour
        current_date = datetime.now().strftime("%Y-%m-%d_%H-%M")
        filepath = f"scan_results_{current_date}.csv"

        # Récupérer les résultats sous forme de liste
        scan_results = []

        with open(filepath, mode="w", newline='', encoding="utf-8") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(["Nom_Machine", "Adresse_IP", "Ports_ouverts", "Statuts"])  # En-têtes

            for host in scanner.all_hosts():
                hostname = scanner[host].hostname() if scanner[host].hostname() else "Non résolu"
                open_ports = []
                statuses = []

                # Parcours des protocoles et ports ouverts sur l'hôte
                for proto in scanner[host].all_protocols():
                    for port in scanner[host][proto].keys():
                        open_ports.append(str(port))
                        state = scanner[host][proto][port]["state"]
                        statuses.append(f"{port}/{state}")

                ports_str = ", ".join(open_ports)
                statuses_str = ", ".join(statuses)
                csv_writer.writerow([hostname, host, ports_str, statuses_str])

                # Ajouter les résultats à la liste pour l'envoi
                for port, state in zip(open_ports, statuses):
                    scan_results.append({
                        "ip": host,
                        "port": port,
                        "status": state
                    })

        result_label.config(text=f"Scan terminé ! Résultats enregistrés dans {filepath}")
        
        # Envoyer les résultats au serveur Flask
        send_results_to_server(scan_results)
        load_csv(filepath)

    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue :\n{e}")


# Fonction pour charger un fichier CSV
def load_csv(filepath=None):
    try:
        if filepath is None:
            filepath = filedialog.askopenfilename(
                title="Sélectionner un fichier CSV",
                filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
            )
            if not filepath:
                return

        with open(filepath, mode="r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)

            # Vérifier les colonnes
            if "Nom_Machine" not in csv_reader.fieldnames or \
               "Adresse_IP" not in csv_reader.fieldnames or \
               "Ports_ouverts" not in csv_reader.fieldnames or \
               "Statuts" not in csv_reader.fieldnames:
                messagebox.showerror("Erreur", "Le fichier CSV ne contient pas les colonnes requises.")
                return

            # Supprimer les anciennes données
            for row in tree.get_children():
                tree.delete(row)

            # Charger les nouvelles données
            rows = list(csv_reader)
            rows.sort(key=lambda row: ipaddress.ip_address(row["Adresse_IP"]))  # Trier par adresse IP

            for line in rows:
                tree.insert("", tk.END, values=(line["Nom_Machine"], line["Adresse_IP"], line["Ports_ouverts"], line["Statuts"]))

        result_label.config(text=f"Fichier chargé : {filepath}")

    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de lire le fichier CSV.\n{e}")

# Fenêtre principale
window = tk.Tk()
window.title("Seahawks Harvester")
window.geometry("1000x700")
window.configure(bg="#F3F4F6")

# Styles modernes
style = ttk.Style()
style.configure("Treeview", font=("Helvetica", 12), rowheight=30)
style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"))
style.configure("TButton", font=("Helvetica", 12), padding=10)
style.map("TButton", foreground=[("hover", "white")], background=[("hover", "#1A73E8")])

# Header
header_frame = tk.Frame(window, bg="#1A73E8")
header_frame.pack(fill=tk.X, pady=5)
title_label = tk.Label(header_frame, text="Seahawks Harvester", font=("Helvetica", 24, "bold"), bg="#1A73E8", fg="white")
title_label.pack(pady=10)

# Section principale
main_frame = tk.Frame(window, bg="#FFFFFF", bd=2, relief="groove")
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

# Résultats
result_label = tk.Label(main_frame, text="Aucun fichier chargé.", font=("Helvetica", 16), bg="#FFFFFF", fg="#1A73E8")
result_label.pack(pady=10)


# Barre de recherche
search_frame = tk.Frame(main_frame, bg="#FFFFFF")
search_frame.pack(fill=tk.X, pady=10)
search_entry = tk.Entry(search_frame, font=("Helvetica", 14), width=30)
search_entry.pack(side=tk.LEFT, padx=10, pady=5)
search_button = ttk.Button(search_frame, text="Rechercher", command=None)  # Fonction de recherche à implémenter
search_button.pack(side=tk.LEFT, padx=10)

# Section tableau des résultats avec ascenseurs
table_frame = tk.Frame(main_frame, bg="#FFFFFF")
table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

# Ascenseur horizontal
x_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

# Ascenseur vertical (si nécessaire)
y_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Création du Treeview
columns = ("Nom de la machine", "Adresse IP", "Ports ouverts", "Statuts")
tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=15,
    xscrollcommand=x_scrollbar.set,
    yscrollcommand=y_scrollbar.set
)

# Configurer les ascenseurs pour interagir avec le Treeview
x_scrollbar.config(command=tree.xview)
y_scrollbar.config(command=tree.yview)

# Configurer les colonnes
tree.heading("Nom de la machine", text="Nom de la machine")
tree.heading("Adresse IP", text="Adresse IP")
tree.heading("Ports ouverts", text="Ports ouverts")
tree.heading("Statuts", text="Statuts")
tree.column("Nom de la machine", width=300, anchor="center")
tree.column("Adresse IP", width=200, anchor="center")
tree.column("Ports ouverts", width=400, anchor="center")
tree.column("Statuts", width=600, anchor="center")

# Ajouter le Treeview au cadre
tree.pack(fill=tk.BOTH, expand=True)

# Boutons
button_frame = tk.Frame(main_frame, bg="#FFFFFF")
button_frame.pack(pady=10)
scan_button = ttk.Button(button_frame, text="Scanner le réseau", command=scan_network)
scan_button.pack(side=tk.LEFT, padx=10)
load_button = ttk.Button(button_frame, text="Charger un fichier", command=lambda: load_csv())
load_button.pack(side=tk.LEFT, padx=10)

# Footer
footer_label = tk.Label(window, text="© Seahawks Monitoring, 2024", font=("Helvetica", 12), bg="#F3F4F6", fg="#888888")
footer_label.pack(side=tk.BOTTOM, pady=10)

# Lancer l'application
window.mainloop()
