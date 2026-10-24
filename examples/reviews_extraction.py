"""Google Reviews extraction example for boltscraper Python SDK.

Demonstrates extracting customer reviews and ratings without OAuth.
"""

import os
from boltscraper import BoltScraper

def main():
    api_key = os.environ.get("BOLTSCRAPER_API_KEY", "YOUR_API_KEY_HERE")
    client = BoltScraper(api_key=api_key)

    # Example Place ID
    place_id = "ChIJ-bfVTh8VkFQRDZLQnmqHgSg"

    print(f"Fetching customer reviews for Place ID: {place_id}...")
    result = client.reviews.search(
        place_id=place_id,
        max_reviews=50,
        sort="newest"
    )

    reviews = result.get("data") or result.get("reviews", [])
    print(f"\nFetched {len(reviews)} reviews:\n")

    for r in reviews:
        stars_val = r.get("stars") or r.get("rating", 0)
        stars = "★" * int(stars_val)
        author = r.get("reviewer", {}).get("name") if isinstance(r.get("reviewer"), dict) else r.get("reviewer_name", "Anonymous")
        date = r.get("review_date_relative") or r.get("date", "N/A")
        text = r.get("review_text") or r.get("text", "(No text)")

        print(f"{stars} by {author} ({date})")
        print(f"\"{text[:140]}...\"" if len(text) > 140 else f"\"{text}\"")

        owner_resp = r.get("owner_response")
        if isinstance(owner_resp, dict) and owner_resp.get("text"):
            print(f"   ↳ Owner response: {owner_resp['text'][:100]}...")
        elif isinstance(owner_resp, str):
            print(f"   ↳ Owner response: {owner_resp[:100]}...")
        print("-" * 50)

if __name__ == "__main__":
    main()
