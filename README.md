HEAD
# ATS Filter Analyzer 🎯

Built after seeing how often qualified candidates, including myself, get filtered out by ATS software before a human ever reads their resume, often over fixable issues like missing keywords or formatting the system can't parse.

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
- **NLP**: Text Processing: scikit-learn (TF-IDF), regex-based keyword extraction
- **File Parsing**: PyPDF2, python-docx
- **Frontend**: Vanilla JavaScript with modern CSS
- **Deployment**: Configured for Render, Railway, or any Python-compatible host (via Procfile)

## 📋 Requirements

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

## 🚀 Quick Start

### 1. Clone or Download the Project

```bash
git clone https://github.com/AndiswaMbonambi08/ATS-Filter-Analyzer.git
cd ATS-Filter-Analyzer
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


## Screenshots

<img width="1844" height="1024" alt="Screenshot_25-5-2026_182937_127 0 0 1" src="https://github.com/user-attachments/assets/67fad97d-a53c-4d82-a661-6ebcb903da1e" />

<img width="1835" height="1024" alt="Screenshot_25-5-2026_18911_127 0 0 1" src="https://github.com/user-attachments/assets/6217f383-de07-4544-86b9-4c637b0b76ed" />

<img width="1838" height="1024" alt="Screenshot_25-5-2026_18957_127 0 0 1" src="https://github.com/user-attachments/assets/3cfc5345-7d43-444b-a672-a06cd0a7fa22" />

<img width="1836" height="1024" alt="Screenshot_25-5-2026_18040_127 0 0 1" src="https://github.com/user-attachments/assets/bb489a8b-1c1d-4707-bce1-48a4577f76b5" />




