#!/bin/bash
# JobPulse Quick Start Script
# This script helps you get JobPulse up and running quickly

set -e

echo "======================================"
echo "JobPulse Quick Start"
echo "======================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Download spaCy model
echo "🤖 Downloading spaCy model..."
python -m spacy download en_core_web_sm

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cat > .env << EOF
DB_USER=airflow
DB_PASSWORD=airflow_pass
DB_HOST=localhost
DB_PORT=5432
DB_NAME=jobpulse_db
API_URL=http://localhost:8000
API_HOST=localhost
API_PORT=8000
EOF
    echo "✅ Created .env file"
fi

# Check PostgreSQL
echo "🔍 Checking PostgreSQL..."
if command -v psql &> /dev/null; then
    echo "✅ PostgreSQL found"
    
    # Check if database exists
    if psql -U postgres -lqt | cut -d \| -f 1 | grep -qw jobpulse_db; then
        echo "✅ Database 'jobpulse_db' exists"
    else
        echo "📊 Creating database..."
        psql -U postgres -c "CREATE DATABASE jobpulse_db;"
        psql -U postgres -c "CREATE USER airflow WITH PASSWORD 'airflow_pass';"
        psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE jobpulse_db TO airflow;"
        echo "✅ Database created"
    fi
    
    # Apply schema
    echo "📋 Applying database schema..."
    psql -U airflow -d jobpulse_db -f warehouse/schema.sql
    echo "✅ Schema applied"
else
    echo "⚠️  PostgreSQL not found. Please install PostgreSQL and run this script again."
    exit 1
fi

# Generate sample data
echo ""
echo "Would you like to generate sample data for testing? (y/n)"
read -r response
if [ "$response" = "y" ]; then
    echo "📊 Generating sample data..."
    python generate_sample_data.py <<< "y"
fi

echo ""
echo "======================================"
echo "✅ Setup Complete!"
echo "======================================"
echo ""
echo "To start JobPulse:"
echo ""
echo "1. Start the API server:"
echo "   uvicorn api.main:app --reload"
echo ""
echo "2. In another terminal, start the website:"
echo "   cd website && python -m http.server 3000"
echo ""
echo "3. Open your browser:"
echo "   http://localhost:3000"
echo ""
echo "4. Test the integration:"
echo "   python test_integration.py"
echo ""
echo "======================================"
