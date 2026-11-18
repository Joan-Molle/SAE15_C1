
import pandas as pd


# 1. LECTURE DU FICHIER


df = pd.read_csv("sup_support.txt", sep=";", dtype=str)

# Afficher les 5 premières lignes
print("Aperçu du fichier :")
print(df.head())

# Afficher les noms des colonnes
print("\nListe des colonnes :")
print(df.columns.tolist())



# 2. DESCRIPTION DES COLONNES


descriptions = {
    "SUP_ID": "Identifiant du support",
    "STA_NM_ANFR": "Identifiant de l'installation ANFR",
    "NAT_ID": "Nature du support",
    "COR_NB_DG_LAT": "Latitude : degrés",
    "COR_NB_MN_LAT": "Latitude : minutes",
    "COR_NB_SC_LAT": "Latitude : secondes",
    "COR_CD_NS_LAT": "Latitude : Nord ou Sud",
    "COR_NB_DG_LON": "Longitude : degrés",
    "COR_NB_MN_LON": "Longitude : minutes",
    "COR_NB_SC_LON": "Longitude : secondes",
    "COR_CD_EW_LON": "Longitude : Est ou Ouest",
    "SUP_NM_HAUT": "Hauteur du support",
    "TPO_ID": "Identifiant du propriétaire",
    "ADR_LB_LIEU": "Lieu d'implantation",
    "ADR_LB_ADD1": "Adresse complémentaire 1",
    "ADR_LB_ADD2": "Adresse complémentaire 2",
    "ADR_LB_ADD3": "Adresse complémentaire 3",
    "ADR_NM_CP": "Code postal",
    "COM_CD_INSEE": "Code INSEE de la commune"
}

# Afficher les colonnes et leurs descriptions
print("\nDescription des colonnes :")

for colonne in df.columns:
    print(colonne, ":", descriptions.get(colonne, "Non identifiée"))


# 3. DICTIONNAIRE DES DEPARTEMENTS


noms_departements = {
    "01": "Ain",
    "02": "Aisne",
    "03": "Allier",
    "04": "Alpes-de-Haute-Provence",
    "05": "Hautes-Alpes",
    "06": "Alpes-Maritimes",
    "07": "Ardèche",
    "08": "Ardennes",
    "09": "Ariège",
    "10": "Aube",
    "11": "Aude",
    "12": "Aveyron",
    "13": "Bouches-du-Rhône",
    "14": "Calvados",
    "15": "Cantal",
    "16": "Charente",
    "17": "Charente-Maritime",
    "18": "Cher",
    "19": "Corrèze",
    "2A": "Corse-du-Sud",
    "2B": "Haute-Corse",
    "21": "Côte-d'Or",
    "22": "Côtes-d'Armor",
    "23": "Creuse",
    "24": "Dordogne",
    "25": "Doubs",
    "26": "Drôme",
    "27": "Eure",
    "28": "Eure-et-Loir",
    "29": "Finistère",
    "30": "Gard",
    "31": "Haute-Garonne",
    "32": "Gers",
    "33": "Gironde",
    "34": "Hérault",
    "35": "Ille-et-Vilaine",
    "36": "Indre",
    "37": "Indre-et-Loire",
    "38": "Isère",
    "39": "Jura",
    "40": "Landes",
    "41": "Loir-et-Cher",
    "42": "Loire",
    "43": "Haute-Loire",
    "44": "Loire-Atlantique",
    "45": "Loiret",
    "46": "Lot",
    "47": "Lot-et-Garonne",
    "48": "Lozère",
    "49": "Maine-et-Loire",
    "50": "Manche",
    "51": "Marne",
    "52": "Haute-Marne",
    "53": "Mayenne",
    "54": "Meurthe-et-Moselle",
    "55": "Meuse",
    "56": "Morbihan",
    "57": "Moselle",
    "58": "Nièvre",
    "59": "Nord",
    "60": "Oise",
    "61": "Orne",
    "62": "Pas-de-Calais",
    "63": "Puy-de-Dôme",
    "64": "Pyrénées-Atlantiques",
    "65": "Hautes-Pyrénées",
    "66": "Pyrénées-Orientales",
    "67": "Bas-Rhin",
    "68": "Haut-Rhin",
    "69": "Rhône",
    "70": "Haute-Saône",
    "71": "Saône-et-Loire",
    "72": "Sarthe",
    "73": "Savoie",
    "74": "Haute-Savoie",
    "75": "Paris",
    "76": "Seine-Maritime",
    "77": "Seine-et-Marne",
    "78": "Yvelines",
    "79": "Deux-Sèvres",
    "80": "Somme",
    "81": "Tarn",
    "82": "Tarn-et-Garonne",
    "83": "Var",
    "84": "Vaucluse",
    "85": "Vendée",
    "86": "Vienne",
    "87": "Haute-Vienne",
    "88": "Vosges",
    "89": "Yonne",
    "90": "Territoire de Belfort",
    "91": "Essonne",
    "92": "Hauts-de-Seine",
    "93": "Seine-Saint-Denis",
    "94": "Val-de-Marne",
    "95": "Val-d'Oise",
    "971": "Guadeloupe",
    "972": "Martinique",
    "973": "Guyane",
    "974": "La Réunion",
    "976": "Mayotte"
}

print("\nNombre de départements dans le dictionnaire :",
      len(noms_departements))
