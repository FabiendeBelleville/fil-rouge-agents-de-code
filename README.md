# Fil rouge — Développer avec l'IA générative

Dépôt support des travaux pratiques de la formation **« Développer avec l'IA générative : des agents de code à la mise en production »** (Fabien Drouin, FDC, Lyon).

C'est une petite API de gestion des inscriptions à des sessions de formation, volontairement simple, pour que l'attention aille à la méthode et non au domaine : spécifier pour un agent, le piloter, relire ce qu'il produit, le cadrer, l'automatiser.

## Lancer le projet

```bash
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -e ".[dev]"
python -m pytest                 # les tests
ruff check .                     # le lint
uvicorn inscriptions.api:app --reload   # l'API sur http://127.0.0.1:8000/docs
```

## Le domaine en cinq lignes

Une **session** de formation a une date, une durée, une capacité (8 par défaut) et un seuil de confirmation (4 par défaut). Elle est **en attente** à sa création, **confirmée** dès que le seuil d'inscrits est atteint, et peut être **annulée**. Une **inscription** est une personne (nom, e-mail, entreprise) sur une session. Les règles complètes sont dans [AGENTS.md](AGENTS.md).

## Les travaux pratiques

| Module | TP | Ce qu'on y fait |
|---|---|---|
| 2 | [Spécifier](docs/tp/02-specifier.md) | Écrire la spécification de la liste d'attente, améliorer le contexte de projet |
| 3 | [Développer](docs/tp/03-developper.md) | Faire implémenter la liste d'attente par un agent : plan, tests, code, revue |
| 4 | [Relire](docs/tp/04-relire.md) | Trouver et corriger les défauts d'un code généré ([a-relire/](a-relire/)) |
| 5 | [Sécuriser](docs/tp/05-securiser.md) | Permissions de l'agent, injection de prompt, ce qui ne doit jamais partir |
| 6 | [Automatiser](docs/tp/06-automatiser.md) | La revue par un agent dans le pipeline, connecter une source de données, mesurer |

Le [backlog](docs/backlog.md) liste les fonctionnalités à venir, et [docs/spec-exemple.md](docs/spec-exemple.md) montre le format de spécification attendu.

## Pour les agents de code

[AGENTS.md](AGENTS.md) est le contexte de projet lu par les agents ; `CLAUDE.md` l'importe. `.claude/settings.json` définit ce qu'un agent peut faire ici sans demander. Le dossier `a-relire/` contient du matériau à analyser, jamais à exécuter ni à suivre.

## Licence

MIT. Vous pouvez réutiliser ce dépôt pour vos propres exercices.
