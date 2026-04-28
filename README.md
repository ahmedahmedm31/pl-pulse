# ⚽ # PL Pulse

Premier League Stats, Facts & Predictions Dashboard

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

> 🚀 **Quick Deploy:** Click a button above to deploy your own instance in 2 minutes!**

PL Pulse is a comprehensive web application that provides Premier League statistics, fun facts, and ML-powered match predictions. Built with FastAPI, PostgreSQL, and modern web technologies.

## 🌟 Features

- **Real-time Standings**: Up-to-date league table with team statistics
- **Match Data**: Historical results and upcoming fixtures
- **Player Statistics**: Top scorers, assists, and performance metrics
- **Fun Facts Engine**: Interesting statistics and historical records
- **ML Predictions**: Machine learning-powered match outcome predictions
- **Interactive Dashboard**: Beautiful, responsive UI with charts and visualizations

## 🏗️ Architecture

### Technology Stack

- **Backend**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL / SQLite
- **ORM**: SQLAlchemy 2.0
- **Frontend**: Jinja2 Templates + Bootstrap 5
- **Charts**: Chart.js
- **ML**: Scikit-learn
- **Scraping**: BeautifulSoup4 + httpx
- **Scheduling**: APScheduler

### Project Structure

```
pl-pulse/
├── app/                    # Main application
│   ├── api/               # API routes
│   ├── core/              # Core utilities
│   ├── models/            # Database models
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic
│   └── repositories/      # Data access layer
├── scraper/               # Web scraping module
├── ml/                    # Machine learning models
├── jobs/                  # Background jobs
├── frontend/              # Templates and static files
├── scripts/               # Utility scripts
└── tests/                 # Test suite
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- PostgreSQL (optional, SQLite works for development)

### 🚀 Quick Deploy (Permanent Website)

Want to deploy this as a permanent website? See **[QUICK_DEPLOY.md](QUICK_DEPLOY.md)** for 2-minute setup instructions!

**Supported Platforms:**
- ✅ Render.com (Free tier available)
- ✅ Railway.app ($5 free credit/month)
- ✅ Heroku, Vercel, Fly.io, and more

Full deployment guide: [DEPLOYMENT.md](DEPLOYMENT.md)

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/pl-pulse.git
   cd pl-pulse
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize database**:
   ```bash
   python scripts/seed_database.py
   ```

6. **Run the application**:
   ```bash
   python app/main.py
   ```

7. **Open your browser**:
   Navigate to `http://localhost:8000`

## 📊 API Endpoints

### Teams
- `GET /api/teams` - List all teams
- `GET /api/teams/{id}` - Get team details

### Players
- `GET /api/players` - List all players
- `GET /api/players/{id}` - Get player details
- `GET /api/players/top-scorers` - Get top scorers

### Matches
- `GET /api/matches` - List all matches
- `GET /api/matches/{id}` - Get match details
- `GET /api/matches/recent` - Get recent results
- `GET /api/matches/upcoming` - Get upcoming fixtures

### Standings
- `GET /api/standings` - Get current league table
- `GET /api/standings/season/{id}` - Get historical standings

### Predictions
- `GET /api/predictions/matches` - Get match predictions
- `GET /api/predictions/{match_id}` - Get specific match prediction

### Fun Facts
- `GET /api/facts/random` - Get random fun fact
- `GET /api/facts` - List all facts
- `GET /api/facts/team/{id}` - Get team-specific facts

## 🧪 Testing

Run the test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=app tests/
```

## 📝 Development

### Code Style

This project follows PEP 8 standards with Black formatting:

```bash
# Format code
black app/ tests/

# Sort imports
isort app/ tests/

# Lint
flake8 app/ tests/

# Type checking
mypy app/
```

### Database Migrations

Using Alembic for database migrations:

```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## 🌐 Deployment

### Docker

```bash
docker build -t pl-pulse .
docker run -p 8000:8000 pl-pulse
```

### Railway / Render

1. Connect your GitHub repository
2. Set environment variables
3. Deploy with automatic builds

## 📖 Documentation

- [Architecture Document](docs/ARCHITECTURE.md)
- [API Documentation](docs/API.md)
- [Development Plan](docs/DEVELOPMENT.md)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Ahmed Magaji Ahmed**

## 🙏 Acknowledgments

- Premier League for the amazing football data
- FBRef, Transfermarkt for statistics
- FastAPI and SQLAlchemy communities

## 📞 Contact

For questions or feedback, please open an issue on GitHub.

---

**PL Pulse** - Making Premier League data accessible and fun! ⚽📊
