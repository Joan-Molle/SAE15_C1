# 4.1 - Technologies des emetteurs (2G, 3G, 4G, 5G)
# Les donnees viennent de used_data.py.
# La colonne "Technologie" est deja calculee par charger_emetteurs()
# grace a la fonction classer_technologie (dans used_data.py).

import matplotlib.pyplot as plt
from used_data import charger_emetteurs

# 1. Lire les emetteurs
emetteurs = charger_emetteurs()

# 2. Afficher les premieres lignes
print("\nLes 5 premieres lignes :")
print(emetteurs.head())

# 3. Compter les emetteurs par systeme (valeurs brutes du fichier, ex : "LTE 800")
print("\nNombre d'emetteurs par systeme :")
print(emetteurs["EMR_LB_SYSTEME"].value_counts())

# 4. Nombre total d'emetteurs
print("\nNombre total d'emetteurs :")
print(len(emetteurs))

# 5. Compter les emetteurs par technologie (2G, 3G, 4G, 5G, Autres)
comptage_technologie = emetteurs["Technologie"].value_counts()
print("\nNombre d'emetteurs par technologie :")
print(comptage_technologie)

# 6. Graphique en barres (2G a 5G, dans l'ordre)
ordre = ["2G", "3G", "4G", "5G"]
nombres = []
for techno in ordre:
    nombres.append(comptage_technologie.get(techno, 0))   # 0 si la techno est absente

plt.figure(figsize=(9, 5))
plt.bar(ordre, nombres)
plt.title("Nombre d'emetteurs par technologie")
plt.xlabel("Technologie")
plt.ylabel("Nombre d'emetteurs")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("graphique_technologies.png")
plt.show()