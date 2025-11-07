import requests
import json
import os
import re
import time
import logging
import pandas as pd
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("y_combinator_scraper")


class YCombinatorScraper:
    BASE_URL = "https://www.workatastartup.com/api/v1/jobs"

    def __init__(self, delay_between_requests: float = 2.0):
        self.delay = delay_between_requests
        self.skill_keywords = [
            "python", "java", "c++", "c#", "javascript", "typescript", "react",
            "angular", "node", "flask", "django", "spring", "fastapi", "sql",
            "mongodb", "postgresql", "pandas", "numpy", "spark", "aws", "azure",
            "gcp", "docker", "kubernetes", "terraform", "git", "linux",
            "rest api", "agile", "machine learning", "data engineering", "etl"
        ]

    # -------------------- Core Extraction -------------------- #
    def _make_request(self) -> Optional[List[Dict[str, Any]]]:
        """Fetch all jobs from YC Work at a Startup API."""
        try:
            resp = requests.get(self.BASE_URL, timeout=30)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None

    def _extract_skills(self, text: str) -> List[str]:
        """Extract known skills from job description."""
        text_lower = text.lower() if text else ""
        return [kw for kw in self.skill_keywords if re.search(rf"\b{kw}\b", text_lower)]

    def _process_job(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """Convert raw YC job object into standardized format."""
        description = job.get("description", "") or job.get("company_description", "")
        skills = self._extract_skills(description)
        return {
            "job_id": job.get("id"),
            "title": job.get("title"),
            "company_name": job.get("company_name"),
            "location": job.get("location") or "Remote/Not specified",
            "url": f"https://www.workatastartup.com/jobs/{job.get('id')}",
            "description": description,
            "skills": skills,
            "salary": job.get("compensation", {}).get("salary"),
            "published": job.get("published_at"),
            "source": "y_combinator",
            "scraped_date": datetime.now(timezone.utc).isoformat(),
        }

    # -------------------- Incremental Logic -------------------- #
    def fetch_all_jobs(self, meta_dir: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Fetch job postings with checkpointing logic.
        Returns a list[dict] (no file I/O). Metadata checkpoint saved in meta_dir.
        """
        if meta_dir is None:
            meta_dir = os.path.join(os.path.dirname(__file__), "meta_data_checkpoints")
        os.makedirs(meta_dir, exist_ok=True)
        meta_path = os.path.join(meta_dir, "ycombinator_ingestion_meta.json")

        last_job_id = None
        if os.path.exists(meta_path):
            try:
                with open(meta_path, "r") as f:
                    meta = json.load(f)
                    last_job_id = meta.get("last_job_id")
            except Exception:
                pass

        logger.info(f"Resuming scraping from last job ID: {last_job_id or 'start'}")

        data = self._make_request()
        if not data:
            logger.warning("No jobs fetched from YC API.")
            return []

        new_jobs: List[Dict[str, Any]] = []

        # Sort by published date descending
        data_sorted = sorted(data, key=lambda j: j.get("published_at") or "", reverse=True)

        for job in data_sorted:
            job_id = job.get("id")
            if str(job_id) == str(last_job_id):
                logger.info("Reached previously scraped job, stopping early.")
                break

            processed = self._process_job(job)
            new_jobs.append(processed)

        if not new_jobs:
            logger.info("No new jobs found since last run.")
            return []

        # Save checkpoint (latest job)
        last_scraped = new_jobs[0]["job_id"]
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump({
                "last_job_id": last_scraped,
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "total_jobs": len(new_jobs)
            }, f, indent=2)

        logger.info(f"✅ Scraped {len(new_jobs)} new jobs. Last job ID checkpoint: {last_scraped}")
        time.sleep(self.delay)
        return new_jobs

# -------------------- DAG WRAPPER -------------------- #
def scrape_ycombinator(output_path: str) -> Optional[str]:
    """
    Wrapper function called by Airflow DAG.
    Fetches jobs, saves them to CSV, and returns output_path.
    """
    scraper = YCombinatorScraper(delay_between_requests=2.0)
    meta_dir = os.path.join(os.path.dirname(__file__), "meta_data_checkpoints")
    jobs = scraper.fetch_all_jobs(meta_dir=meta_dir)

    if not jobs:
        logger.warning("No jobs fetched from YCombinator.")
        return None

    df = pd.DataFrame(jobs)
    if "skills" in df.columns:
        df["skills"] = df["skills"].apply(lambda s: ";".join(s) if isinstance(s, list) else s)

    df.to_csv(output_path, index=False, encoding="utf-8")
    logger.info(f"✅ Saved {len(df)} rows to {output_path}")
    return output_path