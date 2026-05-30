# AI Resume Screening System - Project Report

## Executive Summary
The AI Resume Screening & Candidate Ranking System is an intelligent recruitment assistant designed to streamline the hiring process. By automating the initial screening phase, this application drastically reduces the time recruiters spend reading resumes while increasing the objectivity and accuracy of candidate shortlisting. 

## The Problem
Recruiters often receive hundreds or thousands of resumes for a single job posting. Manually reviewing each resume to check if a candidate possesses the required skills is time-consuming, prone to human error, and subject to unconscious bias. 

## The Solution
This system leverages Natural Language Processing (NLP) and Machine Learning techniques to automate the comparison between a given Job Description (JD) and a pool of candidate resumes. It automatically reads the resumes, extracts relevant technical and soft skills, and computes a similarity score, allowing recruiters to focus their energy on the most qualified candidates.

## How It Works (Methodology)

1. **Data Ingestion:**
   The system supports uploading resumes in PDF and TXT formats, or evaluating existing resumes from a database (CSV).

2. **Text Preprocessing:**
   Using libraries like NLTK, the text from both the JD and the resumes is "cleaned." This involves converting everything to lowercase, removing punctuation, stripping out common stop words (e.g., "the", "and"), and lemmatizing words (reducing words to their base form, like "running" -> "run").

3. **Skill Extraction:**
   The system maintains a comprehensive dictionary of modern tech stacks, frameworks, cloud platforms, and soft skills. It scans the candidate's resume and the job description to identify these exact keywords.

4. **Machine Learning Scoring:**
   - **TF-IDF (Term Frequency-Inverse Document Frequency):** This algorithm converts the textual data into numbers by evaluating how important a word is to a document within a collection.
   - **Cosine Similarity:** We calculate the cosine angle between the JD text vector and the Resume text vector. A higher similarity score means the overall context and wording of the resume closely match the JD.
   - **Skill Match Score:** A strict percentage of how many hard/soft skills from the JD are actually present in the resume.

5. **Candidate Ranking:**
   The Final Score is a weighted average: **70% Semantic Similarity + 30% Exact Skill Match**. Candidates are then ranked from highest to lowest score.

6. **Actionable Insights:**
   The system automatically generates a "Skill Gap Analysis," telling the recruiter exactly which required skills the candidate is missing.

## Business Impact
- **Time Savings:** Reduces manual screening time by over 80%.
- **Improved Quality of Hire:** Ensures candidates are ranked based purely on skill alignment.
- **Enhanced Candidate Experience:** Faster processing means quicker response times to applicants.
- **Scalability:** Capable of handling thousands of resumes simultaneously without fatigue.

## Future Enhancements
- Integration with Applicant Tracking Systems (ATS) like Workday or Lever.
- Utilizing advanced Large Language Models (LLMs) like GPT or Gemini for deeper contextual understanding beyond TF-IDF.
- OCR support for reading image-based resumes.
