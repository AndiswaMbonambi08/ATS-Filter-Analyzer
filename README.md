HEAD
# ATS Filter Analyzer 🎯

A powerful web application that analyzes resumes and CVs against Applicant Tracking System (ATS) filters to help candidates optimize their chances of passing automated screenings.

## ✨ Features

- **Resume Analysis**: Upload PDFs, DOCX, or TXT files for instant analysis
- **Keyword Matching**: Automatically extracts and matches keywords from job descriptions
- **ATS Scoring**: Comprehensive scoring across keyword matching, formatting, and content quality
- **Formatting Checks**: Detects ATS-unfriendly formatting issues (tables, images, special characters)
- **Actionable Recommendations**: Get specific, prioritized suggestions for improvement
- **Job Description Library**: Save and manage job descriptions for future analysis
- **Analytics Dashboard**: Track analysis history and trends

## 🛠 Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite (SQLAlchemy ORM)
- **NLP**: spaCy, NLTK, scikit-learn
- **File Parsing**: PyPDF2, python-docx
- **Frontend**: Vanilla JavaScript with modern CSS
- **Deployment**: can be deployed to Heroku, AWS, or any VPS

## 📋 Requirements

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

## 🚀 Quick Start

### 1. Clone or Download the Project

```bash
cd ats-analyzer
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Download spaCy language model:
```bash
python -m spacy download en_core_web_sm
```

### 4. Initialize Database

```bash
python init_db.py
```

This creates the SQLite database and adds sample data including:
- 2 sample job descriptions
- ATS keywords library with 50+ important keywords

### 5. Run the Application

```bash
python app.py
```

The app will start at `http://localhost:5000`

## 📱 Usage

### For Candidates

1. **Upload Your Resume**
   - Click the upload area or drag & drop
   - Supported formats: PDF, DOCX, TXT

2. **Paste Job Description**
   - Add the job title (optional)
   - Paste the full job description text

3. **Analyze**
   - Click "Analyze Resume"
   - Get instant feedback on ATS compatibility

4. **Review Results**
   - **Scores**: See keyword match, formatting, and overall ATS score
   - **Matched Keywords**: Keywords found in your resume
   - **Missing Keywords**: Add these to improve score
   - **Formatting Issues**: Fix any ATS-unfriendly elements
   - **Recommendations**: Prioritized action items

### Scoring Explained

- **Keyword Match Score (50% weight)**
  - How many important keywords from the job description appear in your resume
  - Target: 70%+ for ATS screening pass

- **Formatting Score (30% weight)**
  - Checks for ATS-unfriendly elements (tables, images, special chars)
  - Target: 90%+ clean formatting

- **Content Quality (20% weight)**
  - Resume length (200-1000 words ideal)
  - Use of action verbs and quantifiable achievements

- **Overall ATS Score**
  - Combined weighted score (0-100)
  - 60+ is typically needed to pass ATS screening

## 🏗 Project Structure

```
ats-analyzer/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── models.py              # SQLAlchemy database models
├── resume_parser.py       # Resume file parsing
├── ats_analyzer.py        # Core ATS analysis engine
├── init_db.py             # Database initialization script
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main HTML template
├── uploads/              # Temporary resume uploads
└── ats_analyzer.db       # SQLite database (auto-created)
```

## 📊 API Endpoints

### Analyze Resume
```
POST /api/analyze
Content-Type: multipart/form-data

Parameters:
- resume (file): Resume file
- job_description (string): Job description text
- job_title (string): Job title (optional)

Response:
{
  "success": true,
  "analysis_id": 1,
  "keyword_match_score": 75.5,
  "formatting_score": 95.0,
  "overall_ats_score": 82.3,
  "ats_pass": true,
  "matched_keywords": [...],
  "missing_keywords": [...],
  "formatting_issues": [...],
  "recommendations": [...]
}
```

### Save Job Description
```
POST /api/job-description
Content-Type: application/json

{
  "title": "Senior Developer",
  "company": "Company Name",
  "description": "Job description text..."
}
```

### Get Job Descriptions
```
GET /api/job-descriptions
```

### Get Analysis Result
```
GET /api/analysis/<id>
```

### Get Recent Analyses
```
GET /api/analyses
```

## 🎨 Frontend Features

### Modern Design
- Dark theme with cyan accent colors
- Responsive layout (mobile, tablet, desktop)
- Smooth animations and transitions
- Drag-and-drop file upload

### Real-time Feedback
- Live score calculations
- Animated progress bars
- Color-coded priority levels
- Detailed issue explanations

### Keyboard Shortcuts
- Tab through form fields
- Enter to submit (when focused on button)

## 🔧 Configuration

Edit `config.py` to customize:

```python
# File upload settings
UPLOAD_FOLDER = 'uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

# ATS Analysis
SCORE_THRESHOLD = 60  # Minimum passing score

# Database
SQLALCHEMY_DATABASE_URI = 'sqlite:///ats_analyzer.db'
```

## 🚢 Deployment

### AWS/EC2

```bash
# Install dependencies
sudo apt-get update
sudo apt-get install python3-pip python3-venv

# Clone and setup
git clone <repo>
cd ats-analyzer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:create_app()
```

### Docker

```dockerfile
FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

COPY . .

ENV FLASK_APP=app.py
RUN python init_db.py

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:create_app()"]
```

## 📈 Analysis Tips

### For Better Scores

1. **Keywords**
   - Use exact phrases from job description
   - Include technical tools and frameworks
   - Add soft skills when relevant
   - Use consistent terminology

2. **Formatting**
   - Keep it plain text or simple formatting
   - Avoid tables, images, unusual fonts
   - Use standard bullet points
   - Include contact info at the top

3. **Content**
   - 300-500 words ideal for one page
   - Start bullets with action verbs
   - Quantify achievements (increased by 25%, etc.)
   - Match the job description language

4. **Structure**
   - Professional Summary
   - Work Experience (most recent first)
   - Education
   - Skills (match job description)
   - Certifications/Awards (if relevant)

### Red Flags for ATS

- ❌ Tables or multi-column layouts
- ❌ Images, graphics, logos
- ❌ Unusual fonts (Comic Sans, Wingdings, etc.)
- ❌ Header/footer information
- ❌ Missing contact information
- ❌ Too short (<150 words)
- ❌ Too long (>1200 words)
- ❌ PDF forms or fillable fields
- ❌ Special Unicode characters

## 🐛 Troubleshooting

### PDF Parse Error
```
Error: "Could not parse PDF"
```
- Try converting PDF to DOCX in Word
- Ensure PDF is not encrypted
- Try text-based PDF (not image-based scan)

### Database Error
```
Error: "database is locked"
```
- Restart the application
- Check file permissions on `ats_analyzer.db`
- Delete `ats_analyzer.db` and run `python init_db.py` again

### Port Already in Use
```
Error: "Address already in use"
```
```bash
# Use different port
python app.py --port 5001

# Or kill process on port 5000
# Windows: netstat -ano | findstr :5000
# Linux: lsof -i :5000 && kill -9 <PID>
```

## 📚 Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [spaCy NLP Library](https://spacy.io/)
- [ATS Best Practices](https://www.indeed.com/resumes/)

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- [ ] Multi-language support
- [ ] LinkedIn integration
- [ ] Resume templates
- [ ] AI-powered rewriting suggestions
- [ ] Batch analysis
- [ ] Export detailed reports (PDF)
- [ ] Advanced analytics dashboard
- [ ] Cover letter analysis

## 🎯 Future Roadmap

- **v2.0**: AI-powered rewriting suggestions
- **v2.0**: Integration with job boards (LinkedIn, Indeed)
- **v2.0**: Resume templates with ATS best practices
- **v2.0**: Video interview preparation
- **v3.0**: Company-specific ATS optimization
- **v3.0**: Salary negotiation guide

## 💬 Support

For issues, questions, or suggestions:
1. Check the Troubleshooting section
2. Review sample analyses with `python init_db.py`
3. Check Flask logs for detailed error messages

## 🌟 Star on GitHub!

If this tool helps you land your next job, please star on GitHub and share with others!

---

**Status:** In Progress 🚧

## Screenshots

