"""Contrat HTTP. Traduit les requêtes en appels au service, et les erreurs métier en codes HTTP.

Aucune règle métier ici : si vous avez envie d'écrire un `if` sur le domaine, il va dans service.py.
"""

from __future__ import annotations

from datetime import date

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

from .models import Inscription, Session
from .repository import Depot
from .service import (
    DejaInscrit,
    ErreurMetier,
    InscriptionInconnue,
    ServiceInscriptions,
    SessionAnnulee,
    SessionComplete,
    SessionInconnue,
)

# --- Schémas d'entrée et de sortie ----------------------------------------


class SessionCreation(BaseModel):
    formation: str = Field(min_length=1)
    date_debut: date
    duree_jours: int = Field(ge=1)
    capacite: int = Field(default=8, ge=1)
    seuil_confirmation: int = Field(default=4, ge=1)


class SessionVue(BaseModel):
    id: int
    formation: str
    date_debut: date
    duree_jours: int
    capacite: int
    seuil_confirmation: int
    statut: str
    nombre_inscrits: int
    places_restantes: int

    @classmethod
    def depuis(cls, session: Session, nombre_inscrits: int) -> SessionVue:
        return cls(
            id=session.id,
            formation=session.formation,
            date_debut=session.date_debut,
            duree_jours=session.duree_jours,
            capacite=session.capacite,
            seuil_confirmation=session.seuil_confirmation,
            statut=session.statut.value,
            nombre_inscrits=nombre_inscrits,
            places_restantes=session.capacite - nombre_inscrits,
        )


class InscriptionCreation(BaseModel):
    nom: str = Field(min_length=1)
    email: str = Field(min_length=3)
    entreprise: str = Field(default="")

    @field_validator("email")
    @classmethod
    def email_plausible(cls, valeur: str) -> str:
        if "@" not in valeur or valeur.startswith("@") or valeur.endswith("@"):
            raise ValueError("adresse e-mail invalide")
        return valeur


class InscriptionVue(BaseModel):
    id: int
    session_id: int
    nom: str
    email: str
    entreprise: str

    @classmethod
    def depuis(cls, inscription: Inscription) -> InscriptionVue:
        return cls(
            id=inscription.id,
            session_id=inscription.session_id,
            nom=inscription.nom,
            email=inscription.email,
            entreprise=inscription.entreprise,
        )


# --- Application -----------------------------------------------------------

CODES_HTTP: dict[type[ErreurMetier], int] = {
    SessionInconnue: status.HTTP_404_NOT_FOUND,
    InscriptionInconnue: status.HTTP_404_NOT_FOUND,
    SessionComplete: status.HTTP_409_CONFLICT,
    SessionAnnulee: status.HTTP_409_CONFLICT,
    DejaInscrit: status.HTTP_409_CONFLICT,
}


def creer_application(service: ServiceInscriptions | None = None) -> FastAPI:
    service = service or ServiceInscriptions(Depot())
    app = FastAPI(title="Inscriptions aux sessions de formation", version="0.1.0")

    @app.exception_handler(ErreurMetier)
    async def erreur_metier(_: Request, erreur: ErreurMetier) -> JSONResponse:
        code = CODES_HTTP.get(type(erreur), status.HTTP_400_BAD_REQUEST)
        return JSONResponse(status_code=code, content={"detail": str(erreur)})

    @app.exception_handler(ValueError)
    async def valeur_invalide(_: Request, erreur: ValueError) -> JSONResponse:
        return JSONResponse(status_code=422, content={"detail": str(erreur)})

    def vue(session: Session) -> SessionVue:
        return SessionVue.depuis(session, len(service.inscrits(session.id)))

    @app.post("/sessions", response_model=SessionVue, status_code=status.HTTP_201_CREATED)
    def creer_session(corps: SessionCreation) -> SessionVue:
        return vue(service.creer_session(**corps.model_dump()))

    @app.get("/sessions", response_model=list[SessionVue])
    def lister_sessions() -> list[SessionVue]:
        return [vue(s) for s in service.sessions()]

    @app.get("/sessions/{session_id}", response_model=SessionVue)
    def lire_session(session_id: int) -> SessionVue:
        return vue(service.session(session_id))

    @app.post("/sessions/{session_id}/annulation", response_model=SessionVue)
    def annuler_session(session_id: int) -> SessionVue:
        return vue(service.annuler_session(session_id))

    @app.get("/sessions/{session_id}/inscriptions", response_model=list[InscriptionVue])
    def lister_inscriptions(session_id: int) -> list[InscriptionVue]:
        return [InscriptionVue.depuis(i) for i in service.inscrits(session_id)]

    @app.post(
        "/sessions/{session_id}/inscriptions",
        response_model=InscriptionVue,
        status_code=status.HTTP_201_CREATED,
    )
    def inscrire(session_id: int, corps: InscriptionCreation) -> InscriptionVue:
        return InscriptionVue.depuis(service.inscrire(session_id, **corps.model_dump()))

    @app.delete("/inscriptions/{inscription_id}", status_code=status.HTTP_204_NO_CONTENT)
    def desinscrire(inscription_id: int) -> None:
        service.desinscrire(inscription_id)

    return app


app = creer_application()
