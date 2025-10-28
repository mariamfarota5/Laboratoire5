# Analyse du fichier log.txt
# Affiche un histogramme des durees comptees par le joueur

import matplotlib.pyplot as plt

# Lecture du fichier log.txt
fichier = "log.txt"
valeurs = []

with open(fichier, "r") as log:
    for ligne in log:
        # On recupere uniquement le nombre a la fin de chaque ligne
        ligne = ligne.strip()
        if not ligne:
            continue
        # Si le format est "xx:xx:xx -> xx:xx:xx = Ns"
        if "=" in ligne:
            try:
                valeur = int(ligne.split("=")[-1].replace("s", "").strip())
                valeurs.append(valeur)
            except ValueError:
                pass
        else:
            # sinon juste un nombre (ex: 14, 16, etc.)
            try:
                valeurs.append(int(ligne))
            except ValueError:
                pass

# Verifier que des donnees ont ete lues
if not valeurs:
    print("Aucun nombre trouve dans log.txt.")
    exit()

# Création de l'histogramme
plt.hist(valeurs, bins=range(min(valeurs), max(valeurs)+2), edgecolor='black', align='left')

plt.title("Histogramme du temps compte par le joueur")
plt.xlabel("Temps compte (secondes)")
plt.ylabel("Nombre de fois")
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Affichage
plt.show()
