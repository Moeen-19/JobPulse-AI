# 🚀 JobPulse - Quick Reference Card

## ⚡ Quick Start Commands

### Setup (First Time Only)
```bash
# Linux/Mac
chmod +x quickstart.sh && ./quickstart.sh

# Windows
quickstart.bat
```

### Daily Development

```bash
# Terminal 1: Start API
uvicorn api.main:app --reload

# Terminal 2: Start Website
cd website && python -m http.server 3000

# Terminal 3: Run Tests
python test_integration.py
```

---

## 🌐 URLs

| Service | URL | Description |
|---------|-----|-------------|
| Website | http://localhost:3000 | Main frontend |
| API | http://localhost:8000 | Backend API |
| API Docs | http://localhost:8000/docs | Interactive API documentation |
| Dashboard | http://localhost:8501 | Streamlit dashboard |
| Airflow | http://localhost:8080 | Airflow web UI |

---

## 📡 API Endpoints

### Jobs
```bash
GET /jobs?limit=10&skip=0
GET /jobs/{job_id}
GET /search?q=python
```

### Skills
```bash
GET /skills?limit=10
GET /skills/{skill_id}
GET /skills/{skill_id}/jobs
```

### Analytics
```bash
GET /insights/trending-skills?days=30&limit=20
GET /insights/salary-ranges?days=90
GET /insights/job-growth?days=90&interval=week
```

### ML
```bash
GET /ml/skill-forecast?skill=python&days_ahead=180
GET /ml/skill-correlations?top_n=20
```

---

## 🗄️ Database Commands

### PostgreSQL
```bash
# Connect to database
psql -U airflow -d jobpulse_db

# Common queries
SELECT COUNT(*) FROM jobs;
SELECT COUNT(*) FROM skills;
SELECT COUNT(*) FROM companies;

# Reset database
DROP DATABASE jobpulse_db;
CREATE DATABASE jobpulse_db;
\i warehouse/schema.sql
```

---

## 🔧 Troubleshooting

### API Won't Start
```bash
# Check if port 8000 is in use
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# Kill process if needed
kill -9 <PID>  # Mac/Linux
taskkill /PID <PID> /F  # Windows
```

### Database Connection Error
```bash
# Check PostgreSQL is running
pg_isready

# Restart PostgreSQL
sudo service postgresql restart  # Linux
brew services restart postgresql  # Mac
# Windows: Services → PostgreSQL → Restart
```

### No Data in Website
```bash
# Generate sample data
python generate_sample_data.py

# Or run scrapers
python -c "from scrapers.remoteok_scraper import scrape_remoteok; scrape_remoteok('data/remoteok_raw.csv')"
```

### CORS Error
```python
# In api/main.py, update CORS:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🧪 Testing

### Run All Tests
```bash
python test_integration.py
```

### Test Individual Endpoints
```bash
# Health check
curl http://localhost:8000/

# Get jobs
curl http://localhost:8000/jobs?limit=5

# Get forecast
curl "http://localhost:8000/ml/skill-forecast?skill=python&days_ahead=30"
```

---

## 📊 Data Collection

### Run Individual Scrapers
```bash
# RemoteOK
python -c "from scrapers.remoteok_scraper import scrape_remoteok; scrape_remoteok('data/remoteok_raw.csv')"

# Naukri
python -c "from scrapers.naukri_scraper import scrape_naukri; scrape_naukri('data/naukri_raw.csv')"

# WeWorkRemotely
python -c "from scrapers.weworkremotely_scraper import scrape_weworkremotely; scrape_weworkremotely('data/weworkremotely_raw.csv')"

# Y Combinator
python -c "from scrapers.y_combinator_scraper import scrape_ycombinator; scrape_ycombinator('data/y_combinator_raw.csv')"
```

### Run Airflow DAG
```bash
# Start Airflow
cd airflow
airflow webserver --port 8080  # Terminal 1
airflow scheduler  # Terminal 2

# Trigger DAG
airflow dags trigger job_ingestion_pipeline
```

---

## 🔑 Environment Variables

```env
# .env file
DB_USER=airflow
DB_PASSWORD=airflow_pass
DB_HOST=localhost
DB_PORT=5432
DB_NAME=jobpulse_db
API_URL=http://localhost:8000
API_HOST=localhost
API_PORT=8000
```

---

## 📁 Project Structure

```
JobPulse/
├── api/                    # Backend API
│   ├── main.py            # FastAPI app
│   ├── models.py          # Database models
│   ├── crud.py            # Database operations
│   └── ml/                # ML models
├── website/               # Frontend
│   ├── index.html         # Home page
│   ├── api-client.js      # API integration
│   └── *.js               # Page logic
├── scrapers/              # Data collection
├── airflow/               # ETL pipeline
├── warehouse/             # Database schema
└── data_processing/       # Data transformation
```

---

## 🐍 Python Commands

### Virtual Environment
```bash
# Create
python -m venv venv

# Activate
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows

# Deactivate
deactivate
```

### Install Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

---

## 🎨 Frontend Development

### Serve Website
```bash
# Python HTTP server
cd website && python -m http.server 3000

# Or use VS Code Live Server
# Right-click index.html → Open with Live Server
```

### Browser Console
```javascript
// Test API connection
api.healthCheck().then(console.log)

// Get jobs
api.getJobs({limit: 5}).then(console.log)

// Get forecast
api.getSkillForecast('python', null, 30).then(console.log)
```

---

## 📝 Common Tasks

### Add New Scraper
1. Create `scrapers/new_scraper.py`
2. Implement `scrape_new_source(output_path)` function
3. Add to `airflow/dags/job_ingestion_dag.py`
4. Update `airflow/etl/data_cleaner.py` input files

### Add New API Endpoint
1. Add function to `api/crud.py`
2. Add endpoint to `api/main.py`
3. Update `website/api-client.js`
4. Use in frontend JavaScript

### Add New Page
1. Create `website/new-page.html`
2. Create `website/new-page.js`
3. Add navigation link in all pages
4. Update `website/api-client.js` if needed

---

## 🔍 Debugging

### Check Logs
```bash
# API logs (in terminal running uvicorn)
# Look for errors and stack traces

# Database logs
tail -f /var/log/postgresql/postgresql-*.log

# Airflow logs
tail -f airflow/logs/scheduler/latest/*.log
```

### Python Debugging
```python
# Add to any Python file
import pdb; pdb.set_trace()

# Or use print statements
print(f"Debug: {variable}")
```

### JavaScript Debugging
```javascript
// Browser console
console.log('Debug:', variable);

// Breakpoint
debugger;
```

---

## 📦 Dependencies

### Core
- Python 3.9+
- PostgreSQL 12+
- pip

### Python Packages
- fastapi
- uvicorn
- sqlalchemy
- pandas
- prophet (optional)
- spacy
- airflow

---

## 🚀 Deployment Checklist

- [ ] Update CORS settings
- [ ] Add authentication
- [ ] Enable HTTPS
- [ ] Set up environment variables
- [ ] Configure database backups
- [ ] Add monitoring
- [ ] Set up logging
- [ ] Add rate limiting
- [ ] Optimize database queries
- [ ] Add caching (Redis)

---

## 💡 Tips & Tricks

### Speed Up Development
```bash
# Use --reload for auto-restart
uvicorn api.main:app --reload

# Use sample data for testing
python generate_sample_data.py
```

### Database Tips
```sql
-- Check table sizes
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Vacuum database
VACUUM ANALYZE;
```

### Performance
```python
# Use pagination
api.getJobs({limit: 100, skip: 0})

# Cache API responses
# Add Redis for production
```

---

## 📚 Documentation Links

- **Setup Guide:** `SETUP_INSTRUCTIONS.md`
- **API Docs:** http://localhost:8000/docs

---

## 🆘 Emergency Commands

### Stop Everything
```bash
# Kill all Python processes
pkill -f python

# Kill specific port
kill -9 $(lsof -t -i:8000)  # API
kill -9 $(lsof -t -i:3000)  # Website
```

### Reset Everything
```bash
# Drop and recreate database
psql -U postgres -c "DROP DATABASE jobpulse_db;"
psql -U postgres -c "CREATE DATABASE jobpulse_db;"
psql -U airflow -d jobpulse_db -f warehouse/schema.sql

# Regenerate data
python generate_sample_data.py

# Restart API
uvicorn api.main:app --reload
```

---

## ✅ Health Check

```bash
# Quick system check
python test_integration.py

# Manual checks
curl http://localhost:8000/  # API
curl http://localhost:3000/  # Website
psql -U airflow -d jobpulse_db -c "SELECT 1;"  # Database
```

---
**Quick Reference v1.0** | Last Updated: December 6, 2025
