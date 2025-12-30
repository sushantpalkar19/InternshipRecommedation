import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
df = pd.read_csv("data.csv")
df["Skills"] = df["Skills"].fillna("").str.lower()

# CountVectorizer
vectorizer = CountVectorizer(stop_words="english")
count_matrix = vectorizer.fit_transform(df["Skills"])


def recommend_countvec(user_skills, top_n=10):
    """
    Recommend internships using CountVectorizer + cosine similarity.
    """
    user_skills = user_skills.lower()

    # Transform user input
    user_vec = vectorizer.transform([user_skills])

    # Compute similarity
    similarity = cosine_similarity(user_vec, count_matrix).flatten()

    # Top matches
    top_indices = similarity.argsort()[::-1][:top_n]

    results = df.iloc[top_indices].copy()
    results["Similarity_Score"] = similarity[top_indices]

    return results[["Title", "Skills", "Location", "Duration", "Stipend", "Mode", "Similarity_Score"]]
