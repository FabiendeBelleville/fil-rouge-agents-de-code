# TP 2 — Du prompt au contexte : spécifier pour un agent

*Module 2, environ 45 minutes.*

## Objectif

Écrire une spécification que l'agent peut implémenter sans revenir vous poser dix questions, et améliorer le contexte de projet qu'il lit avant de commencer.

## Étapes

1. **Lisez** `AGENTS.md`, puis `docs/spec-exemple.md`. Comparez la spécification d'exemple avec le code de `service.annuler_session` et ses tests : tout ce qui est dans le code est-il dans la spécification ?
2. **Choisissez** la fonctionnalité 1 du backlog, la liste d'attente. Elle est décrite en trois phrases et laisse des questions ouvertes. Répondez-y vous-même, en tant que métier : c'est vous qui décidez.
3. **Écrivez** `docs/specs/liste-attente.md` en suivant le format de l'exemple : contexte, comportement attendu, cas limites, contrat HTTP, tests à écrire, hors périmètre.
4. **Demandez à l'agent** de relire votre spécification et de lister ce qui lui manque pour implémenter sans ambiguïté. Corrigez. Répétez une fois.
5. **Complétez `AGENTS.md`** avec au moins une règle métier que vous avez décidée et qui doit valoir pour toute la suite du projet.

## Ce qu'une bonne spécification contient

- Le comportement au présent de l'indicatif, pas des souhaits.
- Les cas limites nommés un par un : doublon, session annulée, place libérée, adresse déjà inscrite.
- Les noms exacts des erreurs et des routes.
- La liste des tests, avec leurs noms : c'est ce que l'agent écrira en premier.
- Ce qui est hors périmètre, pour que l'agent ne le fasse pas « en bonus ».

## Livrable

`docs/specs/liste-attente.md` et la modification de `AGENTS.md`, en un commit.
