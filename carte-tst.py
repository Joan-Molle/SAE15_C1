import pandas as pd
import numpy as np
import folium
from folium.plugins import FastMarkerCluster

# ------------------------------------------------------------
# CHOIX DE LA ZONE : change juste cette ligne
# ------------------------------------------------------------
ZONE = "France"

ZONES = {
    #            lat_min, lat_max, lon_min, lon_max
    "France":    (41.0, 51.5, -5.5, 10.0),    # France métropolitaine
    "Normandie": (48.4, 50.1, -1.9, 1.8),
    "Paris":     (48.7, 49.0, 2.1, 2.6),
    "Marseille": (43.2, 43.4, 5.3, 5.5),
}
lat_min, lat_max, lon_min, lon_max = ZONES[ZONE]

# 1. Lecture
antennes = pd.read_csv("sup_antenne.txt", sep=";", decimal=",", encoding="latin-1", dtype=str)
supports = pd.read_csv("SUP_SUPPORT.txt", sep=";", decimal=",", encoding="latin-1", dtype=str)

# 2. Conversion DMS -> degrés décimaux (version rapide, sur toute la colonne d'un coup)
def dms(deg, mn, sc, hemi):
    val = (pd.to_numeric(deg, errors="coerce")
           + pd.to_numeric(mn, errors="coerce") / 60
           + pd.to_numeric(sc, errors="coerce") / 3600)
    return np.where(hemi.isin(["S", "W"]), -val, val)

supports["lat"] = dms(supports["COR_NB_DG_LAT"], supports["COR_NB_MN_LAT"],
                      supports["COR_NB_SC_LAT"], supports["COR_CD_NS_LAT"])
supports["lon"] = dms(supports["COR_NB_DG_LON"], supports["COR_NB_MN_LON"],
                      supports["COR_NB_SC_LON"], supports["COR_CD_EW_LON"])

# 3. Jointure
nb = antennes.groupby("SUP_ID").size().rename("nb_antennes").reset_index()
data = supports.merge(nb, on="SUP_ID")

# 4. Filtre : on enlève les lignes sans coordonnées, puis on garde la zone choisie
data = data.dropna(subset=["lat", "lon"])
data = data[data["lat"].between(lat_min, lat_max) & data["lon"].between(lon_min, lon_max)]

# 5. Carte IGN (centrée automatiquement sur la zone choisie)
IGN_URL = ("https://data.geopf.fr/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0"
           "&STYLE=normal&TILEMATRIXSET=PM&FORMAT={format}&LAYER={layer}"
           "&TILEMATRIX={{z}}&TILEROW={{y}}&TILECOL={{x}}")

carte = folium.Map(tiles=None)
carte.fit_bounds([[lat_min, lon_min], [lat_max, lon_max]])   # cadre la carte sur la zone

folium.TileLayer(
    tiles=IGN_URL.format(format="image/png", layer="GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2"),
    attr="© IGN - Géoplateforme", name="Plan IGN", max_zoom=19,
).add_to(carte)

folium.TileLayer(
    tiles=IGN_URL.format(format="image/jpeg", layer="ORTHOIMAGERY.ORTHOPHOTOS"),
    attr="© IGN - Géoplateforme", name="Photographies aériennes IGN", max_zoom=19, show=False,
).add_to(carte)

# 6. Points : liste de [lat, lon, texte du popup]
points = [
    [lat, lon, f"Support {sup}<br>{n} antenne(s)"]
    for lat, lon, sup, n in zip(data["lat"], data["lon"], data["SUP_ID"], data["nb_antennes"])
]

# Petit code JavaScript qui dessine un rond rouge par point (ultra rapide)
callback = """
function (row) {
    var marker = L.circleMarker(new L.LatLng(row[0], row[1]),
                                {radius: 5, color: "red", fillOpacity: 0.7});
    marker.bindPopup(row[2]);
    return marker;
};
"""

FastMarkerCluster(points, callback=callback, name="Antennes").add_to(carte)
folium.LayerControl().add_to(carte)

carte.save("carte_antennes.html")
print(len(data), "supports affichés")