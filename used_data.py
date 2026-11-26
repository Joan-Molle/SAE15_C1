#1.2
import pandas as pd


#Les identifiants doivent rester du texte pour garder les zéros du début (ex : 0010030350) et les lettres de la Corse (2A, 2B).
identifiants = {"STA_NM_ANFR": str, "SUP_ID": str, "AER_ID": str, "EMR_ID": str,"ADM_ID": str, "NAT_ID": str, "TPO_ID": str, "TAE_ID": str,"ADR_NM_CP": str, "COM_CD_INSEE": str, "DEM_NM_COMSIS": str, "STA_NM_USER": str,}


#Tous les fichiers sont lus de la même façon : colonnes séparées par ";", virgule pour les décimales, identifiants en texte.
def lire(chemin):
    return pd.read_csv(chemin, sep=";", decimal=",", dtype=identifiants, encoding="utf-8")


def charger_stations():
    stations = lire("data/sup_station.txt")
    exploitants = lire("ref/sup_exploitant.txt")
    stations = stations.merge(exploitants, on="ADM_ID") #On fusionne les deux fichiers pour avoir le nom de l'exploitant.
    stations["ANNEE"] = stations["DTE_EN_SERVICE"].str[6:10] #On garde uniquement l'année.
    return stations


def coordonnee(degres, minutes, secondes, lettre):
    valeur = degres + minutes/60 + secondes/3600 #On convertit les coordonnées en degrés décimaux.
    if lettre == "S" or lettre == "W":
        valeur = -1*valeur
        #Si on projette N, S, E, W sur un plan cartésien, N et E sont positifs tandis que S et W sont négatifs.
    return valeur


def charger_supports():
    supports = lire("data/sup_support.txt")
    natures = lire("ref/sup_nature.txt")
    supports = supports.merge(natures, on="NAT_ID") #On fusionne les deux fichiers pour avoir la nature du support.

    liste_lat = []
    for d, m, s, l in zip(supports["COR_NB_DG_LAT"], supports["COR_NB_MN_LAT"], supports["COR_NB_SC_LAT"], supports["COR_CD_NS_LAT"]):
        liste_lat.append(coordonnee(d, m, s, l))
    #À chaque tour, zip prend les 4 cases d'une ligne (degrés, minutes, secondes, lettre) et on ajoute la latitude en degrés décimaux à la liste.

    liste_lon = []
    for d, m, s, l in zip(supports["COR_NB_DG_LON"], supports["COR_NB_MN_LON"], supports["COR_NB_SC_LON"], supports["COR_CD_EW_LON"]):
        liste_lon.append(coordonnee(d, m, s, l))
    #Même chose pour la longitude.

    supports["lat"] = liste_lat
    supports["lon"] = liste_lon

    supports["DEPARTEMENT"] = supports["COM_CD_INSEE"].str[:2] #On récupère les deux premiers caractères du code INSEE pour avoir le code du département.
    return supports


def charger_antennes():
    antennes = lire("data/sup_antenne.txt")
    return antennes


#4.1 : on classe chaque émetteur selon sa technologie (GSM = 2G, UMTS = 3G, LTE = 4G, 5G NR = 5G, le reste = Autres).
#Les mots "2G", "3G"... ne sont pas dans le fichier, c'est une convention télécom.
def classer_technologie(systeme):
    if isinstance(systeme, str): #On vérifie que la case contient bien du texte (elle peut être vide).
        if systeme.startswith("GSM"):
            return "2G"
        elif systeme.startswith("UMTS"):
            return "3G"
        elif systeme.startswith("LTE"):
            return "4G"
        elif systeme.startswith("5G NR"):
            return "5G"
    return "Autres"


def charger_emetteurs():
    emetteurs = lire("data/sup_emetteur.txt")
    emetteurs["ANNEE"] = emetteurs["EMR_DT_SERVICE"].str[6:10] #On garde uniquement l'année.
    emetteurs["Technologie"] = emetteurs["EMR_LB_SYSTEME"].apply(classer_technologie) #On ajoute la technologie de chaque émetteur.
    return emetteurs