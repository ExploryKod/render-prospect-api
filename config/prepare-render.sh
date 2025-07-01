#!/bin/bash

# Script pour préparer le déploiement sur Render.com
# Ce script copie les fichiers de configuration Render à la racine

set -e

echo "🚀 Préparation du déploiement Render.com..."

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "run.py" ]; then
    echo "❌ Erreur: Ce script doit être exécuté depuis la racine du projet prospects-flow-service"
    exit 1
fi

# Sauvegarder les fichiers existants
echo "📦 Sauvegarde des fichiers existants..."
if [ -f "Dockerfile" ]; then
    cp Dockerfile Dockerfile.backup
    echo "✅ Dockerfile sauvegardé"
fi

if [ -f ".dockerignore" ]; then
    cp .dockerignore .dockerignore.backup
    echo "✅ .dockerignore sauvegardé"
fi

# Copier les fichiers de configuration Render
echo "📋 Copie des fichiers de configuration Render..."

if [ -f "config/Dockerfile.render" ]; then
    cp config/Dockerfile.render Dockerfile
    echo "✅ Dockerfile.render copié vers Dockerfile"
else
    echo "❌ Erreur: config/Dockerfile.render non trouvé"
    exit 1
fi

if [ -f "config/.dockerignore.render" ]; then
    cp config/.dockerignore.render .dockerignore
    echo "✅ .dockerignore.render copié vers .dockerignore"
else
    echo "❌ Erreur: config/.dockerignore.render non trouvé"
    exit 1
fi

if [ -f "config/render.yml" ]; then
    cp config/render.yml render.yml
    echo "✅ render.yml copié"
else
    echo "❌ Erreur: config/render.yml non trouvé"
    exit 1
fi

# Vérifier la structure finale
echo "🔍 Vérification de la structure..."
echo "Fichiers présents :"
ls -la Dockerfile .dockerignore render.yml 2>/dev/null || echo "⚠️  Certains fichiers manquent"

echo ""
echo "✅ Préparation terminée !"
echo ""
echo "📝 Prochaines étapes :"
echo "1. Commitez les changements : git add . && git commit -m 'Prepare for Render deployment'"
echo "2. Poussez vers votre repository : git push"
echo "3. Créez un nouveau Web Service sur Render.com"
echo "4. Configurez les variables d'environnement (GOOGLE_PLACE_API_KEY, etc.)"
echo ""
echo "📚 Consultez config/RENDER_DEPLOYMENT.md pour plus de détails" 