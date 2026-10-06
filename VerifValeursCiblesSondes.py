# Définir une table recensant la valeur cible et l'écart acceptable pour chaque type de sonde
valeurs_cibles = {
    "Cernox": {"valeur_cible": 41, "ecart_acceptable": 9}, #OK
    "PT100": {"valeur_cible": 108, "ecart_acceptable": 20}, #OK
    "Fluxgate_WFb": {"valeur_cible": 55, "ecart_acceptable": 10}, #OK
    "Fluxgate_WEx": {"valeur_cible": 21, "ecart_acceptable": 4}, #OK
    "Stepper_W1": {"valeur_cible": 1, "ecart_acceptable": 1},
    "Stepper_W2": {"valeur_cible": 1, "ecart_acceptable": 1},
    "Piezo_C": {"valeur_cible": 5.5, "ecart_acceptable": 1},
    "Piezo_ESR": {"valeur_cible": 10, "ecart_acceptable": 1},
    "Chaufferette": {"valeur_cible": 40, "ecart_acceptable": 20},
    "ThermoCouple": {"valeur_cible": 3, "ecart_acceptable": 20},
    "Jauge de niveau": {"valeur_cible": 300, "ecart_acceptable": 100},
    "Limit Switch": {"valeur_cible": 1000000, "ecart_acceptable": 0} #OK
}

# Fonction qui détermine le type de sonde à partir de la référence
def determiner_type_sonde(reference):
    reference = reference.upper()
    
    # Séparer la référence par le tiret "-"

    if reference.startswith("TX"):
        return "Cernox"
    elif reference.startswith("TP"):
        return "PT100"
    elif reference.startswith("FG-"):
        # On sépare par le tiret et le underscore
        parties = reference.split("_")
        # On récupère la première partie après le tiret
        type_part = parties[0]  
        # Vérifier si la dernière partie correspond à WFb ou WEx
        if len(parties) > 1:
            if parties[1] == "WFB":
                return "Fluxgate_WFb"
            elif parties[1] == "WEX":
                return "Fluxgate_WEx"
    elif reference.startswith("STM-"):
        # On sépare par le tiret et le underscore
        parties = reference.split("_")
        # On récupère la première partie après le tiret
        type_part = parties[0]  
        # Vérifier si la dernière partie correspond à WFb ou WEx
        if len(parties) > 1:
            if parties[1] == "W1":
                return "Stepper_W1"
            elif parties[1] == "W2":
                return "Stepper_W2"
    elif reference.startswith("PZ"):
        if reference.endswith("_C"):
            return "Piezo_C"
        else:
            return "Piezo_ESR"
    elif reference.startswith("HTR"):
        if reference.endswith("ThC"):
            return "Thermocouple"
        else:
            return "Chaufferette"
    elif reference.startswith("LT"):
        return "Jauge de niveau"
    elif reference.startswith("TLS"):
        return "Limit Switch"
    else:
        return None

# Fonction qui vérifie si la valeur mesurée est dans la plage acceptable pour la sonde
def verifier_mesure(reference, valeur_mesuree):
    type_sonde = determiner_type_sonde(reference)  # On détermine le type de sonde à partir de la référence
    valeur_mesuree = valeur_mesuree[0]
    if not type_sonde:
        print(f"Référence '{reference}' non reconnue.")
        return False

    # Vérifier si le type de sonde a des valeurs cibles définies
    if type_sonde in valeurs_cibles:
        cible = valeurs_cibles[type_sonde]["valeur_cible"]
        ecart = valeurs_cibles[type_sonde]["ecart_acceptable"]
        
        # Vérification si la valeur est dans la plage acceptable
        if type_sonde == "Limit Switch":
            return (cible) <= valeur_mesuree
        else:
            return (cible - ecart) <= valeur_mesuree <= (cible + ecart)
    
    return False  # Si le type de sonde n'est pas reconnu dans les valeurs cibles
