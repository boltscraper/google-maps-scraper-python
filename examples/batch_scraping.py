"""Batch job example for boltscraper Python SDK.

Demonstrates launching an asynchronous background job with website email enrichment,
checking status, and downloading the full CSV dataset.
"""

import os
import time
from boltscraper import BoltScraper

def main():
    api_key = os.environ.get("BOLTSCRAPER_API_KEY", "YOUR_API_KEY_HERE")
    client = BoltScraper(api_key=api_key)

    print("Launching batch scraping job...")
    job = client.maps.create_job(
        keywords=["HVAC repair in Austin, TX", "Roofing contractors in Austin, TX"],
        title="Austin Contractors Q4",
        scrape_websites=True,   # Crawl company websites for direct emails & socials
        ultra_mode=True,        # Multi-point grid scan for maximum lead density
    )

    job_id = job.get("job_id")
    print(f"Created Job ID: {job_id}")

    # Poll status until completed
    while True:
        status_info = client.maps.get_job(job_id)
        current_status = status_info.get("status", "unknown")
        total_leads = status_info.get("total_leads", 0)
        print(f"Status: {current_status} | Extracted leads: {total_leads}")

        if current_status in ("completed", "finished", "done"):
            print("\nJob completed successfully!")
            break
        elif current_status in ("failed", "error", "stopped"):
            print(f"\nJob ended with status: {current_status}")
            return

        time.sleep(10)

    # Download CSV dataset
    print("Downloading results as CSV...")
    csv_bytes = client.maps.download_csv(job_id)
    output_filename = f"leads_{job_id}.csv"
    with open(output_filename, "wb") as f:
        f.write(csv_bytes)
    print(f"Saved results to {output_filename}")

if __name__ == "__main__":
    main()
