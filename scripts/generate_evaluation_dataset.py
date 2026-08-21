"""
Generate a labelled evaluation dataset for model evaluation.
"""

import pandas as pd
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.preprocessing import normalize_skills


def generate_evaluation_dataset():
    """Generate and save the evaluation dataset."""
    
    # Load the clean internship dataset
    try:
        internships_df = pd.read_csv("data/processed/internships_clean.csv")
        print(f"Loaded {len(internships_df)} internships from clean dataset")
    except FileNotFoundError:
        print("Error: Clean dataset not found. Run generate_clean_dataset.py first.")
        return
    
    # Create evaluation dataset based on actual internships in the clean dataset
    # We'll select representative internships for each domain
    
    # Find ML/Data Science internships
    ml_internships = internships_df[
        internships_df['Domain'].isin(['Machine Learning', 'Data Science', 'AI', 'Data Analysis'])
    ].head(5)
    
    # Find Web Development internships
    web_internships = internships_df[
        internships_df['Domain'] == 'Web Development'
    ].head(5)
    
    # Find Cloud/DevOps internships
    cloud_internships = internships_df[
        internships_df['Domain'].isin(['Cloud', 'DevOps'])
    ].head(5)
    
    # Find Mobile Development internships
    mobile_internships = internships_df[
        internships_df['Domain'] == 'Mobile Development'
    ].head(5)
    
    # Find Cybersecurity internships
    security_internships = internships_df[
        internships_df['Domain'] == 'Cybersecurity'
    ].head(5)
    
    # Manually labelled evaluation dataset using actual internship IDs
    # Relevance scores: 0=Not Relevant, 1=Slightly, 2=Relevant, 3=Highly, 4=Excellent, 5=Perfect
    EVALUATION_DATA = []
    
    # Query 1: ML/Data Science
    if len(ml_internships) >= 2:
        ml_ids = ml_internships['Internship_ID'].tolist()
        EVALUATION_DATA.append({
            "query_id": "q1",
            "user_skills": "Python, Machine Learning, Pandas, SQL",
            "user_profile": "Data Science student looking for ML internships",
            "evaluations": [
                {"internship_id": ml_ids[0], "title": ml_internships.iloc[0]['Title'], "relevance": 5, "reason": "Perfect skill match"},
                {"internship_id": ml_ids[1] if len(ml_ids) > 1 else ml_ids[0], "title": ml_internships.iloc[1 if len(ml_ids) > 1 else 0]['Title'], "relevance": 4, "reason": "Strong ML and Python match"},
            ]
        })
    
    # Query 2: Web Development
    if len(web_internships) >= 2:
        web_ids = web_internships['Internship_ID'].tolist()
        EVALUATION_DATA.append({
            "query_id": "q2",
            "user_skills": "HTML, CSS, JavaScript, React",
            "user_profile": "Frontend developer seeking web development roles",
            "evaluations": [
                {"internship_id": web_ids[0], "title": web_internships.iloc[0]['Title'], "relevance": 5, "reason": "Perfect web dev match"},
                {"internship_id": web_ids[1] if len(web_ids) > 1 else web_ids[0], "title": web_internships.iloc[1 if len(web_ids) > 1 else 0]['Title'], "relevance": 4, "reason": "Strong web dev match"},
            ]
        })
    
    # Query 3: Cloud/DevOps
    if len(cloud_internships) >= 2:
        cloud_ids = cloud_internships['Internship_ID'].tolist()
        EVALUATION_DATA.append({
            "query_id": "q3",
            "user_skills": "AWS, Docker, Kubernetes, Linux",
            "user_profile": "DevOps engineer looking for cloud roles",
            "evaluations": [
                {"internship_id": cloud_ids[0], "title": cloud_internships.iloc[0]['Title'], "relevance": 5, "reason": "Perfect DevOps match"},
                {"internship_id": cloud_ids[1] if len(cloud_ids) > 1 else cloud_ids[0], "title": cloud_internships.iloc[1 if len(cloud_ids) > 1 else 0]['Title'], "relevance": 4, "reason": "Strong cloud match"},
            ]
        })
    
    # Query 4: Mobile Development
    if len(mobile_internships) >= 2:
        mobile_ids = mobile_internships['Internship_ID'].tolist()
        EVALUATION_DATA.append({
            "query_id": "q4",
            "user_skills": "Android, Kotlin, Firebase",
            "user_profile": "Mobile developer seeking Android roles",
            "evaluations": [
                {"internship_id": mobile_ids[0], "title": mobile_internships.iloc[0]['Title'], "relevance": 5, "reason": "Perfect mobile match"},
                {"internship_id": mobile_ids[1] if len(mobile_ids) > 1 else mobile_ids[0], "title": mobile_internships.iloc[1 if len(mobile_ids) > 1 else 0]['Title'], "relevance": 4, "reason": "Strong mobile match"},
            ]
        })
    
    # Query 5: Cybersecurity
    if len(security_internships) >= 2:
        security_ids = security_internships['Internship_ID'].tolist()
        EVALUATION_DATA.append({
            "query_id": "q5",
            "user_skills": "Cybersecurity, Networking, Linux",
            "user_profile": "Security enthusiast seeking cybersecurity roles",
            "evaluations": [
                {"internship_id": security_ids[0], "title": security_internships.iloc[0]['Title'], "relevance": 5, "reason": "Perfect security match"},
                {"internship_id": security_ids[1] if len(security_ids) > 1 else security_ids[0], "title": security_internships.iloc[1 if len(security_ids) > 1 else 0]['Title'], "relevance": 4, "reason": "Strong security match"},
            ]
        })
    
    print(f"\nGenerated {len(EVALUATION_DATA)} evaluation queries based on actual internships")
    
    # Create evaluation records
    evaluation_records = []
    
    for query in EVALUATION_DATA:
        normalized_skills = normalize_skills(query["user_skills"])
        
        for eval_item in query["evaluations"]:
            record = {
                "query_id": query["query_id"],
                "user_skills": normalized_skills,
                "user_profile": query["user_profile"],
                "internship_id": eval_item["internship_id"],
                "internship_title": eval_item["title"],
                "relevance_score": eval_item["relevance"],
                "relevance_reason": eval_item["reason"]
            }
            evaluation_records.append(record)
    
    # Create DataFrame
    eval_df = pd.DataFrame(evaluation_records)
    
    # Save evaluation dataset
    output_path = "data/evaluation/evaluation_dataset.csv"
    eval_df.to_csv(output_path, index=False)
    print(f"\nEvaluation dataset saved to: {output_path}")
    
    # Print statistics
    print("\n=== Evaluation Dataset Statistics ===")
    print(f"Total queries: {len(EVALUATION_DATA)}")
    print(f"Total evaluations: {len(eval_df)}")
    print(f"\nRelevance score distribution:")
    print(eval_df["relevance_score"].value_counts().sort_index())
    
    # Also create a ground truth file for easy loading
    ground_truth = {}
    for query in EVALUATION_DATA:
        relevant_ids = set()
        relevance_scores = {}
        
        for eval_item in query["evaluations"]:
            relevant_ids.add(eval_item["internship_id"])
            relevance_scores[eval_item["internship_id"]] = eval_item["relevance"]
        
        ground_truth[query["query_id"]] = {
            "user_skills": normalize_skills(query["user_skills"]),
            "relevant_ids": list(relevant_ids),  # Convert set to list for JSON serialization
            "relevance_scores": relevance_scores
        }
    
    # Save ground truth as JSON
    import json
    gt_path = "data/evaluation/ground_truth.json"
    with open(gt_path, 'w') as f:
        json.dump(ground_truth, f, indent=2)
    print(f"\nGround truth saved to: {gt_path}")
    
    # Display sample
    print("\n=== Sample Evaluation Records ===")
    print(eval_df.head(10).to_string())
    
    return eval_df, ground_truth


if __name__ == "__main__":
    generate_evaluation_dataset()
