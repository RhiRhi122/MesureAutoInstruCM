# Etape_H_ABE.py
import customtkinter as ctk
from math import *
from tkinter import messagebox
from VerifValeursCiblesSondes import verifier_mesure, valeurs_cibles
from SauvExcel import sauvegarder_mesures_excel
from MesureResistance import Mesure4W, Mesure2W
from MesureIsolement import verifier_isolement
import time

# Nom poste
nom_poste = "H-ABE"

etat_mesure = []

# Données Channels Utilisés
source_channels_FW1 = []
sense_channels_FW1 = []
source_channels_TW2 = [209]
source_channels_FW3 = [304, 305]
sense_channels_FW3 = [314, 315]

# Fonction pour afficher la matrice dans une nouvelle fenêtre
def Etape_H_ABE(parent, operateur_nom, cryomodule_num, A_M):
    top = ctk.CTkToplevel(parent)
    top.title("Etape : F-ABE")
    top.attributes("-topmost", True)  # Rendre la fenêtre au premier plan

    # Variable pour stocker la sélection de la cavité
    cavite_selectionnee = ctk.IntVar()
    
    # Création des boutons pour les cavités
    label_choix_cavite = ctk.CTkLabel(top, text="Choisissez la cavité à mesurer :", font=("Arial", 12))
    label_choix_cavite.pack(pady=10)

    # Fonction pour mettre à jour l'état des boutons
    def choisir_cavite(valeur, bouton):
        cavite_selectionnee.set(valeur)
        # Réinitialiser tous les boutons
        for btn in boutons_cavites:
            btn.configure(fg_color="lightgray")  # Remettre en relief
        # Mettre en relief le bouton sélectionné
        bouton.configure(fg_color="#2404b5")

    # Liste des boutons pour les cavités
    boutons_cavites = []
    
    # Boutons de sélection des cavités
    bouton_cavite1 = ctk.CTkButton(top, text="Cavité 1", font=("Arial", 15, "bold"), command=lambda: choisir_cavite(1, bouton_cavite1), width=100, height=50)
    bouton_cavite1.pack(padx=20, pady=5)
    boutons_cavites.append(bouton_cavite1)

    bouton_cavite2 = ctk.CTkButton(top, text="Cavité 2", font=("Arial", 15, "bold"), command=lambda: choisir_cavite(2, bouton_cavite2), width=100, height=50)
    bouton_cavite2.pack(padx=20, pady=5)
    boutons_cavites.append(bouton_cavite2)

    bouton_cavite3 = ctk.CTkButton(top, text="Cavité 3", font=("Arial", 15, "bold"), command=lambda: choisir_cavite(3, bouton_cavite3), width=100, height=50)
    bouton_cavite3.pack(padx=20, pady=5)
    boutons_cavites.append(bouton_cavite3)

    bouton_cavite4 = ctk.CTkButton(top, text="Cavité 4", font=("Arial", 15, "bold"), command=lambda: choisir_cavite(4, bouton_cavite4), width=100, height=50)
    bouton_cavite4.pack(padx=20, pady=5)
    boutons_cavites.append(bouton_cavite4)

    # Fonction qui va gérer la validation et lancer l'étape correspondante
    def valider_choix():
        cavite = cavite_selectionnee.get()
        
        # Vérification si aucune cavité n'est sélectionnée
        if cavite == 0:
            messagebox.showwarning("Avertissement", "Pas de cavité choisie!")
            top.destroy()  # Ferme la fenêtre de choix
            parent.destroy()  # Ferme la fenêtre principale
            return  # Ne pas continuer
        
        print(f"Cavité sélectionnée : {cavite}")
        
        # Appel de la fonction de mesure avec le choix
      
        if A_M == "auto":
            afficher_resultats(parent, cavite, operateur_nom, cryomodule_num)  # Passer cavite et jauges_chauff
        elif A_M == "manuel":
            afficher_resultats_manuel(parent, cavite, operateur_nom, cryomodule_num)
        top.destroy()  # Ferme la fenêtre de sélection

    # Bouton pour valider le choix
    bouton_valider = ctk.CTkButton(top, text="Valider", font=("Arial", 15, "bold"), command=valider_choix, width=300, height=50)
    bouton_valider.pack(pady=20)

    parent.withdraw()  # Cacher la fenêtre principale

def afficher_resultats(parent, cavite, operateur_nom, cryomodule_num):

    top = ctk.CTkToplevel(parent)
    top.title("Résultats de Mesure")
    top.attributes("-topmost", True)  # Rendre la fenêtre au premier plan

    # Initialisation des noms de capteurs
    noms_donnees = []

    # Ajouter les capteurs en fonction de la sélection
    if cavite != 0:  # Une cavité est sélectionnée
        noms_donnees = [f"HTR-{cavite}00", f"TX-{cavite}01", f"TX-{cavite}02"]

    # Affichage des valeurs mesurées (valeurs fictives pour le moment)
    valeurs_mesures = [0] * len(noms_donnees)
    etat_mesure = [False] * len(noms_donnees)
    etat_isolement = [False] * len(noms_donnees)

    # En-têtes des colonnes
    entete_ref = ctk.CTkLabel(top, text="Référence du Capteur", font=("Arial", 14, "italic", "bold"), text_color="#13025e")
    entete_ref.grid(row=0, column=0, padx=10, pady=5)

    entete_resistance = ctk.CTkLabel(top, text="Résistance (Ω)", font=("Arial", 14, "italic", "bold"), text_color="#13025e")
    entete_resistance.grid(row=0, column=1, padx=10, pady=5)

    entete_defaut_mesure = ctk.CTkLabel(top, text="Défaut de Mesure", font=("Arial", 14, "italic", "bold"), text_color="#13025e")
    entete_defaut_mesure.grid(row=0, column=2, padx=10, pady=5)

    entete_defaut_isolement = ctk.CTkLabel(top, text="Défaut Isolement", font=("Arial", 14, "italic", "bold"), text_color="#13025e")
    entete_defaut_isolement.grid(row=0, column=3, padx=10, pady=5)

    # Créer des listes pour stocker les voyants de mesure et d'isolement
    voyants_mesure = []
    voyants_isolement = []

    # Ajouter les colonnes de données
    for i, nom in enumerate(noms_donnees):
        label_nom = ctk.CTkLabel(top, text=nom, font=("Arial", 14, "bold"))
        label_nom.grid(row=i + 1, column=0, padx=10, pady=10)

        label_valeur = ctk.CTkLabel(top, text=str(valeurs_mesures[i]))
        label_valeur.grid(row=i + 1, column=1, padx=10, pady=10)

        couleur_mesure = "green" if etat_mesure[i] else "red"
        voyant_mesure = ctk.CTkCanvas(top, width=100, height=50, bg=couleur_mesure)
        voyant_mesure.grid(row=i + 1, column=2, padx=10, pady=10)
        voyants_mesure.append(voyant_mesure)  # Ajouter le voyant à la liste

        if not etat_mesure[i]:
            voyant_mesure.create_text(50, 25, text="Défaut", fill="white", font=("Arial", 14, "bold"))

        couleur_isolement = "green" if etat_isolement[i] else "red"
        voyant_isolement = ctk.CTkCanvas(top, width=100, height=50, bg=couleur_isolement)
        voyant_isolement.grid(row=i + 1, column=3, padx=10, pady=10)
        voyants_isolement.append(voyant_isolement)  # Ajouter le voyant à la liste

        if not etat_isolement[i]:
            voyant_isolement.create_text(50, 25, text="Défaut", fill="white", font=("Arial", 14, "bold"))

    bouton_lancer_mesure = ctk.CTkButton(top, text="Lancer la mesure", width=200, height=50,
                                    font=("Arial", 15, "bold"), fg_color="#100bb0", text_color="white",
                                    command=lambda: lancer_mesure(noms_donnees, valeurs_mesures, etat_mesure, etat_isolement, voyants_mesure, voyants_isolement, bouton_sauvegarder))
    bouton_lancer_mesure.grid(row=len(noms_donnees) + 1, column=0, columnspan=4, pady=10)
    
    bouton_sauvegarder = ctk.CTkButton(top, text="Sauvegarder mesures", width=200, height=50,
                                    font=("Arial", 15, "bold"), fg_color="#100bb0", text_color="white",
        command=lambda: sauvegarder_mesures_excel(noms_donnees, valeurs_mesures, etat_isolement, etat_mesure, operateur_nom, cryomodule_num, nom_poste, top))
    bouton_sauvegarder.grid(row=len(noms_donnees) + 2, column=0, columnspan=4, pady=10)
    bouton_sauvegarder.grid_remove()  # Masquer le bouton au début

    parent.withdraw()  # Cacher la fenêtre principale

def afficher_resultats_manuel(parent, cavite, operateur_nom, cryomodule_num):
    global resultats_window
    # Vérifier si la fenêtre existe déjà et la détruire si nécessaire
    if 'resultats_window' in globals() and resultats_window.winfo_exists():
        resultats_window.destroy()

    # Créer une nouvelle fenêtre pour afficher les résultats
    resultats_window = ctk.CTkToplevel(parent)
    resultats_window.title("Résultats de Mesure")
    resultats_window.attributes("-topmost", True)

    # Initialisation des noms de capteurs
    noms_donnees = []
    # Ajouter les capteurs en fonction de la sélection
    if cavite != 0:  # Une cavité est sélectionnée
        noms_donnees = [f"HTR-{cavite}00", f"TX-{cavite}01", f"TX-{cavite}02"]
    
    # Initialisation des valeurs mesurées
    valeurs_mesures = [ctk.StringVar(value="") for _ in noms_donnees]
    etat_isolement = [ctk.BooleanVar(value=False) for _ in noms_donnees]
  
    # En-têtes des colonnes
    entete_ref = ctk.CTkLabel(resultats_window, text="Référence du Capteur", font=("Arial", 14, "italic", "bold"), text_color="#13025e")
    entete_ref.grid(row=0, column=0, padx=10, pady=5)

    entete_resistance = ctk.CTkLabel(resultats_window, text="Résistance (Ω)", font=("Arial", 14, "italic", "bold"), text_color="#13025e")
    entete_resistance.grid(row=0, column=1, padx=10, pady=5)

    entete_defaut_mesure = ctk.CTkLabel(resultats_window, text="Défaut de Mesure", font=("Arial", 14, "italic", "bold"), text_color="#13025e")
    entete_defaut_mesure.grid(row=0, column=2, padx=10, pady=5)

    entete_defaut_isolement = ctk.CTkLabel(resultats_window, text="Défaut Isolement", font=("Arial", 14, "italic", "bold"), text_color="#13025e")
    entete_defaut_isolement.grid(row=0, column=3, padx=10, pady=5)

    champs_mesures = []
    voyants_mesure = []
    isolement_vars = []  # Stocker les états d'isolement
    boutons_defaut_isolement = []

    # Fonction pour basculer l'état du bouton d'isolement
    def toggle_defaut_isolement(i):
        if boutons_defaut_isolement[i].cget("fg_color") == "green":
            boutons_defaut_isolement[i].configure(fg_color="red", text="Défaut", text_color="white")
            isolement_vars[i].set(1)
        else:
            boutons_defaut_isolement[i].configure(fg_color="green", text="OK", text_color="white")
            isolement_vars[i].set(0)

    # Ajouter les champs pour chaque sonde
    for i, ref_mesure in enumerate(noms_donnees):
        label_reference = ctk.CTkLabel(resultats_window, text=ref_mesure, font=("Arial", 14, "bold"))
        label_reference.grid(row=i + 1, column= 0, padx=10, pady=10)

        entree_mesure = ctk.CTkEntry(resultats_window)
        entree_mesure.grid(row=i + 1, column= 1, padx=10, pady=10)
        champs_mesures.append(entree_mesure)

        voyant_mesure = ctk.CTkCanvas(resultats_window, width=100, height=50, bg="red")
        voyant_mesure.grid(row=i + 1, column= 2, padx=10, pady=10)
        voyant_mesure.create_text(50, 25, text="Défaut", fill="white", font=("Arial", 14, "bold"))
        voyants_mesure.append(voyant_mesure)

        isolement_var = ctk.IntVar(value=0)
        isolement_vars.append(isolement_var)

        btn_defaut_isolement = ctk.CTkButton(resultats_window, text="OK", fg_color="green", text_color="white", 
                                         font=("Arial", 14, "bold"), width=70, height=35, 
                                         command=lambda i=i: toggle_defaut_isolement(i))
        btn_defaut_isolement.grid(row=i + 1, column= 3, padx=10, pady=10)
        boutons_defaut_isolement.append(btn_defaut_isolement)

    # Fonction pour vérifier la mesure
    def verifier():
        global etat_mesure  # Utiliser la variable globale
        global val_mes  # Déclarer val_mes comme global
        etat_mesure = []  # Réinitialiser la liste des états des mesures
        val_mes = []  # Réinitialiser la liste des valeurs mesurées
        for i, ref_mesure in enumerate(noms_donnees):
            try:
                valeur_mesure = float(champs_mesures[i].get())  # Récupérer la valeur entrée par l'utilisateur
                val_mes.append([valeur_mesure])  # Ajouter la mesure à val_mes en tant que liste
            except ValueError:
                messagebox.showerror("Erreur", f"Valeur non valide pour {ref_mesure}. Veuillez entrer un nombre.")
                return

            voyants_mesure[i].delete("all")  # Effacer tous les anciens textes avant d'afficher le nouvel état

            if verifier_mesure(ref_mesure, [valeur_mesure]):  # Vérification de la mesure
                etat_mesure.append(True)  # Ajouter True si la mesure est correcte
                voyants_mesure[i].config(bg="green")
                voyants_mesure[i].create_text(50, 25, text="OK", fill="white", font=("Arial", 14, "bold"))
            else:
                etat_mesure.append(False)  # Ajouter False si la mesure est incorrecte
                voyants_mesure[i].config(bg="red")
                voyants_mesure[i].create_text(50, 25, text="Défaut", fill="white", font=("Arial", 14, "bold"))
                
        bouton_sauvegarder.grid()  # Afficher le bouton de sauvegarde après vérification des mesures

    # Fonction pour sauvegarder la mesure
    def sauvegarder():
        global etat_mesure  # Utiliser la variable globale
        global val_mes  # Assurez-vous d'accéder à la bonne variable

        # Récupérer les valeurs d'état d'isolement depuis les variables associées
        etat_isolement = [isolement_vars[i].get() for i in range(len(noms_donnees))]

        # Conversion en valeurs booléennes
        etat_isolement_text = [False if etat == 1 else True for etat in etat_isolement]

        # Appel à la fonction de sauvegarde avec les valeurs converties
        sauvegarder_mesures_excel(noms_donnees, val_mes, etat_isolement_text, 
                                  etat_mesure, operateur_nom, cryomodule_num, nom_poste, resultats_window)

    # Bouton pour vérifier la mesure
    bouton_verifier = ctk.CTkButton(resultats_window, text="Vérifier la mesure", 
                                                width=200, height=50,
                                                font=("Arial", 15, "bold"), fg_color="#100bb0", text_color="white",
                                                command=verifier)
    bouton_verifier.grid(row=len(noms_donnees) + 1, column=0, columnspan=4, pady=10)

    # Bouton pour sauvegarder les résultats
    bouton_sauvegarder = ctk.CTkButton(resultats_window, text="Sauvegarder les résultats",
                                                width=200, height=50,
                                                font=("Arial", 15, "bold"), fg_color="#100bb0", text_color="white",
                                                command=sauvegarder)
    bouton_sauvegarder.grid(row=len(noms_donnees) + 2, column=0, columnspan=4, pady=10)
    bouton_sauvegarder.grid_remove()  # Masquer le bouton jusqu'à la vérification

    parent.withdraw()  # Masquer la fenêtre principale
    
# Fonction pour lancer la mesure et vérifier les résultats
def lancer_mesure(references_mesures, valeurs_mesures, etat_mesure, etat_isolement, voyants_mesure, voyants_isolement, bouton_sauvegarder):
    # Créer une liste combinée des canaux des trois listes en conservant l'ordre FW1, TW2, FW3
    channels = source_channels_FW1 + source_channels_TW2 + source_channels_FW3
    sense_channels = sense_channels_FW1 + [None] * len(source_channels_TW2) + sense_channels_FW3  # Aucun sense channel pour TW2

    for i, ref_mesure in enumerate(references_mesures):
        valeurs_mesurees = None  # Initialise la variable pour les valeurs mesurées
        
        # On essaie de mesurer selon la position dans la liste combinée
        if i < len(channels):
            channel = channels[i]
            sense_channel = sense_channels[i]
            
            # Si le canal provient de FW1 ou FW3, utiliser Mesure4W
            if sense_channel is not None:  # Cas pour FW1 ou FW3
                valeurs_mesurees = Mesure4W([channel], [sense_channel])
            else:  # Cas pour TW2
                valeurs_mesurees = Mesure2W([channel])

        # Si aucune mesure n'a été effectuée, afficher un message d'erreur et passer à la sonde suivante
        if valeurs_mesurees is None:
            print(f"Aucune mesure disponible pour la sonde {i}.")
            continue  # Passer à la sonde suivante

        # Mettre à jour la liste des valeurs mesurées
        valeurs_mesures[i] = valeurs_mesurees
        print(ref_mesure)
        # Mettre à jour l'affichage de la résistance mesurée dans la fenêtre
        label_valeur = ctk.CTkLabel(voyants_mesure[i].master, text=f"{valeurs_mesurees[0]:.2f} Ω")  # Ajouter l'unité
        label_valeur.grid(row=i+1, column=1, padx=10, pady=10)
        label_valeur.update()  # Mettre à jour immédiatement l'affichage de la fenêtre

        # Mesurer l'isolement pour la sonde correspondante
        etat_isolement[i] = verifier_isolement([channel])[0]
        
        # Vérifier l'état de la mesure et mettre à jour la liste etat_mesure
        etat_mesure[i] = verifier_mesure(ref_mesure, valeurs_mesures[i])  # Appel à la fonction verifier_mesure
        voyants_mesure[i].delete("all")  # Effacer tous les anciens textes avant d'afficher le nouvel état

        # Mise à jour des voyants pour l'état de la mesure
        if etat_mesure[i]:
            voyants_mesure[i].config(bg="green")
            voyants_mesure[i].create_text(50, 25, text="OK", fill="white", font=("Arial", 14, "bold"))
        else:
            voyants_mesure[i].config(bg="red")
            voyants_mesure[i].create_text(50, 25, text="Défaut", fill="white", font=("Arial", 14, "bold"))

        # Mise à jour des voyants pour l'état d'isolement
        voyants_isolement[i].delete("all")  # Effacer tous les anciens textes avant d'afficher le nouvel état
        if etat_isolement[i]:  # Utiliser l'état spécifique pour chaque sonde
            voyants_isolement[i].config(bg="green")
            voyants_isolement[i].create_text(50, 25, text="OK", fill="white", font=("Arial", 14, "bold"))
        else:
            voyants_isolement[i].config(bg="red")
            voyants_isolement[i].create_text(50, 25, text="Défaut", fill="white", font=("Arial", 14, "bold"))
        
        voyants_mesure[i].update()
        voyants_isolement[i].update()

        # Affichage pour vérifier les résultats dans la console
        print(f"Etat isolement pour sonde {i+1} : {etat_isolement[i]}, Etat mesure pour sonde {i+1} : {etat_mesure[i]}")

        # Ajout d'une temporisation (optionnel) pour laisser du temps entre les mesures
        time.sleep(1)  # Temporisation de 1 seconde entre chaque itération
        
    bouton_sauvegarder.grid()  # Afficher le bouton de sauvegarde après la mesure