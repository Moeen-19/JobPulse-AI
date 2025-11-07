import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime
import os
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

# API configuration
API_URL = os.getenv("API_URL")

# Page configuration
st.set_page_config(
    page_title="JobPulse Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .card {
        border-radius: 5px;
        background-color: #f9f9f9;
        padding: 1rem;
        box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1E88E5;
    }
    .metric-label {
        font-size: 1rem;
        color: #424242;
    }
</style>
""", unsafe_allow_html=True)

# API Functions
@st.cache_data(ttl=3600)
def fetch_api_data(endpoint, params=None):
    """Fetch data from API with caching"""
    try:
        response = requests.get(f"{API_URL}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        return None

@st.cache_data(ttl=3600)
def get_jobs(skip=0, limit=100, **filters):
    """Get jobs with filters"""
    params = {"skip": skip, "limit": limit}
    for key, value in filters.items():
        if value:
            params[key] = value
    return fetch_api_data("/jobs", params)

@st.cache_data(ttl=3600)
def get_trending_skills(days=30, limit=20):
    """Get trending skills from API"""
    return fetch_api_data("/insights/trending-skills", {"days": days, "limit": limit})

@st.cache_data(ttl=3600)
def get_salary_insights(days=90):
    """Get salary insights from API"""
    return fetch_api_data("/insights/salary-ranges", {"days": days})

@st.cache_data(ttl=3600)
def get_job_growth(days=90, interval="week"):
    """Get job growth data from API"""
    return fetch_api_data("/insights/job-growth", {"days": days, "interval": interval})

# Sidebar
st.sidebar.markdown('<div class="main-header">JobPulse</div>', unsafe_allow_html=True)
st.sidebar.markdown("### Job Market Analytics Dashboard")

# Navigation
page = st.sidebar.selectbox(
    "Navigation",
    ["Market Overview", "Job Search", "Skill Analysis", "About"]
)

# Sidebar filters
st.sidebar.markdown("### Global Filters")
time_period = st.sidebar.selectbox(
    "Time Period",
    ["Last 30 days", "Last 90 days", "Last 180 days", "Last year"],
    index=1
)

# Convert time period to days
days_mapping = {
    "Last 30 days": 30,
    "Last 90 days": 90,
    "Last 180 days": 180,
    "Last year": 365
}
days_filter = days_mapping[time_period]

# Market Overview Page
if page == "Market Overview":
    st.markdown('<div class="main-header">Job Market Overview</div>', unsafe_allow_html=True)
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    # Sample metrics
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Total Jobs</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-value">5,432</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Companies Hiring</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-value">842</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Avg. Salary (USD)</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-value">$95,750</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Remote Jobs</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-value">38%</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Job growth chart
    st.markdown('<div class="sub-header">Job Posting Trends</div>', unsafe_allow_html=True)
    
    # Sample data for job growth chart
    dates = pd.date_range(end=datetime.now(), periods=12, freq='W')
    job_counts = [120, 145, 132, 158, 172, 190, 210, 205, 225, 240, 255, 270]
    
    job_growth_df = pd.DataFrame({
        'date': dates,
        'count': job_counts
    })
    
    fig_growth = px.line(
        job_growth_df, 
        x='date', 
        y='count',
        title='Weekly Job Postings',
        labels={'date': 'Week', 'count': 'Number of Jobs Posted'},
        markers=True
    )
    fig_growth.update_layout(
        xaxis_title="Week",
        yaxis_title="Number of Jobs",
        plot_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    st.plotly_chart(fig_growth, use_container_width=True)
    
    # Trending skills and salary insights in two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="sub-header">Trending Skills</div>', unsafe_allow_html=True)
        
        # Sample data for trending skills
        skills = ['Python', 'React', 'AWS', 'Docker', 'SQL', 'TypeScript', 'Kubernetes', 'TensorFlow', 'Node.js', 'Go']
        counts = [425, 380, 350, 320, 310, 290, 275, 260, 245, 230]
        
        trending_df = pd.DataFrame({
            'skill': skills,
            'count': counts
        })
        
        fig_skills = px.bar(
            trending_df.sort_values('count', ascending=True).tail(10),
            y='skill',
            x='count',
            orientation='h',
            color='count',
            color_continuous_scale='Blues',
            title='Top 10 In-Demand Skills'
        )
        fig_skills.update_layout(
            yaxis_title="",
            xaxis_title="Number of Job Listings",
            plot_bgcolor='rgba(0,0,0,0)',
            height=400,
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_skills, use_container_width=True)
    
    with col2:
        st.markdown('<div class="sub-header">Salary Distribution</div>', unsafe_allow_html=True)
        
        # Sample data for salary distribution
        job_titles = ['Data Scientist', 'Software Engineer', 'DevOps Engineer', 'Product Manager', 'Data Engineer']
        min_salaries = [85000, 90000, 95000, 100000, 92000]
        max_salaries = [120000, 140000, 135000, 150000, 130000]
        
        salary_df = pd.DataFrame({
            'title': job_titles,
            'min_salary': min_salaries,
            'max_salary': max_salaries
        })
        
        fig_salary = go.Figure()
        
        for i, row in salary_df.iterrows():
            fig_salary.add_trace(go.Box(
                x=[row['title']],
                y=[row['min_salary'], (row['min_salary'] + row['max_salary'])/2, row['max_salary']],
                name=row['title'],
                boxpoints=False
            ))
        
        fig_salary.update_layout(
            title='Salary Ranges by Job Title',
            xaxis_title="",
            yaxis_title="Annual Salary (USD)",
            plot_bgcolor='rgba(0,0,0,0)',
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig_salary, use_container_width=True)

# Job Search Page
elif page == "Job Search":
    st.markdown('<div class="main-header">Job Search</div>', unsafe_allow_html=True)
    
    # Search filters
    col1, col2 = st.columns(2)
    
    with col1:
        search_query = st.text_input("Job Title or Keyword", "")
    
    with col2:
        location_query = st.text_input("Location", "")
    
    # Additional filters in expandable section
    with st.expander("Advanced Filters"):
        col1, col2 = st.columns(2)
        
        with col1:
            remote_only = st.checkbox("Remote Only")
            min_salary = st.number_input("Minimum Salary (USD)", min_value=0, max_value=500000, value=0, step=10000)
        
        with col2:
            selected_skills = st.multiselect(
                "Required Skills",
                ["Python", "JavaScript", "React", "AWS", "SQL", "Java", "Docker"]
            )
            
            sort_by = st.selectbox(
                "Sort By",
                ["Posted Date", "Salary", "Title"],
                index=0
            )
    
    # Search button
    if st.button("Search Jobs"):
        st.markdown('<div class="sub-header">Search Results</div>', unsafe_allow_html=True)
        
        # Sample job data
        sample_jobs = [
            {
                "id": 1,
                "title": "Senior Python Developer",
                "company": {"name": "Tech Solutions Inc."},
                "location": {"city": "New York", "state": "NY", "is_remote": False},
                "salary_min": 120000,
                "salary_max": 150000,
                "posted_date": "2023-05-01",
                "url": "https://example.com/job1"
            },
            {
                "id": 2,
                "title": "Data Scientist",
                "company": {"name": "AI Innovations"},
                "location": {"city": None, "state": None, "is_remote": True},
                "salary_min": 110000,
                "salary_max": 140000,
                "posted_date": "2023-05-03",
                "url": "https://example.com/job2"
            },
            {
                "id": 3,
                "title": "Frontend Developer (React)",
                "company": {"name": "WebApp Studios"},
                "location": {"city": "San Francisco", "state": "CA", "is_remote": False},
                "salary_min": 100000,
                "salary_max": 130000,
                "posted_date": "2023-05-05",
                "url": "https://example.com/job3"
            }
        ]
        
        # Display job results
        for job in sample_jobs:
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"### {job['title']}")
                    st.markdown(f"**{job['company']['name']}**")
                    
                    # Format location
                    if job['location']['is_remote']:
                        location_str = "Remote"
                    else:
                        city = job['location']['city'] or ""
                        state = job['location']['state'] or ""
                        location_str = f"{city}, {state}".strip()
                        if location_str.endswith(","):
                            location_str = location_str[:-1]
                    
                    st.markdown(f"📍 {location_str}")
                    
                    # Format salary
                    if job.get('salary_min') and job.get('salary_max'):
                        salary_str = f"${job['salary_min']:,} - ${job['salary_max']:,}"
                        st.markdown(f"💰 {salary_str}")
                    
                    # Format date
                    if job.get('posted_date'):
                        posted_date = datetime.strptime(job['posted_date'], "%Y-%m-%d")
                        days_ago = (datetime.now() - posted_date).days
                        st.markdown(f"📅 Posted {days_ago} days ago")
                
                with col2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown(f"[View Job]({job['url']})")
                
                st.markdown("---")

# Skill Analysis Page
elif page == "Skill Analysis":
    st.markdown('<div class="main-header">Skill Analysis</div>', unsafe_allow_html=True)
    
    # Skill selection
    selected_skill = st.selectbox(
        "Select a skill to analyze",
        ["Python", "JavaScript", "React", "AWS", "SQL", "Java", "Docker"]
    )
    
    # Display skill insights
    if selected_skill:
        st.markdown(f'<div class="sub-header">Insights for {selected_skill}</div>', unsafe_allow_html=True)
        
        # Key metrics for the skill
        col1, col2, col3 = st.columns(3)
        
        # Sample data
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Job Listings</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">425</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Avg. Salary</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">$110,500</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Growth (30 days)</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">+15%</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Skill demand over time
        st.markdown('<div class="sub-header">Demand Trend</div>', unsafe_allow_html=True)
        
        # Sample data for skill demand trend
        dates = pd.date_range(end=datetime.now(), periods=12, freq='W')
        counts = [85, 92, 88, 95, 105, 110, 118, 125, 132, 140, 145, 150]
        
        trend_df = pd.DataFrame({
            'date': dates,
            'count': counts
        })
        
        fig_trend = px.line(
            trend_df, 
            x='date', 
            y='count',
            title=f'{selected_skill} Demand Over Time',
            labels={'date': 'Week', 'count': 'Number of Job Listings'},
            markers=True
        )
        fig_trend.update_layout(
            xaxis_title="Week",
            yaxis_title="Number of Job Listings",
            plot_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Complementary skills
        st.markdown('<div class="sub-header">Complementary Skills</div>', unsafe_allow_html=True)
        
        # Sample data for complementary skills
        if selected_skill == "Python":
            comp_skills = ['SQL', 'AWS', 'Pandas', 'TensorFlow', 'Docker', 'Flask', 'Django', 'NumPy']
            comp_counts = [320, 280, 260, 240, 220, 200, 190, 180]
        elif selected_skill == "JavaScript":
            comp_skills = ['React', 'TypeScript', 'Node.js', 'HTML', 'CSS', 'Vue.js', 'Angular', 'AWS']
            comp_counts = [350, 320, 300, 290, 280, 250, 230, 210]
        else:
            comp_skills = ['JavaScript', 'Python', 'SQL', 'AWS', 'Docker', 'Git', 'TypeScript', 'Node.js']
            comp_counts = [300, 280, 260, 240, 220, 200, 190, 180]
        
        comp_df = pd.DataFrame({
            'skill': comp_skills,
            'count': comp_counts
        })
        
        fig_comp = px.bar(
            comp_df.sort_values('count', ascending=True),
            y='skill',
            x='count',
            orientation='h',
            color='count',
            color_continuous_scale='Viridis',
            title=f'Top Skills Found with {selected_skill}'
        )
        fig_comp.update_layout(
            yaxis_title="",
            xaxis_title="Co-occurrence Count",
            plot_bgcolor='rgba(0,0,0,0)',
            height=400,
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_comp, use_container_width=True)

# About Page
elif page == "About":
    st.markdown('<div class="main-header">About JobPulse</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ## Job Market Analytics Platform
    
    JobPulse is a comprehensive job market analytics platform that aggregates and analyzes job postings from multiple sources to provide valuable insights into the job market.
    
    ### Features
    
    - **Data Collection**: Aggregates job postings from Indeed, RemoteOK, Glassdoor, and Adzuna
    - **Market Analysis**: Tracks trends in job postings, skills, and salaries
    - **Skill Insights**: Identifies in-demand skills and their growth over time
    - **Salary Analysis**: Provides detailed salary information by job title, location, and experience level
    - **Job Search**: Allows users to search for jobs with advanced filtering options
    
    ### Technology Stack
    
    - **Data Collection**: Python scrapers and API integrations
    - **Data Processing**: Python with pandas and spaCy
    - **Data Storage**: PostgreSQL database
    - **API**: FastAPI
    - **Dashboard**: Streamlit with Plotly visualizations
    - **Orchestration**: Apache Airflow
    """)

# Footer
st.markdown("---")
st.markdown("© 2023 JobPulse | Job Market Analytics Platform")