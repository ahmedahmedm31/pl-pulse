"""Player model."""
from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Player(BaseModel):
    """Football player model."""

    __tablename__ = "players"

    name = Column(String(100), nullable=False, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    position = Column(String(50))  # Forward, Midfielder, Defender, Goalkeeper
    nationality = Column(String(50))
    birth_date = Column(Date)

    # Relationships
    team = relationship("Team", back_populates="players")
    stats = relationship("PlayerStats", back_populates="player")

    def __repr__(self) -> str:
        """String representation."""
        return f"<Player(id={self.id}, name='{self.name}')>"
