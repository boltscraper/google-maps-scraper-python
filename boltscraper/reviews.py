"""
Google Reviews Scraper Resource
Extracts all customer reviews, ratings, reviewer metadata, and owner replies without OAuth.
"""

from typing import List, Union, Optional, Dict, Any


class ReviewsResource:
    def __init__(self, client):
        self._client = client

    def search(
        self,
        place_id: str,
        max_reviews: int = 500,
        sort: str = "newest"
    ) -> Dict[str, Any]:
        """
        Synchronously extract customer reviews for a Google Place ID without OAuth.
        
        Args:
            place_id: Google Maps Place ID or listing URL
            max_reviews: Maximum reviews to extract (up to 5,000+)
            sort: Sort order ('newest', 'most_relevant', 'highest_rating', 'lowest_rating')
        """
        payload = {
            "place_id": place_id,
            "max_reviews": max_reviews,
            "sort": sort
        }
        return self._client._request("POST", "/reviews/search", json=payload)

    def create_job(
        self,
        place_ids: Union[str, List[str]],
        max_reviews_per_place: int = 500,
        sort: str = "newest",
        webhook_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create an asynchronous batch reviews extraction job.
        """
        if isinstance(place_ids, str):
            place_ids = [place_ids]

        payload = {
            "place_ids": place_ids,
            "max_reviews_per_place": max_reviews_per_place,
            "sort": sort
        }
        if webhook_url:
            payload["webhook_url"] = webhook_url

        return self._client._request("POST", "/reviews/jobs", json=payload)

    def list_jobs(self, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        """List recent reviews scraping jobs."""
        params = {"page": page, "limit": limit}
        return self._client._request("GET", "/reviews/jobs", params=params)

    def get_job(self, job_id: str) -> Dict[str, Any]:
        """Retrieve progress and metadata for a reviews extraction job."""
        return self._client._request("GET", f"/reviews/jobs/{job_id}")

    def download_csv(self, job_id: str) -> bytes:
        """Download reviews CSV export."""
        return self._client._request("GET", f"/reviews/jobs/{job_id}/download", raw_bytes=True)

    def pause_job(self, job_id: str) -> Dict[str, Any]:
        """Pause a running reviews scraping job."""
        return self._client._request("POST", f"/reviews/jobs/{job_id}/pause")

    def resume_job(self, job_id: str) -> Dict[str, Any]:
        """Resume a paused reviews scraping job."""
        return self._client._request("POST", f"/reviews/jobs/{job_id}/resume")

    def stop_job(self, job_id: str) -> Dict[str, Any]:
        """Stop a reviews scraping job."""
        return self._client._request("POST", f"/reviews/jobs/{job_id}/control")
