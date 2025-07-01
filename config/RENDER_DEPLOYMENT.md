# Guide de Déploiement Render.com - Prospects Flow Service

## Vue d'ensemble

Ce guide explique comment déployer l'application Flask Prospects Flow Service sur Render.com en utilisant les fichiers de configuration spécialisés dans le dossier `config/`.

## Architecture Render.com

- **Flask** : Framework web principal avec Blueprints
- **Gunicorn** : Serveur WSGI optimisé pour Render
- **Docker** : Conteneurisation avec Dockerfile spécialisé
- **Variables d'environnement** : Configuration via l'interface Render

## Fichiers de Configuration Render

### 1. `config/Dockerfile.render`
Dockerfile optimisé pour Render.com :
- Utilise la variable `PORT` fournie par Render
- Configuration simplifiée sans docker-compose
- Optimisations pour l'environnement Render

### 2. `config/render.yml`
Configuration des variables d'environnement :
- `PORT` : Port d'écoute (géré par Render)
- `FLASK_ENV` : Environnement de production
- `ENV` : Configuration de l'environnement
- `OLLAMA_URL` : URL du service Ollama

### 3. `config/.dockerignore.render`
Fichier d'exclusion optimisé pour Render :
- Exclut les fichiers de développement
- Garde seulement les fichiers nécessaires
- Optimise la taille de l'image

## Déploiement sur Render.com

### Étape 1 : Préparation du Repository

1. **Copier les fichiers de configuration** :
```bash
# Copier le Dockerfile Render à la racine
cp config/Dockerfile.render Dockerfile

# Copier le .dockerignore Render
cp config/.dockerignore.render .dockerignore

# Copier le render.yml
cp config/render.yml render.yml
```

2. **Vérifier la structure** :
```
prospects-flow-service/
├── Dockerfile              # Dockerfile Render
├── render.yml              # Configuration Render
├── .dockerignore           # .dockerignore Render
├── requirements.txt        # Dépendances Python
├── run.py                  # Point d'entrée Flask
├── app/                    # Application Flask
│   ├── __init__.py
│   ├── google_places/
│   └── llm/
└── config/                 # Configurations alternatives
    ├── Dockerfile.render
    ├── render.yml
    └── .dockerignore.render
```

### Étape 2 : Configuration sur Render.com

1. **Créer un nouveau Web Service** :
   - Connectez-vous à [Render.com](https://render.com)
   - Cliquez sur "New +" → "Web Service"
   - Connectez votre repository GitHub/GitLab

2. **Configuration du service** :
   - **Name** : `prospects-flow-service`
   - **Environment** : `Docker`
   - **Region** : Choisissez la région la plus proche
   - **Branch** : `main` (ou votre branche principale)
   - **Root Directory** : `application-web-de-creation-de-tournees-commerciales-avec-agents-ia/prospects-flow-service`

3. **Variables d'environnement** :
   - `GOOGLE_PLACE_API_KEY` : Votre clé API Google Places
   - `ENV` : `production`
   - `OLLAMA_URL` : URL de votre service Ollama (si externe)

### Étape 3 : Déploiement

1. **Déployer** :
   - Cliquez sur "Create Web Service"
   - Render va automatiquement construire et déployer l'application

2. **Vérifier le déploiement** :
   - Surveillez les logs de build
   - Testez l'endpoint de santé : `https://votre-app.onrender.com/health`

## Endpoints Disponibles

- `GET /health` - Healthcheck
- `GET /google_places/*` - API Google Places
- `GET /llm/*` - API LLM/Ollama

## Monitoring et Logs

### Logs Render
- Accédez aux logs via l'interface Render
- Logs en temps réel disponibles
- Historique des déploiements

### Healthcheck
```bash
curl https://votre-app.onrender.com/health
```

## Configuration Avancée

### Variables d'environnement personnalisées
Ajoutez dans `render.yml` :
```yaml
env:
  - key: CUSTOM_VAR
    value: custom_value
```

### Configuration Gunicorn personnalisée
Modifiez dans `Dockerfile.render` :
```dockerfile
CMD gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --timeout 120 run:app
```

## Dépannage

### Erreurs courantes

1. **Build échoue** :
   - Vérifiez les dépendances dans `requirements.txt`
   - Consultez les logs de build Render

2. **Application ne démarre pas** :
   - Vérifiez la variable `PORT` dans `render.yml`
   - Testez localement avec le Dockerfile Render

3. **Variables d'environnement manquantes** :
   - Configurez `GOOGLE_PLACE_API_KEY` dans Render
   - Vérifiez la configuration dans `render.yml`

### Commandes de test local

```bash
# Tester avec le Dockerfile Render
docker build -f config/Dockerfile.render -t prospects-flow-render .
docker run -p 5000:5000 -e PORT=5000 prospects-flow-render

# Tester l'application
curl http://localhost:5000/health
```

## Migration depuis Docker Compose

Si vous migrez depuis une configuration Docker Compose :

1. **Variables d'environnement** :
   - Transférez les variables du `docker-compose.yml` vers Render
   - Utilisez l'interface Render pour les secrets

2. **Services externes** :
   - Ollama doit être hébergé séparément
   - Configurez l'URL dans les variables d'environnement

3. **Volumes** :
   - Render ne supporte pas les volumes persistants
   - Utilisez des services externes pour le stockage

## Coûts et Limites

- **Free Tier** : 750 heures/mois
- **Limitations** : Pas de volumes persistants
- **Scaling** : Manuel ou automatique selon le plan

## Support

- Documentation Render : [docs.render.com](https://docs.render.com)
- Logs et monitoring via l'interface Render
- Support communautaire disponible 