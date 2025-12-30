# =====================================================
# 🎯 Internship Recommendation System – PS25034
# Developed by: Sushant & Nirbhay
# Description: Streamlit-based system recommending internships
#              using TF-IDF, CountVectorizer, and Word2Vec models.
# =====================================================

import streamlit as st
import pandas as pd
from models.model_tfidf import recommend_tfidf
from models.model_countvec import recommend_countvec
from models.model_word2vec import recommend_word2vec

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
💡 Discover the best internship opportunities tailored to your **skills and interests**.
""")

st.markdown("---")

# -------------------- Sidebar Section --------------------
st.sidebar.header("⚙️ Model Selection")
model_choice = st.sidebar.radio(
    "Select a Recommendation Model:",
    ("TF-IDF (Recommended)", "CountVectorizer (Baseline)", "Word2Vec (Semantic Model)")
)

st.sidebar.markdown("---")
st.sidebar.info("""
👨‍💻 **How to use:**
1. Enter your key skills (comma-separated)
2. Choose a model
3. Click **Get Recommendations** to view top internships
""")

# -------------------- Load Dataset --------------------
try:
    df = pd.read_csv("data.csv")
except FileNotFoundError:
    st.error("❌ Dataset `data.csv` not found! Please make sure it exists in your project directory.")
    st.stop()

# -------------------- Input Section --------------------
st.subheader("🧠 Enter Your Skills")
user_skills = st.text_input(
    "Enter skills (comma-separated):",
    placeholder="e.g. Python, Machine Learning, Data Analysis"
)

# -------------------- Main Logic --------------------
if st.button("🔍 Get Recommendations"):
    if not user_skills.strip():
        st.warning("⚠️ Please enter at least one skill to get recommendations.")
    else:
        with st.spinner("🔎 Matching internships to your skills... Please wait..."):
            if model_choice.startswith("TF-IDF"):
                results = recommend_tfidf(user_skills)
                model_used = "TF-IDF"
            elif model_choice.startswith("CountVectorizer"):
                results = recommend_countvec(user_skills)
                model_used = "CountVectorizer"
            else:
                results = recommend_word2vec(user_skills)
                model_used = "Word2Vec"

        # -------------------- Display Results --------------------
        if not results.empty:
            st.success(f"✅ Recommendations generated using **{model_used} Model**")

            # Clean and format results
            results.columns = results.columns.str.strip()

            # Format stipend for consistency
            if "Stipend" in results.columns:
                results["Stipend"] = results["Stipend"].astype(str).apply(
                    lambda x: f"₹{x}/month"
                    if x.replace("₹", "").replace(",", "").replace("/month", "").isdigit() else x
                )

            # Reorder columns for better display
            display_cols = ["Title", "Skills", "Location", "Duration", "Stipend", "Mode"]
            available_cols = [col for col in display_cols if col in results.columns]

            # ✅ Display clean DataFrame without any highlight or extra columns
            st.markdown("### 🏆 Top Internship Matches")
            st.dataframe(results[available_cols].head(10), use_container_width=True)

        else:
            st.error("😕 No matching internships found. Try adjusting your skill keywords.")

# -------------------- Footer --------------------
st.markdown("---")
st.caption("""
Developed by **Sushant & Nirbhay.**
""")
