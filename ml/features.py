"""Feature engineering for ML models."""
from typing import Dict, List
import pandas as pd
from sqlalchemy.orm import Session

from app.models import Match, Standing, Team


def calculate_form(matches: List[Match], team_id: int, last_n: int = 5) -> float:
    """Calculate team form from recent matches.
    
    Args:
        matches: List of recent matches.
        team_id: Team ID.
        last_n: Number of recent matches to consider.
        
    Returns:
        Form score (0-3 scale, 3=win, 1=draw, 0=loss).
    """
    form_points = []
    
    for match in matches[-last_n:]:
        if match.home_team_id == team_id:
            if match.home_goals > match.away_goals:
                form_points.append(3)
            elif match.home_goals == match.away_goals:
                form_points.append(1)
            else:
                form_points.append(0)
        elif match.away_team_id == team_id:
            if match.away_goals > match.home_goals:
                form_points.append(3)
            elif match.away_goals == match.home_goals:
                form_points.append(1)
            else:
                form_points.append(0)
    
    return sum(form_points) / len(form_points) if form_points else 1.5


def extract_match_features(
    match: Match,
    db: Session,
) -> Dict[str, float]:
    """Extract features for a match prediction.
    
    Args:
        match: Match object.
        db: Database session.
        
    Returns:
        Dictionary of features.
    """
    features = {}
    
    # Get recent matches for both teams
    home_matches = (
        db.query(Match)
        .filter(
            (Match.home_team_id == match.home_team_id)
            | (Match.away_team_id == match.home_team_id)
        )
        .filter(Match.status == "completed")
        .filter(Match.match_date < match.match_date)
        .order_by(Match.match_date.desc())
        .limit(10)
        .all()
    )
    
    away_matches = (
        db.query(Match)
        .filter(
            (Match.home_team_id == match.away_team_id)
            | (Match.away_team_id == match.away_team_id)
        )
        .filter(Match.status == "completed")
        .filter(Match.match_date < match.match_date)
        .order_by(Match.match_date.desc())
        .limit(10)
        .all()
    )
    
    # Calculate form
    features["home_form"] = calculate_form(home_matches, match.home_team_id)
    features["away_form"] = calculate_form(away_matches, match.away_team_id)
    
    # Get standings
    home_standing = (
        db.query(Standing)
        .filter(Standing.team_id == match.home_team_id)
        .filter(Standing.season_id == match.season_id)
        .order_by(Standing.matchday.desc())
        .first()
    )
    
    away_standing = (
        db.query(Standing)
        .filter(Standing.team_id == match.away_team_id)
        .filter(Standing.season_id == match.season_id)
        .order_by(Standing.matchday.desc())
        .first()
    )
    
    # Position features
    features["home_position"] = home_standing.position if home_standing else 10
    features["away_position"] = away_standing.position if away_standing else 10
    features["position_diff"] = features["away_position"] - features["home_position"]
    
    # Goals features
    if home_standing:
        features["home_goals_avg"] = (
            home_standing.goals_for / home_standing.played
            if home_standing.played > 0
            else 1.0
        )
        features["home_conceded_avg"] = (
            home_standing.goals_against / home_standing.played
            if home_standing.played > 0
            else 1.0
        )
    else:
        features["home_goals_avg"] = 1.0
        features["home_conceded_avg"] = 1.0
    
    if away_standing:
        features["away_goals_avg"] = (
            away_standing.goals_for / away_standing.played
            if away_standing.played > 0
            else 1.0
        )
        features["away_conceded_avg"] = (
            away_standing.goals_against / away_standing.played
            if away_standing.played > 0
            else 1.0
        )
    else:
        features["away_goals_avg"] = 1.0
        features["away_conceded_avg"] = 1.0
    
    # Home advantage
    features["home_advantage"] = 1.0
    
    return features
