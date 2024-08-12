      Rapport d'utilisation de l'application Flask avec MongoDB
      1. Introduction
Ce document présente une vue d'ensemble du fonctionnement d'une application web développée avec Flask, utilisant MongoDB comme base de données via MongoEngine.
L'application permet de gérer une collection de livres, offrant des fonctionnalités pour insérer, récupérer, mettre à jour et supprimer des livres via une API REST.

    2. Structure du Code
Le code est structuré autour des éléments principaux suivants :

Application Flask : L'application est créée à l'aide de Flask, un microframework Python.
MongoDB : La base de données MongoDB est utilisée pour stocker les informations sur les livres. MongoEngine est employé comme ORM (Object-Relational Mapping) pour interagir avec MongoDB.
Journalisation : Une configuration de journalisation est mise en place pour enregistrer les événements importants, comme les erreurs et les opérations de base de données.

    3. Fonctionnalités
    3.1 Configuration de la Base de Données
La base de données MongoDB est configurée via les paramètres suivants :

Nom de la base de données : APLI
URI de connexion : mongodb://localhost:27017/APLI
La configuration de MongoDB est effectuée dans la section app.config["MONGODB_SETTINGS"] du code.

    3.2 Modèle de Données
Un modèle Book est défini pour représenter les livres dans MongoDB. Ce modèle contient les champs suivants :

book_id : Un identifiant unique pour chaque livre (entier, requis).
nom : Le nom du livre (chaîne de caractères, requis).
auteur : L'auteur du livre (chaîne de caractères, requis).
Le modèle inclut une méthode convert_to_json() pour convertir les objets Book en dictionnaires JSON, facilitant ainsi leur manipulation et leur retour dans les réponses HTTP.

      3.3 Routes HTTP
L'application expose plusieurs routes pour interagir avec les livres.

      3.3.1 Route /APLI/db_Insertion
Méthode : POST
Description : Cette route permet de peupler la base de données avec un ensemble initial de livres. Elle insère quatre livres prédéfinis dans MongoDB et enregistre ces opérations dans les logs.

      3.3.2 Route /APLI/books
Méthodes : GET, POST
GET : Récupère tous les livres stockés dans la base de données et les retourne sous forme de JSON.
POST : Ajoute un nouveau livre dans la base de données. Si un livre avec le même book_id existe déjà, une erreur est renvoyée.

    3.3.3 Route /APLI/books/<int:book_id>
Méthodes : GET, PUT, DELETE
GET : Récupère les informations d'un livre spécifique identifié par book_id. Si le livre n'existe pas, une erreur est renvoyée.
PUT : Met à jour les informations d'un livre existant (nom et auteur) basé sur son book_id.
DELETE : Supprime un livre spécifique de la base de données. Si le livre n'est pas trouvé, une erreur est renvoyée.

    4. Détails Techniques
    4.1 Environnement de Base de Données
Base de Données : MongoDB
ORM : MongoEngine
    
    4.2 Gestion des Requêtes
Les requêtes HTTP sont gérées de manière à garantir que les opérations CRUD (Create, Read, Update, Delete) sur les livres sont réalisées en toute sécurité. Les réponses sont renvoyées au format JSON pour assurer une compatibilité maximale avec les clients web.

    4.3 Journalisation
La journalisation est configurée pour capturer des événements clés, y compris les erreurs et les succès d'opérations, ce qui aide à la surveillance et au débogage de l'application.

    5. Lancement de l'Application
Pour lancer l'application, suivez ces étapes :

1- installer mongodb
2-Installer les dépendances Python requises avec "pip install flask flask_mongoengine".
3- configurer le chemin d’accès: variable Path.
4- saisir “mongod” en ligne de commande pour lancer l'exécution de shell mongodb
5- Installer les dépendances Python requises avec pip install flask flask_mongoengine.
6- Exécutez le script Python avec la commande python apli_mongo.py.
7- pour Insérer les données dans la base de données Mongodb:
  ->  Executer la commande : curl -X POST http://127.0.0.1:5001/APLI/db_Insertion pour insérer la donnees (books) dans la base mongodb
  ->  Suivre les routes pour la vérification.

L'application sera accessible sur le port 5001 et sera en mode débogage pour faciliter le développement.
