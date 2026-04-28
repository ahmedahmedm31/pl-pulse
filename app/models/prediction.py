"""Prediction model."""
from sqlalchemy import Column, Integer, ForeignKey, Float, String
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Prediction(BaseModel):
    """Match prediction model."""

    __tablename__ = "predictions"

    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False, unique=True)
    home_win_prob = Column(Float, nullable=False)
    draw_prob = Column(Float, nullable=False)
    away_win_prob = Column(Float, nullable=False)
    predicted_home_goals = Column(Float)
    predicted_away_goals = Column(Float)
    model_version = Column(String(50))
    confidence = Column(Float)  # Overall confidence score

    # Relationships
    match = relationship("Match", back_populates="prediction")

    def __repr__(self) -> str:
        """String representation."""
        return f"<Prediction(match_id={self.match_id}, home_win={self.home_win_prob:.2f})>"
