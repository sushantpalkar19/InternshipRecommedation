"""
Evaluate recommendation models using the expanded evaluation dataset.
"""

import sys
import os
import pandas as pd
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.evaluation import RecommendationEvaluator, create_evaluation_report, compare_models
from src.config import Config


def load_ground_truth(use_expanded: bool = True):
    """Load ground truth from JSON file."""
    if use_expanded:
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
    print("Internship Recommendation System - Model Evaluation")
    print("="*60)
    
    # Load data
    print("\nLoading data...")
    use_expanded = True  # Use expanded dataset
    ground_truth = load_ground_truth(use_expanded)
    df = load_internship_data()
    
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
        print("Make sure the models are refactored to use the clean dataset first.")
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
    
    # Semantic Model
    if semantic_available:
        try:
            semantic_metrics = evaluate_model("Semantic", recommend_semantic, ground_truth, df)
            model_metrics["Semantic"] = semantic_metrics
            print(create_evaluation_report(semantic_metrics, "Semantic"))
        except Exception as e:
            print(f"Error evaluating Semantic: {e}")
    
    # Compare models
    if model_metrics:
        print("\n" + "="*60)
        print("MODEL COMPARISON")
        print("="*60)
        comparison_df = compare_models(model_metrics)
        print(comparison_df.to_string(index=False))
        
        # Save comparison
        config = Config()
        comparison_path = config.DATA_PATHS["model_comparison"]
        comparison_df.to_csv(comparison_path, index=False)
        print(f"\nModel comparison saved to: {comparison_path}")
        
        # Find best model based on primary metric
        selection_config = config.get_model_selection_config()
        primary_metric = selection_config["primary_metric"]
        best_model = comparison_df.loc[comparison_df[primary_metric].idxmax(), "Model"]
        best_score = comparison_df.loc[comparison_df[primary_metric].idxmax(), primary_metric]
        print(f"\n🏆 Best model based on {primary_metric}: {best_model} ({best_score:.4f})")
        
        # Show secondary metrics for best model
        print(f"\nSecondary metrics for {best_model}:")
        for metric in selection_config["secondary_metrics"]:
            if metric in comparison_df.columns:
                score = comparison_df.loc[comparison_df["Model"] == best_model, metric].values[0]
                print(f"  {metric}: {score:.4f}")
    
    print("\n" + "="*60)
    print("Evaluation complete!")
    print("="*60)


if __name__ == "__main__":
    main()
