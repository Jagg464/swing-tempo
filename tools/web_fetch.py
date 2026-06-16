"""Web fetch (stub): httpx for standard pages, Playwright for JS-rendered. Respect
robots/ToS, FETCH_MIN_INTERVAL_SECONDS per domain, no authenticated content."""
from config import settings


def fetch(url: str, render: str = "httpx") -> str:
    raise NotImplementedError("Implement httpx/Playwright fetch with rate limiting.")


def extract_links(html: str, selectors: dict) -> list[dict]:
    raise NotImplementedError("Implement site-specific link/title extraction (BeautifulSoup).")