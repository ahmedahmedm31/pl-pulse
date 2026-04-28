"""Predictions API routes."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models import Prediction, Match
from app.models.schemas import PredictionResponse

router = APIRouter(prefix="/predictions")

@router.get("/matches", response_model=List[PredictionResponse])
async def get_match_predictions(
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """Get predictions for upcoming matches."""
    predictions = (
        db.query(Prediction)
        .join(Match)
        .filter(Match.status == "scheduled")
        .limit(limit)
        .all()
    )
    return predictions

@router.get("/{match_id}", response_model=PredictionResponse)
async def get_match_prediction(
    match_id: int,
    db: Session = Depends(get_db),
):
    """Get prediction for a specific match."""
    prediction = db.query(Prediction).filter(Prediction.match_id == match_id).first()
    if not prediction:
        raise HTTPException(
            status_code=404, detail=f"Prediction for match {match_id} not found"
        )
    return prediction
