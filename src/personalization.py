"""
Basic personalization based on user feedback.
"""

import pandas as pd
from typing import Dict, List, Set
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import get_data_loader


class PersonalizationEngine:
    """Simple personalization engine based on user feedback."""
    
    def __init__(self):
        """Initialize the personalization engine."""
        self.data_loader = get_data_loader()
        self.df = self.data_loader.get_data()
        
        # Domain weights (default = 1.0)
        self.domain_weights = {}
        
        # Initialize all domains with weight 1.0
        for domain in self.data_loader.get_unique_domains():
            self.domain_weights[domain] = 1.0
    
    def update_from_feedback(
        self,
        liked_internships: List[int],
        disliked_internships: List[int]
    ):
        """
        Update domain weights based on user feedback.
        
        Args:
            liked_internships: List of internship IDs user liked
            disliked_internships: List of internship IDs user disliked
        """
        if not liked_internships and not disliked_internships:
            return
        
        # Get domains of liked internships
        liked_domains = []
        if liked_internships:
            liked_df = self.df[self.df["Internship_ID"].isin(liked_internships)]
            liked_domains = liked_df["Domain"].tolist()
        
        # Get domains of disliked internships
        disliked_domains = []
        if disliked_internships:
            disliked_df = self.df[self.df["Internship_ID"].isin(disliked_internships)]
            disliked_domains = disliked_df["Domain"].tolist()
        
        # Update weights
        # Increase weight for liked domains
        for domain in liked_domains:
            if domain in self.domain_weights:
                self.domain_weights[domain] = min(self.domain_weights[domain] * 1.2, 2.0)  # Max 2.0
        
        # Decrease weight for disliked domains
        for domain in disliked_domains:
            if domain in self.domain_weights:
                self.domain_weights[domain] = max(self.domain_weights[domain] * 0.8, 0.5)  # Min 0.5
        
        print(f"Updated domain weights: {self.domain_weights}")
    
    def apply_personalization(
        self,
        recommendations: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Apply personalization weights to recommendations.
        
        Args:
            recommendations: DataFrame of recommendations
            
        Returns:
            DataFrame with adjusted scores
        """
        if recommendations.empty:
            return recommendations
        
        results = recommendations.copy()
        
        # Add personalization score
        personalization_scores = []
        for _, row in results.iterrows():
            domain = row.get("Domain", "")
            weight = self.domain_weights.get(domain, 1.0)
            personalization_scores.append(weight)
        
        results["Personalization_Weight"] = personalization_scores
        
        # Adjust final score if it exists
        if "Final_Score" in results.columns:
            results["Final_Score"] = results["Final_Score"] * results["Personalization_Weight"]
        
        # Re-sort by final score
        if "Final_Score" in results.columns:
            results = results.sort_values("Final_Score", ascending=False)
            results = results.reset_index(drop=True)
        
        return results
    
    def get_domain_weights(self) -> Dict[str, float]:
        """Get current domain weights."""
        return self.domain_weights.copy()
    
    def reset_weights(self):
        """Reset all domain weights to 1.0."""
        for domain in self.domain_weights:
            self.domain_weights[domain] = 1.0


# Global personalization engine instance
_personalization_engine = None


def get_personalization_engine() -> PersonalizationEngine:
    """
    Get or create the global personalization engine instance.
    
    Returns:
        PersonalizationEngine instance
    """
    global _personalization_engine
    
    if _personalization_engine is None:
        _personalization_engine = PersonalizationEngine()
    
    return _personalization_engine
