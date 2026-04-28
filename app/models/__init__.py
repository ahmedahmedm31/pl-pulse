"""Database models."""
from app.models.base import BaseModel
from app.models.team import Team
from app.models.season import Season
from app.models.player import Player
from app.models.match import Match
from app.models.standing import Standing
from app.models.player_stats import PlayerStats
from app.models.prediction import Prediction
from app.models.fun_fact import FunFact

__all__ = [
    "BaseModel",
    "Team",
    "Season",
    "Player",
    "Match",
    "Standing",
    "PlayerStats",
    "Prediction",
    "FunFact",
]
