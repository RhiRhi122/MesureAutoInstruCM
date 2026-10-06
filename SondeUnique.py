import customtkinter as ctk
from math import *
from tkinter import messagebox
from VerifValeursCiblesSondes import verifier_mesure, valeurs_cibles
from SauvExcel import sauvegarder_mesures_excel
from MesureResistance import Mesure4W, Mesure2W, MesurePiezo
from MesureIsolement import verifier_isolement

# Fonction pour gérer la sélection de l'étape et de la sonde
def controle_sonde_unique(parent, operateur_nom, cryomodule_num):
    def demander_etape_reference(etape_pre_remplie=None):
        # Effacer tous les widgets actuels de la fenêtre parent
        for widget in parent.winfo_children():
            widget.destroy()

        # Label et entrée pour demander l'étape
        label_etape = ctk.CTkLabel(parent, text="À quelle étape de l'assemblage, \n cette mesure est-elle réalisée ?", font=("Arial", 15))
        label_etape.grid(row=0, column=0, pady=10)

        # Entrée de l'étape pré-remplie si disponible
        entree_etape = ctk.CTkEntry(parent)
        entree_etape.grid(row=1, column=0, padx=20, pady=5)
                      
        if etape_pre_remplie:
            entree_etape.insert(0, etape_pre_remplie)

        # Label et entrée pour la référence de la sonde
        label_reference = ctk.CTkLabel(parent, text="Entrez la référence de la sonde :", font=("Arial", 15))
        label_reference.grid(row=2, column=0, pady=10)

        entree_reference = ctk.CTkEntry(parent)
        entree_reference.grid(row=3, column=0, padx=20, pady=5)

        # Fonction de validation de l'étape et de la référence
        def valider_etape_reference():
            etape = entree_etape.get()
            reference = entree_reference.get().upper()

            if not etape:
                messagebox.showerror("Erreur", "Veuillez entrer une étape.")
                return
            if not reference:
                messagebox.showerror("Erreur", "Veuillez entrer une référence.")
                return

            # En fonction du préfixe de la référence, proposer les sondes correspondantes
            if reference.startswith("TX"):
                type_sonde = "Cernox"
            elif reference.startswith("TP"):
                type_sonde = "PT100"
            elif reference.startswith("FG"):
                type_sonde = "Fluxgate"
            elif reference.startswith("STM"):
                type_sonde = "Stepper"
            elif reference.startswith("PZ"):
                type_sonde = "Piézo"
            elif reference.startswith("HTR"):
                type_sonde = "Chaufferette"
            elif reference.startswith("LT"):
                type_sonde = "Jauge de Niveau"
            elif reference.startswith("TLS"):
                type_sonde = "Limit Switch"
            else:
                messagebox.showerror("Erreur", "Référence invalide ou non reconnue.")
                return

            # Ouvrir la fenêtre de résultats après validation
            valider_choix(reference, type_sonde, etape)

        # Bouton de validation de l'étape et de la référence
        bouton_valider = ctk.CTkButton(parent, text="Valider Étape et Référence", command=valider_etape_reference, width=60, height=10, font=("Arial", 15, "bold"))
        bouton_valider.grid(row=4, column=0, pady=20)

    # Fonction pour afficher la boîte de dialogue de confirmation
    def valider_choix(reference, type_sonde, etape):
        reponse = messagebox.askyesno("Confirmation", f"Voulez-vous réaliser la mesure pour la sonde '{type_sonde}' '{reference}' ?")

        if reponse:
            afficher_resultats(reference, type_sonde, etape)  # Ouvrir la fenêtre de mesure si "Oui"
        else:
            demander_etape_reference(etape)  # Revenir à la fenêtre d'entrée de référence si "Non"

    # Fonction pour afficher les résultats de la mesure
    def afficher_resultats(reference, type_sonde, etape):
        global resultats_window  # Déclaration de la variable globale ici

        # Vérifier si la fenêtre existe déjà et la détruire si nécessaire
        if 'resultats_window' in globals() and resultats_window.winfo_exists():
            resultats_window.destroy()

        # Créer une nouvelle fenêtre pour afficher les résultats
        resultats_window = ctk.CTkToplevel(parent)
        resultats_window.title(f"Résultats de Mesure - {type_sonde}")
        resultats_window.attributes("-topmost", True)

        # Valeurs par défaut : résistance nulle et voyants en défaut
        valeurs_mesures = [0, 0] if type_sonde in ["Stepper", "Fluxgate", "Piézo"] else [0]
        etat_mesure = [False, False] if type_sonde in ["Stepper", "Fluxgate", "Piézo"] else [False]
        etat_isolement = [False, False] if type_sonde in ["Stepper", "Fluxgate", "Piézo"] else [False]

        # Déterminer les références spécifiques pour les mesures multiples
        if type_sonde == "Stepper":
            references_mesures = [f"{reference}_W1", f"{reference}_W2"]
        elif type_sonde == "Fluxgate":
            references_mesures = [f"{reference}_WEx", f"{reference}_WFb"]
        elif type_sonde == "Piézo":
            references_mesures = [f"{reference}_C", f"{reference}_ESR"]
        else:
            references_mesures = [reference]

        # En-têtes des colonnes
        entete_ref = ctk.CTkLabel(resultats_window, text="Référence du Capteur", font=("Arial", 14, "italic", "bold"), text_color="#13025e")
        entete_ref.grid(row=0, column=0, padx=10, pady=5)

        if type_sonde == "Piézo":
            entete_resistance = ctk.CTkLabel(resultats_window, text="Résistance (Ω) \n Capacité (pC)", font=("Arial", 10, "bold"))
            entete_resistance.grid(row=0, column=1, padx=10, pady=5)
        else:
            entete_resistance = ctk.CTkLabel(resultats_window, text="Résistance (Ω)", font=("Arial", 14, "italic", "bold"), text_color="#13025e")
            entete_resistance.grid(row=0, column=1, padx=10, pady=5)

        entete_defaut_mesure = ctk.CTkLabel(resultats_window, text="Défaut de Mesure", font=("Arial", 14, "italic", "bold"), text_color="#13025e")
        entete_defaut_mesure.grid(row=0, column=2, padx=10, pady=5)

        entete_defaut_isolement = ctk.CTkLabel(resultats_window, text="Défaut Isolement", font=("Arial", 14, "italic", "bold"), text_color="#13025e")
        entete_defaut_isolement.grid(row=0, column=3, padx=10, pady=5)

        # Affichage des résultats pour chaque référence (1 ou 2 selon le type de sonde)
        voyants_mesure = []
        voyants_isolement = []

        for i, ref_mesure in enumerate(references_mesures):
            label_reference = ctk.CTkLabel(resultats_window, text=ref_mesure, font=("Arial", 14, "bold"))
            label_reference.grid(row=i + 1, column=0, padx=10, pady=10)

            label_resistance = ctk.CTkLabel(resultats_window, text=str(valeurs_mesures[i]))
            label_resistance.grid(row=i + 1, column=1, padx=10, pady=10)

            # Voyants pour les défauts de mesure et d'isolement
            couleur_mesure = "red"  # Par défaut, on commence en rouge
            voyant_mesure = ctk.CTkCanvas(resultats_window, width=100, height=50, bg=couleur_mesure)
            voyant_mesure.grid(row=i + 1, column=2, padx=10, pady=10)
            voyant_mesure.create_text(50, 25, text="Défaut", fill="white", font=("Arial", 14, "bold"))
            voyants_mesure.append(voyant_mesure)

            couleur_isolement = "red"  # Par défaut, on commence en rouge
            voyant_isolement = ctk.CTkCanvas(resultats_window, width=100, height=50, bg=couleur_isolement)
            voyant_isolement.grid(row=i + 1, column=3, padx=10, pady=10)
            voyant_isolement.create_text(50, 25, text="Défaut", fill="white", font=("Arial", 14, "bold"))
            voyants_isolement.append(voyant_isolement)

        # Bouton pour lancer la mesure
        bouton_lancer_mesure = ctk.CTkButton(resultats_window, text="Lancer la mesure", width=200, height=50,
                                    font=("Arial", 15, "bold"), fg_color="#100bb0", text_color="white",
                                    command=lambda: lancer_mesure(references_mesures, valeurs_mesures, etat_mesure, etat_isolement, voyants_mesure, voyants_isolement, bouton_fermer))
        bouton_lancer_mesure.grid(row=len(references_mesures) + 1, column=0, columnspan=4, pady=10)

        # Ajoutez ici le bouton Fermer
        bouton_fermer = ctk.CTkButton(resultats_window, text="Sauvegarder mesures", width=200, height=50,
                                    font=("Arial", 15, "bold"), fg_color="#100bb0", text_color="white",
                                    command=lambda: fermer_resultats(resultats_window, references_mesures, valeurs_mesures, etat_isolement, etat_mesure, operateur_nom, cryomodule_num, etape))
        bouton_fermer.grid(row=len(references_mesures) + 2, column=0, columnspan=4, pady=10)
        bouton_fermer.grid_remove()  # Masquer le bouton au début

    # Fonction pour fermer la fenêtre des résultats
    def fermer_resultats(fenetre, references_mesures, valeurs_mesures, etat_isolement, etat_mesure, operateur_nom, cryomodule_num, nom_poste):
        # Appeler la fonction de sauvegarde
        sauvegarder_mesures_excel(references_mesures, valeurs_mesures, etat_isolement, etat_mesure, operateur_nom, cryomodule_num, nom_poste, fenetre)
    
        global resultats_window
        if resultats_window.winfo_exists():
            resultats_window.destroy()
        demander_etape_reference(etape_pre_remplie=nom_poste)

    # Appel initial de la fonction pour demander l'étape
    demander_etape_reference()


# Fonction pour lancer la mesure et vérifier les résultats
def lancer_mesure(references_mesures, valeurs_mesures, etat_mesure, etat_isolement, voyants_mesure, voyants_isolement, bouton_fermer):
    
    # Données Channels Utilisés
    source_channels_FW3 = []
    sense_channels_FW3 = []
    
    ref_mes = references_mesures[0]
    print(ref_mes)
    
    if ref_mes.startswith("TX") or ref_mes.startswith("TP") or ref_mes.startswith("LT"):
        source_channels_FW1 = [101]
        sense_channels_FW1 = [111]
        source_channels_TW2 = []
    elif ref_mes.startswith("FG") or ref_mes.startswith("STM"):
        source_channels_FW1 = []
        sense_channels_FW1 = []
        source_channels_TW2 = [201, 202]
    elif ref_mes.startswith("HTR") or ref_mes.startswith("TLS"):
        source_channels_FW1 = []
        sense_channels_FW1 = []
        source_channels_TW2 = [201]
    elif ref_mes.startswith("PZ"):
        source_channels_FW1 = []
        sense_channels_FW1 = []
        source_channels_TW2 = [201, 201]
                  
    # Créer une liste combinée des canaux des trois listes en conservant l'ordre FW1, TW2, FW3

    channels = source_channels_FW1 + source_channels_TW2 + source_channels_FW3
    sense_channels = sense_channels_FW1 + [None] * len(source_channels_TW2) + sense_channels_FW3  # Aucun sense channel pour TW2

    for i, ref_mesure in enumerate(references_mesures):
        valeurs_mesurees = None  # Initialise la variable pour les valeurs mesurées
        
        # On essaie de mesurer selon la position dans la liste combinée
        if i < len(channels):
            channel = channels[i]
            sense_channel = sense_channels[i]
            
            # Cas des piézos (mesure de capacité ou ESR)
            if source_channels_TW2 == [201, 201]:
                # Pour la première occurrence, mesurer la capacité
                if i % 2 == 0:
                    print(f"Mesure de capacité pour la sonde {channel}")
                    C_ESR = 1
                    valeurs_mesurees = MesurePiezo([channel], C_ESR)
                # Pour la seconde occurrence, mesurer l'ESR
                else:
                    print(f"Mesure ESR pour la sonde {channel}")
                    C_ESR = 2
                    valeurs_mesurees = MesurePiezo([channel], C_ESR)
            else:
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
        if ref_mesure.endswith("_C"):
            label_valeur = ctk.CTkLabel(voyants_mesure[i].master, text=f"{valeurs_mesurees[0]:.2f} pC")  # Ajouter l'unité
        else:
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
        
    bouton_fermer.grid()  # Afficher le bouton de sauvegarde après la mesure