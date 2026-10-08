# Image de base Python 3.11 sous Alpine Linux pour le serveur de jeu dédié
FROM python:3.11-alpine

# Définition du répertoire de travail
WORKDIR /app

# Copie du script du serveur de jeu
COPY server.py .

# Exposition du port interne du serveur de jeu
EXPOSE 6000

# Lancement du serveur de jeu
CMD ["python", "server.py"]