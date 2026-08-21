"""
Evaluation metrics for recommendation systems.
"""

import numpy as np
from typing import List, Dict, Set
import pandas as pd


class RecommendationEvaluator:
    """Evaluator for recommendation system metrics."""
    
    def __init__(self, relevance_threshold: int = 3):
        """
        Initialize the evaluator.
        
        Args:
            relevance_threshold: Minimum relevance score to consider an item relevant (0-5 scale)
        """
        self.relevance_threshold = relevance_threshold
    
    def precision_at_k(self, recommended_ids: List[int], relevant_ids: Set[int], k: int) -> float:
        """
        Calculate Precision@K.
        
        Args:
            recommended_ids: List of recommended internship IDs (ordered by relevance)
            relevant_ids: Set of relevant internship IDs
            k: Number of recommendations to consider
            
        Returns:
            Precision@K score
        """
        if k <= 0 or not recommended_ids:
            return 0.0
        
        k = min(k, len(recommended_ids))
        top_k = recommended_ids[:k]
        
        relevant_in_top_k = sum(1 for item_id in top_k if item_id in relevant_ids)
        
        return relevant_in_top_k / k
    
    def recall_at_k(self, recommended_ids: List[int], relevant_ids: Set[int], k: int) -> float:
        """
        Calculate Recall@K.
        
        Args:
            recommended_ids: List of recommended internship IDs (ordered by relevance)
            relevant_ids: Set of relevant internship IDs
            k: Number of recommendations to consider
            
        Returns:
            Recall@K score
        """
        if not relevant_ids:
            return 0.0
        
        k = min(k, len(recommended_ids))
        top_k = recommended_ids[:k]
        
        relevant_in_top_k = sum(1 for item_id in top_k if item_id in relevant_ids)
        
        return relevant_in_top_k / len(relevant_ids)
    
    def ndcg_at_k(self, recommended_ids: List[int], relevance_scores: Dict[int, int], k: int) -> float:
        """
        Calculate Normalized Discounted Cumulative Gain@K.
        
        Args:
            recommended_ids: List of recommended internship IDs (ordered by relevance)
            relevance_scores: Dictionary mapping internship IDs to relevance scores (0-5)
            k: Number of recommendations to consider
            
        Returns:
            NDCG@K score
        """
        if k <= 0 or not recommended_ids:
            return 0.0
        
        k = min(k, len(recommended_ids))
        
        # Calculate DCG
        dcg = 0.0
        for i, item_id in enumerate(recommended_ids[:k]):
            relevance = relevance_scores.get(item_id, 0)
            dcg += (2 ** relevance - 1) / np.log2(i + 2)
        
        # Calculate ideal DCG (perfect ranking)
        ideal_scores = sorted([relevance_scores.get(id, 0) for id in relevance_scores.keys()], reverse=True)
        ideal_dcg = 0.0
        for i, relevance in enumerate(ideal_scores[:k]):
            ideal_dcg += (2 ** relevance - 1) / np.log2(i + 2)
        
        # Avoid division by zero
        if ideal_dcg == 0:
            return 0.0
        
        return dcg / ideal_dcg
    
    def mrr(self, recommended_ids: List[int], relevant_ids: Set[int]) -> float:
        """
        Calculate Mean Reciprocal Rank.
        
        Args:
            recommended_ids: List of recommended internship IDs (ordered by relevance)
            relevant_ids: Set of relevant internship IDs
            
        Returns:
            MRR score
        """
        if not relevant_ids or not recommended_ids:
            return 0.0
        
        for i, item_id in enumerate(recommended_ids):
            if item_id in relevant_ids:
                return 1.0 / (i + 1)
        
        return 0.0
    
    def coverage(self, all_recommended_ids: List[Set[int]], total_catalog_size: int) -> float:
        """
        Calculate catalog coverage.
        
        Args:
            all_recommended_ids: List of sets of recommended IDs for multiple queries
            total_catalog_size: Total number of items in the catalog
            
        Returns:
            Coverage score (0-1)
        """
        if total_catalog_size == 0:
            return 0.0
        
        all_recommended = set()
        for recommended_set in all_recommended_ids:
            all_recommended.update(recommended_set)
        
        return len(all_recommended) / total_catalog_size
    
    def zero_result_rate(self, all_recommended_ids: List[List[int]]) -> float:
        """
        Calculate the rate of queries that returned no results.
        
        Args:
            all_recommended_ids: List of recommended ID lists for multiple queries
            
        Returns:
            Zero result rate (0-1)
        """
        if not all_recommended_ids:
            return 0.0
        
        zero_results = sum(1 for rec_list in all_recommended_ids if not rec_list)
        
        return zero_results / len(all_recommended_ids)
    
    def evaluate_query(
        self,
        recommended_ids: List[int],
        relevant_ids: Set[int],
        relevance_scores: Dict[int, int],
        k_values: List[int] = [5, 10]
    ) -> Dict[str, float]:
        """
        Evaluate a single query across multiple metrics.
        
        Args:
            recommended_ids: List of recommended internship IDs
            relevant_ids: Set of relevant internship IDs
            relevance_scores: Dictionary mapping IDs to relevance scores
            k_values: List of K values for Precision@K and Recall@K
            
        Returns:
            Dictionary of metric scores
        """
        results = {}
        
        for k in k_values:
            results[f"precision@{k}"] = self.precision_at_k(recommended_ids, relevant_ids, k)
            results[f"recall@{k}"] = self.recall_at_k(recommended_ids, relevant_ids, k)
            results[f"ndcg@{k}"] = self.ndcg_at_k(recommended_ids, relevance_scores, k)
        
        results["mrr"] = self.mrr(recommended_ids, relevant_ids)
        
        return results
    
    def evaluate_dataset(
        self,
        recommendations: Dict[str, List[int]],  # query_id -> recommended_ids
        ground_truth: Dict[str, Dict],  # query_id -> {"relevant_ids": List/Set, "relevance_scores": Dict}
        k_values: List[int] = [5, 10],
        total_catalog_size: int = None
    ) -> Dict[str, float]:
        """
        Evaluate multiple queries and aggregate results.
        
        Args:
            recommendations: Dictionary mapping query IDs to recommended IDs
            ground_truth: Dictionary mapping query IDs to ground truth data
            k_values: List of K values for metrics
            total_catalog_size: Total catalog size for coverage calculation
            
        Returns:
            Dictionary of aggregated metric scores
        """
        all_metrics = []
        all_recommended_sets = []
        
        for query_id, recommended_ids in recommendations.items():
            if query_id not in ground_truth:
                continue
            
            gt = ground_truth[query_id]
            relevant_ids = gt.get("relevant_ids", set())
            # Convert to set if it's a list
            if isinstance(relevant_ids, list):
                relevant_ids = set(relevant_ids)
            relevance_scores = gt.get("relevance_scores", {})
            
            metrics = self.evaluate_query(recommended_ids, relevant_ids, relevance_scores, k_values)
            all_metrics.append(metrics)
            all_recommended_sets.append(set(recommended_ids))
        
        if not all_metrics:
            return {}
        
        # Aggregate metrics (average across all queries)
        aggregated = {}
        for key in all_metrics[0].keys():
            values = [m[key] for m in all_metrics]
            aggregated[key] = np.mean(values)
        
        # Add coverage and zero result rate
        if total_catalog_size:
            aggregated["coverage"] = self.coverage(all_recommended_sets, total_catalog_size)
        
        all_recommended_lists = [list(rec_set) for rec_set in all_recommended_sets]
        aggregated["zero_result_rate"] = self.zero_result_rate(all_recommended_lists)
        
        return aggregated


def create_evaluation_report(metrics: Dict[str, float], model_name: str) -> str:
    """
    Create a formatted evaluation report.
    
    Args:
        metrics: Dictionary of metric scores
        model_name: Name of the model being evaluated
        
    Returns:
        Formatted report string
    """
    report = f"\n{'='*50}\n"
    report += f"Evaluation Report: {model_name}\n"
    report += f"{'='*50}\n"
    
    for metric, value in sorted(metrics.items()):
        if isinstance(value, float):
            report += f"{metric:20s}: {value:.4f}\n"
        else:
            report += f"{metric:20s}: {value}\n"
    
    report += f"{'='*50}\n"
    
    return report


def compare_models(model_metrics: Dict[str, Dict[str, float]]) -> pd.DataFrame:
    """
    Compare multiple models and return a comparison DataFrame.
    
    Args:
        model_metrics: Dictionary mapping model names to their metric dictionaries
        
    Returns:
        DataFrame with model comparison
    """
    data = []
    for model_name, metrics in model_metrics.items():
        row = {"Model": model_name}
        row.update(metrics)
        data.append(row)
    
    df = pd.DataFrame(data)
    
    # Reorder columns for better display
    metric_cols = [col for col in df.columns if col != "Model"]
    df = df[["Model"] + sorted(metric_cols)]
    
    return df
