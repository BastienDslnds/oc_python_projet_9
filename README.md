# Développement d'un application web en Django
Programme permettant la gestion de de demandes et recherches de critiques de livres.

## Description

Le projet a pour but de :
* créer/modifier/supprimer des tickets/critiques
* rechercher des tickets/critiques
* s'abonner à des utilisateurs


## Se préparer à commencer

### Dépendances

* installer Windows, version 10.0.19043
* installer Python 3.10

### Installation

* git clone https://github.com/BastienDslnds/oc_python_projet_9.git
* Créer et activer l'environnement virtuel 
  * 1- ouvrir l'application "invite de commande"
  * 2- se positionner dans le dossier "oc_python_projet_9"
  * 3- créer l'environnement virtuel avec: "python -m venv .env"
  * 4- Activer l'environnement virtuel avec: "source .venv/Scripts/activate"
  * 5- utiliser la commande suivante pour installer les packages: "pip install -r requirements.txt"

### Lancer l'application Web

* Se positionner dans le dossier "litreview" avec: "cd litreview"
* Lancer l'application web avec: "python manage.py runserver"
* Ouvrir un navigateur web
* Charger l'url suivant: http://127.0.0.1:8000/home/

### Data

* Identifiants d'un user pour tester:
    * Nom d'utilisateur: Bastien 1
    * Mot de passe: Totooooo1

### Fonctionnement de l'application

* Pour pouvoir utiliser l'application, il faut:
    * se créer un compte
    * se connecter
* La page "feed" permet de:
    * visualiser les tickets et les critiques des utilisateurs que l'on suit
    * créer un ticket et/ou une critique
* La page "posts" permet de:
    * Modifier/supprimer un(e) de ces tickets/critiques

### Vérifier le respect de la PEP8

* Se positionner dans le dossier "litreview"
* Utiliser la commande "flake8 --exclude=review/migrations,users/migrations,config/settings.py"

## Auteurs

Bastien Deslandes

bastien.deslandes@free.fr