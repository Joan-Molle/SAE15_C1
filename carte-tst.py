import pandas as pd
import folium
from folium.plugins import MarkerCluster

# 1. Lecture (séparateur ; et virgule décimale)
antennes = pd.read_csv("sup_antenne.txt", sep=";", decimal=",",
                       encoding="latin-1", dtype=str)
supports = pd.read_csv("SUP_SUPPORT.txt", sep=";", decimal=",",
                       encoding="latin-1", dtype=str)

# 2. Conversion DMS -> degrés décimaux
def dms(deg, mn, sc, hemi):
    val = float(deg) + float(mn) / 60 + float(sc) / 3600
    return -val if hemi in ("S", "W") else val

supports["lat"] = supports.apply(lambda r: dms(r["COR_NB_DG_LAT"], r["COR_NB_MN_LAT"],
                                               r["COR_NB_SC_LAT"], r["COR_CD_NS_LAT"]), axis=1)
supports["lon"] = supports.apply(lambda r: dms(r["COR_NB_DG_LON"], r["COR_NB_MN_LON"],
                                               r["COR_NB_SC_LON"], r["COR_CD_EW_LON"]), axis=1)

# 3. Jointure sur SUP_ID (une ligne par support, avec le nb d'antennes)
nb = antennes.groupby("SUP_ID").size().rename("nb_antennes").reset_index()
data = supports.merge(nb, on="SUP_ID")

# 4. Filtre sur une zone (ici autour de Rouen) pour ne pas afficher 100 000 points
data = data[data["lat"].between(49.35, 49.50) & data["lon"].between(0.95, 1.25)]

# 5. Carte
carte = folium.Map(location=[49.44, 1.095], zoom_start=13)
cluster = MarkerCluster().add_to(carte)

for _, r in data.iterrows():
    folium.CircleMarker(
        location=[r["lat"], r["lon"]],
        radius=5, color="red", fill=True, fill_color="red",
        popup=f"Support {r['SUP_ID']}<br>{r['nb_antennes']} antenne(s)",
    ).add_to(cluster)

carte.save("carte_antennes.html")
print(len(data), "supports affichés")