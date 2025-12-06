@echo off
REM JobPulse Quick Start Script for Windows
REM This script helps you get JobPulse up and running quickly

echo ======================================
echo JobPulse Quick Start
echo ======================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -q --upgrade pip
pip install -q -r requirements.txt

REM Download spaCy model
echo Downloading spaCy model...
python -m spacy download en_core_web_sm

REM Check if .env exists
if not exist ".env" (
    echo Creating .env file...
    (
        echo DB_USER=airflow
        echo DB_PASSWORD=airflow_pass
        echo DB_HOST=localhost
        echo DB_PORT=5432
        echo DB_NAME=jobpulse_db
        echo API_URL=http://localhost:8000
        echo API_HOST=localhost
        echo API_PORT=8000
    ) > .env
    echo Created .env file
)

echo.
echo ======================================
echo Setup Complete!
echo ======================================
echo.
echo Next steps:
echo.
echo 1. Make sure PostgreSQL is installed and running
echo 2. Create the database:
echo    psql -U postgres -c "CREATE DATABASE jobpulse_db;"
echo    psql -U postgres -c "CREATE USER airflow WITH PASSWORD 'airflow_pass';"
echo    psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE jobpulse_db TO airflow;"
echo.
echo 3. Apply schema:
echo    psql -U airflow -d jobpulse_db -f warehouse\schema.sql
echo.
echo 4. Generate sample data:
echo    python generate_sample_data.py
echo.
echo 5. Start the API server:
echo    uvicorn api.main:app --reload
echo.
echo 6. In another terminal, start the website:
echo    cd website
echo    python -m http.server 3000
echo.
echo 7. Open your browser:
echo    http://localhost:3000
echo.
echo ======================================

pause
