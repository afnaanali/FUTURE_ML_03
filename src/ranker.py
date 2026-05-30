import pandas as pd
from .scorer import score_candidate

def rank_candidates(candidates_data, jd_text):
    """
    Takes a list of candidate data dictionaries and a job description.
    Scores each candidate, ranks them, and returns a sorted DataFrame.
    
    candidates_data format: [{'name': 'John Doe', 'resume_text': '...'}, ...]
    """
    results = []
    
    for candidate in candidates_data:
        name = candidate.get('name', 'Unknown Candidate')
        resume_text = candidate.get('resume_text', '')
        
        # Calculate scores
        scores = score_candidate(resume_text, jd_text)
        
        # Append to results
        results.append({
            'Candidate Name': name,
            'Similarity Score (%)': scores['similarity_score'],
            'Skill Match Score (%)': scores['skill_match_score'],
            'Final Score (%)': scores['final_score'],
            'Matched Skills': ", ".join(scores['skill_gap']['matched_skills']),
            'Missing Skills': ", ".join(scores['skill_gap']['missing_skills']),
            '_skill_gap_raw': scores['skill_gap'] # Hidden column for detailed views
        })
        
    # Convert to DataFrame
    df = pd.DataFrame(results)
    
    if not df.empty:
        # Sort by Final Score in descending order
        df = df.sort_values(by='Final Score (%)', ascending=False).reset_index(drop=True)
        # Add Rank column (1-indexed)
        df.insert(0, 'Rank', df.index + 1)
        
    return df

def generate_recommendation(row):
    """
    Generates a recruiter-friendly explanation based on scores and missing skills.
    """
    final_score = row['Final Score (%)']
    missing_skills = row['Missing Skills']
    
    if final_score >= 80:
        base_rec = "Highly suitable candidate."
    elif final_score >= 60:
        base_rec = "Good potential, but may require some upskilling."
    else:
        base_rec = "Does not strongly match the requirements."
        
    if missing_skills:
        skill_rec = f" Consider assessing them on missing skills: {missing_skills}."
    else:
        skill_rec = " Strong match on required skills."
        
    return f"{base_rec}{skill_rec}"
