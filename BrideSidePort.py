# BrideSidePort.py
import customtkinter as ctk
from math import *
from tkinter import messagebox
from VerifValeursCiblesSondes import verifier_mesure, valeurs_cibles
from SauvExcel import sauvegarder_mesures_excel
from MesureResistance import Mesure4W, Mesure2W
from MesureIsolement import verifier_isolement
import time

# Nom poste
nom_poste = "Side Port"

etat_mesure = []

# Données Channels Utilisés
source_channels_FW1 = [101, 102, 103, 104, 105, 106, 107, 108]
sense_channels_FW1 = [111, 112, 113, 114, 115, 116, 117, 118]
source_channels_TW2 = []
source_channels_FW3 = [301, 302, 303, 304, 305, 306, 307, 308]
sense_channels_FW3 = [311, 312, 313, 314, 315, 316, 317, 318]

# Fonction pour afficher la matrice dans une nouvelle fenêtre
def BrideSidePortControle(parent, operateur_nom, cryomodule_num, A_M):
    top = ctk.CTkToplevel()
    top.title("Etape : Contrôle Bride Side Port")
    top.attributes("-topmost", True)  # S'assurer que cette fenêtre est au premier plan

    noms_donnees = ["TX-030A", "TX-030B", "TX-031A", "TX-031B", "TX-032A", "TX-032B", "TX-033A", "TX-033B",
                    "TX-035A", "TX-035B", "TX-036A", "TX-036B", "TX-041A", "TX-041B", "TX-042A", "TX-042B"]
    valeurs_mesures = [0] * len(noms_donnees)  # Initialise à zéro
    etat_mesure = [False] * len(noms_donnees)  # Toutes les mesures sont par défaut OK
    etat_isolement = [False] * len(noms_donnees)  # Toutes les isolations sont par défaut OK

    # En-têtes des colonnes
    entete_ref = ctk.CTkLabel(top, text="Référence du Capteur", font=("Arial", 14, "italic", "bold"), text_color="#13025e")
    entete_ref.grid(row=0, column=0, padx=10, pady=5)

    entete_resistance = ctk.CTkLabel(top, text="Résistance (Ω)", font=("Arial", 14, "italic", "bold"), text_color="#13025e")
    entete_resistance.grid(row=0, column=1, padx=10, pady=5)

    entete_defaut_mesure = ctk.CTkLabel(top, text="Défaut de Mesure", font=("Arial", 14, "italic", "bold"), text_color="#13025e")
    entete_defaut_mesure.grid(row=0, column=2, padx=10, pady=5)

    entete_defaut_isolement = ctk.CTkLabel(top, text="Défaut Isolement", font=("Arial", 14, "italic", "bold"), text_color="#13025e")
    entete_defaut_isolement.grid(row=0, column=3, padx=10, pady=5)
    
    # En-têtes des colonnes pour le second groupe de sondes
    entete_ref2 = ctk.CTkLabel(top, text="Référence du Capteur", font=("Arial", 14, "italic", "bold"), text_color="#13025e")
    entete_ref2.grid(row=0, column=4, padx=10, pady=5)

    entete_resistance2 = ctk.CTkLabel(top, text="Résistance (Ω)", font=("Arial", 14, "italic", "bold"), text_color="#13025e")
    entete_resistance2.grid(row=0, column=5, padx=10, pady=5)

    entete_defaut_mesure2 = ctk.CTkLabel(top, text="Défaut de Mesure", font=("Arial", 14, "italic", "bold"), text_color="#13025e")
    entete_defaut_mesure2.grid(row=0, column=6, padx=10, pady=5)

    entete_defaut_isolement2 = ctk.CTkLabel(top, text="Défaut Isolement", font=("Arial", 14, "italic", "bold"), text_color="#13025e")
    entete_defaut_isolement2.grid(row=0, column=7, padx=10, pady=5)
   
    if A_M == "auto":
        # Créer des listes pour stocker les voyants de mesure et d'isolement
        voyants_mesure = []
        voyants_isolement = []

        # Ajouter les colonnes de données, en utilisant deux colonnes pour les capteurs
        for i, nom in enumerate(noms_donnees):
            col = i % 2  # Utilise le reste pour décider de la colonne
            row = i // 2 + 1  # Utilise la division entière pour la ligne
            
            label_nom = ctk.CTkLabel(top, text=nom, font=("Arial", 14, "bold"))
            label_nom.grid(row=row, column=col * 4, padx=10, pady=10)

            label_valeur = ctk.CTkLabel(top, text=str(valeurs_mesures[i]))
            label_valeur.grid(row=row, column=col * 4 + 1, padx=10, pady=10)

            couleur_mesure = "green" if etat_mesure[i] else "red"
            voyant_mesure = ctk.CTkCanvas(top, width=100, height=50, bg=couleur_mesure)
            voyant_mesure.grid(row=row, column=col * 4 + 2, padx=10, pady=10)
            voyants_mesure.append(voyant_mesure)  # Ajouter le voyant à la liste

            if not etat_mesure[i]:
                voyant_mesure.create_text(50, 25, text="Défaut", fill="white", font=("Arial", 14, "bold"))

            couleur_isolement = "green" if etat_isolement[i] else "red"
            voyant_isolement = ctk.CTkCanvas(top, width=100, height=50, bg=couleur_isolement)
            voyant_isolement.grid(row=row, column=col * 4 + 3, padx=10, pady=10)
            voyants_isolement.append(voyant_isolement)  # Ajouter le voyant à la liste

            if not etat_isolement[i]:
                voyant_isolement.create_text(50, 25, text="Défaut", fill="white", font=("Arial", 14, "bold"))

        bouton_lancer_mesure = ctk.CTkButton(top, text="Lancer la mesure", width=200, height=50,
                                        font=("Arial", 15, "bold"), fg_color="#100bb0", text_color="white",
                                        command=lambda: lancer_mesure(noms_donnees, valeurs_mesures, etat_mesure, etat_isolement, voyants_mesure, voyants_isolement, bouton_sauvegarder))
        bouton_lancer_mesure.grid(row=len(noms_donnees) + 1, column=2, columnspan=4, pady=10)
        
        bouton_sauvegarder = ctk.CTkButton(top, text="Sauvegarder mesures", width=200, height=50,
                                        font=("Arial", 15, "bold"), fg_color="#100bb0", text_color="white",
            command=lambda: sauvegarder_mesures_excel(noms_donnees, valeurs_mesures, etat_isolement, etat_mesure, operateur_nom, cryomodule_num, nom_poste, top))
        bouton_sauvegarder.grid(row=len(noms_donnees) + 2, column=2, columnspan=4, pady=10)
        bouton_sauvegarder.grid_remove()  # Masquer le bouton au début

        parent.withdraw()  # Cacher la fenêtre principale
        
    elif A_M == "manuel":
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
            col = i % 2  # Utilise le reste pour décider de la colonne
            row = i // 2 + 1  # Utilise la division entière pour la ligne
            
            label_reference = ctk.CTkLabel(top, text=ref_mesure)
            label_reference.grid(row=row, column=col * 4, padx=10, pady=10)

            entree_mesure = ctk.CTkEntry(top)
            entree_mesure.grid(row=row, column=col * 4 + 1, padx=10, pady=10)
            champs_mesures.append(entree_mesure)

            voyant_mesure = ctk.CTkCanvas(top, width=100, height=50, bg="red")
            voyant_mesure.grid(row=row, column=col * 4 + 2, padx=10, pady=10)
            voyant_mesure.create_text(50, 25, text="Défaut", fill="white", font=("Arial", 14, "bold"))
            voyants_mesure.append(voyant_mesure)

            isolement_var = ctk.IntVar(value=0)
            isolement_vars.append(isolement_var)

            btn_defaut_isolement = ctk.CTkButton(top, text="OK", fg_color="green", text_color="white",
                                             font=("Arial", 14, "bold"), width=70, height=35, 
                                             command=lambda i=i: toggle_defaut_isolement(i))
            btn_defaut_isolement.grid(row=row, column=col * 4 + 3, padx=10, pady=10)
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
                                      etat_mesure, operateur_nom, cryomodule_num, nom_poste, top)

        # Bouton pour vérifier la mesure
        bouton_verifier = ctk.CTkButton(top, text="Vérifier la mesure", 
                                                    width=200, height=50,
                                                    font=("Arial", 15, "bold"), fg_color="#100bb0", text_color="white",
                                                    command=verifier)
        bouton_verifier.grid(row=len(noms_donnees) + 1, column=2, columnspan=4, pady=10)

        # Bouton pour sauvegarder les résultats
        bouton_sauvegarder = ctk.CTkButton(top, text="Sauvegarder les résultats",
                                                    width=200, height=50,
                                                    font=("Arial", 15, "bold"), fg_color="#100bb0", text_color="white",
                                                    command=sauvegarder)
        bouton_sauvegarder.grid(row=len(noms_donnees) + 2, column=2, columnspan=4, pady=10)
        bouton_sauvegarder.grid_remove()  # Masquer le bouton jusqu'à la vérification

    parent.withdraw()  # Masquer la fenêtre principale

# Fonction pour lancer la mesure et vérifier les résultats
def lancer_mesure(references_mesures, valeurs_mesures, etat_mesure, etat_isolement, voyants_mesure, voyants_isolement, bouton_sauvegarder):
    # Créer une liste combinée des canaux des trois listes en conservant l'ordre FW1, TW2, FW3
    channels = source_channels_FW1 + source_channels_TW2 + source_channels_FW3
    sense_channels = sense_channels_FW1 + [None] * len(source_channels_TW2) + sense_channels_FW3  # Aucun sense channel pour TW2

    for i, ref_mesure in enumerate(references_mesures):
        valeurs_mesurees = None  # Initialise la variable pour les valeurs mesurées
        
        col = i % 2  # Utilise le reste pour décider de la colonne
        row = i // 2 + 1  # Utilise la division entière pour la ligne
        
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
        label_valeur.grid(row=row, column=col * 4 + 1, padx=10, pady=10)
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