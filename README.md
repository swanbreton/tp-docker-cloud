# Documentation TP Docker Cloud

## Images personnalisees
- **front**: Nginx Alpine personnalise avec page Web dediee.
- **back**: API Python Flask avec gestion SIGTERM.
- **game-server**: Socket TCP Python sur port 9000 sous utilisateur non-root.

## Orchestration
- Limitations de ressources vCPU et RAM sur tous les conteneurs.
- Healthchecks et dependances de demarrage configurees.