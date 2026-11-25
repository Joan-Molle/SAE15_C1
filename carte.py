import folium
import pandas as pd
from folium.plugins import FastMarkerCluster

# ---------- Paramètres ----------
ZONE = "France"
ZONES = {
    "France":    (41.3, 51.1, -5.5, 9.0),   # lat_min, lat_max, lon_min, lon_max
    "Normandie": (48.4, 50.1, -1.9, 1.8),
}
lat_min, lat_max, lon_min, lon_max = ZONES[ZONE]

URL_IGN = ("https://data.geopf.fr/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0"
           "&STYLE=normal&TILEMATRIXSET=PM&FORMAT={format}&LAYER={layer}"
           "&TILEMATRIX={{z}}&TILEROW={{y}}&TILECOL={{x}}")

# ---------- 1. Lecture ----------
supports = pd.read_csv("SUP_SUPPORT.txt", encoding="latin-1", sep=";", dtype=str)
antennes = pd.read_csv("sup_antenne.txt", encoding="latin-1", sep=";", dtype=str)

# ---------- 2. Conversion DMS -> degrés décimaux ----------
def en_nombre(serie):
    # "12,5" -> 12.5 ; valeur invalide -> NaN
    return pd.to_numeric(serie.str.replace(",", ".", regex=False), errors="coerce")

def dms_vers_decimal(deg, mn, sc, hemi):
    valeur = en_nombre(deg) + en_nombre(mn) / 60 + en_nombre(sc) / 3600
    return valeur.where(~hemi.isin(["S", "W"]), -valeur)

supports["lat"] = dms_vers_decimal(supports["COR_NB_DG_LAT"], supports["COR_NB_MN_LAT"],
                                   supports["COR_NB_SC_LAT"], supports["COR_CD_NS_LAT"])
supports["lon"] = dms_vers_decimal(supports["COR_NB_DG_LON"], supports["COR_NB_MN_LON"],
                                   supports["COR_NB_SC_LON"], supports["COR_CD_EW_LON"])

# ---------- 3. Jointure ----------
def ajouter_nb_antennes(supports, antennes):
    nb = antennes.groupby("SUP_ID").size().rename("nb_antennes").reset_index()
    return supports.merge(nb, on="SUP_ID")

data = ajouter_nb_antennes(supports, antennes)

# ---------- 4. Filtre ----------
data = data.dropna(subset=["lat", "lon"])
masque = data["lat"].between(lat_min, lat_max) & data["lon"].between(lon_min, lon_max)
data = data[masque]
print(len(data), "supports dans la zone")

# ---------- 5. Carte ----------
carte = folium.Map(tiles=None)
carte.fit_bounds([[lat_min, lon_min], [lat_max, lon_max]])

folium.TileLayer(
    tiles=URL_IGN.format(format="image/png", layer="GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2"),
    attr="© IGN - Géoplateforme",
    name="Plan IGN",
    max_zoom=19,
).add_to(carte)

folium.TileLayer(
    tiles=URL_IGN.format(format="image/jpeg", layer="ORTHOIMAGERY.ORTHOPHOTOS"),
    attr="© IGN - Géoplateforme",
    name="Photos aériennes IGN",
    max_zoom=19,
    show=False,
).add_to(carte)

# ---------- 6. Points ----------
points = data[["lat", "lon"]].values.tolist()
FastMarkerCluster(points, name="Antennes").add_to(carte)

folium.LayerControl().add_to(carte)
carte.save("carte_antennes.html")
print("carte enregistrée :", len(points), "points")