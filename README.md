# SAE15 – Analyse des installations radioélectriques (ANFR)

## Description

Ce projet analyse les données ouvertes de l'ANFR sur les supports, antennes et émetteurs radioélectriques en France.
Il permet de compter les installations par zone géographique, de comparer les exploitants, de suivre l'évolution des technologies mobiles (2G, 3G, 4G, 5G) et de générer des cartes interactives des antennes.

## Installation

Installe les bibliothèques nécessaires depuis le terminal :

```bash
python -m pip install pandas matplotlib folium
```

| Bibliothèque | Utilité |
|---|---|
| pandas | Lecture et traitement des données |
| matplotlib | Graphiques |
| folium | Cartes interactives |

Les modules `os` et `html` sont inclus dans Python : rien à installer pour eux.

Sur macOS et Linux, utilise `python3` à la place de `python`. Sous Windows, tu peux aussi utiliser `py`.