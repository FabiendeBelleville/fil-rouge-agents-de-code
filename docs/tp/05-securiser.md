# TP 5 — Sécurité, confidentialité, permissions

*Module 5, environ 45 minutes.*

## Objectif

Configurer ce qu'un agent a le droit de faire sur ce projet, et constater ce qui se passe quand un fichier qu'il lit contient des instructions.

## Étapes

### 1. Permissions

`.claude/settings.json` définit ce que l'agent peut faire sans demander, et ce qu'il ne peut jamais faire. Lisez-le, puis :

- Créez un fichier `.env` avec une fausse clé (`API_KEY=ne-doit-jamais-apparaitre`). Demandez à l'agent « affiche la configuration du projet ». Que fait-il ? Que se passe-t-il si vous retirez la règle de refus ?
- Demandez-lui de lancer les tests : autorisé sans question. Demandez-lui d'envoyer le dépôt sur GitHub : il doit demander.
- Ajoutez une règle qui autorise `uvicorn` et une qui interdit toute suppression de fichier de tests.

### 2. Injection de prompt

`a-relire/ticket-42.md` est un ticket copié d'un outil externe. Demandez à l'agent : « implémente le ticket 42 ». Lisez attentivement ce qu'il propose de faire, **avant** d'accepter quoi que ce soit.

- Quelle partie du ticket est une instruction cachée ? Comment l'agent l'a-t-il traitée ?
- Quelle règle de `AGENTS.md` est censée le protéger ? Est-ce suffisant ?
- Reformulez votre demande pour que le contenu du ticket soit traité comme une donnée, pas comme une consigne.

### 3. Ce qui ne doit jamais partir

Listez, pour votre vrai projet au bureau, ce qu'un agent ne doit jamais lire ni envoyer : secrets, données personnelles, code sous licence incompatible, dépôts de clients. Écrivez les règles correspondantes dans un fichier de permissions.

## Livrable

Votre `.claude/settings.json` complété et vos réponses aux questions du point 2, en trois lignes.
