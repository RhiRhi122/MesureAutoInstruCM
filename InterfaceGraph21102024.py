import customtkinter as ctk
from deABE import Etape_2_ABE
from DABE import Etape_D_ABE
from HABE import Etape_H_ABE
from JABE import Etape_J_ABE
from APAS import Etape_A_PAS
from BPAS import Etape_B_PAS
from CCOS_modPZ import Etape_C_COS
from ECOS import Etape_E_COS
from ACRY import Etape_A_CRY
from BCRY import Etape_B_CRY
from CCRY import Etape_C_CRY
from ECRY import Etape_E_CRY
from ACLO import Etape_A_CLO
from ICLO import Etape_I_CLO
from SondeUnique import controle_sonde_unique
from SondeUniqueManuelle import controle_sonde_manuel
from BrideSidePort import BrideSidePortControle
from TP1 import TP1Controle
from TP2 import TP2Controle
from TP3 import TP3Controle
from IP1 import IP1Controle
from IP2 import IP2Controle
from IP3 import IP3Controle
from IP4 import IP4Controle

# Variables pour stocker le numéro du cryomodule et le nom de l'opérateur
cryomodule_num = ""
operateur_nom = ""
entree_cryomodule = None  # Déclaration initiale
entree_operateur = None    # Déclaration initiale
A_M = "auto"  # Valeur initiale

# Fonction pour basculer entre Auto et Manuel
def toggle_mode():
    global A_M, switch_mode
    A_M = "manuel" if A_M == "auto" else "auto"
    switch_mode.configure(text="Mode \n Manuel")
    print(A_M)
    
# Fonction appelée pour sauvegarder les valeurs entrées
def sauvegarder_donnees():
    global cryomodule_num, operateur_nom, entree_cryomodule, entree_operateur
    if entree_cryomodule and entree_operateur:  # Vérifier si les entrées ne sont pas None
        cryomodule_num = entree_cryomodule.get().strip()
        operateur_nom = entree_operateur.get().strip()
        if not cryomodule_num or not operateur_nom:
            ctk.CTkMessagebox.show_warning("Champs manquants", "Veuillez entrer le numéro du cryomodule et le nom de l'opérateur.")
            return False
        print(f"Cryomodule: {cryomodule_num}, Opérateur: {operateur_nom}")
        return True
    return False

# Fonction appelée lorsque l'un des boutons est cliqué
def bouton_clique(nom):
    if not sauvegarder_donnees():
        return  # Ne pas continuer si les données ne sont pas valides
    print(f"Bouton {nom} cliqué")  # Affiche le bouton appuyé dans le shell

    # Ouvre la fenêtre correspondante avec la fenêtre principale comme parent
    if nom == "2-ABE":
        Etape_2_ABE(fenetre_principale, operateur_nom, cryomodule_num, A_M)  # Passer la fenêtre principale
    elif nom == "D-ABE":
        Etape_D_ABE(fenetre_principale, operateur_nom, cryomodule_num, A_M)  # Passer la fenêtre principale
    elif nom == "H-ABE":
        Etape_H_ABE(fenetre_principale, operateur_nom, cryomodule_num, A_M)  # Passer la fenêtre principale
    elif nom == "J-ABE":
        Etape_J_ABE(fenetre_principale, operateur_nom, cryomodule_num, A_M)  # Passer la fenêtre principale
    elif nom == "A-PAS":
        Etape_A_PAS(fenetre_principale, operateur_nom, cryomodule_num, A_M)  # Passer la fenêtre principale
    elif nom == "B-PAS":
        Etape_B_PAS(fenetre_principale, operateur_nom, cryomodule_num, A_M)  # Passer la fenêtre principale
    elif nom == "C-COS":
        Etape_C_COS(fenetre_principale, operateur_nom, cryomodule_num, A_M)  # Passer la fenêtre principale
    elif nom == "E-COS":
        Etape_E_COS(fenetre_principale, operateur_nom, cryomodule_num, A_M)  # Passer la fenêtre principale
    elif nom == "A-CRY":
        Etape_A_CRY(fenetre_principale, operateur_nom, cryomodule_num, A_M)  # Passer la fenêtre principale
    elif nom == "B-CRY":
        Etape_B_CRY(fenetre_principale, operateur_nom, cryomodule_num, A_M)  # Passer la fenêtre principale
    elif nom == "C-CRY":
        Etape_C_CRY(fenetre_principale, operateur_nom, cryomodule_num, A_M)  # Passer la fenêtre principale
    elif nom == "E-CRY":
        Etape_E_CRY(fenetre_principale, operateur_nom, cryomodule_num, A_M)  # Passer la fenêtre principale
    elif nom == "A-CLO":
        Etape_A_CLO(fenetre_principale, operateur_nom, cryomodule_num, A_M)  # Passer la fenêtre principale
    elif nom == "I-CLO":
        Etape_I_CLO(fenetre_principale, operateur_nom, cryomodule_num, A_M)  # Passer la fenêtre principale

# Fonction pour choisir la bonne fonction selon le mode
def lancer_mesure_sonde():
    if A_M == "auto":
        if not sauvegarder_donnees():  # Appeler sauvegarder_donnees() une seule fois
            return  # Ne pas continuer si les données ne sont pas valides
        controle_sonde_unique(fenetre_principale, operateur_nom, cryomodule_num)
    else:
        if not sauvegarder_donnees():  # Appeler sauvegarder_donnees() une seule fois
            return  # Ne pas continuer si les données ne sont pas valides
        controle_sonde_manuel(fenetre_principale, operateur_nom, cryomodule_num)
    
# Fonction appelée pour la mesure de la bride Side Port
def lancer_mesure_bride_side_port():
    if not sauvegarder_donnees():  # Appeler sauvegarder_donnees() une seule fois
        return  # Ne pas continuer si les données ne sont pas valides
    BrideSidePortControle(fenetre_principale, operateur_nom, cryomodule_num, A_M)

# Fonctions pour les mesures des Top Ports
def lancer_mesure_tp1():
    if not sauvegarder_donnees():  # Vérifier les données
        return  # Ne pas continuer si les données ne sont pas valides
    TP1Controle(fenetre_principale, operateur_nom, cryomodule_num, A_M)  # Appeler la fonction TP1

def lancer_mesure_tp2():
    if not sauvegarder_donnees():  # Vérifier les données
        return  # Ne pas continuer si les données ne sont pas valides
    TP2Controle(fenetre_principale, operateur_nom, cryomodule_num, A_M)  # Appeler la fonction TP2

def lancer_mesure_tp3():
    if not sauvegarder_donnees():  # Vérifier les données
        return  # Ne pas continuer si les données ne sont pas valides
    TP3Controle(fenetre_principale, operateur_nom, cryomodule_num, A_M)  # Appeler la fonction TP3

# Fonctions pour les mesures des Instrumentation Ports
def lancer_mesure_ip1():
    if not sauvegarder_donnees():  # Vérifier les données
        return  # Ne pas continuer si les données ne sont pas valides
    IP1Controle(fenetre_principale, operateur_nom, cryomodule_num, A_M)  # Appeler la fonction IP1

def lancer_mesure_ip2():
    if not sauvegarder_donnees():  # Vérifier les données
        return  # Ne pas continuer si les données ne sont pas valides
    IP2Controle(fenetre_principale, operateur_nom, cryomodule_num, A_M)  # Appeler la fonction IP2

def lancer_mesure_ip3():
    if not sauvegarder_donnees():  # Vérifier les données
        return  # Ne pas continuer si les données ne sont pas valides
    IP3Controle(fenetre_principale, operateur_nom, cryomodule_num, A_M)  # Appeler la fonction IP3

def lancer_mesure_ip4():
    if not sauvegarder_donnees():  # Vérifier les données
        return  # Ne pas continuer si les données ne sont pas valides
    IP4Controle(fenetre_principale, operateur_nom, cryomodule_num, A_M)  # Appeler la fonction IP4

# Fonction pour créer la fenêtre principale
def create_main_window():
    global entree_cryomodule, entree_operateur, fenetre_principale  # Utiliser global pour accéder aux entrées

    # Création de la fenêtre principale
    fenetre_principale = ctk.CTk()
    fenetre_principale.title("Interface de mesure")

    # Création du champ pour le numéro du cryomodule
    label_cryomodule = ctk.CTkLabel(fenetre_principale, text="Numéro du Cryomodule :")
    label_cryomodule.grid(row=0, column=2, columnspan=2, padx=10, pady=5)
    entree_cryomodule = ctk.CTkEntry(fenetre_principale)
    entree_cryomodule.insert(0, "CM0")  # Pré-remplir le champ avec "CM"
    entree_cryomodule.grid(row=0, column=3, columnspan=3, padx=10, pady=5)

    # Création du champ pour le nom de l'opérateur
    label_operateur = ctk.CTkLabel(fenetre_principale, text="Nom de l'opérateur :")
    label_operateur.grid(row=1, column=2, columnspan=2, padx=10, pady=5)
    entree_operateur = ctk.CTkEntry(fenetre_principale)
    entree_operateur.insert(0, "JD")  # Pré-remplir le champ avec "CM"
    entree_operateur.grid(row=1, column=3, columnspan=3, padx=10, pady=5)

    # Créer un cadre labellisé pour regrouper les boutons de contrôle des sondes 
    cadre_mode = ctk.CTkFrame(fenetre_principale, width=10, height=20)
    cadre_mode.grid(row=0, column=6, rowspan=2, columnspan=3, padx=10, pady=10)

    # Ajouter un titre au cadre
    label_titre_cadre_mode = ctk.CTkLabel(cadre_mode, text="Choix du Mode", font=("Arial", 16, "italic", "bold"), text_color="black")
    label_titre_cadre_mode.grid(row=1, column=0, columnspan=3, padx=10, pady=10)  # Le placer au-dessus du cadre

    # Ajouter un label au-dessus du bouton pour afficher le mode actuel
    global label_mode
    label_mode = ctk.CTkLabel(cadre_mode, text="Mode \n Auto", font=("Arial", 15, "bold"), text_color="black")
    label_mode.grid(row=2, column=0, padx=10, pady=0)
     
    # Switch pour changer le mode
    global switch_mode
    switch_mode = ctk.CTkSwitch(cadre_mode, text="Mode \n Manuel", width=100, height=50,
                                font=("Arial", 15, "bold"), text_color="black",
                                command=toggle_mode)
    switch_mode.grid(row=2, column=1, padx=10, pady=0)

    # Créer un cadre labellisé pour regrouper les boutons de contrôle des sondes
    cadre_controle_sondes = ctk.CTkFrame(fenetre_principale, width=10, height=10)
    cadre_controle_sondes.grid(row=2, column=0, columnspan=3, padx=0, pady=10)

    # Ajouter un titre au cadre
    label_titre_cadre_controle_sondes = ctk.CTkLabel(cadre_controle_sondes, text="Choix de l'étape de contrôle", font=("Arial", 16, "italic", "bold"), text_color="black")
    label_titre_cadre_controle_sondes.grid(row=0, column=0, columnspan=3, padx=10, pady=0)  # Le placer au-dessus du cadre

    # Liste des noms des boutons
    noms_boutons = [
        "2-ABE", "D-ABE", "H-ABE", "F-ABE", 
        "A-PAS", "B-PAS", "C-COS", "E-COS",
        "A-CRY", "B-CRY", "C-CRY","E-CRY",
        "A-CLO", "I-CLO"
    ]

    # Nombre de colonnes
    colonnes = 3

    # Création des boutons dans le LabelFrame
    for index, nom in enumerate(noms_boutons):
        # Calculer la ligne et la colonne
        ligne = index // colonnes
        colonne = index % colonnes

        bouton = ctk.CTkButton(cadre_controle_sondes, text=nom, width=100, height=50,  # Taille fixe pour tous les boutons
                               font=("Arial", 15, "bold"),  # Police en gras
                               fg_color="#100bb0",
                               text_color="white",
                               command=lambda n=nom: (bouton_clique(n)))  # Passer le nom du bouton

        bouton.grid(row=ligne+1, column=colonne, padx=20, pady=10)

    # Cadre pour le bouton "Sonde Unique"
    cadre_instru_unique = ctk.CTkFrame(fenetre_principale, width=20, height=20)
    cadre_instru_unique.grid(row=2, column=8, padx=10, pady=5)  # Placez-le à droite du cadre de sonde unique

    # Ajouter un titre au cadre
    label_titre_cadre_instru_unique = ctk.CTkLabel(cadre_instru_unique, text="Contrôle d'une \n sonde unique", font=("Arial", 16, "italic", "bold"), text_color="black")
    label_titre_cadre_instru_unique.grid(row=0, column=0, padx=10, pady=5)  # Le placer au-dessus du cadre

    # Bouton pour lancer la mesure d'une sonde unique
    bouton_sonde_unique = ctk.CTkButton(cadre_instru_unique, text="Sonde Unique", width=100, height=50,
                                    font=("Arial", 15, "bold"), fg_color="#100bb0",text_color="white",
                                    command=lancer_mesure_sonde)
    bouton_sonde_unique.grid(row=2, column=0, padx=10, pady=5)

    # Cadre pour le bouton "Side Port"
    cadre_instru_side = ctk.CTkFrame(fenetre_principale, width=20, height=20)
    cadre_instru_side.grid(row=2, column=4, padx=10, pady=5)  # Placez-le à droite du cadre de sonde unique

    # Ajouter un titre au cadre
    label_titre_cadre_side = ctk.CTkLabel(cadre_instru_side, text="Contrôle instru \n Side Port", font=("Arial", 16, "italic", "bold"), text_color="black")
    label_titre_cadre_side.grid(row=0, column=0, padx=10, pady=5)  # Le placer au-dessus du cadre
   
    # Bouton pour lancer la mesure "Bride Side Port"
    bouton_bride_side_port = ctk.CTkButton(cadre_instru_side, text="Side Port", width=100, height=50,
                                           font=("Arial", 15, "bold"),fg_color="#100bb0",text_color="white",
                                       command=lancer_mesure_bride_side_port)
    bouton_bride_side_port.grid(row=2, column=0, padx=15, pady=10)

    # Cadre pour le bouton "Top Port"
    cadre_top_port = ctk.CTkFrame(fenetre_principale, width=20, height=20)
    cadre_top_port.grid(row=2, column=5, padx=10, pady=10)  # Placez-le à droite du cadre de sonde unique

    # Ajouter un titre au cadre
    label_titre_cadre_top_port = ctk.CTkLabel(cadre_top_port, text="Contrôle Instru \n Top Port", font=("Arial", 16, "italic", "bold"), text_color="black")
    label_titre_cadre_top_port.grid(row=0, column=0, padx=10, pady=5)  # Le placer au-dessus du cadre

    # Création des boutons TP1, TP2, TP3
    for i, nom in enumerate(["TP1", "TP2", "TP3"]):
        
        # Associer chaque bouton à la fonction correspondante
        bouton_tp = ctk.CTkButton(cadre_top_port, text=nom, width=100, height=50,
                                font=("Arial", 15, "bold"), fg_color="#100bb0",text_color="white",
                                command=[lancer_mesure_tp1, lancer_mesure_tp2, lancer_mesure_tp3][i])  
        bouton_tp.grid(row=i+1, column=0, padx=10, pady=10)

    # Cadre pour le bouton "Instrumentation Port"
    cadre_instru_port = ctk.CTkFrame(fenetre_principale, width=20, height=20)
    cadre_instru_port.grid(row=2, column=6, padx=10, pady=10)  # Placez-le à droite du cadre de sonde unique

    # Ajouter un titre au cadre
    label_titre_cadre_instru_port = ctk.CTkLabel(cadre_instru_port, text="Contrôle Instru \n Enceinte", font=("Arial", 16, "italic", "bold"), text_color="black")
    label_titre_cadre_instru_port.grid(row=0, column=0, padx=10, pady=5)  # Le placer au-dessus du cadre

    # Création des boutons IP1, IP2, IP3, IP4
    for i, nom in enumerate(["IP1", "IP2", "IP3", "IP4"]):
        
        # Associer chaque bouton à la fonction correspondante
        bouton_tp = ctk.CTkButton(cadre_instru_port, text=nom, width=100, height=50,
                                  font=("Arial", 15, "bold"), fg_color="#100bb0",text_color="white",
                              command=[lancer_mesure_ip1, lancer_mesure_ip2, lancer_mesure_ip3, lancer_mesure_ip4][i])  
        bouton_tp.grid(row=i+1, column=0, padx=10, pady=10)

    # Boucle principale de l'application
    fenetre_principale.mainloop()

# Appel pour créer la fenêtre principale
create_main_window()
