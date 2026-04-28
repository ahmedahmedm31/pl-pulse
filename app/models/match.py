"""Match model."""
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, String
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Match(BaseModel):
    """Football match model."""

    __tablename__ = "matches"

    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)
    matchday = Column(Integer, nullable=False)
    home_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    away_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    home_goals = Column(Integer)
    away_goals = Column(Integer)
    home_xg = Column(Float)  # Expected goals
    away_xg = Column(Float)
    match_date = Column(DateTime, nullable=False, index=True)
    venue = Column(String(100))
    attendance = Column(Integer)
    status = Column(String(20), default="scheduled")  # scheduled, completed, postponed

    # Relationships
    season = relationship("Season", back_populates="matches")
    home_team = relationship("Team", foreign_keys=[home_team_id], back_populates="home_matches")
    away_team = relationship("Team", foreign_keys=[away_team_id], back_populates="away_matches")
    prediction = relationship("Prediction", back_populates="match", uselist=False)

    def __repr__(self) -> str:
        """String representation."""
        return f"<Match(id={self.id}, home_team_id={self.home_team_id}, away_team_id={self.away_team_id})>"
