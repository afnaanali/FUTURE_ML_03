import streamlit as st
import pandas as pd
import time
import os
from src.preprocessing import extract_text_from_pdf, extract_text_from_txt
from src.ranker import rank_candidates, generate_recommendation
from src.visualizer import plot_top_candidates, plot_score_comparison, plot_skill_distribution, plot_candidate_radar

# Page Config
st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for UI Enhancement
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 20px;
        font-weight: 700;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #3B82F6;
        margin-top: 20px;
        margin-bottom: 10px;
        font-weight: 600;
    }
    .metric-card {
        background-color: #F3F4F6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    .stButton>button {
        background-color: #2563EB;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #1D4ED8;
    }
</style>
""", unsafe_allow_html=True)

# Application Header
st.markdown("<div class='main-header'>🤖 AI Resume Screening & Candidate Ranking System</div>", unsafe_allow_html=True)
st.markdown("Automate your hiring process with AI. Upload a Job Description and Resumes to find the best match.")

# Sidebar for Inputs
with st.sidebar:
    st.header("📋 Input Configuration")
    
    # 1. Job Description Input
    st.subheader("1. Job Description")
    jd_input_method = st.radio("Provide Job Description via:", ("Text Input", "File Upload"))
    
    jd_text = ""
    if jd_input_method == "Text Input":
        jd_text = st.text_area("Paste Job Description Here:", height=200, 
                              placeholder="e.g. We are looking for a Software Engineer with Python, SQL, and Machine Learning experience...")
    else:
        jd_file = st.file_uploader("Upload JD (TXT)", type=['txt'])
        if jd_file is not None:
            jd_text = extract_text_from_txt(jd_file)
            st.success("JD Uploaded Successfully!")

    # 2. Resume Input
    st.subheader("2. Candidate Resumes")
    resume_input_method = st.radio("Source of Resumes:", ("Upload Files (PDF/TXT)", "Use Sample Database (CSV)"))
    
    candidates_data = []
    
    if resume_input_method == "Upload Files (PDF/TXT)":
        uploaded_resumes = st.file_uploader("Upload Resumes", type=['pdf', 'txt'], accept_multiple_files=True)
        if uploaded_resumes:
            for file in uploaded_resumes:
                if file.name.endswith('.pdf'):
                    text = extract_text_from_pdf(file)
                else:
                    text = extract_text_from_txt(file)
                
                # Use filename without extension as candidate name
                name = os.path.splitext(file.name)[0].replace('_', ' ').title()
                candidates_data.append({'name': name, 'resume_text': text})
            st.success(f"{len(uploaded_resumes)} Resumes Uploaded!")
            
    else:
        st.info("Using Resume.csv from database.")
        csv_path = "Resume/Resume.csv"
        # We will load a subset to avoid slow processing during demo
        num_resumes = st.slider("Number of Sample Resumes to Evaluate:", min_value=5, max_value=50, value=10)
        try:
            # Look in multiple possible locations
            paths = [csv_path, "../Resume/Resume.csv", "c:/Users/MUHAMMED AFNAN/OneDrive/Dokumen/future intern/resume_candidate/Resume/Resume.csv"]
            df_resumes = None
            for p in paths:
                if os.path.exists(p):
                    df_resumes = pd.read_csv(p).head(num_resumes)
                    break
            
            if df_resumes is not None:
                # The Kaggle dataset usually has 'Resume_str' or 'Resume' columns
                text_col = 'Resume_str' if 'Resume_str' in df_resumes.columns else df_resumes.columns[0]
                
                for idx, row in df_resumes.iterrows():
                    name = f"Candidate {idx+1}"
                    # If dataset has a 'Category' column, append it to name
                    if 'Category' in df_resumes.columns:
                        name += f" ({row['Category']})"
                    
                    candidates_data.append({
                        'name': name,
                        'resume_text': str(row[text_col])
                    })
                st.success(f"Loaded {num_resumes} resumes from database.")
            else:
                st.error("Could not find Resume.csv. Please use File Upload instead.")
        except Exception as e:
            st.error(f"Error loading CSV: {e}")

    # Process Button
    process_btn = st.button("🚀 Analyze Candidates", use_container_width=True)

# Main Content Area
if process_btn:
    if not jd_text.strip():
        st.warning("⚠️ Please provide a Job Description.")
    elif not candidates_data:
        st.warning("⚠️ Please upload at least one Resume or select sample database.")
    else:
        with st.spinner("Analyzing resumes using NLP..."):
            # Simulate processing time for UX
            time.sleep(1) 
            
            # 1. Rank Candidates
            results_df = rank_candidates(candidates_data, jd_text)
            
            # Add Recommendation column
            results_df['Recommendation'] = results_df.apply(generate_recommendation, axis=1)
            
            # Hide the raw data column for display
            display_df = results_df.drop(columns=['_skill_gap_raw'])
            
            st.success("✅ Analysis Complete!")
            
            # Top Level Metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"<div class='metric-card'><h3>Total Candidates</h3><h1>{len(candidates_data)}</h1></div>", unsafe_allow_html=True)
            with col2:
                top_score = results_df.iloc[0]['Final Score (%)'] if not results_df.empty else 0
                st.markdown(f"<div class='metric-card'><h3>Highest Score</h3><h1>{top_score}%</h1></div>", unsafe_allow_html=True)
            with col3:
                avg_score = results_df['Final Score (%)'].mean() if not results_df.empty else 0
                st.markdown(f"<div class='metric-card'><h3>Average Score</h3><h1>{avg_score:.1f}%</h1></div>", unsafe_allow_html=True)
            
            # --- TABBED VIEW ---
            tab1, tab2, tab3 = st.tabs(["🏆 Leaderboard", "📊 Visualizations", "🔍 Detailed Analysis"])
            
            with tab1:
                st.markdown("<div class='sub-header'>Candidate Rankings</div>", unsafe_allow_html=True)
                st.dataframe(
                    display_df.style.background_gradient(subset=['Final Score (%)'], cmap='Greens'),
                    use_container_width=True,
                    height=400
                )
                
                # Download button for CSV
                csv = display_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Results as CSV",
                    data=csv,
                    file_name="candidate_rankings.csv",
                    mime="text/csv",
                )
                
            with tab2:
                st.markdown("<div class='sub-header'>Dashboard Insights</div>", unsafe_allow_html=True)
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.pyplot(plot_top_candidates(results_df))
                with col_b:
                    st.plotly_chart(plot_score_comparison(results_df), use_container_width=True)
                    
                st.markdown("---")
                st.pyplot(plot_skill_distribution(results_df))
                
            with tab3:
                st.markdown("<div class='sub-header'>Individual Candidate Profile</div>", unsafe_allow_html=True)
                
                selected_candidate = st.selectbox("Select Candidate to view details:", results_df['Candidate Name'].tolist())
                
                if selected_candidate:
                    candidate_row = results_df[results_df['Candidate Name'] == selected_candidate].iloc[0]
                    
                    st.markdown(f"### Profile: **{selected_candidate}**")
                    st.info(f"**Recommendation:** {candidate_row['Recommendation']}")
                    
                    c1, c2 = st.columns([1, 1])
                    with c1:
                        st.markdown("#### Score Breakdown")
                        st.markdown(f"- **Final Score:** `{candidate_row['Final Score (%)']}%`")
                        st.markdown(f"- **Similarity Score (TF-IDF):** `{candidate_row['Similarity Score (%)']}%`")
                        st.markdown(f"- **Skill Match Score:** `{candidate_row['Skill Match Score (%)']}%`")
                        
                        st.markdown("#### Skill Gap Analysis")
                        st.success(f"**Matched Skills:**\n{candidate_row['Matched Skills'] if candidate_row['Matched Skills'] else 'None'}")
                        st.error(f"**Missing Skills:**\n{candidate_row['Missing Skills'] if candidate_row['Missing Skills'] else 'None'}")
                        
                        # Show additional skills if any
                        raw_data = candidate_row['_skill_gap_raw']
                        if raw_data['additional_skills']:
                            st.warning(f"**Candidate has additional skills not in JD:**\n{', '.join(raw_data['additional_skills'][:10])}{'...' if len(raw_data['additional_skills'])>10 else ''}")
                            
                    with c2:
                        st.plotly_chart(plot_candidate_radar(candidate_row), use_container_width=True)
else:
    # Display welcome message when app first loads
    st.info("👈 Please input the Job Description and upload Candidates Resumes in the sidebar, then click 'Analyze Candidates'.")
    st.markdown("""
    ### How it works:
    1. **NLP Preprocessing:** Cleans and tokenizes text.
    2. **Skill Extraction:** Uses specialized dictionaries to extract tech stacks and soft skills.
    3. **Similarity Scoring:** Uses TF-IDF and Cosine Similarity to compare semantic meaning.
    4. **Ranking:** Calculates a weighted Final Score to rank the best fits.
    """)
