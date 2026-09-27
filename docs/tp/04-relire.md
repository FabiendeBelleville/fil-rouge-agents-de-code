# TP 4 — Relire du code généré

*Module 4, environ 1 heure.*

## Objectif

Repérer les défauts typiques d'un code produit par un agent, puis les corriger avec des tests.

## Le matériau

`a-relire/export_emargement.py` a été généré par un agent pour les fonctionnalités 2, 3 et 4 du backlog, en une seule demande, sans spécification et sans tests. Il « marche » sur l'exemple que son auteur a essayé. Il contient au moins huit défauts : logique, robustesse, sécurité, style.

## Étapes

1. **Relisez à la main, d'abord.** Dix minutes, sans agent. Notez chaque défaut avec sa ligne et sa catégorie : bug fonctionnel, cas limite, robustesse, sécurité, maintenabilité.
2. **Demandez ensuite à l'agent une revue** du même fichier. Comparez les deux listes. Qu'a-t-il trouvé que vous aviez manqué ? Qu'avez-vous trouvé qu'il a manqué ? Qu'a-t-il signalé qui n'est pas un défaut ?
3. **Corrigez avec des tests.** Pour chaque défaut fonctionnel, écrivez d'abord le test qui le met en évidence (dans `tests/test_export.py`), puis faites corriger. Le code corrigé rejoint `src/inscriptions/` selon l'organisation décrite dans `AGENTS.md`.
4. **Supprimez** `a-relire/export_emargement.py` une fois le code corrigé intégré.

## Les familles de défauts à connaître

- **Décalages d'indice et bornes** : boucles qui sautent un élément, comparaisons strictes là où il faut une inclusion.
- **Ressources** : fichiers non fermés, encodage absent, chemins concaténés.
- **Formats** : CSV construit à la main sans échappement, dates comparées en chaînes.
- **Erreurs avalées** : `except Exception: pass`.
- **Sécurité** : secrets en dur, `shell=True` avec des données de l'utilisateur, désérialisation.
- **Pièges Python** : argument par défaut mutable, variables globales.
- **Docstrings qui mentent** : « testé », « sûr », « gère tous les cas ».

## Livrable

Votre liste de défauts, la liste de l'agent, et le commit de correction avec ses tests.
