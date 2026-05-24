import pytest
import json
from io import BytesIO
from pathlib import Path
from app import create_app, db
from models import JobDescription, AnalysisResult
from ats_analyzer import ATSAnalyzer


@pytest.fixture
def app():
    """Create Flask app for testing"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Flask test client"""
    return app.test_client()


@pytest.fixture
def sample_resume():
    """Sample resume text"""
    return """
    JOHN DOE
    john.doe@email.com | (555) 123-4567
    
    PROFESSIONAL SUMMARY
    Senior Python Developer with 5+ years of experience in building scalable web applications
    using Django and Flask. Proficient in PostgreSQL, Docker, and AWS cloud services.
    
    WORK EXPERIENCE
    
    Senior Developer | Tech Company (2022-Present)
    - Designed and implemented microservices architecture using Python and Docker
    - Optimized database queries reducing response time by 40%
    - Led team of 3 junior developers on major feature releases
    - Managed CI/CD pipelines using Jenkins and GitLab CI
    
    Full Stack Developer | StartupXYZ (2020-2022)
    - Built REST APIs using Flask and SQLAlchemy
    - Developed React frontend for real-time data visualization
    - Implemented automated testing with pytest, achieving 85% code coverage
    - Deployed applications on AWS EC2 and S3
    
    EDUCATION
    Bachelor of Science in Computer Science | University (2019)
    
    SKILLS
    Languages: Python, JavaScript, SQL
    Frameworks: Django, Flask, React
    Databases: PostgreSQL, MongoDB, Redis
    Tools: Docker, Kubernetes, Git, Jenkins
    Cloud: AWS, Google Cloud Platform
    """


@pytest.fixture
def sample_job_description():
    """Sample job description"""
    return """
    Senior Python Developer Position
    
    We are seeking an experienced Senior Python Developer to join our team.
    
    Required Skills:
    - Python 3.7+
    - Django or Flask
    - PostgreSQL or MySQL
    - REST API development
    - Git version control
    - Docker
    - AWS
    
    Nice to Have:
    - Kubernetes experience
    - Machine Learning basics
    - React or Vue.js
    
    Responsibilities:
    - Design scalable web applications
    - Write clean, maintainable code
    - Conduct code reviews
    - Mentor junior developers
    """


class TestATSAnalyzer:
    """Test ATS Analyzer core functionality"""
    
    def test_analyzer_initialization(self, sample_resume, sample_job_description):
        """Test analyzer initialization"""
        analyzer = ATSAnalyzer(sample_resume, sample_job_description)
        assert analyzer.resume_text is not None
        assert analyzer.job_description_text is not None
    
    def test_keyword_extraction(self, sample_resume, sample_job_description):
        """Test keyword extraction from job description"""
        analyzer = ATSAnalyzer(sample_resume, sample_job_description)
        analyzer.extract_keywords_from_jd()
        assert len(analyzer.required_keywords) > 0
        assert 'python' in [k.lower() for k in analyzer.required_keywords]
    
    def test_keyword_matching(self, sample_resume, sample_job_description):
        """Test keyword matching"""
        analyzer = ATSAnalyzer(sample_resume, sample_job_description)
        analyzer.extract_keywords_from_jd()
        analyzer.match_keywords()
        
        assert len(analyzer.matched_keywords) > 0
        assert any('python' in str(k).lower() for k in analyzer.matched_keywords)
    
    def test_formatting_check(self, sample_resume):
        """Test formatting checks"""
        analyzer = ATSAnalyzer(sample_resume)
        analyzer.check_formatting()
        
        # Sample resume should have good formatting
        assert analyzer.formatting_score > 70
    
    def test_scoring(self, sample_resume, sample_job_description):
        """Test scoring calculation"""
        analyzer = ATSAnalyzer(sample_resume, sample_job_description)
        analyzer.analyze()
        
        assert 0 <= analyzer.overall_ats_score <= 100
        assert 0 <= analyzer.keyword_match_score <= 100
        assert 0 <= analyzer.formatting_score <= 100
    
    def test_full_analysis(self, sample_resume, sample_job_description):
        """Test full analysis pipeline"""
        analyzer = ATSAnalyzer(sample_resume, sample_job_description)
        results = analyzer.analyze()
        
        assert 'matched_keywords' in results
        assert 'missing_keywords' in results
        assert 'formatting_issues' in results
        assert 'recommendations' in results
        assert 'overall_ats_score' in results
        assert 'ats_pass' in results
    
    def test_low_quality_resume(self):
        """Test analysis on low-quality resume"""
        bad_resume = "Resume"
        jd = "Python Django Flask PostgreSQL AWS Docker Kubernetes"
        
        analyzer = ATSAnalyzer(bad_resume, jd)
        results = analyzer.analyze()
        
        assert results['overall_ats_score'] < 50
        assert len(results['recommendations']) > 0


class TestFlaskApp:
    """Test Flask application endpoints"""
    
    def test_index_page(self, client):
        """Test index page loads"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'ATS' in response.data
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get('/api/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
    
    def test_analyze_missing_file(self, client, sample_job_description):
        """Test analyze endpoint without file"""
        response = client.post('/api/analyze', data={
            'job_description': sample_job_description,
            'job_title': 'Test'
        })
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_save_job_description(self, client, sample_job_description):
        """Test saving job description"""
        response = client.post('/api/job-description',
            json={
                'title': 'Test Job',
                'company': 'Test Company',
                'description': sample_job_description
            },
            content_type='application/json'
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'job_id' in data
    
    def test_list_job_descriptions(self, client, sample_job_description):
        """Test listing job descriptions"""
        # Save a job first
        client.post('/api/job-description',
            json={
                'title': 'Test Job',
                'company': 'Test Company',
                'description': sample_job_description
            },
            content_type='application/json'
        )
        
        # List jobs
        response = client.get('/api/job-descriptions')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert len(data['jobs']) > 0
    
    def test_404_error(self, client):
        """Test 404 error handling"""
        response = client.get('/nonexistent')
        assert response.status_code == 404


class TestResumeParser:
    """Test resume parsing functionality"""
    
    def test_text_file_parsing(self, sample_resume):
        """Test basic text parsing"""
        from resume_parser import ResumeParser
        
        # Create temp file
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(sample_resume)
            temp_path = f.name
        
        try:
            text = ResumeParser.parse(temp_path)
            assert 'JOHN DOE' in text
            assert 'Senior Developer' in text
        finally:
            Path(temp_path).unlink()
    
    def test_allowed_file(self):
        """Test file extension validation"""
        from resume_parser import ResumeParser
        
        assert ResumeParser.allowed_file('resume.pdf')
        assert ResumeParser.allowed_file('cv.docx')
        assert ResumeParser.allowed_file('resume.txt')
        assert not ResumeParser.allowed_file('resume.exe')
        assert not ResumeParser.allowed_file('resume.html')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
