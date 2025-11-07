import os
import logging
import pandas as pd
from data_processing.clean_transform import JobDataProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("etl.data_cleaner")


def clean_job_data(data_dir: str) -> str:
    """
    Combine, clean, and transform raw job data from multiple job boards.

    Args:
        data_dir (str): Path to directory containing raw job CSV files.

    Returns:
        str: Path to the final cleaned CSV file.
    """
    logger.info(f"Starting job data cleaning from directory: {data_dir}")

    # Define expected input CSV files (produced by scrapers)
    input_files = [
        "data/processed/remoteok_jobs.csv",
        "data/processed/weworkremotely_jobs.csv",
        "data/processed/y_combinator_jobs.csv",
        "data/processed/naukri_jobs.csv"
    ]

    all_dfs = []
    for file_name in input_files:
        file_path = os.path.join(data_dir, file_name)
        if os.path.exists(file_path):
            try:
                logger.info(f"Reading {file_path}")
                df = pd.read_csv(file_path)
                all_dfs.append(df)
            except Exception as e:
                logger.warning(f"⚠️ Error reading {file_name}: {e}")
        else:
            logger.warning(f"⚠️ Missing file: {file_path}")

    if not all_dfs:
        logger.error("❌ No job data found! Did the scrapers run?")
        raise FileNotFoundError("No input job data found for processing.")

    # Combine all job data
    combined_df = pd.concat(all_dfs, ignore_index=True)
    logger.info(f"Combined {len(combined_df)} total job records from {len(all_dfs)} sources.")

    # Initialize processor and process combined data
    processor = JobDataProcessor()
    df_cleaned = processor.process_jobs(combined_df)

    # Ensure output directory exists
    os.makedirs(data_dir, exist_ok=True)
    output_path = os.path.join(data_dir, "jobs_processed.csv")

    df_cleaned.to_csv(output_path, index=False)
    logger.info(f"✅ Processed {len(df_cleaned)} jobs → {output_path}")

    return output_path