"""Google Reviews extraction example for boltscraper Python SDK.

Demonstrates extracting up to thousands of customer reviews without OAuth.
"""

import os
from boltscraper import BoltScraper

def main():
    api_key = os.environ.get("BOLTSCRAPER_API_KEY", "YOUR_API_KEY_HERE")
    client = BoltScraper(api_key=api_key)

    # Example Place ID: Space Needle, Seattle
    place_id = "ChIJ-bfVTh8VkFQRDZLQnmqHgSg"

    print(f"Fetching customer reviews for Place ID: {place_id}...")
    result = client.reviews.search(
        place_id=place_id,
        max_reviews=50,
        sort="newest"
    )

    reviews = result.get("reviews", [])
    print(f"\nFetched {len(reviews)} reviews:\n")

    for r in reviews:
        stars = "★" * int(r.get("rating", 0))
        author = r.get("reviewer_name", "Anonymous")
        date = r.get("date", "N/A")
        text = r.get("text", "(No text)")

        print(f"{stars} by {author} ({date})")
        print(f"\"{text[:140]}...\"" if len(text) > 140 else f"\"{text}\"")
        if r.get("owner_response"):
            print(f"   ↳ Owner response: {r['owner_response'][:100]}...")
        print("-" * 50)

if __name__ == "__main__":
    main()
