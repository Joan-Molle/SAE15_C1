import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Charger les donnees
dossier = Path(__file__).resolve().parent

df = pd.read_csv(
    dossier / "data/sup_emetteur.txt",
    sep=";", dtype=str, encoding="latin1"
)

# Convertir les dates
df["Date"] = pd.to_datetime(
    df["EMR_DT_SERVICE"],
    dayfirst=True,
    errors="coerce"
)

df["Annee"] = df["Date"].dt.year

# Regrouper les technologies
systeme = df["EMR_LB_SYSTEME"].str.upper()

df.loc[systeme.str.contains("GSM", na=False), "Techno"] = "2G"
df.loc[systeme.str.contains("UMTS", na=False), "Techno"] = "3G"
df.loc[systeme.str.contains("LTE", na=False), "Techno"] = "4G"
df.loc[systeme.str.contains("5G NR", na=False), "Techno"] = "5G"

# Selectionner les annees
df = df[df["Annee"].between(1990, 2026)]

# Compter les emetteurs par annee
evolution = df.groupby(
    ["Annee", "Techno"]
).size().unstack(fill_value=0)

evolution = evolution.reindex(
    index=range(1990, 2027),
    columns=["2G", "3G", "4G", "5G"],
    fill_value=0
)

# Calculer le nombre cumule
evolution = evolution.cumsum()

# Creer les courbes
plt.figure(figsize=(14, 7))

for techno in evolution.columns:
    plt.plot(
        evolution.index,
        evolution[techno],
        label=techno,
        linewidth=3
    )

plt.title("Evolution des technologies mobiles")
plt.xlabel("Annee")
plt.ylabel("Nombre cumule d'emetteurs")
plt.legend(title="Technologies")
plt.grid(alpha=0.3)
plt.xlim(1990, 2026)
plt.ylim(bottom=0)
plt.tight_layout()

# Enregistrer et afficher
plt.savefig(
    dossier / "evolution_technologies.png",
    dpi=300
)

plt.show()