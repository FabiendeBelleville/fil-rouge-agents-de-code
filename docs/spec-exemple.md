# Spécification : annuler une session

*Exemple du format attendu pour une spécification exploitable par un agent de code. Courte, concrète, avec ses cas limites et ses tests. C'est la fonctionnalité déjà implémentée dans `service.annuler_session`, pour que vous puissiez comparer la spécification et le code.*

## Contexte

Le formateur annule parfois une session : pas assez d'inscrits, indisponibilité, cas de force majeure. Les inscrits existants doivent rester visibles pour être prévenus, mais personne ne doit plus pouvoir s'inscrire.

## Comportement attendu

- Une session peut être annulée quel que soit son statut (en attente ou confirmée).
- Une session annulée refuse toute nouvelle inscription avec l'erreur `SessionAnnulee`.
- Les inscriptions existantes sont conservées.
- L'annulation est idempotente : annuler deux fois ne change rien.

## Cas limites

- Session inconnue : `SessionInconnue`.
- Désinscription d'une session annulée : autorisée (la personne peut se retirer).

## Contrat HTTP

- `POST /sessions/{id}/annulation` → 200 avec la session ; 404 si inconnue.
- `POST /sessions/{id}/inscriptions` sur une session annulée → 409.

## Tests à écrire

- `test_une_session_annulee_refuse_les_inscriptions`
- `test_annulation_puis_inscription_409`

## Hors périmètre

- Prévenir les inscrits (e-mail) : plus tard.
- Rembourser : dépend de la fonctionnalité « frais d'annulation ».
