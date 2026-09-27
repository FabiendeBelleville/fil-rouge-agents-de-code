# TP 3 — Développer avec un agent : la boucle plan, tests, code, revue

*Module 3, environ 2 heures.*

## Objectif

Faire implémenter par l'agent la liste d'attente spécifiée au TP 2, en gardant la main à chaque étape.

## La boucle

1. **Plan.** Demandez à l'agent un plan d'implémentation à partir de `docs/specs/liste-attente.md` et de `AGENTS.md` : fichiers touchés, nouvelles erreurs, routes, tests. Ne le laissez pas coder avant d'avoir validé le plan. Corrigez ce qui ne respecte pas l'organisation du code.
2. **Tests d'abord.** Faites-lui écrire les tests de `tests/test_service.py` listés dans la spécification. Lancez `python -m pytest` : ils doivent échouer, pour la bonne raison.
3. **Implémentation.** Laissez-le implémenter dans `service.py`, `repository.py` et `models.py`. Puis les routes dans `api.py` et leurs tests dans `tests/test_api.py`.
4. **Revue.** Lisez le diff en entier, comme si un collègue l'avait écrit. Vérifiez au moins : la règle « une personne en attente ne compte pas dans le seuil », le passage automatique d'attente à inscrit quand une place se libère, et l'absence de logique métier dans `api.py`.
5. **Finition.** `ruff check .` propre, tests verts, un commit avec un message à l'impératif.

## Variante, si vous êtes en avance

Faites implémenter la fonctionnalité 2 du backlog (frais d'annulation) **sans écrire de spécification**, en une seule demande. Comparez le nombre d'allers-retours et la qualité du résultat avec la liste d'attente. C'est la démonstration la plus convaincante du module 2.

## Livrable

Le commit de la liste d'attente, tests compris. Notez, pour le bilan de fin de journée, combien de fois vous avez dû corriger l'agent et sur quoi.
