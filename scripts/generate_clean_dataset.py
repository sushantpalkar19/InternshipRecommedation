"""
Generate a clean, realistic internship dataset with proper title-skill mappings.
"""

import pandas as pd
import random
from datetime import datetime, timedelta
from typing import List, Dict, Tuple


# Realistic internship templates with proper skill mappings
INTERNSHIP_TEMPLATES = {
    "Machine Learning": {
        "titles": ["Machine Learning Intern", "AI Research Intern", "Data Science Intern", "ML Engineer Intern"],
        "skills": ["Python", "Machine Learning", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch", "SQL", "Statistics", "Deep Learning"],
        "companies": ["Google", "Microsoft", "Amazon", "Flipkart", "Swiggy", "Zomato", "Uber", "Ola", "Razorpay", "PhonePe"],
        "stipend_range": (15000, 35000),
        "domains": ["Data Science", "Machine Learning", "AI"]
    },
    "Web Development": {
        "titles": ["Web Developer Intern", "Frontend Developer Intern", "Backend Developer Intern", "Full Stack Developer Intern"],
        "skills": ["HTML", "CSS", "JavaScript", "React", "Node.js", "Angular", "Vue", "TypeScript", "MongoDB", "SQL", "REST API"],
        "companies": ["Infosys", "TCS", "Wipro", "HCL", "Tech Mahindra", "Accenture", "Cognizant", "Capgemini"],
        "stipend_range": (10000, 25000),
        "domains": ["Web Development"]
    },
    "Data Analysis": {
        "titles": ["Data Analyst Intern", "Business Analyst Intern", "Analytics Intern"],
        "skills": ["Python", "Pandas", "NumPy", "SQL", "Excel", "Power BI", "Tableau", "Data Visualization", "Statistics"],
        "companies": ["Deloitte", "KPMG", "PwC", "EY", "McKinsey", "BCG", "Bain", "Fractal", "Mu Sigma"],
        "stipend_range": (12000, 28000),
        "domains": ["Data Analysis", "Data Science"]
    },
    "Cloud/DevOps": {
        "titles": ["DevOps Intern", "Cloud Computing Intern", "Site Reliability Engineer Intern"],
        "skills": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Linux", "Bash", "Jenkins", "CI/CD", "Terraform", "Ansible"],
        "companies": ["AWS", "Microsoft", "Google Cloud", "Red Hat", "Canonical", "HashiCorp"],
        "stipend_range": (15000, 30000),
        "domains": ["Cloud", "DevOps"]
    },
    "Mobile Development": {
        "titles": ["Mobile App Developer Intern", "Android Developer Intern", "iOS Developer Intern"],
        "skills": ["Android", "Kotlin", "iOS", "Swift", "Flutter", "React Native", "Firebase", "Java", "Mobile Development"],
        "companies": ["Google", "Apple", "Meta", "Samsung", "OnePlus", "Xiaomi", "Paytm", "PhonePe"],
        "stipend_range": (12000, 28000),
        "domains": ["Mobile Development"]
    },
    "Cybersecurity": {
        "titles": ["Cybersecurity Intern", "Security Analyst Intern", "Network Security Intern"],
        "skills": ["Cybersecurity", "Networking", "Firewalls", "Penetration Testing", "Ethical Hacking", "Linux", "Python", "SIEM"],
        "companies": ["Cisco", "Palo Alto Networks", "Fortinet", "Check Point", "Symantec", "McAfee"],
        "stipend_range": (15000, 32000),
        "domains": ["Cybersecurity"]
    },
    "IoT": {
        "titles": ["IoT Developer Intern", "Embedded Systems Intern", "IoT Engineer Intern"],
        "skills": ["IoT", "Arduino", "Raspberry Pi", "Sensors", "Embedded C", "Python", "C++", "Communication Protocols"],
        "companies": ["Bosch", "Siemens", "Intel", "Texas Instruments", "STMicroelectronics", "NXP"],
        "stipend_range": (10000, 25000),
        "domains": ["IoT", "Embedded Systems"]
    },
    "Digital Marketing": {
        "titles": ["Digital Marketing Intern", "Social Media Intern", "SEO Intern", "Content Marketing Intern"],
        "skills": ["Digital Marketing", "SEO", "Social Media", "Google Analytics", "Content Writing", "Email Marketing", "Facebook Ads"],
        "companies": ["Dentsu", "WPP", "Publicis", "Omnicom", "Interpublic", "HubSpot"],
        "stipend_range": (8000, 20000),
        "domains": ["Digital Marketing"]
    }
}


LOCATIONS = ["Pune", "Mumbai", "Bangalore", "Hyderabad", "Delhi", "Chennai", "Kolkata", "Remote"]
MODES = ["Remote", "Hybrid", "In-Office"]
DURATIONS = ["1 Month", "2 Months", "3 Months", "4 Months", "6 Months"]
EXPERIENCE_LEVELS = ["Entry Level", "Intermediate", "Advanced"]
ELIGIBILITY = ["B.Tech/B.E", "M.Tech/M.E", "BCA/MCA", "BSc/MSc", "Any Graduate"]


def generate_description(title: str, skills: List[str], company: str) -> str:
    """Generate a realistic internship description."""
    skill_str = ", ".join(skills[:4])
    return f"""
    Join {company} as a {title}. You will work on cutting-edge projects using {skill_str}. 
    This internship offers hands-on experience with real-world applications and mentorship from industry experts. 
    Ideal for students passionate about learning and contributing to impactful projects.
    """


def generate_internship_record(internship_id: int) -> Dict:
    """Generate a single realistic internship record."""
    # Randomly select a domain
    domain = random.choice(list(INTERNSHIP_TEMPLATES.keys()))
    template = INTERNSHIP_TEMPLATES[domain]
    
    # Select title, company, and skills
    title = random.choice(template["titles"])
    company = random.choice(template["companies"])
    
    # Select 3-6 relevant skills
    num_skills = random.randint(3, 6)
    skills = random.sample(template["skills"], min(num_skills, len(template["skills"])))
    skills_str = ", ".join(skills)
    
    # Other attributes
    location = random.choice(LOCATIONS)
    mode = random.choice(MODES)
    duration = random.choice(DURATIONS)
    
    stipend_min, stipend_max = template["stipend_range"]
    stipend = random.randint(stipend_min, stipend_max)
    stipend_str = f"₹{stipend:,}/month"
    
    experience_level = random.choice(EXPERIENCE_LEVELS)
    eligibility = random.choice(ELIGIBILITY)
    
    # Dates
    posted_date = datetime.now() - timedelta(days=random.randint(1, 60))
    deadline = posted_date + timedelta(days=random.randint(15, 45))
    status = "Open" if deadline > datetime.now() else "Closed"
    
    # Generate description
    description = generate_description(title, skills, company).strip()
    
    # Generate application URL
    application_url = f"https://example.com/apply/{internship_id}"
    
    return {
        "Internship_ID": internship_id,
        "Title": title,
        "Company": company,
        "Description": description,
        "Skills": skills_str,
        "Location": location,
        "Duration": duration,
        "Stipend": stipend_str,
        "Mode": mode,
        "Domain": random.choice(template["domains"]),
        "Eligibility": eligibility,
        "Experience_Level": experience_level,
        "Application_URL": application_url,
        "Posted_Date": posted_date.strftime("%Y-%m-%d"),
        "Deadline": deadline.strftime("%Y-%m-%d"),
        "Status": status
    }


def generate_dataset(num_records: int = 200) -> pd.DataFrame:
    """Generate a complete internship dataset."""
    print(f"Generating {num_records} realistic internship records...")
    
    records = []
    for i in range(1, num_records + 1):
        record = generate_internship_record(i)
        records.append(record)
        
        if i % 50 == 0:
            print(f"Generated {i} records...")
    
    df = pd.DataFrame(records)
    print(f"Dataset generation complete: {len(df)} records")
    
    return df


def main():
    """Main function to generate and save the clean dataset."""
    # Generate dataset
    df = generate_dataset(num_records=200)
    
    # Save to processed data directory
    output_path = "data/processed/internships_clean.csv"
    df.to_csv(output_path, index=False)
    print(f"\nClean dataset saved to: {output_path}")
    
    # Print statistics
    print("\n=== Dataset Statistics ===")
    print(f"Total records: {len(df)}")
    print(f"\nDomain distribution:")
    print(df["Domain"].value_counts())
    print(f"\nLocation distribution:")
    print(df["Location"].value_counts())
    print(f"\nMode distribution:")
    print(df["Mode"].value_counts())
    print(f"\nStatus distribution:")
    print(df["Status"].value_counts())
    
    # Display sample records
    print("\n=== Sample Records ===")
    print(df.head(3).to_string())


if __name__ == "__main__":
    main()
