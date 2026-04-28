"""Teams API routes."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models import Team
from app.models.schemas import TeamResponse

router = APIRouter(prefix="/teams")

@router.get("/", response_model=List[TeamResponse])
async def list_teams(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    """List all Premier League teams."""
    teams = db.query(Team).offset(skip).limit(limit).all()
    return teams

@router.get("/{team_id}", response_model=TeamResponse)
async def get_team(
    team_id: int,
    db: Session = Depends(get_db),
):
    """Get team details by ID."""
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail=f"Team {team_id} not found")
    return team
