from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .preprocessing import preprocess_text
from .skill_extractor import get_skill_list, analyze_skill_gap

def calculate_similarity(resume_text, jd_text):
    """
    Calculates TF-IDF Cosine Similarity between a single resume and a job description.
    """
    # Preprocess texts
    processed_resume = preprocess_text(resume_text)
    processed_jd = preprocess_text(jd_text)
    
    if not processed_resume or not processed_jd:
        return 0.0
        
    # Combine texts for vectorization to ensure same vocabulary
    documents = [processed_jd, processed_resume]
    
    # Create TF-IDF vectors
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    # Calculate Cosine Similarity (Index 0 is JD, Index 1 is Resume)
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    
    return float(cosine_sim) * 100 # Return as percentage

def score_candidate(resume_text, jd_text):
    """
    Calculates the final score based on:
    70% Similarity Score + 30% Skill Match Score
    """
    # 1. Similarity Score
    similarity_score = calculate_similarity(resume_text, jd_text)
    
    # 2. Skill Match Score
    resume_skills = get_skill_list(resume_text)
    jd_skills = get_skill_list(jd_text)
    
    skill_gap = analyze_skill_gap(resume_skills, jd_skills)
    skill_match_score = skill_gap['match_percentage']
    
    # Final Score Formula
    # If there are no skills extracted from JD, rely heavily on Similarity
    if len(jd_skills) == 0:
        final_score = similarity_score
    else:
        final_score = (0.7 * similarity_score) + (0.3 * skill_match_score)
        
    return {
        "similarity_score": round(similarity_score, 2),
        "skill_match_score": round(skill_match_score, 2),
        "final_score": round(final_score, 2),
        "skill_gap": skill_gap
    }
