

# On importe pandas pour lire, organiser et analyser les données.
# On lui donne le raccourci "pd" pour écrire moins de code.
import pandas as pd

# On importe matplotlib.pyplot pour créer des graphiques.
# On lui donne le raccourci "plt".
import matplotlib.pyplot as plt



# 1. LIRE LE FICHIER


# On ouvre le fichier sup_support.txt avec pandas.
# sep=";" indique que les informations sont séparées par des points-virgules.
# dtype=str indique que toutes les données seront considérées comme du texte.
# Le fichier est stocké dans une variable appelée df.
df = pd.read_csv("sup_support.txt", sep=";", dtype=str)

# On affiche un message pour présenter les premières lignes du fichier.
print("Les 5 premières lignes :")

# head() permet d'afficher les 5 premières lignes du tableau.
# Cela permet de vérifier que le fichier a bien été lu.
print(df.head())

# On affiche les noms des différentes colonnes du fichier.
print("\nLes colonnes :")

# columns.tolist() récupère les noms des colonnes et les transforme en liste.
print(df.columns.tolist())



# 2. DESCRIPTION DES COLONNES


# On crée un dictionnaire.
# Un dictionnaire associe une information à une autre information.
# Ici, chaque nom de colonne est associé à une description.
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

# On affiche un titre.
print("\nDescription des colonnes :")

# On parcourt toutes les colonnes du tableau df.
# La variable colonne prend le nom de chaque colonne l'une après l'autre.
for colonne in df.columns:

    # On affiche le nom de la colonne et sa description.
    # descriptions.get() recherche la description correspondante.
    # Si la colonne n'existe pas dans le dictionnaire,
    # le programme affiche "Non identifiée".
    print(colonne, ":", descriptions.get(colonne, "Non identifiée"))



# 3. DICTIONNAIRE DES DEPARTEMENTS


# On crée un dictionnaire qui associe chaque numéro de département
# à son nom.
# Par exemple : "76" correspond à "Seine-Maritime".
noms_departements = {
    "01": "Ain", "02": "Aisne", "03": "Allier",
    "04": "Alpes-de-Haute-Provence", "05": "Hautes-Alpes",
    "06": "Alpes-Maritimes", "07": "Ardèche",
    "08": "Ardennes", "09": "Ariège", "10": "Aube",
    "11": "Aude", "12": "Aveyron",
    "13": "Bouches-du-Rhône", "14": "Calvados",
    "15": "Cantal", "16": "Charente",
    "17": "Charente-Maritime", "18": "Cher",
    "19": "Corrèze", "2A": "Corse-du-Sud",
    "2B": "Haute-Corse", "21": "Côte-d'Or",
    "22": "Côtes-d'Armor", "23": "Creuse",
    "24": "Dordogne", "25": "Doubs", "26": "Drôme",
    "27": "Eure", "28": "Eure-et-Loir",
    "29": "Finistère", "30": "Gard",
    "31": "Haute-Garonne", "32": "Gers",
    "33": "Gironde", "34": "Hérault",
    "35": "Ille-et-Vilaine", "36": "Indre",
    "37": "Indre-et-Loire", "38": "Isère",
    "39": "Jura", "40": "Landes",
    "41": "Loir-et-Cher", "42": "Loire",
    "43": "Haute-Loire", "44": "Loire-Atlantique",
    "45": "Loiret", "46": "Lot",
    "47": "Lot-et-Garonne", "48": "Lozère",
    "49": "Maine-et-Loire", "50": "Manche",
    "51": "Marne", "52": "Haute-Marne",
    "53": "Mayenne", "54": "Meurthe-et-Moselle",
    "55": "Meuse", "56": "Morbihan",
    "57": "Moselle", "58": "Nièvre",
    "59": "Nord", "60": "Oise", "61": "Orne",
    "62": "Pas-de-Calais", "63": "Puy-de-Dôme",
    "64": "Pyrénées-Atlantiques", "65": "Hautes-Pyrénées",
    "66": "Pyrénées-Orientales", "67": "Bas-Rhin",
    "68": "Haut-Rhin", "69": "Rhône",
    "70": "Haute-Saône", "71": "Saône-et-Loire",
    "72": "Sarthe", "73": "Savoie",
    "74": "Haute-Savoie", "75": "Paris",
    "76": "Seine-Maritime", "77": "Seine-et-Marne",
    "78": "Yvelines", "79": "Deux-Sèvres",
    "80": "Somme", "81": "Tarn",
    "82": "Tarn-et-Garonne", "83": "Var",
    "84": "Vaucluse", "85": "Vendée",
    "86": "Vienne", "87": "Haute-Vienne",
    "88": "Vosges", "89": "Yonne",
    "90": "Territoire de Belfort",
    "91": "Essonne", "92": "Hauts-de-Seine",
    "93": "Seine-Saint-Denis", "94": "Val-de-Marne",
    "95": "Val-d'Oise",
    "971": "Guadeloupe", "972": "Martinique",
    "973": "Guyane", "974": "La Réunion",
    "976": "Mayotte"
}



# 4. DICTIONNAIRE DES REGIONS

# On crée un deuxième dictionnaire.
# Cette fois, chaque région est associée à une liste de départements.
# Par exemple, la Normandie contient les départements 14, 27, 50, 61 et 76.
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
    "Guadeloupe": ["971"],
    "Martinique": ["972"],
    "Guyane": ["973"],
    "La Réunion": ["974"],
    "Mayotte": ["976"]
}



# 5. EXTRAIRE LE DEPARTEMENT


# On crée une fonction appelée extraire_departement.
# Elle reçoit un code INSEE en paramètre.
def extraire_departement(code):

    # str() transforme le code en texte.
    # strip() enlève les espaces inutiles au début et à la fin.
    # upper() transforme les lettres en majuscules.
    code = str(code).strip().upper()

    # Si le code commence par 2A ou 2B,
    # on récupère les deux premiers caractères.
    # Cela permet de reconnaître les départements corses.
    if code.startswith("2A") or code.startswith("2B"):
        return code[:2]

    # Si le code commence par 971, 972, 973, 974 ou 976,
    # on récupère les trois premiers caractères.
    # Cela permet de reconnaître les départements d'outre-mer.
    if code.startswith(("971", "972", "973", "974", "976")):
        return code[:3]

    # Pour les autres départements,
    # on récupère uniquement les deux premiers caractères.
    return code[:2]



# 6. FONCTION USED_DATA


# Cette fonction permet de rechercher les installations
# selon une zone géographique choisie.
# La zone peut être la France, Paris, une région ou un département.
def used_data(zone):

    # On lit le fichier de données.
    df = pd.read_csv("sup_support.txt", sep=";", dtype=str)

    # On crée une nouvelle colonne appelée DEPARTEMENT.
    # Pour chaque commune, on utilise la fonction précédente
    # pour retrouver son numéro de département à partir du code INSEE.
    df["DEPARTEMENT"] = df["COM_CD_INSEE"].apply(extraire_departement)

    # On nettoie le nom de la zone recherchée.
    # strip() enlève les espaces.
    # casefold() permet de comparer les textes sans tenir compte
    # des différences entre majuscules et minuscules.
    zone = zone.strip().casefold()

    # Si l'utilisateur demande toute la France,
    # on conserve toutes les installations.
    if zone == "france":
        resultat = df

    # Si l'utilisateur demande Paris,
    # on conserve uniquement les installations du département 75.
    elif zone == "paris":
        resultat = df[df["DEPARTEMENT"] == "75"]

    # Dans les autres cas, on recherche une région ou un département.
    else:

        # On crée un tableau vide pour commencer.
        resultat = df.iloc[0:0]

        # On parcourt toutes les régions du dictionnaire.
        for region in regions_departements:

            # On compare le nom de la région demandée
            # avec les noms présents dans le dictionnaire.
            if region.casefold() == zone:

                # isin() vérifie si le département de chaque ligne
                # appartient à la liste des départements de cette région.
                # On conserve uniquement les installations correspondantes.
                resultat = df[
                    df["DEPARTEMENT"].isin(regions_departements[region])
                ]

        # On parcourt ensuite tous les numéros de départements.
        for numero in noms_departements:

            # On vérifie si la zone demandée correspond
            # soit au numéro du département, soit à son nom.
            if numero.casefold() == zone or noms_departements[numero].casefold() == zone:

                # On conserve uniquement les installations
                # appartenant au département recherché.
                resultat = df[df["DEPARTEMENT"] == numero]

    # Si le résultat ne contient aucune ligne,
    # cela signifie qu'aucune installation n'a été trouvée.
    if resultat.empty:
        print("Aucune installation trouvée pour cette zone.")

    # len() compte le nombre de lignes du tableau.
    # Chaque ligne représente une installation.
    nombre = len(resultat)

    # return renvoie deux résultats :
    # le tableau des installations et leur nombre total.
    return resultat, nombre



# 7. CLASSEMENT PAR ECHELLE (3.1)


# Cette fonction permet de compter les installations
# à différentes échelles géographiques :
# France, région, département et commune.
def classement_echelles():

    # On relit le fichier de données.
    df = pd.read_csv("sup_support.txt", sep=";", dtype=str)

    # On ajoute une colonne DEPARTEMENT.
    # Chaque code INSEE est utilisé pour retrouver le département.
    df["DEPARTEMENT"] = df["COM_CD_INSEE"].apply(extraire_departement)

    # On ajoute une nouvelle colonne REGION.
    # Au départ, toutes les cases sont vides.
    df["REGION"] = ""

    # On parcourt chaque région du dictionnaire.
    for region in regions_departements:

        # Pour chaque région, on parcourt ses départements.
        for departement in regions_departements[region]:

            # loc permet de modifier certaines lignes du tableau.
            # On recherche les lignes dont le département correspond.
            # On leur attribue le nom de la région correspondante.
            df.loc[df["DEPARTEMENT"] == departement, "REGION"] = region

    # len(df) compte toutes les lignes du tableau.
    # On obtient donc le nombre total d'installations en France.
    nombre_france = len(df)

    # groupby("REGION") regroupe les installations par région.
    # size() compte le nombre de lignes dans chaque groupe.
    nombre_regions = df.groupby("REGION").size()

    # On regroupe maintenant les installations par département.
    # size() compte le nombre d'installations dans chaque département.
    nombre_departements = df.groupby("DEPARTEMENT").size()

    # On regroupe les installations par commune.
    # Le code INSEE permet d'identifier chaque commune.
    nombre_communes = df.groupby("COM_CD_INSEE").size()

    # On affiche le nombre total d'installations en France.
    print("\nNOMBRE D'INSTALLATIONS EN FRANCE :")
    print(nombre_france)

    # On affiche le nombre d'installations pour chaque région.
    print("\nNOMBRE D'INSTALLATIONS PAR REGION :")
    print(nombre_regions)

    # On affiche le nombre d'installations pour chaque département.
    print("\nNOMBRE D'INSTALLATIONS PAR DEPARTEMENT :")
    print(nombre_departements)

    # On affiche le nombre d'installations pour chaque commune.
    print("\nNOMBRE D'INSTALLATIONS PAR COMMUNE :")
    print(nombre_communes)

    # On renvoie les quatre résultats obtenus.
    return nombre_france, nombre_regions, nombre_departements, nombre_communes



# 8. TESTS DES FONCTIONS


# On appelle la fonction used_data en lui donnant "Normandie".
# La fonction va rechercher toutes les installations de cette région.
# Les deux résultats sont enregistrés dans deux variables :
# installations contient le tableau des installations.
# nombre contient le nombre total d'installations.
installations, nombre = used_data("Normandie")

# On affiche un titre pour présenter les résultats.
print("\nINSTALLATIONS EN NORMANDIE :")

# head() affiche uniquement les cinq premières installations.
print(installations.head())

# On affiche le nombre total d'installations trouvées.
print("Nombre total :", nombre)

# On appelle la fonction classement_echelles().
# Elle affiche les nombres d'installations à chaque échelle géographique.
classement_echelles()



# 9. GRAPHIQUE PAR DEPARTEMENT (3.2)

# On copie les données
nombre_departements = df.copy()

# On récupère les départements
nombre_departements["DEPARTEMENT"] = nombre_departements["COM_CD_INSEE"].apply(extraire_departement)

# On supprime le code 97
nombre_departements = nombre_departements[
    nombre_departements["DEPARTEMENT"] != "97"
]

# On compte les installations par département
nombre_departements = nombre_departements.groupby("DEPARTEMENT").size()

# On crée un graphique très large
plt.figure(figsize=(24, 8))

# On crée un emplacement pour chaque département
positions = range(len(nombre_departements))

# On affiche des barres fines et espacées
plt.bar(positions, nombre_departements.values, width=0.45)

# On ajoute une légende pour expliquer le code 98
plt.plot([], [], " ", label="98 : Territoires d'outre-mer regroupés")
plt.legend()


# On affiche tous les numéros des départements
plt.xticks(positions, nombre_departements.index, rotation=60, fontsize=9)

# On ajoute les titres
plt.title("Nombre d'installations par département", fontsize=16)
plt.xlabel("Départements", fontsize=12)
plt.ylabel("Nombre d'installations", fontsize=12)

# On règle l'échelle verticale
plt.yticks(range(0, 5501, 500))

# On ajoute une grille horizontale
plt.grid(axis="y", linestyle="--", alpha=0.3)
plt.gca().set_axisbelow(True)

# On explique le code 98
plt.figtext(
    0.5, 0.01,
    "98 : territoires dont le code INSEE commence par 98.",
    ha="center",
    fontsize=10
)

# On laisse de l'espace en bas pour lire les départements
plt.subplots_adjust(bottom=0.22, left=0.07, right=0.98, top=0.90)

# On affiche le graphique
plt.show()
