#  Lab 5 – I2C, Temps et Journal

from machine import Pin, I2C
import time

# Initialisation I2C 
i2c = I2C(1, sda=Pin(14), scl=Pin(15))
rtc_address = 0x68  # Adresse I2C du module DS3231

# Initialisation du bouton 
bouton = Pin(22, Pin.IN, Pin.PULL_DOWN)

# Fonction pour lire l'heure depuis le RTC (format BCD)
def lire_temps():
    data = i2c.readfrom_mem(rtc_address, 0x00, 3)
    secondes = ((data[0] >> 4) * 10) + (data[0] & 0x0F)
    minutes = ((data[1] >> 4) * 10) + (data[1] & 0x0F)
    heures = ((data[2] >> 4) * 10) + (data[2] & 0x0F)
    return heures, minutes, secondes


# Ouverture du fichier journal
log = open("log.txt", "a")

print("Jeu de perception du temps (15 secondes)")
print("Appuie sur le bouton pour commencer...")

try:
    while True:
        # Attente du premier appui (pull-up: appui = 0)
        while bouton.value() == 1:
            pass
        # petit anti-rebond
        time.sleep_ms(20)
        # lire le temps de départ
        h1, m1, s1 = lire_temps()
        print("Chrono dEmarre, comptez 15 secondes puis appuyez a nouveau...")

        # attendre le relâchement du bouton pour éviter double-détection
        while bouton.value() == 0:
            pass
        time.sleep_ms(20)

        # Attente du second appui
        while bouton.value() == 1:
            pass
        time.sleep_ms(20)
        # lire le temps de fin
        h2, m2, s2 = lire_temps()

        # Conversion en secondes depuis minuit
        start_total = h1 * 3600 + m1 * 60 + s1
        end_total = h2 * 3600 + m2 * 60 + s2
        delta = end_total - start_total
        # gestion du passage minuit
        if delta < 0:
            delta += 24 * 3600

        print("Tu as compte", delta, "secondes.")
        log.write(f"{delta}\n")
        log.flush()  # forcer l'ecriture sur la memoire flash

        print("Appuie à nouveau pour rejouer...")

except KeyboardInterrupt:
    print("\nFin du jeu ! Le journal a ete sauvegarde.")

finally:
    # Fermeture securisee du fichier
    log.close()