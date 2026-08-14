# 🤖 AI Resume Screening Agent

An AI-powered Resume Screening Agent that evaluates multiple candidate resumes against a Job Description, calculates ATS scores using skill matching and NLP semantic similarity, ranks candidates, and generates AI-based hiring analysis.

---

## 🚀 Features

- 📄 Job Description analysis
- 📁 Upload multiple PDF resumes
- 🔍 Extract skills, experience, and education
- 🎯 Required, preferred, and critical skill matching
- 🧠 NLP semantic similarity
- 📊 Weighted ATS scoring
- 🏆 Candidate ranking
- 🤖 AI-generated hiring analysis
- ✅ Strengths and skill gaps
- 💡 Hiring recommendation
- 📈 Interactive Streamlit dashboard
- 📥 CSV and JSON results
- ⚡ Supports 10+ resumes in a single screening session

---

## 🔄 How It Works

```text
Job Description + Multiple Resumes
                ↓
        PDF Text Extraction
                ↓
      JD Requirement Extraction
                ↓
          Skill Matching
                ↓
      Critical Skill Analysis
                ↓
       Semantic Similarity
                ↓
   Experience + Education Analysis
                ↓
          ATS Score
                ↓
       Candidate Ranking
                ↓
        LLM Hiring Analysis
                ↓
 Summary + Strengths + Gaps + Recommendation
```

---

## 🏗️ System Architecture

```text 
                    ┌──────────────────────┐
                    │    User / Recruiter  │
                    └──────────┬───────────┘
                               │
                               ▼
                  ┌────────────────────────┐
                  │   Streamlit Interface  │
                  │  JD + Resume Uploads   │
                  └───────────┬────────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
              ▼                               ▼
    ┌──────────────────┐             ┌──────────────────┐
    │ Job Description  │             │ Resume PDFs      │
    │ Requirement      │             │ Text Extraction  │
    │ Extraction       │             │                  │
    └────────┬─────────┘             └────────┬─────────┘
             │                                │
             ▼                                ▼
    ┌──────────────────┐             ┌──────────────────┐
    │ Required /       │             │ Skills /         │
    │ Preferred Skills │             │ Experience /     │
    │ Critical Skills  │             │ Education        │
    └────────┬─────────┘             └────────┬─────────┘
             │                                │
             └───────────────┬────────────────┘
                             ▼
                  ┌────────────────────────┐
                  │     Matching Engine    │
                  │                        │
                  │ • Critical Skills      │
                  │ • Supporting Skills    │
                  │ • Semantic Similarity  │
                  │ • Experience           │
                  │ • Education            │
                  └───────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │    ATS Score Engine    │
                  │     Weighted Score     │
                  └───────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │ Candidate Ranking      │
                  │ Strong / Good /        │
                  │ Moderate / Weak       │
                  └───────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │    LLM Analysis        │
                  │                        │
                  │ • Summary              │
                  │ • Strengths            │
                  │ • Gaps                 │
                  │ • Recommendation       │
                  └───────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │ Final Streamlit Output │
                  │                        │
                  │ • Ranking              │
                  │ • Score Breakdown      │
                  │ • Candidate Analysis   │
                  │ • AI Recommendation    │
                  └────────────────────────┘


## 🧠 AI & NLP

The system uses:

- Sentence Transformers
- `all-MiniLM-L6-v2`
- Cosine Similarity
- Rule-based skill matching
- LLM-based candidate analysis

The numerical ATS score is calculated by the scoring engine. The LLM is used to explain the candidate's strengths, gaps, and recommendation.

---

## 📊 ATS Scoring

| Component | Weight |
|---|---:|
| Critical Skills | 45% |
| Supporting Skills | 15% |
| Semantic Similarity | 15% |
| Experience | 15% |
| Education | 10% |
| **Total** | **100%** |

### Formula

```text
Final ATS Score =
    Critical Skills × 0.45
  + Supporting Skills × 0.15
  + Semantic Similarity × 0.15
  + Experience × 0.15
  + Education × 0.10
```

### Candidate Classification

```text
80–100  → Strong Match
65–79   → Good Match
50–64   → Moderate Match
0–49    → Weak Match
```

---

## 🖥️ Streamlit Dashboard

The project includes an interactive Streamlit interface.

The dashboard provides:

- Candidate count
- Strong / Good / Moderate / Weak statistics
- Candidate ranking
- ATS score comparison
- Individual candidate analysis
- Score breakdown
- Critical skills
- Supporting skills
- Required skills
- Preferred skills
- Experience analysis
- Education analysis
- AI hiring summary
- Strengths
- Gaps
- Recommendation

Candidates are ranked first. Selecting a candidate shows that candidate's complete performance separately.

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Sentence Transformers
- Scikit-learn
- Pandas
- Plotly
- PDF text extraction
- LLM API

---

## 📁 Project Structure

```text
AI-Resume-Screening-Agent/
│
├── app.py                 # Streamlit application
├── main.py                # CLI screening pipeline
├── config.py              # Configuration and scoring settings
│
├── extractor.py           # Resume and JD extraction
├── matcher.py             # Skill matching and NLP similarity
├── scorer.py              # ATS scoring and decisions
├── explainer.py           # Rule-based explanations
├── llm_explainer.py       # LLM hiring analysis
├── reporter.py            # CSV / JSON reporting
│
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── resumes/
│   ├── candidate_01.pdf
│   ├── candidate_02.pdf
│   └── ...
│
└── outputs/
    ├── ranked_candidates.csv
    └── ranked_candidates.json
```

---

## ⚙️ Installation

### 1. Clone the Repository

```powershell
git clone YOUR_GITHUB_REPOSITORY_URL
cd AI-Resume-Screening-Agent
```

### 2. Create Virtual Environment

```powershell
python -m venv venv
```

### 3. Activate Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## 🔑 API Configuration

If the LLM module requires an API key, create a `.env` file in the project root.

Example:

```env
GROQ_API_KEY=your_api_key_here
```

Do not upload your `.env` file to GitHub.

Use `.env.example` to show the required environment variables without exposing your API key.

---

## ▶️ Run the Application

### Streamlit

Run:

```powershell
streamlit run app.py
```

Then open the URL shown in the terminal:

```text
http://localhost:8501
```

### CLI Version

The project also includes a command-line screening pipeline.

Run:

```powershell
python main.py
```

---

## 🧪 How to Use

### Step 1

Start the Streamlit application:

```powershell
streamlit run app.py
```

### Step 2

Paste the Job Description.

### Step 3

Upload multiple candidate PDF resumes.

### Step 4

Click:

```text
🚀 Screen Resumes
```

### Step 5

View the ranked candidates.

### Step 6

Select a candidate to view:

- Final ATS Score
- Decision
- Score Breakdown
- Critical Skills
- Supporting Skills
- Required Skills
- Preferred Skills
- Experience
- Education
- AI Hiring Analysis

---

## 📌 Example Output

```text
Rank 3: Data Engineer resume New.pdf

Score: 62.03%

Decision: Moderate Match
```

### AI Hiring Analysis

**Summary:**

The candidate has a moderate match with the job description.

**Strengths:**

- ✓ Strong Python and SQL skills
- ✓ Relevant internship experience
- ✓ Data analytics experience

**Gaps:**

- Missing critical role-specific technologies
- Limited experience with required technologies

**Recommendation:**

The candidate may be considered for a related role with additional training.

---

## 📦 Challenge Deliverables

This project provides:

- ✅ Job Description
- ✅ Multiple sample resumes
- ✅ Ranked candidate output
- ✅ CSV / JSON results
- ✅ NLP similarity scoring
- ✅ ATS scoring methodology
- ✅ Candidate reasoning
- ✅ Streamlit interface
- ✅ Batch processing of 10+ resumes

---

## ⚠️ Limitations

- Currently optimized for PDF resumes.
- Skill detection depends on the configured skill database.
- Scanned/image-only PDFs may require OCR.
- Experience extraction may not work perfectly with unusual resume formats.
- AI recommendations should support human hiring decisions rather than replace them.

---

## 🔮 Future Improvements

- DOCX resume support
- OCR for scanned resumes
- Improved skill synonyms
- Better experience extraction
- RAG-based resume analysis
- Resume database
- Cloud deployment
- Recruiter feedback system

---

## 👨‍💻 Author

### Prem Kumar Shaw

B.Tech Computer Science / Data Science

**Contact:** premshaw117@gmail.com

### Skills Demonstrated

`Python` `NLP` `Machine Learning` `LLM` `Streamlit` `Sentence Transformers` `Scikit-learn` `Pandas`