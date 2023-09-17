import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import time
from plyer import notification  # Assurez-vous d'installer la bibliothèque plyer avec "pip install plyer"
from twilio.rest import Client

# URL du site Web à surveiller
url = "https://..."

# Remplacez ces valeurs par votre Account SID et Auth Token Twilio
account_sid = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
auth_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'

# Créez un client Twilio
client = Client(account_sid, auth_token)

# Remplacez par votre numéro Twilio
from_number = '+123456789'

# Remplacez par le numéro de téléphone du destinataire
# Liste des numéros de téléphone des destinataires
to_numbers = [
    '+33XXXXXXXXX',  # 
    '+33XXXXXXXXX',  # 
    '+33XXXXXXXXX',  # 
    '+33XXXXXXXXX'  # 
]
message = 'Des places sont disponibles !! \nGo les prendre : https://...'

# Fonction pour vérifier la disponibilité des places de camping
def check_camping_availability():
    # Faites une demande GET pour récupérer la page Web
    response = requests.get(url)

    # Vérifiez si la demande a réussi
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        print("Réussite de la demande HTTP.")

        # Recherchez un élément spécifique qui indique la disponibilité des places de camping
        # Vous devrez inspecter le site Web pour trouver l'élément approprié
        availability_element = soup.find("td", {"class": "note quantity"})  # Exemple factice

        print(availability_element.text.lower())

        # Vérifiez si l'élément indique que les places de camping sont en vente
        if availability_element and "épuisés" in availability_element.text.lower():
            return False
        else:
            return True
    else:
        print("Échec de la demande HTTP.")
        return False

# Fonction pour envoyer une notification
def send_notification(message):
    notification.notify(
        title='Places de disponibles !',
        message=message,
        app_name='Y a-t-il des places ?',
        timeout=20  # Durée d'affichage de la notification en secondes
    )

    try:
        # Envoi du SMS
        # Envoi du SMS à chaque destinataire
        for to_number in to_numbers:
            client.messages.create(
                body=message,
                from_=from_number,
                to=to_number
            )
        print('SMS envoyé avec succès.')
        root.quit()
    except Exception as e:
        print(f'Erreur lors de l\'envoi du SMS : {str(e)}')


# Fonction pour démarrer la vérification automatique
def start_checking():
    frequency = int(interval_entry.get())  # Récupère l'intervalle en secondes depuis l'entrée
    while not should_quit:
        if check_camping_availability():
            send_notification("Des places sont disponibles !")
        
        root.update()
        # Attendez la prochaine vérification
        time.sleep(frequency)


# Fonction pour quitter l'application
def quit_application():
    global should_quit
    should_quit = True
    root.destroy()  # Ferme la fenêtre principale et quitte l'application

# Créer la fenêtre principale
root = tk.Tk()
root.title("Recherche...")

# Créer une étiquette
label = tk.Label(root, text="Entrez l'intervalle de vérification (en secondes):")
label.pack()

# Créer une zone de saisie pour l'intervalle
interval_entry = tk.Entry(root)
interval_entry.pack()

# Créer un bouton pour démarrer la vérification automatique
start_button = tk.Button(root, text="Démarrer la vérification", command=start_checking)
start_button.pack()

# Bouton pour quitter l'application
quit_button = tk.Button(root, text="Quitter", command=quit_application)
quit_button.pack()

should_quit = False  # Variable de contrôle pour la boucle

root.mainloop()
