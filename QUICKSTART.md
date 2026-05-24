# ATS Filter Analyzer - Quick Start Guide

Welcome! This guide will get you up and running in 5 minutes.

## Prerequisites

- Python 3.8 or higher
- A code editor (VS Code, PyCharm, etc.)
- Terminal/Command Prompt

## Step-by-Step Setup

### Step 1: Download & Open Project (1 min)

1. Download the ATS Analyzer project files
2. Open a terminal/command prompt
3. Navigate to the project directory:
   ```bash
   cd path/to/ats-analyzer
   ```

### Step 2: Create Virtual Environment (1 min)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the beginning of your terminal line.

### Step 3: Install Dependencies (2 min)

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

This installs all required packages and downloads the language model.

### Step 4: Initialize Database (30 sec)

```bash
python init_db.py
```

You'll see:
```
✓ Database tables created
✓ Added 2 sample job descriptions
✓ Added 50 keywords to library
✓ Database initialization complete!
```

### Step 5: Start the Application (1 min)

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

Open your browser and go to: **http://localhost:5000**

## First Run

### Demo Analysis

1. **Get a Sample Resume**
   - Copy the sample resume from `test_app.py` (lines 24-60)
   - Or use your own resume

2. **Get a Sample Job Description**
   - Copy the sample JD from `test_app.py` (lines 65-87)
   - Or use the ones in `init_db.py`

3. **Upload & Analyze**
   - Click "Upload Resume"
   - Paste the job description
   - Click "Analyze Resume"
   - See your ATS score and recommendations!

## File Formats Accepted

✓ **PDF** - Most common format
✓ **DOCX** - Microsoft Word
✓ **TXT** - Plain text files

## Understanding Your Score

### Score Breakdown

| Score | What It Means |
|-------|--------------|
| 80-100 | ✓ Excellent - Likely to pass ATS |
| 60-79 | ⚠ Good - Should pass most systems |
| 40-59 | ⚠ Fair - At risk, make improvements |
| 0-39 | ✗ Poor - Likely to be filtered out |

### Three Components

1. **Keyword Match (50%)**
   - How many job keywords appear in your resume
   - Higher = more matches

2. **Formatting (30%)**
   - How ATS-friendly your resume layout is
   - No tables, images, or special characters

3. **Content Quality (20%)**
   - Length, action verbs, achievements
   - 300-500 words is ideal

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'spacy'"

**Solution:**
```bash
pip install spacy
python -m spacy download en_core_web_sm
```

### Issue: Port 5000 Already in Use

**Solution:**
```bash
python app.py --port 5001
```

### Issue: "Permission Denied" Error

**Solution (Windows):**
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Solution (Mac/Linux):**
```bash
chmod +x venv/bin/activate
```

### Issue: Database "Locked" Error

**Solution:**
```bash
# Delete the database
rm ats_analyzer.db

# Recreate it
python init_db.py
```

## What Each File Does

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application |
| `models.py` | Database structure |
| `ats_analyzer.py` | ATS analysis logic |
| `resume_parser.py` | Resume file parsing |
| `config.py` | Settings |
| `templates/index.html` | Web interface |
| `init_db.py` | Database setup |

## Next Steps

### Basic Features
- [x] Analyze resume against job description
- [x] View keyword matches
- [x] Get formatting feedback
- [x] See recommendations

### Try These:
1. **Test with Multiple Formats**
   - Save resume as PDF, DOCX, and TXT
   - See how format affects scores

2. **Try Different Jobs**
   - Tech job descriptions
   - Non-tech jobs
   - Different industries

3. **Improve Your Score**
   - Add missing keywords
   - Fix formatting issues
   - Follow recommendations

## Advanced Usage

### Save Job Descriptions

```bash
# Use the API
curl -X POST http://localhost:5000/api/job-description \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Developer",
    "company": "Tech Corp",
    "description": "Job description text..."
  }'
```

### Run Tests

```bash
pip install -r requirements-dev.txt
pytest test_app.py -v
```

### Deploy to Heroku

1. Create Heroku account
2. Install Heroku CLI
3. Run:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

## Tips for Best Results

### Resume Tips
- ✓ Use keywords from the job description
- ✓ Quantify achievements (increased by 25%)
- ✓ Use action verbs (led, designed, implemented)
- ✓ Keep it to 1-2 pages
- ✓ Use standard formatting

### ATS-Friendly Formatting
- ✓ Plain text or simple formatting
- ✓ Standard fonts (Arial, Calibri, Times)
- ✓ Single column layout
- ✓ No tables or graphics
- ✓ Contact info at the top

### Keywords to Include
- Technical skills from job description
- Tool names (Python, Docker, AWS, etc.)
- Soft skills (leadership, communication)
- Certifications and awards
- Industry-specific terminology

## Getting Help

### Check These Resources
1. `README.md` - Full documentation
2. `test_app.py` - Code examples
3. Flask docs: https://flask.palletsprojects.com/
4. GitHub issues (if available)

### Debug Mode

To see detailed logs:
```bash
# Edit config.py
DEBUG = True

# Run with verbose output
python app.py --debug
```

## Congratulations! 🎉

You're all set up! Start analyzing your resume and optimizing it for ATS success.

---

**Questions?** Check the full README.md file for comprehensive documentation.

**Ready to land that job!** 🚀
