"""Player statistics model."""
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class PlayerStats(BaseModel):
    """Player statistics per season model."""

    __tablename__ = "player_stats"

    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)
    matches_played = Column(Integer, default=0)
    goals = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    minutes = Column(Integer, default=0)
    yellow_cards = Column(Integer, default=0)
    red_cards = Column(Integer, default=0)
    clean_sheets = Column(Integer, default=0)  # For goalkeepers/defenders

    # Relationships
    player = relationship("Player", back_populates="stats")
    season = relationship("Season", back_populates="player_stats")

    def __repr__(self) -> str:
        """String representation."""
        return f"<PlayerStats(player_id={self.player_id}, goals={self.goals}, assists={self.assists})>"
