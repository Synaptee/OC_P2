## Programme de scraping du site Web https://books.toscrape.com

Ce programme est conçu pour extraire des éléments spécifiques du site Web https://books.toscrape.com.

# Fonctionnalités

* Récupère les éléments ci-après pour tous les livres de toutes les catégories du site : [Code UPC, Titre, Prix HT, Prix TTC, Qté en stock, Catégorie, Synopsis, Note et image de couverture]
* Stockage des résultats dans des dossiers par catégories, avec une fichier .csv contenant les données, et les images. 


# Pré-requis

* Python 3.x
* Modules recensés dans le fichiere requirements.txt

# Création de votre environnement virtuel

Nous vous conseillons de créer un environnement virtuel afin d'y installer les dépendances nécessaires et exécuter votre code. 
Pour créer un environnement virtuel (nommé venv par convention), vous pouvez utiliser la commande : `python3 -m venv .venv`.

Pensez bien à activer vote environnement virtuel avec la commande : `. .venv/bin/activate`

# Installation

1. Cloner le projet sur votre ordinateur : `git clone https://github.com/Synaptee/OC_P2.git`
2. Installer les dépendances en utilisant pip : `pip install -r requirements.txt`

# Utilisation

1. Lancez le programme en utilisant la commande `python main.py`.
2. Laissez le programme s'exécuter
3. Un message s'affichera dans la console lorsque le programme sera terminé.
4. Vous pouvez désactiver votre environnement virtuel avec la commande : `deactivate`

# Avertissement

Veuillez utiliser ce programme de manière responsable et respecter les politiques de robots et de scraping des sites web que vous visitez. L'utilisation abusive de ce programme peut entraîner des conséquences juridiques. Le développeur de ce programme ne peut être tenu responsable de toute utilisation abusive ou illégale de ce programme.
