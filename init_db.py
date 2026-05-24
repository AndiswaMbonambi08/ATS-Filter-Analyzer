#!/usr/bin/env python
"""Initialize the ATS Analyzer database with sample data"""

import os
from app import create_app, db
from models import JobDescription, ATSKeywordLibrary

# Sample job descriptions
SAMPLE_JOBS = [
    {
        'title': 'Senior Python Developer',
        'company': 'Tech Company ABC',
        'description': '''
        We are seeking a Senior Python Developer with 5+ years of experience.
        
        Required Skills:
        - Python 3.7+
        - Django or Flask
        - PostgreSQL or MySQL
        - REST API development
        - Git version control
        - Linux/Unix
        - Docker and Kubernetes
        - AWS or GCP
        
        Nice to Have:
        - Machine Learning experience (TensorFlow, PyTorch)
        - Redis caching
        - Microservices architecture
        - CI/CD pipelines (Jenkins, GitLab CI)
        - Agile/Scrum experience
        
        Responsibilities:
        - Design and develop scalable web applications
        - Write clean, maintainable code
        - Conduct code reviews
        - Mentor junior developers
        - Collaborate with cross-functional teams
        '''
    },
    {
        'title': 'Full Stack JavaScript Engineer',
        'company': 'Web Startup XYZ',
        'description': '''
        Join our dynamic team as a Full Stack JavaScript Engineer.
        
        Requirements:
        - JavaScript/TypeScript (3+ years)
        - React or Vue.js
        - Node.js and Express
        - MongoDB or PostgreSQL
        - RESTful API design
        - HTML5 & CSS3
        - Git
        - Testing frameworks (Jest, Mocha)
        
        Preferred:
        - GraphQL experience
        - Docker
        - AWS deployment
        - Agile methodology
        - Open source contributions
        
        You will:
        - Build responsive web applications
        - Develop backend services
        - Optimize application performance
        - Work in agile sprints
        - Contribute to architecture decisions
        '''
    }
]

# ATS Keywords Library
ATS_KEYWORDS = [
    # Technical Skills
    ('Python', 'Programming', 'high'),
    ('Java', 'Programming', 'high'),
    ('JavaScript', 'Programming', 'high'),
    ('C++', 'Programming', 'medium'),
    ('C#', 'Programming', 'medium'),
    ('Ruby', 'Programming', 'medium'),
    ('Go', 'Programming', 'medium'),
    ('Rust', 'Programming', 'medium'),
    
    # Web Frameworks
    ('Django', 'Framework', 'high'),
    ('Flask', 'Framework', 'high'),
    ('React', 'Framework', 'high'),
    ('Angular', 'Framework', 'high'),
    ('Vue.js', 'Framework', 'high'),
    ('Express.js', 'Framework', 'high'),
    ('Spring', 'Framework', 'high'),
    ('FastAPI', 'Framework', 'medium'),
    
    # Databases
    ('SQL', 'Database', 'high'),
    ('PostgreSQL', 'Database', 'high'),
    ('MySQL', 'Database', 'high'),
    ('MongoDB', 'Database', 'high'),
    ('Redis', 'Database', 'medium'),
    ('Elasticsearch', 'Database', 'medium'),
    ('DynamoDB', 'Database', 'medium'),
    
    # Cloud & DevOps
    ('AWS', 'Cloud', 'high'),
    ('Azure', 'Cloud', 'high'),
    ('Google Cloud', 'Cloud', 'high'),
    ('Docker', 'DevOps', 'high'),
    ('Kubernetes', 'DevOps', 'high'),
    ('CI/CD', 'DevOps', 'high'),
    ('Jenkins', 'DevOps', 'medium'),
    ('Terraform', 'DevOps', 'medium'),
    
    # Data & ML
    ('Machine Learning', 'Data', 'high'),
    ('TensorFlow', 'Data', 'medium'),
    ('PyTorch', 'Data', 'medium'),
    ('Pandas', 'Data', 'medium'),
    ('Scikit-learn', 'Data', 'medium'),
    ('Data Analysis', 'Data', 'high'),
    ('Big Data', 'Data', 'medium'),
    
    # Soft Skills
    ('Leadership', 'Soft Skill', 'high'),
    ('Communication', 'Soft Skill', 'high'),
    ('Project Management', 'Soft Skill', 'high'),
    ('Teamwork', 'Soft Skill', 'high'),
    ('Problem Solving', 'Soft Skill', 'high'),
    ('Agile', 'Soft Skill', 'high'),
    ('Scrum', 'Soft Skill', 'medium'),
    ('Critical Thinking', 'Soft Skill', 'medium'),
    
    # Other Tools
    ('Git', 'Tools', 'high'),
    ('REST API', 'Tools', 'high'),
    ('Linux', 'Tools', 'high'),
    ('GraphQL', 'Tools', 'medium'),
    ('Microservices', 'Architecture', 'high'),
    ('Object-Oriented Programming', 'Concepts', 'high'),
]


def init_database():
    """Initialize database with sample data"""
    app = create_app('development')
    
    with app.app_context():
        # Drop all tables and recreate (be careful with this!)
        db.drop_all()
        db.create_all()
        print("✓ Database tables created")
        
        # Add sample job descriptions
        for job_data in SAMPLE_JOBS:
            job = JobDescription(**job_data)
            db.session.add(job)
        db.session.commit()
        print(f"✓ Added {len(SAMPLE_JOBS)} sample job descriptions")
        
        # Add ATS keywords
        for keyword, category, importance in ATS_KEYWORDS:
            kw = ATSKeywordLibrary(
                keyword=keyword,
                category=category,
                importance=importance
            )
            db.session.add(kw)
        db.session.commit()
        print(f"✓ Added {len(ATS_KEYWORDS)} keywords to library")
        
        print("\n✓ Database initialization complete!")
        print("\nYou can now start the app with: python app.py")


if __name__ == '__main__':
    init_database()
