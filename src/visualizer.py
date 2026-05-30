import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Set default styling for seaborn
sns.set_theme(style="whitegrid")

def plot_top_candidates(df, top_n=5):
    """
    Creates a bar chart of the top N candidates based on Final Score.
    """
    top_df = df.head(top_n).sort_values(by='Final Score (%)', ascending=True)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create horizontal bar chart
    bars = ax.barh(top_df['Candidate Name'], top_df['Final Score (%)'], color='skyblue')
    
    # Add values on bars
    for bar in bars:
        ax.text(
            bar.get_width() + 1, 
            bar.get_y() + bar.get_height()/2, 
            f'{bar.get_width():.1f}%', 
            va='center', 
            ha='left',
            fontsize=10
        )
        
    ax.set_xlabel('Final Score (%)')
    ax.set_title(f'Top {top_n} Candidates Ranked by Final Score')
    ax.set_xlim(0, 110) # Give some space for labels
    plt.tight_layout()
    
    return fig

def plot_score_comparison(df):
    """
    Creates a scatter plot comparing Similarity Score vs Skill Match Score.
    Uses Plotly for interactivity.
    """
    fig = px.scatter(
        df, 
        x="Similarity Score (%)", 
        y="Skill Match Score (%)", 
        color="Final Score (%)",
        hover_name="Candidate Name",
        hover_data=["Rank"],
        title="Candidate Score Comparison",
        color_continuous_scale="Viridis",
        size="Final Score (%)"
    )
    fig.update_layout(
        xaxis_title="TF-IDF Similarity Score (%)",
        yaxis_title="Skill Match Score (%)"
    )
    return fig

def plot_skill_distribution(df):
    """
    Creates a bar chart showing the frequency of matched skills across all candidates.
    """
    all_matched_skills = []
    for skills_str in df['Matched Skills']:
        if pd.notna(skills_str) and skills_str.strip():
            # split by comma and strip whitespace
            skills = [s.strip() for s in skills_str.split(',')]
            all_matched_skills.extend(skills)
            
    if not all_matched_skills:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, 'No skills matched', ha='center', va='center')
        ax.set_axis_off()
        return fig
        
    skill_counts = pd.Series(all_matched_skills).value_counts().head(10)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=skill_counts.values, y=skill_counts.index, hue=skill_counts.index, palette="viridis", legend=False, ax=ax)
    
    ax.set_xlabel('Number of Candidates')
    ax.set_ylabel('Skill')
    ax.set_title('Top 10 Matched Skills Across Candidates')
    plt.tight_layout()
    
    return fig

def plot_candidate_radar(candidate_row, all_categories=None):
    """
    Creates a radar chart for a specific candidate's skill match profile.
    Since we don't have category-level scoring in the basic implementation,
    we will simulate this by comparing their scores.
    """
    categories = ['Similarity', 'Skill Match', 'Final Score']
    
    # Get values and pad to match categories
    values = [
        candidate_row['Similarity Score (%)'],
        candidate_row['Skill Match Score (%)'],
        candidate_row['Final Score (%)']
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]], # Close the polygon
        theta=categories + [categories[0]],
        fill='toself',
        name=candidate_row['Candidate Name']
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=False,
        title=f"Score Profile: {candidate_row['Candidate Name']}"
    )
    
    return fig
