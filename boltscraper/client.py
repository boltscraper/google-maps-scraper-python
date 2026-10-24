"""
Bolt Scraper Official Python SDK Client
"""

import os
import time
from typing import Optional, Dict, Any
import requests

from .exceptions import (
    BoltScraperError,
    AuthenticationError,
    QuotaExceededError,
    NotFoundError,
    RateLimitError,
    UpstreamError
)
from .maps import MapsResource
from .reviews import ReviewsResource
from .website import WebsiteResource
from .webhooks import WebhooksResource

DEFAULT_BASE_URL = "https://boltscraper.com/api/v1"
VERSION = "1.0.0"


class BoltScraper:
    """
    Official Python SDK client for Bolt Scraper.
    
    Usage:
        from boltscraper import BoltScraper

        # Initialize with your API key
        client = BoltScraper(api_key="bs_live_your_key_here")

        # 1. Search Google Maps in real time
        results = client.maps.search("Plumbers in Austin, TX", page=1)

        # 2. Extract customer reviews without OAuth
        reviews = client.reviews.search("ChIJb8Jg9q-1RIYRAxvq_mZ0gXY", max_reviews=100)

        # 3. Extract direct business emails and socials from a domain
        company = client.website.scrape("https://example.com")
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = 60,
        max_retries: int = 3,
        auto_retry_rate_limit: bool = True
    ):
        self.api_key = api_key or os.getenv("BOLTSCRAPER_API_KEY")
        if not self.api_key:
            raise AuthenticationError(
                "Missing Bolt Scraper API key. Pass 'api_key' to BoltScraper(api_key='bs_...') "
                "or set the 'BOLTSCRAPER_API_KEY' environment variable. "
                "Get your key at https://app.boltscraper.com"
            )

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.auto_retry_rate_limit = auto_retry_rate_limit

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": f"boltscraper-python/{VERSION}"
        })

        # Initialize resources
        self.maps = MapsResource(self)
        self.reviews = ReviewsResource(self)
        self.website = WebsiteResource(self)
        self.webhooks = WebhooksResource(self)

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        raw_bytes: bool = False
    ) -> Any:
        url = f"{self.base_url}{path}"
        retries = 0

        while True:
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json,
                    timeout=self.timeout
                )
            except requests.exceptions.RequestException as e:
                raise BoltScraperError(f"Network request to Bolt Scraper failed: {str(e)}")

            if response.status_code == 200:
                if raw_bytes:
                    return response.content
                try:
                    return response.json()
                except ValueError:
                    return response.text

            # Handle 429 with automatic exponential backoff
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 2 ** retries))
                if self.auto_retry_rate_limit and retries < self.max_retries:
                    retries += 1
                    time.sleep(retry_after)
                    continue
                try:
                    err_json = response.json()
                except ValueError:
                    err_json = {}
                raise RateLimitError(
                    f"Bolt Scraper rate limit exceeded (60 req/min). Retry after {retry_after}s.",
                    retry_after=retry_after,
                    response_body=err_json
                )

            # Parse error payload
            try:
                err_body = response.json()
                err_msg = err_body.get("error") or err_body.get("message") or response.text
            except ValueError:
                err_body = {}
                err_msg = response.text or f"HTTP {response.status_code}"

            if response.status_code == 401:
                raise AuthenticationError(
                    f"Authentication failed: {err_msg}. Verify your 'bs_...' API key at https://app.boltscraper.com",
                    status_code=401,
                    response_body=err_body
                )
            elif response.status_code == 403:
                raise QuotaExceededError(
                    f"Quota exceeded: {err_msg}. Upgrade your plan at https://boltscraper.com/pricing",
                    status_code=403,
                    response_body=err_body
                )
            elif response.status_code == 404:
                raise NotFoundError(
                    f"Resource not found: {err_msg}",
                    status_code=404,
                    response_body=err_body
                )
            elif response.status_code in (502, 503, 504):
                raise UpstreamError(
                    f"Target upstream error (0 credits billed): {err_msg}",
                    status_code=response.status_code,
                    response_body=err_body
                )
            else:
                raise BoltScraperError(
                    f"Bolt Scraper API error ({response.status_code}): {err_msg}",
                    status_code=response.status_code,
                    response_body=err_body
                )
