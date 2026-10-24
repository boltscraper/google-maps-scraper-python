"""
Bolt Scraper Official Python SDK
Fast, reliable, and proxy-free scraping for Google Maps, Google Reviews, and Websites.
"""

from .client import BoltScraper, VERSION
from .maps import MapsResource
from .reviews import ReviewsResource
from .website import WebsiteResource
from .webhooks import WebhooksResource
from .exceptions import (
    BoltScraperError,
    AuthenticationError,
    QuotaExceededError,
    NotFoundError,
    RateLimitError,
    UpstreamError
)

__version__ = VERSION
__all__ = [
    "BoltScraper",
    "MapsResource",
    "ReviewsResource",
    "WebsiteResource",
    "WebhooksResource",
    "BoltScraperError",
    "AuthenticationError",
    "QuotaExceededError",
    "NotFoundError",
    "RateLimitError",
    "UpstreamError"
]
