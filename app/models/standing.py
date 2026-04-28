"""Standing model."""
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Standing(BaseModel):
    """League standings model."""

    __tablename__ = "standings"

    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)
    matchday = Column(Integer, nullable=False)
    position = Column(Integer, nullable=False)
    played = Column(Integer, default=0)
    won = Column(Integer, default=0)
    drawn = Column(Integer, default=0)
    lost = Column(Integer, default=0)
    goals_for = Column(Integer, default=0)
    goals_against = Column(Integer, default=0)
    goal_difference = Column(Integer, default=0)
    points = Column(Integer, default=0)
    form = Column(String(10))  # e.g., "WWDLW"

    # Relationships
    team = relationship("Team", back_populates="standings")
    season = relationship("Season", back_populates="standings")

    def __repr__(self) -> str:
        """String representation."""
        return f"<Standing(team_id={self.team_id}, position={self.position}, points={self.points})>"
