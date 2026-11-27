import os
import html
import folium
import pandas as pd
import matplotlib.pyplot as plt
from folium.plugins import MarkerCluster

# =====================================================================
# 1. CHARGEMENT DES DONNEES (les tables sont trouvées par leurs colonnes,
#    quel que soit le nom des fichiers dans data/ et ref/)
# =====================================================================

BASE = os.path.dirname(os.path.abspath(__file__))
DOSSIERS = [os.path.join(BASE, "data"), os.path.join(BASE, "ref")]

identifiants = {"STA_NM_ANFR": str, "SUP_ID": str, "AER_ID": str, "EMR_ID": str, "ADM_ID": str,
                "NAT_ID": str, "TPO_ID": str, "TAE_ID": str, "ADR_NM_CP": str, "COM_CD_INSEE": str,
                "DEM_NM_COMSIS": str, "STA_NM_USER": str}


def lire(chemin, **options):
    try:
        df = pd.read_csv(chemin, sep=";", decimal=",", dtype=identifiants, encoding="utf-8-sig", **options)
    except UnicodeDecodeError:
        df = pd.read_csv(chemin, sep=";", decimal=",", dtype=identifiants, encoding="latin-1", **options)
    df.columns = df.columns.str.strip()
    return df


_cache = {}

def trouver(colonnes, obligatoire=True):
    """Cherche dans data/ et ref/ le fichier qui contient toutes les colonnes demandées."""
    cle = tuple(colonnes)
    if cle in _cache:
        return _cache[cle]
    for dossier in DOSSIERS:
        if not os.path.isdir(dossier):
            continue
        for nom in sorted(os.listdir(dossier)):
            chemin = os.path.join(dossier, nom)
            if not os.path.isfile(chemin):
                continue
            try:
                entete = lire(chemin, nrows=0)
            except Exception:
                continue
            if set(colonnes) <= set(entete.columns):
                _cache[cle] = chemin
                return chemin
    if obligatoire:
        raise FileNotFoundError(f"Aucun fichier de data/ ou ref/ ne contient les colonnes : {colonnes}")
    return None


def charger_stations():
    stations = lire(trouver(["STA_NM_ANFR", "ADM_ID", "DTE_EN_SERVICE"]))
    exploitants = lire(trouver(["ADM_ID", "ADM_LB_NOM"]))
    stations = stations.merge(exploitants, on="ADM_ID", how="left")
    stations["ANNEE"] = stations["DTE_EN_SERVICE"].str[6:10]
    return stations


def coordonnee(degres, minutes, secondes, lettre):
    valeur = degres + minutes/60 + secondes/3600      # degrés décimaux
    if lettre == "S" or lettre == "W":
        valeur = -1*valeur                            # S et W sont négatifs
    return valeur


def charger_supports():
    supports = lire(trouver(["SUP_ID", "COR_NB_DG_LAT", "COR_NB_DG_LON"]))
    chemin_nature = trouver(["NAT_ID", "NAT_LB_NOM"], obligatoire=False)
    if chemin_nature:
        supports = supports.merge(lire(chemin_nature), on="NAT_ID", how="left")

    for col in ["COR_NB_DG_LAT", "COR_NB_MN_LAT", "COR_NB_SC_LAT",
                "COR_NB_DG_LON", "COR_NB_MN_LON", "COR_NB_SC_LON", "SUP_NM_HAUT"]:
        supports[col] = pd.to_numeric(supports[col].astype(str).str.replace(",", ".", regex=False),
                                      errors="coerce")

    liste_lat = []
    for d, m, s, l in zip(supports["COR_NB_DG_LAT"], supports["COR_NB_MN_LAT"],
                          supports["COR_NB_SC_LAT"], supports["COR_CD_NS_LAT"]):
        liste_lat.append(coordonnee(d, m, s, l))
    liste_lon = []
    for d, m, s, l in zip(supports["COR_NB_DG_LON"], supports["COR_NB_MN_LON"],
                          supports["COR_NB_SC_LON"], supports["COR_CD_EW_LON"]):
        liste_lon.append(coordonnee(d, m, s, l))
    supports["lat"] = liste_lat
    supports["lon"] = liste_lon

    supports["DEPARTEMENT"] = supports["COM_CD_INSEE"].str[:2]
    return supports


def charger_antennes():
    return lire(trouver(["AER_ID", "AER_NB_ALT_BAS", "SUP_ID", "TAE_ID"]))


def charger_emetteurs():
    emetteurs = lire(trouver(["EMR_ID", "EMR_LB_SYSTEME", "EMR_DT_SERVICE"]))
    emetteurs["ANNEE"] = emetteurs["EMR_DT_SERVICE"].str[6:10]
    return emetteurs


def charger_proprietaires():
    return lire(trouver(["TPO_ID", "TPO_LB"]))


def charger_types():
    return lire(trouver(["TAE_ID", "TAE_LB"]))


# =====================================================================
# 2. EMETTEURS ET TECHNOLOGIES
# =====================================================================

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


def technologies():
    emetteurs = charger_emetteurs()

    print("\nLes 5 premieres lignes :")
    print(emetteurs.head())

    print("\nNombre d'emetteurs par systeme :")
    print(emetteurs["EMR_LB_SYSTEME"].value_counts())

    print("\nNombre total d'emetteurs :")
    print(len(emetteurs))

    emetteurs["Technologie"] = emetteurs["EMR_LB_SYSTEME"].apply(classer_technologie)
    comptage_technologie = emetteurs["Technologie"].value_counts()
    print("\nNombre d'emetteurs par technologie :")
    print(comptage_technologie)

    donnees_graphique = comptage_technologie.reindex(["2G", "3G", "4G", "5G"], fill_value=0)

    plt.figure(figsize=(9, 5))
    plt.bar(donnees_graphique.index, donnees_graphique.values)
    plt.title("Nombre d'emetteurs par technologie")
    plt.xlabel("Technologie")
    plt.ylabel("Nombre d'emetteurs")
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("graphique_technologies.png")
    plt.show()

    # Dictionnaire de recherche d'un emetteur
    dictionnaire_emetteurs = emetteurs.set_index("EMR_ID").to_dict("index")

    def rechercher_emetteur(id_emetteur):
        if id_emetteur in dictionnaire_emetteurs:
            print("\nInformations de l'emetteur :")
            for cle, valeur in dictionnaire_emetteurs[id_emetteur].items():
                print(f"{cle} : {valeur}")
        else:
            print("Aucun emetteur trouve avec cet ID.")

    rechercher_emetteur("850")


# =====================================================================
# 3. CLASSEMENT DES EXPLOITANTS
# =====================================================================

def classement_exploitants():
    stations = charger_stations()
    resultat = stations["ADM_LB_NOM"].fillna("Exploitant inconnu").value_counts().head(10)
    resultat.to_csv("classement_exploitants.csv", header=["Nombre d'installations"])
    print("\nClassement des exploitants :")
    print(resultat)

    plt.bar(resultat.index, resultat.values)
    plt.title("Nombre d'installations par exploitant")
    plt.xlabel("Exploitants")
    plt.ylabel("Nombre d'installations")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


# =====================================================================
# 4. GEOGRAPHIE (departements, regions, graphique)
# =====================================================================

noms_departements = {
    "01": "Ain", "02": "Aisne", "03": "Allier", "04": "Alpes-de-Haute-Provence", "05": "Hautes-Alpes",
    "06": "Alpes-Maritimes", "07": "Ardèche", "08": "Ardennes", "09": "Ariège", "10": "Aube",
    "11": "Aude", "12": "Aveyron", "13": "Bouches-du-Rhône", "14": "Calvados", "15": "Cantal",
    "16": "Charente", "17": "Charente-Maritime", "18": "Cher", "19": "Corrèze", "2A": "Corse-du-Sud",
    "2B": "Haute-Corse", "21": "Côte-d'Or", "22": "Côtes-d'Armor", "23": "Creuse", "24": "Dordogne",
    "25": "Doubs", "26": "Drôme", "27": "Eure", "28": "Eure-et-Loir", "29": "Finistère", "30": "Gard",
    "31": "Haute-Garonne", "32": "Gers", "33": "Gironde", "34": "Hérault", "35": "Ille-et-Vilaine",
    "36": "Indre", "37": "Indre-et-Loire", "38": "Isère", "39": "Jura", "40": "Landes",
    "41": "Loir-et-Cher", "42": "Loire", "43": "Haute-Loire", "44": "Loire-Atlantique", "45": "Loiret",
    "46": "Lot", "47": "Lot-et-Garonne", "48": "Lozère", "49": "Maine-et-Loire", "50": "Manche",
    "51": "Marne", "52": "Haute-Marne", "53": "Mayenne", "54": "Meurthe-et-Moselle", "55": "Meuse",
    "56": "Morbihan", "57": "Moselle", "58": "Nièvre", "59": "Nord", "60": "Oise", "61": "Orne",
    "62": "Pas-de-Calais", "63": "Puy-de-Dôme", "64": "Pyrénées-Atlantiques", "65": "Hautes-Pyrénées",
    "66": "Pyrénées-Orientales", "67": "Bas-Rhin", "68": "Haut-Rhin", "69": "Rhône", "70": "Haute-Saône",
    "71": "Saône-et-Loire", "72": "Sarthe", "73": "Savoie", "74": "Haute-Savoie", "75": "Paris",
    "76": "Seine-Maritime", "77": "Seine-et-Marne", "78": "Yvelines", "79": "Deux-Sèvres", "80": "Somme",
    "81": "Tarn", "82": "Tarn-et-Garonne", "83": "Var", "84": "Vaucluse", "85": "Vendée", "86": "Vienne",
    "87": "Haute-Vienne", "88": "Vosges", "89": "Yonne", "90": "Territoire de Belfort", "91": "Essonne",
    "92": "Hauts-de-Seine", "93": "Seine-Saint-Denis", "94": "Val-de-Marne", "95": "Val-d'Oise",
    "971": "Guadeloupe", "972": "Martinique", "973": "Guyane", "974": "La Réunion", "976": "Mayotte"
}

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


def extraire_departement(code):
    code = str(code).strip().upper()
    if code.startswith("2A") or code.startswith("2B"):
        return code[:2]                                           # Corse
    if code.startswith(("971", "972", "973", "974", "976")):
        return code[:3]                                           # outre-mer
    return code[:2]


def used_data(zone):
    """Renvoie (installations, nombre) pour la France, Paris, une région ou un département."""
    df = charger_supports()
    df["DEPARTEMENT"] = df["COM_CD_INSEE"].apply(extraire_departement)
    zone = zone.strip().casefold()

    if zone == "france":
        resultat = df
    elif zone == "paris":
        resultat = df[df["DEPARTEMENT"] == "75"]
    else:
        resultat = df.iloc[0:0]
        for region in regions_departements:
            if region.casefold() == zone:
                resultat = df[df["DEPARTEMENT"].isin(regions_departements[region])]
        for numero in noms_departements:
            if numero.casefold() == zone or noms_departements[numero].casefold() == zone:
                resultat = df[df["DEPARTEMENT"] == numero]

    if resultat.empty:
        print("Aucune installation trouvée pour cette zone.")
    return resultat, len(resultat)


def classement_echelles():
    df = charger_supports()
    df["DEPARTEMENT"] = df["COM_CD_INSEE"].apply(extraire_departement)
    df["REGION"] = ""
    for region in regions_departements:
        for departement in regions_departements[region]:
            df.loc[df["DEPARTEMENT"] == departement, "REGION"] = region

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


def geographie():
    df = charger_supports()
    print("Les 5 premières lignes :")
    print(df.head())
    print("\nLes colonnes :")
    print(df.columns.tolist())

    installations, nombre = used_data("Normandie")
    print("\nINSTALLATIONS EN NORMANDIE :")
    print(installations.head())
    print("Nombre total :", nombre)

    classement_echelles()

    # Graphique : nombre d'installations par département
    nombre_departements = df.copy()
    nombre_departements["DEPARTEMENT"] = nombre_departements["COM_CD_INSEE"].apply(extraire_departement)
    nombre_departements = nombre_departements[nombre_departements["DEPARTEMENT"] != "97"]
    nombre_departements = nombre_departements.groupby("DEPARTEMENT").size()

    plt.figure(figsize=(24, 8))
    positions = range(len(nombre_departements))
    plt.bar(positions, nombre_departements.values, width=0.45)
    plt.plot([], [], " ", label="98 : Territoires d'outre-mer regroupés")
    plt.legend()
    plt.xticks(positions, nombre_departements.index, rotation=60, fontsize=9)
    plt.title("Nombre d'installations par département", fontsize=16)
    plt.xlabel("Départements", fontsize=12)
    plt.ylabel("Nombre d'installations", fontsize=12)
    plt.yticks(range(0, 5501, 500))
    plt.grid(axis="y", linestyle="--", alpha=0.3)
    plt.gca().set_axisbelow(True)
    plt.figtext(0.5, 0.01, "98 : territoires dont le code INSEE commence par 98.", ha="center", fontsize=10)
    plt.subplots_adjust(bottom=0.22, left=0.07, right=0.98, top=0.90)
    plt.show()


# =====================================================================
# 5. EVOLUTION DES TECHNOLOGIES
# =====================================================================

def evolution_technologies():
    df = charger_emetteurs()
    df["Date"] = pd.to_datetime(df["EMR_DT_SERVICE"], dayfirst=True, errors="coerce")
    df["Annee"] = df["Date"].dt.year

    systeme = df["EMR_LB_SYSTEME"].str.upper()
    df.loc[systeme.str.contains("GSM", na=False), "Techno"] = "2G"
    df.loc[systeme.str.contains("UMTS", na=False), "Techno"] = "3G"
    df.loc[systeme.str.contains("LTE", na=False), "Techno"] = "4G"
    df.loc[systeme.str.contains("5G NR", na=False), "Techno"] = "5G"

    df = df[df["Annee"].between(1990, 2026)]
    evolution = df.groupby(["Annee", "Techno"]).size().unstack(fill_value=0)
    evolution = evolution.reindex(index=range(1990, 2027), columns=["2G", "3G", "4G", "5G"], fill_value=0)
    evolution = evolution.cumsum()                                  # nombre cumulé

    plt.figure(figsize=(14, 7))
    for techno in evolution.columns:
        plt.plot(evolution.index, evolution[techno], label=techno, linewidth=3)
    plt.title("Evolution des technologies mobiles")
    plt.xlabel("Annee")
    plt.ylabel("Nombre cumule d'emetteurs")
    plt.legend(title="Technologies")
    plt.grid(alpha=0.3)
    plt.xlim(1990, 2026)
    plt.ylim(bottom=0)
    plt.tight_layout()
    plt.savefig(os.path.join(BASE, "evolution_technologies.png"), dpi=300)
    plt.show()


# =====================================================================
# 6. CARTE INTERACTIVE DES ANTENNES
# =====================================================================

MAX_LIGNES = 12                                 # lignes d'antennes max affichées par popup
DOSSIER_CARTES = "cartes"                       # dossier des cartes par département

URL_IGN = ("https://data.geopf.fr/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0"
           "&STYLE=normal&TILEMATRIXSET=PM&FORMAT={format}&LAYER={layer}"
           "&TILEMATRIX={{z}}&TILEROW={{y}}&TILECOL={{x}}")


def texte_hauteur(h_min, h_max):
    if pd.isna(h_min):
        return ""
    if h_min == h_max:
        return f" à {h_min:g} m"
    return f" à {h_min:g}-{h_max:g} m"


def propre(valeur, defaut="?"):
    return html.escape(str(valeur)) if pd.notna(valeur) and str(valeur).strip() else defaut


def construire_carte(sous, chemin, faire_popup):
    carte = folium.Map(tiles=None)
    carte.fit_bounds([[sous["lat"].quantile(0.01), sous["lon"].quantile(0.01)],
                      [sous["lat"].quantile(0.99), sous["lon"].quantile(0.99)]])

    folium.TileLayer(
        tiles=URL_IGN.format(format="image/png", layer="GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2"),
        attr="© IGN - Géoplateforme", name="Plan IGN", max_zoom=19,
    ).add_to(carte)
    folium.TileLayer(
        tiles=URL_IGN.format(format="image/jpeg", layer="ORTHOIMAGERY.ORTHOPHOTOS"),
        attr="© IGN - Géoplateforme", name="Photos aériennes IGN", max_zoom=19, show=False,
    ).add_to(carte)

    cluster = MarkerCluster(name="Antennes").add_to(carte)
    for r in sous.itertuples():
        folium.CircleMarker(
            location=[r.lat, r.lon], radius=5, color="red", fill=True, fill_opacity=0.7,
            popup=folium.Popup(faire_popup(r), max_width=380),
        ).add_to(cluster)

    folium.LayerControl().add_to(carte)
    carte.save(chemin)


def carte_antennes():
    dep = input("Département (vide = tout) : ").strip()

    supports = charger_supports()
    antennes = charger_antennes()
    stations = charger_stations()
    ref_proprio = charger_proprietaires()
    ref_type = charger_types()

    data = supports.dropna(subset=["lat", "lon"]).drop_duplicates(subset="SUP_ID")

    cp = data["ADR_NM_CP"].fillna("").str.strip()
    data = data.assign(dep=cp.str[:3].where(cp.str.startswith(("97", "98")), cp.str[:2]))
    data["dep"] = data["dep"].replace("", "??")

    if dep:
        dep = dep.zfill(2)
        data = data[data["ADR_NM_CP"].str.startswith(dep, na=False)]

    print(len(data), "supports retenus")
    if data.empty:
        print("Aucun support : vérifie le département.")
        return

    data = data.merge(ref_proprio, on="TPO_ID", how="left")

    ant = antennes[antennes["SUP_ID"].isin(data["SUP_ID"])]
    ant = ant.merge(stations[["STA_NM_ANFR", "ADM_ID", "ADM_LB_NOM"]].drop_duplicates("STA_NM_ANFR"),
                    on="STA_NM_ANFR", how="left")
    ant = ant.merge(ref_type, on="TAE_ID", how="left")
    ant["alt"] = pd.to_numeric(ant["AER_NB_ALT_BAS"], errors="coerce")
    ant["ADM_LB_NOM"] = ant["ADM_LB_NOM"].fillna("Exploitant inconnu")
    ant["TAE_LB"] = ant["TAE_LB"].fillna("Type inconnu")

    groupes = (ant.groupby(["SUP_ID", "ADM_LB_NOM", "TAE_LB"])
                  .agg(n=("AER_ID", "nunique"), h_min=("alt", "min"), h_max=("alt", "max"))
                  .reset_index())

    lignes, total = {}, {}
    for r in groupes.itertuples():
        texte = (f"<b>{html.escape(r.ADM_LB_NOM)}</b> : {html.escape(r.TAE_LB)} "
                 f"×{r.n}{texte_hauteur(r.h_min, r.h_max)}")
        lignes.setdefault(r.SUP_ID, []).append(texte)
        total[r.SUP_ID] = total.get(r.SUP_ID, 0) + r.n

    def faire_popup(r):
        adresse = r.ADR_LB_LIEU if pd.notna(r.ADR_LB_LIEU) else r.ADR_LB_ADD1
        liste = lignes.get(r.SUP_ID, [])
        visibles = liste[:MAX_LIGNES]
        if len(liste) > MAX_LIGNES:
            visibles.append(f"… et {len(liste) - MAX_LIGNES} autre(s)")
        return (
            f"<b>{propre(adresse, 'Support')}</b><br>{propre(r.ADR_NM_CP, '')}<hr style='margin:4px 0'>"
            f"<b>Hauteur du support :</b> {propre(r.SUP_NM_HAUT)} m<br>"
            f"<b>Propriétaire :</b> {propre(r.TPO_LB)}<br>"
            f"<b>Antennes :</b> {total.get(r.SUP_ID, 0)}<br>"
            f"<div style='max-height:180px;overflow:auto'>{'<br>'.join(visibles)}</div>")

    os.makedirs(DOSSIER_CARTES, exist_ok=True)

    if dep:
        construire_carte(data, "carte_antennes.html", faire_popup)
        print("carte enregistrée : carte_antennes.html")
    else:
        liens = []
        for code, sous in data.groupby("dep"):
            fichier = f"carte_{code}.html"
            construire_carte(sous, os.path.join(DOSSIER_CARTES, fichier), faire_popup)
            liens.append((code, len(sous), fichier))
            print("département", code, ":", len(sous), "supports")

        lignes_index = "".join(f'<li><a href="{f}">Département {c}</a> ({n} supports)</li>'
                               for c, n, f in liens)
        with open(os.path.join(DOSSIER_CARTES, "index.html"), "w", encoding="utf-8") as fichier_index:
            fichier_index.write("<!DOCTYPE html><html lang='fr'><head><meta charset='utf-8'>"
                                "<title>Cartes des antennes</title></head><body style='font-family:sans-serif'>"
                                f"<h1>Cartes des antennes par département</h1><ul>{lignes_index}</ul></body></html>")
        print("page d'accueil :", os.path.join(DOSSIER_CARTES, "index.html"))


# =====================================================================
# 7. MENU PRINCIPAL
# =====================================================================

MENU = {
    "1": ("Emetteurs et technologies", technologies),
    "2": ("Classement des exploitants", classement_exploitants),
    "3": ("Géographie (départements, régions)", geographie),
    "4": ("Evolution des technologies", evolution_technologies),
    "5": ("Carte interactive des antennes", carte_antennes),
}

if __name__ == "__main__":
    print("Que veux-tu lancer ?")
    for numero, (titre, _) in MENU.items():
        print(f"  {numero} : {titre}")
    print("  0 : Tout lancer")
    choix = input("Choix : ").strip()

    if choix == "0":
        for titre, fonction in MENU.values():
            print(f"\n===== {titre} =====")
            fonction()
    elif choix in MENU:
        MENU[choix][1]()
    else:
        print("Choix non reconnu.")