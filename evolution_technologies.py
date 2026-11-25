# 4.2 - Evolution des technologies par annee de mise en service (2017-2026)
import matplotlib.pyplot as plt
from used_data import charger_emetteurs

# 1. Lire les emetteurs
# used_data ajoute deja ANNEE (texte, ex : "2019") et Technologie (2G, 3G, 4G, 5G, Autres)
emetteurs = charger_emetteurs()

# 2. Annees etudiees (en texte, comme la colonne ANNEE)
annees = ["2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025", "2026"]

# On ne garde que les emetteurs mis en service pendant ces annees
emetteurs = emetteurs[emetteurs["ANNEE"].isin(annees)]

# 3. Une courbe par technologie
plt.figure(figsize=(12, 6))

for techno in ["2G", "3G", "4G", "5G"]:
    nombres = []
    for annee in annees:
        # Emetteurs de cette techno ET de cette annee
        selection = emetteurs[(emetteurs["Technologie"] == techno) & (emetteurs["ANNEE"] == annee)]
        nombres.append(len(selection))
    print(techno, ":", nombres)
    plt.plot(annees, nombres, marker="o", label=techno)

# 4. 2026 n'est pas terminee : on l'indique sous l'axe
etiquettes = annees[:-1] + ["2026\n(en cours)"]
plt.xticks(annees, etiquettes)

plt.title("Emetteurs mis en service chaque annee, par technologie")
plt.xlabel("Annee de mise en service")
plt.ylabel("Nombre d'emetteurs mis en service")
plt.legend(title="Technologies")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("evolution_technologies.png")
plt.show()