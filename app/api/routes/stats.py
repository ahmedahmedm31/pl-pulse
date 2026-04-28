"""Statistics API routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api.dependencies import get_db
from app.models import Team, Player, Match, Standing

router = APIRouter(prefix="/stats")

@router.get("/")
async def get_stats(
    db: Session = Depends(get_db),
):
    """Get general statistics."""
    teams_count = db.query(func.count(Team.id)).scalar() or 0
    players_count = db.query(func.count(Player.id)).scalar() or 0
    matches_count = db.query(func.count(Match.id)).scalar() or 0
    
    return {
        "total_teams": teams_count,
        "total_players": players_count,
        "total_matches": matches_count,
        "status": "active"
    }
