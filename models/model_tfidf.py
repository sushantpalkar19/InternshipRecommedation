import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
df = pd.read_csv("data.csv")

# Preprocess skills
df["Skills"] = df["Skills"].fillna("").str.lower()

# TF-IDF vectorization
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(df["Skills"])


def recommend_tfidf(user_skills, top_n=10):
    """
    Recommend internships using TF-IDF + cosine similarity.
    """
    user_skills = user_skills.lower()

    # Transform user input
    user_vec = vectorizer.transform([user_skills])

    # Compute cosine similarity
    similarity = cosine_similarity(user_vec, tfidf_matrix).flatten()

    # Get top matches
    top_indices = similarity.argsort()[::-1][:top_n]

    results = df.iloc[top_indices].copy()
    results["Similarity_Score"] = similarity[top_indices]

    # Columns to return
    return results[["Title", "Skills", "Location", "Duration", "Stipend", "Mode", "Similarity_Score"]]
