# ==============================================================================
# Image FRONTEND - Nginx (fichiers statiques + reverse proxy /api)
# Base : Alpine Linux nu, Nginx installé via apk (pas d'image nginx Docker Hub).
# ==============================================================================
FROM alpine:3.20

LABEL maintainer="swan.breton75@gmail.com" \
      description="Frontend Nginx du Labyrinthe Warhammer"

# Installation du serveur web Nginx (crée aussi l'utilisateur système "nginx"
# utilisé par les processus workers)
RUN apk add --no-cache nginx

# Opérations sur l'OS :
# - suppression du site par défaut d'Alpine (remplacé par notre configuration)
# - création du dossier du fichier PID et du dossier web
RUN rm -f /etc/nginx/http.d/default.conf \
    && mkdir -p /run/nginx /usr/share/nginx/html

# Configuration personnalisée : site statique + reverse proxy vers le backend
# (Alpine charge automatiquement /etc/nginx/http.d/*.conf)
COPY nginx.conf /etc/nginx/http.d/default.conf

# Copie des fichiers frontend (HTML, CSS, JS)
COPY index.html style.css main.js tree.html tree.js /usr/share/nginx/html/

# Port HTTP (documentaire, publié sur l'hôte via le compose)
EXPOSE 80

# Nginx traite SIGTERM comme un arrêt brutal. SIGQUIT déclenche un arrêt propre
# (graceful shutdown : fin des requêtes en cours), c'est donc ce signal que
# "docker stop" enverra.
STOPSIGNAL SIGQUIT

# Forme exec + "daemon off" : nginx reste au premier plan en PID 1,
# sinon le conteneur s'arrêterait immédiatement
ENTRYPOINT ["nginx", "-g", "daemon off;"]
