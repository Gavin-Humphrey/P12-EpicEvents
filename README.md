Gavin-Humphrey/P12-EpicEvents

Projet réalisé dans le cadre de ma formation OpenClassrooms Développeur d'Applications Python Projet-12.
Il s'agit d'une API réalisée avec Django pour une société fictive d'évenementiel, EpicEvents.
L'application permet de gérer des clients, contrats et événements via une API REST et une interface d'administration.

Features:

Tout les endpoints, leurs détails, et recherche filtrée avec Postman

Installation & lancement:

    Commencez tout d'abord par installer Python.
    Lancez ensuite la console, placez vous dans le dossier de votre choix puis clonez ce repository:

    git clone https://github.com/Gavin-Humphrey/P12-EpicEvents.git

        MacOS ou Linux:

            cd EpicEvents
            python3 -m venv env
            source env/bin/activate
            pip install -r requirements.txt

        Windows:

            cd EpicEvents
            python -m venv env
            env\Scripts\activate
            pip install -r requirements.txt

        
        Créer une base de données PostgreSQL:

            Installez PostgreSQL via https://www.postgresql.org/download/. 

            Créez une nouvelle base de données PostgreSQL avec SQL shell (psql) : CREATE DATABASE your_db_name;

            Variables d'environnement : fichier .env

            Pour générer un fichier .env, exécutez python create_dot_env.py et saisissez les informations requises.


    Ensuite, placez vous à la racine du projet (là ou se trouve le fichier manage.py), puis effectuez les migrations:

        python manage.py makemigrations

        Puis:

        python manage.py migrate

        Create Superuser :

            python manage.py createsuperuser

        Et enfin, lancer le serveur:

            python manage.py runserver

La page d'administration sera accessible à l'adresse http://127.0.0.1:8000/admin. Vous pouvez ensuite vous connecter avec l'e-mail et le mot de passe du superuser précédemment créés. Il est maintenant possible de remplir la base de données, avec quelques membres de l'équipe de MANAGEMENT, SALES, ou de SUPPORT avec des rôles assignés.
