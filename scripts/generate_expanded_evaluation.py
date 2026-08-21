"""
Generate expanded evaluation dataset with 30-50 realistic user queries.
"""

import pandas as pd
import sys
import os
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.preprocessing import normalize_skills


def generate_expanded_evaluation_dataset():
    """Generate expanded evaluation dataset with 30-50 realistic queries."""
    
    # Load the clean internship dataset
    try:
        internships_df = pd.read_csv("data/processed/internships_clean.csv")
        print(f"Loaded {len(internships_df)} internships from clean dataset")
    except FileNotFoundError:
        print("Error: Clean dataset not found. Run generate_clean_dataset.py first.")
        return
    
    # Define realistic user queries covering different domains
    user_queries = [
        # Web Development
        {
            "query_id": "q1",
            "user_skills": "HTML, CSS, JavaScript, React",
            "user_profile": "Frontend developer seeking React roles",
            "domain": "Web Development"
        },
        {
            "query_id": "q2", 
            "user_skills": "JavaScript, Node.js, MongoDB, Express",
            "user_profile": "MERN stack developer",
            "domain": "Web Development"
        },
        {
            "query_id": "q3",
            "user_skills": "Java, Spring Boot, REST API, SQL",
            "user_profile": "Java backend developer",
            "domain": "Web Development"
        },
        {
            "query_id": "q4",
            "user_skills": "Python, Django, Flask, PostgreSQL",
            "user_profile": "Python web developer",
            "domain": "Web Development"
        },
        {
            "query_id": "q5",
            "user_skills": "Angular, TypeScript, JavaScript",
            "user_profile": "Angular frontend developer",
            "domain": "Web Development"
        },
        
        # Machine Learning / Data Science
        {
            "query_id": "q6",
            "user_skills": "Python, Machine Learning, Pandas, NumPy, Scikit-learn",
            "user_profile": "ML engineer seeking data science roles",
            "domain": "Machine Learning"
        },
        {
            "query_id": "q7",
            "user_skills": "Python, TensorFlow, Deep Learning, Neural Networks",
            "user_profile": "Deep learning engineer",
            "domain": "AI"
        },
        {
            "query_id": "q8",
            "user_skills": "Python, NLP, Natural Language Processing, NLTK",
            "user_profile": "NLP engineer",
            "domain": "AI"
        },
        {
            "query_id": "q9",
            "user_skills": "Python, Computer Vision, OpenCV, PyTorch",
            "user_profile": "Computer vision engineer",
            "domain": "AI"
        },
        {
            "query_id": "q10",
            "user_skills": "Python, Pandas, SQL, Data Visualization, Statistics",
            "user_profile": "Data analyst",
            "domain": "Data Analysis"
        },
        {
            "query_id": "q11",
            "user_skills": "Python, R, Statistics, Machine Learning",
            "user_profile": "Data scientist",
            "domain": "Data Science"
        },
        {
            "query_id": "q12",
            "user_skills": "Python, SQL, Excel, Power BI, Tableau",
            "user_profile": "Business intelligence analyst",
            "domain": "Data Analysis"
        },
        
        # Cloud / DevOps
        {
            "query_id": "q13",
            "user_skills": "AWS, Docker, Kubernetes, CI/CD",
            "user_profile": "AWS DevOps engineer",
            "domain": "Cloud"
        },
        {
            "query_id": "q14",
            "user_skills": "Azure, DevOps, Terraform, Ansible",
            "user_profile": "Azure cloud engineer",
            "domain": "Cloud"
        },
        {
            "query_id": "q15",
            "user_skills": "GCP, Kubernetes, Helm, Linux",
            "user_profile": "GCP cloud engineer",
            "domain": "Cloud"
        },
        {
            "query_id": "q16",
            "user_skills": "Linux, Bash, Jenkins, Git, CI/CD",
            "user_profile": "DevOps engineer",
            "domain": "DevOps"
        },
        {
            "query_id": "q17",
            "user_skills": "Docker, Kubernetes, Prometheus, Grafana",
            "user_profile": "Container orchestration engineer",
            "domain": "DevOps"
        },
        
        # Cybersecurity
        {
            "query_id": "q18",
            "user_skills": "Cybersecurity, Network Security, Firewalls, Linux",
            "user_profile": "Cybersecurity analyst",
            "domain": "Cybersecurity"
        },
        {
            "query_id": "q19",
            "user_skills": "Penetration Testing, Ethical Hacking, Python",
            "user_profile": "Penetration tester",
            "domain": "Cybersecurity"
        },
        {
            "query_id": "q20",
            "user_skills": "SIEM, Security Operations, Linux, Python",
            "user_profile": "SOC analyst",
            "domain": "Cybersecurity"
        },
        
        # Mobile Development
        {
            "query_id": "q21",
            "user_skills": "Android, Kotlin, Java, Firebase",
            "user_profile": "Android developer",
            "domain": "Mobile Development"
        },
        {
            "query_id": "q22",
            "user_skills": "iOS, Swift, Swift UI, Objective-C",
            "user_profile": "iOS developer",
            "domain": "Mobile Development"
        },
        {
            "query_id": "q23",
            "user_skills": "Flutter, Dart, Mobile Development, Firebase",
            "user_profile": "Flutter developer",
            "domain": "Mobile Development"
        },
        {
            "query_id": "q24",
            "user_skills": "React Native, JavaScript, Mobile Development",
            "user_profile": "React Native developer",
            "domain": "Mobile Development"
        },
        
        # IoT / Embedded Systems
        {
            "query_id": "q25",
            "user_skills": "Arduino, C++, Embedded Systems, Sensors",
            "user_profile": "Embedded systems engineer",
            "domain": "IoT"
        },
        {
            "query_id": "q26",
            "user_skills": "Raspberry Pi, Python, IoT, MQTT",
            "user_profile": "IoT developer",
            "domain": "IoT"
        },
        
        # Database
        {
            "query_id": "q27",
            "user_skills": "SQL, PostgreSQL, MySQL, Database Administration",
            "user_profile": "Database administrator",
            "domain": "Database"
        },
        {
            "query_id": "q28",
            "user_skills": "MongoDB, NoSQL, Database, JavaScript",
            "user_profile": "NoSQL database engineer",
            "domain": "Database"
        },
        
        # Backend
        {
            "query_id": "q29",
            "user_skills": "Python, Django, REST API, PostgreSQL",
            "user_profile": "Python backend developer",
            "domain": "Backend"
        },
        {
            "query_id": "q30",
            "user_skills": "Node.js, Express, MongoDB, JavaScript",
            "user_profile": "Node.js backend developer",
            "domain": "Backend"
        },
        
        # Mixed skill queries
        {
            "query_id": "q31",
            "user_skills": "Python, Machine Learning, SQL, Django",
            "user_profile": "Full stack ML engineer",
            "domain": "Mixed"
        },
        {
            "query_id": "q32",
            "user_skills": "JavaScript, React, Node.js, MongoDB",
            "user_profile": "MERN full stack developer",
            "domain": "Mixed"
        },
        {
            "query_id": "q33",
            "user_skills": "Java, Spring Boot, AWS, Docker",
            "user_profile": "Java cloud developer",
            "domain": "Mixed"
        },
        {
            "query_id": "q34",
            "user_skills": "Python, AWS, Lambda, Serverless",
            "user_profile": "Serverless engineer",
            "domain": "Mixed"
        },
        {
            "query_id": "q35",
            "user_skills": "Android, Kotlin, Firebase, Machine Learning",
            "user_profile": "Android ML engineer",
            "domain": "Mixed"
        },
    ]
    
    print(f"Created {len(user_queries)} user queries")
    
    # For each query, find relevant internships and assign relevance scores
    evaluation_records = []
    ground_truth = {}
    
    for query in user_queries:
        normalized_skills = normalize_skills(query["user_skills"])
        user_skills_list = [s.strip().lower() for s in normalized_skills.split(",")]
        
        relevant_internships = []
        relevance_scores = {}
        
        # Find internships in the same or related domain
        domain_filter = query["domain"]
        if domain_filter == "Mixed":
            # For mixed queries, consider all domains
            candidate_internships = internships_df
        else:
            # Map domain names to dataset domains
            domain_mapping = {
                "Web Development": ["Web Development"],
                "Machine Learning": ["Machine Learning", "Data Science", "AI"],
                "AI": ["AI", "Machine Learning"],
                "Data Analysis": ["Data Analysis", "Data Science"],
                "Data Science": ["Data Science", "Data Analysis", "Machine Learning"],
                "Cloud": ["Cloud", "DevOps"],
                "DevOps": ["DevOps", "Cloud"],
                "Cybersecurity": ["Cybersecurity"],
                "Mobile Development": ["Mobile Development"],
                "IoT": ["IoT", "Embedded Systems"],
                "Database": ["Web Development", "Backend"],  # Database roles often in backend
                "Backend": ["Web Development", "Backend"],
            }
            
            related_domains = domain_mapping.get(domain_filter, [domain_filter])
            candidate_internships = internships_df[internships_df["Domain"].isin(related_domains)]
        
        # Calculate skill overlap for each candidate internship
        for _, internship in candidate_internships.iterrows():
            internship_skills = [s.strip().lower() for s in str(internship["Skills"]).split(",")]
            
            # Calculate skill overlap
            matching_skills = sum(1 for skill in user_skills_list if skill in internship_skills)
            skill_overlap_ratio = matching_skills / len(user_skills_list) if user_skills_list else 0
            
            # Assign relevance score based on skill overlap
            if skill_overlap_ratio >= 0.6:
                relevance = 5  # Perfect match
            elif skill_overlap_ratio >= 0.4:
                relevance = 4  # Excellent match
            elif skill_overlap_ratio >= 0.3:
                relevance = 3  # Highly relevant
            elif skill_overlap_ratio >= 0.2:
                relevance = 2  # Relevant
            elif skill_overlap_ratio >= 0.1:
                relevance = 1  # Slightly relevant
            else:
                relevance = 0  # Not relevant
            
            # Only include internships with some relevance
            if relevance >= 2:
                relevant_internships.append({
                    "internship_id": internship["Internship_ID"],
                    "title": internship["Title"],
                    "relevance": relevance,
                    "reason": f"Skill overlap: {skill_overlap_ratio:.2f}"
                })
                relevance_scores[internship["Internship_ID"]] = relevance
        
        # Sort by relevance and take top 5-10 per query
        relevant_internships.sort(key=lambda x: x["relevance"], reverse=True)
        relevant_internships = relevant_internships[:8]  # Top 8 per query
        
        # Add to evaluation records
        for eval_item in relevant_internships:
            record = {
                "query_id": query["query_id"],
                "user_skills": normalized_skills,
                "user_profile": query["user_profile"],
                "domain": query["domain"],
                "internship_id": eval_item["internship_id"],
                "internship_title": eval_item["title"],
                "relevance_score": eval_item["relevance"],
                "relevance_reason": eval_item["reason"]
            }
            evaluation_records.append(record)
        
        # Add to ground truth
        relevant_ids = [item["internship_id"] for item in relevant_internships]
        ground_truth[query["query_id"]] = {
            "user_skills": normalized_skills,
            "relevant_ids": relevant_ids,
            "relevance_scores": relevance_scores
        }
    
    # Create DataFrame
    eval_df = pd.DataFrame(evaluation_records)
    
    # Save evaluation dataset
    output_path = "data/evaluation/evaluation_dataset_expanded.csv"
    eval_df.to_csv(output_path, index=False)
    print(f"\nExpanded evaluation dataset saved to: {output_path}")
    
    # Print statistics
    print("\n=== Expanded Evaluation Dataset Statistics ===")
    print(f"Total queries: {len(user_queries)}")
    print(f"Total evaluations: {len(eval_df)}")
    print(f"\nRelevance score distribution:")
    print(eval_df["relevance_score"].value_counts().sort_index())
    print(f"\nDomain distribution:")
    print(eval_df["domain"].value_counts())
    
    # Save ground truth as JSON
    gt_path = "data/evaluation/ground_truth_expanded.json"
    with open(gt_path, 'w') as f:
        json.dump(ground_truth, f, indent=2)
    print(f"\nExpanded ground truth saved to: {gt_path}")
    
    # Display sample
    print("\n=== Sample Evaluation Records ===")
    print(eval_df.head(15).to_string())
    
    return eval_df, ground_truth


if __name__ == "__main__":
    generate_expanded_evaluation_dataset()
