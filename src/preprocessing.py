"""
Skill normalization and preprocessing utilities.
"""

import re
from typing import Dict, List, Set


# Skill alias dictionary for normalization
SKILL_ALIASES: Dict[str, str] = {
    # ML/AI
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "nlp": "natural language processing",
    "dl": "deep learning",
    "cv": "computer vision",
    
    # Web Development
    "js": "javascript",
    "reactjs": "react",
    "react.js": "react",
    "nodejs": "node.js",
    "node.js": "node.js",
    "node": "node.js",
    "vuejs": "vue",
    "vue.js": "vue",
    "angularjs": "angular",
    "angular.js": "angular",
    
    # Databases
    "mongo": "mongodb",
    "mysql": "mysql",
    "postgres": "postgresql",
    "psql": "postgresql",
    
    # Languages
    "python3": "python",
    "py": "python",
    "c++": "cpp",
    "c#": "csharp",
    "ts": "typescript",
    
    # Cloud/DevOps
    "aws": "amazon web services",
    "gcp": "google cloud platform",
    "azure": "microsoft azure",
    "k8s": "kubernetes",
    "kubes": "kubernetes",
    
    # Tools
    "gitlab": "git",
    "github": "git",
    "jira": "agile",
    "trello": "agile",
    
    # Data
    "pandas": "pandas",
    "numpy": "numpy",
    "sklearn": "scikit-learn",
    "scikit": "scikit-learn",
    "tf": "tensorflow",
    "pytorch": "pytorch",
    "torch": "pytorch",
}


def normalize_skill(skill: str) -> str:
    """
    Normalize a single skill string.
    
    Args:
        skill: Raw skill string
        
    Returns:
        Normalized skill string
    """
    if not skill:
        return ""
    
    # Remove extra whitespace
    skill = skill.strip()
    
    # Convert to lowercase
    skill_lower = skill.lower()
    
    # Check if alias exists
    if skill_lower in SKILL_ALIASES:
        return SKILL_ALIASES[skill_lower]
    
    # Title case for display
    return skill.title()


def normalize_skills(skills_string: str) -> str:
    """
    Normalize a comma-separated skills string.
    
    Args:
        skills_string: Raw skills string (e.g., "Python, ML, ReactJS")
        
    Returns:
        Normalized skills string (e.g., "Python, Machine Learning, React")
    """
    if not skills_string:
        return ""
    
    # Split by comma
    skills = [s.strip() for s in skills_string.split(",")]
    
    # Normalize each skill
    normalized_skills = [normalize_skill(s) for s in skills if s.strip()]
    
    # Remove duplicates while preserving order
    seen: Set[str] = set()
    unique_skills = []
    for skill in normalized_skills:
        if skill.lower() not in seen:
            seen.add(skill.lower())
            unique_skills.append(skill)
    
    return ", ".join(unique_skills)


def extract_skills_from_text(text: str) -> List[str]:
    """
    Extract skills from free-form text using keyword matching.
    
    Args:
        text: Free-form text description
        
    Returns:
        List of extracted skills
    """
    if not text:
        return []
    
    text_lower = text.lower()
    found_skills = []
    
    # Check for known aliases and normalized forms
    for alias, normalized in SKILL_ALIASES.items():
        if alias in text_lower:
            if normalized not in found_skills:
                found_skills.append(normalized)
    
    # Also check for normalized forms directly
    for normalized in set(SKILL_ALIASES.values()):
        if normalized in text_lower:
            if normalized not in found_skills:
                found_skills.append(normalized)
    
    return found_skills


def clean_skill_string(skills_string: str) -> str:
    """
    Clean and standardize a skills string.
    
    Args:
        skills_string: Raw skills string
        
    Returns:
        Cleaned skills string
    """
    if not skills_string:
        return ""
    
    # Remove special characters except commas and hyphens
    cleaned = re.sub(r'[^\w\s,-]', ' ', skills_string)
    
    # Normalize whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned)
    
    # Normalize skills
    return normalize_skills(cleaned)


def get_skill_domain(skill: str) -> str:
    """
    Categorize a skill into a domain.
    
    Args:
        skill: Normalized skill name
        
    Returns:
        Domain category
    """
    skill_lower = skill.lower()
    
    domain_mapping = {
        "Web Development": ["html", "css", "javascript", "react", "angular", "vue", "node.js", "django", "flask", "spring boot"],
        "Data Science": ["python", "pandas", "numpy", "scikit-learn", "r", "sql", "excel", "tableau", "power bi"],
        "Machine Learning": ["machine learning", "tensorflow", "pytorch", "deep learning", "nlp", "computer vision"],
        "Cloud/DevOps": ["aws", "azure", "gcp", "docker", "kubernetes", "devops", "ci/cd", "jenkins", "linux", "bash"],
        "Mobile Development": ["android", "ios", "kotlin", "swift", "flutter", "react native", "firebase"],
        "Cybersecurity": ["cybersecurity", "networking", "firewalls", "penetration testing", "ethical hacking"],
        "IoT": ["iot", "arduino", "raspberry pi", "sensors", "embedded systems"],
        "Data Analysis": ["data analysis", "statistics", "data visualization", "analytics"],
    }
    
    for domain, domain_skills in domain_mapping.items():
        if any(ds in skill_lower for ds in domain_skills):
            return domain
    
    return "General"
