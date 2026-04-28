"""Team model."""
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Team(BaseModel):
    """Premier League team model."""

    __tablename__ = "teams"

    name = Column(String(100), nullable=False, unique=True, index=True)
    short_name = Column(String(10), nullable=False)
    logo_url = Column(String(500))
    founded = Column(Integer)
    stadium = Column(String(100))

    # Relationships
    players = relationship("Player", back_populates="team")
    home_matches = relationship(
        "Match",
        foreign_keys="Match.home_team_id",
        back_populates="home_team",
    )
    away_matches = relationship(
        "Match",
        foreign_keys="Match.away_team_id",
        back_populates="away_team",
    )
    standings = relationship("Standing", back_populates="team")

    def __repr__(self) -> str:
        """String representation."""
        return f"<Team(id={self.id}, name='{self.name}')>"
