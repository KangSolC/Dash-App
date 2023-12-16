# Projet d'Analyse de Données - Master TIW 2023-2024

## Étudiantes

- AMAKHZOUN Hajar
- EL GARB Mouna
- NGUYEN Cécilia

## Jeu de données

- [Fichier source pris sur Kaggle](https://www.kaggle.com/datasets/alitaqi000/world-university-rankings-2023)
- Le jeu de données du fichier source vient lui-même de *Times Higher Education* : [Lien du classement officiel](https://www.timeshighereducation.com/world-university-rankings/2023/world-ranking)

Le jeu de données pris sur Kaggle a ensuite été de nouveau modifié pour ne garder que les 200 premières universités et rajouter les pays manquants dans la colonne *Location*. Nous avons réduit le nombre d'universités dans les données, car à partir de la 200ème, le rang n'était plus unique et était sous la forme : 201-250, 251-300, etc.

## Exécution du projet

- Installer les packages nécessaires
```bash
pip install -r requirements.txt
```
- Lancer le projet
```bash
python3 app.py
```
