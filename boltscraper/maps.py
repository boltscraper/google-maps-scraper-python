"""
Google Maps Scraper Resource
Handles real-time search, asynchronous scraping jobs, and lead exports.
"""

from typing import List, Union, Optional, Dict, Any


class MapsResource:
    def __init__(self, client):
        self._client = client

    def search(
        self,
        keyword: str,
        page: int = 1,
        hl: str = "en"
    ) -> Dict[str, Any]:
        """
        Synchronous real-time Google Maps search (~2-4s response).
        
        Args:
            keyword: Search query (e.g. 'Coffee shops in Seattle' or 'Dentists Paris')
            page: Page number (1 to 15, yielding up to 20 results per page)
            hl: Two-letter interface language code (e.g. 'en', 'es', 'de', 'fr')
            
        Returns:
            Dictionary containing pagination metadata and extracted leads with 60+ attributes.
        """
        payload = {
            "keyword": keyword,
            "page": page,
            "hl": hl
        }
        return self._client._request("POST", "/maps/search", json=payload)

    def create_job(
        self,
        keywords: Union[str, List[str]],
        title: Optional[str] = None,
        scrape_websites: bool = True,
        ultra_mode: bool = True,
        max_results: Optional[int] = None,
        webhook_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create an asynchronous Google Maps background scraping job.
        
        Args:
            keywords: Single search string or list of query strings
            title: Custom label for the scraping task
            scrape_websites: Automatically crawl discovered websites for emails and social links
            ultra_mode: Enable multi-point grid scanning for up to 3x more listings
            max_results: Optional cap on listings per query
            webhook_url: Optional webhook URL to notify when completed
            
        Returns:
            Dictionary containing job_id and initial job status.
        """
        if isinstance(keywords, str):
            keywords = [keywords]

        payload = {
            "keywords": keywords,
            "scrape_websites": scrape_websites,
            "ultra_mode": ultra_mode
        }
        if title:
            payload["title"] = title
        if max_results:
            payload["max_results"] = max_results
        if webhook_url:
            payload["webhook_url"] = webhook_url

        return self._client._request("POST", "/maps/jobs", json=payload)

    def list_jobs(self, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        """
        List your recent Google Maps scraping jobs with status and progress.
        """
        params = {"page": page, "limit": limit}
        return self._client._request("GET", "/maps/jobs", params=params)

    def get_job(self, job_id: str) -> Dict[str, Any]:
        """
        Retrieve live progress and metadata for a specific scraping job.
        """
        return self._client._request("GET", f"/maps/jobs/{job_id}")

    def download_csv(self, job_id: str) -> bytes:
        """
        Download the full CSV dataset for a completed or paused job.
        """
        return self._client._request("GET", f"/maps/jobs/{job_id}/download", raw_bytes=True)

    def pause_job(self, job_id: str) -> Dict[str, Any]:
        """Pause an active Google Maps scraping job."""
        return self._client._request("POST", f"/maps/jobs/{job_id}/pause")

    def resume_job(self, job_id: str) -> Dict[str, Any]:
        """Resume a paused Google Maps scraping job."""
        return self._client._request("POST", f"/maps/jobs/{job_id}/resume")

    def stop_job(self, job_id: str) -> Dict[str, Any]:
        """Stop/cancel a scraping job and finalize partial results."""
        return self._client._request("POST", f"/maps/jobs/{job_id}/stop")
