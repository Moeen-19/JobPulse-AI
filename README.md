# 💼 JobPulse — Intelligent Job Market Analytics Platform

 **Real-time job data analytics and skill forecasting platform** powered by FastAPI, Airflow, and Prophet.

JobPulse is a data engineering–driven platform that **collects, cleans, analyzes, and visualizes** job market data across multiple sources to uncover **emerging skill trends, regional demand, and future forecasts**.  
Designed for scalability and real-world data pipelines, it integrates ETL workflows, machine learning forecasting, and an interactive dashboard for instant insights.

---

## 📋 Table of Contents

- [🚀 Overview](#-overview)
- [✨ Key Features](#-key-features)
- [🏗️ Architecture](#️-architecture)
- [🛠️ Tech Stack](#️-tech-stack)
- [⚙️ Installation](#️-installation)
- [🔧 Configuration](#-configuration)
- [🚀 Getting Started](#-getting-started)
- [📊 Dashboard Guide](#-dashboard-guide)
- [🔌 API Reference](#-api-reference)
- [📈 ML Capabilities](#-ml-capabilities)
- [🔍 Authors](#-authors)
- [🧪 Acknowledgments](#-acknowledgments)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🚀 Overview

**JobPulse** is an end-to-end data engineering solution that collects, processes, analyzes, and visualizes job market data from multiple sources. The platform provides real-time insights into:

- 📊 **Emerging skill trends** across industries and regions
- 🌍 **Geographic demand patterns** for various roles
- 💰 **Salary distributions** by position and location
- 🔮 **Future skill demand forecasts** using time-series analysis

Built with a modern data stack, JobPulse integrates ETL workflows, machine learning forecasting, and interactive visualizations to deliver actionable intelligence for job seekers, recruiters, and educational institutions.

---

## ✨ Key Features

### 🔄 Data Pipeline & Integration
- **Multi-source data collection** from job boards and APIs:
  - WeWorkRemotely (RSS feed)
  - Naukri (web scraping)
  - Y Combinator (web scraping)
  - RemoteOK (web scraping)
- **Automated ETL workflows** with Apache Airflow
- **Incremental data loading** with checkpoint tracking
- **Robust error handling** and retry mechanisms

### 🧠 Data Processing & Analytics
- **NLP-powered skill extraction** from job descriptions
- **Skill correlation analysis** to identify complementary skills
- **Time-series forecasting** for skill demand trends
- **Salary analysis** and normalization across regions

### 🖥️ API & Dashboard
- **RESTful API** with comprehensive documentation
- **Interactive Streamlit dashboard** with:
  - Market overview with key metrics
  - Job search with advanced filtering
  - Skill analysis with demand trends
  - Salary insights by role and location

---

## 🏗️ Architecture

JobPulse follows a modular architecture with clear separation of concerns:

```
JobPulse/
│
├── airflow/                      # Workflow orchestration
│   ├── dags/
│   │   └── job_ingestion_dag.py  # Main ETL pipeline
│   └── etl/
│       ├── data_cleaner.py       # Data transformation
│       └── load_to_warehouse.py  # Database loading
│
├── api/                          # FastAPI backend
│   ├── crud.py                   # Database operations
│   ├── database.py               # DB connection
│   ├── main.py                   # API endpoints
│   ├── models.py                 # SQLAlchemy models
│   ├── schemas.py                # Pydantic schemas
│   └── ml/                       # ML components
│       ├── correlation.py        # Skill correlations
│       └── forecasting.py        # Demand forecasting
│
├── dashboard/                    # Visualization
│   └── app.py                    # Streamlit dashboard
│
├── data_processing/              # Data transformation
│   └── clean_transform.py        # Cleaning pipeline
│
├── scrapers/                     # Data collection
│   ├── naukri_scraper.py
│   ├── remoteok_scraper.py
│   ├── weworkremotely_scraper.py
│   ├── y_combinator_scraper.py
│   └── meta_data_checkpoints/    # Ingestion tracking
│
├── warehouse/                    # Database
│   └── schema.sql                # DB schema
│
├── .env                          # Environment variables
├── requirements.txt              # Dependencies
└── README.md                     # Documentation
```

---

## 🛠️ Tech Stack

### Backend & Data Processing
- **Python 3.9+**: Core programming language
- **FastAPI**: High-performance API framework
- **SQLAlchemy**: ORM for database operations
- **Pydantic**: Data validation and settings management
- **Apache Airflow**: Workflow orchestration
- **spaCy**: Natural language processing
- **pandas**: Data manipulation and analysis

### Data Storage
- **PostgreSQL**: Primary database
- **JSON/CSV**: Intermediate data storage

### Analytics & ML
- **scikit-learn**: Machine learning algorithms
- **Prophet**: Time series forecasting
- **numpy**: Numerical computing

### Frontend & Visualization
- **Streamlit**: Interactive dashboard
- **Plotly**: Advanced data visualizations

---

## ⚙️ Installation & Prerequisites

### Step 1: Clone the repository
```bash
git clone https://github.com/yourusername/JobPulse.git
cd JobPulse
```

### Step 2: Create and activate a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt # In case the requirements.txt is unable to install all the dependencies, you have to manually install them

# Install spaCy english language model
python -m spacy download en_core_web_sm
```

### Step 4: Set up the database
```bash
# Create PostgreSQL database
psql -U postgres -c "CREATE DATABASE jobpulse_db;"

# Apply schema
psql -U postgres -d jobpulse_db -f warehouse/schema.sql
```

---

### Step 5: Set up Apache Airflow
```bash
# Initialize Airflow database (first time only)
cd airflow
airflow db init

# Create Airflow user
airflow users create \
    --username admin \
    --password admin \
    --firstname Moeen \
    --lastname Shaikh \
    --role Admin \
    --email moeen@example.com
```

## 🔧 Configuration

Create a `.env` file in the project root with the following variables:

```
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=jobpulse_db
DB_USER=postgres
DB_PASSWORD=your_password

```

---

## 🚀 Getting Started

### Quick Start (Recommended)

#### Linux/Mac:
```bash
chmod +x quickstart.sh
./quickstart.sh
```

#### Windows:
```cmd
quickstart.bat
```

### Manual Setup

#### 1. Install Dependencies
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

#### 2. Setup Database
```bash
# Create database
psql -U postgres -c "CREATE DATABASE jobpulse_db;"
psql -U postgres -c "CREATE USER airflow WITH PASSWORD 'airflow_pass';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE jobpulse_db TO airflow;"

# Apply schema
psql -U airflow -d jobpulse_db -f warehouse/schema.sql

# Generate sample data (optional)
python generate_sample_data.py
```

#### 3. Start the API Server
```bash
uvicorn api.main:app --reload
```
The API will be available at http://localhost:8000  
API Documentation: http://localhost:8000/docs

#### 4. Start the Website
```bash
cd website
python -m http.server 3000
```
The website will be available at http://localhost:3000

#### 5. Test Integration
```bash
python test_integration.py
```

### Optional: Run Data Collection

#### Option A: Run Scrapers Manually
```bash
python -c "from scrapers.remoteok_scraper import scrape_remoteok; scrape_remoteok('data/remoteok_raw.csv')"
```

#### Option B: Use Airflow
```bash
# Terminal 1: Start webserver
cd airflow && airflow webserver --port 8080

# Terminal 2: Start scheduler
cd airflow && airflow scheduler

# Access http://localhost:8080 and trigger 'job_ingestion_pipeline'
```

#### Option C: Launch the Dashboard
```bash
streamlit run dashboard/app.py
```
The dashboard will be available at http://localhost:8501

---

## 📊 Dashboard Guide

The JobPulse dashboard consists of four main sections:

### 1. Market Overview
- Key metrics on job volume, top skills, and hiring trends
- Interactive charts showing job posting trends over time
- Geographic distribution of job opportunities

### 2. Job Search
- Advanced search with filters for skills, locations, and companies
- Detailed job listings with skill requirements and salary information
- Save and export job search results

### 3. Skill Analysis
- Skill demand trends over time
- Complementary skills analysis
- Regional skill demand comparison
- Skill growth forecasting

### 4. About
- Platform information and data sources
- Methodology explanation
- Contact information

---

## 🔌 API Reference

The JobPulse API provides comprehensive endpoints for accessing job market data:

### Jobs
- `GET /api/jobs`: List all jobs with pagination and filtering
- `GET /api/jobs/{job_id}`: Get detailed information about a specific job
- `GET /api/jobs/search`: Search jobs with advanced filtering

### Skills
- `GET /api/skills`: List all skills with demand metrics
- `GET /api/skills/{skill_id}`: Get detailed information about a specific skill
- `GET /api/skills/trending`: Get trending skills by time period

### Analytics
- `GET /api/analytics/skill-forecast/{skill_id}`: Get demand forecast for a skill
- `GET /api/analytics/salary-insights`: Get salary distribution by role and location
- `GET /api/analytics/job-growth`: Get job posting growth by category

For complete API documentation, visit `/docs` when the API server is running.

---

## 📈 ML Capabilities

JobPulse incorporates several machine learning components:

### Skill Extraction
- Uses NLP techniques to extract technical skills from job descriptions
- Employs named entity recognition and pattern matching

### Skill Correlation
- Identifies complementary skills using co-occurrence analysis
- Generates skill relationship graphs

### Demand Forecasting
- Uses Prophet for time-series forecasting of skill demand
- Provides confidence intervals for predictions

### Salary Analysis
- Normalizes salary data across regions
- Identifies factors influencing compensation

---

## 🧑‍💻 Authors

**Moeen G. Shaikh** — 🎓 *Computer Science Student* | 💡 *Data Engineering Enthusiast* | 🌍 *Building intelligent data-driven systems*

### 👨‍🔬 Contributions:
- Architected and implemented the **end-to-end data engineering pipeline**, integrating ETL workflows using **Apache Airflow**.  
- Developed the **FastAPI backend** for seamless API management and database operations.  
- Engineered **skill growth forecasting** and **skill–region correlation models** using **Prophet** and **scikit-learn**.  
- Created efficient **data ingestion and cleaning modules** to handle multi-platform job datasets.   
- Authored technical documentation and optimized project structure for scalability, maintainability, and deployment readiness.


---

## 🌟 Acknowledgments

Special thanks to the following tools and frameworks that power **JobPulse**:

- **FastAPI**, **SQLAlchemy**, and **PostgreSQL** — for building a robust backend API and database layer.  
- **Apache Airflow** — for orchestrating ETL workflows and ensuring smooth data pipelines.  
- **Prophet**, **scikit-learn**, and **Pandas** — for skill forecasting and analytical computation.  
- **SpaCy**, **NLTK**, **BeautifulSoup**, and **lxml** — for NLP processing and job data extraction.  
- **Requests** and **python-dateutil** — for API communication and date-time normalization.  
- **Streamlit** and **Plotly** — for creating interactive visual dashboards.  
- The **open-source developer community** — for their invaluable tools, research, and continuous innovation.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

