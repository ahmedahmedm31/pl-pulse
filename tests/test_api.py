"""API endpoint tests for PL Pulse."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db

# Use an in-memory SQLite database for tests
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "1.0.0"


def test_list_teams_empty(client):
    response = client.get("/api/teams/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_players_empty(client):
    response = client.get("/api/players/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_top_scorers_empty(client):
    response = client.get("/api/players/top-scorers")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_recent_matches_empty(client):
    response = client.get("/api/matches/recent")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_upcoming_matches_empty(client):
    response = client.get("/api/matches/upcoming")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_standings_empty(client):
    response = client.get("/api/standings/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_stats_endpoint(client):
    response = client.get("/api/stats/")
    assert response.status_code == 200
    data = response.json()
    assert "total_teams" in data
    assert "total_players" in data
    assert "total_matches" in data


def test_team_not_found(client):
    response = client.get("/api/teams/99999")
    assert response.status_code == 404


def test_player_not_found(client):
    response = client.get("/api/players/99999")
    assert response.status_code == 404


def test_match_not_found(client):
    response = client.get("/api/matches/99999")
    assert response.status_code == 404


def test_random_fact_not_found(client):
    response = client.get("/api/facts/random")
    assert response.status_code == 404


def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"PL Pulse" in response.content
