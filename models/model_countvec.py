import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data_loader import get_data_loader
from src.preprocessing import normalize_skills

# Load dataset using centralized loader
data_loader = get_data_loader()
df = data_loader.get_data()

# Use normalized skills
df["Skills"] = df["Skills_Normalized"].fillna("").str.lower()

# CountVectorizer
vectorizer = CountVectorizer(stop_words="english")
count_matrix = vectorizer.fit_transform(df["Skills"])


def recommend_countvec(user_skills, top_n=10):
    """
    Recommend internships using CountVectorizer + cosine similarity.
    
    Args:
        user_skills: Comma-separated user skills string
        top_n: Number of recommendations to return
        
    Returns:
        DataFrame with recommended internships
    """
    # Normalize user skills
    user_skills_normalized = normalize_skills(user_skills).lower()
    
    if not user_skills_normalized.strip():
        return pd.DataFrame()

    # Transform user input
    user_vec = vectorizer.transform([user_skills_normalized])

    # Compute similarity
    similarity = cosine_similarity(user_vec, count_matrix).flatten()

    # Top matches
    top_indices = similarity.argsort()[::-1][:top_n]

    results = df.iloc[top_indices].copy()
    results["Similarity_Score"] = similarity[top_indices]

    # Columns to return
    return_cols = ["Internship_ID", "Title", "Company", "Skills", "Location", "Duration", "Stipend", "Mode", "Similarity_Score"]
    available_cols = [col for col in return_cols if col in results.columns]
    
    return results[available_cols]
