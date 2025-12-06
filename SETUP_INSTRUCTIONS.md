# 🚀 JobPulse - Complete Setup Instructions

## Prerequisites

- Python 3.9+
- PostgreSQL 12+
- Node.js (optional, for development)
- Git

---

## Step 1: Clone and Setup Environment

```bash
# Clone the repository
git clone <your-repo-url>
cd JobPulse

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

---

## Step 2: Database Setup

```bash
# Create PostgreSQL database
psql -U postgres

# In psql:
CREATE DATABASE jobpulse_db;
CREATE USER airflow WITH PASSWORD 'airflow_pass';
GRANT ALL PRIVILEGES ON DATABASE jobpulse_db TO airflow;
\q

# Apply schema
psql -U airflow -d jobpulse_db -f warehouse/schema.sql
```

---

## Step 3: Configure Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
DB_USER=airflow
DB_PASSWORD=airflow_pass
DB_HOST=localhost
DB_PORT=5432
DB_NAME=jobpulse_db

# API Configuration
API_URL=http://localhost:8000
API_HOST=localhost
API_PORT=8000
```

---

## Step 4: Initialize Airflow (Optional - for ETL)

```bash
# Set Airflow home
export AIRFLOW_HOME=$(pwd)/airflow

# Initialize Airflow database
cd airflow
airflow db init

# Create admin user
airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@jobpulse.com

cd ..
```

---

## Step 5: Start the Backend API

```bash
# From project root
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: http://localhost:8000
API Documentation: http://localhost:8000/docs

---

## Step 6: Run Data Collection (Optional)

### Option A: Run Scrapers Manually

```bash
# Run individual scrapers
python -c "from scrapers.remoteok_scraper import scrape_remoteok; scrape_remoteok('data/remoteok_raw.csv')"
python -c "from scrapers.naukri_scraper import scrape_naukri; scrape_naukri('data/naukri_raw.csv')"
python -c "from scrapers.weworkremotely_scraper import scrape_weworkremotely; scrape_weworkremotely('data/weworkremotely_raw.csv')"
python -c "from scrapers.y_combinator_scraper import scrape_ycombinator; scrape_ycombinator('data/y_combinator_raw.csv')"
```

### Option B: Run Airflow DAG

```bash
# Terminal 1: Start Airflow webserver
cd airflow
airflow webserver --port 8080

# Terminal 2: Start Airflow scheduler
cd airflow
airflow scheduler

# Access Airflow UI at http://localhost:8080
# Username: admin, Password: admin
# Trigger the 'job_ingestion_pipeline' DAG
```

---

## Step 7: Open the Website

```bash
# Option 1: Use Python's built-in server
cd website
python -m http.server 3000

# Option 2: Use VS Code Live Server extension
# Right-click on index.html and select "Open with Live Server"

# Option 3: Open directly in browser
# Open website/index.html in your browser
```

Website will be available at: http://localhost:3000

---

## Step 8: Run the Dashboard (Optional)

```bash
# From project root
streamlit run dashboard/app.py
```

Dashboard will be available at: http://localhost:8501

---

## 🧪 Testing the Integration

### 1. Test API Health

```bash
curl http://localhost:8000/
```

Expected response:
```json
{
  "message": "Welcome to JobPulse API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

### 2. Test API Endpoints

```bash
# Get jobs
curl http://localhost:8000/jobs?limit=5

# Get trending skills
curl http://localhost:8000/insights/trending-skills?days=30&limit=10

# Get skill forecast
curl "http://localhost:8000/ml/skill-forecast?skill=python&days_ahead=30"

# Get skill correlations
curl "http://localhost:8000/ml/skill-correlations?top_n=10"
```

### 3. Test Website Integration

1. Open http://localhost:3000 in your browser
2. Open browser console (F12)
3. Check for API connection messages
4. Navigate to Market Analysis page
5. Select a skill and click "Generate Forecast"
6. Verify data loads from API

---

## 🔧 Troubleshooting

### Issue: API Connection Failed

**Solution:**
- Ensure FastAPI server is running: `uvicorn api.main:app --reload`
- Check if port 8000 is available
- Verify `.env` file configuration

### Issue: Database Connection Error

**Solution:**
- Verify PostgreSQL is running: `pg_isready`
- Check database credentials in `.env`
- Ensure database exists: `psql -U postgres -l`

### Issue: CORS Error in Browser

**Solution:**
- API already configured with CORS
- If still having issues, update `api/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: No Data in Website

**Solution:**
1. Run scrapers to collect data
2. Verify data in database: `psql -U airflow -d jobpulse_db -c "SELECT COUNT(*) FROM jobs;"`
3. Check API returns data: `curl http://localhost:8000/jobs`

### Issue: Prophet Import Error

**Solution:**
```bash
pip install prophet
# or
conda install -c conda-forge prophet
```

### Issue: spaCy Model Not Found

**Solution:**
```bash
python -m spacy download en_core_web_sm
```

---

## 📊 Quick Start (Minimal Setup)

If you just want to see the website working:

```bash
# 1. Start API with sample data
uvicorn api.main:app --reload

# 2. Open website
cd website
python -m http.server 3000

# 3. Visit http://localhost:3000
```

Note: Without running scrapers, some endpoints may return empty data.

---

## 🎯 Development Workflow

### Daily Development

```bash
# Terminal 1: API Server
uvicorn api.main:app --reload

# Terminal 2: Website Server
cd website && python -m http.server 3000

# Terminal 3: Development/Testing
# Run tests, scrapers, etc.
```

### Running ETL Pipeline

```bash
# Terminal 1: Airflow Webserver
cd airflow && airflow webserver --port 8080

# Terminal 2: Airflow Scheduler
cd airflow && airflow scheduler

# Access http://localhost:8080 and trigger DAG
```

---

## 📝 Project Structure

```
JobPulse/
├── api/                    # FastAPI backend
│   ├── main.py            # API endpoints
│   ├── models.py          # Database models
│   ├── crud.py            # Database operations
│   └── ml/                # ML models
├── website/               # Frontend
│   ├── index.html         # Home page
│   ├── api-client.js      # API integration
│   └── *.js               # Page-specific logic
├── scrapers/              # Data collection
├── airflow/               # ETL pipeline
├── dashboard/             # Streamlit dashboard
├── warehouse/             # Database schema
└── data_processing/       # Data transformation
```

---

## 🚀 Next Steps

1. **Populate Database**: Run scrapers to collect job data
2. **Explore API**: Visit http://localhost:8000/docs
3. **Test Website**: Navigate through all pages
4. **Run Analysis**: Try the Market Analysis forecasting
5. **Customize**: Modify scrapers, add new features

---

## 📚 Additional Resources

- FastAPI Documentation: https://fastapi.tiangolo.com/
- PostgreSQL Documentation: https://www.postgresql.org/docs/
- Apache Airflow: https://airflow.apache.org/docs/
- Prophet: https://facebook.github.io/prophet/

---

**Need Help?** Check the PROJECT_AUDIT_REPORT.md for detailed technical information.
