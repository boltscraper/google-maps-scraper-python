"""
Bolt Scraper Python SDK - Exception Classes
"""

class BoltScraperError(Exception):
    """Base exception for all Bolt Scraper SDK errors."""
    def __init__(self, message: str, status_code: int = None, response_body: dict = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_body = response_body or {}


class AuthenticationError(BoltScraperError):
    """Raised on 401 Unauthorized - invalid or missing API key."""
    pass


class QuotaExceededError(BoltScraperError):
    """Raised on 403 Forbidden - monthly lead or crawl credits exhausted."""
    pass


class NotFoundError(BoltScraperError):
    """Raised on 404 Not Found - resource or job ID not found."""
    pass


class RateLimitError(BoltScraperError):
    """Raised on 429 Too Many Requests - hit 60 req/min limit."""
    def __init__(self, message: str, retry_after: int = 1, status_code: int = 429, response_body: dict = None):
        super().__init__(message, status_code, response_body)
        self.retry_after = retry_after


class UpstreamError(BoltScraperError):
    """Raised on 502/504 Bad Gateway - target domain unreachable or upstream failure."""
    pass
