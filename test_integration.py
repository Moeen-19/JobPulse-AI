#!/usr/bin/env python3
"""
Quick integration test script for JobPulse
Tests API endpoints and database connectivity
"""

import requests
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000")

def test_api_health():
    """Test if API is running"""
    print("🔍 Testing API health...")
    try:
        response = requests.get(f"{API_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ API is running")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to API at {API_URL}")
        print("   Make sure the API server is running:")
        print("   uvicorn api.main:app --reload")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_jobs_endpoint():
    """Test jobs endpoint"""
    print("\n🔍 Testing /jobs endpoint...")
    try:
        response = requests.get(f"{API_URL}/jobs?limit=5", timeout=5)
        if response.status_code == 200:
            jobs = response.json()
            print(f"✅ Jobs endpoint working - Found {len(jobs)} jobs")
            if len(jobs) > 0:
                print(f"   Sample job: {jobs[0].get('title', 'N/A')}")
            else:
                print("   ⚠️  No jobs in database. Run scrapers to populate data.")
            return True
        else:
            print(f"❌ Jobs endpoint returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_skills_endpoint():
    """Test skills endpoint"""
    print("\n🔍 Testing /skills endpoint...")
    try:
        response = requests.get(f"{API_URL}/skills?limit=5", timeout=5)
        if response.status_code == 200:
            skills = response.json()
            print(f"✅ Skills endpoint working - Found {len(skills)} skills")
            if len(skills) > 0:
                print(f"   Sample skill: {skills[0].get('skill_name', 'N/A')}")
            return True
        else:
            print(f"❌ Skills endpoint returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_trending_skills():
    """Test trending skills endpoint"""
    print("\n🔍 Testing /insights/trending-skills endpoint...")
    try:
        response = requests.get(f"{API_URL}/insights/trending-skills?days=30&limit=5", timeout=5)
        if response.status_code == 200:
            trending = response.json()
            print(f"✅ Trending skills endpoint working - Found {len(trending)} trending skills")
            return True
        else:
            print(f"❌ Trending skills endpoint returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_ml_forecast():
    """Test ML forecast endpoint"""
    print("\n🔍 Testing /ml/skill-forecast endpoint...")
    try:
        response = requests.get(
            f"{API_URL}/ml/skill-forecast?skill=python&days_ahead=30", 
            timeout=10
        )
        if response.status_code == 200:
            forecast = response.json()
            print("✅ ML forecast endpoint working")
            if forecast.get('message'):
                print(f"   ℹ️  {forecast['message']}")
            else:
                hist_points = len(forecast.get('historical_points', []))
                fore_points = len(forecast.get('forecast_points', []))
                print(f"   Historical points: {hist_points}")
                print(f"   Forecast points: {fore_points}")
            return True
        else:
            print(f"❌ ML forecast endpoint returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_ml_correlations():
    """Test ML correlations endpoint"""
    print("\n🔍 Testing /ml/skill-correlations endpoint...")
    try:
        response = requests.get(
            f"{API_URL}/ml/skill-correlations?top_n=5", 
            timeout=10
        )
        if response.status_code == 200:
            correlations = response.json()
            print("✅ ML correlations endpoint working")
            if isinstance(correlations, dict):
                corr_list = correlations.get('correlations', [])
                print(f"   Found {len(corr_list)} skill correlations")
            return True
        else:
            print(f"❌ ML correlations endpoint returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_database_connection():
    """Test database connection through API"""
    print("\n🔍 Testing database connection...")
    try:
        # Try to get companies (should work even with empty DB)
        response = requests.get(f"{API_URL}/companies?limit=1", timeout=5)
        if response.status_code == 200:
            print("✅ Database connection working")
            return True
        else:
            print(f"❌ Database connection issue - status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("JobPulse Integration Test Suite")
    print("=" * 60)
    
    tests = [
        ("API Health", test_api_health),
        ("Database Connection", test_database_connection),
        ("Jobs Endpoint", test_jobs_endpoint),
        ("Skills Endpoint", test_skills_endpoint),
        ("Trending Skills", test_trending_skills),
        ("ML Forecast", test_ml_forecast),
        ("ML Correlations", test_ml_correlations),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your integration is working correctly.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
