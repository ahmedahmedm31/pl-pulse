"""Fun fact model."""
from sqlalchemy import Column, Integer, ForeignKey, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class FunFact(BaseModel):
    """Fun fact model."""

    __tablename__ = "fun_facts"

    category = Column(String(50), nullable=False, index=True)  # records, streaks, unusual, etc.
    content = Column(Text, nullable=False)
    entity_type = Column(String(20))  # team, player, match
    entity_id = Column(Integer)
    season_id = Column(Integer, ForeignKey("seasons.id"))
    is_active = Column(Boolean, default=True)
    priority = Column(Integer, default=0)  # Higher priority shown first
    expires_at = Column(DateTime)  # Optional expiration date

    # Relationships
    season = relationship("Season", back_populates="fun_facts")

    def __repr__(self) -> str:
        """String representation."""
        return f"<FunFact(id={self.id}, category='{self.category}')>"
