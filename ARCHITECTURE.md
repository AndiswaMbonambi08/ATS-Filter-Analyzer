# ATS Filter Analyzer - Architecture & Design

## System Overview

```
┌─────────────────────────────────────────────────────────┐
│                   Web Browser (UI)                      │
│              (HTML/CSS/JavaScript Frontend)             │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/JSON
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Flask Web Application                      │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Routes (API Endpoints)                           │  │
│  │ - POST /api/analyze                              │  │
│  │ - POST /api/job-description                      │  │
│  │ - GET /api/job-descriptions                      │  │
│  │ - GET /api/analyses                              │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Resume     │ │ ATS Analysis │ │   Database   │
│   Parser     │ │   Engine     │ │  (SQLite)    │
│              │ │              │ │              │
│ - Parse PDF  │ │ - Keyword    │ │ - Models     │
│ - Parse DOCX │ │   matching   │ │ - Data store │
│ - Parse TXT  │ │ - Scoring    │ │ - Queries    │
│              │ │ - Format     │ │              │
│              │ │   checking   │ │              │
└──────────────┘ └──────────────┘ └──────────────┘
```

## Architecture Layers

### 1. Presentation Layer (Frontend)
**File**: `templates/index.html`

**Responsibilities**:
- User interface for uploading resumes
- Job description input
- Real-time results display
- Visualization of scores and recommendations

**Key Features**:
- Drag-and-drop file upload
- Form validation
- Responsive design
- Smooth animations
- Error handling

### 2. Application Layer (Flask)
**File**: `app.py`

**Responsibilities**:
- HTTP request/response handling
- Route definitions
- Request validation
- Response formatting

**Routes**:
```
POST /api/analyze
├── Input: Resume file + Job description
├── Processing: Call ATSAnalyzer
└── Output: Analysis results JSON

POST /api/job-description
├── Input: Job details (title, company, description)
├── Processing: Extract keywords, save to DB
└── Output: Saved job ID

GET /api/job-descriptions
├── Input: None
├── Processing: Query database
└── Output: List of saved jobs

GET /api/analyses
├── Input: None
├── Processing: Query recent analyses
└── Output: Analysis history
```

### 3. Business Logic Layer
**Files**: `ats_analyzer.py`, `resume_parser.py`

#### Resume Parser
```python
ResumeParser
├── allowed_file() - Validate file type
├── parse() - Route to appropriate parser
│   ├── parse_pdf() - PDF extraction
│   ├── parse_docx() - DOCX extraction
│   └── parse_txt() - TXT reading
├── clean_text() - Normalize text
├── extract_contact_info() - Email/phone extraction
└── extract_sections() - Section identification
```

#### ATS Analyzer
```python
ATSAnalyzer
├── analyze() - Main analysis pipeline
├── extract_keywords_from_jd() - Keyword extraction
│   ├── _extract_tech_terms() - Technical skills
│   └── _extract_soft_skills() - Soft skills
├── match_keywords() - Compare resume vs JD
├── check_formatting() - ATS compatibility checks
├── calculate_scores() - Scoring algorithm
│   ├── Keyword match score (50%)
│   ├── Formatting score (30%)
│   └── Content quality score (20%)
└── generate_recommendations() - Action items
```

### 4. Data Layer
**File**: `models.py`

**Database Schema**:

```
JobDescription
├── id (PK)
├── title
├── company
├── description
├── keywords (JSON)
├── required_skills (JSON)
├── nice_to_have_skills (JSON)
├── created_at
└── updated_at

AnalysisResult
├── id (PK)
├── job_id (FK)
├── resume_text
├── resume_filename
├── keyword_match_score
├── formatting_score
├── overall_ats_score
├── matched_keywords (JSON)
├── missing_keywords (JSON)
├── formatting_issues (JSON)
├── recommendations (JSON)
├── ats_pass (boolean)
└── created_at

ATSKeywordLibrary
├── id (PK)
├── category
├── keyword
└── importance
```

## Data Flow

### Analysis Request Flow

```
1. User Uploads Resume
   └─> File received at frontend
   └─> FormData created with resume + job description
   └─> POST /api/analyze

2. Backend Processing
   └─> app.py: analyze_resume()
   └─> resume_parser.ResumeParser.parse()
   └─> Extract text from PDF/DOCX/TXT
   └─> ats_analyzer.ATSAnalyzer()
   
3. Analysis Pipeline
   └─> extract_keywords_from_jd()
       └─> Extract technical + soft skills
   └─> match_keywords()
       └─> Compare resume vs keywords
   └─> check_formatting()
       └─> Look for ATS red flags
   └─> calculate_scores()
       └─> Weighted scoring algorithm
   └─> generate_recommendations()
       └─> Create actionable feedback

4. Data Storage
   └─> Save AnalysisResult to database
   └─> Store matched/missing keywords as JSON
   └─> Store formatting issues and recommendations

5. Response
   └─> Return JSON with scores and details
   └─> Frontend receives response
   └─> Display results with animations
```

## Scoring Algorithm

### Keyword Match Score (50% of total)

```python
percentage = (matched_keywords / total_keywords) * 100
keyword_match_score = min(100, percentage)
```

**Algorithm**:
1. Extract keywords from job description
2. For each keyword, check if in resume using word boundary regex
3. Calculate match percentage
4. Cap at 100%

### Formatting Score (30% of total)

```python
formatting_deductions = len(formatting_issues) * 15
formatting_score = max(0, 100 - formatting_deductions)
```

**Checks**:
- Tables or columns detected
- Images or graphics
- Special fonts (Symbol, Wingdings)
- Header/footer content
- Non-standard formatting
- Missing contact info

### Content Quality Score (20% of total)

```
Word Count Check:
├─ 200-1000 words: 100 points
├─ 100-200 words: 70 points
├─ < 100 words: 50 points
└─ > 1000 words: 90 points

Action Verbs:
├─ +2 points per action verb found
└─ -20 points if none found
```

### Overall ATS Score

```python
overall_score = (
    keyword_match_score * 0.5 +
    formatting_score * 0.3 +
    content_score * 0.2
)
```

**Pass Threshold**: >= 60

## Configuration Management

**File**: `config.py`

```python
Config Classes:
├── DevelopmentConfig
│   └─ DEBUG = True
│   └─ SQLite database
│   └─ Hot reload enabled
│
├── ProductionConfig
│   └─ DEBUG = False
│   └─ PostgreSQL recommended
│   └─ Secure cookies
│
└── TestingConfig
    └─ In-memory database
    └─ Testing utilities enabled
```

## Error Handling

### Try-Catch Strategy

```
File Upload
├─> FileNotFoundError
├─> ValueError (invalid format)
└─> werkzeug.exceptions.RequestEntityTooLarge (>16MB)

Resume Parsing
├─> PyPDF2 errors
├─> docx parsing errors
└─> Encoding errors

Analysis
├─> NLP library errors
├─> Database errors
└─> Processing timeouts
```

### Error Responses

```json
{
    "error": "User-friendly error message",
    "status": 400,
    "details": "Technical details if DEBUG=True"
}
```

## Performance Optimizations

### Current
- Text-based keyword matching (fast)
- Simple SQLite database
- Synchronous processing

### Recommended Future
- Cache frequently used keywords
- Implement request queuing for large files
- Async processing with Celery
- Elasticsearch for resume indexing
- Redis for session management

## Security Considerations

### Implemented
- File type validation
- Filename sanitization
- Max file size limit (16MB)
- CSRF protection ready
- SQL injection prevention (SQLAlchemy)

### Recommended
- SSL/TLS in production (nginx.conf included)
- Rate limiting on API endpoints
- User authentication
- Encrypted database connections
- Input validation for all endpoints
- API key authentication

## Deployment Architecture

### Development
```
Local Machine
└─ python app.py
   └─ Flask development server
   └─ SQLite database
```

### Production (Docker)
```
Docker Container
└─ Gunicorn WSGI server (4 workers)
   └─ Flask application
   └─ SQLite database
└─ Exposed port 5000
```

### Production (With Nginx)
```
Internet
└─ Nginx (Reverse Proxy)
   ├─ SSL/TLS termination
   ├─ Static file serving
   └─ Load balancing
└─ Gunicorn workers
   ├─ Flask app instance 1
   ├─ Flask app instance 2
   ├─ Flask app instance 3
   └─ Flask app instance 4
└─ PostgreSQL database (recommended)
```

## Testing Strategy

### Unit Tests (`test_app.py`)

```
TestATSAnalyzer
├─ test_analyzer_initialization
├─ test_keyword_extraction
├─ test_keyword_matching
├─ test_formatting_check
├─ test_scoring
└─ test_full_analysis

TestFlaskApp
├─ test_index_page
├─ test_health_check
├─ test_analyze_endpoint
├─ test_save_job_description
└─ test_error_handling

TestResumeParser
├─ test_pdf_parsing
├─ test_docx_parsing
└─ test_text_parsing
```

## Scaling Considerations

### Current Limitations
- Single database (SQLite)
- Synchronous processing
- Monolithic application
- No caching

### Scaling Path
1. **Database**: SQLite → PostgreSQL
2. **Async**: Add Celery for background jobs
3. **Caching**: Redis for frequent queries
4. **API**: Add rate limiting, authentication
5. **Storage**: S3 for uploaded files
6. **Monitoring**: Logging, error tracking (Sentry)

## Future Enhancements

### Phase 2
- [ ] AI-powered rewriting suggestions
- [ ] Multi-language support
- [ ] Cover letter analysis
- [ ] Video interview tips

### Phase 3
- [ ] Integration with LinkedIn
- [ ] Resume templates
- [ ] Salary negotiation guide
- [ ] Interview preparation

### Phase 4
- [ ] Machine learning model training
- [ ] Predictive scoring
- [ ] Company-specific optimization
- [ ] Batch resume analysis

---

**Document Version**: 1.0
**Last Updated**: 2024
