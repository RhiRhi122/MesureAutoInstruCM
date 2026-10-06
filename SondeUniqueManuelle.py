import customtkinter as ctk
from tkinter import messagebox
from VerifValeursCiblesSondes import verifier_mesure
from SauvExcel import sauvegarder_mesures_excel

def controle_sonde_manuel(parent, operateur_nom, cryomodule_num):
    etat_mesure = []  # Déclarez etat_mesure ici pour qu'il soit accessible
    val_mes = []
    entree_reference = None  # Déclarez une variable ici
    nom_poste = ""  # Déclarez la variable pour le nom du poste ici
    
    # Fonction pour demander l'étape et la référence de la sonde
    def demander_etape_reference(etape_pre_remplie = None):
        nonlocal entree_reference  # Utiliser nonlocal pour accéder à la variable
        for widget in parent.winfo_children():
            widget.destroy()
        
        # Saisie de l'étape
        label_etape = ctk.CTkLabel(parent, text="Étape de l'assemblage :", font=("Arial", 15))
        label_etape.grid(row=0, column=0, pady=10)
        entree_etape = ctk.CTkEntry(parent)
        entree_etape.grid(row=1, column=0, padx=20, pady=5)
        
        # Pré-remplir le champ de l'étape si elle est déjà définie
        if etape_pre_remplie:
            entree_etape.insert(0, etape_pre_remplie)

        # Saisie de la référence de la sonde
        label_reference = ctk.CTkLabel(parent, text="Référence de la sonde :", font=("Arial", 15))
        label_reference.grid(row=2, column=0, pady=10)
        entree_reference = ctk.CTkEntry(parent)
        entree_reference.grid(row=3, column=0, padx=20, pady=5)
               
        # Fonction de validation de l'étape et de la référence
        def valider_etape_reference():
            nonlocal nom_poste  # Indiquez que vous voulez utiliser la variable nonlocal
            etape = entree_etape.get()
            reference = entree_reference.get().upper()

            if not etape:
                messagebox.showerror("Erreur", "Veuillez entrer une étape.")
                return
            if not reference:
                messagebox.showerror("Erreur", "Veuillez entrer une référence.")
                return

            # Récupérer le nom de poste à partir de l'étape
            nom_poste = etape  # Mettez à jour nom_poste ici

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
        reponse = messagebox.askyesno("Confirmation", f"Voulez-vous réaliser la mesure manuelle pour la sonde '{type_sonde}' '{reference}' ?")

        if reponse:
            afficher_fenetre_mesure(reference, type_sonde, etape)  # Ouvrir la fenêtre de mesure si "Oui"
        else:
            demander_etape_reference(etape)  # Revenir à la fenêtre d'entrée de référence si "Non"

        # Fonction pour afficher la fenêtre de mesure
    def afficher_fenetre_mesure(reference, type_sonde, etape):
        global resultats_window

        # Vérifier si la fenêtre existe déjà et la détruire si nécessaire
        if 'resultats_window' in globals() and resultats_window.winfo_exists():
            resultats_window.destroy()

        # Créer une nouvelle fenêtre pour afficher les résultats
        resultats_window = ctk.CTkToplevel(parent)
        resultats_window.title(f"Résultats de Mesure - {type_sonde}")
        resultats_window.attributes("-topmost", True)

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

        entete_defaut_isolement = ctk.CTkLabel(resultats_window, text="Défaut Isolement \n (A VERIFIER)", font=("Arial", 10, "bold"))
        entete_defaut_isolement.grid(row=0, column=3, padx=10, pady=5)

        # Champs pour saisir les mesures
        champs_mesures = []
        voyants_mesure = []
        isolement_vars = []  # Stocker les états d'isolement

        for i, ref_mesure in enumerate(references_mesures):
            label_reference = ctk.CTkLabel(resultats_window, text=ref_mesure, font=("Arial", 14, "bold"))
            label_reference.grid(row=i + 1, column=0, padx=10, pady=10)

            entree_mesure = ctk.CTkEntry(resultats_window)
            entree_mesure.grid(row=i + 1, column=1, padx=10, pady=10)
            champs_mesures.append(entree_mesure)

            couleur_mesure = "red"  # Par défaut, on commence en rouge
            voyant_mesure = ctk.CTkCanvas(resultats_window, width=100, height=50, bg=couleur_mesure)
            voyant_mesure.grid(row=i + 1, column=2, padx=10, pady=10)
            voyant_mesure.create_text(50, 25, text="Défaut", fill="white", font=("Arial", 14, "bold"))
            voyants_mesure.append(voyant_mesure)
            
            isolement_var = ctk.IntVar(value=1)  # 0 pour "OK", 1 pour "Défaut"
            isolement_vars.append(isolement_var)
            
        # Fonction pour basculer l'état du bouton d'isolement
        def toggle_defaut_isolement(i):
            # Si le bouton est vert, on le passe au rouge pour indiquer un défaut
            if boutons_defaut_isolement[i].cget("fg_color") == "green":
                boutons_defaut_isolement[i].configure(fg_color="red", text="Défaut", text_color="white")
                isolement_vars[i].set(1)  # Mettre à jour la variable d'isolement pour indiquer un défaut
            else:
                # Si le bouton est rouge, on le passe au vert pour indiquer OK
                boutons_defaut_isolement[i].configure(fg_color="green", text="OK", text_color="white")
                isolement_vars[i].set(0)  # Mettre à jour la variable d'isolement pour indiquer OK



        # Création des boutons d'isolement pour chaque mesure
        isolement_vars = []  # Liste pour stocker l'état de chaque isolement (une ou deux valeurs selon le type de sonde)
        boutons_defaut_isolement = []

        for i in range(len(references_mesures)):
            isolement_var = ctk.IntVar(value=0)  # 0 pour "OK", 1 pour "Défaut"
            isolement_vars.append(isolement_var)

            btn_defaut_isolement = ctk.CTkButton(resultats_window, text="OK", fg_color="green", text_color="white", 
                                             font=("Arial", 14, "bold"), width=70, height=35, 
                                             command=lambda i=i: toggle_defaut_isolement(i))
            btn_defaut_isolement.grid(row=i + 1, column=3, padx=10, pady=10)
            boutons_defaut_isolement.append(btn_defaut_isolement)

        
        # Bouton pour sauvegarder la mesure
        def sauvegarder():
            # Récupérer les états d'isolement
            etat_isolement = [isolement_vars[i].get() for i in range(len(references_mesures))]

            # Convertir les états d'isolement en texte "True"/"False"
            etat_isolement_text = [False if etat == 1 else True for etat in etat_isolement]

            sauvegarder_mesures_excel(references_mesures, val_mes, etat_isolement_text, etat_mesure, operateur_nom, cryomodule_num, etape, resultats_window)

            # Réinitialiser les champs
            entree_reference.delete(0, ctk.END)  # Efface le champ de référence
            
            demander_etape_reference(etape_pre_remplie=nom_poste)         
            
        # Fonction pour vérifier la mesure
        def verifier():
            nonlocal etat_mesure  # Utilisez nonlocal pour accéder à la variable dans l'espace de noms englobant
            nonlocal val_mes  # On utilise nonlocal pour accéder à val_mes
            etat_mesure = []
            val_mes = []
            for i, ref_mesure in enumerate(references_mesures):
                try:
                    valeur_mesure = float(champs_mesures[i].get())  # Récupérer la valeur entrée
                    val_mes.append([valeur_mesure])
                except ValueError:
                    messagebox.showerror("Erreur", f"Valeur non valide pour {ref_mesure}. Veuillez entrer un nombre.")
                    return
                    
                valeur_mesure = [valeur_mesure]
                                
                # etat_mesure = verifier_mesure(ref_mesure, valeur_mesure)  # Appel à la fonction verifier_mesure
                voyants_mesure[i].delete("all")  # Effacer tous les anciens textes avant d'afficher le nouvel état

                if verifier_mesure(ref_mesure, valeur_mesure):  # Fonction à adapter selon vos besoins
                    etat_mesure.append(True)
                    voyants_mesure[i].config(bg="green")
                    voyants_mesure[i].create_text(50, 25, text="OK", fill="white", font=("Arial", 14, "bold"))
                else:
                    etat_mesure.append(False)  # Ajouter à la liste des états
                    voyants_mesure[i].config(bg="red")
                    voyants_mesure[i].create_text(50, 25, text="Défaut", fill="white", font=("Arial", 14, "bold"))
                    
            bouton_sauvegarder.grid()  # Afficher le bouton de sauvegarde après la mesure

            # Bouton pour vérifier la mesure
        bouton_verifier = ctk.CTkButton(resultats_window, text="Vérifier la mesure", 
                                                    width=200, height=50,
                                                    font=("Arial", 15, "bold"), fg_color="#100bb0", text_color="white",
                                                    command=verifier)
        bouton_verifier.grid(row=len(references_mesures) + 1, column=0, columnspan=4, pady=10)

        # Bouton pour sauvegarder les résultats
        bouton_sauvegarder = ctk.CTkButton(resultats_window, text="Sauvegarder les résultats",
                                                    width=200, height=50,
                                                    font=("Arial", 15, "bold"), fg_color="#100bb0", text_color="white",
                                                    command=sauvegarder)
        bouton_sauvegarder.grid(row=len(references_mesures) + 2, column=0, columnspan=4, pady=10)
        bouton_sauvegarder.grid_remove()  # Masquer le bouton jusqu'à la vérification

    # Lancer la demande d'étape et de référence au début
    demander_etape_reference()

