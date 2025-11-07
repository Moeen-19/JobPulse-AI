# naukri_scraper.py
import requests
from bs4 import BeautifulSoup
import json
import time
import re
import logging
from datetime import datetime, timezone
import os
from typing import Dict, List, Any, Optional

import pandas as pd

# --- Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("naukri_scraper")


class NaukriScraper:
    BASE_URL = "https://www.naukri.com"
    SEARCH_URL = BASE_URL + "/{}-jobs-{}"

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }

    def __init__(self, delay_between_requests: float = 2.0, max_pages: int = 10):
        self.delay = delay_between_requests
        self.max_pages = max_pages
        self.skill_keywords = [
            "python", "java", "c++", "c#", "javascript", "typescript", "react",
            "angular", "vue", "node", "flask", "django", "spring", "fastapi",
            "sql", "mongodb", "postgresql", "pandas", "numpy", "spark",
            "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
            "git", "linux", "rest api", "agile", "ml", "data science",
            "etl", "marketing", "design", "seo", "figma"
        ]

    # -------------------- HELPERS -------------------- #
    def _extract_skills(self, text: str) -> List[str]:
        if not text:
            return []
        text = text.lower()
        return sorted({skill for skill in self.skill_keywords if re.search(rf"\b{re.escape(skill)}\b", text)})

    def _parse_job_card(self, card) -> Dict[str, Any]:
        title_tag = card.find("a", class_="title")
        company_tag = card.find("a", class_="subTitle")
        desc_tag = card.find("div", class_="job-description")
        location_tag = card.find("li", class_="location")
        salary_tag = card.find("li", class_="salary")
        date_tag = card.find("span", class_="job-post-day")

        # --- Extract fields safely ---
        job_title = title_tag.text.strip() if title_tag else "N/A"
        job_url = title_tag["href"].strip() if title_tag and title_tag.has_attr("href") else None
        company_name = company_tag.text.strip() if company_tag else "Unknown"
        description = desc_tag.text.strip() if desc_tag else ""
        location = location_tag.text.strip() if location_tag else "Remote/Not specified"
        salary = salary_tag.text.strip() if salary_tag else None
        published = date_tag.text.strip() if date_tag else None
        skills = self._extract_skills(description)

        # standard schema (consistent with other scrapers)
        return {
            "job_id": job_url or f"naukri-{abs(hash(job_title + company_name))}",
            "title": job_title,
            "company_name": company_name,
            "location": location,
            "url": job_url,
            "description": description,
            "skills": skills,
            "salary": salary,
            "published": published,
            "source": "naukri",
            "scraped_date": datetime.now(timezone.utc).isoformat()
        }

    def _fetch_page(self, role: str, page: int) -> List[Dict[str, Any]]:
        role_prefix = f"{role}-" if role else ""
        url = self.SEARCH_URL.format(role_prefix, page)
        logger.info(f"Fetching page {page} for role '{role}' → {url}")
        resp = requests.get(url, headers=self.HEADERS, timeout=10)
        if resp.status_code != 200:
            logger.warning(f"Failed to fetch page {page}: {resp.status_code}")
            return []
        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.find_all("article", class_="jobTuple")
        return [self._parse_job_card(card) for card in cards]

    # -------------------- MAIN SCRAPER -------------------- #
    def fetch_all_jobs(
        self,
        role: str = "",
        meta_dir: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch job postings for a given role (resumable).
        Returns: list of standardized job dicts (does NOT write files).
        Metadata checkpoint is stored/updated in meta_dir.
        """

        if meta_dir is None:
            meta_dir = os.path.join(os.path.dirname(__file__), "meta_data_checkpoints")
        os.makedirs(meta_dir, exist_ok=True)
        meta_path = os.path.join(meta_dir, "naukri_ingestion_meta.json")

        # load checkpoint (last page resumed)
        last_page = 1
        if os.path.exists(meta_path):
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                    last_page = int(meta.get("last_page", 1))
            except Exception:
                last_page = 1

        logger.info(f"Resuming from page {last_page} for role '{role}'")

        all_jobs: List[Dict[str, Any]] = []
        for page in range(last_page, self.max_pages + 1):
            try:
                jobs = self._fetch_page(role, page)
                if not jobs:
                    logger.info("No jobs found on page; stopping early.")
                    break

                all_jobs.extend(jobs)
                logger.info(f"Fetched {len(jobs)} jobs from page {page}")
                time.sleep(self.delay)

                # update checkpoint (last_page next)
                try:
                    with open(meta_path, "w", encoding="utf-8") as f:
                        json.dump({
                            "last_page": page + 1,
                            "last_updated": datetime.now(timezone.utc).isoformat(),
                            "total_jobs": len(all_jobs)
                        }, f, indent=2)
                except Exception as e:
                    logger.warning(f"Failed to write meta checkpoint: {e}")

            except Exception as e:
                logger.error(f"Error on page {page}: {e}")
                break

        logger.info(f"✅ Completed scraping {len(all_jobs)} jobs for role '{role}'.")
        return all_jobs


# -------------------- WRAPPER FUNCTION -------------------- #
def scrape_naukri(output_path: str, role: str = "") -> Optional[str]:
    """
    Airflow wrapper:
    - Calls NaukriScraper.fetch_all_jobs(role, meta_dir)
    - Converts results to a DataFrame and saves CSV to output_path
    - Returns the output_path (or None if no data)
    """
    meta_dir = os.path.join(os.path.dirname(__file__), "meta_data_checkpoints")

    scraper = NaukriScraper(delay_between_requests=2.0, max_pages=5)
    jobs = scraper.fetch_all_jobs(role=role, meta_dir=meta_dir)

    df = pd.DataFrame(jobs)
    if df.empty:
        logger.warning("No data fetched from Naukri.")
        return None
    
    df.to_csv(output_path, index=False)
    logger.info(f"✅ Saved {len(df)} rows to {output_path}")
    return output_path