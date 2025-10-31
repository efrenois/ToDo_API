# Gestionnaire de tâches API REST avec Flask
 
 Ce petit projet implémente une API REST pour gérer une liste de tâches (to-do list) en utilisant Flask, SQLAlchemy et JWT pour l'authentification.
 
 ## Fonctionnalités
 
 - Créer, lire, mettre à jour et supprimer des tâches.
 - Authentification des utilisateurs avec JWT.
 - Interface graphique simple pour interagir avec l'API.
 
 ## Installation
 
 1. Cloner le dépôt :
 
    ```bash
    git clone

2. Créer un environnement virtuel (optionnel mais recommandé) :
 
    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur Windows utilisez `venv\Scripts\activate`
    ```
3. Installer les dépendances :
 
    ```bash
    pip install -r requirements.txt
    ```
 ## Utilisation
 
 1. Lancer l'application Flask :
 
    ```bash
    python app.py
    ```
 
 2. Accéder à l'interface graphique via l'url : `http://http://127.0.0.1:5000`