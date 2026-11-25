import pandas as pd


identifiants = {"STA_NM_ANFR": str, "SUP_ID": str, "AER_ID": str, "EMR_ID": str,"ADM_ID": str, "NAT_ID": str, "TPO_ID": str, "TAE_ID": str,"ADR_NM_CP": str, "COM_CD_INSEE": str, "DEM_NM_COMSIS": str, "STA_NM_USER": str,}


def lire(chemin):
    return pd.read_csv(chemin, sep=";", decimal=",", dtype=identifiants, encoding="utf-8")

def charger_stations():
    stations = lire("data/sup_station.txt")
    exploitants = lire("ref/sup_exploitant.txt")
    stations = stations.merge(exploitants, on="ADM_ID")
    stations["ANNEE"] = stations["DTE_EN_SERVICE"].str[6:10] #On garde uniquement l'année
    return stations


def coordonnee(degres, minutes, secondes, lettre):
    valeur = degres + minutes/60 + secondes/3600 #on convertit les coordonnées en degrés décimaux
    if lettre == "S" or lettre == "W":
        valeur = -1*valeur
        #si on projette N, S, E, W sur un plan cartésien, N et E sont positifs tandis que S et W sont négatifs.
    return valeur



def charger_supports():
    supports = lire("data/sup_support.txt")
    natures = lire("ref/sup_nature.txt")
    supports = supports.merge(natures, on="NAT_ID")
    liste_lat = []
    
    for d, m, s, l in zip(supports["COR_NB_DG_LAT"], supports["COR_NB_MN_LAT"], supports["COR_NB_SC_LAT"], supports["COR_CD_NS_LAT"]):
        liste_lat.append(coordonnee(d, m, s, l))
    #la boucle retourne les coordonnées en degrés décimaux (latitude)
    liste_lon = []
    for d, m, s, l in zip(supports["COR_NB_DG_LON"], supports["COR_NB_MN_LON"], supports["COR_NB_SC_LON"], supports["COR_CD_EW_LON"]):
        liste_lon.append(coordonnee(d, m, s, l))
    #la boucle retourne les coordonnées en degrés décimaux (longitude)
    supports["lat"] = liste_lat
    supports["lon"] = liste_lon

    supports["DEPARTEMENT"] = supports["COM_CD_INSEE"].str[:2]
    return supports

def charger_antennes():
    antennes = lire("data/sup_antenne.txt")
    return antennes

def charger_emetteurs():
    emetteurs = lire("data/sup_emetteur.txt")
    emetteurs["ANNEE"] = emetteurs["EMR_DT_SERVICE"].str[6:10]
    return emetteurs