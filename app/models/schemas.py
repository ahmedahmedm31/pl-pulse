"""Pydantic schemas for API validation and serialization."""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class TeamBase(BaseModel):
    name: str
    short_name: str
    founded: int
    stadium: str
    logo_url: Optional[str] = None

class TeamResponse(TeamBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class PlayerBase(BaseModel):
    name: str
    team_id: int
    position: str
    nationality: str
    birth_date: Optional[datetime] = None

class PlayerResponse(PlayerBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class PlayerStatsResponse(BaseModel):
    player_id: int
    season_id: int
    matches_played: int
    goals: int
    assists: int
    minutes: int
    yellow_cards: int
    red_cards: int
    clean_sheets: int
    model_config = ConfigDict(from_attributes=True)

class MatchBase(BaseModel):
    season_id: int
    matchday: int
    home_team_id: int
    away_team_id: int
    home_goals: Optional[int] = None
    away_goals: Optional[int] = None
    home_xg: Optional[float] = None
    away_xg: Optional[float] = None
    match_date: datetime
    venue: Optional[str] = None
    attendance: Optional[int] = None
    status: str

class MatchResponse(MatchBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class StandingBase(BaseModel):
    team_id: int
    season_id: int
    matchday: int
    position: int
    played: int
    won: int
    drawn: int
    lost: int
    goals_for: int
    goals_against: int
    goal_difference: int
    points: int
    form: Optional[str] = None

class StandingResponse(StandingBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class PredictionBase(BaseModel):
    match_id: int
    home_win_prob: float
    draw_prob: float
    away_win_prob: float
    predicted_home_goals: Optional[float] = None
    predicted_away_goals: Optional[float] = None
    model_config = ConfigDict(from_attributes=True)

class PredictionResponse(PredictionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class FunFactBase(BaseModel):
    category: str
    content: str
    entity_type: Optional[str] = None
    entity_id: Optional[int] = None
    season_id: Optional[int] = None
    is_active: bool
    priority: int

class FunFactResponse(FunFactBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
