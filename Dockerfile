FROM python:3.11-slim

# Définir les variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=run.py \
    FLASK_ENV=production

# Créer et définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn

# Copier le code source de l'application
COPY . .

# Créer un utilisateur non-root pour la sécurité
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app
USER appuser

# Exposer le port
EXPOSE 5000

# Rendre le script de démarrage exécutable
RUN chmod +x start.sh

# Commande de démarrage
CMD ["./start.sh"]

# Labels pour GitLab
LABEL maintainer="prospects-flow-team"
LABEL version="1.0"
LABEL description="Prospects Flow Service - API pour la gestion des prospects et tournées commerciales"
LABEL org.opencontainers.image.source="https://gitlab.com/votre-groupe/prospects-flow-service"
