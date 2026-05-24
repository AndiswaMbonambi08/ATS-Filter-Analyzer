# ATS Filter Analyzer - Complete Step-by-Step Setup Guide

## For Complete Beginners

This guide walks you through every single step. It should take about 15-20 minutes.

---

## PART 1: PREPARE YOUR COMPUTER (5 minutes)

### Step 1: Check if Python is Installed

**Windows:**
1. Press `Win + R` (opens Run dialog)
2. Type: `cmd` and press Enter
3. In the black window that opens, type:
   ```
   python --version
   ```
4. Press Enter

**Mac/Linux:**
1. Open Terminal (Cmd+Space, type "Terminal", press Enter)
2. Type:
   ```
   python3 --version
   ```
3. Press Enter

**Expected result:** You should see something like `Python 3.11.6` or higher

**If you don't have Python:**
- Go to https://www.python.org/downloads/
- Click "Download Python 3.11" (or latest)
- Run the installer
- ⚠️ **IMPORTANT**: Check the box "Add Python to PATH"
- Click "Install Now"
- Wait for installation to complete
- Restart your terminal/command prompt

---

## PART 2: DOWNLOAD AND ORGANIZE FILES (3 minutes)

### Step 2: Create a Project Folder

**Windows:**
1. Open File Explorer
2. Go to Documents folder
3. Right-click → "New Folder"
4. Name it: `ats-analyzer`
5. Double-click to open it

**Mac/Linux:**
1. Open Finder (Mac) or File Manager (Linux)
2. Create a new folder called `ats-analyzer`
3. Open the folder

### Step 3: Download All Project Files

You already downloaded all the files. Now put them in the folder:

1. Download all the files from the output folder
2. Extract them (if they're in a .zip)
3. Move ALL files into your `ats-analyzer` folder

**Your folder should look like this:**
```
ats-analyzer/
├── app.py
├── config.py
├── models.py
├── ats_analyzer.py
├── resume_parser.py
├── init_db.py
├── test_app.py
├── templates/
│   └── index.html
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── Procfile
├── runtime.txt
├── nginx.conf
├── README.md
├── QUICKSTART.md
├── ARCHITECTURE.md
├── INDEX.md
└── (other files)
```

---

## PART 3: OPEN A TERMINAL IN YOUR PROJECT FOLDER (2 minutes)

### Step 4: Open Terminal/Command Prompt in the Right Location

**Windows:**
1. Open your `ats-analyzer` folder
2. Click on the address bar at the top (where it shows the folder path)
3. Type: `cmd` and press Enter
4. A black command prompt window opens in that folder ✓

**Mac:**
1. Open the `ats-analyzer` folder in Finder
2. Right-click anywhere in the folder
3. Select "New Terminal at Folder"
4. Terminal opens ✓

**Linux:**
1. Right-click in the `ats-analyzer` folder
2. Select "Open Terminal Here"
3. Terminal opens ✓

**Verify it worked:** Type `dir` (Windows) or `ls` (Mac/Linux) and press Enter. You should see the files listed.

---

## PART 4: CREATE VIRTUAL ENVIRONMENT (3 minutes)

A virtual environment is like a "sandbox" where we install Python packages just for this project.

### Step 5: Create Virtual Environment

**Windows:**
```
python -m venv venv
```

**Mac/Linux:**
```
python3 -m venv venv
```

Press Enter and wait 30 seconds. You should see no errors.

**Verify it worked:** Look in your folder - you should see a new folder named `venv` created.

### Step 6: Activate Virtual Environment

**Windows:**
```
venv\Scripts\activate
```

**Mac/Linux:**
```
source venv/bin/activate
```

Press Enter.

**How to know it worked:** Your terminal line should start with `(venv)` now.

**Example:**
```
(venv) C:\Users\YourName\Documents\ats-analyzer>
```

✓ If you see `(venv)` at the beginning, you're good!

---

## PART 5: INSTALL PACKAGES (4 minutes)

### Step 7: Install Python Dependencies

Copy and paste this command (make sure you're still in the terminal with `(venv)` showing):

```
pip install -r requirements.txt
```

Press Enter and wait. It will download and install about 10-15 packages. This might take 2-3 minutes.

**What to expect:**
```
Collecting Flask==2.3.3
Downloading Flask-2.3.3-py3-none-any.whl
...
Successfully installed Flask-2.3.3 ...
```

**If you see errors:** Try this instead:
```
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 8: Download NLP Model

This is needed for keyword extraction. Copy and paste:

```
python -m spacy download en_core_web_sm
```

Press Enter and wait about 1-2 minutes for it to download (~40MB).

**Verify it worked:** If it ends with "✓ Download successful", you're done!

---

## PART 6: SET UP DATABASE (2 minutes)

### Step 9: Initialize Database with Sample Data

The database is where we store analysis results. Let's create it and add sample data:

```
python init_db.py
```

Press Enter and wait 10 seconds.

**Expected output:**
```
✓ Database tables created
✓ Added 2 sample job descriptions
✓ Added 50 keywords to library
✓ Database initialization complete!
```

**What was created:**
- `ats_analyzer.db` file (the database)
- Sample job descriptions for testing
- Keyword library for analysis

---

## PART 7: START THE APPLICATION (1 minute)

### Step 10: Run the Flask Application

```
python app.py
```

Press Enter.

**Expected output:**
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

**Important:** Keep this terminal window open! The app is now running.

---

## PART 8: OPEN IN BROWSER (1 minute)

### Step 11: Open the Web Interface

1. Open any web browser (Chrome, Firefox, Safari, Edge, etc.)
2. In the address bar, type:
   ```
   http://localhost:5000
   ```
3. Press Enter

**Expected result:** You should see the ATS Filter Analyzer interface with:
- A logo saying "ATS Analyzer"
- An upload area for resumes
- A text box for job descriptions
- An "Analyze Resume" button

✅ **Congratulations! The app is running!**

---

## PART 9: TEST IT WITH SAMPLE DATA (3 minutes)

### Step 12: Create a Test Resume

Let's test it with sample data:

1. **Create a test file:**
   - Open Notepad (Windows) or TextEdit (Mac)
   - Copy this text:
   ```
   JOHN DOE
   john.doe@email.com | (555) 123-4567
   
   PROFESSIONAL SUMMARY
   Senior Python Developer with 5+ years of experience in building 
   scalable web applications using Django and Flask. Proficient in 
   PostgreSQL, Docker, and AWS cloud services.
   
   WORK EXPERIENCE
   
   Senior Developer | Tech Company (2022-Present)
   - Designed and implemented microservices architecture using Python and Docker
   - Optimized database queries reducing response time by 40%
   - Led team of 3 junior developers on major feature releases
   
   Full Stack Developer | StartupXYZ (2020-2022)
   - Built REST APIs using Flask and SQLAlchemy
   - Developed React frontend for real-time data visualization
   - Implemented automated testing with pytest
   
   EDUCATION
   Bachelor of Science in Computer Science | University (2019)
   
   SKILLS
   Languages: Python, JavaScript, SQL
   Frameworks: Django, Flask, React
   Databases: PostgreSQL, MongoDB, Redis
   Tools: Docker, Kubernetes, Git, Jenkins
   Cloud: AWS, Google Cloud Platform
   ```

2. **Save it:**
   - Click "Save"
   - Name it: `sample_resume.txt`
   - Save it anywhere you can find it
   - **Mac users:** Make sure to choose "Plain Text" format

### Step 13: Create a Test Job Description

1. **Open another text editor window**
2. **Copy this text:**
   ```
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
   ```

3. **Save it** as `sample_job.txt`

### Step 14: Test the Analysis

1. **In your browser** (where the app is running):

2. **Upload the resume:**
   - Click on the upload area (where it says "Drop your resume here")
   - Select `sample_resume.txt`
   - You should see the filename appear

3. **Add job title (optional):**
   - Type: `Senior Python Developer`

4. **Paste job description:**
   - Copy the job description from `sample_job.txt`
   - Paste it in the "Job Description" text box

5. **Click "Analyze Resume":**
   - Watch the loading spinner
   - Wait 5-10 seconds

6. **See the results!** 🎉

You should see:
- **ATS Compatibility Score** (out of 100)
- **Three score breakdowns:** Keyword Match, Formatting, Content Quality
- **Matched Keywords:** Keywords found in your resume
- **Missing Keywords:** Keywords you should add
- **Recommendations:** Specific improvements

---

## 🎉 YOU'RE DONE! 

The app is fully set up and working!

---

## WHAT TO DO NOW

### Option A: Keep Using the App

1. **Keep the terminal running** (don't close it)
2. **Try more analyses** - upload your real resume and job descriptions
3. **See how to improve** - follow the recommendations

### Option B: Stop the App

1. **Go to the terminal window**
2. **Press `Ctrl + C`** (hold Ctrl and press C)
3. The app will stop
4. Type: `deactivate` to exit the virtual environment

### Option C: Run It Again Later

Next time you want to run the app:

1. **Open terminal in the `ats-analyzer` folder**
2. **Activate environment:**
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
3. **Start app:** `python app.py`
4. **Open browser:** Go to `http://localhost:5000`

---

## TROUBLESHOOTING

### Problem: "ModuleNotFoundError: No module named 'flask'"

**Solution:**
1. Make sure `(venv)` shows at the start of your terminal line
2. Make sure you ran: `pip install -r requirements.txt`
3. Try again:
   ```
   pip install -r requirements.txt
   ```

### Problem: "The server is already running on http://127.0.0.1:5000"

**Solution:**
1. You might have the app already running in another terminal
2. Close the other terminal window
3. Or use a different port: `python app.py --port 5001`

### Problem: "No such file or directory: 'requirements.txt'"

**Solution:**
1. Make sure you're in the `ats-analyzer` folder
2. Verify you can see `requirements.txt` when you type `dir` (Windows) or `ls` (Mac/Linux)
3. If not, navigate to the right folder

### Problem: "Python is not recognized"

**Solution:**
1. You didn't install Python or didn't check "Add Python to PATH"
2. Install Python from https://www.python.org/downloads/
3. **Make sure to check "Add Python to PATH" during installation!**
4. Restart your terminal

### Problem: Port 5000 is already in use

**Solution:**
Either:
- Find what's using port 5000 and close it, OR
- Use a different port:
  ```
  python app.py --port 5001
  ```
- Then open: `http://localhost:5001`

### Problem: File upload doesn't work

**Solution:**
1. Make sure the file is one of: `.pdf`, `.docx`, or `.txt`
2. Make sure the file is smaller than 16MB
3. Try with the sample resume file first

---

## KEY COMMANDS TO REMEMBER

| Task | Command |
|------|---------|
| Activate environment (Windows) | `venv\Scripts\activate` |
| Activate environment (Mac/Linux) | `source venv/bin/activate` |
| Deactivate environment | `deactivate` |
| Install packages | `pip install -r requirements.txt` |
| Download spaCy model | `python -m spacy download en_core_web_sm` |
| Initialize database | `python init_db.py` |
| Start app | `python app.py` |
| Stop app | `Ctrl + C` |
| Run tests | `pytest test_app.py` |

---

## FILES EXPLAINED (Simplified)

| File | What It Does |
|------|--------------|
| `app.py` | Runs the web server |
| `models.py` | Stores data in database |
| `ats_analyzer.py` | Does the analysis and scoring |
| `resume_parser.py` | Reads resume files |
| `templates/index.html` | The web page you see |
| `requirements.txt` | List of packages to install |

---

## HOW IT WORKS (Simple Explanation)

1. **You upload a resume** → Browser sends it to the app
2. **App reads the file** → `resume_parser.py` extracts text
3. **App analyzes it** → `ats_analyzer.py` checks keywords, formatting, etc.
4. **App calculates scores** → Keyword match (50%) + Formatting (30%) + Content (20%)
5. **App saves results** → Stored in the database
6. **Browser shows results** → You see scores and recommendations

---

## NEXT STEPS

After getting comfortable with the basic setup:

1. **Read the documentation:**
   - Open `README.md` for full features
   - Open `ARCHITECTURE.md` to understand how it works

2. **Try different resumes:**
   - Test with your real resume
   - Test with different job descriptions
   - See how the score changes

3. **Customize it (Optional):**
   - Change the colors (edit `templates/index.html`)
   - Add more keywords (edit `init_db.py`)
   - Modify the scoring (edit `ats_analyzer.py`)

4. **Deploy it (Advanced):**
   - Run on Heroku (see `README.md`)
   - Run in Docker (see `README.md`)

---

## FREQUENTLY ASKED QUESTIONS

**Q: Do I need to be a programmer?**
A: No! Just follow these steps exactly.

**Q: Can I close the terminal?**
A: Not while using the app. The app stops when you close the terminal.

**Q: Can I use my own resume?**
A: Yes! Upload a PDF, DOCX, or TXT file.

**Q: Can I save my analyses?**
A: Yes! They're saved in the database automatically.

**Q: How do I use it with multiple people?**
A: If you run it on a server, multiple people can access `http://your-server:5000`

**Q: Can I make it look different?**
A: Yes! Edit `templates/index.html` to change colors, fonts, etc.

**Q: Can I add more keywords?**
A: Yes! Edit `init_db.py` and rerun it.

---

**You're all set! Enjoy using ATS Filter Analyzer! 🚀**

If you get stuck, check the Troubleshooting section above.
