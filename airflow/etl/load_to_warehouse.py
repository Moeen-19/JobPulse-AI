# etl/load_to_warehouse.py
import psycopg2
import logging
import os
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# --- Connection Settings ---
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
}

# --- Helper Function ---
def execute_sql_file(conn, file_path):
    with open(file_path, "r") as file:
        sql = file.read()
    with conn.cursor() as cur:
        cur.execute(sql)
        conn.commit()
    logging.info(f"✅ Executed: {os.path.basename(file_path)}")

# --- Main Loader Function ---
def load_to_warehouse(schema_path, load_sql_path):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        logging.info("✅ Connected to PostgreSQL")

        # Run schema first
        execute_sql_file(conn, schema_path)

        # Then run load_jobs.sql to insert data
        execute_sql_file(conn, load_sql_path)

        logging.info("🎯 Successfully loaded cleaned jobs data into warehouse.")

    except Exception as e:
        logging.error(f"❌ Error loading data: {e}")
        raise
    finally:
        conn.close()
