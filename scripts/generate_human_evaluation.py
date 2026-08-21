"""
Generate human-curated evaluation dataset with manual relevance labels.
"""

import pandas as pd
import sys
import os
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.preprocessing import normalize_skills


def generate_human_curated_evaluation():
    """Generate human-curated evaluation dataset with manual relevance labels."""
    
    # Load the clean internship dataset
    try:
        internships_df = pd.read_csv("data/processed/internships_clean.csv")
        print(f"Loaded {len(internships_df)} internships from clean dataset")
    except FileNotFoundError:
        print("Error: Clean dataset not found. Run generate_clean_dataset.py first.")
        return
    
    # Human-curated evaluation queries with manual relevance labels
    # Relevance scores: 0=Not Relevant, 1=Slightly, 2=Relevant, 3=Highly, 4=Excellent, 5=Perfect
    HUMAN_EVALUATION_DATA = [
        {
            "query_id": "hq1",
            "user_skills": "Python, Machine Learning, Pandas, SQL",
            "user_profile": "Data Science student looking for ML internships",
            "evaluations": [
                {"internship_id": 3, "title": "Machine Learning Intern", "relevance": 5, "reason": "Perfect ML match with Python, ML, Pandas, SQL"},
                {"internship_id": 7, "title": "Data Analyst Intern", "relevance": 4, "reason": "Strong Python and Pandas match"},
                {"internship_id": 8, "title": "Data Analyst Intern", "relevance": 4, "reason": "Strong data analysis match"},
                {"internship_id": 15, "title": "Data Analyst Intern", "relevance": 3, "reason": "Good Python and SQL match"},
                {"internship_id": 1, "title": "Web Developer Intern", "relevance": 0, "reason": "No relevant skills"},
                {"internship_id": 2, "title": "Backend Developer Intern", "relevance": 0, "reason": "No relevant skills"},
            ]
        },
        {
            "query_id": "hq2",
            "user_skills": "HTML, CSS, JavaScript, React",
            "user_profile": "Frontend developer seeking React roles",
            "evaluations": [
                {"internship_id": 1, "title": "Web Developer Intern", "relevance": 4, "reason": "Strong web dev match"},
                {"internship_id": 67, "title": "Full Stack Developer Intern", "relevance": 5, "reason": "Perfect React match"},
                {"internship_id": 98, "title": "Frontend Developer Intern", "relevance": 5, "reason": "Perfect frontend match"},
                {"internship_id": 51, "title": "Frontend Developer Intern", "relevance": 4, "reason": "Strong frontend match"},
                {"internship_id": 3, "title": "Machine Learning Intern", "relevance": 0, "reason": "No relevant skills"},
                {"internship_id": 4, "title": "Security Analyst Intern", "relevance": 0, "reason": "No relevant skills"},
            ]
        },
        {
            "query_id": "hq3",
            "user_skills": "AWS, Docker, Kubernetes, Linux",
            "user_profile": "DevOps engineer looking for cloud roles",
            "evaluations": [
                {"internship_id": 5, "title": "DevOps Intern", "relevance": 5, "reason": "Perfect DevOps match"},
                {"internship_id": 6, "title": "Cloud Computing Intern", "relevance": 4, "reason": "Strong cloud match"},
                {"internship_id": 16, "title": "IoT Engineer Intern", "relevance": 2, "reason": "Some Linux overlap"},
                {"internship_id": 1, "title": "Web Developer Intern", "relevance": 0, "reason": "No relevant skills"},
                {"internship_id": 7, "title": "Data Analyst Intern", "relevance": 0, "reason": "No relevant skills"},
            ]
        },
        {
            "query_id": "hq4",
            "user_skills": "Android, Kotlin, Firebase",
            "user_profile": "Mobile developer seeking Android roles",
            "evaluations": [
                {"internship_id": 9, "title": "Android Developer Intern", "relevance": 5, "reason": "Perfect Android match"},
                {"internship_id": 12, "title": "iOS Developer Intern", "relevance": 1, "reason": "Mobile but wrong platform"},
                {"internship_id": 23, "title": "Flutter Developer Intern", "relevance": 3, "reason": "Mobile development overlap"},
                {"internship_id": 1, "title": "Web Developer Intern", "relevance": 0, "reason": "No relevant skills"},
                {"internship_id": 5, "title": "DevOps Intern", "relevance": 0, "reason": "No relevant skills"},
            ]
        },
        {
            "query_id": "hq5",
            "user_skills": "Cybersecurity, Linux, Networking",
            "user_profile": "Security enthusiast seeking cybersecurity roles",
            "evaluations": [
                {"internship_id": 4, "title": "Security Analyst Intern", "relevance": 5, "reason": "Perfect security match"},
                {"internship_id": 44, "title": "Network Security Intern", "relevance": 4, "reason": "Strong network security match"},
                {"internship_id": 5, "title": "DevOps Intern", "relevance": 2, "reason": "Some Linux overlap"},
                {"internship_id": 1, "title": "Web Developer Intern", "relevance": 0, "reason": "No relevant skills"},
                {"internship_id": 7, "title": "Data Analyst Intern", "relevance": 0, "reason": "No relevant skills"},
            ]
        },
        {
            "query_id": "hq6",
            "user_skills": "Python, Django, REST API, PostgreSQL",
            "user_profile": "Python backend developer",
            "evaluations": [
                {"internship_id": 56, "title": "Backend Developer Intern", "relevance": 5, "reason": "Perfect Python backend match"},
                {"internship_id": 60, "title": "Backend Developer Intern", "relevance": 4, "reason": "Strong backend match"},
                {"internship_id": 133, "title": "Backend Developer Intern", "relevance": 4, "reason": "Strong backend match"},
                {"internship_id": 1, "title": "Web Developer Intern", "relevance": 2, "reason": "Some web overlap"},
                {"internship_id": 3, "title": "Machine Learning Intern", "relevance": 1, "reason": "Python overlap but wrong domain"},
            ]
        },
        {
            "query_id": "hq7",
            "user_skills": "JavaScript, Node.js, MongoDB, Express",
            "user_profile": "MERN stack developer",
            "evaluations": [
                {"internship_id": 189, "title": "Full Stack Developer Intern", "relevance": 5, "reason": "Perfect MERN match"},
                {"internship_id": 28, "title": "Frontend Developer Intern", "relevance": 3, "reason": "JavaScript and Node.js overlap"},
                {"internship_id": 135, "title": "Frontend Developer Intern", "relevance": 3, "reason": "JavaScript overlap"},
                {"internship_id": 1, "title": "Web Developer Intern", "relevance": 2, "reason": "Some web tech overlap"},
                {"internship_id": 3, "title": "Machine Learning Intern", "relevance": 0, "reason": "No relevant skills"},
            ]
        },
        {
            "query_id": "hq8",
            "user_skills": "Java, Spring Boot, SQL",
            "user_profile": "Java backend developer",
            "evaluations": [
                {"internship_id": 9, "title": "Android Developer Intern", "relevance": 3, "reason": "Java overlap"},
                {"internship_id": 13, "title": "Embedded Systems Intern", "relevance": 2, "reason": "Some Java overlap"},
                {"internship_id": 1, "title": "Web Developer Intern", "relevance": 2, "reason": "Some web overlap"},
                {"internship_id": 3, "title": "Machine Learning Intern", "relevance": 0, "reason": "No relevant skills"},
                {"internship_id": 7, "title": "Data Analyst Intern", "relevance": 0, "reason": "No relevant skills"},
            ]
        },
    ]
    
    print(f"Created {len(HUMAN_EVALUATION_DATA)} human-curated evaluation queries")
    
    # Create evaluation records
    evaluation_records = []
    ground_truth = {}
    
    for query in HUMAN_EVALUATION_DATA:
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
        
        # Add to ground truth
        relevant_ids = [item["internship_id"] for item in query["evaluations"]]
        relevance_scores = {item["internship_id"]: item["relevance"] for item in query["evaluations"]}
        
        ground_truth[query["query_id"]] = {
            "user_skills": normalized_skills,
            "relevant_ids": relevant_ids,
            "relevance_scores": relevance_scores
        }
    
    # Create DataFrame
    eval_df = pd.DataFrame(evaluation_records)
    
    # Save evaluation dataset
    output_path = "data/evaluation/evaluation_dataset_human.csv"
    eval_df.to_csv(output_path, index=False)
    print(f"\nHuman-curated evaluation dataset saved to: {output_path}")
    
    # Print statistics
    print("\n=== Human-Curated Evaluation Dataset Statistics ===")
    print(f"Total queries: {len(HUMAN_EVALUATION_DATA)}")
    print(f"Total evaluations: {len(eval_df)}")
    print(f"\nRelevance score distribution:")
    print(eval_df["relevance_score"].value_counts().sort_index())
    
    # Save ground truth as JSON
    gt_path = "data/evaluation/ground_truth_human.json"
    with open(gt_path, 'w') as f:
        json.dump(ground_truth, f, indent=2)
    print(f"\nHuman-curated ground truth saved to: {gt_path}")
    
    # Display sample
    print("\n=== Sample Human-Curated Evaluation Records ===")
    print(eval_df.head(10).to_string())
    
    return eval_df, ground_truth


if __name__ == "__main__":
    generate_human_curated_evaluation()
