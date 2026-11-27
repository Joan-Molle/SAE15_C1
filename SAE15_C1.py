# Lire le README.md avant d'exécuter ce code.
## Read the README.md before running this code.

# Ce code peut être découpé en plusieurs parties : 1.2, 2.1, 2.2, 2.3, 3.1, 3.2, 4.1, 4.2.
## This code can be split into several parts: 1.2, 2.1, 2.2, 2.3, 3.1, 3.2, 4.1, 4.2.

import pandas as pd
import matplotlib.pyplot as plt


# 1.2 - Lecture des données
## 1.2 - Reading the data

# Les identifiants restent du texte pour garder les zéros du début (ex : 0010030350) et les lettres de la Corse (2A, 2B).
## The IDs stay text to keep the leading zeros (ex: 0010030350) and the letters of Corsica (2A, 2B).
identifiants = {"STA_NM_ANFR": str, "SUP_ID": str, "AER_ID": str, "EMR_ID": str, "ADM_ID": str, "NAT_ID": str, "TPO_ID": str, "TAE_ID": str, "ADR_NM_CP": str, "COM_CD_INSEE": str, "DEM_NM_COMSIS": str, "STA_NM_USER": str}


# Tous les fichiers sont lus de la même façon : colonnes séparées par ";", virgule pour les décimales, identifiants en texte.
## All the files are read the same way: columns separated by ";", comma for decimals, IDs as text.
def lire(chemin):
    return pd.read_csv(chemin, sep=";", decimal=",", dtype=identifiants, encoding="utf-8")


def charger_stations():
    stations = lire("data/sup_station.txt")
    exploitants = lire("ref/sup_exploitant.txt")

    # On fusionne les deux fichiers pour avoir le nom de l'exploitant.
    ## We merge the two files to get the name of the operator.
    stations = stations.merge(exploitants, on="ADM_ID")

    # On garde uniquement l'année.
    ## We only keep the year.
    stations["ANNEE"] = stations["DTE_EN_SERVICE"].str[6:10]
    return stations


def coordonnee(degres, minutes, secondes, lettre):
    # On convertit les coordonnées en degrés décimaux.
    ## We convert the coordinates into decimal degrees.
    valeur = degres + minutes/60 + secondes/3600

    # Si on projette N, S, E, W sur un plan cartésien, N et E sont positifs tandis que S et W sont négatifs.
    ## If we put N, S, E, W on a Cartesian plane, N and E are positive while S and W are negative.
    if lettre == "S" or lettre == "W":
        valeur = -1*valeur
    return valeur


def charger_supports():
    supports = lire("data/sup_support.txt")
    natures = lire("ref/sup_nature.txt")

    # On fusionne les deux fichiers pour avoir la nature du support.
    ## We merge the two files to get the type of the support.
    supports = supports.merge(natures, on="NAT_ID")

    # À chaque tour, zip prend les 4 cases d'une ligne (degrés, minutes, secondes, lettre) et on ajoute la latitude en degrés décimaux à la liste.
    ## At each turn, zip takes the 4 cells of a row (degrees, minutes, seconds, letter) and we add the latitude in decimal degrees to the list.
    liste_lat = []
    for d, m, s, l in zip(supports["COR_NB_DG_LAT"], supports["COR_NB_MN_LAT"], supports["COR_NB_SC_LAT"], supports["COR_CD_NS_LAT"]):
        liste_lat.append(coordonnee(d, m, s, l))

    # Même chose pour la longitude.
    ## Same thing for the longitude.
    liste_lon = []
    for d, m, s, l in zip(supports["COR_NB_DG_LON"], supports["COR_NB_MN_LON"], supports["COR_NB_SC_LON"], supports["COR_CD_EW_LON"]):
        liste_lon.append(coordonnee(d, m, s, l))

    supports["lat"] = liste_lat
    supports["lon"] = liste_lon

    # On récupère les deux premiers caractères du code INSEE pour avoir le code du département.
    ## We take the first two characters of the INSEE code to get the department code.
    supports["DEPARTEMENT"] = supports["COM_CD_INSEE"].str[:2]
    return supports


# 4.1 : on classe chaque émetteur selon sa technologie (GSM = 2G, UMTS = 3G, LTE = 4G, 5G NR = 5G, le reste = Autres).
## 4.1: we sort each transmitter by its technology (GSM = 2G, UMTS = 3G, LTE = 4G, 5G NR = 5G, the rest = Autres).

# Les mots "2G", "3G"... ne sont pas dans le fichier, c'est une convention télécom.
## The words "2G", "3G"... are not in the file, it is a telecom convention.
def classer_technologie(systeme):
    # str() transforme la case en texte : une case vide devient "nan" et part dans "Autres".
    ## str() turns the cell into text: an empty cell becomes "nan" and goes into "Autres".
    systeme = str(systeme)

    # On regarde les premiers caractères du nom : [:3] donne les 3 premiers, [:4] les 4 premiers...
    ## We look at the first characters of the name: [:3] gives the first 3, [:4] the first 4...
    if systeme[:3] == "GSM":
        return "2G"
    elif systeme[:4] == "UMTS":
        return "3G"
    elif systeme[:3] == "LTE":
        return "4G"
    elif systeme[:5] == "5G NR":
        return "5G"
    return "Autres"


def charger_emetteurs():
    emetteurs = lire("data/sup_emetteur.txt")

    # On garde uniquement l'année.
    ## We only keep the year.
    emetteurs["ANNEE"] = emetteurs["EMR_DT_SERVICE"].str[6:10]

    # On ajoute la technologie de chaque émetteur.
    ## We add the technology of each transmitter.
    emetteurs["Technologie"] = emetteurs["EMR_LB_SYSTEME"].apply(classer_technologie)
    return emetteurs


# On lit chaque fichier une seule fois, puis toutes les parties s'en servent.
## Each file is read only once, then all the parts use it.
print("Lecture des données...")
stations = charger_stations()
supports = charger_supports()
emetteurs = charger_emetteurs()


# 2.1 - Classement des exploitants par nombre d'installations
## 2.1 - Ranking of the operators by number of installations

# nunique() compte les identifiants DIFFÉRENTS : une installation n'est comptée qu'une fois.
## nunique() counts the DIFFERENT IDs: an installation is counted only once.
comptage = stations.groupby("ADM_LB_NOM")["STA_NM_ANFR"].nunique()
comptage = comptage.sort_values(ascending=False)

# On garde les 10 premiers exploitants et on additionne tous les autres dans une ligne "Autres".
## We keep the first 10 operators and add up all the others in an "Autres" row.
resultat = comptage.head(10)
resultat["Autres"] = comptage.iloc[10:].sum()

print("\nClassement des exploitants par nombre d'installations :")
print(resultat)
resultat.to_csv("classement_exploitants.csv", header=["Nombre d'installations"])


# 2.2 - Graphique en barres du classement des exploitants
## 2.2 - Bar chart of the operator ranking

plt.figure(figsize=(12, 6))
plt.bar(resultat.index, resultat.values)
plt.title("Nombre d'installations par exploitant")
plt.xlabel("Exploitants")
plt.ylabel("Nombre d'installations")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("graphique_exploitants.png")


# 2.3 - Technologies des 10 plus gros exploitants, barres côte à côte
## 2.3 - Technologies of the 10 biggest operators, bars side by side

# On relie chaque émetteur au nom de l'exploitant de sa station (on ne garde que le lien STA_NM_ANFR et le nom).
## We link each transmitter to the name of the operator of its station (we only keep the link STA_NM_ANFR and the name).
donnees = pd.merge(emetteurs, stations[["STA_NM_ANFR", "ADM_LB_NOM"]], on="STA_NM_ANFR")

# On garde les 10 exploitants qui ont le plus d'émetteurs.
## We keep the 10 operators with the most transmitters.
top_exploitants = donnees["ADM_LB_NOM"].value_counts().head(10).index
donnees = donnees[donnees["ADM_LB_NOM"].isin(top_exploitants)]

# On compte : une ligne par exploitant, une colonne par technologie.
## We count: one row per operator, one column per technology.
ordre = ["2G", "3G", "4G", "5G", "Autres"]
tableau = pd.DataFrame(index=top_exploitants)
for techno in ordre:
    selection = donnees[donnees["Technologie"] == techno]
    tableau[techno] = selection["ADM_LB_NOM"].value_counts()

# Case vide = l'exploitant n'a aucun émetteur de cette technologie : on met 0.
## Empty cell = the operator has no transmitter of this technology: we put 0.
tableau = tableau.fillna(0).astype(int)

print("\nNombre d'émetteurs par exploitant et technologie :")
print(tableau)

# Pour chaque exploitant, 5 barres côte à côte : on décale chaque technologie un peu vers la droite.
## For each operator, 5 bars side by side: we move each technology a little to the right.
largeur = 0.15
positions = range(len(tableau))

plt.figure(figsize=(12, 6))
for i in range(len(ordre)):
    techno = ordre[i]
    x = []
    for p in positions:
        x.append(p + i * largeur)
    plt.bar(x, tableau[techno], width=largeur, label=techno)

# Le nom de l'exploitant au milieu de son groupe de 5 barres.
## The name of the operator in the middle of its group of 5 bars.
milieux = []
for p in positions:
    milieux.append(p + 2 * largeur)
plt.xticks(milieux, tableau.index, rotation=45, ha="right")

plt.title("Nombre d'émetteurs par technologie et exploitant")
plt.xlabel("Exploitants")
plt.ylabel("Nombre d'émetteurs")
plt.legend(title="Technologies")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("graphique_technologie_exploitant.png")


# 3.1 et 3.2 - Géographie
## 3.1 and 3.2 - Geography

# Le fichier sup_support.txt a déjà été lu au début (variable supports) : on l'appelle df dans cette partie.
## The sup_support.txt file was already read at the start (supports variable): we call it df in this part.
df = supports

print("\nLes 5 premières lignes :")
print(df.head())
print("\nLes colonnes :")
print(df.columns.tolist())

# Chaque nom de colonne est associé à sa description.
## Each column name is linked to its description.
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

# On affiche chaque colonne avec sa description ("Non identifiée" si elle n'est pas dans le dictionnaire).
## We print each column with its description ("Non identifiée" if it is not in the dictionary).
print("\nDescription des colonnes :")
for colonne in df.columns:
    print(colonne, ":", descriptions.get(colonne, "Non identifiée"))

# Dictionnaire qui associe chaque numéro de département à son nom (ex : "76" correspond à "Seine-Maritime").
## Dictionary that links each department number to its name (ex: "76" is "Seine-Maritime").
noms_departements = {
    "01": "Ain", "02": "Aisne", "03": "Allier", "04": "Alpes-de-Haute-Provence", "05": "Hautes-Alpes",
    "06": "Alpes-Maritimes", "07": "Ardèche", "08": "Ardennes", "09": "Ariège", "10": "Aube",
    "11": "Aude", "12": "Aveyron", "13": "Bouches-du-Rhône", "14": "Calvados", "15": "Cantal",
    "16": "Charente", "17": "Charente-Maritime", "18": "Cher", "19": "Corrèze", "2A": "Corse-du-Sud",
    "2B": "Haute-Corse", "21": "Côte-d'Or", "22": "Côtes-d'Armor", "23": "Creuse", "24": "Dordogne",
    "25": "Doubs", "26": "Drôme", "27": "Eure", "28": "Eure-et-Loir", "29": "Finistère",
    "30": "Gard", "31": "Haute-Garonne", "32": "Gers", "33": "Gironde", "34": "Hérault",
    "35": "Ille-et-Vilaine", "36": "Indre", "37": "Indre-et-Loire", "38": "Isère", "39": "Jura",
    "40": "Landes", "41": "Loir-et-Cher", "42": "Loire", "43": "Haute-Loire", "44": "Loire-Atlantique",
    "45": "Loiret", "46": "Lot", "47": "Lot-et-Garonne", "48": "Lozère", "49": "Maine-et-Loire",
    "50": "Manche", "51": "Marne", "52": "Haute-Marne", "53": "Mayenne", "54": "Meurthe-et-Moselle",
    "55": "Meuse", "56": "Morbihan", "57": "Moselle", "58": "Nièvre", "59": "Nord",
    "60": "Oise", "61": "Orne", "62": "Pas-de-Calais", "63": "Puy-de-Dôme", "64": "Pyrénées-Atlantiques",
    "65": "Hautes-Pyrénées", "66": "Pyrénées-Orientales", "67": "Bas-Rhin", "68": "Haut-Rhin", "69": "Rhône",
    "70": "Haute-Saône", "71": "Saône-et-Loire", "72": "Sarthe", "73": "Savoie", "74": "Haute-Savoie",
    "75": "Paris", "76": "Seine-Maritime", "77": "Seine-et-Marne", "78": "Yvelines", "79": "Deux-Sèvres",
    "80": "Somme", "81": "Tarn", "82": "Tarn-et-Garonne", "83": "Var", "84": "Vaucluse",
    "85": "Vendée", "86": "Vienne", "87": "Haute-Vienne", "88": "Vosges", "89": "Yonne",
    "90": "Territoire de Belfort", "91": "Essonne", "92": "Hauts-de-Seine", "93": "Seine-Saint-Denis", "94": "Val-de-Marne",
    "95": "Val-d'Oise", "971": "Guadeloupe", "972": "Martinique", "973": "Guyane", "974": "La Réunion",
    "976": "Mayotte"
}

# Dictionnaire qui associe chaque région à la liste de ses départements.
## Dictionary that links each region to the list of its departments.
regions_departements = {
    "Normandie": ["14", "27", "50", "61", "76"],
    "Île-de-France": ["75", "77", "78", "91", "92", "93", "94", "95"],
    "Bretagne": ["22", "29", "35", "56"],
    "Hauts-de-France": ["02", "59", "60", "62", "80"],
    "Grand Est": ["08", "10", "51", "52", "54", "55", "57", "67", "68", "88"],
    "Pays de la Loire": ["44", "49", "53", "72", "85"],
    "Centre-Val de Loire": ["18", "28", "36", "37", "41", "45"],
    "Bourgogne-Franche-Comté": ["21", "25", "39", "58", "70", "71", "89", "90"],
    "Nouvelle-Aquitaine": ["16", "17", "19", "23", "24", "33", "40", "47", "64", "79", "86", "87"],
    "Occitanie": ["09", "11", "12", "30", "31", "32", "34", "46", "48", "65", "66", "81", "82"],
    "Auvergne-Rhône-Alpes": ["01", "03", "07", "15", "26", "38", "42", "43", "63", "69", "73", "74"],
    "Provence-Alpes-Côte d'Azur": ["04", "05", "06", "13", "83", "84"],
    "Corse": ["2A", "2B"],
    "Guadeloupe": ["971"], "Martinique": ["972"], "Guyane": ["973"], "La Réunion": ["974"], "Mayotte": ["976"]
}


# Cette fonction reçoit un code INSEE et renvoie le numéro de son département.
## This function receives an INSEE code and gives back the number of its department.
def extraire_departement(code):
    # On transforme le code en texte sans espaces, en majuscules.
    ## We turn the code into text without spaces, in capital letters.
    code = str(code).strip().upper()

    # Corse : 2A ou 2B ([:2] donne les deux premiers caractères).
    ## Corsica: 2A or 2B ([:2] gives the first two characters).
    if code[:2] == "2A" or code[:2] == "2B":
        return code[:2]

    # Départements d'outre-mer : on garde les trois premiers caractères (971, 972, 973, 974, 976).
    ## Overseas departments: we keep the first three characters (971, 972, 973, 974, 976).
    if code[:3] in ["971", "972", "973", "974", "976"]:
        return code[:3]

    # Autres départements : les deux premiers caractères.
    ## Other departments: the first two characters.
    return code[:2]


# On crée la colonne DEPARTEMENT une seule fois pour toute la partie géographie.
## We create the DEPARTEMENT column only once for the whole geography part.
df["DEPARTEMENT"] = df["COM_CD_INSEE"].apply(extraire_departement)


# 3.1 - Cette fonction renvoie les installations d'une zone (France, Paris, une région ou un département) et leur nombre.
## 3.1 - This function gives back the installations of an area (France, Paris, a region or a department) and their number.
def installations_zone(zone):
    # On compare les textes sans tenir compte des espaces ni des majuscules.
    ## We compare the texts without caring about spaces or capital letters.
    zone = zone.strip().casefold()

    if zone == "france":
        resultat = df
    elif zone == "paris":
        resultat = df[df["DEPARTEMENT"] == "75"]
    else:
        # On part d'un tableau vide, puis on cherche une région, puis un département (par son numéro ou son nom).
        ## We start with an empty table, then we look for a region, then a department (by its number or its name).
        resultat = df.iloc[0:0]

        for region in regions_departements:
            if region.casefold() == zone:
                # isin() garde les lignes dont le département est dans la liste de la région.
                ## isin() keeps the rows whose department is in the list of the region.
                resultat = df[df["DEPARTEMENT"].isin(regions_departements[region])]

        for numero in noms_departements:
            if numero.casefold() == zone or noms_departements[numero].casefold() == zone:
                resultat = df[df["DEPARTEMENT"] == numero]

    if resultat.empty:
        print("Aucune installation trouvée pour cette zone.")

    # On renvoie le tableau des installations et leur nombre (nombre de lignes).
    ## We give back the table of the installations and their number (number of rows).
    nombre = len(resultat)
    return resultat, nombre


# 3.1 - Cette fonction compte les installations à chaque échelle : France, région, département et commune.
## 3.1 - This function counts the installations at each scale: France, region, department and town.
def classement_echelles():
    # On ajoute la colonne REGION : chaque ligne reçoit le nom de la région de son département.
    ## We add the REGION column: each row gets the name of the region of its department.
    df["REGION"] = ""
    for region in regions_departements:
        for departement in regions_departements[region]:
            df.loc[df["DEPARTEMENT"] == departement, "REGION"] = region

    # groupby() regroupe les lignes, size() compte les lignes de chaque groupe.
    ## groupby() groups the rows, size() counts the rows of each group.
    nombre_france = len(df)
    nombre_regions = df.groupby("REGION").size()
    nombre_departements = df.groupby("DEPARTEMENT").size()
    nombre_communes = df.groupby("COM_CD_INSEE").size()

    print("\nNOMBRE D'INSTALLATIONS EN FRANCE :")
    print(nombre_france)
    print("\nNOMBRE D'INSTALLATIONS PAR REGION :")
    print(nombre_regions)
    print("\nNOMBRE D'INSTALLATIONS PAR DEPARTEMENT :")
    print(nombre_departements)
    print("\nNOMBRE D'INSTALLATIONS PAR COMMUNE :")
    print(nombre_communes)

    return nombre_france, nombre_regions, nombre_departements, nombre_communes


# Test des fonctions avec la Normandie.
## Test of the functions with Normandie.
installations, nombre = installations_zone("Normandie")
print("\nINSTALLATIONS EN NORMANDIE :")
print(installations.head())
print("Nombre total :", nombre)

classement_echelles()


# 3.2 - Graphique en barres : un département = une barre, hauteur = nombre d'installations.
## 3.2 - Bar chart: one department = one bar, height = number of installations.

# On enlève le code "97" exact (les codes 971, 972... sont gardés), puis on compte les lignes de chaque département.
## We remove the exact code "97" (the codes 971, 972... are kept), then we count the rows of each department.
nombre_departements = df[df["DEPARTEMENT"] != "97"]
nombre_departements = nombre_departements.groupby("DEPARTEMENT").size()

# Une position par département sur l'axe horizontal : 0, 1, 2...
## One position per department on the horizontal axis: 0, 1, 2...
positions = range(len(nombre_departements))

plt.figure(figsize=(24, 8))
plt.bar(positions, nombre_departements.values, width=0.45)

# Légende vide qui explique le code 98.
## Empty legend item that explains the code 98.
plt.plot([], [], " ", label="98 : Territoires d'outre-mer regroupés")
plt.legend()

plt.xticks(positions, nombre_departements.index, rotation=60, fontsize=9)
plt.title("Nombre d'installations par département", fontsize=16)
plt.xlabel("Départements", fontsize=12)
plt.ylabel("Nombre d'installations", fontsize=12)
plt.yticks(range(0, 5501, 500))
plt.grid(axis="y", linestyle="--", alpha=0.3)

# On place la grille derrière les barres.
## We put the grid behind the bars.
plt.gca().set_axisbelow(True)

plt.figtext(0.5, 0.01, "98 : territoires dont le code INSEE commence par 98.", ha="center", fontsize=10)
plt.subplots_adjust(bottom=0.22, left=0.07, right=0.98, top=0.90)
plt.savefig("graphique_departements.png")


# 4.1 - Technologies des émetteurs : 2G, 3G, 4G, 5G
## 4.1 - Technologies of the transmitters: 2G, 3G, 4G, 5G

# La colonne "Technologie" est déjà calculée par charger_emetteurs() grâce à classer_technologie().
## The "Technologie" column is already made by charger_emetteurs() with classer_technologie().
print("\nLes 5 premières lignes des émetteurs :")
print(emetteurs.head())

print("\nNombre d'émetteurs par système :")
print(emetteurs["EMR_LB_SYSTEME"].value_counts())

print("\nNombre total d'émetteurs :")
print(len(emetteurs))

comptage_technologie = emetteurs["Technologie"].value_counts()
print("\nNombre d'émetteurs par technologie :")
print(comptage_technologie)

# get(techno, 0) donne le nombre de la technologie, ou 0 si elle est absente.
## get(techno, 0) gives the number of the technology, or 0 if it is missing.
ordre = ["2G", "3G", "4G", "5G"]
nombres = []
for techno in ordre:
    nombres.append(comptage_technologie.get(techno, 0))

plt.figure(figsize=(9, 5))
plt.bar(ordre, nombres)
plt.title("Nombre d'émetteurs par technologie")
plt.xlabel("Technologie")
plt.ylabel("Nombre d'émetteurs")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("graphique_technologies.png")


# 4.2 - Évolution des technologies par année de mise en service, 2017 à 2026
## 4.2 - Evolution of the technologies by year of start of service, 2017 to 2026

annees = ["2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025", "2026"]

# On garde les émetteurs de ces années dans une NOUVELLE variable pour ne pas modifier "emetteurs".
## We keep the transmitters of these years in a NEW variable so that "emetteurs" does not change.
emetteurs_periode = emetteurs[emetteurs["ANNEE"].isin(annees)]

plt.figure(figsize=(12, 6))

print("\nNombre d'émetteurs mis en service par année (2017 à 2026) :")
for techno in ["2G", "3G", "4G", "5G"]:
    nombres = []
    for annee in annees:
        # Émetteurs de cette technologie ET de cette année.
        ## Transmitters of this technology AND of this year.
        selection = emetteurs_periode[(emetteurs_periode["Technologie"] == techno) & (emetteurs_periode["ANNEE"] == annee)]
        nombres.append(len(selection))
    print(techno, ":", nombres)
    plt.plot(annees, nombres, marker="o", label=techno)

# 2026 n'est pas terminée : on l'indique sous l'axe.
## 2026 is not over: we write it under the axis.
etiquettes = annees[:-1] + ["2026\n(en cours)"]
plt.xticks(annees, etiquettes)

plt.title("Émetteurs mis en service chaque année, par technologie")
plt.xlabel("Année de mise en service")
plt.ylabel("Nombre d'émetteurs mis en service")
plt.legend(title="Technologies")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("evolution_technologies.png")


# Fin : on affiche tous les graphiques en même temps (ils sont aussi enregistrés en .png).
## End: we show all the charts at the same time (they are also saved as .png).
print("\nTous les résultats ont été générés.")
plt.show()