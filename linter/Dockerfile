# ==============================================================================
# Image CI - LINTER (analyse statique du code Python avec flake8)
# Base : Alpine Linux nu. flake8 est installé AU BUILD : au run le conteneur
# est sur le réseau interne (sans Internet) et n'a donc rien à télécharger.
# ==============================================================================
FROM alpine:3.20

LABEL maintainer="swan.breton75@gmail.com" \
      description="Linter flake8 pour le code Python du projet"

ENV PYTHONDONTWRITEBYTECODE=1

# - python3     : interpréteur
# - py3-flake8  : linter PEP8 (pycodestyle + pyflakes)
RUN apk add --no-cache python3 py3-flake8

# Utilisateur non-root : le linter ne fait que lire le code
RUN addgroup -S ci && adduser -S ci -G ci
USER ci

# Le code à analyser est monté en lecture seule sur /code par le compose
WORKDIR /code

# ENTRYPOINT = l'outil (fixe), CMD = ses arguments par défaut (surchargeables
# au run, ex : docker compose run linter --select=E9,F app.py)
# E501 ignoré : game_data.py contient de longues descriptions textuelles
# W503 ignoré : règle obsolète, contradictoire avec W504
ENTRYPOINT ["flake8"]
CMD ["--extend-ignore=E501,W503", "."]
