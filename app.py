# =====================================================
# 🎯 Internship Recommendation System – PS25034
# Developed by: Sushant & Nirbhay
# Description: Streamlit-based system recommending internships
#              using TF-IDF, CountVectorizer, and Word2Vec models.
# =====================================================

import streamlit as st
import pandas as pd
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from models.model_tfidf import recommend_tfidf
from models.model_countvec import recommend_countvec
from models.model_word2vec import recommend_word2vec
from src.data_loader import get_data_loader
from src.preprocessing import normalize_skills
from src.ranking import RankingSystem
from src.explanations import ExplanationGenerator
from src.config import Config
from src.recommender import get_hybrid_recommender
from src.personalization import get_personalization_engine

# -------------------- Page Configuration --------------------
st.set_page_config(
    page_title="Internship Recommendation System",
    page_icon="🎓",
    layout="wide"
)

# -------------------- App Header --------------------
st.title("🎓 Internship Recommendation System")
st.markdown("""
Welcome to **Internship Recommender (PS25034)**  
💡 Discover the best internship opportunities tailored to your **skills and preferences**.
""")

st.markdown("---")

# -------------------- Load Data --------------------
@st.cache_resource
def load_data():
    """Load and cache the data."""
    data_loader = get_data_loader()
    return data_loader

data_loader = load_data()
df = data_loader.get_data()

# -------------------- Sidebar Section --------------------
st.sidebar.header("⚙️ Preferences")

# User Profile Section
st.sidebar.subheader("👤 User Profile")
with st.sidebar.expander("Profile Settings"):
    profile_name = st.text_input("Name", key="profile_name")
    profile_education = st.selectbox(
        "Education",
        ["", "B.Tech/B.E", "M.Tech/M.E", "BCA/MCA", "BSc/MSc", "Any Graduate"],
        key="profile_education"
    )
    profile_domain = st.selectbox(
        "Preferred Domain",
        [""] + data_loader.get_unique_domains(),
        key="profile_domain"
    )

# Skills input
st.sidebar.subheader("🧠 Your Skills")
user_skills = st.sidebar.text_area(
    "Enter your skills (comma-separated):",
    placeholder="e.g. Python, Machine Learning, Data Analysis",
    height=100
)

# Filters
st.sidebar.subheader("🎛️ Filters")

# Location filter
all_locations = data_loader.get_unique_locations()
selected_locations = st.sidebar.multiselect(
    "Location",
    options=all_locations,
    default=[]
)

# Work mode filter
all_modes = data_loader.get_unique_modes()
selected_modes = st.sidebar.multiselect(
    "Work Mode",
    options=all_modes,
    default=[]
)

# Domain filter
all_domains = data_loader.get_unique_domains()
selected_domains = st.sidebar.multiselect(
    "Domain",
    options=all_domains,
    default=[]
)

# Duration filter
all_durations = data_loader.get_unique_durations()
selected_durations = st.sidebar.multiselect(
    "Duration",
    options=all_durations,
    default=[]
)

# Stipend filter
col1, col2 = st.sidebar.columns(2)
min_stipend = col1.number_input("Min Stipend (₹)", min_value=0, value=0, step=1000)
max_stipend = col2.number_input("Max Stipend (₹)", min_value=0, value=100000, step=1000)

# Model selection (in Advanced section)
st.sidebar.markdown("---")
st.sidebar.header("🔧 Advanced")
model_choice = st.sidebar.radio(
    "Recommendation Model:",
    ("TF-IDF (Recommended)", "CountVectorizer (Baseline)", "Word2Vec (Experimental)")
)

# Weight configuration
st.sidebar.markdown("**Ranking Weights:**")
skill_weight = st.sidebar.slider("Skill Weight", 0.0, 1.0, 0.70, 0.05)
pref_weight = st.sidebar.slider("Preference Weight", 0.0, 1.0, 0.20, 0.05)
quality_weight = st.sidebar.slider("Quality Weight", 0.0, 1.0, 0.10, 0.05)

# Validate weights
if abs(skill_weight + pref_weight + quality_weight - 1.0) > 0.01:
    st.sidebar.warning("⚠️ Weights should sum to 1.0")

st.sidebar.markdown("---")
st.sidebar.info("""
👨‍💻 **How to use:**
1. Enter your skills
2. Set your preferences
3. Click **Get Recommendations**
""")

# -------------------- Model Performance Dashboard --------------------
st.sidebar.markdown("---")
with st.sidebar.expander("📊 Model Performance"):
    try:
        comparison_df = pd.read_csv("data/evaluation/model_comparison.csv")
        st.dataframe(comparison_df, use_container_width=True)
    except:
        st.info("Run evaluation to see model performance")

# -------------------- Session State for Feedback --------------------
if "saved_internships" not in st.session_state:
    st.session_state.saved_internships = []
if "liked_internships" not in st.session_state:
    st.session_state.liked_internships = []
if "disliked_internships" not in st.session_state:
    st.session_state.disliked_internships = []

# -------------------- Main Logic --------------------
if st.button("🔍 Get Recommendations"):
    if not user_skills.strip():
        st.warning("⚠️ Please enter at least one skill to get recommendations.")
    else:
        # Normalize user skills
        normalized_skills = normalize_skills(user_skills)
        user_skills_list = [s.strip() for s in normalized_skills.split(",")]
        
        with st.spinner("🔎 Finding the best internships for you..."):
            # Use hybrid recommender
            try:
                recommender = get_hybrid_recommender()
                
                # Map UI choice to model name
                model_mapping = {
                    "TF-IDF (Recommended)": "tfidf",
                    "CountVectorizer (Baseline)": "countvectorizer", 
                    "Word2Vec (Experimental)": "word2vec"
                }
                model_name = model_mapping.get(model_choice, "tfidf")
                
                results = recommender.recommend(
                    user_skills,
                    model_name=model_name,
                    top_n=10,
                    apply_ranking=True,
                    preferred_location=selected_locations[0] if selected_locations else None,
                    preferred_mode=selected_modes[0] if selected_modes else None,
                    min_stipend=min_stipend if min_stipend > 0 else None,
                    max_stipend=max_stipend if max_stipend < 100000 else None,
                    preferred_duration=selected_durations[0] if selected_durations else None
                )
                model_used = model_choice
            except Exception as e:
                st.error(f"Error using hybrid recommender: {e}. Falling back to direct model calls.")
                # Fallback to direct model calls
                if model_choice.startswith("TF-IDF"):
                    results = recommend_tfidf(user_skills)
                    model_used = "TF-IDF"
                elif model_choice.startswith("CountVectorizer"):
                    results = recommend_countvec(user_skills)
                    model_used = "CountVectorizer"
                else:
                    results = recommend_word2vec(user_skills)
                    model_used = "Word2Vec"
        
        # Apply filters
        if not results.empty:
            filtered_df = df.copy()
            
            if selected_locations:
                filtered_df = filtered_df[filtered_df["Location"].isin(selected_locations)]
            if selected_modes:
                filtered_df = filtered_df[filtered_df["Mode"].isin(selected_modes)]
            if selected_domains:
                filtered_df = filtered_df[filtered_df["Domain"].isin(selected_domains)]
            if selected_durations:
                filtered_df = filtered_df[filtered_df["Duration"].isin(selected_durations)]
            if min_stipend > 0 or max_stipend < 100000:
                filtered_df = data_loader.filter_by_stipend(min_stipend, max_stipend)
            
            # Filter results to only include internships that match filters
            if "Internship_ID" in results.columns:
                valid_ids = filtered_df["Internship_ID"].tolist()
                results = results[results["Internship_ID"].isin(valid_ids)]
        
        # Apply weighted ranking
        if not results.empty:
            try:
                ranking_system = RankingSystem(
                    skill_weight=skill_weight,
                    preference_weight=pref_weight,
                    quality_weight=quality_weight
                )
                
                results = ranking_system.rank_recommendations(
                    results,
                    user_skills_list,
                    preferred_location=selected_locations[0] if selected_locations else None,
                    preferred_mode=selected_modes[0] if selected_modes else None,
                    min_stipend=min_stipend if min_stipend > 0 else None,
                    max_stipend=max_stipend if max_stipend < 100000 else None,
                    preferred_duration=selected_durations[0] if selected_durations else None
                )
            except Exception as e:
                st.warning(f"Ranking error: {e}. Using similarity scores only.")
        
        # Apply personalization based on feedback
        if not results.empty and (st.session_state.liked_internships or st.session_state.disliked_internships):
            try:
                personalization_engine = get_personalization_engine()
                personalization_engine.update_from_feedback(
                    st.session_state.liked_internships,
                    st.session_state.disliked_internships
                )
                results = personalization_engine.apply_personalization(results)
                st.info("🎯 Personalization applied based on your feedback")
            except Exception as e:
                st.warning(f"Personalization error: {e}")
        
        # -------------------- Display Results --------------------
        if not results.empty:
            st.success(f"✅ Found {len(results)} recommendations using **{model_used} Model**")
            
            # Generate explanations
            explanation_gen = ExplanationGenerator()
            explanations = explanation_gen.generate_batch_explanations(
                results.head(10),
                user_skills_list,
                results if "Final_Score" in results.columns else None
            )
            
            # Display as cards
            st.markdown("### 🏆 Top Internship Recommendations")
            
            for i, (idx, row) in enumerate(results.head(10).iterrows()):
                explanation = explanations[i] if i < len(explanations) else None
                
                with st.container():
                    # Card header
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.markdown(f"### {row['Title']}")
                        st.markdown(f"**{row.get('Company', 'N/A')}**")
                    
                    with col2:
                        match_pct = int(row.get('Final_Score', row.get('Similarity_Score', 0.5)) * 100)
                        st.metric("Match", f"{match_pct}%")
                    
                    with col3:
                        col3a, col3b = st.columns(2)
                        with col3a:
                            if st.button(f"Apply 📎", key=f"apply_{idx}"):
                                st.info(f"Application opened for {row['Title']}")
                        with col3b:
                            internship_id = row.get('Internship_ID', idx)
                            if st.button(f"Save 🔖", key=f"save_{idx}"):
                                if internship_id not in st.session_state.saved_internships:
                                    st.session_state.saved_internships.append(internship_id)
                                    st.success(f"Saved {row['Title']}")
                                else:
                                    st.info("Already saved")
                    
                    # Card details
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.markdown(f"📍 {row['Location']}")
                    with col2:
                        st.markdown(f"💼 {row['Mode']}")
                    with col3:
                        st.markdown(f"💰 {row['Stipend']}")
                    with col4:
                        st.markdown(f"⏱ {row['Duration']}")
                    
                    # Skills
                    st.markdown("**Required Skills:**")
                    st.markdown(f"{row['Skills']}")
                    
                    # Explanation
                    if explanation:
                        with st.expander("Why recommended?"):
                            if explanation['matched_skills']:
                                st.markdown(f"**✓ Matched Skills:** {', '.join(explanation['matched_skills'])}")
                            if explanation['missing_skills']:
                                st.markdown(f"**Missing Skills:** {', '.join(explanation['missing_skills'])}")
                            st.markdown(f"**Reasoning:** {explanation['reasoning']}")
                    
                    # Feedback buttons
                    col_feedback1, col_feedback2, col_feedback3 = st.columns(3)
                    internship_id = row.get('Internship_ID', idx)
                    
                    with col_feedback1:
                        if st.button(f"👍 Relevant", key=f"like_{idx}"):
                            if internship_id not in st.session_state.liked_internships:
                                st.session_state.liked_internships.append(internship_id)
                                st.success("Thanks for feedback!")
                    
                    with col_feedback2:
                        if st.button(f"👎 Not Relevant", key=f"dislike_{idx}"):
                            if internship_id not in st.session_state.disliked_internships:
                                st.session_state.disliked_internships.append(internship_id)
                                st.success("Thanks for feedback!")
                    
                    with col_feedback3:
                        if st.button(f"🔖 Save", key=f"save2_{idx}"):
                            if internship_id not in st.session_state.saved_internships:
                                st.session_state.saved_internships.append(internship_id)
                                st.success("Saved!")
                    
                    st.markdown("---")
        
        else:
            st.error("😕 No matching internships found with your criteria. Try:")
            st.markdown("- Adjusting your skill keywords")
            st.markdown("- Removing some filters")
            st.markdown("- Expanding your location or domain preferences")

# -------------------- Saved Internships Section --------------------
st.markdown("---")
st.subheader("🔖 Saved Internships")
if st.session_state.saved_internships:
    saved_df = df[df["Internship_ID"].isin(st.session_state.saved_internships)]
    st.dataframe(saved_df[["Title", "Company", "Location", "Stipend", "Mode"]], use_container_width=True)
else:
    st.info("No saved internships yet.")

# -------------------- Footer --------------------
st.markdown("---")
st.caption("""
Developed by **Sushant & Nirbhay.**
""")
