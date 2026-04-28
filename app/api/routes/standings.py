"""Standings API routes."""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.api.dependencies import get_db
from app.models import Standing, Season
from app.models.schemas import StandingResponse

router = APIRouter(prefix="/standings")

@router.get("/season/{season_id}", response_model=List[StandingResponse])
async def get_season_standings(
    season_id: int,
    matchday: int | None = None,
    db: Session = Depends(get_db),
):
    """Get standings for a specific season."""
    query = db.query(Standing).filter(Standing.season_id == season_id)
    
    if matchday:
        query = query.filter(Standing.matchday == matchday)
    else:
        latest = (
            db.query(Standing.matchday)
            .filter(Standing.season_id == season_id)
            .order_by(desc(Standing.matchday))
            .first()
        )
        if latest:
            query = query.filter(Standing.matchday == latest[0])
    
    standings = query.order_by(Standing.position).all()
    return standings

@router.get("/", response_model=List[StandingResponse])
async def get_current_standings(
    db: Session = Depends(get_db),
):
    """Get current league standings."""
    current_season = db.query(Season).filter(Season.is_current == True).first()
    
    if not current_season:
        return []
        
    standings = (
        db.query(Standing)
        .filter(Standing.season_id == current_season.id)
        .order_by(Standing.position)
        .all()
    )
    
    if standings:
        latest_matchday = standings[0].matchday
        standings = [s for s in standings if s.matchday == latest_matchday]
    
    return standings
