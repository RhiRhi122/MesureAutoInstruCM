import pyvisa
import time

rm = pyvisa.ResourceManager()

mux = rm.open_resource("USB0::0x0957::0x2007::MY49000000::INSTR")
dmm = rm.open_resource("USB0::0x2A8D::0x0201::MY59000000::INSTR")

def lire_resistance(max_retry=3):
    """Lecture robuste avec retry."""
    
    for _ in range(max_retry):
        try:
            dmm.write("INIT")          # Lance la mesure
            dmm.query("*OPC?")         # Attend fin de mesure
            val = float(dmm.query("FETC?"))
            return val
        except:
            time.sleep(0.2)

    return None  # échec

def verifier_isolement(source_channels_FW):

    resistance_ref = 1e6
    etat_isolement = []

    # Configuration faite une seule fois
    dmm.write("CONF:RES 10E6,1")

    for src in source_channels_FW:

        # Ouvre tous les relais
        mux.write("ROUT:OPEN:ALL")
        time.sleep(0.3)

        # Ferme canal
        mux.write(f"ROUT:CLOS (@{src})")

        # Stabilisation multiplexeur + câbles
        time.sleep(0.5)

        # Lecture robuste
        resistance_isolement = lire_resistance()

        if resistance_isolement is None:
            print(f"Lecture échouée canal {src}")
            etat_isolement.append(False)
            continue

        print(f"Canal {src} : {resistance_isolement:.3e} Ohm")

        etat_isolement.append(resistance_isolement >= resistance_ref)

    return etat_isolement


# --- Exemple utilisation ---
channels = [101, 102, 103]
resultat = verifier_isolement(channels)

mux.close()
dmm.close()
