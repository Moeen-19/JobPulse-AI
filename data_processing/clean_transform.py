import re
import pandas as pd
import numpy as np
import spacy
import logging
from typing import Dict, List, Any, Set, Tuple, Optional
from datetime import datetime, timedelta
import json 
import os 

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger('data_processing')

# Try to load spaCy model, with fallback
try:
    nlp = spacy.load("en_core_web_sm")
    logger.info("Loaded spaCy model: en_core_web_sm")
except OSError:
    logger.warning("Could not load en_core_web_sm. Using en_core_web_md instead.")
    try:
        nlp = spacy.load("en_core_web_md")
    except OSError:
        logger.error("No spaCy models found. Please install one with: python -m spacy download en_core_web_sm")
        nlp = None

class JobDataProcessor:
    """
    Process and transform job data from various sources
    """
    
    def __init__(self):
        """
        Initialize the job data processor
        """
        # Common tech skills for extraction
        self.tech_skills = {
            'languages': [
                'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'go', 'golang', 'php', 
                'swift', 'kotlin', 'rust', 'scala', 'perl', 'r', 'bash', 'shell', 'sql', 'html', 'css'
            ],
            'frameworks': [
                'react', 'angular', 'vue', 'django', 'flask', 'spring', 'express', 'node.js', 'nodejs',
                'laravel', 'rails', 'asp.net', '.net', 'tensorflow', 'pytorch', 'keras', 'pandas', 
                'numpy', 'scikit-learn', 'bootstrap', 'jquery', 'symfony', 'fastapi'
            ],
            'databases': [
                'mysql', 'postgresql', 'postgres', 'mongodb', 'sqlite', 'oracle', 'sql server', 'redis',
                'elasticsearch', 'dynamodb', 'cassandra', 'mariadb', 'neo4j', 'couchdb', 'firebase'
            ],
            'cloud': [
                'aws', 'azure', 'gcp', 'google cloud', 'heroku', 'digitalocean', 'kubernetes', 'docker',
                'terraform', 'lambda', 'ec2', 's3', 'rds', 'cloudfront', 'route53', 'ecs', 'eks'
            ],
            'tools': [
                'git', 'github', 'gitlab', 'bitbucket', 'jira', 'jenkins', 'travis', 'circleci', 'ansible',
                'puppet', 'chef', 'kubernetes', 'docker', 'nginx', 'apache', 'linux', 'unix', 'windows',
                'macos', 'agile', 'scrum', 'kanban', 'ci/cd', 'cicd'
            ]
        }
        
        # Flatten the skills list for easier matching
        self.all_skills = set[Any]()
        for category in self.tech_skills.values():
            self.all_skills.update(category)
    
    def process_jobs(self, jobs: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Process a list of job dictionaries into a standardized DataFrame
        
        Args:
            jobs: List of job dictionaries from various sources
            
        Returns:
            Processed DataFrame
        """
        if not jobs:
            return pd.DataFrame()
        
        # Convert to DataFrame
        df = pd.DataFrame(jobs)
        
        # Standardize column names
        df = self._standardize_columns(df)
        
        # Clean and normalize data
        df = self._clean_data(df)
        
        # Extract skills from job descriptions
        if 'description' in df.columns:
            df['extracted_skills'] = df['description'].apply(self.extract_skills)
        
        # Normalize locations
        if 'location' in df.columns:
            df['normalized_location'] = df['location'].apply(self._normalize_location)
        
        # Parse salary information
        if 'salary' in df.columns:
            salary_info = df['salary'].apply(self._parse_salary)
            
            # Create new columns from the parsed salary info
            df['salary_min'] = salary_info.apply(lambda x: x.get('min'))
            df['salary_max'] = salary_info.apply(lambda x: x.get('max'))
            df['salary_currency'] = salary_info.apply(lambda x: x.get('currency'))
            df['salary_period'] = salary_info.apply(lambda x: x.get('period'))
        
        # Standardize dates
        if 'posted_date' in df.columns:
            df['posted_date'] = df['posted_date'].apply(self._parse_date)
        
        return df
    
    def _standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize column names across different sources
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with standardized column names
        """
        # Map of common column name variations
        column_mapping = {
            'position': 'title',
            'job_title': 'title',
            'company_name': 'company',
            'description_snippet': 'description',
            'full_description': 'description',
            'job_description': 'description',
            'date': 'posted_date',
            'created': 'posted_date',
        }
        
        # Rename columns based on mapping
        df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
        
        return df
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and normalize data
        
        Args:
            df: Input DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        # Make a copy to avoid SettingWithCopyWarning
        df = df.copy()
        
        # Clean text fields
        text_columns = ['title', 'company', 'description', 'location']
        for col in text_columns:
            if col in df.columns:
                # Replace NaN with empty string
                df[col] = df[col].fillna('')
                
                # Clean text
                df[col] = df[col].astype(str).apply(self._clean_text)
        
        # Deduplicate jobs based on title, company, and description
        if all(col in df.columns for col in ['title', 'company']):
            df = df.drop_duplicates(subset=['title', 'company'])
        
        return df
    
    def _clean_text(self, text: str) -> str:
        """
        Clean text by removing extra whitespace and special characters
        
        Args:
            text: Input text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', text)
        
        # Replace newlines and tabs with spaces
        text = re.sub(r'[\n\t\r]+', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def extract_skills(self, text: str) -> List[str]:
        """
        Extract technical skills from job description
        
        Args:
            text: Job description text
            
        Returns:
            List of extracted skills
        """
        if not text:
            return []
        
        text = text.lower()
        found_skills = set()
        
        # Simple pattern matching for skills
        for skill in self.all_skills:
            # Create a regex pattern that matches the skill as a whole word
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text):
                found_skills.add(skill)
        
        # Use spaCy for more advanced NER if available
        if nlp and len(text) < 1000000:  # Limit text size to avoid memory issues
            try:
                doc = nlp(text)
                
                # Extract entities that might be technologies
                for ent in doc.ents:
                    if ent.label_ in ["PRODUCT", "ORG", "GPE"]:
                        skill_candidate = ent.text.lower()
                        # Check if this entity matches any known skill
                        for skill in self.all_skills:
                            if skill in skill_candidate:
                                found_skills.add(skill)
            except Exception as e:
                logger.error(f"Error in spaCy processing: {e}")
        
        return list(found_skills)
    
    def _normalize_location(self, location: str) -> Dict[str, str]:
        """
        Normalize location strings into structured components
        
        Args:
            location: Location string
            
        Returns:
            Dictionary with city, state, country
        """
        if not location or location.lower() in ['remote', 'work from home', 'wfh']:
            return {'city': None, 'state': None, 'country': None, 'is_remote': True}
        
        # Initialize result
        result = {'city': None, 'state': None, 'country': None, 'is_remote': False}
        
        # Check for remote indicators
        if re.search(r'\bremote\b', location.lower()):
            result['is_remote'] = True
        
        # Try to extract location components
        # This is a simplified approach - in a real system, you'd use a location database
        
        # US format: "City, State"
        us_match = re.match(r'([^,]+),\s*([A-Z]{2})', location)
        if us_match:
            result['city'] = us_match.group(1).strip()
            result['state'] = us_match.group(2).strip()
            result['country'] = 'United States'
            return result
        
        # International format: "City, Country"
        intl_match = re.match(r'([^,]+),\s*(.+)', location)
        if intl_match:
            result['city'] = intl_match.group(1).strip()
            result['country'] = intl_match.group(2).strip()
            return result
        
        # If no pattern matches, use the whole string as the city
        result['city'] = location.strip()
        
        return result
    
    def _parse_salary(self, salary_text: str) -> Dict[str, Any]:
        """
        Parse salary information from text
        
        Args:
            salary_text: Salary text
            
        Returns:
            Dictionary with min, max, currency, and period
        """
        if not salary_text:
            return {'min': None, 'max': None, 'currency': None, 'period': None}
        
        salary_text = str(salary_text).lower()
        result = {'min': None, 'max': None, 'currency': None, 'period': None}
        
        # Extract currency
        currency_map = {
            '$': 'USD',
            '£': 'GBP',
            '€': 'EUR',
            '¥': 'JPY',
            'usd': 'USD',
            'gbp': 'GBP',
            'eur': 'EUR',
            'jpy': 'JPY'
        }
        
        for symbol, code in currency_map.items():
            if symbol in salary_text:
                result['currency'] = code
                break
        
        # Extract period
        period_patterns = {
            'year': r'\b(year|yearly|annual|per year|/year|p\.a\.)\b',
            'month': r'\b(month|monthly|per month|/month)\b',
            'week': r'\b(week|weekly|per week|/week)\b',
            'hour': r'\b(hour|hourly|per hour|/hour)\b',
            'day': r'\b(day|daily|per day|/day)\b'
        }
        
        for period, pattern in period_patterns.items():
            if re.search(pattern, salary_text):
                result['period'] = period
                break
        
        # Extract salary range
        # Look for patterns like "$50,000 - $70,000" or "50k-70k"
        range_match = re.search(r'(\d[\d,.]+)(?:k)?(?:\s*-\s*|\s*to\s*)(\d[\d,.]+)(?:k)?', salary_text)
        if range_match:
            min_val = range_match.group(1).replace(',', '')
            max_val = range_match.group(2).replace(',', '')
            
            # Handle 'k' suffix
            if 'k' in salary_text:
                min_val = float(min_val) * 1000
                max_val = float(max_val) * 1000
            else:
                min_val = float(min_val)
                max_val = float(max_val)
            
            result['min'] = min_val
            result['max'] = max_val
        else:
            # Look for a single number
            single_match = re.search(r'(\d[\d,.]+)(?:k)?', salary_text)
            if single_match:
                val = single_match.group(1).replace(',', '')
                
                # Handle 'k' suffix
                if 'k' in salary_text:
                    val = float(val) * 1000
                else:
                    val = float(val)
                
                result['min'] = val
                result['max'] = val
        
        return result
    
    def _parse_date(self, date_text: str) -> Optional[str]:
        """
        Parse date from various formats to ISO format
        
        Args:
            date_text: Date text
            
        Returns:
            ISO formatted date string or None
        """
        if not date_text:
            return None
        
        date_text = str(date_text).lower().strip()
        
        # Handle relative dates like "2 days ago", "1 week ago"
        relative_match = re.search(r'(\d+)\s+(day|days|week|weeks|month|months)\s+ago', date_text)
        if relative_match:
            num = int(relative_match.group(1))
            unit = relative_match.group(2)
            
            today = datetime.now()
            
            if unit in ['day', 'days']:
                date = today - timedelta(days=num)
            elif unit in ['week', 'weeks']:
                date = today - timedelta(weeks=num)
            elif unit in ['month', 'months']:
                # Approximate a month as 30 days
                date = today - timedelta(days=num * 30)
            
            return date.strftime('%Y-%m-%d')
        
        # Try to parse with various formats
        date_formats = [
            '%Y-%m-%d',
            '%d/%m/%Y',
            '%m/%d/%Y',
            '%B %d, %Y',
            '%b %d, %Y',
            '%d %B %Y',
            '%d %b %Y'
        ]
        
        for fmt in date_formats:
            try:
                date = datetime.strptime(date_text, fmt)
                return date.strftime('%Y-%m-%d')
            except ValueError:
                continue
        
        return None