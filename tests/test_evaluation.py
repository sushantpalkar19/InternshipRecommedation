"""
Unit tests for evaluation metrics.
"""

import sys
import os
import unittest

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.evaluation import RecommendationEvaluator


class TestEvaluationMetrics(unittest.TestCase):
    """Test evaluation metrics functionality."""
    
    def setUp(self):
        """Set up evaluator."""
        self.evaluator = RecommendationEvaluator(relevance_threshold=3)
    
    def test_precision_at_k(self):
        """Test Precision@"""
        recommended = [1, 2, 3, 4, 5]
        relevant = {1, 3, 5}
        precision = self.evaluator.precision_at_k(recommended, relevant, 5)
        self.assertEqual(precision, 0.6)  # 3 out of 5 are relevant
    
    def test_recall_at_k(self):
        """Test Recall@"""
        recommended = [1, 2, 3, 4, 5]
        relevant = {1, 3, 5, 7, 9}
        recall = self.evaluator.recall_at_k(recommended, relevant, 5)
        self.assertEqual(recall, 0.6)  # 3 out of 5 relevant items retrieved
    
    def test_mrr(self):
        """Test Mean Reciprocal Rank."""
        recommended = [5, 3, 1, 2, 4]
        relevant = {1, 3, 5}
        mrr = self.evaluator.mrr(recommended, relevant)
        # First relevant item is at position 0 (5), so 1/(0+1) = 1.0
        self.assertEqual(mrr, 1.0)
    
    def test_mrr_no_relevant(self):
        """Test MRR with no relevant items."""
        recommended = [1, 2, 3, 4, 5]
        relevant = set()
        mrr = self.evaluator.mrr(recommended, relevant)
        self.assertEqual(mrr, 0.0)
    
    def test_ndcg_at_k_with_known_relevance(self):
        """Test NDCG@K with known relevance scores."""
        recommended = [1, 2, 3]
        relevance_scores = {1: 5, 2: 0, 3: 3}
        ndcg = self.evaluator.ndcg_at_k(recommended, relevance_scores, 3)
        
        # Calculate expected NDCG
        # DCG = (2^5-1)/log2(2) + (2^0-1)/log2(3) + (2^3-1)/log2(4)
        # DCG = 31/1 + 0/1.585 + 7/2 = 31 + 0 + 3.5 = 34.5
        # Ideal DCG = (2^5-1)/log2(2) + (2^3-1)/log2(3) + (2^0-1)/log2(4)
        # Ideal DCG = 31/1 + 7/1.585 + 0/2 = 31 + 4.417 + 0 = 35.417
        # NDCG = 34.5 / 35.417 ≈ 0.974
        
        self.assertGreater(ndcg, 0.9)  # Should be close to 1.0
        self.assertLessEqual(ndcg, 1.0)
    
    def test_ndcg_at_k_zero_relevance(self):
        """Test NDCG@K with all zero relevance."""
        recommended = [1, 2, 3]
        relevance_scores = {1: 0, 2: 0, 3: 0}
        ndcg = self.evaluator.ndcg_at_k(recommended, relevance_scores, 3)
        self.assertEqual(ndcg, 0.0)
    
    def test_ndcg_at_k_perfect_ranking(self):
        """Test NDCG@K with perfect ranking."""
        recommended = [1, 2, 3]
        relevance_scores = {1: 5, 2: 4, 3: 3}
        ndcg = self.evaluator.ndcg_at_k(recommended, relevance_scores, 3)
        self.assertEqual(ndcg, 1.0)  # Perfect ranking should give NDCG = 1.0
    
    def test_coverage(self):
        """Test catalog coverage."""
        all_recommended = [{1, 2, 3}, {2, 3, 4}, {3, 4, 5}]
        total_catalog = 10
        coverage = self.evaluator.coverage(all_recommended, total_catalog)
        self.assertEqual(coverage, 0.5)  # 5 unique items out of 10
    
    def test_zero_result_rate(self):
        """Test zero result rate."""
        all_recommended = [[1, 2, 3], [], [4, 5], []]
        zero_rate = self.evaluator.zero_result_rate(all_recommended)
        self.assertEqual(zero_rate, 0.5)  # 2 out of 4 queries returned no results
    
    def test_evaluate_query(self):
        """Test full query evaluation."""
        recommended = [1, 2, 3, 4, 5]
        relevant = {1, 3, 5}
        relevance_scores = {1: 5, 2: 0, 3: 3, 4: 0, 5: 4}
        
        results = self.evaluator.evaluate_query(recommended, relevant, relevance_scores, [5, 10])
        
        self.assertIn("precision@5", results)
        self.assertIn("recall@5", results)
        self.assertIn("ndcg@5", results)
        self.assertIn("mrr", results)
        
        # Verify NDCG is not zero
        self.assertGreater(results["ndcg@5"], 0.0)


if __name__ == "__main__":
    unittest.main()
