import pandas as pd
from gensim.models import Word2Vec
import numpy as np

# Load data
df = pd.read_csv("data.csv")
df["Skills"] = df["Skills"].fillna("").str.lower()

# Tokenize skills
tokenized_skills = [s.split(",") for s in df["Skills"]]

# Train Word2Vec model
w2v_model = Word2Vec(sentences=tokenized_skills, vector_size=100, window=5, min_count=1, workers=4)


def get_vector(words):
    """
    Average the vectors for all valid words in the list.
    """
    valid_words = [w.strip() for w in words if w.strip() in w2v_model.wv]
    if not valid_words:
        return np.zeros(w2v_model.vector_size)
    return np.mean([w2v_model.wv[w] for w in valid_words], axis=0)


def recommend_word2vec(user_skills, top_n=10):
    """
    Recommend internships using Word2Vec semantic similarity.
    """
    user_tokens = [s.strip().lower() for s in user_skills.split(",")]
    user_vec = get_vector(user_tokens)

    skill_vectors = np.array([get_vector(s.split(",")) for s in df["Skills"]])

    # Compute cosine similarity
    sims = np.dot(skill_vectors, user_vec) / (
        np.linalg.norm(skill_vectors, axis=1) * np.linalg.norm(user_vec) + 1e-10
    )

    top_indices = sims.argsort()[::-1][:top_n]
    results = df.iloc[top_indices].copy()
    results["Similarity_Score"] = sims[top_indices]

    return results[["Title", "Skills", "Location", "Duration", "Stipend", "Mode", "Similarity_Score"]]
