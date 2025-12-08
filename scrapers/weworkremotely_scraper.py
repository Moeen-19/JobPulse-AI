import feedparser
import pandas as pd
import json
import time
import logging
import re
import os
from datetime import datetime, timezone
from typing import Dict, List, Any

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("weworkremotely_scraper")


class WeWorkRemotelyScraper:
    """
    RSS Feed Scraper for WeWorkRemotely job listings.
    Legal and public — no authentication required.
    """

    BASE_FEEDS = {
        "programming": "https://weworkremotely.com/categories/remote-programming-jobs.rss",
        "design": "https://weworkremotely.com/categories/remote-design-jobs.rss",
        "marketing": "https://weworkremotely.com/categories/remote-marketing-jobs.rss",
        "sales": "https://weworkremotely.com/categories/remote-sales-and-marketing-jobs.rss",
        "support": "https://weworkremotely.com/categories/remote-customer-support-jobs.rss",
        "management": "https://weworkremotely.com/categories/remote-management-and-finance-jobs.rss",
    }

    def __init__(self, delay_between_requests: float = 2.0):
        self.delay = delay_between_requests
        self.skill_keywords = [
            "python", "java", "c++", "c#", "javascript", "typescript", "react",
            "angular", "vue", "node", "flask", "django", "spring", "fastapi",
            "sql", "mongodb", "postgresql", "pandas", "numpy", "spark",
            "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
            "git", "linux", "rest api", "agile", "machine learning",
            "data engineering", "etl", "marketing", "design", "seo", "figma"
        ]

    # -------------------- INTERNAL HELPERS -------------------- #
    def _extract_skills(self, text: str) -> List[str]:
        if not text:
            return []
        text_lower = text.lower()
        found = {skill for skill in self.skill_keywords if re.search(rf"\b{re.escape(skill)}\b", text_lower)}
        return sorted(found)

    def _extract_company(self, title: str) -> str:
        if "—" in title:
            return title.split("—")[-1].strip()
        elif "-" in title:
            return title.split("-")[-1].strip()
        return "Unknown"

    def _process_entry(self, job: Dict[str, Any]) -> Dict[str, Any]:
        description = job.get("description", "")
        skills = self._extract_skills(description)

        return {
            "job_id": job.get("id"),
            "title": job.get("position"),
            "company_name": job.get("company"),
            "location": job.get("location"),
            "url": job.get("url"),
            "description": description,
            "skills": skills,
            "salary": job.get("salary"),
            "published": job.get("date"),
            "source": "weworkremotely",
            "scraped_date": datetime.now(timezone.utc).isoformat()
        }

    # -------------------- MAIN FUNCTION -------------------- #
    def fetch_all_jobs(self, meta_dir: str) -> List[Dict[str, Any]]:
        """Fetch all jobs and return a list of job dicts. Metadata checkpoint is saved in meta_dir."""
        os.makedirs(meta_dir, exist_ok=True)
        meta_path = os.path.join(meta_dir, "weworkremotely_ingestion_meta.json")

        # Load last ingested job IDs
        last_job_ids = set()
        if os.path.exists(meta_path):
            try:
                with open(meta_path, "r") as f:
                    meta = json.load(f)
                    last_job_ids = set(meta.get("last_job_ids", []))
            except Exception:
                last_job_ids = set()

        logger.info(f"Resuming ingestion — {len(last_job_ids)} previously saved job IDs found.")

        new_jobs = []
        processed_jobs = []

        for category, feed_url in self.BASE_FEEDS.items():
            logger.info(f"Fetching category: {category} ({feed_url})")
            feed = feedparser.parse(feed_url)
            time.sleep(self.delay)

            for entry in feed.entries:
                job_id = entry.get("id") or entry.get("link")
                if not job_id or job_id in last_job_ids:
                    continue

                # --- Construct job dict consistent with other scrapers ---
                job = {
                    "id": job_id,
                    "position": entry.get("title"),
                    "company": entry.get("author") or self._extract_company(entry.get("title", "")),
                    "location": entry.get("location", "Remote"),  # fallback to 'Remote' if not present,
                    "url": entry.get("link"),
                    "description": entry.get("summary", ""),
                    "salary": None,
                    "date": entry.get("published", "")
                }

                try:
                    processed_jobs.append(self._process_entry(job))
                    new_jobs.append(job_id)
                except Exception as e:
                    logger.error(f"Error processing entry {job_id}: {e}")

        # --- Save metadata checkpoint ---
        all_job_ids = list(last_job_ids.union(set(new_jobs)))
        with open(meta_path, "w") as f:
            json.dump({
                "last_job_ids": all_job_ids[-10000:],
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "total_jobs": len(all_job_ids)
            }, f, indent=2)

        logger.info(f"✅ Ingestion completed successfully — {len(processed_jobs)} jobs fetched.")
        return processed_jobs


# Standalone function for Airflow DAG
def scrape_weworkremotely(output_path: str):
    """
    Wrapper function for Airflow DAG.
    - Runs the WeWorkRemotely scraper.
    - Saves output to CSV in airflow/data/processed/.
    - Returns the output_path.
    """
    meta_dir = os.path.join(os.path.dirname(__file__), "..", "scrapers", "meta_data_checkpoints")
    scraper = WeWorkRemotelyScraper(delay_between_requests=1.5)

    jobs = scraper.fetch_all_jobs(meta_dir=meta_dir)
    df = pd.DataFrame(jobs)
    if df.empty:
        logger.warning("No data fetched from WeWorkRemotely.")
        return None
    
    df.to_csv(output_path, index=False)
    return output_path