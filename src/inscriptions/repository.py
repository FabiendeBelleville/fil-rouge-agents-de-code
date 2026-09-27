"""Stockage en mémoire.

Volontairement minimal : le remplacer par SQLite est une fonctionnalité du backlog
(docs/backlog.md). Le service ne dépend que des méthodes publiques de cette classe.
"""

from __future__ import annotations

from .models import Inscription, Session


class Depot:
    def __init__(self) -> None:
        self._sessions: dict[int, Session] = {}
        self._inscriptions: dict[int, Inscription] = {}
        self._id_session = 0
        self._id_inscription = 0

    # --- Sessions -------------------------------------------------------

    def prochain_id_session(self) -> int:
        self._id_session += 1
        return self._id_session

    def ajouter_session(self, session: Session) -> None:
        self._sessions[session.id] = session

    def session(self, session_id: int) -> Session | None:
        return self._sessions.get(session_id)

    def sessions(self) -> list[Session]:
        return list(self._sessions.values())

    # --- Inscriptions ---------------------------------------------------

    def prochain_id_inscription(self) -> int:
        self._id_inscription += 1
        return self._id_inscription

    def ajouter_inscription(self, inscription: Inscription) -> None:
        self._inscriptions[inscription.id] = inscription

    def inscription(self, inscription_id: int) -> Inscription | None:
        return self._inscriptions.get(inscription_id)

    def inscriptions_de(self, session_id: int) -> list[Inscription]:
        return [i for i in self._inscriptions.values() if i.session_id == session_id]

    def supprimer_inscription(self, inscription_id: int) -> None:
        self._inscriptions.pop(inscription_id, None)
