import pandas as pd

# Lire le fichier des natures
natures = pd.read_csv("sup_nature.txt", sep=";")

# Demander à l'utilisateur ce qu'il veut rechercher
recherche = input("Entrez un NAT_ID ou le nom de la nature : ")

# Rechercher par identifiant
resultat_id = natures[
    natures["NAT_ID"].astype(str) == recherche
]

# Rechercher par nom
resultat_nom = natures[
    natures["NAT_LB_NOM"].str.upper() == recherche.upper()
]

# Afficher le résultat
if not resultat_id.empty:
    print("Nom de la nature :", resultat_id.iloc[0]["NAT_LB_NOM"])

elif not resultat_nom.empty:
    print("Identifiant de la nature :", resultat_nom.iloc[0]["NAT_ID"])

else:
    print("Nature introuvable.")