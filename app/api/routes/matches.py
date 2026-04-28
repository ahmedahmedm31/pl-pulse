"""Matches API routes."""
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc

from app.api.dependencies import get_db
from app.models import Match
from app.models.schemas import MatchResponse

router = APIRouter(prefix="/matches")

@router.get("/recent", response_model=List[MatchResponse])
async def get_recent_matches(
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """Get recent completed matches."""
    matches = (
        db.query(Match)
        .filter(Match.status == "completed")
        .filter(Match.match_date <= datetime.utcnow())
        .order_by(desc(Match.match_date))
        .limit(limit)
        .all()
    )
    return matches

@router.get("/upcoming", response_model=List[MatchResponse])
async def get_upcoming_matches(
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """Get upcoming scheduled matches."""
    matches = (
        db.query(Match)
        .filter(Match.status == "scheduled")
        .filter(Match.match_date >= datetime.utcnow())
        .order_by(asc(Match.match_date))
        .limit(limit)
        .all()
    )
    return matches

@router.get("/", response_model=List[MatchResponse])
async def list_matches(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    """List all matches."""
    matches = (
        db.query(Match)
        .order_by(desc(Match.match_date))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return matches

@router.get("/{match_id}", response_model=MatchResponse)
async def get_match(
    match_id: int,
    db: Session = Depends(get_db),
):
    """Get match details by ID."""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail=f"Match {match_id} not found")
    return match
