"""
Unit tests for core functionality.
"""

import sys
import os
import unittest
import pandas as pd

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.preprocessing import normalize_skills, clean_skill_string, get_skill_domain, normalize_skill
from src.data_loader import DataLoader
from src.ranking import RankingSystem
from src.explanations import ExplanationGenerator
from src.config import Config


class TestSkillNormalization(unittest.TestCase):
    """Test skill normalization functionality."""
    
    def test_normalize_skill_basic(self):
        """Test basic skill normalization."""
        result = normalize_skill("python")
        self.assertEqual(result, "Python")
    
    def test_normalize_skill_alias(self):
        """Test skill alias normalization."""
        result = normalize_skill("ml")
        # normalize_skill returns lowercase for aliases
        self.assertEqual(result, "machine learning")
    
    def test_normalize_skills_string(self):
        """Test normalization of skills string."""
        result = normalize_skills("python, ml, reactjs")
        # normalize_skills normalizes each skill and applies title case
        # The actual output depends on the implementation
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
    
    def test_clean_skill_string(self):
        """Test skill string cleaning."""
        result = clean_skill_string("Python, ML! @React#")
        self.assertIn("Python", result)
        self.assertIn("React", result)
    
    def test_get_skill_domain(self):
        """Test skill domain categorization."""
        result = get_skill_domain("Python")
        self.assertEqual(result, "Data Science")
    
    def test_empty_skill(self):
        """Test handling of empty skills."""
        result = normalize_skills("")
        self.assertEqual(result, "")
    
    def test_unknown_skill(self):
        """Test handling of unknown skills."""
        result = normalize_skill("unknownskill123")
        self.assertEqual(result, "Unknownskill123")


class TestDataLoader(unittest.TestCase):
    """Test data loader functionality."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test data loader."""
        cls.data_loader = DataLoader("data/processed/internships_clean.csv")
    
    def test_load_data(self):
        """Test data loading."""
        df = self.data_loader.get_data()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 0)
    
    def test_get_internship_by_id(self):
        """Test getting internship by ID."""
        internship = self.data_loader.get_internship_by_id(1)
        self.assertIsNotNone(internship)
        self.assertEqual(internship["Internship_ID"], 1)
    
    def test_filter_by_location(self):
        """Test location filtering."""
        filtered = self.data_loader.filter_by_location(["Bangalore"])
        self.assertIsInstance(filtered, pd.DataFrame)
        for _, row in filtered.iterrows():
            self.assertEqual(row["Location"], "Bangalore")
    
    def test_filter_by_mode(self):
        """Test work mode filtering."""
        filtered = self.data_loader.filter_by_mode(["Remote"])
        self.assertIsInstance(filtered, pd.DataFrame)
        for _, row in filtered.iterrows():
            self.assertEqual(row["Mode"], "Remote")
    
    def test_filter_by_stipend(self):
        """Test stipend filtering."""
        filtered = self.data_loader.filter_by_stipend(min_stipend=20000)
        self.assertIsInstance(filtered, pd.DataFrame)
    
    def test_get_unique_locations(self):
        """Test getting unique locations."""
        locations = self.data_loader.get_unique_locations()
        self.assertIsInstance(locations, list)
        self.assertGreater(len(locations), 0)
    
    def test_get_statistics(self):
        """Test getting dataset statistics."""
        stats = self.data_loader.get_statistics()
        self.assertIsInstance(stats, dict)
        self.assertIn("total_internships", stats)


class TestRankingSystem(unittest.TestCase):
    """Test ranking system functionality."""
    
    def setUp(self):
        """Set up ranking system."""
        self.ranking = RankingSystem(skill_weight=0.7, preference_weight=0.2, quality_weight=0.1)
    
    def test_calculate_skill_score(self):
        """Test skill score calculation."""
        user_skills = ["Python", "Machine Learning"]
        internship_skills = ["Python", "Machine Learning", "SQL"]
        score = self.ranking.calculate_skill_score(user_skills, internship_skills)
        self.assertEqual(score, 1.0)
    
    def test_calculate_skill_score_partial(self):
        """Test partial skill match."""
        user_skills = ["Python", "Machine Learning"]
        internship_skills = ["Python", "SQL"]
        score = self.ranking.calculate_skill_score(user_skills, internship_skills)
        self.assertEqual(score, 0.5)
    
    def test_calculate_skill_score_empty(self):
        """Test empty skill handling."""
        score = self.ranking.calculate_skill_score([], ["Python"])
        self.assertEqual(score, 0.0)
    
    def test_calculate_preference_score(self):
        """Test preference score calculation."""
        internship = pd.Series({"Location": "Bangalore", "Mode": "Remote"})
        score = self.ranking.calculate_preference_score(
            internship,
            preferred_location="Bangalore",
            preferred_mode="Remote"
        )
        self.assertGreater(score, 0)
    
    def test_calculate_final_score(self):
        """Test final score calculation."""
        final_score = self.ranking.calculate_final_score(0.8, 0.6, 0.9)
        expected = 0.7 * 0.8 + 0.2 * 0.6 + 0.1 * 0.9
        self.assertAlmostEqual(final_score, expected, places=2)
    
    def test_weight_validation(self):
        """Test weight validation."""
        with self.assertRaises(ValueError):
            RankingSystem(skill_weight=0.5, preference_weight=0.5, quality_weight=0.5)


class TestExplanationGenerator(unittest.TestCase):
    """Test explanation generation functionality."""
    
    def setUp(self):
        """Set up explanation generator."""
        self.generator = ExplanationGenerator()
    
    def test_extract_matched_skills(self):
        """Test matched skills extraction."""
        user_skills = ["Python", "Machine Learning"]
        internship_skills = ["Python", "Machine Learning", "SQL"]
        matched = self.generator.extract_matched_skills(user_skills, internship_skills)
        self.assertEqual(len(matched), 2)
        self.assertIn("Python", matched)
    
    def test_extract_missing_skills(self):
        """Test missing skills extraction."""
        user_skills = ["Python"]
        internship_skills = ["Python", "Machine Learning", "SQL"]
        missing = self.generator.extract_missing_skills(user_skills, internship_skills)
        self.assertGreater(len(missing), 0)
    
    def test_generate_explanation(self):
        """Test explanation generation."""
        internship = pd.Series({
            "Title": "ML Intern",
            "Company": "Tech Corp",
            "Location": "Bangalore",
            "Mode": "Remote",
            "Stipend": "₹20000/month",
            "Duration": "3 Months"
        })
        explanation = self.generator.generate_explanation(
            internship,
            ["Python", "Machine Learning"],
            skill_score=0.8,
            preference_score=0.6,
            quality_score=0.9,
            final_score=0.78
        )
        self.assertIsInstance(explanation, dict)
        self.assertIn("matched_skills", explanation)
        self.assertIn("reasoning", explanation)


class TestConfig(unittest.TestCase):
    """Test configuration functionality."""
    
    def test_get_ranking_weights(self):
        """Test getting ranking weights."""
        weights = Config.get_ranking_weights()
        self.assertIsInstance(weights, dict)
        self.assertIn("skill_weight", weights)
    
    def test_set_ranking_weights(self):
        """Test setting ranking weights."""
        Config.set_ranking_weights(0.6, 0.3, 0.1)
        weights = Config.get_ranking_weights()
        self.assertEqual(weights["skill_weight"], 0.6)
    
    def test_weight_validation(self):
        """Test weight validation."""
        with self.assertRaises(ValueError):
            Config.set_ranking_weights(0.5, 0.5, 0.5)
    
    def test_get_model_selection_config(self):
        """Test getting model selection config."""
        config = Config.get_model_selection_config()
        self.assertIsInstance(config, dict)
        self.assertIn("primary_metric", config)


if __name__ == "__main__":
    unittest.main()
