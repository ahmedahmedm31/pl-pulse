"""FastAPI application entry point."""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.config import settings
from app.core import init_db, logger
from app.api.routes import teams, players, matches, standings, predictions, facts, stats

# Get absolute paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "frontend", "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "frontend", "templates")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    logger.info("Starting PL Pulse application...")
    init_db()
    logger.info("Database initialized")
    yield
    logger.info("Shutting down PL Pulse application...")

# Create FastAPI app
app = FastAPI(
    title="PL Pulse",
    description="Premier League Stats, Facts & Predictions",
    version="1.0.0",
    debug=settings.DEBUG,
    lifespan=lifespan,
)

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Setup templates
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Include API routers
app.include_router(teams.router, prefix="/api", tags=["teams"])
app.include_router(players.router, prefix="/api", tags=["players"])
app.include_router(matches.router, prefix="/api", tags=["matches"])
app.include_router(standings.router, prefix="/api", tags=["standings"])
app.include_router(predictions.router, prefix="/api", tags=["predictions"])
app.include_router(facts.router, prefix="/api", tags=["facts"])
app.include_router(stats.router, prefix="/api", tags=["stats"])

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
