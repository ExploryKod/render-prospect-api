#!/bin/bash

# Script de démarrage pour l'application Flask en production

set -e

echo "🚀 Démarrage de Prospects Flow Service..."

# Vérifier que les variables d'environnement nécessaires sont définies
if [ -z "$GOOGLE_PLACE_API_KEY" ]; then
    echo "⚠️  Attention: GOOGLE_PLACE_API_KEY n'est pas définie"
fi

# Créer le répertoire de logs s'il n'existe pas
mkdir -p logs

# Démarrer l'application avec Gunicorn
echo "📦 Démarrage de Gunicorn..."
exec gunicorn --config gunicorn.conf.py run:app 