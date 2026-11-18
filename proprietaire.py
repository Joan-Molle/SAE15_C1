import pandas as pd

# Lire le fichier des propriétaires
proprietaires = pd.read_csv("sup_proprietaire.txt", sep=";")

# Demander à l'utilisateur ce qu'il veut rechercher
recherche = input("Entrez un TPO_ID ou le nom du propriétaire : ")

# Rechercher par identifiant
resultat_id = proprietaires[
    proprietaires["TPO_ID"].astype(str) == recherche
]

# Rechercher par nom
resultat_nom = proprietaires[
    proprietaires["TPO_LB"].str.upper() == recherche.upper()
]

# Afficher le résultat
if not resultat_id.empty:
    print("Nom du propriétaire :", resultat_id.iloc[0]["TPO_LB"])

elif not resultat_nom.empty:
    print("Identifiant du propriétaire :", resultat_nom.iloc[0]["TPO_ID"])

else:
    print("Propriétaire introuvable.")