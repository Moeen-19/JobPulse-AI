import os
import sys
import logging
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from api.ml.forecasting import run_forecast
from api.ml.correlation import run_correlation

# Add project root for relative imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from scrapers.weworkremotely_scraper import scrape_weworkremotely
from scrapers.naukri_scraper import scrape_naukri
from scrapers.y_combinator_scraper import scrape_ycombinator
from scrapers.remoteok_scraper import scrape_remoteok
from etl.data_cleaner import clean_job_data
from etl.load_to_warehouse import load_to_warehouse

# --- CONFIG ---
data_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
os.makedirs(data_dir, exist_ok=True)

# --- DAG DEFAULT ARGS ---
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'job_ingestion_pipeline',
    default_args=default_args,
    description='ETL pipeline for scraping and loading job data',
    schedule_interval='@daily',
    start_date=datetime(2025, 10, 1),
    catchup=False,
)

# --- PYTHON TASKS: Scraping + Cleaning ---

scrape_weworkremotely_task = PythonOperator(
    task_id='scrape_weworkremotely',
    python_callable=scrape_weworkremotely,
    op_kwargs={'output_path': f"{data_dir}/weworkremotely_raw.csv"},
    dag=dag,
)

scrape_naukri_task = PythonOperator(
    task_id='scrape_naukri',
    python_callable=scrape_naukri,
    op_kwargs={'output_path': f"{data_dir}/naukri_raw.csv"},
    dag=dag,
)

scrape_yc_task = PythonOperator(
    task_id='scrape_y_combinator',
    python_callable=scrape_ycombinator,
    op_kwargs={'output_path': f"{data_dir}/y_combinator_raw.csv"},
    dag=dag,
)

scrape_remoteok_task = PythonOperator(
    task_id='scrape_remoteok',
    python_callable=scrape_remoteok,
    op_kwargs={'output_path': f"{data_dir}/remoteok_raw.csv"},
    dag=dag,
)

clean_data_task = PythonOperator(
    task_id='clean_job_data',
    python_callable=clean_job_data,
    op_kwargs={
        'input_dir': data_dir,
        'output_path': f"{data_dir}/jobs_processed.csv",
    },
    dag=dag,
)

# --- SQL GENERATION FUNCTION ---
def generate_sql_file(**context):
    processed_file = f"{data_dir}/jobs_processed.csv"
    sql_file = os.path.join(data_dir, 'load_jobs.sql')

    with open(sql_file, 'w') as f:
        f.write(f"""
-- Load jobs data
\\COPY staging.jobs(title, company, location, description, url, salary, posted_date, source)
FROM '{processed_file}' DELIMITER ',' CSV HEADER;

-- Insert companies
INSERT INTO companies(name)
SELECT DISTINCT company FROM staging.jobs
ON CONFLICT (name) DO NOTHING;

-- Insert locations
INSERT INTO locations(city, state, country, is_remote)
SELECT DISTINCT 
    normalized_location->>'city',
    normalized_location->>'state',
    normalized_location->>'country',
    COALESCE((normalized_location->>'is_remote')::boolean, false)
FROM staging.jobs
WHERE normalized_location IS NOT NULL
ON CONFLICT (city, state, country) DO NOTHING;

-- Insert skills
INSERT INTO skills(name, category)
SELECT DISTINCT 
    skill,
    CASE
        WHEN skill IN ('python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'go', 'golang', 'php', 'swift', 'kotlin', 'rust', 'scala', 'perl', 'r', 'bash', 'shell', 'sql', 'html', 'css') THEN 'language'
        WHEN skill IN ('react', 'angular', 'vue', 'django', 'flask', 'spring', 'express', 'node.js', 'nodejs', 'laravel', 'rails', 'asp.net', '.net', 'tensorflow', 'pytorch', 'keras', 'pandas', 'numpy', 'scikit-learn', 'bootstrap', 'jquery', 'symfony', 'fastapi') THEN 'framework'
        WHEN skill IN ('mysql', 'postgresql', 'postgres', 'mongodb', 'sqlite', 'oracle', 'sql server', 'redis', 'elasticsearch', 'dynamodb', 'cassandra', 'mariadb', 'neo4j', 'couchdb', 'firebase') THEN 'database'
        WHEN skill IN ('aws', 'azure', 'gcp', 'google cloud', 'heroku', 'digitalocean', 'kubernetes', 'docker', 'terraform', 'lambda', 'ec2', 's3', 'rds', 'cloudfront', 'route53', 'ecs', 'eks') THEN 'cloud'
        ELSE 'other'
    END
FROM staging.jobs, unnest(extracted_skills) AS skill
ON CONFLICT (name) DO NOTHING;

-- Insert jobs
INSERT INTO jobs(title, company_id, location_id, description, url, salary_min, salary_max, salary_currency, salary_period, posted_date, source)
SELECT 
    j.title,
    c.id AS company_id,
    l.id AS location_id,
    j.description,
    j.url,
    j.salary_min,
    j.salary_max,
    j.salary_currency,
    j.salary_period,
    j.posted_date::date,
    j.source
FROM staging.jobs j
JOIN companies c ON j.company = c.name
LEFT JOIN locations l ON 
    j.normalized_location->>'city' = l.city AND
    j.normalized_location->>'state' = l.state AND
    j.normalized_location->>'country' = l.country
ON CONFLICT (url) DO UPDATE SET
    title = EXCLUDED.title,
    description = EXCLUDED.description,
    salary_min = EXCLUDED.salary_min,
    salary_max = EXCLUDED.salary_max,
    salary_currency = EXCLUDED.salary_currency,
    salary_period = EXCLUDED.salary_period,
    updated_at = NOW();

-- Insert job_skills
INSERT INTO job_skills(job_id, skill_id)
SELECT 
    j.id AS job_id,
    s.id AS skill_id
FROM jobs j
JOIN staging.jobs sj ON j.url = sj.url
CROSS JOIN unnest(sj.extracted_skills) AS skill_name
JOIN skills s ON skill_name = s.name
ON CONFLICT (job_id, skill_id) DO NOTHING;

-- Update trending_insights
INSERT INTO trending_insights(skill_id, job_count, avg_salary, date)
SELECT 
    s.id AS skill_id,
    COUNT(DISTINCT j.id) AS job_count,
    AVG(j.salary_min + j.salary_max) / 2 AS avg_salary,
    CURRENT_DATE AS date
FROM skills s
JOIN job_skills js ON s.id = js.skill_id
JOIN jobs j ON js.job_id = j.id
WHERE j.posted_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY s.id, CURRENT_DATE
ON CONFLICT (skill_id, date) DO UPDATE SET
    job_count = EXCLUDED.job_count,
    avg_salary = EXCLUDED.avg_salary,
    updated_at = NOW();

-- Clean up staging table
TRUNCATE TABLE staging.jobs;
        """)
    
    logging.info(f"✅ Generated SQL load file: {sql_file}")
    return sql_file

generate_sql_task = PythonOperator(
    task_id='generate_sql_file',
    python_callable=generate_sql_file,
    dag=dag,
)

# --- CREATE STAGING TABLE ---
create_staging_table = PostgresOperator(
    task_id='create_staging_table',
    postgres_conn_id='postgres_default',
    sql="""
    CREATE SCHEMA IF NOT EXISTS staging;
    DROP TABLE IF EXISTS staging.jobs;
    CREATE TABLE staging.jobs (
        id SERIAL PRIMARY KEY,
        title TEXT,
        company TEXT,
        location TEXT,
        description TEXT,
        url TEXT,
        salary TEXT,
        posted_date TEXT,
        source TEXT,
        extracted_skills TEXT[],
        normalized_location JSONB,
        salary_min NUMERIC,
        salary_max NUMERIC,
        salary_currency TEXT,
        salary_period TEXT
    );
    """,
    dag=dag,
)

# --- LOAD TO POSTGRES ---
load_to_postgres = PostgresOperator(
    task_id='load_processed_data',
    postgres_conn_id='postgres_default',
    sql=f"{data_dir}/load_jobs.sql",
    dag=dag,
)

# --- LOAD TO WAREHOUSE ---
load_to_db_task = PythonOperator(
    task_id="load_to_warehouse",
    python_callable=load_to_warehouse,
    op_kwargs={
        "schema_path": f"{data_dir}/../warehouse/schema.sql",
        "load_sql_path": f"{data_dir}/load_jobs.sql",
    },
    dag=dag,
)

correlation_task = PythonOperator(
    task_id='skill_correlation',
    python_callable=run_correlation,
    dag=dag
)

forecast_task = PythonOperator(
    task_id='skill_forecast',
    python_callable=run_forecast,
    dag=dag
)

# DAG dependencies
[scrape_weworkremotely_task, scrape_naukri_task, scrape_yc_task, scrape_remoteok_task] >> clean_data_task >> generate_sql_task >> create_staging_table >> load_to_postgres >> load_to_db_task >> [correlation_task, forecast_task]
