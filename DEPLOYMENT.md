# Guide de Déploiement - Prospects Flow Service

## Vue d'ensemble

Cette application Flask utilise des Blueprints pour organiser le code et est configurée pour fonctionner en production avec Docker et Gunicorn.

## Architecture

- **Flask** : Framework web principal
- **Blueprints** : Organisation modulaire du code (`google_places`, `llm`)
- **Gunicorn** : Serveur WSGI pour la production
- **Docker** : Conteneurisation
- **Docker Compose** : Orchestration des services

## Prérequis

- Docker et Docker Compose installés
- Variable d'environnement `GOOGLE_PLACE_API_KEY` configurée

## Déploiement

### 1. Configuration des variables d'environnement

Créez un fichier `.env` à la racine du projet :

```bash
GOOGLE_PLACE_API_KEY=votre_clé_api_google
ENV=production
OLLAMA_URL=http://127.0.0.1:11434/api/generate
```

### 2. Construction et démarrage

```bash
# Construire l'image
docker-compose build

# Démarrer les services
docker-compose up -d

# Voir les logs
docker-compose logs -f prospects-flow-service
```

### 3. Démarrage avec Ollama (optionnel)

Si vous voulez inclure Ollama dans le même compose :

```bash
docker-compose --profile ollama up -d
```

## Structure des Blueprints

```
app/
├── __init__.py          # Factory pattern pour Flask
├── google_places/       # Blueprint Google Places API
│   ├── __init__.py
│   └── routes.py
└── llm/                 # Blueprint LLM/Ollama
    ├── __init__.py
    └── routes.py
```

## Endpoints disponibles

- `GET /health` - Healthcheck pour Docker
- `GET /google_places/*` - Endpoints Google Places API
- `GET /llm/*` - Endpoints LLM/Ollama

## Configuration Gunicorn

Le fichier `gunicorn.conf.py` configure :
- Nombre de workers basé sur les CPU
- Timeouts et limites de requêtes
- Logging et sécurité
- Performance optimisée

## Monitoring

### Healthcheck
L'application expose un endpoint `/health` pour vérifier l'état du service.

### Logs
Les logs sont disponibles via :
```bash
docker-compose logs prospects-flow-service
```

## Sécurité

- Utilisateur non-root dans le conteneur
- Variables d'environnement pour les secrets
- Configuration Gunicorn sécurisée
- Headers de sécurité configurés

## Performance

- Workers Gunicorn optimisés
- Préchargement de l'application
- Configuration des timeouts
- Gestion des connexions

## Dépannage

### Vérifier l'état du service
```bash
curl http://localhost:5000/health
```

### Voir les logs en temps réel
```bash
docker-compose logs -f prospects-flow-service
```

### Redémarrer le service
```bash
docker-compose restart prospects-flow-service
```

## Variables d'environnement

| Variable | Description | Obligatoire |
|----------|-------------|-------------|
| `GOOGLE_PLACE_API_KEY` | Clé API Google Places | Oui |
| `ENV` | Environnement (dev/prod) | Non |
| `OLLAMA_URL` | URL du service Ollama | Non |

## Ports

- **5000** : Application Flask
- **11434** : Ollama (si activé) 