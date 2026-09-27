# TP 6 — Étendre et automatiser : la revue de code dans le pipeline

*Module 6, environ 1 h 15.*

## Objectif

Faire relire chaque pull request par un agent, selon les règles de `AGENTS.md`, et mesurer ce que ça apporte.

## Étapes

1. **Le pipeline existant.** `.github/workflows/ci.yml` lance `ruff` et `pytest` à chaque push. Poussez une branche avec une modification volontairement fausse (un test qui échoue) et regardez le résultat sur GitHub.
2. **La revue par un agent.** Le même fichier contient, en commentaire, un second job `revue-ia`. Activez-le : il faut une clé d'API dans les secrets du dépôt (le formateur en fournit une pour la session). Le prompt de revue est à écrire : il doit renvoyer l'agent vers `AGENTS.md` et lui demander de ne signaler que ce qui est faux, risqué ou contraire aux règles, avec le fichier et la ligne.
3. **Testez la revue** sur la pull request du TP 4 (le code corrigé) puis sur une pull request qui viole une règle métier de `AGENTS.md`, par exemple une inscription en double autorisée. La revue le voit-elle ?
4. **Connectez l'agent à une source de données.** Donnez-lui accès en lecture à un outil de votre choix (un fichier de tickets, une base SQLite, une API publique) et demandez-lui de croiser cette source avec le code : par exemple, « quels tickets du fichier sont déjà implémentés ? ».
5. **Mesurez.** Pour la liste d'attente (TP 3), estimez le temps que vous auriez mis sans agent. Comparez avec le temps réel, corrections comprises. Notez ce qui a pris plus de temps que prévu : c'est presque toujours la spécification et la relecture, jamais la frappe.

## Ce qu'il faut retenir

- Une revue automatique ne remplace pas la vôtre : elle la rend plus rapide et plus régulière.
- Le prompt de revue est du code : versionné, relu, amélioré à chaque faux positif.
- Le gain se mesure sur un mois, pas sur une démo.

## Livrable

Le job `revue-ia` actif, une pull request relue par l'agent, et vos trois chiffres : temps estimé, temps réel, nombre de corrections.
