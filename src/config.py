"""
Configuration file for the Internship Recommendation System.
"""


class Config:
    """Configuration settings for the recommendation system."""
    
    # Ranking weights (should sum to 1.0)
    RANKING_WEIGHTS = {
        "skill_weight": 0.70,
        "preference_weight": 0.20,
        "quality_weight": 0.10
    }
    
    # Model selection strategy
    MODEL_SELECTION = {
        "primary_metric": "ndcg@10",  # Primary metric for model selection
        "secondary_metrics": ["mrr", "precision@10", "recall@10"],  # Secondary metrics
        "prefer_simpler": True,  # Prefer simpler/faster models when metrics are close
        "metric_threshold": 0.05  # Threshold for considering metrics "close"
    }
    
    # Available models
    AVAILABLE_MODELS = [
        "tfidf",
        "countvectorizer", 
        "word2vec",
        "semantic"
    ]
    
    # Default model (used if auto-selection fails)
    DEFAULT_MODEL = "tfidf"
    
    # Evaluation settings
    EVALUATION = {
        "k_values": [5, 10],  # K values for Precision@K, Recall@K, NDCG@K
        "relevance_threshold": 3,  # Minimum relevance score to consider an item relevant
        "top_n_recommendations": 10  # Number of recommendations to evaluate
    }
    
    # Data paths
    DATA_PATHS = {
        "clean_dataset": "data/processed/internships_clean.csv",
        "evaluation_dataset": "data/evaluation/evaluation_dataset_expanded.csv",
        "ground_truth": "data/evaluation/ground_truth_expanded.json",
        "model_comparison": "data/evaluation/model_comparison.csv"
    }
    
    # Skill normalization settings
    SKILL_NORMALIZATION = {
        "case_sensitive": False,
        "remove_duplicates": True,
        "apply_aliases": True
    }
    
    # UI settings
    UI = {
        "default_top_n": 10,
        "max_top_n": 50,
        "enable_filters": True,
        "enable_explanations": True,
        "enable_ranking_weights": True
    }
    
    @classmethod
    def get_ranking_weights(cls) -> dict:
        """Get current ranking weights."""
        return cls.RANKING_WEIGHTS.copy()
    
    @classmethod
    def set_ranking_weights(cls, skill_weight: float, preference_weight: float, quality_weight: float):
        """
        Update ranking weights.
        
        Args:
            skill_weight: Weight for skill relevance
            preference_weight: Weight for user preferences
            quality_weight: Weight for quality/freshness
        """
        total = skill_weight + preference_weight + quality_weight
        if abs(total - 1.0) > 0.01:
            raise ValueError(f"Weights must sum to 1.0, got {total}")
        
        cls.RANKING_WEIGHTS = {
            "skill_weight": skill_weight,
            "preference_weight": preference_weight,
            "quality_weight": quality_weight
        }
    
    @classmethod
    def get_model_selection_config(cls) -> dict:
        """Get model selection configuration."""
        return cls.MODEL_SELECTION.copy()
