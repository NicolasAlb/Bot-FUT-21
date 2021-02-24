# Bot-FUT-21
Python Bot of buying sell in FIFA 21 FUT

Bot de navigation automatisée pour faire de l'achat-revent sur FIFA 21 FUT.
Techniques aux enchères: 
* Joueurs or commun
* Joueurs or rare
* Un joueur précis (à définir dans le .env)
* Joueurs italiens
* Consommable : MC -> MOC
* Consommable : BU -> AT

### Ce projet est open-source n'hésitez pas à l'améliorer et à créer des pull requests je les regarderais

### Prérequis

* Python 2.7+
* Pip
```
pip install selenium
pip install python-decouple
```

### Lancer le projet

* Copier le .example.env en .env et ajouter ses informations personnelles (EMAIL_EA + PWD_EA)
* Regarder le prix du marché avant de lancer un bot et le mettre à jour dans le .env
* python buy_italian.py (faire pareil pour tous les bots que vous souhaitez lancer)
