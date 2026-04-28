"""Base scraper class for web scraping."""
import asyncio
import time
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import httpx

from app.core.logger import logger
from app.core.exceptions import ScrapingError
from app.config import settings


class BaseScraper:
    """Base scraper with common functionality."""

    BASE_URL: str = ""
    RATE_LIMIT: float = settings.SCRAPE_RATE_LIMIT

    def __init__(self):
        """Initialize scraper."""
        self.client = httpx.AsyncClient(
            headers={"User-Agent": settings.USER_AGENT},
            timeout=30.0,
            follow_redirects=True,
        )
        self._last_request = 0

    async def _rate_limit(self) -> None:
        """Enforce rate limiting between requests."""
        elapsed = time.time() - self._last_request
        if elapsed < self.RATE_LIMIT:
            await asyncio.sleep(self.RATE_LIMIT - elapsed)
        self._last_request = time.time()

    async def fetch(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse a URL with rate limiting.
        
        Args:
            url: URL to fetch.
            
        Returns:
            BeautifulSoup object or None if failed.
            
        Raises:
            ScrapingError: If scraping fails.
        """
        await self._rate_limit()
        
        try:
            logger.info(f"Fetching: {url}")
            response = await self.client.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch {url}: {e}")
            raise ScrapingError(f"Failed to fetch {url}: {e}")

    async def scrape(self) -> List[Dict]:
        """Scrape data. To be implemented by subclasses.
        
        Returns:
            List of scraped data dictionaries.
        """
        raise NotImplementedError("Subclasses must implement scrape()")

    async def close(self) -> None:
        """Close the HTTP client."""
        await self.client.aclose()

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
