# 🚀 Start JobPulse - Step by Step

## ✅ Prerequisites Check
- ✅ Python 3.12.0 installed
- ✅ PostgreSQL 17.5 installed
- ✅ Database `jobpulse_db` exists
- ✅ All Python packages installed

---

## 🎯 Quick Start (3 Steps)

### Step 1: Start the API Server

Open a **NEW PowerShell/Terminal window** and run:

```powershell
cd "C:\Users\LENOVO\OneDrive\ドキュメント\JobPulse"
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

✅ **API is now running at:** http://localhost:8000

---

### Step 2: Generate Sample Data (Optional but Recommended)

Open **ANOTHER PowerShell/Terminal window** and run:

```powershell
cd "C:\Users\LENOVO\OneDrive\ドキュメント\JobPulse"
python generate_sample_data.py
```

When prompted, type `y` and press Enter.

**This will:**
- Create 14 companies
- Create 8 locations
- Create 40+ skills
- Create 100 sample jobs
- Generate trending insights

---

### Step 3: Open the Website

Open **ANOTHER PowerShell/Terminal window** and run:

```powershell
cd "C:\Users\LENOVO\OneDrive\ドキュメント\JobPulse\website"
python -m http.server 3000
```

**Expected Output:**
```
Serving HTTP on :: port 3000 (http://[::]:3000/) ...
```

✅ **Website is now running at:** http://localhost:3000

---

## 🌐 Access the Application

1. **Open your browser** (Chrome, Firefox, Edge)
2. **Go to:** http://localhost:3000
3. **You should see:** The JobPulse home page with dark theme

---

## 🧪 Test the Integration

Open **ANOTHER PowerShell/Terminal window** and run:

```powershell
cd "C:\Users\LENOVO\OneDrive\ドキュメント\JobPulse"
python test_integration.py
```

This will test all API endpoints and verify everything is working.

---

## 📊 What to Try

### 1. Home Page (http://localhost:3000)
- Should show job statistics
- Trending skills
- Companies hiring

### 2. Market Analysis Page
- Click "Market Analysis" in navigation
- Select a skill (e.g., "python")
- Click "Generate Forecast"
- Watch the chart update with real data!

### 3. Job Discovery Page
- Click "Job Discovery" in navigation
- Toggle between Map View and Graph View
- Explore the interactive visualizations

### 4. API Documentation
- Go to: http://localhost:8000/docs
- Try out the API endpoints interactively

---

## 🛑 How to Stop

Press `CTRL+C` in each terminal window to stop:
1. API Server (Terminal 1)
2. Website Server (Terminal 2)

---

## 🔧 Troubleshooting

### Issue: Port Already in Use

**Error:** `Address already in use`

**Solution:**
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace <PID> with actual number)
taskkill /PID <PID> /F
```

### Issue: Database Connection Error

**Solution:**
```powershell
# Check PostgreSQL is running
pg_isready

# If not running, start it from Services
# Windows Key + R → services.msc → Find PostgreSQL → Start
```

### Issue: Module Not Found

**Solution:**
```powershell
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv pandas
```

---

## 📝 Summary of Commands

```powershell
# Terminal 1: API Server
cd "C:\Users\LENOVO\OneDrive\ドキュメント\JobPulse"
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Generate Data (one time)
cd "C:\Users\LENOVO\OneDrive\ドキュメント\JobPulse"
python generate_sample_data.py

# Terminal 3: Website
cd "C:\Users\LENOVO\OneDrive\ドキュメント\JobPulse\website"
python -m http.server 3000

# Terminal 4: Test (optional)
cd "C:\Users\LENOVO\OneDrive\ドキュメント\JobPulse"
python test_integration.py
```

---

## ✨ You're All Set!

Your JobPulse application should now be running with:
- ✅ Backend API on port 8000
- ✅ Frontend website on port 3000
- ✅ Database with sample data
- ✅ Full integration working

**Enjoy exploring your job market analytics platform! 🎉**
