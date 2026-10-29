# ==============================================================================
# Image BACKEND - API Flask
# Base : Alpine Linux nu (aucune image applicative Docker Hub : Python et Flask
# sont installés à la main via le gestionnaire de paquets apk).
# ==============================================================================
FROM alpine:3.20

# Métadonnées de l'image
LABEL maintainer="swan.breton75@gmail.com" \
      description="Backend Flask du Labyrinthe Warhammer"

# Variables d'environnement Python :
# - PYTHONUNBUFFERED : logs envoyés immédiatement sur stdout (visibles via docker logs)
# - PYTHONDONTWRITEBYTECODE : pas de fichiers .pyc dans l'image
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=5000 \
    DATA_DIR=/app/data \
    LOG_DIR=/app/logs

# Installation des dépendances système (--no-cache : pas d'index apk conservé) :
# - python3          : interpréteur
# - py3-flask        : micro-framework web de l'API
# - py3-flask-cors   : en-têtes CORS pour les appels cross-origin
# - curl             : utilisé par le healthcheck docker compose
RUN apk add --no-cache python3 py3-flask py3-flask-cors curl

# Création d'un utilisateur système non-root (moindre privilège)
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

# Préparation des dossiers des volumes persistants, appartenant à appuser
# (un volume nommé vide hérite des droits du dossier de l'image)
RUN mkdir -p /app/data /app/logs && chown -R appuser:appgroup /app

# Copie du code applicatif
COPY --chown=appuser:appgroup game_data.py app.py ./

USER appuser

# Port HTTP de l'API (documentaire, la publication se fait dans le compose)
EXPOSE 5000

# Forme exec : python3 devient le PID 1 et reçoit directement le SIGTERM
# envoyé par "docker stop" (géré dans app.py par signal.signal)
ENTRYPOINT ["python3", "app.py"]
