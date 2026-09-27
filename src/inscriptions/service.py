"""Règles métier des inscriptions.

Tout ce qui décide vit ici. Ni HTTP, ni stockage concret : le service reçoit un dépôt
et ne connaît que ses méthodes. Chaque règle a son test dans tests/test_service.py.
"""

from __future__ import annotations

from datetime import date

from .models import Inscription, Session, StatutSession
from .repository import Depot


class ErreurMetier(Exception):
    """Base des erreurs métier. L'API les traduit en réponses HTTP 4xx."""


class SessionInconnue(ErreurMetier):
    pass


class SessionComplete(ErreurMetier):
    pass


class SessionAnnulee(ErreurMetier):
    pass


class DejaInscrit(ErreurMetier):
    pass


class InscriptionInconnue(ErreurMetier):
    pass


class ServiceInscriptions:
    def __init__(self, depot: Depot) -> None:
        self.depot = depot

    # --- Sessions -------------------------------------------------------

    def creer_session(
        self,
        formation: str,
        date_debut: date,
        duree_jours: int,
        capacite: int = 8,
        seuil_confirmation: int = 4,
    ) -> Session:
        if duree_jours < 1:
            raise ValueError("La durée doit être d'au moins un jour.")
        if capacite < 1:
            raise ValueError("La capacité doit être d'au moins une place.")
        if not 1 <= seuil_confirmation <= capacite:
            raise ValueError("Le seuil de confirmation doit être compris entre 1 et la capacité.")
        session = Session(
            id=self.depot.prochain_id_session(),
            formation=formation.strip(),
            date_debut=date_debut,
            duree_jours=duree_jours,
            capacite=capacite,
            seuil_confirmation=seuil_confirmation,
        )
        self.depot.ajouter_session(session)
        return session

    def session(self, session_id: int) -> Session:
        session = self.depot.session(session_id)
        if session is None:
            raise SessionInconnue(f"Session {session_id} inconnue.")
        return session

    def sessions(self) -> list[Session]:
        return self.depot.sessions()

    def annuler_session(self, session_id: int) -> Session:
        session = self.session(session_id)
        session.statut = StatutSession.ANNULEE
        return session

    def places_restantes(self, session_id: int) -> int:
        session = self.session(session_id)
        return session.capacite - len(self.depot.inscriptions_de(session_id))

    # --- Inscriptions ---------------------------------------------------

    def inscrits(self, session_id: int) -> list[Inscription]:
        self.session(session_id)
        return self.depot.inscriptions_de(session_id)

    def inscrire(self, session_id: int, nom: str, email: str, entreprise: str) -> Inscription:
        session = self.session(session_id)
        if session.statut is StatutSession.ANNULEE:
            raise SessionAnnulee(f"La session {session_id} est annulée.")
        email_normalise = email.strip().lower()
        if any(i.email == email_normalise for i in self.depot.inscriptions_de(session_id)):
            raise DejaInscrit(f"{email_normalise} est déjà inscrit à la session {session_id}.")
        if self.places_restantes(session_id) <= 0:
            raise SessionComplete(f"La session {session_id} est complète.")
        inscription = Inscription(
            id=self.depot.prochain_id_inscription(),
            session_id=session_id,
            nom=nom.strip(),
            email=email_normalise,
            entreprise=entreprise.strip(),
        )
        self.depot.ajouter_inscription(inscription)
        self._confirmer_si_seuil_atteint(session)
        return inscription

    def desinscrire(self, inscription_id: int) -> None:
        inscription = self.depot.inscription(inscription_id)
        if inscription is None:
            raise InscriptionInconnue(f"Inscription {inscription_id} inconnue.")
        self.depot.supprimer_inscription(inscription_id)
        # Règle : une session confirmée le reste. On ne repasse jamais en attente.

    # --- Règles internes ------------------------------------------------

    def _confirmer_si_seuil_atteint(self, session: Session) -> None:
        if session.statut is not StatutSession.EN_ATTENTE:
            return
        if len(self.depot.inscriptions_de(session.id)) >= session.seuil_confirmation:
            session.statut = StatutSession.CONFIRMEE
