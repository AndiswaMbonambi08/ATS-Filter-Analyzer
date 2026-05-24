import os
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from datetime import datetime
import json

from config import config
from models import db, JobDescription, AnalysisResult, ATSKeywordLibrary
from resume_parser import ResumeParser
from ats_analyzer import ATSAnalyzer


def create_app(config_name=None):
    """Application factory"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Create upload folder if doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize extensions
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    # Register blueprints and routes
    register_routes(app)
    
    return app


def register_routes(app):
    """Register Flask routes"""
    
    @app.route('/')
    def index():
        """Home page"""
        return render_template('index.html')
    
    @app.route('/api/analyze', methods=['POST'])
    def analyze_resume():
        """Analyze resume against job description"""
        try:
            # Check if file is present
            if 'resume' not in request.files:
                return jsonify({'error': 'No resume file provided'}), 400
            
            resume_file = request.files['resume']
            if resume_file.filename == '':
                return jsonify({'error': 'No selected file'}), 400
            
            if not ResumeParser.allowed_file(resume_file.filename):
                return jsonify({'error': 'Only PDF, DOCX, and TXT files are allowed'}), 400
            
            # Get job description from form
            job_description = request.form.get('job_description', '')
            job_title = request.form.get('job_title', 'Analysis')
            
            # Save uploaded file
            filename = secure_filename(resume_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            resume_file.save(filepath)
            
            # Parse resume
            resume_text = ResumeParser.parse(filepath)
            resume_text_clean = ResumeParser.clean_text(resume_text)
            
            # Analyze with ATS
            analyzer = ATSAnalyzer(resume_text, job_description)
            results = analyzer.analyze()
            
            # Save to database
            analysis = AnalysisResult(
                resume_text=resume_text_clean,
                resume_filename=filename,
                keyword_match_score=results['keyword_match_score'],
                formatting_score=results['formatting_score'],
                overall_ats_score=results['overall_ats_score'],
                ats_pass=results['ats_pass']
            )
            analysis.set_matched_keywords(results['matched_keywords'])
            analysis.set_missing_keywords(results['missing_keywords'])
            analysis.set_formatting_issues(results['formatting_issues'])
            analysis.set_recommendations(results['recommendations'])
            
            db.session.add(analysis)
            db.session.commit()
            
            # Return results
            return jsonify({
                'success': True,
                'analysis_id': analysis.id,
                'job_title': job_title,
                'matched_keywords': results['matched_keywords'][:10],
                'missing_keywords': results['missing_keywords'][:10],
                'formatting_issues': results['formatting_issues'],
                'recommendations': results['recommendations'],
                'keyword_match_score': results['keyword_match_score'],
                'formatting_score': results['formatting_score'],
                'overall_ats_score': results['overall_ats_score'],
                'ats_pass': results['ats_pass'],
                'timestamp': datetime.now().isoformat()
            }), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            # Clean up uploaded file
            if 'filepath' in locals() and os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except:
                    pass
    
    @app.route('/api/job-description', methods=['POST'])
    def save_job_description():
        """Save a job description for later analysis"""
        try:
            data = request.get_json()
            
            jd = JobDescription(
                title=data.get('title', 'Untitled'),
                company=data.get('company', ''),
                description=data.get('description', '')
            )
            
            # Extract and store keywords
            analyzer = ATSAnalyzer(data.get('description', ''), data.get('description', ''))
            analyzer.extract_keywords_from_jd()
            jd.set_keywords(analyzer.required_keywords)
            
            db.session.add(jd)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'job_id': jd.id,
                'message': 'Job description saved successfully'
            }), 201
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/job-descriptions', methods=['GET'])
    def list_job_descriptions():
        """Get all saved job descriptions"""
        try:
            jobs = JobDescription.query.all()
            return jsonify({
                'success': True,
                'jobs': [{
                    'id': job.id,
                    'title': job.title,
                    'company': job.company,
                    'created_at': job.created_at.isoformat(),
                    'keyword_count': len(job.get_keywords())
                } for job in jobs]
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/job-descriptions/<int:job_id>', methods=['GET'])
    def get_job_description(job_id):
        """Get a specific job description"""
        try:
            job = JobDescription.query.get_or_404(job_id)
            return jsonify({
                'success': True,
                'job': {
                    'id': job.id,
                    'title': job.title,
                    'company': job.company,
                    'description': job.description,
                    'keywords': job.get_keywords(),
                    'created_at': job.created_at.isoformat()
                }
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/analysis/<int:analysis_id>', methods=['GET'])
    def get_analysis(analysis_id):
        """Get a previous analysis result"""
        try:
            analysis = AnalysisResult.query.get_or_404(analysis_id)
            return jsonify({
                'success': True,
                'analysis': {
                    'id': analysis.id,
                    'resume_filename': analysis.resume_filename,
                    'matched_keywords': analysis.get_matched_keywords(),
                    'missing_keywords': analysis.get_missing_keywords(),
                    'formatting_issues': analysis.get_formatting_issues(),
                    'recommendations': analysis.get_recommendations(),
                    'keyword_match_score': analysis.keyword_match_score,
                    'formatting_score': analysis.formatting_score,
                    'overall_ats_score': analysis.overall_ats_score,
                    'ats_pass': analysis.ats_pass,
                    'created_at': analysis.created_at.isoformat()
                }
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/analyses', methods=['GET'])
    def list_analyses():
        """Get recent analyses"""
        try:
            analyses = AnalysisResult.query.order_by(AnalysisResult.created_at.desc()).limit(10).all()
            return jsonify({
                'success': True,
                'analyses': [{
                    'id': analysis.id,
                    'resume_filename': analysis.resume_filename,
                    'overall_ats_score': analysis.overall_ats_score,
                    'ats_pass': analysis.ats_pass,
                    'created_at': analysis.created_at.isoformat()
                } for analysis in analyses]
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({'status': 'healthy'}), 200
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
