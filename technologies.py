
import pandas as pd
import matplotlib.pyplot as plt

# ==================================
# 1. Lire le fichier des emetteurs
# ==================================

emetteurs = pd.read_csv(
    "data/sup_emetteur.txt",
    sep=";",
    encoding="utf-8"
)


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
