# Backlog

Les fonctionnalités à venir, dans l'ordre où le métier les demande. Certaines sont décrites en une phrase, exprès : écrire la spécification est le travail du module 2. D'autres sont plus précises, pour le module 3.

## 1. Liste d'attente

Quand une session est complète, une personne doit pouvoir se mettre en liste d'attente. Quand une place se libère, la première personne en attente devient inscrite. Une personne en attente ne compte pas dans le seuil de confirmation.

*À spécifier au module 2 : que se passe-t-il si la session est annulée ? Une adresse déjà inscrite peut-elle être en attente ? Quelles routes HTTP ?*

## 2. Frais d'annulation

Une désinscription entraîne des frais selon le délai avant le début de la session : aucun frais jusqu'à 15 jours calendaires avant le début, 50 % du prix entre 15 et 7 jours, 100 % à moins de 7 jours. Le prix est un attribut de la session (entier, en euros HT).

*Précis : les bornes sont inclusives côté « moins cher » (15 jours exactement = gratuit, 7 jours exactement = 50 %).*

## 3. Feuille d'émargement

Exporter, pour une session, la feuille d'émargement au format CSV : une ligne par inscrit (nom, e-mail, entreprise), une colonne de signature par demi-journée. Le nombre de demi-journées découle de la durée de la session.

## 4. Rappels

Lister les inscrits à relancer à une date donnée : ceux dont la session commence dans 7 jours ou moins et n'a pas encore commencé, sans doublon.

## 5. Persistance

Remplacer le dépôt en mémoire par SQLite, sans changer le service ni les tests du service.
