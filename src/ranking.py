"""
Weighted ranking system for recommendations.
"""

import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime
import re


class RankingSystem:
    """Weighted ranking system for internship recommendations."""
    
    def __init__(
        self,
        skill_weight: float = 0.70,
        preference_weight: float = 0.20,
        quality_weight: float = 0.10
    ):
        """
        Initialize the ranking system.
        
        Args:
            skill_weight: Weight for skill relevance (default: 0.70)
            preference_weight: Weight for user preferences (default: 0.20)
            quality_weight: Weight for internship quality/freshness (default: 0.10)
        """
        self.skill_weight = skill_weight
        self.preference_weight = preference_weight
        self.quality_weight = quality_weight
        
        # Validate weights sum to 1
        total = skill_weight + preference_weight + quality_weight
        if abs(total - 1.0) > 0.01:
            raise ValueError(f"Weights must sum to 1.0, got {total}")
    
    def calculate_skill_score(
        self,
        user_skills: List[str],
        internship_skills: List[str]
    ) -> float:
        """
        Calculate skill relevance score based on matching skills.
        
        Args:
            user_skills: List of user's skills
            internship_skills: List of internship's required skills
            
        Returns:
            Skill score between 0 and 1
        """
        if not user_skills or not internship_skills:
            return 0.0
        
        # Normalize to lowercase for comparison
        user_skills_lower = [s.lower().strip() for s in user_skills]
        internship_skills_lower = [s.lower().strip() for s in internship_skills]
        
        # Count matching skills
        matches = sum(1 for skill in user_skills_lower if skill in internship_skills_lower)
        
        # Calculate score as ratio of matches to user skills
        score = matches / len(user_skills_lower) if user_skills_lower else 0.0
        
        return min(score, 1.0)
    
    def calculate_preference_score(
        self,
        internship: pd.Series,
        preferred_location: Optional[str] = None,
        preferred_mode: Optional[str] = None,
        min_stipend: Optional[int] = None,
        max_stipend: Optional[int] = None,
        preferred_duration: Optional[str] = None
    ) -> float:
        """
        Calculate preference score based on user preferences.
        
        Args:
            internship: Internship record
            preferred_location: Preferred location
            preferred_mode: Preferred work mode
            min_stipend: Minimum stipend
            max_stipend: Maximum stipend
            preferred_duration: Preferred duration
            
        Returns:
            Preference score between 0 and 1
        """
        score = 0.0
        total_criteria = 0
        
        # Location preference
        if preferred_location:
            total_criteria += 1
            if preferred_location.lower() == internship.get("Location", "").lower():
                score += 1.0
            elif preferred_location.lower() == "remote" and internship.get("Mode", "").lower() == "remote":
                score += 0.8
            elif internship.get("Location", "").lower() == "remote":
                score += 0.8
        
        # Mode preference
        if preferred_mode:
            total_criteria += 1
            if preferred_mode.lower() == internship.get("Mode", "").lower():
                score += 1.0
        
        # Stipend preference
        if min_stipend is not None or max_stipend is not None:
            total_criteria += 1
            stipend_str = internship.get("Stipend", "0")
            stipend = self._extract_stipend(stipend_str)
            
            if min_stipend is not None and stipend >= min_stipend:
                score += 0.5
            if max_stipend is not None and stipend <= max_stipend:
                score += 0.5
        
        # Duration preference
        if preferred_duration:
            total_criteria += 1
            if preferred_duration.lower() == internship.get("Duration", "").lower():
                score += 1.0
        
        return score / total_criteria if total_criteria > 0 else 0.0
    
    def _extract_stipend(self, stipend_str: str) -> int:
        """Extract numeric stipend value from string."""
        if pd.isna(stipend_str) or stipend_str == "Not Specified" or stipend_str == "Unpaid":
            return 0
        match = re.search(r'[\d,]+', str(stipend_str))
        if match:
            return int(match.group().replace(',', ''))
        return 0
    
    def calculate_quality_score(
        self,
        internship: pd.Series,
        current_date: datetime = None
    ) -> float:
        """
        Calculate quality/freshness score based on posting date and status.
        
        Args:
            internship: Internship record
            current_date: Current date for freshness calculation
            
        Returns:
            Quality score between 0 and 1
        """
        score = 0.0
        
        # Status score (Open is better)
        if internship.get("Status", "").lower() == "open":
            score += 0.5
        
        # Freshness score (more recent is better)
        if current_date and "Posted_Date" in internship:
            try:
                posted_date = pd.to_datetime(internship["Posted_Date"])
                days_since_posted = (current_date - posted_date).days
                
                # Decay score over time (30-day window)
                if days_since_posted <= 7:
                    score += 0.5
                elif days_since_posted <= 14:
                    score += 0.4
                elif days_since_posted <= 30:
                    score += 0.3
                elif days_since_posted <= 60:
                    score += 0.2
                else:
                    score += 0.1
            except:
                pass
        
        return min(score, 1.0)
    
    def calculate_final_score(
        self,
        skill_score: float,
        preference_score: float,
        quality_score: float
    ) -> float:
        """
        Calculate final weighted score.
        
        Args:
            skill_score: Skill relevance score
            preference_score: Preference match score
            quality_score: Quality/freshness score
            
        Returns:
            Final weighted score between 0 and 1
        """
        final_score = (
            self.skill_weight * skill_score +
            self.preference_weight * preference_score +
            self.quality_weight * quality_score
        )
        
        return min(final_score, 1.0)
    
    def rank_recommendations(
        self,
        recommendations: pd.DataFrame,
        user_skills: List[str],
        preferred_location: Optional[str] = None,
        preferred_mode: Optional[str] = None,
        min_stipend: Optional[int] = None,
        max_stipend: Optional[int] = None,
        preferred_duration: Optional[str] = None,
        current_date: datetime = None
    ) -> pd.DataFrame:
        """
        Apply weighted ranking to recommendations.
        
        Args:
            recommendations: DataFrame of recommended internships with similarity scores
            user_skills: List of user's skills
            preferred_location: Preferred location
            preferred_mode: Preferred work mode
            min_stipend: Minimum stipend
            max_stipend: Maximum stipend
            preferred_duration: Preferred duration
            current_date: Current date for freshness calculation
            
        Returns:
            DataFrame with added ranking scores and sorted by final score
        """
        if recommendations.empty:
            return recommendations
        
        if current_date is None:
            current_date = datetime.now()
        
        results = recommendations.copy()
        
        # Calculate individual scores
        skill_scores = []
        preference_scores = []
        quality_scores = []
        final_scores = []
        
        for _, internship in results.iterrows():
            # Parse internship skills
            internship_skills = []
            if "Skills" in internship and pd.notna(internship["Skills"]):
                internship_skills = [s.strip() for s in str(internship["Skills"]).split(",")]
            
            # Calculate scores
            skill_score = self.calculate_skill_score(user_skills, internship_skills)
            preference_score = self.calculate_preference_score(
                internship, preferred_location, preferred_mode,
                min_stipend, max_stipend, preferred_duration
            )
            quality_score = self.calculate_quality_score(internship, current_date)
            final_score = self.calculate_final_score(skill_score, preference_score, quality_score)
            
            skill_scores.append(skill_score)
            preference_scores.append(preference_score)
            quality_scores.append(quality_score)
            final_scores.append(final_score)
        
        # Add scores to DataFrame
        results["Skill_Score"] = skill_scores
        results["Preference_Score"] = preference_scores
        results["Quality_Score"] = quality_scores
        results["Final_Score"] = final_scores
        
        # Sort by final score (descending)
        results = results.sort_values("Final_Score", ascending=False)
        
        # Reset index
        results = results.reset_index(drop=True)
        
        return results
    
    def update_weights(
        self,
        skill_weight: float = None,
        preference_weight: float = None,
        quality_weight: float = None
    ):
        """
        Update ranking weights.
        
        Args:
            skill_weight: New skill weight
            preference_weight: New preference weight
            quality_weight: New quality weight
        """
        if skill_weight is not None:
            self.skill_weight = skill_weight
        if preference_weight is not None:
            self.preference_weight = preference_weight
        if quality_weight is not None:
            self.quality_weight = quality_weight
        
        # Validate weights
        total = self.skill_weight + self.preference_weight + self.quality_weight
        if abs(total - 1.0) > 0.01:
            raise ValueError(f"Weights must sum to 1.0, got {total}")
