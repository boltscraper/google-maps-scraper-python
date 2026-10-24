"""Website enrichment example for boltscraper Python SDK.

Demonstrates extracting direct business emails, telephone numbers, and social media
profiles from any corporate or local business domain without manual scraping.
"""

import os
from boltscraper import BoltScraper

def main():
    api_key = os.environ.get("BOLTSCRAPER_API_KEY", "YOUR_API_KEY_HERE")
    client = BoltScraper(api_key=api_key)

    domains = ["https://stripe.com", "https://github.com"]

    for url in domains:
        print(f"\nEnriching website domain: {url}...")
        res = client.website.scrape(url)
        info = res.get("data", res)

        print(f"Company:      {info.get('title', 'N/A')}")
        print(f"Emails found: {info.get('emails', [])}")
        print(f"Phone lines:  {info.get('phones', [])}")
        socials = info.get("social_links") or info.get("socials", {})
        print(f"Socials:      {socials}")

if __name__ == "__main__":
    main()
