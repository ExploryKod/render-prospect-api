#!/bin/bash

# Script pour restaurer la configuration Docker Compose
# Ce script restaure les fichiers de sauvegarde après le déploiement Render

set -e

echo "🔄 Restauration de la configuration Docker Compose..."

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "run.py" ]; then
    echo "❌ Erreur: Ce script doit être exécuté depuis la racine du projet prospects-flow-service"
    exit 1
fi

# Restaurer les fichiers de sauvegarde
echo "📦 Restauration des fichiers de sauvegarde..."

if [ -f "Dockerfile.backup" ]; then
    mv Dockerfile.backup Dockerfile
    echo "✅ Dockerfile restauré"
else
    echo "⚠️  Aucune sauvegarde Dockerfile trouvée"
fi

if [ -f ".dockerignore.backup" ]; then
    mv .dockerignore.backup .dockerignore
    echo "✅ .dockerignore restauré"
else
    echo "⚠️  Aucune sauvegarde .dockerignore trouvée"
fi

# Supprimer les fichiers Render
echo "🗑️  Suppression des fichiers Render..."
if [ -f "render.yml" ]; then
    rm render.yml
    echo "✅ render.yml supprimé"
fi

# Vérifier la structure finale
echo "🔍 Vérification de la structure..."
echo "Fichiers présents :"
ls -la Dockerfile .dockerignore docker-compose.yml 2>/dev/null || echo "⚠️  Certains fichiers manquent"

echo ""
echo "✅ Restauration terminée !"
echo ""
echo "📝 Vous pouvez maintenant utiliser Docker Compose :"
echo "docker-compose up -d"
echo ""
echo "📚 Consultez DEPLOYMENT.md pour plus de détails" 