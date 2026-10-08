# Image de base Nginx basée sur Alpine pour servir les fichiers statiques du frontend
FROM nginx:alpine

# Copie des fichiers frontend (HTML, CSS, JS) dans le répertoire web par défaut de Nginx
COPY index.html /usr/share/nginx/html/index.html
COPY style.css /usr/share/nginx/html/style.css
COPY main.js /usr/share/nginx/html/main.js

# Exposition du port 80 pour l'accès web
EXPOSE 80

# Démarrage de Nginx en arrière-plan (mode foreground pour Docker)
CMD ["nginx", "-g", "daemon off;"]