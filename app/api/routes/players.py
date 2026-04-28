"""Players API routes."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.api.dependencies import get_db
from app.models import Player, PlayerStats, Season
from app.models.schemas import PlayerResponse, PlayerStatsResponse

router = APIRouter(prefix="/players")

@router.get("/top-scorers", response_model=List[PlayerStatsResponse])
async def get_top_scorers(
    limit: int = 20,
    season_id: int | None = None,
    db: Session = Depends(get_db),
):
    """Get top scorers."""
    query = db.query(PlayerStats).join(Player)
    
    if season_id:
        query = query.filter(PlayerStats.season_id == season_id)
    else:
        current_season = db.query(Season).filter(Season.is_current == True).first()
        if current_season:
            query = query.filter(PlayerStats.season_id == current_season.id)
    
    top_scorers = query.order_by(desc(PlayerStats.goals)).limit(limit).all()
    return top_scorers

@router.get("/", response_model=List[PlayerResponse])
async def list_players(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    """List all players."""
    players = db.query(Player).offset(skip).limit(limit).all()
    return players

@router.get("/{player_id}", response_model=PlayerResponse)
async def get_player(
    player_id: int,
    db: Session = Depends(get_db),
):
    """Get player details by ID."""
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail=f"Player {player_id} not found")
    return player
