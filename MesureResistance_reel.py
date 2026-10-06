import pyvisa
import time

# Connexion aux instruments
rm = pyvisa.ResourceManager()
keysight_34972A = rm.open_resource("USB0::0x0957::0x2007::MY49000000::INSTR")  # Remplace l'adresse par celle de ton appareil

def Mesure4W(source_channels_FW, sense_channels_FW):
    """Mesure de résistance en 4 fils."""
    resultats = []

    for src, sense in zip(source_channels_FW, sense_channels_FW):
        print(f"Configuration de la mesure 4 fils entre les canaux {src} et {sense}")
        keysight_34972A.write(f"ROUT:OPEN:ALL")  # Ouvre tous les relais
        time.sleep(0.5)
        keysight_34972A.write(f"ROUT:CLOS (@{src},{sense})")  # Ferme les relais des canaux source et sense
        time.sleep(0.5)
        keysight_34972A.write("CONF:FRES")  # Configure pour une mesure de résistance 4 fils
        time.sleep(1)
        resistance = float(keysight_34972A.query("READ?"))  # Récupère la mesure
        print(f"Résistance mesurée entre {src} et {sense} : {resistance:.2f} Ohms")
        resultats.append(resistance)

    return resultats

def Mesure2W(source_channels_TW):
    """Mesure de résistance en 2 fils."""
    resultats = []

    for src in source_channels_TW:
        print(f"Configuration de la mesure 2 fils sur le canal {src}")
        keysight_34972A.write("ROUT:OPEN:ALL")
        time.sleep(0.5)
        keysight_34972A.write(f"ROUT:CLOS (@{src})")  # Ferme le relais du canal source
        time.sleep(0.5)
        keysight_34972A.write("CONF:RES")  # Configure pour une mesure de résistance 2 fils
        time.sleep(1)
        resistance = float(keysight_34972A.query("READ?"))  # Récupère la mesure
        print(f"Résistance mesurée sur {src} : {resistance:.2f} Ohms")
        resultats.append(resistance)

    return resultats

  
def MesurePiezo(source_channels_TW, C_ESR):
    """Mesure de capacité (moyennée sur 10 s) ou résistance ESR des piézos."""
    resultats = []

    for src in source_channels_TW:
        print(f"Configuration de la mesure 2 fils sur le canal {src}")
        keysight_34972A.write("ROUT:OPEN:ALL")
        time.sleep(0.5)
        keysight_34972A.write(f"ROUT:CLOS (@{src})")
        time.sleep(0.5)

        if C_ESR == 1:
            keysight_34972A.write("CONF:CAP")  # Configuration mesure capacité
            time.sleep(0.5)

            # Mesure moyenne sur 10 secondes
            mesures = []
            t_debut = time.time()
            while time.time() - t_debut < 10:
                try:
                    valeur = float(keysight_34972A.query("READ?"))
                    mesures.append(valeur)
                except Exception as e:
                    print(f"Erreur lecture capacité sur {src} : {e}")
                time.sleep(0.5)  # Attendre un peu entre les mesures

            if mesures:
                moyenne = sum(mesures) / len(mesures)
                print(f"Valeur mesurée sur {src} : {moyenne:.2e} F (moyenne sur {len(mesures)} mesures)")
                resultats.append(moyenne)
            else:
                print(f"Aucune mesure valide sur {src}")
                resultats.append(None)

        elif C_ESR == 2:
            keysight_34972A.write("CONF:RES")  # Mesure ESR
            time.sleep(1)
            try:
                valeur_mesuree = float(keysight_34972A.query("READ?"))
                print(f"Valeur mesurée sur {src} : {valeur_mesuree:.2f} Ohms")
                resultats.append(valeur_mesuree)
            except Exception as e:
                print(f"Erreur lecture ESR sur {src} : {e}")
                resultats.append(None)

    return resultats


# Fermeture de la connexion
keysight_34972A.close()
