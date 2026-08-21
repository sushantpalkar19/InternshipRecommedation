"""
Hybrid recommendation system combining multiple models.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import Config
from src.data_loader import get_data_loader
from src.preprocessing import normalize_skills
from src.ranking import RankingSystem


class HybridRecommender:
    """Hybrid recommendation system combining multiple models."""
    
    def __init__(self, config: Config = None):
        """
        Initialize the hybrid recommender.
        
        Args:
            config: Configuration object (uses default if None)
        """
        self.config = config or Config()
        self.data_loader = get_data_loader()
        self.df = self.data_loader.get_data()
        self.ranking_system = RankingSystem(
            skill_weight=self.config.RANKING_WEIGHTS["skill_weight"],
            preference_weight=self.config.RANKING_WEIGHTS["preference_weight"],
            quality_weight=self.config.RANKING_WEIGHTS["quality_weight"]
        )
        
        # Load models
        self._load_models()
    
    def _load_models(self):
        """Load all available recommendation models."""
        try:
            # Import models directly
            import models.model_tfidf as tfidf_module
            import models.model_countvec as countvec_module
            import models.model_word2vec as word2vec_module
            
            self.models = {
                "tfidf": tfidf_module.recommend_tfidf,
                "countvectorizer": countvec_module.recommend_countvec,
                "word2vec": word2vec_module.recommend_word2vec
            }
            
            print("Base models loaded successfully")
            
            # Try to load semantic model
            try:
                from src.models.semantic_model import recommend_semantic
                self.models["semantic"] = recommend_semantic
                print("Semantic model loaded successfully")
            except ImportError:
                print("Semantic model not available (sentence-transformers not installed)")
            except Exception as e:
                print(f"Error loading semantic model: {e}")
                
        except ImportError as e:
            print(f"Error loading models: {e}")
            self.models = {}
    
    def recommend(
        self,
        user_skills: str,
        model_name: str = None,
        top_n: int = 10,
        apply_ranking: bool = True,
        preferred_location: Optional[str] = None,
        preferred_mode: Optional[str] = None,
        min_stipend: Optional[int] = None,
        max_stipend: Optional[int] = None,
        preferred_duration: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Generate recommendations using specified or best model.
        
        Args:
            user_skills: User skills string
            model_name: Specific model to use (None for auto-selection)
            top_n: Number of recommendations
            apply_ranking: Whether to apply weighted ranking
            preferred_location: Preferred location
            preferred_mode: Preferred work mode
            min_stipend: Minimum stipend
            max_stipend: Maximum stipend
            preferred_duration: Preferred duration
            
        Returns:
            DataFrame with recommendations
        """
        # Normalize user skills
        normalized_skills = normalize_skills(user_skills)
        user_skills_list = [s.strip() for s in normalized_skills.split(",")]
        
        # Select model
        if model_name is None:
            model_name = self._select_best_model()
        
        if model_name not in self.models:
            print(f"Model {model_name} not available, using default")
            model_name = self.config.DEFAULT_MODEL
        
        # Get base recommendations
        model_func = self.models[model_name]
        results = model_func(user_skills, top_n=top_n * 2)  # Get more for ranking
        
        if results.empty:
            return results
        
        # Apply weighted ranking if requested
        if apply_ranking:
            results = self.ranking_system.rank_recommendations(
                results,
                user_skills_list,
                preferred_location=preferred_location,
                preferred_mode=preferred_mode,
                min_stipend=min_stipend,
                max_stipend=max_stipend,
                preferred_duration=preferred_duration
            )
        
        # Return top N
        return results.head(top_n)
    
    def _select_best_model(self) -> str:
        """
        Select the best model based on evaluation results.
        
        Returns:
            Name of the best model
        """
        try:
            # Try to load human-curated comparison first, then expanded
            for comparison_path in ["data/evaluation/model_comparison_human.csv", 
                                   "data/evaluation/model_comparison.csv"]:
                try:
                    comparison_df = pd.read_csv(comparison_path)
                    if not comparison_df.empty:
                        break
                except:
                    continue
            else:
                return self.config.DEFAULT_MODEL
            
            # Get model selection config
            selection_config = self.config.get_model_selection_config()
            primary_metric = selection_config["primary_metric"]
            
            # Filter out models with zero results
            valid_models = comparison_df[comparison_df["zero_result_rate"] < 1.0]
            
            if valid_models.empty:
                return self.config.DEFAULT_MODEL
            
            # Find best model based on primary metric
            best_model = valid_models.loc[valid_models[primary_metric].idxmax(), "Model"]
            
            # Map display names to internal names
            model_name_mapping = {
                "TF-IDF": "tfidf",
                "CountVectorizer": "countvectorizer",
                "Word2Vec": "word2vec",
                "Semantic": "semantic",
                "Hybrid": "tfidf"  # Hybrid falls back to tfidf
            }
            
            # If prefer simpler and metrics are close, choose simpler model
            if selection_config["prefer_simpler"]:
                threshold = selection_config["metric_threshold"]
                best_score = valid_models.loc[valid_models[primary_metric].idxmax(), primary_metric]
                
                # Check if simpler models are close
                simpler_models = ["TF-IDF", "CountVectorizer"]
                for simpler_model in simpler_models:
                    if simpler_model in valid_models["Model"].values:
                        simpler_score = valid_models.loc[valid_models["Model"] == simpler_model, primary_metric].values[0]
                        if abs(best_score - simpler_score) <= threshold:
                            best_model = simpler_model
                            break
            
            return model_name_mapping.get(best_model, "tfidf")
            
        except Exception as e:
            print(f"Error selecting best model: {e}, using default")
            return self.config.DEFAULT_MODEL
    
    def get_available_models(self) -> List[str]:
        """Get list of available models."""
        return list(self.models.keys())
    
    def compare_models(
        self,
        user_skills: str,
        top_n: int = 10
    ) -> Dict[str, pd.DataFrame]:
        """
        Compare recommendations from all available models.
        
        Args:
            user_skills: User skills string
            top_n: Number of recommendations per model
            
        Returns:
            Dictionary mapping model names to recommendation DataFrames
        """
        results = {}
        
        for model_name in self.models.keys():
            try:
                model_results = self.recommend(
                    user_skills,
                    model_name=model_name,
                    top_n=top_n,
                    apply_ranking=False
                )
                results[model_name] = model_results
            except Exception as e:
                print(f"Error with model {model_name}: {e}")
                results[model_name] = pd.DataFrame()
        
        return results


# Global recommender instance
_hybrid_recommender = None


def get_hybrid_recommender(config: Config = None) -> HybridRecommender:
    """
    Get or create the global hybrid recommender instance.
    
    Args:
        config: Configuration object
        
    Returns:
        HybridRecommender instance
    """
    global _hybrid_recommender
    
    if _hybrid_recommender is None:
        _hybrid_recommender = HybridRecommender(config)
    
    return _hybrid_recommender
