import pandas as pd

# Lire le fichier des types d'antennes
antennes = pd.read_csv("sup_type_antenne.txt", sep=";")

# Demander à l'utilisateur ce qu'il veut rechercher
recherche = input("Entrez un TAE_ID ou le nom du type d'antenne : ")

# Rechercher par identifiant
resultat_id = antennes[
    antennes["TAE_ID"].astype(str) == recherche
]

# Rechercher par nom
resultat_nom = antennes[
    antennes["TAE_LB"].str.upper() == recherche.upper()
]

# Afficher le résultat
if not resultat_id.empty:
    print("Nom du type d'antenne :", resultat_id.iloc[0]["TAE_LB"])

elif not resultat_nom.empty:
    print("Identifiant du type d'antenne :", resultat_nom.iloc[0]["TAE_ID"])

else:
    print("Type d'antenne introuvable.")