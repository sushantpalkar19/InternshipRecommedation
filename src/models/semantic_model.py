"""
Semantic embedding model using Sentence Transformers.
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.data_loader import get_data_loader
from src.preprocessing import normalize_skills


class SemanticModel:
    """Semantic embedding model using Sentence Transformers."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the semantic model.
        
        Args:
            model_name: Name of the Sentence Transformer model to use
        """
        self.model_name = model_name
        self.model = None
        self.embeddings = None
        self.df = None
        self._load_model_and_data()
    
    def _load_model_and_data(self):
        """Load the Sentence Transformer model and data."""
        try:
            from sentence_transformers import SentenceTransformer
            print(f"Loading Sentence Transformer model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            print("Model loaded successfully")
        except ImportError:
            print("Error: sentence-transformers not installed. Install with: pip install sentence-transformers")
            raise
        
        # Load data
        data_loader = get_data_loader()
        self.df = data_loader.get_data()
        
        # Generate embeddings for internships
        self._generate_embeddings()
    
    def _generate_embeddings(self):
        """Generate embeddings for all internships."""
        print("Generating embeddings for internships...")
        
        # Combine title and skills for embedding
        texts = []
        for _, row in self.df.iterrows():
            text = f"{row['Title']} {row.get('Skills', '')} {row.get('Description', '')}"
            texts.append(text)
        
        # Generate embeddings
        self.embeddings = self.model.encode(texts, show_progress_bar=True)
        print(f"Generated embeddings for {len(self.embeddings)} internships")
    
    def get_embedding(self, text: str) -> np.ndarray:
        """
        Get embedding for a single text.
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector
        """
        return self.model.encode(text)
    
    def recommend(self, user_skills: str, top_n: int = 10) -> pd.DataFrame:
        """
        Recommend internships using semantic similarity.
        
        Args:
            user_skills: User skills string
            top_n: Number of recommendations to return
            
        Returns:
            DataFrame with recommended internships
        """
        # Normalize user skills
        normalized_skills = normalize_skills(user_skills)
        
        if not normalized_skills.strip():
            return pd.DataFrame()
        
        # Create query text
        query_text = f"User skills: {normalized_skills}"
        
        # Get query embedding
        query_embedding = self.get_embedding(query_text)
        
        # Calculate cosine similarity
        query_embedding = query_embedding.reshape(1, -1)
        similarities = cosine_similarity(query_embedding, self.embeddings).flatten()
        
        # Get top matches
        top_indices = similarities.argsort()[::-1][:top_n]
        
        results = self.df.iloc[top_indices].copy()
        results["Similarity_Score"] = similarities[top_indices]
        
        # Columns to return
        return_cols = ["Internship_ID", "Title", "Company", "Skills", "Location", "Duration", "Stipend", "Mode", "Similarity_Score"]
        available_cols = [col for col in return_cols if col in results.columns]
        
        return results[available_cols]


# Global model instance
_semantic_model = None


def get_semantic_model(model_name: str = "all-MiniLM-L6-v2") -> SemanticModel:
    """
    Get or create the global semantic model instance.
    
    Args:
        model_name: Name of the Sentence Transformer model
        
    Returns:
        SemanticModel instance
    """
    global _semantic_model
    
    if _semantic_model is None:
        _semantic_model = SemanticModel(model_name)
    
    return _semantic_model


def recommend_semantic(user_skills: str, top_n: int = 10) -> pd.DataFrame:
    """
    Recommend internships using semantic similarity.
    
    Args:
        user_skills: User skills string
        top_n: Number of recommendations to return
        
    Returns:
        DataFrame with recommended internships
    """
    model = get_semantic_model()
    return model.recommend(user_skills, top_n)
