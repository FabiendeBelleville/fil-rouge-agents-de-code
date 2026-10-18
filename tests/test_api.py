"""Contrat HTTP : codes de retour et forme des réponses. Les règles métier sont testées ailleurs."""

import pytest
from fastapi.testclient import TestClient

from inscriptions.api import creer_application

SESSION = {
    "formation": "Développer avec l'IA générative",
    "date_debut": "2026-11-16",
    "duree_jours": 2,
}


@pytest.fixture
def client() -> TestClient:
    return TestClient(creer_application())


def creer_session(client: TestClient, **surcharges) -> dict:
    reponse = client.post("/sessions", json={**SESSION, **surcharges})
    assert reponse.status_code == 201, reponse.text
    return reponse.json()


def test_creer_puis_lire_une_session(client):
    session = creer_session(client)
    assert session["statut"] == "en_attente"
    assert session["places_restantes"] == 8
    lue = client.get(f"/sessions/{session['id']}")
    assert lue.status_code == 200
    assert lue.json() == session
    assert client.get("/sessions").json() == [session]


def test_les_inscriptions_confirment_la_session(client):
    session = creer_session(client, seuil_confirmation=2)
    for i in range(2):
        reponse = client.post(
            f"/sessions/{session['id']}/inscriptions",
            json={"nom": f"P{i}", "email": f"p{i}@exemple.fr", "entreprise": "Exemple"},
        )
        assert reponse.status_code == 201
    assert client.get(f"/sessions/{session['id']}").json()["statut"] == "confirmee"
    assert len(client.get(f"/sessions/{session['id']}/inscriptions").json()) == 2


def test_session_inconnue_404(client):
    assert client.get("/sessions/42").status_code == 404
    reponse = client.post(
        "/sessions/42/inscriptions", json={"nom": "Ana", "email": "ana@exemple.fr"}
    )
    assert reponse.status_code == 404


def test_session_complete_409(client):
    session = creer_session(client, capacite=1, seuil_confirmation=1)
    client.post(f"/sessions/{session['id']}/inscriptions", json={"nom": "A", "email": "a@x.fr"})
    reponse = client.post(
        f"/sessions/{session['id']}/inscriptions", json={"nom": "B", "email": "b@x.fr"}
    )
    assert reponse.status_code == 409
    assert "complète" in reponse.json()["detail"]


def test_doublon_409(client):
    session = creer_session(client)
    corps = {"nom": "Ana", "email": "ana@exemple.fr"}
    client.post(f"/sessions/{session['id']}/inscriptions", json=corps)
    assert client.post(f"/sessions/{session['id']}/inscriptions", json=corps).status_code == 409


def test_annulation_puis_inscription_409(client):
    session = creer_session(client)
    reponse = client.post(f"/sessions/{session['id']}/annulation")
    assert reponse.status_code == 200
    assert reponse.json()["statut"] == "annulee"
    reponse = client.post(
        f"/sessions/{session['id']}/inscriptions", json={"nom": "Ana", "email": "ana@exemple.fr"}
    )
    assert reponse.status_code == 409


def test_desinscription_204_puis_404(client):
    session = creer_session(client)
    inscription = client.post(
        f"/sessions/{session['id']}/inscriptions", json={"nom": "Ana", "email": "ana@exemple.fr"}
    ).json()
    assert client.delete(f"/inscriptions/{inscription['id']}").status_code == 204
    assert client.delete(f"/inscriptions/{inscription['id']}").status_code == 404


@pytest.mark.parametrize(
    "corps",
    [
        {**SESSION, "duree_jours": 0},
        {**SESSION, "formation": ""},
        {**SESSION, "capacite": 2, "seuil_confirmation": 3},
    ],
)
def test_validation_422(client, corps):
    assert client.post("/sessions", json=corps).status_code == 422


def test_email_invalide_422(client):
    session = creer_session(client)
    reponse = client.post(
        f"/sessions/{session['id']}/inscriptions", json={"nom": "Ana", "email": "pas-un-mail"}
    )
    assert reponse.status_code == 422
