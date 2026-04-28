"""Fun facts API routes."""
import random
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api.dependencies import get_db
from app.models import FunFact
from app.models.schemas import FunFactResponse

router = APIRouter(prefix="/facts")

@router.get("/random", response_model=FunFactResponse)
async def get_random_fact(
    category: str | None = None,
    db: Session = Depends(get_db),
):
    """Get a random fun fact."""
    query = db.query(FunFact).filter(FunFact.is_active == True)
    
    if category:
        query = query.filter(FunFact.category == category)
    
    facts = query.all()
    
    if not facts:
        raise HTTPException(status_code=404, detail="No facts found")
    
    return random.choice(facts)

@router.get("/team/{team_id}", response_model=List[FunFactResponse])
async def get_team_facts(
    team_id: int,
    db: Session = Depends(get_db),
):
    """Get facts about a specific team."""
    facts = (
        db.query(FunFact)
        .filter(FunFact.is_active == True)
        .filter(FunFact.entity_type == "team")
        .filter(FunFact.entity_id == team_id)
        .all()
    )
    return facts

@router.get("/", response_model=List[FunFactResponse])
async def list_facts(
    category: str | None = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    """List fun facts."""
    query = db.query(FunFact).filter(FunFact.is_active == True)
    
    if category:
        query = query.filter(FunFact.category == category)
    
    facts = query.order_by(FunFact.priority.desc()).offset(skip).limit(limit).all()
    return facts
