"""Règles métier. Un test par règle, nommé comme la règle."""

import itertools
from datetime import date

import pytest

from inscriptions.models import StatutSession
from inscriptions.repository import Depot
from inscriptions.service import (
    DejaInscrit,
    InscriptionInconnue,
    ServiceInscriptions,
    SessionAnnulee,
    SessionComplete,
    SessionInconnue,
)

DEBUT = date(2026, 11, 16)
_compteur = itertools.count()


@pytest.fixture
def service() -> ServiceInscriptions:
    return ServiceInscriptions(Depot())


def inscrire_n(service: ServiceInscriptions, session_id: int, n: int) -> None:
    """Inscrit n personnes distinctes, avec des adresses uniques d'un appel à l'autre."""
    for _ in range(n):
        k = next(_compteur)
        service.inscrire(session_id, f"Personne {k}", f"p{k}@exemple.fr", "Exemple SAS")


def test_une_session_nouvelle_est_en_attente(service):
    session = service.creer_session("Développer avec l'IA générative", DEBUT, 2)
    assert session.statut is StatutSession.EN_ATTENTE
    assert service.places_restantes(session.id) == 8


def test_la_session_est_confirmee_quand_le_seuil_est_atteint(service):
    session = service.creer_session("Formation", DEBUT, 2, capacite=8, seuil_confirmation=4)
    inscrire_n(service, session.id, 3)
    assert session.statut is StatutSession.EN_ATTENTE
    inscrire_n(service, session.id, 1)
    assert session.statut is StatutSession.CONFIRMEE


def test_une_session_complete_refuse_les_inscriptions(service):
    session = service.creer_session("Formation", DEBUT, 1, capacite=2, seuil_confirmation=1)
    inscrire_n(service, session.id, 2)
    with pytest.raises(SessionComplete):
        service.inscrire(session.id, "Trop Tard", "tard@exemple.fr", "")
    assert service.places_restantes(session.id) == 0


def test_une_adresse_ne_s_inscrit_qu_une_fois_par_session(service):
    session = service.creer_session("Formation", DEBUT, 1)
    service.inscrire(session.id, "Ana", "Ana@Exemple.fr", "")
    with pytest.raises(DejaInscrit):
        service.inscrire(session.id, "Ana bis", " ana@exemple.fr ", "")


def test_la_meme_adresse_peut_s_inscrire_a_deux_sessions(service):
    s1 = service.creer_session("Formation A", DEBUT, 1)
    s2 = service.creer_session("Formation B", DEBUT, 1)
    service.inscrire(s1.id, "Ana", "ana@exemple.fr", "")
    service.inscrire(s2.id, "Ana", "ana@exemple.fr", "")
    assert len(service.inscrits(s2.id)) == 1


def test_une_session_annulee_refuse_les_inscriptions(service):
    session = service.creer_session("Formation", DEBUT, 1)
    service.annuler_session(session.id)
    with pytest.raises(SessionAnnulee):
        service.inscrire(session.id, "Ana", "ana@exemple.fr", "")


def test_une_session_confirmee_le_reste_apres_une_desinscription(service):
    session = service.creer_session("Formation", DEBUT, 1, capacite=8, seuil_confirmation=2)
    inscrire_n(service, session.id, 2)
    assert session.statut is StatutSession.CONFIRMEE
    premiere = service.inscrits(session.id)[0]
    service.desinscrire(premiere.id)
    assert session.statut is StatutSession.CONFIRMEE
    assert len(service.inscrits(session.id)) == 1


def test_la_desinscription_libere_une_place(service):
    session = service.creer_session("Formation", DEBUT, 1, capacite=1, seuil_confirmation=1)
    inscription = service.inscrire(session.id, "Ana", "ana@exemple.fr", "")
    service.desinscrire(inscription.id)
    assert service.places_restantes(session.id) == 1
    service.inscrire(session.id, "Bob", "bob@exemple.fr", "")


def test_les_champs_sont_nettoyes(service):
    session = service.creer_session("  Formation  ", DEBUT, 1)
    inscription = service.inscrire(session.id, "  Ana ", " ANA@Exemple.fr ", " Exemple ")
    assert session.formation == "Formation"
    assert (inscription.nom, inscription.email, inscription.entreprise) == (
        "Ana",
        "ana@exemple.fr",
        "Exemple",
    )


@pytest.mark.parametrize(
    ("capacite", "seuil"),
    [(0, 1), (8, 0), (8, 9)],
)
def test_les_parametres_incoherents_sont_refuses(service, capacite, seuil):
    with pytest.raises(ValueError):
        service.creer_session("Formation", DEBUT, 1, capacite=capacite, seuil_confirmation=seuil)


def test_une_duree_nulle_est_refusee(service):
    with pytest.raises(ValueError):
        service.creer_session("Formation", DEBUT, 0)


def test_session_inconnue(service):
    with pytest.raises(SessionInconnue):
        service.inscrire(42, "Ana", "ana@exemple.fr", "")


def test_inscription_inconnue(service):
    with pytest.raises(InscriptionInconnue):
        service.desinscrire(42)
