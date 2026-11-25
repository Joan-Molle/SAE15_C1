import matplotlib.pyplot as plt
from used_data import charger_emetteurs
# ==================================
# 1. Lire le fichier des emetteurs
# ==================================

emetteurs = charger_emetteurs()


# ==================================
# 2. Afficher les premieres lignes
# ==================================

print("\nLes 5 premieres lignes :")
print(emetteurs.head())

# ==================================
# 3. Compter les emetteurs par systeme
# ==================================

comptage = emetteurs["EMR_LB_SYSTEME"].value_counts()

print("\nNombre d'emetteurs par systeme :")
print(comptage)

# ==================================
# 4. Afficher le nombre total
# ==================================

print("\nNombre total d'emetteurs :")
print(len(emetteurs))


# ==================================
# 5. Regrouper les systemes par technologie
# ==================================

def classer_technologie(systeme):

    if isinstance(systeme, str):
        if systeme.startswith("GSM"):
            return "2G"
        elif systeme.startswith("UMTS"):
            return "3G"
        elif systeme.startswith("LTE"):
            return "4G"
        elif systeme.startswith("5G NR"):
            return "5G"

    return "Autres"


emetteurs["Technologie"] = emetteurs["EMR_LB_SYSTEME"].apply(
    classer_technologie
)

# Compter les emetteurs par technologie
comptage_technologie = emetteurs["Technologie"].value_counts()

print("\nNombre d'emetteurs par technologie :")
print(comptage_technologie)

# ==================================
# 6. Creer un graphique
# ==================================

# Selectionner les technologies
ordre = ["2G", "3G", "4G", "5G"]

donnees_graphique = comptage_technologie.reindex(
    ordre, fill_value=0
)

# Creer le graphique
plt.figure(figsize=(9, 5))

plt.bar(
    donnees_graphique.index,
    donnees_graphique.values
)

# Ajouter un titre et les axes
plt.title("Nombre d'emetteurs par technologie")
plt.xlabel("Technologie")
plt.ylabel("Nombre d'emetteurs")

# Ajouter une grille
plt.grid(axis="y", linestyle="--", alpha=0.5)

# Ameliorer l'affichage
plt.tight_layout()

# Enregistrer le graphique
plt.savefig("graphique_technologies.png")

# Afficher le graphique
plt.show()



# ==================================
# Dictionnaire de recherche
# ==================================

# Creer un dictionnaire avec les informations des emetteurs
dictionnaire_emetteurs = emetteurs.set_index("EMR_ID").to_dict("index")


def rechercher_emetteur(id_emetteur):

    if id_emetteur in dictionnaire_emetteurs:

        print("\nInformations de l'emetteur :")

        informations = dictionnaire_emetteurs[id_emetteur]

        for cle, valeur in informations.items():
            print(f"{cle} : {valeur}")

    else:
        print("Aucun emetteur trouve avec cet ID.")


# Exemple de recherche
rechercher_emetteur("850")



while True:
    id_recherche = input("\nEntrez l'ID de l'emetteur (ou 'q' pour quitter) : ")

    if id_recherche.lower() == 'q':
        print("Fin de la recherche.")
        break

    rechercher_emetteur(id_recherche)
