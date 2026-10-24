"""
Website Scraper Resource
Extracts direct business emails, phone numbers, and social links from company domains.
"""

from typing import List, Union, Optional, Dict, Any


class WebsiteResource:
    def __init__(self, client):
        self._client = client

    def scrape(self, url: str) -> Dict[str, Any]:
        """
        Synchronously scrape a single website domain for emails, phone numbers, and social media URLs.
        Automatically crawls subpages (/contact, /about, /team, etc.).
        
        Args:
            url: Company website URL (e.g. 'https://stripe.com')
            
        Returns:
            Dictionary containing extracted emails, phones, and social profile links.
        """
        payload = {"url": url}
        return self._client._request("POST", "/website/scrape", json=payload)

    def create_job(
        self,
        urls: Union[str, List[str]],
        name: Optional[str] = None,
        webhook_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create an asynchronous batch website extraction task for up to 10,000 URLs.
        
        Args:
            urls: Single domain string or list of website URLs
            name: Optional descriptive label for the task
            webhook_url: Optional callback URL when task completes
        """
        if isinstance(urls, str):
            urls = [urls]

        payload = {"urls": urls}
        if name:
            payload["name"] = name
        if webhook_url:
            payload["webhook_url"] = webhook_url

        return self._client._request("POST", "/website/jobs", json=payload)

    def list_jobs(self, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        """List recent website contact enrichment jobs."""
        params = {"page": page, "limit": limit}
        return self._client._request("GET", "/website/jobs", params=params)

    def get_job(self, job_id: str) -> Dict[str, Any]:
        """Retrieve progress and metadata for a website scraping job."""
        return self._client._request("GET", f"/website/jobs/{job_id}")

    def download_csv(self, job_id: str) -> bytes:
        """Download full website contact enrichment CSV dataset."""
        return self._client._request("GET", f"/website/jobs/{job_id}/download", raw_bytes=True)

    def stop_job(self, job_id: str) -> Dict[str, Any]:
        """Stop/cancel a website scraping job."""
        return self._client._request("POST", f"/website/jobs/{job_id}/control")
