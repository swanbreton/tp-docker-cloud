# ==============================================================================
# Image GAME SERVER - serveur de jeu TCP
# Base : Alpine Linux nu, Python installé via apk (aucune dépendance pip :
# le serveur n'utilise que la bibliothèque standard, module socket).
# ==============================================================================
FROM alpine:3.20

LABEL maintainer="swan.breton75@gmail.com" \
      description="Serveur de jeu TCP du Labyrinthe Warhammer"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HOST=0.0.0.0 \
    PORT=9000

# Seule dépendance : l'interpréteur Python 3
RUN apk add --no-cache python3

# Création d'un utilisateur non-root pour respecter le principe du moindre privilège
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

# Copie du script, propriété de l'utilisateur non-root
COPY --chown=appuser:appgroup server.py .

USER appuser

# Port TCP interne (jamais publié sur l'hôte, uniquement sur backend-net)
EXPOSE 9000

# Forme exec : python3 est le PID 1 et reçoit le SIGTERM (géré dans server.py)
ENTRYPOINT ["python3", "server.py"]
