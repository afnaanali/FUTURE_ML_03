# AI Resume Screening & Candidate Ranking System

An intelligent recruitment assistant built with Python and Streamlit that automatically analyzes resumes, compares them with a job description, scores candidates, ranks them, and identifies missing skills.

## Features
- **Resume Processing:** Extracts text from PDF and TXT files.
- **NLP Preprocessing:** Uses NLTK and spaCy for text cleaning, tokenization, stopword removal, and lemmatization.
- **Skill Extraction:** Identifies programming languages, frameworks, tools, and soft skills using a predefined dictionary and text matching.
- **Similarity Scoring:** Uses TF-IDF Vectorization and Cosine Similarity to find semantic matches between the job description and candidate profiles.
- **Candidate Ranking:** Computes a Final Score (70% Similarity + 30% Skill Match) and ranks candidates.
- **Skill Gap Analysis:** Highlights matched skills, missing skills, and provides AI-generated recruiter recommendations.
- **Interactive Dashboard:** Built with Streamlit, featuring dynamic charts (Plotly/Seaborn) and CSV result downloads.

## Folder Structure
```
resume_candidate/
├── data/                    # Placeholder for any datasets
├── notebooks/               # Jupyter notebook for step-by-step tutorial
│   └── ai_resume_screening.ipynb
├── src/                     # Core logic modules
│   ├── preprocessing.py     # NLP cleaning pipeline
│   ├── skill_extractor.py   # Skill matching logic
│   ├── scorer.py            # TF-IDF & Scoring calculations
│   ├── ranker.py            # Ranking & recommendation logic
│   └── visualizer.py        # Chart generation
├── app.py                   # Streamlit web application
├── requirements.txt         # Dependencies
├── README.md                # This file
└── project_report.md        # Recruiter-friendly report
```

## Setup Instructions

1. **Clone or Download the Repository**

2. **Install Dependencies**
   Ensure you have Python 3.8+ installed. Run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download Required NLP Models**
   The application uses NLTK and spaCy models. It will attempt to download them automatically, but you can manually run:
   ```bash
   python -m spacy download en_core_web_sm
   python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"
   ```

4. **Run the Streamlit App**
   ```bash
   streamlit run app.py
   ```

5. **Using the App**
   - Provide a Job Description (paste text or upload a .txt file).
   - Upload Candidate Resumes (.pdf or .txt) OR select the option to load sample data from the database.
   - Click "Analyze Candidates".
   - View the leaderboard, graphical insights, and individual detailed profiles.

## Technologies Used
- **Python**
- **Pandas & NumPy:** Data manipulation
- **Scikit-learn:** TF-IDF & Cosine Similarity
- **NLTK & spaCy:** Natural Language Processing
- **Streamlit:** Web UI
- **Plotly, Matplotlib, Seaborn:** Data Visualization
- **PyPDF2:** PDF text extraction
