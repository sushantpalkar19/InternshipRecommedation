"""
Final comprehensive evaluation with validation and hybrid model testing.
"""

import sys
import os
import pandas as pd
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.evaluation import RecommendationEvaluator, create_evaluation_report, compare_models
from src.config import Config
from src.recommender import get_hybrid_recommender


def load_ground_truth(dataset_type: str = "human"):
    """Load ground truth from JSON file."""
    if dataset_type == "human":
        path = "data/evaluation/ground_truth_human.json"
    elif dataset_type == "expanded":
        path = "data/evaluation/ground_truth_expanded.json"
    else:
        path = "data/evaluation/ground_truth.json"
    
    with open(path, 'r') as f:
        ground_truth = json.load(f)
    
    # Convert lists back to sets and fix relevance_scores keys
    for query_id in ground_truth:
        ground_truth[query_id]["relevant_ids"] = set(ground_truth[query_id]["relevant_ids"])
        
        # Convert string keys to integers in relevance_scores
        relevance_scores = ground_truth[query_id]["relevance_scores"]
        fixed_scores = {}
        for key, value in relevance_scores.items():
            fixed_scores[int(key)] = value
        ground_truth[query_id]["relevance_scores"] = fixed_scores
    
    return ground_truth


def load_internship_data():
    """Load the clean internship dataset."""
    df = pd.read_csv("data/processed/internships_clean.csv")
    return df


def validate_evaluation_data(ground_truth: dict, df: pd.DataFrame):
    """Validate evaluation data before running evaluation."""
    print("\n=== Evaluation Data Validation ===")
    
    # Check number of queries
    num_queries = len(ground_truth)
    print(f"Number of queries: {num_queries}")
    if num_queries == 0:
        raise ValueError("No evaluation queries found")
    
    # Check number of ground truth records
    num_records = sum(len(gt["relevance_scores"]) for gt in ground_truth.values())
    print(f"Number of ground truth records: {num_records}")
    if num_records == 0:
        raise ValueError("No ground truth records found")
    
    # Check relevance values are valid
    for query_id, gt in ground_truth.items():
        for internship_id, relevance in gt["relevance_scores"].items():
            if not isinstance(relevance, (int, float)):
                raise ValueError(f"Invalid relevance type for query {query_id}, internship {internship_id}")
            if relevance < 0 or relevance > 5:
                raise ValueError(f"Invalid relevance value {relevance} for query {query_id}, internship {internship_id}")
    
    print("✓ Relevance values are valid (0-5 scale)")
    
    # Check internship IDs exist
    all_ids = set(df["Internship_ID"].tolist())
    for query_id, gt in ground_truth.items():
        for internship_id in gt["relevant_ids"]:
            if internship_id not in all_ids:
                print(f"⚠ Warning: Internship ID {internship_id} not found in dataset (query {query_id})")
    
    print("✓ Internship ID validation complete")
    print("✓ Evaluation data validation passed")


def evaluate_model(model_name: str, model_function, ground_truth: dict, df: pd.DataFrame, top_k: int = 10):
    """
    Evaluate a single model.
    
    Args:
        model_name: Name of the model
        model_function: Function that takes user_skills and returns recommendations
        ground_truth: Ground truth dictionary
        df: Internship dataframe
        top_k: Number of recommendations to generate
        
    Returns:
        Dictionary of evaluation metrics
    """
    print(f"\nEvaluating {model_name}...")
    
    recommendations = {}
    failed_queries = []
    
    for query_id, gt_data in ground_truth.items():
        user_skills = gt_data["user_skills"]
        
        try:
            # Get recommendations from the model
            results = model_function(user_skills, top_n=top_k)
            
            # Extract internship IDs
            if "Internship_ID" in results.columns:
                recommended_ids = results["Internship_ID"].tolist()
            else:
                # If no Internship_ID column, use index
                recommended_ids = results.index.tolist()
            
            recommendations[query_id] = recommended_ids
            
        except Exception as e:
            print(f"Error processing query {query_id}: {e}")
            recommendations[query_id] = []
            failed_queries.append(query_id)
    
    if failed_queries:
        print(f"Failed queries for {model_name}: {failed_queries}")
    
    # Evaluate
    config = Config()
    evaluator = RecommendationEvaluator(relevance_threshold=config.EVALUATION["relevance_threshold"])
    metrics = evaluator.evaluate_dataset(
        recommendations=recommendations,
        ground_truth=ground_truth,
        k_values=config.EVALUATION["k_values"],
        total_catalog_size=len(df)
    )
    
    return metrics


def evaluate_hybrid_model(ground_truth: dict, df: pd.DataFrame, top_k: int = 10):
    """Evaluate the hybrid recommender."""
    print(f"\nEvaluating Hybrid Model...")
    
    try:
        recommender = get_hybrid_recommender()
    except Exception as e:
        print(f"Error loading hybrid recommender: {e}")
        return None
    
    recommendations = {}
    failed_queries = []
    
    for query_id, gt_data in ground_truth.items():
        user_skills = gt_data["user_skills"]
        
        try:
            # Get recommendations from hybrid recommender
            results = recommender.recommend(
                user_skills,
                model_name=None,  # Auto-select best model
                top_n=top_k,
                apply_ranking=True
            )
            
            # Extract internship IDs
            if "Internship_ID" in results.columns:
                recommended_ids = results["Internship_ID"].tolist()
            else:
                recommended_ids = results.index.tolist()
            
            recommendations[query_id] = recommended_ids
            
        except Exception as e:
            print(f"Error processing query {query_id}: {e}")
            recommendations[query_id] = []
            failed_queries.append(query_id)
    
    if failed_queries:
        print(f"Failed queries for Hybrid: {failed_queries}")
    
    # Evaluate
    config = Config()
    evaluator = RecommendationEvaluator(relevance_threshold=config.EVALUATION["relevance_threshold"])
    metrics = evaluator.evaluate_dataset(
        recommendations=recommendations,
        ground_truth=ground_truth,
        k_values=config.EVALUATION["k_values"],
        total_catalog_size=len(df)
    )
    
    return metrics


def main():
    """Main evaluation function."""
    print("="*60)
    print("Internship Recommendation System - Final Evaluation")
    print("="*60)
    
    # Use human-curated dataset for final evaluation
    dataset_type = "human"
    print(f"\nUsing {dataset_type}-curated evaluation dataset")
    
    # Load data
    print("\nLoading data...")
    ground_truth = load_ground_truth(dataset_type)
    df = load_internship_data()
    
    # Validate evaluation data
    try:
        validate_evaluation_data(ground_truth, df)
    except ValueError as e:
        print(f"❌ Validation failed: {e}")
        return
    
    print(f"Loaded {len(ground_truth)} evaluation queries")
    print(f"Loaded {len(df)} internships")
    
    # Import models
    print("\nLoading models...")
    try:
        from models.model_tfidf import recommend_tfidf
        from models.model_countvec import recommend_countvec
        from models.model_word2vec import recommend_word2vec
        print("Base models loaded successfully")
    except ImportError as e:
        print(f"Error importing models: {e}")
        return
    
    # Try to load semantic model
    semantic_available = False
    try:
        from src.models.semantic_model import recommend_semantic
        semantic_available = True
        print("Semantic model loaded successfully")
    except ImportError:
        print("Semantic model not available (sentence-transformers not installed)")
    except Exception as e:
        print(f"Error loading semantic model: {e}")
    
    # Evaluate each model
    model_metrics = {}
    
    # TF-IDF
    try:
        tfidf_metrics = evaluate_model("TF-IDF", recommend_tfidf, ground_truth, df)
        model_metrics["TF-IDF"] = tfidf_metrics
        print(create_evaluation_report(tfidf_metrics, "TF-IDF"))
    except Exception as e:
        print(f"Error evaluating TF-IDF: {e}")
    
    # CountVectorizer
    try:
        countvec_metrics = evaluate_model("CountVectorizer", recommend_countvec, ground_truth, df)
        model_metrics["CountVectorizer"] = countvec_metrics
        print(create_evaluation_report(countvec_metrics, "CountVectorizer"))
    except Exception as e:
        print(f"Error evaluating CountVectorizer: {e}")
    
    # Word2Vec
    try:
        w2v_metrics = evaluate_model("Word2Vec", recommend_word2vec, ground_truth, df)
        model_metrics["Word2Vec"] = w2v_metrics
        print(create_evaluation_report(w2v_metrics, "Word2Vec"))
    except Exception as e:
        print(f"Error evaluating Word2Vec: {e}")
    
    # Semantic Model (only if available)
    if semantic_available:
        try:
            semantic_metrics = evaluate_model("Semantic", recommend_semantic, ground_truth, df)
            # Check if semantic model actually produced results
            if semantic_metrics["zero_result_rate"] < 1.0:
                model_metrics["Semantic"] = semantic_metrics
                print(create_evaluation_report(semantic_metrics, "Semantic"))
            else:
                print("⚠ Semantic model produced no results, excluding from comparison")
        except Exception as e:
            print(f"Error evaluating Semantic: {e}")
    
    # Hybrid Model
    try:
        hybrid_metrics = evaluate_hybrid_model(ground_truth, df)
        if hybrid_metrics:
            model_metrics["Hybrid"] = hybrid_metrics
            print(create_evaluation_report(hybrid_metrics, "Hybrid"))
    except Exception as e:
        print(f"Error evaluating Hybrid: {e}")
    
    # Compare models
    if model_metrics:
        print("\n" + "="*60)
        print("MODEL COMPARISON")
        print("="*60)
        comparison_df = compare_models(model_metrics)
        print(comparison_df.to_string(index=False))
        
        # Save comparison
        config = Config()
        comparison_path = f"data/evaluation/model_comparison_{dataset_type}.csv"
        comparison_df.to_csv(comparison_path, index=False)
        print(f"\nModel comparison saved to: {comparison_path}")
        
        # Select best model
        selection_config = config.get_model_selection_config()
        primary_metric = selection_config["primary_metric"]
        
        # Filter out models with zero results
        valid_models = comparison_df[comparison_df["zero_result_rate"] < 1.0]
        
        if not valid_models.empty:
            best_model = valid_models.loc[valid_models[primary_metric].idxmax(), "Model"]
            best_score = valid_models.loc[valid_models[primary_metric].idxmax(), primary_metric]
            print(f"\n🏆 Best model based on {primary_metric}: {best_model} ({best_score:.4f})")
            
            # Show secondary metrics for best model
            print(f"\nSecondary metrics for {best_model}:")
            for metric in selection_config["secondary_metrics"]:
                if metric in valid_models.columns:
                    score = valid_models.loc[valid_models["Model"] == best_model, metric].values[0]
                    print(f"  {metric}: {score:.4f}")
        else:
            print("\n⚠ No valid models found (all have zero results)")
    
    print("\n" + "="*60)
    print("Evaluation complete!")
    print("="*60)


if __name__ == "__main__":
    main()
