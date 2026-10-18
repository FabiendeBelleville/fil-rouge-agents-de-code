"""Modèle du domaine : sessions de formation et inscriptions. Aucune logique ici."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import StrEnum


class StatutSession(StrEnum):
    EN_ATTENTE = "en_attente"  # ouverte aux inscriptions, seuil de confirmation pas atteint
    CONFIRMEE = "confirmee"  # le seuil est atteint : la session aura lieu
    ANNULEE = "annulee"  # n'accepte plus d'inscription


@dataclass
class Session:
    id: int
    formation: str
    date_debut: date
    duree_jours: int
    capacite: int = 8
    seuil_confirmation: int = 4
    statut: StatutSession = StatutSession.EN_ATTENTE


@dataclass
class Inscription:
    id: int
    session_id: int
    nom: str
    email: str
    entreprise: str
