import spacy
import re

# Load small English NLP model. We'll download it in app.py or requirements.
# If not available, we can fallback to regex or simple word matching.
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# Predefined Skill Dictionary
SKILLS_DB = {
    "Programming Languages": ["python", "java", "c++", "c#", "javascript", "typescript", "ruby", "php", "go", "swift", "kotlin", "r", "rust", "scala", "dart"],
    "Frameworks & Libraries": ["react", "angular", "vue", "django", "flask", "fastapi", "spring", "express", "node.js", "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy", "matplotlib", "seaborn", "bootstrap", "tailwind"],
    "Databases": ["sql", "mysql", "postgresql", "mongodb", "sqlite", "oracle", "sql server", "redis", "cassandra", "dynamodb", "elasticsearch"],
    "Cloud & DevOps": ["aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "gitlab", "github actions", "terraform", "ansible", "linux", "unix"],
    "Tools & Platforms": ["git", "github", "bitbucket", "jira", "trello", "confluence", "postman", "swagger", "figma", "excel", "tableau", "power bi"],
    "Machine Learning & AI": ["machine learning", "deep learning", "nlp", "computer vision", "data analysis", "data science", "predictive modeling", "llm", "generative ai"],
    "Soft Skills": ["communication", "teamwork", "problem solving", "leadership", "time management", "adaptability", "critical thinking", "agile", "scrum"]
}

# Flatten the dictionary to get a master list of all skills (lowercase)
ALL_SKILLS = [skill for category, skills in SKILLS_DB.items() for skill in skills]

def extract_skills(text):
    """
    Extracts skills from text based on a predefined dictionary and spaCy.
    Returns a dictionary of categorized skills found in the text.
    """
    found_skills = {category: [] for category in SKILLS_DB.keys()}
    
    # Simple regex-based matching for now, as it's often more reliable for specific tech terms
    # than generic NER if the NER model isn't trained on tech resumes.
    text_lower = text.lower()
    
    # Process with spaCy for tokenization and lemmatization, 
    # but we can also just use simple string matching for our exact keywords.
    # To handle multi-word skills like "machine learning" properly, we pad the text
    padded_text = f" {text_lower} "
    
    for category, skills in SKILLS_DB.items():
        for skill in skills:
            # Create a regex boundary for the skill
            # Handle special characters in skills like C++, C#, Node.js
            escaped_skill = re.escape(skill)
            pattern = r'\b' + escaped_skill + r'\b'
            
            if re.search(pattern, text_lower):
                found_skills[category].append(skill)
                
    # Filter out empty categories
    extracted = {k: v for k, v in found_skills.items() if v}
    return extracted

def get_skill_list(text):
    """Returns a flat list of extracted skills from the text."""
    categorized_skills = extract_skills(text)
    return [skill for skills in categorized_skills.values() for skill in skills]

def analyze_skill_gap(candidate_skills, job_skills):
    """
    Compares candidate skills with job description skills to identify gaps.
    """
    candidate_set = set([s.lower() for s in candidate_skills])
    job_set = set([s.lower() for s in job_skills])
    
    matched_skills = job_set.intersection(candidate_set)
    missing_skills = job_set.difference(candidate_set)
    additional_skills = candidate_set.difference(job_set)
    
    match_percentage = len(matched_skills) / len(job_set) * 100 if len(job_set) > 0 else 0
    
    return {
        "match_percentage": round(match_percentage, 2),
        "matched_skills": list(matched_skills),
        "missing_skills": list(missing_skills),
        "additional_skills": list(additional_skills)
    }
