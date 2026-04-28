"""Season model."""
from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Season(BaseModel):
    """Football season model."""

    __tablename__ = "seasons"

    year_start = Column(Integer, nullable=False)
    year_end = Column(Integer, nullable=False)
    name = Column(String(20), nullable=False, unique=True)  # e.g., "2023-24"
    is_current = Column(Boolean, default=False)

    # Relationships
    matches = relationship("Match", back_populates="season")
    standings = relationship("Standing", back_populates="season")
    player_stats = relationship("PlayerStats", back_populates="season")
    fun_facts = relationship("FunFact", back_populates="season")

    def __repr__(self) -> str:
        """String representation."""
        return f"<Season(id={self.id}, name='{self.name}')>"
