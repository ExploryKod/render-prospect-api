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

4. **Configurer les variables d'environnement**
```bash
# Créer un fichier .env
FLASK_PORT=5000
FLASK_HOST=0.0.0.0
FLASK_DEBUG=True
```

### Démarrage

```bash
# Port par défaut (5000)
./venv/bin/python run.py

# Port personnalisé
./venv/bin/python run.py --port 8080

# Avec variables d'environnement
FLASK_PORT=9000 ./venv/bin/python run.py
```

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

### Exemples d'utilisation

#### Recherche d'entreprises
```bash
# Recherche de restaurants à Paris
curl "http://localhost:5000/gov_places/enterprises/search?q=restaurant&code_postal=75001&effectif_min=10"

# Recherche d'entreprises technologiques
curl "http://localhost:5000/gov_places/enterprises/search?q=informatique&code_naf=62.01Z"
```

#### Recherche géographique
```bash
# Recherche autour de la Tour Eiffel
curl "http://localhost:5000/gov_places/enterprises/geographic?lat=48.8584&lon=2.2945&radius=2000"
```

#### Détails d'entreprise
```bash
# Obtenir les détails d'Orange
curl "http://localhost:5000/gov_places/enterprises/380129867"
```

### Documentation complète

Pour une documentation API complète, consultez : [Documentation API](docs/DOCUMENTATION_API.md)

## Structure du projet
