import pyvisa
import time

rm = pyvisa.ResourceManager()

# --- Connexions instruments ---
mux = rm.open_resource("USB0::0x0957::0x2007::MY49000000::INSTR")   # 34972A
dmm = rm.open_resource("USB0::0x2A8D::0x0201::MY59000000::INSTR")   # 34461A

# ---- Fonctions utilitaires ----
def lire_valeur(retry=3, delay=0.2):
    """Lecture robuste via INIT / FETC? sur le DMM"""
    for _ in range(retry):
        try:
            dmm.write("INIT")
            dmm.query("*OPC?")  # attend fin mesure
            val = float(dmm.query("FETC?"))
            return val
        except Exception as e:
            print(f"Erreur lecture, retry... : {e}")
            time.sleep(delay)
    return None


def fermer_tous_les_relais():
    mux.write("ROUT:OPEN:ALL")
    time.sleep(0.2)  # stabilisation multiplexeur
    
def lire_valeur_stable():
    """Lecture avec première valeur jetée"""
    _ = lire_valeur()
    return lire_valeur()


# ---- Mesures ----
def Mesure4W(source_channels_FW, sense_channels_FW):
    """Mesure de résistance 4 fils"""

    if len(source_channels_FW) != len(sense_channels_FW):
        raise ValueError("Listes source et sense de tailles différentes")

    resultats = []
    dmm.write("CONF:FRES")

    for src, sense in zip(source_channels_FW, sense_channels_FW):
        print(f"Mesure 4 fils entre {src} et {sense}")

        fermer_tous_les_relais()
        mux.write(f"ROUT:CLOS (@{src},{sense})")

        time.sleep(0.3)  # stabilisation câbles
        R = lire_valeur_stable()

        if R is not None:
            print(f"Résistance mesurée : {R:.2f} Ω")
            resultats.append(R)
        else:
            print(f"Erreur mesure canal {src}-{sense}")
            resultats.append(None)

    return resultats


def Mesure2W(source_channels_TW):
    """Mesure de résistance 2 fils"""
    resultats = []

    dmm.write("CONF:RES")  # config 2 fils

    for src in source_channels_TW:
        print(f"Mesure 2 fils sur canal {src}")

        fermer_tous_les_relais()
        mux.write(f"ROUT:CLOS (@{src})")

        time.sleep(0.3)
        R = lire_valeur_stable()

        if R is not None:
            print(f"Résistance mesurée : {R:.2f} Ω")
            resultats.append(R)
        else:
            print(f"Erreur mesure canal {src}")
            resultats.append(None)

    return resultats


def MesurePiezo(source_channels_TW, C_ESR=1):
    """Mesure capacité (C_ESR=1) ou ESR (C_ESR=2)"""
    resultats = []

    for src in source_channels_TW:
        fermer_tous_les_relais()
        mux.write(f"ROUT:CLOS (@{src})")

        time.sleep(0.3)

        if C_ESR == 1:
            dmm.write("CONF:CAP")

            periode = 0.3
            nb_mesures = int(10 / (periode + 0.25))

            mesures = []
            for _ in range(nb_mesures):
                val = lire_valeur_stable()
                if val is not None:
                    mesures.append(val)
                time.sleep(periode)

            if mesures:
                moyenne = sum(mesures) / len(mesures)
                print(f"Capacité moyenne sur {src} : {moyenne:.2e} F")
                resultats.append(moyenne)
            else:
                print(f"Aucune mesure valide sur {src}")
                resultats.append(None)

        elif C_ESR == 2:
            dmm.write("CONF:RES")

            val = lire_valeur_stable()
            if val is not None:
                print(f"ESR mesurée sur {src} : {val:.2f} Ω")
                resultats.append(val)
            else:
                print(f"Erreur ESR sur {src}")
                resultats.append(None)

    return resultats


# --- Fermeture à faire dans le programme principal ---
# mux.close()
# dmm.close()
