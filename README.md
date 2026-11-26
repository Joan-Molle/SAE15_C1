##### **SAE 15 - << Mais que fait l'ANFR ? >>**

* ###### **Démarche :**

Le but du projet étant de décrire les installations radioélectriques en France à partir des fichiers publics de l'ANFR, nous avons lu, relié et trié ces fichiers avec Python (module <<pandas>>) afin de mettre au point :

- un classement des 10 plus gros exploitants selon leur nombre d'installations, avec un graphique en barres.
- un graphique sur les technologies (2G, 3G, 4G, 5G) utilisées par le TOP 10 des plus gros exploitants.
- un comptage des installations par zone (France, région, département, commune), avec un graphique par département.
- un graphique sur le nombre d'émetteurs par technologie.
- un graphique sur l'évolution des technologies, selon l'année de mise en service (2017 à 2026).
- une carte interactive des supports d'antennes.

* ###### **Structure du code :**

- used_data.py (1.2) : c'est le fichier qui lit les données. Tous les autres se servent dedans au lieu de relire les fichiers eux-mêmes.
- classement_exploitant.py (2.1) : on classe les 10 plus gros exploitants selon leur nombre d'installations, et on met tous les autres dans <<Autres>>.
- graphique_exploitant.py (2.2) : on fait un graphique en barres avec le classement du 2.1.
- graphe_technologie_exploitant.py (2.3) : on compte les émetteurs 2G, 3G, 4G, 5G et Autres des 10 plus gros exploitants.
- geographie.py (3.1 et 3.2) : on compte les installations par zone (France, région, département, commune) et on fait un graphique par département.
- technologies.py (4.1) : on compte les émetteurs par technologie.
- evolution_technologies.py (4.2) : on regarde combien d'émetteurs ont été mis en service chaque année, de 2017 à 2026.
- carte.py (5) : on place les supports d'antennes sur une carte intéractive.

* ###### **Contraintes :**

Le bon fonctionnement nécessite un arborescence telle quelle :

```
SAE15_C1/
    data/
        sup_station.txt
        sup_support.txt
        sup_antenne.txt
        sup_emetteur.txt
        sup_bande.txt
    ref/
        sup_exploitant.txt
        sup_nature.txt
        sup_propritaire.txt
        sup_type_antenne.txt
    used_data.py
    classement_exploitant.py
    graphique_exploitant.py
    graphe_technologie-exploitant.py
    geographie.py
    technologies.py
    evolution_technologies.py
```

groupe : Mombembo Glory Ethan, Karimi Khalil, Ismaël Sow, Sevgi Dinner, Joan Molle