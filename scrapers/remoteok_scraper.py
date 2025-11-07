import requests
import json
import time
import logging
import re
import os
import pandas as pd
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("remoteok_scraper")


class RemoteScraper:
    BASE_URL = "https://remoteok.com/api"

    def __init__(self, delay_between_requests: float = 1.0, max_retries: int = 3):
        self.delay = delay_between_requests
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            "Accept": "application/json",
        })

        # Skill keywords for analytics
        self.skill_keywords = [
            "python", "java", "c++", "c#", "javascript", "typescript",
            "react", "angular", "vue", "node", "flask", "django", "spring",
            "fastapi", "sql", "mongodb", "postgresql", "pandas", "numpy",
            "spark", "aws", "azure", "gcp", "docker", "kubernetes",
            "terraform", "git", "linux", "rest api", "agile",
            "machine learning", "data engineering", "etl", "api"
        ]

    # -------------------- INTERNAL HELPERS -------------------- #
    def _make_request(self) -> Optional[List[Dict[str, Any]]]:
        """Make GET request to RemoteOK API with retry + delay."""
        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info("Fetching data from RemoteOK API...")
                resp = self.session.get(self.BASE_URL, timeout=30)
                resp.raise_for_status()
                data = resp.json()

                # RemoteOK includes a notice as first item
                if data and isinstance(data, list) and "notice" in data[0]:
                    data = data[1:]
                return data
            except requests.RequestException as e:
                logger.warning(f"[Attempt {attempt}/{self.max_retries}] Request error: {e}")
                time.sleep(self.delay * attempt)
        logger.error("Failed to fetch data after retries.")
        return None

    def _extract_skills(self, text: str) -> List[str]:
        """Extracts skills from description or tags using regex match."""
        if not text:
            return []
        text_lower = text.lower()
        found = {skill for skill in self.skill_keywords if re.search(rf"\b{re.escape(skill)}\b", text_lower)}
        return sorted(found)

    def _process_job(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """Standardize and enrich RemoteOK job record."""
        description = job.get("description", "") or ""
        tags = job.get("tags", [])
        tag_list = tags if isinstance(tags, list) else []

        # Extract skills from both tags and description
        skills = list(set(self._extract_skills(description) + [t.lower() for t in tag_list]))

        job_data = {
            "id": job.get("id"),
            "position": job.get("position"),
            "company": job.get("company"),
            "location": job.get("location") or "Remote",
            "url": job.get("url"),
            "description": description,
            "skills": skills,
            "salary": job.get("salary"),
            "date": job.get("date"),
        }

        return {
            "job_id": job_data["id"],
            "title": job_data["position"],
            "company_name": job_data["company"],
            "location": job_data["location"],
            "url": job_data["url"],
            "description": job_data["description"],
            "skills": job_data["skills"],
            "salary": job_data["salary"],
            "published": job_data["date"],
            "source": "remoteok",
            "scraped_date": datetime.now(timezone.utc).isoformat()
        }

    # -------------------- MAIN FUNCTION -------------------- #
    def fetch_all_jobs(self) -> pd.DataFrame:
        """Fetch all job postings from RemoteOK and return as DataFrame."""
        meta_dir = os.path.join(os.path.dirname(__file__), "meta_data_checkpoints")
        os.makedirs(meta_dir, exist_ok=True)
        meta_path = os.path.join(meta_dir, "remoteok_ingestion_meta.json")

        # Load metadata to resume
        last_job_ids = set()
        if os.path.exists(meta_path):
            try:
                with open(meta_path, "r") as f:
                    meta = json.load(f)
                    last_job_ids = set(meta.get("last_job_ids", []))
            except Exception:
                last_job_ids = set()

        logger.info(f"Resuming ingestion — {len(last_job_ids)} jobs previously stored.")

        all_jobs = self._make_request()
        if not all_jobs:
            logger.error("No jobs received from API.")
            return pd.DataFrame()

        total_fetched = 0
        new_jobs = []
        processed_jobs = []

        for job in all_jobs:
            job_id = str(job.get("id"))
            if job_id in last_job_ids:
                continue  # skip duplicates

            try:
                processed = self._process_job(job)
                processed_jobs.append(processed)
                new_jobs.append(job_id)
                total_fetched += 1
            except Exception as e:
                logger.error(f"Error processing job {job_id}: {e}")

        logger.info(f"✅ Processed {total_fetched} new jobs from RemoteOK.")

        # Update metadata
        all_job_ids = list(last_job_ids.union(set(new_jobs)))
        with open(meta_path, "w") as f:
            json.dump({
                "last_job_ids": all_job_ids[-10000:],
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "total_jobs": len(all_job_ids)
            }, f, indent=2)

        df = pd.DataFrame(processed_jobs)
        return df


# -------------------- WRAPPER FUNCTION -------------------- #
def scrape_remoteok(output_path: str):
    """Wrapper function for Airflow DAG."""
    scraper = RemoteScraper(delay_between_requests=1.0)
    df = scraper.fetch_all_jobs()
    if df.empty:
        logger.warning("No data fetched from RemoteOK.")
        return None
    df.to_csv(output_path, index=False)
    logger.info(f"✅ Saved data to {output_path}")
    return output_path