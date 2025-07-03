# Service de Flux de Prospects - Application de Création de Tournées Commerciales avec Agents IA

## Vue d'ensemble

Le Service de Flux de Prospects est une application web moderne conçue pour créer et optimiser des tournées commerciales intelligentes en utilisant l'intelligence artificielle. L'application intègre plusieurs sources de données pour identifier les meilleurs prospects et optimiser les déplacements commerciaux.

## Fonctionnalités principales

- 🔍 **Recherche d'entreprises françaises** - Intégration avec l'API gouvernementale française
- 🌍 **Géolocalisation avancée** - Intégration Google Places pour la localisation
- 🤖 **Intelligence artificielle** - Services LLM pour l'analyse et la qualification des prospects
- 📊 **Optimisation de tournées** - Algorithmes d'optimisation pour maximiser l'efficacité
- 🎨 **Interface moderne** - Interface utilisateur responsive avec Bootstrap 5

## Technologies utilisées

- **Backend :** Flask (Python)
- **Frontend :** HTML5, CSS3, JavaScript, Bootstrap 5
- **APIs :** Google Places API, API Recherche d'Entreprises (gouvernement français)
- **Templates :** Jinja2
- **Déploiement :** Docker, Gunicorn

## Installation et démarrage

### Prérequis

- Python 3.8+
- pip
- Git

### Installation

1. **Cloner le repository**
```bash
git clone <repository-url>
cd prospects-flow-service
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

ou pour rester isolé de sa machine en utilisant le python du venv (linux, windows ?): 
```sh
./venv/bin/python -m pip install -r requirements.txt
```

4. **Configurer les variables d'environnement**
```bash
# Créer un fichier .env
GOOGLE_PLACE_API_KEY=google-places-api-key (voir avec Amaury)
ENV=production
OLLAMA_URL=http://127.0.0.1:11434/api/generate
FLASK_PORT=5000
FLASK_HOST=0.0.0.0
FLASK_DEBUG=True
```

### Démarrage

```bash
# Port par défaut (5000)
./venv/bin/python run.py

# Port personnalisé
./venv/bin/python run.py --port 5008

Aller sur la racine de l'app `http://localhost:<mon-port>` pour avoir une page d'accueil qui des rédirection vers des docs en page web. Sinon il y a aussi des readme et bientôt swagger pour la précision.

## API Documentation

### Points de terminaison principaux

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Page d'accueil |
| `/health` | GET | Vérification de santé |
| `/gov_places/enterprises/search` | GET | Recherche d'entreprises françaises |
| `/gov_places/enterprises/{siren}` | GET | Détails d'une entreprise par SIREN |
| `/gov_places/enterprises/geographic` | GET | Recherche géographique d'entreprises |
| `/google_places/search` | GET | Recherche de lieux avec Google Places |
| `/llm/health` | GET | Santé du service LLM |

### Documentation complète

Pour une documentation API complète, consultez : [Documentation API](docs/DOCUMENTATION_API.md)

## Structure du projet

Nous organisons avec des blueprints pour rendre le projet évolutif.
- Il pourra se doter d'une base de donnée
- Il peut intégrer facilement de nouveaux service isolés avec leurs propres routes API

A ce stade nous ne sommes pas encore RESTFUL car il nous manque un nombre consistant de demande pour que cela commence à avoir un intérêt. Pour autant nous y travaillons, notamment sur les routes de l'api du gouvernement qui sont nombreuses.
