import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class ATSAnalyzer:
    """Analyze resumes against ATS filters and job descriptions"""
    
    # Common ATS formatting red flags
    FORMATTING_ISSUES = {
        'tables': r'<table|┌|└|├',
        'images': r'<img|<image|\.png|\.jpg|\.jpeg|\.gif',
        'headers_footers': r'<header|<footer|^Page \d+',
        'multiple_columns': r'<col|column|col-',
        'special_fonts': r'<font|Comic Sans|Wingdings|Symbol',
        'unusual_formatting': r'<div|<span|<!DOCTYPE',
    }
    
    def __init__(self, resume_text, job_description_text=None, required_keywords=None):
        self.resume_text = resume_text.lower()
        self.resume_text_original = resume_text
        self.job_description_text = job_description_text.lower() if job_description_text else ""
        self.required_keywords = required_keywords or []
        
        # Analysis results
        self.matched_keywords = []
        self.missing_keywords = []
        self.formatting_issues = []
        self.recommendations = []
        self.keyword_match_score = 0.0
        self.formatting_score = 0.0
        self.overall_ats_score = 0.0
    
    def analyze(self):
        """Run complete ATS analysis"""
        self.extract_keywords_from_jd()
        self.match_keywords()
        self.check_formatting()
        self.calculate_scores()
        self.generate_recommendations()
        
        return {
            'matched_keywords': self.matched_keywords,
            'missing_keywords': self.missing_keywords,
            'formatting_issues': self.formatting_issues,
            'recommendations': self.recommendations,
            'keyword_match_score': self.keyword_match_score,
            'formatting_score': self.formatting_score,
            'overall_ats_score': self.overall_ats_score,
            'ats_pass': self.overall_ats_score >= 60
        }
    
    def extract_keywords_from_jd(self):
        """Extract keywords from job description"""
        if not self.job_description_text:
            return
        
        # Extract technical skills, frameworks, tools
        tech_keywords = self._extract_tech_terms()
        soft_skills = self._extract_soft_skills()
        
        self.required_keywords = list(set(tech_keywords + soft_skills))
    
    def _extract_tech_terms(self):
        """Extract technical terms and tools"""
        common_tech = {
            # Programming languages
            'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin',
            'typescript', 'go', 'rust', 'scala', 'r', 'matlab', 'perl', 'groovy',
            
            # Web frameworks
            'django', 'flask', 'spring', 'react', 'angular', 'vue', 'express', 'fastapi',
            'rails', 'laravel', 'asp.net', 'dot net', '.net',
            
            # Databases
            'sql', 'mysql', 'postgresql', 'mongodb', 'nosql', 'oracle', 'dynamodb',
            'redis', 'elasticsearch', 'cassandra', 'firestore',
            
            # Cloud & DevOps
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'ci/cd', 'terraform',
            'ansible', 'cloudformation', 'heroku',
            
            # Data & ML
            'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn',
            'pandas', 'numpy', 'spark', 'hadoop', 'data science', 'analytics',
            
            # Others
            'git', 'linux', 'unix', 'rest api', 'graphql', 'microservices', 'agile',
            'scrum', 'jira', 'confluence', 'html', 'css', 'json', 'xml'
        }
        
        found_terms = []
        for term in common_tech:
            if term in self.job_description_text:
                found_terms.append(term)
        
        return found_terms
    
    def _extract_soft_skills(self):
        """Extract soft skills mentioned in job description"""
        soft_skills_keywords = {
            'leadership', 'communication', 'teamwork', 'collaboration', 'problem solving',
            'project management', 'analytical', 'strategic thinking', 'innovation',
            'adaptability', 'critical thinking', 'decision making', 'mentoring'
        }
        
        found_skills = []
        for skill in soft_skills_keywords:
            if skill in self.job_description_text:
                found_skills.append(skill)
        
        return found_skills
    
    def match_keywords(self):
        """Match required keywords against resume"""
        self.matched_keywords = []
        self.missing_keywords = []
        
        # If no JD provided, use required_keywords
        keywords_to_check = self.required_keywords if self.required_keywords else self._get_default_keywords()
        
        for keyword in keywords_to_check:
            if self._keyword_in_resume(keyword):
                self.matched_keywords.append({
                    'keyword': keyword,
                    'frequency': self.resume_text.count(keyword.lower())
                })
            else:
                self.missing_keywords.append(keyword)
    
    def _keyword_in_resume(self, keyword):
        """Check if keyword appears in resume"""
        # Use word boundary matching for whole words
        pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
        return bool(re.search(pattern, self.resume_text))
    
    def _get_default_keywords(self):
        """Default important keywords if no JD provided"""
        return [
            'professional summary', 'work experience', 'education',
            'skills', 'technical', 'results', 'achieved', 'managed',
            'led', 'designed', 'implemented', 'developed'
        ]
    
    def check_formatting(self):
        """Check for ATS formatting issues"""
        self.formatting_issues = []
        resume_clean = self.resume_text_original
        
        # Check for common formatting problems
        checks = {
            'Unusual characters or symbols': r'[®™©§¶†‡]',
            'Table formatting detected': r'<table|┌|└|├|→|←',
            'Image or graphic content': r'\.(png|jpg|jpeg|gif|svg)\b|<img',
            'Headers/Footers detected': r'<header|<footer',
            'Multiple column layout': r'<col|column-layout',
            'Non-standard fonts': r'Symbol|Wingdings|Zapf|Dingbat',
            'Excessive special formatting': r'<style|<script|<div|<span',
            'PDF form detected': r'form field|fillable|acrobat',
        }
        
        for issue_name, pattern in checks.items():
            if re.search(pattern, resume_clean, re.IGNORECASE):
                self.formatting_issues.append({
                    'issue': issue_name,
                    'severity': 'medium',
                    'recommendation': f'Avoid {issue_name.lower()} - use plain text formatting'
                })
        
        # Check for contact info visibility
        if not self._check_contact_info():
            self.formatting_issues.append({
                'issue': 'No clear contact information',
                'severity': 'high',
                'recommendation': 'Include email and phone in plain text at top of resume'
            })
    
    def _check_contact_info(self):
        """Verify contact information is present"""
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        phone_pattern = r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}'
        
        has_email = bool(re.search(email_pattern, self.resume_text_original))
        has_phone = bool(re.search(phone_pattern, self.resume_text_original))
        
        return has_email and has_phone
    
    def calculate_scores(self):
        """Calculate ATS scores"""
        # Keyword match score (0-100)
        if self.required_keywords:
            match_percentage = len(self.matched_keywords) / len(self.required_keywords) * 100
            self.keyword_match_score = min(100, match_percentage)
        else:
            self.keyword_match_score = 100
        
        # Formatting score (0-100)
        # Deduct points for each issue
        formatting_deductions = len(self.formatting_issues) * 15
        self.formatting_score = max(0, 100 - formatting_deductions)
        
        # Content quality score based on length and structure
        content_score = self._calculate_content_score()
        
        # Overall ATS score (weighted average)
        self.overall_ats_score = (
            self.keyword_match_score * 0.5 +  # 50% keyword matching
            self.formatting_score * 0.3 +       # 30% formatting
            content_score * 0.2                 # 20% content quality
        )
        
        self.overall_ats_score = round(self.overall_ats_score, 1)
    
    def _calculate_content_score(self):
        """Calculate content quality score"""
        words = self.resume_text_original.split()
        word_count = len(words)
        
        # Resume should be 200-800 words ideally
        if 200 <= word_count <= 1000:
            score = 100
        elif 100 <= word_count < 200:
            score = 70
        elif word_count < 100:
            score = 50
        else:
            score = 90  # Slightly penalize very long resumes
        
        # Check for action verbs
        action_verbs = [
            'achieved', 'managed', 'led', 'designed', 'developed', 'implemented',
            'created', 'improved', 'optimized', 'increased', 'reduced', 'enhanced',
            'contributed', 'collaborated', 'directed', 'coordinated', 'established'
        ]
        
        action_verb_count = sum(1 for verb in action_verbs if verb in self.resume_text)
        if action_verb_count > 0:
            score = min(100, score + (action_verb_count * 2))
        else:
            score = max(50, score - 20)
        
        return min(100, score)
    
    def generate_recommendations(self):
        """Generate actionable recommendations"""
        self.recommendations = []
        
        # Keyword recommendations
        if self.missing_keywords:
            top_missing = self.missing_keywords[:5]
            self.recommendations.append({
                'category': 'Keywords',
                'priority': 'high' if len(self.missing_keywords) > 5 else 'medium',
                'action': f"Add these missing keywords: {', '.join(top_missing)}",
                'details': f'These keywords appear in the job description but not in your resume. Incorporate them naturally in your experience section.'
            })
        
        # Formatting recommendations
        if self.formatting_issues:
            high_severity = [i for i in self.formatting_issues if i.get('severity') == 'high']
            if high_severity:
                self.recommendations.append({
                    'category': 'Formatting',
                    'priority': 'high',
                    'action': f"Fix {len(high_severity)} critical formatting issues",
                    'details': '; '.join([i['recommendation'] for i in high_severity])
                })
        else:
            self.recommendations.append({
                'category': 'Formatting',
                'priority': 'low',
                'action': 'Your formatting looks ATS-friendly',
                'details': 'Keep using plain text without tables, images, or special formatting.'
            })
        
        # Structure recommendations
        if self.keyword_match_score < 50:
            self.recommendations.append({
                'category': 'Structure',
                'priority': 'high',
                'action': 'Restructure your experience bullets',
                'details': 'Use job description keywords in your bullet points. Match the language used in the job posting.'
            })
        
        # Length recommendations
        words = len(self.resume_text_original.split())
        if words < 200:
            self.recommendations.append({
                'category': 'Content',
                'priority': 'medium',
                'action': 'Expand your resume content',
                'details': 'Your resume is quite short. Add more accomplishments and details (target: 300-500 words).'
            })
        elif words > 1200:
            self.recommendations.append({
                'category': 'Content',
                'priority': 'medium',
                'action': 'Condense your resume',
                'details': 'Reduce to 1 page. Focus on most relevant experience and remove dated information.'
            })
        
        # Positive feedback
        if self.overall_ats_score >= 80:
            self.recommendations.append({
                'category': 'Overall',
                'priority': 'info',
                'action': '✓ Strong ATS compatibility',
                'details': 'Your resume has excellent ATS compatibility. Focus on tailoring content for specific roles.'
            })
