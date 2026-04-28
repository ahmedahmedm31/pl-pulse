"""Seed database with sample data."""
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import SessionLocal, init_db
from app.models import Team, Season, Player, Match, Standing, PlayerStats, FunFact
from app.core.logger import logger


def seed_teams(db):
    """Seed teams data."""
    teams_data = [
        {"name": "Arsenal", "short_name": "ARS", "founded": 1886, "stadium": "Emirates Stadium"},
        {"name": "Manchester City", "short_name": "MCI", "founded": 1880, "stadium": "Etihad Stadium"},
        {"name": "Liverpool", "short_name": "LIV", "founded": 1892, "stadium": "Anfield"},
        {"name": "Chelsea", "short_name": "CHE", "founded": 1905, "stadium": "Stamford Bridge"},
        {"name": "Manchester United", "short_name": "MUN", "founded": 1878, "stadium": "Old Trafford"},
        {"name": "Tottenham Hotspur", "short_name": "TOT", "founded": 1882, "stadium": "Tottenham Hotspur Stadium"},
        {"name": "Newcastle United", "short_name": "NEW", "founded": 1892, "stadium": "St James' Park"},
        {"name": "Aston Villa", "short_name": "AVL", "founded": 1874, "stadium": "Villa Park"},
        {"name": "Brighton", "short_name": "BHA", "founded": 1901, "stadium": "Amex Stadium"},
        {"name": "West Ham United", "short_name": "WHU", "founded": 1895, "stadium": "London Stadium"},
    ]
    
    teams = []
    for team_data in teams_data:
        team = Team(**team_data)
        db.add(team)
        teams.append(team)
    
    db.commit()
    logger.info(f"Seeded {len(teams)} teams")
    return teams


def seed_seasons(db):
    """Seed seasons data."""
    seasons_data = [
        {"year_start": 2023, "year_end": 2024, "name": "2023-24", "is_current": False},
        {"year_start": 2024, "year_end": 2025, "name": "2024-25", "is_current": False},
        {"year_start": 2025, "year_end": 2026, "name": "2025-26", "is_current": True},
    ]
    
    seasons = []
    for season_data in seasons_data:
        season = Season(**season_data)
        db.add(season)
        seasons.append(season)
    
    db.commit()
    logger.info(f"Seeded {len(seasons)} seasons")
    return seasons


def seed_players(db, teams):
    """Seed players data."""
    players_data = [
        {"name": "Bukayo Saka", "team_id": teams[0].id, "position": "Forward", "nationality": "England"},
        {"name": "Erling Haaland", "team_id": teams[1].id, "position": "Forward", "nationality": "Norway"},
        {"name": "Mohamed Salah", "team_id": teams[2].id, "position": "Forward", "nationality": "Egypt"},
        {"name": "Cole Palmer", "team_id": teams[3].id, "position": "Midfielder", "nationality": "England"},
        {"name": "Bruno Fernandes", "team_id": teams[4].id, "position": "Midfielder", "nationality": "Portugal"},
        {"name": "Son Heung-min", "team_id": teams[5].id, "position": "Forward", "nationality": "South Korea"},
        {"name": "Alexander Isak", "team_id": teams[6].id, "position": "Forward", "nationality": "Sweden"},
        {"name": "Ollie Watkins", "team_id": teams[7].id, "position": "Forward", "nationality": "England"},
        {"name": "Kaoru Mitoma", "team_id": teams[8].id, "position": "Forward", "nationality": "Japan"},
        {"name": "Jarrod Bowen", "team_id": teams[9].id, "position": "Forward", "nationality": "England"},
    ]
    
    players = []
    for player_data in players_data:
        player = Player(**player_data)
        db.add(player)
        players.append(player)
    
    db.commit()
    logger.info(f"Seeded {len(players)} players")
    return players


def seed_matches(db, teams, seasons):
    """Seed matches data."""
    current_season = [s for s in seasons if s.is_current][0]
    
    matches = []
    base_date = datetime.now() - timedelta(days=30)
    
    # Create some completed matches
    for i in range(10):
        match = Match(
            season_id=current_season.id,
            matchday=i + 1,
            home_team_id=teams[i % len(teams)].id,
            away_team_id=teams[(i + 1) % len(teams)].id,
            home_goals=(i % 3) + 1,
            away_goals=i % 2,
            match_date=base_date + timedelta(days=i * 3),
            status="completed",
        )
        db.add(match)
        matches.append(match)
    
    # Create some upcoming matches
    future_date = datetime.now() + timedelta(days=7)
    for i in range(5):
        match = Match(
            season_id=current_season.id,
            matchday=11 + i,
            home_team_id=teams[(i + 2) % len(teams)].id,
            away_team_id=teams[(i + 3) % len(teams)].id,
            match_date=future_date + timedelta(days=i * 3),
            status="scheduled",
        )
        db.add(match)
        matches.append(match)
    
    db.commit()
    logger.info(f"Seeded {len(matches)} matches")
    return matches


def seed_standings(db, teams, seasons):
    """Seed standings data."""
    current_season = [s for s in seasons if s.is_current][0]
    
    standings = []
    for i, team in enumerate(teams):
        standing = Standing(
            team_id=team.id,
            season_id=current_season.id,
            matchday=10,
            position=i + 1,
            played=10,
            won=8 - i,
            drawn=2,
            lost=i,
            goals_for=25 - (i * 2),
            goals_against=10 + i,
            goal_difference=15 - (i * 3),
            points=26 - (i * 3),
            form="WWDLW",
        )
        db.add(standing)
        standings.append(standing)
    
    db.commit()
    logger.info(f"Seeded {len(standings)} standings")
    return standings


def seed_player_stats(db, players, seasons):
    """Seed player stats data."""
    current_season = [s for s in seasons if s.is_current][0]
    
    stats = []
    for i, player in enumerate(players):
        stat = PlayerStats(
            player_id=player.id,
            season_id=current_season.id,
            matches_played=10,
            goals=15 - i,
            assists=8 - (i // 2),
            minutes=900,
            yellow_cards=i % 3,
            red_cards=0,
        )
        db.add(stat)
        stats.append(stat)
    
    db.commit()
    logger.info(f"Seeded {len(stats)} player stats")
    return stats


def seed_fun_facts(db, teams, seasons):
    """Seed fun facts data."""
    current_season = [s for s in seasons if s.is_current][0]
    
    facts_data = [
        {
            "category": "records",
            "content": "Erling Haaland scored 36 goals in the 2022-23 season, breaking the Premier League single-season record.",
            "entity_type": "player",
            "entity_id": 2,
            "season_id": current_season.id,
        },
        {
            "category": "streaks",
            "content": "Arsenal are currently on a 15-match unbeaten run at the Emirates Stadium.",
            "entity_type": "team",
            "entity_id": teams[0].id,
            "season_id": current_season.id,
        },
        {
            "category": "unusual",
            "content": "Teams wearing red kits have won 58% of their matches this season.",
            "entity_type": None,
            "entity_id": None,
            "season_id": current_season.id,
        },
        {
            "category": "historical",
            "content": "Arsenal went the entire 2003-04 season unbeaten, earning the nickname 'The Invincibles'.",
            "entity_type": "team",
            "entity_id": teams[0].id,
            "season_id": None,
        },
        {
            "category": "records",
            "content": "Alan Shearer holds the all-time Premier League scoring record with 260 goals.",
            "entity_type": None,
            "entity_id": None,
            "season_id": None,
        },
    ]
    
    facts = []
    for fact_data in facts_data:
        fact = FunFact(**fact_data)
        db.add(fact)
        facts.append(fact)
    
    db.commit()
    logger.info(f"Seeded {len(facts)} fun facts")
    return facts


def main():
    """Main seeding function."""
    logger.info("Starting database seeding...")
    
    # Initialize database
    init_db()
    
    # Create session
    db = SessionLocal()
    
    try:
        # Seed data
        teams = seed_teams(db)
        seasons = seed_seasons(db)
        players = seed_players(db, teams)
        matches = seed_matches(db, teams, seasons)
        standings = seed_standings(db, teams, seasons)
        player_stats = seed_player_stats(db, players, seasons)
        fun_facts = seed_fun_facts(db, teams, seasons)
        
        logger.info("Database seeding completed successfully!")
        
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
