"""
Recommendation explanation system.
"""

import pandas as pd
from typing import List, Dict, Tuple


class ExplanationGenerator:
    """Generate explanations for recommendation results."""
    
    def __init__(self):
        """Initialize the explanation generator."""
        pass
    
    def extract_matched_skills(
        self,
        user_skills: List[str],
        internship_skills: List[str]
    ) -> List[str]:
        """
        Extract skills that match between user and internship.
        
        Args:
            user_skills: List of user's skills
            internship_skills: List of internship's required skills
            
        Returns:
            List of matched skills
        """
        if not user_skills or not internship_skills:
            return []
        
        user_skills_lower = [s.lower().strip() for s in user_skills]
        internship_skills_lower = [s.lower().strip() for s in internship_skills]
        
        matched = []
        for user_skill in user_skills_lower:
            if user_skill in internship_skills_lower:
                # Find the original casing from internship skills
                for orig_skill in internship_skills:
                    if orig_skill.lower().strip() == user_skill:
                        matched.append(orig_skill)
                        break
        
        return matched
    
    def extract_missing_skills(
        self,
        user_skills: List[str],
        internship_skills: List[str]
    ) -> List[str]:
        """
        Extract skills from internship that user doesn't have.
        
        Args:
            user_skills: List of user's skills
            internship_skills: List of internship's required skills
            
        Returns:
            List of missing/useful skills
        """
        if not user_skills or not internship_skills:
            return []
        
        user_skills_lower = [s.lower().strip() for s in user_skills]
        internship_skills_lower = [s.lower().strip() for s in internship_skills]
        
        missing = []
        for i, intern_skill_lower in enumerate(internship_skills_lower):
            if intern_skill_lower not in user_skills_lower:
                missing.append(internship_skills[i])
        
        return missing
    
    def generate_explanation(
        self,
        internship: pd.Series,
        user_skills: List[str],
        skill_score: float,
        preference_score: float,
        quality_score: float,
        final_score: float
    ) -> Dict[str, any]:
        """
        Generate a comprehensive explanation for a recommendation.
        
        Args:
            internship: Internship record
            user_skills: List of user's skills
            skill_score: Calculated skill score
            preference_score: Calculated preference score
            quality_score: Calculated quality score
            final_score: Final weighted score
            
        Returns:
            Dictionary containing explanation components
        """
        # Parse internship skills
        internship_skills = []
        if "Skills" in internship and pd.notna(internship["Skills"]):
            internship_skills = [s.strip() for s in str(internship["Skills"]).split(",")]
        
        # Extract matched and missing skills
        matched_skills = self.extract_matched_skills(user_skills, internship_skills)
        missing_skills = self.extract_missing_skills(user_skills, internship_skills)
        
        # Generate reasoning text
        reasoning = self._generate_reasoning(
            matched_skills,
            internship,
            skill_score,
            preference_score,
            quality_score
        )
        
        # Build explanation dictionary
        explanation = {
            "match_percentage": int(final_score * 100),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills[:5],  # Limit to top 5
            "skill_score": int(skill_score * 100),
            "preference_score": int(preference_score * 100),
            "quality_score": int(quality_score * 100),
            "reasoning": reasoning,
            "internship_title": internship.get("Title", ""),
            "company": internship.get("Company", ""),
            "location": internship.get("Location", ""),
            "mode": internship.get("Mode", ""),
            "stipend": internship.get("Stipend", ""),
            "duration": internship.get("Duration", "")
        }
        
        return explanation
    
    def _generate_reasoning(
        self,
        matched_skills: List[str],
        internship: pd.Series,
        skill_score: float,
        preference_score: float,
        quality_score: float
    ) -> str:
        """
        Generate natural language reasoning for the recommendation.
        
        Args:
            matched_skills: List of matched skills
            internship: Internship record
            skill_score: Skill score
            preference_score: Preference score
            quality_score: Quality score
            
        Returns:
            Natural language explanation
        """
        reasons = []
        
        # Skill-based reasoning
        if matched_skills:
            if len(matched_skills) >= 3:
                reasons.append(f"Strong match with your skills: {', '.join(matched_skills[:3])}")
            elif len(matched_skills) == 2:
                reasons.append(f"Good match with your skills: {', '.join(matched_skills)}")
            else:
                reasons.append(f"Matches your skill: {matched_skills[0]}")
        
        # Preference-based reasoning
        if preference_score > 0.7:
            location = internship.get("Location", "")
            mode = internship.get("Mode", "")
            if location and mode:
                reasons.append(f"Aligns with your preference for {location} and {mode} work")
            elif location:
                reasons.append(f"Matches your preferred location: {location}")
            elif mode:
                reasons.append(f"Matches your preferred work mode: {mode}")
        
        # Quality-based reasoning
        if quality_score > 0.7:
            reasons.append("Recently posted opportunity")
        
        # Combine reasons
        if not reasons:
            return "This internship matches your profile based on overall similarity."
        
        return ". ".join(reasons) + "."
    
    def generate_batch_explanations(
        self,
        recommendations: pd.DataFrame,
        user_skills: List[str],
        ranking_scores: pd.DataFrame = None
    ) -> List[Dict[str, any]]:
        """
        Generate explanations for multiple recommendations.
        
        Args:
            recommendations: DataFrame of recommended internships
            user_skills: List of user's skills
            ranking_scores: DataFrame with calculated ranking scores (optional)
            
        Returns:
            List of explanation dictionaries
        """
        explanations = []
        
        for idx, internship in recommendations.iterrows():
            # Get scores if available
            if ranking_scores is not None and idx < len(ranking_scores):
                skill_score = ranking_scores.iloc[idx].get("Skill_Score", 0.5)
                preference_score = ranking_scores.iloc[idx].get("Preference_Score", 0.5)
                quality_score = ranking_scores.iloc[idx].get("Quality_Score", 0.5)
                final_score = ranking_scores.iloc[idx].get("Final_Score", 0.5)
            else:
                # Use similarity score if ranking scores not available
                final_score = internship.get("Similarity_Score", 0.5)
                skill_score = final_score
                preference_score = 0.5
                quality_score = 0.5
            
            explanation = self.generate_explanation(
                internship,
                user_skills,
                skill_score,
                preference_score,
                quality_score,
                final_score
            )
            
            explanations.append(explanation)
        
        return explanations
    
    def format_explanation_for_display(self, explanation: Dict[str, any]) -> str:
        """
        Format explanation for display in UI.
        
        Args:
            explanation: Explanation dictionary
            
        Returns:
            Formatted string for display
        """
        lines = []
        
        # Header
        lines.append(f"**{explanation['internship_title']}**")
        lines.append(f"{explanation['company']}")
        lines.append("")
        
        # Match percentage
        lines.append(f"**Match Score: {explanation['match_percentage']}%**")
        lines.append("")
        
        # Details
        lines.append(f"📍 {explanation['location']}")
        lines.append(f"💼 {explanation['mode']}")
        lines.append(f"💰 {explanation['stipend']}")
        lines.append(f"⏱ {explanation['duration']}")
        lines.append("")
        
        # Matched skills
        if explanation['matched_skills']:
            lines.append("**✓ Matched Skills:**")
            lines.append(", ".join(explanation['matched_skills']))
            lines.append("")
        
        # Missing skills
        if explanation['missing_skills']:
            lines.append("**Missing / Useful Skills:**")
            lines.append(", ".join(explanation['missing_skills']))
            lines.append("")
        
        # Reasoning
        lines.append("**Why recommended?**")
        lines.append(explanation['reasoning'])
        
        return "\n".join(lines)
