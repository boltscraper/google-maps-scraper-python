# Google Maps Scraper Python API (`boltscraper`)

[![PyPI version](https://img.shields.io/pypi/v/boltscraper.svg?color=ff4747)](https://pypi.org/project/boltscraper/)
[![Python versions](https://img.shields.io/pypi/pyversions/boltscraper.svg)](https://pypi.org/project/boltscraper/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Free Tier](https://img.shields.io/badge/Free%20Credits-1%2C000%20Leads%2Fmo-green.svg)](https://app.boltscraper.com)

The official Python SDK for **[Bolt Scraper](https://boltscraper.com)** — fast, proxy-free, cloud-native data extraction for **Google Maps listings**, **Google customer reviews**, and **company websites**.

Extract **60+ business attributes** (names, phones, direct emails, social profiles, hours, ratings, coordinates) without browser automation overhead, CAPTCHA hassles, or IP bans.

---

## Why Developers Use `boltscraper`

| Feature | Selenium / BeautifulSoup | Google Places API (New) | Bolt Scraper Python SDK |
| :--- | :--- | :--- | :--- |
| **Speed & Setup** | Slow browser overhead | Complex GCP console setup | **5 lines of Python code** |
| **IP Bans & CAPTCHAs** | Frequent blocks & CAPTCHAs | None (metered API) | **0% bans** (automatic proxy rotation) |
| **Direct Emails** | Requires custom scraping | **Not offered (0% returned)** | **Included** (crawls company websites) |
| **Customer Reviews** | DOM fragile / breaks | Max 5 reviews only | **Extracts all 5,000+ reviews** |
| **Data Storage** | Unstructured HTML | 30-day cache ban | **100% owned indefinitely** |
| **Pricing** | Proxy costs ($50+/mo) | **$32 – $65+ per 1k requests** | **$0 Free tier** ($0.38 / 1k on paid) |

---

## Installation

```bash
pip install boltscraper
```

Requires Python 3.8+.

---

## Quickstart

Get your free API key at **[app.boltscraper.com](https://app.boltscraper.com)** (includes 1,000 free lead credits every month).

```python
from boltscraper import BoltScraper

# Initialize client (or set BOLTSCRAPER_API_KEY environment variable)
client = BoltScraper(api_key="bs_live_YOUR_API_KEY")

# 1. Real-time Google Maps search (~2-4 seconds)
results = client.maps.search("Coffee shops in Seattle", page=1)

print(f"Found {results['pagination']['total_results']} places:")
for place in results["data"]:
    print(f"Name:    {place['Name']}")
    print(f"Phone:   {place['Phone']} ({place['Phone Type']})")
    print(f"Website: {place['Website']}")
    print(f"Rating:  {place['Average Rating']} ({place['Review Count']} reviews)")
    print("-" * 40)
```

---

## Core Capabilities & Examples

### 1. Synchronous Real-time Maps Search
Perfect for search bars, AI agent tool calling, and live user queries. Returns instant JSON without background polling:

```python
response = client.maps.search(
    keyword="Dentists in Austin, TX",
    page=1,
    hl="en"
)

for lead in response["data"]:
    print(lead["Name"], lead["Full Address"], lead["Coordinates"])
```

### 2. Large-Scale Asynchronous Batch Jobs
Scrape entire cities or hundreds of queries with automatic website email enrichment and Ultra Mode:

```python
# Launch background scraping job
job = client.maps.create_job(
    keywords=["Roofers in Miami, FL", "Solar contractors in Miami, FL"],
    title="Miami Home Services",
    scrape_websites=True,   # Crawls company websites for direct emails & socials
    ultra_mode=True,        # Multi-point grid scan for up to 3x more results
    webhook_url="https://your-crm.com/api/webhooks/bolt"
)

job_id = job["job_id"]
print(f"Started job: {job_id}")

# Check status
status = client.maps.get_job(job_id)
print(f"Status: {status['status']} — Extracted: {status['total_leads']} leads")

# Download CSV dataset upon completion
csv_bytes = client.maps.download_csv(job_id)
with open("miami_leads.csv", "wb") as f:
    f.write(csv_bytes)
```

### 3. Google Reviews Extraction (Without OAuth)
Bypass Google's 5-review API limitation and extract all customer reviews, ratings, reviewer levels, and owner responses:

```python
# Synchronously extract up to 5,000+ reviews for any Google Place ID
reviews_data = client.reviews.search(
    place_id="ChIJb8Jg9q-1RIYRAxvq_mZ0gXY",
    max_reviews=500,
    sort="newest"  # 'newest', 'most_relevant', 'highest_rating', 'lowest_rating'
)

for review in reviews_data.get("reviews", []):
    print(f"★ {review['rating']} by {review['reviewer_name']}")
    print(f"Text: {review['text']}")
    print(f"Date: {review['date']}")
```

### 4. Website Email & Social Link Enrichment
Turn raw domain lists into enriched B2B contact lists:

```python
# Instant single-domain enrichment (crawls /contact, /about, /team subpages)
company = client.website.scrape("https://example.com")

print("Direct Emails:", company.get("emails", []))
print("Phone Numbers:", company.get("phones", []))
print("Social Links: ", company.get("socials", {}))
```

### 5. Webhook Signature Verification
Verify incoming webhook payloads with HMAC SHA-256 to ensure authenticity:

```python
from boltscraper import WebhooksResource

# In your FastAPI / Flask / Django webhook handler:
is_valid = WebhooksResource.verify_signature(
    raw_body=request.body,
    signature_header=request.headers.get("X-Bolt-Signature"),
    secret="YOUR_WEBHOOK_SECRET"
)

if not is_valid:
    return "Invalid signature", 401
```

---

## 60+ Extracted Data Points

Each Google Maps listing returns comprehensive, production-ready structured data:

* **Identity**: Business Name, Category, Sub-categories, Google Category IDs, Place ID, CID, KGMID, Feature ID.
* **Location**: Full Address, Street Address, City, State, ZIP/Postal Code, Country, Municipality, Latitude, Longitude, Timezone.
* **Contact**: Formatted Phone, Phone Type (Mobile, Landline, VOIP), International Phone, Phone URI (`tel:`), Website URL, Domain.
* **Enrichment**: Direct Emails discovered from company websites, Social Media URLs (LinkedIn, Facebook, Instagram, Twitter/X, YouTube).
* **Reputation & Hours**: Star Rating, Total Reviews Count, Review URL, Operating Status (Open, Closed), Opening Hours (Monday–Sunday schedules).
* **Media Assets**: Logo URL, Main Photo URL, Photos Page URL, Favicon URL.

---

## Rate Limits & Error Handling

All requests are rate-limited to **60 requests per minute** per API key. The SDK automatically handles `429 Too Many Requests` responses with exponential backoff using the server's `Retry-After` header.

```python
from boltscraper.exceptions import (
    AuthenticationError,
    QuotaExceededError,
    RateLimitError,
    BoltScraperError
)

try:
    results = client.maps.search("Plumbers Denver")
except AuthenticationError:
    print("Invalid API key. Check https://app.boltscraper.com")
except QuotaExceededError:
    print("Monthly quota exhausted. Upgrade plan at https://boltscraper.com/pricing")
except RateLimitError as e:
    print(f"Rate limited. Reset in {e.retry_after} seconds.")
except BoltScraperError as e:
    print(f"API Error ({e.status_code}): {e.message}")
```

---

## Documentation & Resources

* **Documentation Portal**: [https://boltscraper.com/api/](https://boltscraper.com/api/)
* **In-Depth Guides & Tutorials**: [https://boltscraper.com/blogs/](https://boltscraper.com/blogs/)
* **Pricing Calculator**: [Google Places API Cost Calculator](https://boltscraper.com/tools/google-places-api-pricing-calculator/)
* **Sign Up (1,000 Free Leads/mo)**: [https://app.boltscraper.com](https://app.boltscraper.com)

---

## License

MIT License. Copyright (c) 2026 Bolt Scraper.
