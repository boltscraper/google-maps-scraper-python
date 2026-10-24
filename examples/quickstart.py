"""Quickstart example for boltscraper Python SDK.

Demonstrates real-time Google Maps search in ~2-4 seconds.
Requires BOLTSCRAPER_API_KEY environment variable or passing api_key directly.
"""

import os
from boltscraper import BoltScraper

def main():
    api_key = os.environ.get("BOLTSCRAPER_API_KEY", "YOUR_API_KEY_HERE")
    client = BoltScraper(api_key=api_key)

    print("Searching Google Maps for 'Coffee shops in Seattle'...")
    results = client.maps.search("Coffee shops in Seattle", page=1)

    pagination = results.get("pagination", {})
    total = pagination.get("total_results", len(results.get("data", [])))
    print(f"\nFound {total} places (showing page {pagination.get('page', 1)}):\n")

    for place in results.get("data", []):
        name = place.get("Name", "N/A")
        phone = place.get("Phone", "N/A")
        phone_type = place.get("Phone Type", "N/A")
        website = place.get("Website", "N/A")
        rating = place.get("Average Rating", "N/A")
        reviews = place.get("Review Count", "0")
        address = place.get("Full Address", "N/A")

        print(f"☕ {name}")
        print(f"   Address: {address}")
        print(f"   Phone:   {phone} ({phone_type})")
        print(f"   Website: {website}")
        print(f"   Rating:  ★ {rating} ({reviews} reviews)")
        print("-" * 50)

if __name__ == "__main__":
    main()
