
import pandas as pd

# Lire le fichier
df = pd.read_csv("sup_support.txt", sep=";")

# Afficher les 5 premières lignes
print(df.head())

# Afficher les noms des colonnes
print(df.columns)

# Dictionnaire des descriptions
descriptions = {
    "SUP_ID": "Identifiant du support",
    "STA_NM_ANFR": "Identifiant de l'installation ANFR",
    "NAT_ID": "Nature du support",
    "COR_NB_DG_LAT": "Latitude : degres",
    "COR_NB_MN_LAT": "Latitude : minutes",
    "COR_NB_SC_LAT": "Latitude : secondes",
    "COR_CD_NS_LAT": "Latitude : Nord ou Sud",
    "COR_NB_DG_LON": "Longitude : degres",
    "COR_NB_MN_LON": "Longitude : minutes",
    "COR_NB_SC_LON": "Longitude : secondes",
    "COR_CD_EW_LON": "Longitude : Est ou Ouest",
    "SUP_NM_HAUT": "Hauteur du support",
    "TPO_ID": "Identifiant du proprietaire",
    "ADR_LB_LIEU": "Lieu d'implantation",
    "ADR_LB_ADD1": "Adresse complementaire 1",
    "ADR_LB_ADD2": "Adresse complementaire 2",
    "ADR_LB_ADD3": "Adresse complementaire 3",
    "ADR_NM_CP": "Code postal",
    "COM_CD_INSEE": "Code INSEE de la commune"
}

# Afficher les colonnes avec leurs descriptions
for colonne in df.columns:
    print(colonne, ":", descriptions.get(colonne, "Non identifie"))
