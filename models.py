from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class JobDescription(db.Model):
    """Store job descriptions and their extracted keywords"""
    __tablename__ = 'job_descriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255))
    description = db.Column(db.Text, nullable=False)
    keywords = db.Column(db.Text)  # JSON string of keyword list
    required_skills = db.Column(db.Text)  # JSON string
    nice_to_have_skills = db.Column(db.Text)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    analyses = db.relationship('AnalysisResult', backref='job_description', lazy=True, cascade='all, delete-orphan')
    
    def set_keywords(self, keywords):
        """Store keywords as JSON"""
        self.keywords = json.dumps(keywords)
    
    def get_keywords(self):
        """Retrieve keywords from JSON"""
        return json.loads(self.keywords) if self.keywords else []
    
    def set_required_skills(self, skills):
        self.required_skills = json.dumps(skills)
    
    def get_required_skills(self):
        return json.loads(self.required_skills) if self.required_skills else []
    
    def set_nice_to_have_skills(self, skills):
        self.nice_to_have_skills = json.dumps(skills)
    
    def get_nice_to_have_skills(self):
        return json.loads(self.nice_to_have_skills) if self.nice_to_have_skills else []


class AnalysisResult(db.Model):
    """Store resume analysis results"""
    __tablename__ = 'analysis_results'
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job_descriptions.id'), nullable=True)
    resume_text = db.Column(db.Text, nullable=False)
    resume_filename = db.Column(db.String(255))
    
    # Scores
    keyword_match_score = db.Column(db.Float, default=0.0)
    formatting_score = db.Column(db.Float, default=0.0)
    overall_ats_score = db.Column(db.Float, default=0.0)
    
    # Detailed analysis
    matched_keywords = db.Column(db.Text)  # JSON string
    missing_keywords = db.Column(db.Text)  # JSON string
    formatting_issues = db.Column(db.Text)  # JSON string
    recommendations = db.Column(db.Text)  # JSON string
    ats_pass = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_matched_keywords(self, keywords):
        self.matched_keywords = json.dumps(keywords)
    
    def get_matched_keywords(self):
        return json.loads(self.matched_keywords) if self.matched_keywords else []
    
    def set_missing_keywords(self, keywords):
        self.missing_keywords = json.dumps(keywords)
    
    def get_missing_keywords(self):
        return json.loads(self.missing_keywords) if self.missing_keywords else []
    
    def set_formatting_issues(self, issues):
        self.formatting_issues = json.dumps(issues)
    
    def get_formatting_issues(self):
        return json.loads(self.formatting_issues) if self.formatting_issues else []
    
    def set_recommendations(self, recommendations):
        self.recommendations = json.dumps(recommendations)
    
    def get_recommendations(self):
        return json.loads(self.recommendations) if self.recommendations else []


class ATSKeywordLibrary(db.Model):
    """Common ATS keywords and technical terms"""
    __tablename__ = 'ats_keyword_library'
    
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100))  # e.g., 'Programming', 'Leadership', 'Tools'
    keyword = db.Column(db.String(255), unique=True, nullable=False)
    importance = db.Column(db.String(20), default='medium')  # high, medium, low
    
    def __repr__(self):
        return f"<ATSKeyword {self.keyword}>"
